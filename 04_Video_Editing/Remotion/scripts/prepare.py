"""
Prepare the Remotion engine to enhance one video.

Copies a target video's images + narration into the engine's public/ folder and
generates src/data/timeline.json + src/data/config.json from that video's editing
metadata. After this runs, `npx remotion render Enhanced <out>` produces the
zoom-panned video (subtitles come from transcribe.py, music is wired via --music).

Usage:
    python scripts/prepare.py --video "<path to Videos/[Topic]>" [--fps 25]
                              [--music "<path to a music file>"] [--music-volume 0.14]

Timeline source (in priority order):
    1. <video>/Editing/images.txt  (ffmpeg concat list with `duration` lines) — the
       authoritative beat-aligned timing the pipeline already produced.
    2. Fallback: every PNG in <video>/Generated_Images sorted by name, each shown for
       an equal slice of the narration duration (needs a readable narration length).
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
PUBLIC = ENGINE / "public"
DATA = ENGINE / "src" / "data"


def log(msg):
    print(msg, flush=True)


def find_narration(video: Path):
    audio = video / "Audio"
    if not audio.is_dir():
        return None
    # Prefer a clean narration file; accept common names/extensions.
    prefs = ["narration.wav", "Narration.wav", "narration.mp3", "Narration.mp3"]
    for name in prefs:
        p = audio / name
        if p.is_file():
            return p
    # Otherwise, first file that looks like narration.
    for p in sorted(audio.iterdir()):
        if p.is_file() and "narration" in p.name.lower():
            return p
    return None


def wav_duration_seconds(path: Path):
    try:
        with wave.open(str(path), "rb") as w:
            return w.getnframes() / float(w.getframerate())
    except Exception:
        return None


def audio_duration_seconds(path: Path):
    """Duration for any audio file: native wave for .wav, else ffprobe. None if unknown."""
    if path.suffix.lower() == ".wav":
        d = wav_duration_seconds(path)
        if d:
            return d
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None
    try:
        out = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, timeout=30,
        ).stdout.strip()
        return float(out) if out else None
    except Exception:
        return None


def scenes_from_images_txt(images_txt: Path):
    lines = [l.strip() for l in images_txt.read_text(encoding="utf-8").splitlines() if l.strip()]
    pairs = []
    i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("file "):
            m = re.search(r"([^/\\']+\.(?:png|jpe?g))'?\s*$", l, re.IGNORECASE)
            if m and i + 1 < len(lines) and lines[i + 1].startswith("duration"):
                pairs.append((m.group(1), float(lines[i + 1].split()[1])))
                i += 2
                continue
        i += 1
    # Drop the trailing duplicate the ffmpeg concat trick appends.
    if len(pairs) >= 2 and pairs[-1][0] == pairs[-2][0]:
        pairs = pairs[:-1]
    return pairs


def scenes_from_glob(video: Path, narration: Path | None):
    gen_dir = video / "Generated_Images"
    imgs = sorted(
        p for p in glob.glob(str(gen_dir / "*"))
        if os.path.splitext(p)[1].lower() in (".png", ".jpg", ".jpeg")
    )
    if not imgs:
        return []
    dur = None
    if narration and narration.suffix.lower() == ".wav":
        dur = wav_duration_seconds(narration)
    per = (dur / len(imgs)) if dur else 8.0
    if not dur:
        log("  ! No images.txt and narration length unknown (mp3) — defaulting to 8.0s/image.")
        log("    For exact timing, run the ffmpeg pipeline first so Editing/images.txt exists.")
    return [(os.path.basename(p), per) for p in imgs]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True, help="Path to Videos/[Topic] folder")
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--width", type=int, default=1920, help="Output canvas width (fixed 16:9)")
    ap.add_argument("--height", type=int, default=1080, help="Output canvas height (fixed 16:9)")
    ap.add_argument("--music", default=None, help="Optional path to a music file to use")
    ap.add_argument("--music-volume", type=float, default=0.01)
    args = ap.parse_args()

    video = Path(args.video).resolve()
    if not video.is_dir():
        log(f"ERROR: video folder not found: {video}")
        sys.exit(1)

    fps = args.fps
    gen = video / "Generated_Images"
    if not gen.is_dir():
        log(f"ERROR: no Generated_Images/ in {video}")
        sys.exit(1)

    narration = find_narration(video)
    if not narration:
        log(f"ERROR: no narration audio found in {video / 'Audio'}")
        sys.exit(1)

    # Build scene list.
    images_txt = video / "Editing" / "images.txt"
    if images_txt.is_file():
        log(f"Timeline from {images_txt}")
        pairs = scenes_from_images_txt(images_txt)
    else:
        log("No Editing/images.txt — falling back to Generated_Images glob.")
        pairs = scenes_from_glob(video, narration)
    if not pairs:
        log("ERROR: could not determine any scenes.")
        sys.exit(1)

    # Reset public asset dirs.
    for sub in ("images", "audio"):
        d = PUBLIC / sub
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)

    # Copy images (only those referenced) and determine dimensions from the first.
    missing = []
    for f, _ in pairs:
        src = gen / f
        if src.is_file():
            shutil.copy2(src, PUBLIC / "images" / f)
        else:
            missing.append(f)
    if missing:
        log(f"WARNING: {len(missing)} images referenced but not found, e.g. {missing[:3]}")

    # Frame-accurate cumulative rounding so total stays aligned to the audio.
    boundaries = [0]
    cum = 0.0
    for _, d in pairs:
        cum += d
        boundaries.append(round(cum * fps))
    scenes = []
    for idx, (f, _) in enumerate(pairs):
        frames = boundaries[idx + 1] - boundaries[idx]
        if frames > 0 and (PUBLIC / "images" / f).is_file():
            scenes.append({"file": f"images/{f}", "durationInFrames": frames})
    total_frames = boundaries[-1]

    # Timing sanity: warn if the scene track and narration diverge by > 0.75s.
    # Catches a malformed images.txt (e.g. a missing `duration` line silently
    # dropping the final scene and truncating the narration tail).
    narr_dur = audio_duration_seconds(narration)
    if narr_dur:
        drift = total_frames / fps - narr_dur
        if abs(drift) > 0.75:
            log(f"WARNING: scene track is {total_frames / fps:.1f}s but narration is "
                f"{narr_dur:.1f}s ({drift:+.1f}s). Check Editing/images.txt — a scene may be "
                f"mistimed or dropped (missing `duration` line?).")

    # Copy narration.
    narr_ext = narration.suffix.lower()
    narr_name = f"narration{narr_ext}"
    shutil.copy2(narration, PUBLIC / "audio" / narr_name)

    # Optional music.
    music_rel = None
    if args.music:
        mp = Path(args.music).resolve()
        if mp.is_file():
            music_name = f"music{mp.suffix.lower()}"
            shutil.copy2(mp, PUBLIC / "audio" / music_name)
            music_rel = f"audio/{music_name}"
            log(f"Music: {mp.name} -> {music_rel}")
        else:
            log(f"WARNING: --music path not found: {mp}")

    # Fixed 16:9 output canvas. KenBurns uses objectFit:cover, so source images
    # (any near-16:9 size) fill this without letterboxing. Standard is 1920x1080.
    width, height = args.width, args.height

    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "timeline.json").write_text(
        json.dumps(
            {"fps": fps, "width": width, "height": height, "totalFrames": total_frames, "scenes": scenes},
            indent=2,
        ),
        encoding="utf-8",
    )
    (DATA / "config.json").write_text(
        json.dumps(
            {"narration": f"audio/{narr_name}", "music": music_rel, "musicVolume": args.music_volume},
            indent=2,
        ),
        encoding="utf-8",
    )

    log("")
    log(f"Prepared: {len(scenes)} scenes, {total_frames} frames "
        f"({total_frames / fps:.1f}s) @ {fps}fps, {width}x{height}")
    log(f"Narration: {narration.name}")
    log(f"Next: python scripts/transcribe.py  (captions)  then  npx remotion render Enhanced <out.mp4>")


if __name__ == "__main__":
    main()

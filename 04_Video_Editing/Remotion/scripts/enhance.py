"""
One-shot orchestrator: enhance a video's body in a single command.

Runs prepare -> transcribe -> render end to end so the assembly pipeline can call
ONE command instead of a multi-step, token-spending reasoning loop. Deterministic:
it never calls any AI/MCP service. Music is only added if you pass --music (reuse an
existing track); generating a new track is a separate, explicit action.

Produces the enhanced BODY video (motion + narration + music + animated subtitles).
Prepending the channel intro stays a separate step (see FFmpeg_Pipeline.md Step 7),
because that step has "is the intro present?" judgment checks worth keeping explicit.

Usage:
    python scripts/enhance.py --video "<path to Videos/[Topic]>" \
        [--music "<track>"] [--no-subs] [--model small.en] [--crf 18] \
        [--fps 25] [--width 1920] [--height 1080] [--music-volume 0.01] [--out "<file.mp4>"]

Exit code is non-zero if any stage fails, so the caller can stop the pipeline.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
SCRIPTS = ENGINE / "scripts"
DATA = ENGINE / "src" / "data"


def run(cmd, **kw):
    print(f"\n$ {cmd if isinstance(cmd, str) else ' '.join(map(str, cmd))}", flush=True)
    r = subprocess.run(cmd, cwd=str(ENGINE), **kw)
    if r.returncode != 0:
        print(f"FAILED (exit {r.returncode})", flush=True)
        sys.exit(r.returncode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--music", default=None)
    ap.add_argument("--no-subs", action="store_true")
    ap.add_argument("--model", default="small.en")
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--music-volume", type=float, default=0.01)
    ap.add_argument("--out", default=None)
    ap.add_argument("--frames", default=None, help="Frame range to render, e.g. 0-250 (preview/testing)")
    args = ap.parse_args()

    video = Path(args.video).resolve()
    topic = video.name
    out = Path(args.out).resolve() if args.out else (video / "Editing" / f"{topic}_enhanced_body.mp4")
    out.parent.mkdir(parents=True, exist_ok=True)

    py = sys.executable

    # 1) Prepare assets + timeline (+ music copy if provided).
    prep = [py, str(SCRIPTS / "prepare.py"), "--video", str(video),
            "--fps", str(args.fps), "--width", str(args.width), "--height", str(args.height),
            "--music-volume", str(args.music_volume)]
    if args.music:
        prep += ["--music", str(args.music)]
    run(prep)

    # 2) Subtitles: transcribe, or blank the captions file when off.
    if args.no_subs:
        (DATA / "captions.json").write_text("[]", encoding="utf-8")
        print("Subtitles off — captions blanked.", flush=True)
    else:
        run([py, str(SCRIPTS / "transcribe.py"), "--model", args.model])

    # 3) Render the enhanced body. npx resolves the bundled Remotion CLI + ffmpeg.
    npx = "npx.cmd" if sys.platform.startswith("win") else "npx"
    render_cmd = [npx, "remotion", "render", "Enhanced", str(out), "--codec=h264", f"--crf={args.crf}"]
    if args.frames:
        render_cmd.append(f"--frames={args.frames}")
    run(render_cmd, shell=sys.platform.startswith("win"))

    fps = json.loads((DATA / "timeline.json").read_text(encoding="utf-8")).get("fps", args.fps)
    print(f"\nDONE. Enhanced body -> {out}", flush=True)
    print(f"Next: prepend the intro (FFmpeg_Pipeline.md Step 7) to produce Publish/{topic}.mp4",
          flush=True)


if __name__ == "__main__":
    main()

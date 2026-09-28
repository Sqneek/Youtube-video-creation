"""
Transcribe the prepared narration into word-level caption timings.

Reads the narration path from src/data/config.json (written by prepare.py), runs
faster-whisper, and writes src/data/captions.json in the @remotion/captions shape
(one entry per word) that Captions.tsx consumes for the word-by-word highlight.

Run prepare.py first. Then:
    python scripts/transcribe.py [--model small.en]

Models trade speed for accuracy: tiny.en / base.en (fast) -> small.en (default,
good for clear narration) -> medium.en (slow, most accurate).
"""
import argparse
import json
from pathlib import Path

from faster_whisper import WhisperModel

ENGINE = Path(__file__).resolve().parent.parent
DATA = ENGINE / "src" / "data"
PUBLIC = ENGINE / "public"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="small.en")
    args = ap.parse_args()

    config = json.loads((DATA / "config.json").read_text(encoding="utf-8"))
    narr_rel = config.get("narration")
    if not narr_rel:
        raise SystemExit("No narration in config.json — run prepare.py first.")
    audio = PUBLIC / narr_rel
    if not audio.is_file():
        raise SystemExit(f"Narration not found: {audio}")

    print(f"loading model {args.model} ...", flush=True)
    model = WhisperModel(args.model, device="cpu", compute_type="int8")

    print(f"transcribing {audio.name} ...", flush=True)
    segments, _ = model.transcribe(str(audio), word_timestamps=True, vad_filter=True, beam_size=5)

    captions = []
    for seg in segments:
        for w in seg.words or []:
            captions.append({
                "text": w.word,
                "startMs": int(round(w.start * 1000)),
                "endMs": int(round(w.end * 1000)),
                "timestampMs": int(round((w.start + w.end) / 2 * 1000)),
                "confidence": getattr(w, "probability", None),
            })
        if captions and len(captions) % 200 == 0:
            print(f"  ...{len(captions)} words, t={seg.end:.0f}s", flush=True)

    (DATA / "captions.json").write_text(json.dumps(captions, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"DONE: {len(captions)} words -> {DATA / 'captions.json'}", flush=True)


if __name__ == "__main__":
    main()

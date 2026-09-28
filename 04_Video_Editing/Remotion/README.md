# Video Enhancer (Remotion engine)

Reusable, data-driven Remotion engine that adds **Ken Burns zoom/pan**, a **looped
music bed**, and **word-by-word animated subtitles** to a slideshow video built from
`Generated_Images/` + narration. It rebuilds from source assets (not the flattened
`Publish` MP4), so motion is per-scene and quality is preserved.

Driven by the **`enhance-video` skill** and the assembly step in
`New_Video_Workflow.md`. Both call one deterministic command — `<V>` = `Videos/[Topic]`:

```bash
# from this directory (04_Video_Editing/Remotion)
npm install && npm approve-scripts esbuild          # first time only
python scripts/enhance.py --video "<V>" [--music "<track>"] [--no-subs]
```

`enhance.py` runs prepare → transcribe → render in sequence and writes the enhanced
body to `<V>/Editing/[Topic]_enhanced_body.mp4`. Prepend the channel intro
(`FFmpeg_Pipeline.md` Step 7) to produce the final `Publish/[Topic].mp4`.

Run the stages by hand only when debugging:

```bash
python scripts/prepare.py --video "<V>" --fps 25 [--music "<track>"]
python scripts/transcribe.py --model small.en       # subtitle timing (slow)
npx remotion studio                                 # live preview
npx remotion render Enhanced "<out>.mp4" --codec=h264 --crf=18
```

Everything per-video is regenerated into `src/data/*.json` and `public/` by
`prepare.py` / `transcribe.py`, so those start empty/stubbed. Tuning knobs:
`src/KenBurns.tsx` (motion), `src/Captions.tsx` (subtitle look), `--music-volume`.

Requires Node, and Python + `faster-whisper` for subtitles. ffmpeg ships with Remotion.

Runs locally via Claude Code — not from a Cowork/cloud sandbox.

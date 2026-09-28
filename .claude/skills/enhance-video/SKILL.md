---
name: enhance-video
description: >-
  Adds cinematic motion, music, and animated subtitles to a specific finished
  slideshow video in this Video Generator project. Use this when the user points at
  an existing Videos/[Topic]/ video and asks to "enhance" it, or asks for any of:
  Ken Burns / zoom / pan / "make the images move" / "the stills feel static";
  background or custom MUSIC under the narration; or animated / word-by-word /
  karaoke / burned-in SUBTITLES that match the narration — even if they name only
  one of the three. It runs the deterministic enhance.py orchestrator (one command),
  not a step-by-step loop. Do NOT trigger it during a normal new-video build — the
  assembly step in New_Video_Workflow.md already invokes enhance.py at the right
  time; this skill is for enhancing an already-existing video on request. Not for
  generating a new video (that's new-video) or plain ffmpeg edits with no
  motion/music/subtitles.
---

# Enhance Video (one-command)

Rebuilds a video's body from its source assets with per-scene Ken Burns zoom/pan, a
looped music bed under the narration, and word-by-word highlighted subtitles. The
whole thing is a single deterministic script — run it, don't hand-run the stages.

Engine + scripts live at `04_Video_Editing/Remotion/`. `<V>` = the target
`Videos/[Topic]` folder (must contain `Generated_Images/` and a narration file in
`Audio/`; exact timing comes from `Editing/images.txt` if present).

## Steps (keep it lean — this should cost few tokens)

1. **Confirm the target video** if it isn't obvious from the request.

2. **Ask the one music question** (the only interactive point):
   generate a new track, reuse an existing one, or none.
   - *Generate*: call `vidiq_generate_music` (instrumental prompt fitting the tone,
     `durationSeconds: 180`; it loops to full length), poll `vidiq_job_poll` until
     `completed`, download the `audioUrl` with `curl -sL`, verify/rename via
     `npx remotion ffprobe` (it's often an MP3). This costs credits — only on request.
   - *Reuse*: a track in `<V>/Audio/` or `04_Video_Editing/Assets/Music/`.
   - *None*: pass nothing.

3. **Run the orchestrator** (from `04_Video_Editing/Remotion/`):
   ```bash
   python scripts/enhance.py --video "<V>" [--music "<track>"] [--no-subs]
   ```
   It runs prepare → transcribe → render and prints the output path. Don't render
   test stills or babysit stages unless it actually errors — the pipeline is proven.

4. **Prepend the intro** to make the final deliverable: follow
   `04_Video_Editing/FFmpeg_Pipeline.md` Step 7 on the enhanced body, output to
   `<V>/Publish/[Topic].mp4` (or `[Topic]_enhanced.mp4` if preserving the original).
   Use the **system ffmpeg** for the concat, not the Remotion-bundled wrapper (it
   mangles `;`/`setsar` filter strings). Body is fixed 1920×1080@25; intro conforms to it.

5. **Report** the output path and offer the tuning knobs below.

## If a prerequisite is missing
- No `04_Video_Editing/Remotion/node_modules`: `npm install` there, then
  `npm approve-scripts esbuild`.
- `faster-whisper` import fails: `python -m pip install faster-whisper` (or run
  `--no-subs`). ffmpeg ships with Remotion — never install it separately.
- vidIQ MCP not connected: offer reuse/none instead of generating.

## Tuning knobs (edit, re-run enhance.py — no other change)
- Music level: `--music-volume` (default 0.01).
- Subtitle look: `src/Captions.tsx` (`ACCENT` color, `fontSize`, position).
- Zoom style: `src/KenBurns.tsx` `MOVES` (keep scale ≥ ~1.08 so pans don't expose black).
- Resolution: fixed **1920×1080** via `--width/--height` (KenBurns cover-fills; sub-1080 source images upscale — generate at 1920×1080 for real detail).
- Render size/quality: `--crf` (18 master; 21 ≈ 1/3 size, no visible loss).

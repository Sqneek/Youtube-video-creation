# FFmpeg Assembly Pipeline

Turns a folder of scene images + a narration track + (optional) music/captions into a finished video. No GUI editor — everything is scripted so it's repeatable per video.

> **This doc handles timing (Step 1) and the intro (Step 7). The body itself is built by the Remotion enhancer** — hand this command to the user to run locally in Claude Code, from `04_Video_Editing/Remotion/`:
> `python scripts/enhance.py --video "Videos/[Topic_Name]" [--music "<track>"] [--no-subs]`
> Wait for the enhanced body file, then continue to Step 7. Steps 2–6 below are kept as a plain-ffmpeg fallback. See `04_Video_Editing/Remotion/README.md`.

## Inputs expected per video

Everything lives in `Videos/[Topic_Name]/` — work from there directly:

- `Audio/narration.mp3` (no `.srt` — Grok doesn't produce timestamps)
- `Generated_Images/` — the scene images, named per the prompt batch's Filename column (e.g. `01_hook-close-trenches.png`, `02_singing-carries-across.png`, ...). The two-digit numeric prefix keeps them in script order for the concat step below.
- Optional background music track, pulled in from the shared `04_Video_Editing/Assets/Music/` library
- The channel intro, pulled from the shared `04_Video_Editing/Assets/Intro/intro.mp4` — a fixed, reusable clip (animated logo + personal spoken greeting, ~4-6s) that's the same across every video. It's a self-contained file with its own baked-in audio, provided directly by the user — never generated or edited per video. If it's missing, flag that to the user before Step 7 rather than shipping without it.
- Working/intermediate files for this step go in `Videos/[Topic_Name]/Editing/`

## Step 1 — Time each image to the narration

If you have exact per-scene durations from the script/prompt batch, skip to Step 2. Otherwise, use the word-count-based per-beat duration estimate from `03_Voice_Over/TTS_Setup_Guide.md` (no `.srt` is available). For a single flat scale factor instead of per-beat estimation, a quick even-split approach:

```bash
# Get narration duration in seconds
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 narration.mp3)
# Divide by number of images to get seconds-per-image, then build a concat file (Step 2)
```

**If the user flags that image timing feels out of sync with the narration**, ask before applying a fix — do not do this automatically. If approved, anchor durations per script beat instead of one flat scale factor, using the word-count-based per-beat duration estimate from `03_Voice_Over/TTS_Setup_Guide.md`, then distribute each beat's images proportionally *within that beat's estimated time window*.

## Step 2 — Build a concat file with per-image durations (Ken Burns optional)

Create `images.txt` (using each image's assigned filename from the prompt batch):
```
file '01_hook-close-trenches.png'
duration 5.2
file '02_singing-carries-across.png'
duration 4.8
file '03_shouted-proposal.png'
duration 6.0
file '03_shouted-proposal.png'
```
(Note: ffmpeg's concat demuxer requires the last file listed twice — a known quirk — without a trailing duration.)

**Static images, simple crossfade-free assembly:**
```bash
ffmpeg -f concat -safe 0 -i images.txt -vsync vfr -pix_fmt yuv420p images_only.mp4
```

**With a subtle Ken Burns (slow zoom) effect per image**, use `zoompan` per input instead of concat — for a single image example:
```bash
ffmpeg -loop 1 -i "01_hook-close-trenches.png" -t 5.2 -vf "scale=3840:2160,zoompan=z='min(zoom+0.0015,1.1)':d=125:s=1920x1080:fps=25" -c:v libx264 -pix_fmt yuv420p 01_hook-close-trenches.mp4
```
Repeat per image, then concat the resulting per-image `.mp4` clips with the same concat-demuxer approach (no durations needed this time, since duration is baked in).

## Step 3 — Mux narration onto the image track

```bash
ffmpeg -i images_only.mp4 -i narration.mp3 -c:v copy -c:a aac -b:a 192k -shortest video_with_narration.mp4
```

## Step 4 — Add background music, ducked under narration

```bash
ffmpeg -i video_with_narration.mp4 -i music.mp3 -filter_complex \
"[1:a]volume=0.15[music]; [0:a][music]amix=inputs=2:duration=first:dropout_transition=2[aout]" \
-map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k video_with_music.mp4
```
Adjust `volume=0.15` to taste — music should sit well under narration, not compete.

## Step 5 — Burn in captions (optional)

Ask the user whether they want burned-in captions for this video before running this step. If not, skip straight to Step 6 using `video_with_music.mp4` in place of `final.mp4`.

Grok produces no `.srt`, so if captions are wanted, first generate one by transcribing `narration.mp3` (e.g. via a Whisper-based transcription tool), then burn it in:

```bash
ffmpeg -i video_with_music.mp4 -vf "subtitles=narration.srt:force_style='FontName=Arial,FontSize=22,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=2'" -c:a copy final.mp4
```

## Step 6 — Final export settings for YouTube

```bash
ffmpeg -i final.mp4 -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart final_youtube.mp4
```
`-crf 18` is visually near-lossless; drop to `-crf 20`–`23` if file size matters more than max quality. `-movflags +faststart` makes it stream-ready on upload.

## Step 7 — Prepend the channel intro

Runs after the enhanced body is built, on that body file (narration, music, captions baked in). The intro clip carries its own audio (voiceover + logo sound) and must not be muxed with the body's narration/music track — this is a straight concatenation of two already-finished clips, not another audio mix.

> **Use the system ffmpeg for this step, not the Remotion-bundled one.** The wrapper (`node_modules/.bin/remotion ffmpeg`) mangles filter strings — it rejects `;` chains and `setsar=1` — so filter_complex concats fail through it. Call the real binary directly (`ffmpeg` on PATH, e.g. the Gyan build). ffprobe via the wrapper is fine.

The enhanced body is a **fixed 1920×1080 @ 25fps** canvas (set in `scripts/prepare.py`). The channel intro is natively 1920×1080 @ 30fps, so normalization is just an fps conversion (adjust if your own intro's native resolution/fps differs).

1. Confirm `04_Video_Editing/Assets/Intro/intro.mp4` exists. If it's missing, tell the user and hold off — don't ship a video without checking first.
2. Confirm the body is 1920×1080 (it is, unless `--width/--height` were overridden):
   ```bash
   ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "<V>/Editing/[Topic]_enhanced_body.mp4"
   ```
3. Normalize the intro to 1920×1080 @ 25fps (never touch the body — the intro is the asset being conformed). Plain `scale` is enough since both are already 16:9; avoid `pad`/`setsar` in this pass — some ffmpeg builds choke on the expression:
   ```bash
   ffmpeg -y -i intro.mp4 -vf "scale=1920:1080" -r 25 -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k "<V>/Editing/intro_normalized.mp4"
   ```
4. Concatenate intro + body. Force matching pixel format / fps / SAR inside the graph — a raw concat can silently drop packets on a pixel-format mismatch between clips (e.g. `yuvj420p` pc-range vs `yuv420p` tv-range):
   ```bash
   ffmpeg -y -i "<V>/Editing/intro_normalized.mp4" -i "<V>/Editing/[Topic]_enhanced_body.mp4" -filter_complex \
   "[0:v]format=yuv420p,fps=25,setsar=1[v0];[1:v]format=yuv420p,fps=25,setsar=1[v1];[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[outv][outa]" \
   -map "[outv]" -map "[outa]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "<V>/Publish/[Topic].mp4"
   ```
5. `Publish/[Topic].mp4` is the true final deliverable.

## Notes

- Keep all intermediate files (`images_only.mp4`, `video_with_narration.mp4`, etc.) in `Videos/[Topic_Name]/Editing/` until final export is confirmed good — re-running only the failed step is much faster than redoing the whole chain.
- The finished, final export (post-intro, from Step 7) gets renamed and placed directly in `Videos/[Topic_Name]/Publish/[Topic_Name].mp4` — sitting right alongside the research, script, prompts, and audio for that same video, not in a separate folder.

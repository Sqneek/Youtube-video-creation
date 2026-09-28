# Creating a New Video

This is the intake flow that runs at the start of every new video. Five questions, asked up front, before any research or writing starts.

## The 5 intake questions

1. **Topic** — what is this video about? (User provides one, or asks Claude to propose a few options.)
   **Scheduled/autonomous pipeline exception**: the topic is picked automatically — check
   `00_Project_Overview/Topics_Covered.md`, pick something in the established niche not already
   listed there, and append it to that file's Log immediately, before research starts.
2. **Length** — target runtime (e.g. "90 seconds", "8-10 minutes", "15-20 minutes"). Drives script word count (~150 words/minute) and scene count.
3. **Number of images** — how many scenes/images to break the script into, or a target seconds-per-image pace. Default guidance if unsure: roughly one image per 6-8 seconds of narration.
4. **Visual style** — Style A (Flat Vector) or Style B (Simple Sketch)? See `00_Project_Overview/README.md` for what each looks like.
5. **Voiceover** — Grok TTS (voice chosen by the user directly in Grok) or a personal voice-over recording. See `03_Voice_Over/TTS_Setup_Guide.md` for both the manual handoff and the automated device-bound method.

Ask all five before starting research/scripting in an interactive session — don't assume defaults silently. For the scheduled/autonomous pipeline, use the established defaults already locked in for this channel (same style, same length range, same image pacing as prior videos) unless the user has changed them.

## One folder per video — everything lives together

As soon as a topic is confirmed, create `Videos/[Topic_Name]/` and immediately scaffold the **entire** folder skeleton below — all subfolders, not just the one needed for the step you're about to do. Create `Generated_Images/`, `Audio/`, `Editing/`, and `Publish/` up front, even though they'll sit empty until their pipeline step runs. Don't create folders lazily one step at a time — that leaves the project structure incomplete if the pipeline pauses at a checkpoint. Nothing about a specific video gets filed into `01_Research_and_Script/`, `02_Image_Prompts/`, `03_Voice_Over/`, or `04_Video_Editing/` — those four folders hold only the reusable systems (style guides, setup docs, templates), never per-video content.

```
Videos/[Topic_Name]/
  Research_Notes.md
  Script.md                  (annotated with scene/beat labels)
  Narration.txt              (clean, narration-only — ready for TTS)
  Image_Prompt_Batch.md      (scene table with filenames + Flow prompts)
  Generated_Images/          (images downloaded from Google Flow, renamed per the batch)
  Audio/                     (narration.mp3, + music if used — no .srt)
  Editing/                   (FFmpeg/Remotion intermediate/working files; also where the
                              READY_FOR_ASSEMBLY.txt / DONE_ASSEMBLY.txt / FAILED_ASSEMBLY.txt
                              handoff markers live for the scheduled pipeline — see Step 5)
  Publish/
    [Topic_Name].mp4         (the finished video — final deliverable)
    Thumbnail.png
    Description.txt
```

## Pipeline after intake

1. **Research** — write `Videos/[Topic_Name]/Research_Notes.md`, following the process in `01_Research_and_Script/Research_Workflow.md`.
2. **Script** — write `Videos/[Topic_Name]/Script.md` (annotated) and `Narration.txt` (clean), sized to the requested length, following `01_Research_and_Script/Script_Style_Guide.md`.
3. **Image prompts** — break the script into the requested number of scenes, write `Videos/[Topic_Name]/Image_Prompt_Batch.md` following `02_Image_Prompts/Image_Style_Guide.md` and the naming convention in `02_Image_Prompts/Batch_Template.md`. Open the Flow project matching the style chosen at intake — "Footnotes Image Creation" for Style A, "Footnote image creator. S2" for Style B — and follow that style's file under `02_Image_Prompts/Styles/`. Each prompt must match the exact line of narration it sits next to (not a generic beat-level mood shot), and the batch must be scanned for repeated shot types/subject setups before it's considered done — see "Script relevance and scene variety" in `Image_Style_Guide.md`. Claude generates the images in Google Flow using chrome browser tools — following `02_Image_Prompts/Flow_Automation_Technique.md` exactly — renames each to its assigned filename, and drops them into `Videos/[Topic_Name]/Generated_Images/`.
4. **Voiceover** — per `03_Voice_Over/TTS_Setup_Guide.md`: use the automated method (Method A) when the session is device-bound with Chrome logged into the xAI/Grok account, otherwise hand `Narration.txt` to the user for Grok generation and wait for `narration.mp3` in `Videos/[Topic_Name]/Audio/`. Either way, listen through and align beats per that guide before continuing.
5. **Assembly** — the render itself (`scripts/enhance.py` + intro prepend) needs native Windows Node/Chrome and cannot run inside any Cowork/cloud sandbox, device-bound or not. Two paths:
   - **Interactive session**: hand off a single command; the user runs it locally in Claude Code and it produces the finished, intro-prepended video without further involvement from this side. Working files land in `Videos/[Topic_Name]/Editing/`.
     - Make sure per-scene timing exists first: `Videos/[Topic_Name]/Editing/images.txt` (produced per `FFmpeg_Pipeline.md` Step 1). The enhancer reads its durations.
     - **Music — ask once**: generate a new track (vidIQ music tool — costs credits), reuse an existing one from `04_Video_Editing/Assets/Music/`, or none.
     - **Hand off this command** for the user to paste into a local Claude Code session, from `04_Video_Editing/Remotion/`:
       `python scripts/enhance.py --video "Videos/[Topic_Name]" [--music "<track>"] [--no-subs]`
       Local Claude Code runs this end to end — body render (Ken Burns zoom/pan, music mixed under narration, word-by-word subtitles by default; `--no-subs` to skip — see `04_Video_Editing/Remotion/README.md`) followed by the intro prepend (`04_Video_Editing/Assets/Intro/intro.mp4`, per `FFmpeg_Pipeline.md` Step 7) — landing the final file directly at `Videos/[Topic_Name]/Publish/[Topic_Name].mp4`. That's a single handoff, not two steps to babysit separately.
     - **No review needed here** — once the user confirms the command finished and the file is sitting in `Publish/`, treat that as the final edit and move straight to Step 6. Don't re-open or re-check the video from this side.
   - **Scheduled/autonomous pipeline**: build `Editing/images.txt` per `FFmpeg_Pipeline.md` Step 1, resolve the music choice (reuse an existing track from `04_Video_Editing/Assets/Music/` by default — no interactive "ask once" available), then write `Videos/[Topic_Name]/Editing/READY_FOR_ASSEMBLY.txt` (first line = the music track filename, or empty for none) and stop — do not attempt to run `enhance.py` or ffmpeg yourself in this session. A separate Windows Task Scheduler job (`04_Video_Editing/Run_Assembly.ps1`) picks up the marker on the user's PC, runs the same deterministic render + intro-prepend, and writes `DONE_ASSEMBLY.txt` (success) or `FAILED_ASSEMBLY.txt` (with the error) next to it. A later scheduled run checks for that marker before continuing a given video to Step 6 — see `Run_Assembly.ps1`'s header comment for the exact contract.
6. **Thumbnail** — generate 3-4 concept options via vidIQ (`vidiq_generate_thumbnail`). In an interactive session, present them to the user as a chooser; in the scheduled pipeline, pick the strongest option yourself (state your reasoning in the run report) rather than blocking on a choice. Save the chosen image to `Videos/[Topic_Name]/Publish/Thumbnail.png` and proceed directly to Step 7.
7. **Title & Description** — generate 3-4 title options via vidIQ (`vidiq_generate_titles`). In an interactive session, present them to the user as a chooser; in the scheduled pipeline, pick the strongest option yourself (state your reasoning in the run report). Write the compact description (1-2 sentences on what the video's about — no chapters, sources, unless asked), save both to `Videos/[Topic_Name]/Publish/Description.txt`, and proceed directly to Step 8.
8. **Delivery** — finished video saved as `Videos/[Topic_Name]/Publish/[Topic_Name].mp4`, alongside the thumbnail and description. The whole project — research, script, prompts, images, audio, and the publish-ready bundle — stays together in that one folder. **Never upload/publish to YouTube automatically, regardless of pipeline mode** — that step always waits for the user's explicit go-ahead.
   - **Best time to post** — run `vidiq_subscriber_insights` on the channel and report the top 2-3 highest-activity windows (adjusted to the user's local timezone) before they publish. This is a recommendation only — the user decides whether to schedule against it or publish on their own timing.

## Checkpoints

Don't run the whole pipeline unattended end to end by default — confirm with the user after script + image prompt batch are ready, before spending time on TTS/assembly, unless they've said to just run straight through.

**Explicit, deliberate exception**: the scheduled/autonomous pipeline (see `CLAUDE.md` → "Scheduled/autonomous pipeline") runs straight through every step without pausing for confirmation, by the user's explicit request — every run instead sends an email report afterward (what got done, what's blocked, a contact sheet of generated images for visual QA) so review happens after the fact rather than blocking mid-run. This exception applies only to that scheduled task, never to an interactive session unless the user says otherwise in that session.

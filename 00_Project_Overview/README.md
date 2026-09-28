# YouTube Content Engine — History Channel

A folder-based pipeline that turns a topic into a finished video: research → script → image prompts → voiceover → assembly → thumbnail → publish-ready description. Four reusable systems handle the mechanics; every individual video gets its own self-contained project folder.

## Quick start

Starting a new video? Say so, and the intake flow kicks in: topic, length, image count, voiceover choice. Full steps: `00_Project_Overview/New_Video_Workflow.md`.

## Folder map

| Folder | Contents |
|---|---|
| `01_Research_and_Script/` | Reusable — script style guide + research process |
| `02_Image_Prompts/` | Reusable — image style guide, batch template, reference images |
| `03_Voice_Over/` | Reusable — Grok voice-over handoff + beat-alignment guide |
| `04_Video_Editing/` | Reusable — FFmpeg pipeline doc (timing + intro), Remotion enhancer (body render), shared Music/Intro assets |
| `Videos/[Topic_Name]/` | **Per-video** — research, script, image prompts, generated images, audio, editing files, and the finished `.mp4`, all together |

`Videos/` is the only place to look for anything about a specific video. Everything in `01`–`04` is shared across all videos.

## The two things that must stay consistent

Research and FFmpeg commands are mechanical — same every time. Voice-over is a manual handoff to Grok, not a command Claude runs. Only two things carry a defined *style* that needs to hold steady video to video:

**Script style** — `01_Research_and_Script/Script_Style_Guide.md`
Locked in: History Explainer. Hooks with a question, explains context before narrative, closes on why it matters today.

**Image style** — `02_Image_Prompts/Image_Style_Guide.md` (shared mechanics) plus one of two locked per-video styles in `02_Image_Prompts/Styles/`, chosen once at intake and never mixed within a batch:
- **Style A — Flat Vector:** minimalist flat-vector characters (plain circular heads, dot eyes) against richly detailed, moody environments, desaturated palette, strong directional "god ray" lighting. Derived from reference frames; screen captions, title text, YouTube UI, and edit-layer effects were excluded on purpose.
- **Style B — Simple Sketch:** semi-realistic painted illustration — a simplified but fully clothed character (circle head, tousled hair, expressive eyebrows/eyes, cel-shaded fold lines on clothing) against fully painted, textured, atmospheric environments with moody directional lighting. Revised 2026-08-03 from an earlier flat/no-shading version; see `02_Image_Prompts/Styles/Style_B_SimpleSketch.md` for the full spec and revision note.

## Known limitation

Narration generation happens outside Claude's sandbox entirely — Claude hands off the finished script, the user generates the voice-over manually via Grok, and saves the audio back into the video's `Audio/` folder.

The Remotion body render is the same kind of handoff — it runs locally via Claude Code, not in this sandbox. Claude prepares the timing and assets, the user runs the render, and Claude picks back up once the enhanced body file exists.

## Status

- [x] Folder structure (per-video projects under `Videos/`, reusable systems in `01`–`04`)
- [x] Script Style Guide (History Explainer)
- [x] Research workflow
- [x] Voice-over setup (Grok handoff + beat-alignment check)
- [x] FFmpeg assembly pipeline
- [x] Image Style Guide (derived from reference frames)
- [x] New video intake flow (topic / length / image count / voiceover)
- [x] Channel intro asset (`04_Video_Editing/Assets/Intro/`)
- [x] Remotion body-render enhancer (Ken Burns zoom/pan, music, animated subtitles — local Claude Code handoff)

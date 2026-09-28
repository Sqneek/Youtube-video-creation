# Video Generator — History-Explainer YouTube Pipeline

A folder-based, Claude-driven pipeline that turns a topic into a finished YouTube video:
**research → script → image prompts → AI-generated images → AI voiceover → assembled video
(Ken Burns motion + music + animated subtitles) → thumbnail → title/description**, ready for
a human to review and manually publish.

This repo holds the **reusable system only** — style guides, workflow docs, and the Remotion
render engine. Per-video output (research notes, scripts, generated images, audio, finished
`.mp4` files) is intentionally **not** checked in here; each video gets its own
`Videos/[Topic_Name]/` folder locally when you actually make one (see
`00_Project_Overview/New_Video_Workflow.md`), and that folder is git-ignored.

## Start here

New to this project? Read these two in order:

1. **[INSTALLATION.md](INSTALLATION.md)** — one-time setup: accounts, dependencies, the two
   Google Flow style projects, your own binary assets (channel intro, music).
2. **[USAGE.md](USAGE.md)** — the day-to-day guide: how to start a video, what happens at each
   pipeline stage, where the checkpoints are, and how a finished video gets to `Publish/`.

Then, for the deeper reference docs behind those two guides:

3. `CLAUDE.md` — the operating rules for whoever/whatever (human or Claude) works in this repo.
4. `00_Project_Overview/README.md` — the folder map and the two things that must stay
   visually/tonally consistent video to video.
5. `00_Project_Overview/New_Video_Workflow.md` — the full intake + pipeline spec that
   `USAGE.md` summarizes.

## Layout

```
INSTALLATION.md                One-time setup guide
USAGE.md                       Day-to-day "how to use it" guide
CLAUDE.md                      Operating rules / project context for Claude
SETUP.md                       Same setup info as INSTALLATION.md, in the original reference-doc format
00_Project_Overview/           Workflow doc, topic log, folder-map README, channel branding (empty, yours to fill)
01_Research_and_Script/        Research process + script style guide
02_Image_Prompts/              Image prompt formula, batch template, Flow automation technique,
                                the two locked visual styles, reference images (empty, yours to fill)
03_Voice_Over/                 TTS setup guide (automated + manual handoff)
04_Video_Editing/               FFmpeg assembly pipeline doc, the Remotion "enhancer" render engine,
                                shared asset folders (Music/SFX/Intro — empty, yours to fill)
.claude/skills/enhance-video/  A Claude Code project skill for re-enhancing an existing video on request
```

`Videos/` and `YOUTUBE_PUBLISH/` are not in this repo (see `.gitignore`) — they hold per-video
generated content and are created locally as you actually make videos.

## License / use

Personal project scaffolding — adapt freely for your own channel.

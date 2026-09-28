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

1. Read `CLAUDE.md` — the operating rules for whoever/whatever (human or Claude) works in this repo.
2. Read `00_Project_Overview/README.md` — the folder map and the two things that must stay
   visually/tonally consistent video to video.
3. Read `00_Project_Overview/New_Video_Workflow.md` — the actual intake + pipeline steps.
4. Follow `SETUP.md` for the parts that can't live in git: accounts, the two Google Flow style
   projects, binary assets (channel intro, music), and dependency installation.

## Layout

```
CLAUDE.md                     Operating rules / project context for Claude
SETUP.md                      Everything needed to get this running on a fresh machine
00_Project_Overview/          Workflow doc, topic log, folder-map README, channel branding (empty, yours to fill)
01_Research_and_Script/       Research process + script style guide
02_Image_Prompts/             Image prompt formula, batch template, Flow automation technique,
                               the two locked visual styles, reference images (empty, yours to fill)
03_Voice_Over/                TTS setup guide (automated + manual handoff)
04_Video_Editing/             FFmpeg assembly pipeline doc, the Remotion "enhancer" render engine,
                               shared asset folders (Music/SFX/Intro — empty, yours to fill)
.claude/skills/enhance-video/ A Claude Code project skill for re-enhancing an existing video on request
```

`Videos/` and `YOUTUBE_PUBLISH/` are not in this repo (see `.gitignore`) — they hold per-video
generated content and are created locally as you actually make videos.

## License / use

Personal project scaffolding — adapt freely for your own channel.

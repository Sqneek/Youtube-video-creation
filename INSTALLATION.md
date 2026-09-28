# Installation Guide

Welcome to the Video Generator project. This is the one-time setup — do this once per machine.
Once it's running, see **[USAGE.md](USAGE.md)** for how to actually make a video with it day to day.

## What you'll need before you start

- **A Google account** with access to **Google Flow** (Google's AI image/video generation tool). You'll set up two custom Flow "projects" by hand in Step 4 below.
- **An xAI/Grok account** with access to `console.x.ai` (Voice → Text-to-Speech), for narration audio.
- **A vidIQ account** — connect it to Claude as an MCP tool/connector for thumbnails, titles, and best-time-to-post insights.
- **ffmpeg** installed and on your PATH (`ffmpeg -version` should work in a terminal).
- **Node.js + npm** (`node -v` should work).
- **Python 3 + pip**.
- **Chrome**, logged into the Google Flow and xAI accounts above — Claude drives both through browser automation, so it needs to already be signed in.
- **A channel intro video** (`intro.mp4`, ~4-6 seconds, your own logo/greeting, with its own audio) — you'll need this before final assembly works.
- Ask whoever gave you access to this repo for the channel's login details for the Flow/xAI/vidIQ accounts if you're joining an existing channel, rather than starting a new one.

## Step 1 — Get the code

```bash
git clone https://github.com/Sqneek/Youtube-video-creation.git
cd Youtube-video-creation
```

## Step 2 — Connect it to Claude

- **Claude Code**: open a terminal in this folder and start Claude Code there — it reads `CLAUDE.md` automatically and knows the project's rules.
- **Claude Cowork / Desktop app**: connect this folder to a session so Claude can read and write files in it.

Either way, Claude should be able to read `CLAUDE.md` and `00_Project_Overview/New_Video_Workflow.md` right away — that's what makes it recognize this as the Video Generator project instead of a generic folder.

## Step 3 — Install the render engine's dependencies

From `04_Video_Editing/Remotion/`:

```bash
npm install
npm approve-scripts esbuild
```

Then, for subtitle transcription:

```bash
pip install faster-whisper
```

(add `--break-system-packages` if your Python environment requires it.)

## Step 4 — Set up the two Google Flow style projects

This is the one part that genuinely can't be automated — Flow projects carry a trained visual identity that lives on Google's side, not in a file.

1. In Google Flow, create a project named **exactly** `Footnotes Image Creation` (Style A — the docs reference this name literally).
2. Open `02_Image_Prompts/Styles/Style_A_FlatVector.md` and use its Art style / Character / Background / Lighting / Color palette sections as that project's guiding reference. Generate a small test batch (a character, an object close-up, an environment) and check it actually matches the spec before trusting it for a real video.
3. Set up the `@Narrator` character per that same file's "A-roll — Narrator" section, if you want narrator cutaways.
4. Repeat for a second project named **exactly** `Footnote image creator. S2` (Style B), using `02_Image_Prompts/Styles/Style_B_SimpleSketch.md`.
5. You only need one style working to start making videos — set up the other whenever.

## Step 5 — Add your own assets (not included in this repo on purpose)

These are binary files that don't belong in git — see the `README.md` inside each folder for what goes where:

- `04_Video_Editing/Assets/Intro/intro.mp4` — **required** before a video can be fully assembled.
- `04_Video_Editing/Assets/Music/` — optional instrumental tracks to reuse across videos.
- `00_Project_Overview/Channel_Branding/` and `02_Image_Prompts/Reference_Images/` — optional, for your own reference.

## Step 6 — Verify everything

- [ ] `04_Video_Editing/Remotion/node_modules/` exists (from `npm install`).
- [ ] `python -c "import faster_whisper"` doesn't error.
- [ ] `ffmpeg -version` and `ffprobe -version` both work.
- [ ] At least one Google Flow project produces a test image matching its style file.
- [ ] `04_Video_Editing/Assets/Intro/intro.mp4` exists.
- [ ] Claude, opened in this folder, can read `CLAUDE.md` and `00_Project_Overview/New_Video_Workflow.md` without you pointing it there manually.
- [ ] Saying "let's make a new video" to Claude here starts a 5-question intake, not a guess.

All green? Head to **[USAGE.md](USAGE.md)** — that's the actual day-to-day guide.

## Optional: unattended scheduled automation

Not required to use the pipeline, and worth setting up only once the manual flow feels solid. See `CLAUDE.md`'s "Scheduled/autonomous pipeline" section and `04_Video_Editing/Run_Assembly.ps1`'s header comment if you want to go there later.

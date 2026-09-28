# Setup

This repo is the reusable *machinery*. It intentionally does not include:

- Any per-video content (`Videos/` — research, scripts, generated images, audio, finished video files)
- Binary channel assets (channel intro video, music library, branding images, reference images)
- `node_modules/` (regenerate with `npm install`)
- Anything that only exists inside a live Google Flow / xAI / vidIQ account

## 1. Accounts & software checklist

- **Google account** with access to **Google Flow**. You'll create two custom Flow "projects"
  by hand (Section 2 below) — this can't be scripted, it's done through Flow's own UI.
- **xAI/Grok account** with access to `console.x.ai` (Voice → Text-to-Speech), for narration audio.
- **vidIQ account**, connected to Claude as an MCP tool/connector — thumbnails, titles, best-time-to-post, optional music generation.
- **Gmail connected to Claude** as an MCP connector, only if you set up the optional scheduled/autonomous pipeline later.
- **ffmpeg** on PATH (`ffmpeg -version`, `ffprobe -version`).
- **Node.js + npm** (`node -v`).
- **Python 3 + pip**, plus `pip install faster-whisper` (subtitle transcription).
- **Chrome**, logged into the Google Flow and xAI accounts above — Claude drives both via browser automation.
- **A channel intro video** (`intro.mp4`, ~4-6s, your own logo/greeting, own baked-in audio) — required before final assembly (Step 7 of `04_Video_Editing/FFmpeg_Pipeline.md`) will work. Put it at `04_Video_Editing/Assets/Intro/intro.mp4`.
- Optional: instrumental music tracks in `04_Video_Editing/Assets/Music/` to reuse across videos.

## 2. Set up the two Google Flow style projects

Google Flow projects carry a trained visual identity that lives on Google's side, not in a file:

1. Create a Flow project named **exactly** `Footnotes Image Creation` (Style A — the workflow docs reference this name literally).
2. Use `02_Image_Prompts/Styles/Style_A_FlatVector.md`'s Art style / Character / Background / Lighting / Color palette sections as the project's guiding description/reference. Generate a small test batch (a character, an object close-up, an environment) and check it matches the spec before trusting it for a real video.
3. Set up the `@Narrator` character per that file's "A-roll — Narrator" section, if you want narrator cutaways.
4. Repeat for a second project named **exactly** `Footnote image creator. S2` (Style B), using `02_Image_Prompts/Styles/Style_B_SimpleSketch.md`.
5. You only need one style to start — set up the other later.

## 3. Install dependencies

From `04_Video_Editing/Remotion/`:

```bash
npm install
npm approve-scripts esbuild
```

Then:

```bash
pip install faster-whisper
```

(add `--break-system-packages` if your environment requires it).

## 4. Connect accounts/tools in Claude

- Connect this repo's local checkout to your Claude Code / Cowork session.
- Add the **vidIQ** MCP connector for thumbnails/titles/insights.
- Add **Gmail** only if setting up the optional scheduled pipeline later (see `04_Video_Editing/Run_Assembly.ps1`'s header comment and `CLAUDE.md`'s "Scheduled/autonomous pipeline" section).
- Make sure Chrome is reachable by Claude's browser tools and logged into the accounts from Section 1.

## 5. Verify

- [ ] `04_Video_Editing/Remotion/node_modules/` exists (`npm install` ran).
- [ ] `python -c "import faster_whisper"` doesn't error.
- [ ] `ffmpeg -version` / `ffprobe -version` both work.
- [ ] At least one Google Flow project produces a test image matching its style file.
- [ ] `04_Video_Editing/Assets/Intro/intro.mp4` exists.
- [ ] Claude, opened in this repo, can read `CLAUDE.md` and `00_Project_Overview/New_Video_Workflow.md`.
- [ ] Saying "let's make a new video" to Claude here starts the 5-question intake, not a guess.

## 6. Optional: unattended scheduled automation

Not required to use the pipeline. See `CLAUDE.md` → "Scheduled/autonomous pipeline",
`00_Project_Overview/New_Video_Workflow.md`'s scheduled-pipeline branch of Step 5, and
`04_Video_Editing/Run_Assembly.ps1`'s header comment for the full contract (edit the `$Root`
path in that script before registering it with Windows Task Scheduler). Set this up only once
the manual flow is working and trusted.

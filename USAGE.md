# How to Use

For anyone who already has this project installed and connected to Claude (see
**[INSTALLATION.md](INSTALLATION.md)** if you haven't done that yet). This is what it's
actually like to make a video with it, day to day.

## The short version

Open Claude in this folder (Claude Code, or Cowork connected to this folder) and just say
something like *"let's make a new video"* or *"I want to do a video about [topic]"*. Claude
takes it from there — the sections below explain what to expect at each stage.

## Step 0 — The 5 intake questions

Before any research starts, Claude will ask (or you can answer up front):

1. **Topic** — what's the video about? You can name one, or ask Claude to propose a few.
2. **Length** — target runtime (e.g. "90 seconds", "8-10 minutes").
3. **Number of images** — how many scenes to break the script into, or just say "you decide."
4. **Visual style** — Style A (Flat Vector) or Style B (Simple Sketch)? See
   `00_Project_Overview/README.md` for what each looks like.
5. **Voiceover** — automated (Claude generates it via the xAI console) or you'll record/generate
   it yourself and hand back an audio file.

Don't skip these — the whole pipeline downstream is sized and styled from these five answers.

## Step 1 — Research

Claude writes `Videos/[Topic_Name]/Research_Notes.md`: a timeline, key people, disputed points,
and visual reference notes, sourced and cross-checked per
`01_Research_and_Script/Research_Workflow.md`. Nothing for you to do here except skim it for
anything that looks off.

## Step 2 — Script

Claude writes `Script.md` (annotated, with beat labels and visual notes) and `Narration.txt`
(the clean text that actually gets voiced), following
`01_Research_and_Script/Script_Style_Guide.md` — a specific "smart friend explaining something
wild" voice, not a documentary narrator. **This is the first checkpoint** — Claude will stop and
show you the script before spending time on anything downstream, unless you've told it to run
straight through.

## Step 3 — Image prompts + generation

Claude breaks the script into scenes and writes `Image_Prompt_Batch.md` (one prompt per image,
in script order), then generates every image in Google Flow and drops them into
`Generated_Images/`. **This is the second checkpoint** — you'll see the full batch of prompts
before generation starts.

Once images are generated, Claude shows you all of them **without pre-screening or rejecting
any itself** — deciding what needs a redo is your call, not Claude's. If something looks off,
just say so and point at the image; Claude will explain what it sees against the style file, or
fix it if you describe the problem.

## Step 4 — Voiceover

Either Claude generates the narration automatically (if it has browser access to the xAI/Grok
console), or it hands you `Narration.txt` and waits for you to generate the audio yourself and
drop it in `Audio/narration.mp3`. Either way, listen through it once before moving on — if the
audio doesn't match the script's beat boundaries, that gets fixed in the script, never by editing
the audio.

## Step 5 — Assembly

This is the one step Claude can't fully do inside a Cowork/cloud session — the actual video
render needs to run locally (native Node + Chrome). Claude will hand you a single command to
paste into a local Claude Code session, something like:

```bash
python scripts/enhance.py --video "Videos/[Topic_Name]" [--music "<track>"] [--no-subs]
```

Claude will ask once whether you want background music (reuse a track from
`04_Video_Editing/Assets/Music/`, generate a new one via vidIQ, or none). Running that command
builds the finished video — motion, music, subtitles, and the channel intro — straight into
`Videos/[Topic_Name]/Publish/[Topic_Name].mp4`. No further review needed on Claude's side once
that file exists.

## Step 6 — Thumbnail

Claude generates 3-4 thumbnail concepts via vidIQ and presents them to you to pick from. The
chosen one is saved to `Publish/Thumbnail.png`.

## Step 7 — Title & Description

Same idea: 3-4 title options via vidIQ for you to choose from, plus a short 1-2 sentence
description. Both land in `Publish/Description.txt`.

## What "done" looks like

`Videos/[Topic_Name]/Publish/` ends up with three things: the finished `.mp4`, `Thumbnail.png`,
and `Description.txt`. Everything else in that video's folder (research, script, prompts, raw
images, audio) stays right there alongside it.

## Publishing — always manual

**Claude will never upload or publish to YouTube, under any circumstance.** Once `Publish/` has
your finished video, thumbnail, and description, that's the handoff point — you review it and
publish it yourself, on your own timing. Claude can optionally tell you the channel's
highest-activity posting windows (via vidIQ) as a recommendation, but the actual publish step is
always yours.

## If you're not sure where a video is stuck

Look inside `Videos/[Topic_Name]/` — whichever files/folders are missing tell you the next step:
no `Research_Notes.md` → research hasn't started; no `Script.md` → script hasn't started; no
`Image_Prompt_Batch.md` → prompts haven't been written; fewer images in `Generated_Images/` than
rows in the batch → generation is still in progress; no `Audio/narration.mp3` → voiceover is
pending; no `Publish/[Topic].mp4` → assembly hasn't been run locally yet; `Publish/` has the
video but no `Thumbnail.png`/`Description.txt` → those last two steps are pending. Just tell
Claude "continue this video" and it'll figure out where it left off.

## Working with Claude on this project

`CLAUDE.md` sets the tone deliberately: Claude is meant to push back on weak ideas here, not
just agree with you — if something in a script, image batch, or plan looks off to Claude, it
should say so and suggest a better approach rather than silently comply. That's intentional, not
a bug. If you disagree with a pushback, just say so; Claude will proceed once you've made the
call.

## Optional: full unattended automation

Not covered here — this guide is the normal, interactive way to make a video, checkpoints and
all. A separate scheduled/autonomous mode exists (see `CLAUDE.md`'s "Scheduled/autonomous
pipeline" section) where Claude runs the whole pipeline unattended on a schedule and emails a
status report instead of pausing for approval. Set that up later, only once you're comfortable
with how the manual flow behaves — it's a deliberate, explicit opt-in, not the default.

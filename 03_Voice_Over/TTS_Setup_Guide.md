# Voice Over — Grok

## Purpose

Governs how narration audio is produced and how image timing gets synced to it. Two ways to produce
the audio — manual handoff (original method) or automated generation via the xAI Voice API console
(added once it was confirmed to work from a device-bound Cowork session) — plus the beat-alignment
check against the real audio and the duration math that drives image timing in assembly.

## Producing the audio

**Method A — Automated (xAI Voice console, requires a device-bound browser session)**

Confirmed working: `https://console.x.ai/team/<team-id>/voice/text-to-speech` is a browser-usable
playground (not just a raw API) — type text into the box, pick a voice, click "Generate audio", then
click the download icon next to the resulting waveform player to save an `.mp3`. This can be driven
with the same browser-automation tools used for Google Flow, as long as the session is bound to a
device with Chrome logged into the user's xAI/Grok account.

1. Paste `Videos/[Topic_Name]/Narration.txt` into the text box. Note the field's character limit
   (15,000 observed) — if the narration is longer, split it into consecutive chunks at beat
   boundaries and generate/download each separately, then concatenate the resulting audio files in
   order (e.g. via ffmpeg concat) into a single `narration.mp3`.
2. Keep the voice selection consistent across every video on this channel unless deliberately
   changed — pick once, record the choice here or in the per-video notes, and reuse it.
3. Click "Generate audio", wait for the waveform player to appear (this is the completion signal —
   no separate "done" toast was observed), then click the download icon.
4. Verify the newest file in the Downloads folder is a real, non-trivial-size audio file before
   trusting it, then move/rename it to `Videos/[Topic_Name]/Audio/narration.mp3`.
5. Check the account's credit balance if generation starts failing (a free-tier allowance can
   exist without a paid balance, but don't assume that persists forever) — flag it in the run
   report rather than silently blocking. Adding credits is a purchase — never do this
   automatically; surface it for the user to handle themselves.

**Method B — Manual handoff (fallback, or when not device-bound)**

1. Finalize `Videos/[Topic_Name]/Narration.txt` — clean narration text, beat-labeled to match
   `Script.md`. Hand it to the user.
2. Stop and wait. The user generates the audio (in Grok directly, or via their own personal
   recording), saves it to `Videos/[Topic_Name]/Audio/narration.mp3`, and reviews it.

## Rules (apply to either method)

- Always listen through the finished audio before doing any timing math.
- If the audio doesn't match the script's beat boundaries, fix it by realigning the beat in the
  script. **Never edit the audio to fix a misalignment.**
- Never assume a `.srt`/timestamp file exists — neither method produces one.
- Don't estimate beat durations before beat boundaries are verified against the actual audio (step 4
  below must happen before step 6).
- Don't derive image timing fixes from word count a second time — post-assembly corrections are
  manual, beat by beat.

## Instructions (after audio exists, either method)

3. Once the audio is reviewed (by the user, or — for an unattended run — flagged in the run report
   for the user to review after the fact), listen through the full audio.
4. Check whether the audio's spoken content matches the beat boundaries in `Narration.txt`/`Script.md`.
   If a beat doesn't align with where that content falls in the audio, realign the beat boundary in
   the script.
5. Run: `ffprobe -v error -show_entries format=duration -of csv=p=0 narration.mp3` → total duration.
6. Count words per beat, using the realigned beat boundaries from step 4.
7. Per beat: `estimated duration = (beat word count ÷ total word count) × total audio duration`.
8. Distribute each beat's images evenly across its estimated time window, per
   `04_Video_Editing/FFmpeg_Pipeline.md` Steps 1–2.
9. After assembly, listen through once. If an image lands early/late, correct only that beat's timing
   by hand.

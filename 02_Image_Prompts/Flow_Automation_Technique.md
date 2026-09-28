# Google Flow Image Generation — Browser Automation Technique

Reference for driving the "Footnotes Image Creation" (Style A) / "Footnote image creator. S2" (Style B)
Google Flow project via Chrome browser tools, unattended or supervised. Written after generating dozens
of images live and hitting every failure mode below more than once. Follow this exactly — deviations
(coordinate-only clicks, skipping verification steps, short waits) are what caused failures during
development.

## Per-image loop

1. **Navigate fresh** to the Flow project URL for every image (don't reuse a stale in-page state).
2. **Wait for the media grid to load** before doing anything else — 10s, then another 8-10s, then
   screenshot to confirm. The grid renders progressively slower as more images accumulate in the
   project; blank/dark tiles in the screenshot mean it's still loading. If still blank, wait another
   8-10s and re-check. Do not proceed to click the prompt field while the grid is visibly unloaded —
   this is the single biggest cause of focus failures below.
3. **Find and click the prompt textbox** (`find` query: "What do you want to create prompt input text
   field"). It's a rich contenteditable `<div>`.
4. **Verify focus actually landed** before typing — inspect the page (e.g. read_page or an equivalent
   focus check) to confirm the contenteditable element became the focused element. This fails on
   roughly 1 in 3 attempts, especially right after navigation. If not focused, repeat step 3 (fresh
   `find` + click) — do not just retype blindly. Budget 2-4 retries as normal, not exceptional.
   **A programmatic `.focus()` call is not a substitute for a real click** — it can make the element
   report as focused while a subsequent typed input still fails to insert any text. Always use a real
   click via a freshly-found element reference.
5. **Type the full prompt text** once focus is confirmed.
6. **Verify the typed length** matches the intended prompt's character count exactly before submitting.
   A mismatch means characters were dropped or the field wasn't really accepting input — stop and
   redo steps 3-5 rather than submitting a truncated/garbled prompt.
7. **Click Create** (`find` query: "Create button (arrow_forward icon) to submit prompt").
8. **Wait for generation** — 10s, then another 8-10s, then screenshot. Generation tiles show a
   percentage while in progress.

## Downloading at 2K (free tier, not paid 4K)

The download menu is the most error-prone step — `find` and raw coordinate clicks are both unreliable
here (coordinates shift because viewport size is not constant between calls, and `find` has
misidentified the wrong menu item, once clicking straight into a paid-upgrade flow). Use this exact
method every time:

1. Open the image's edit view (click its tile).
2. `find` the Download button in the top toolbar of the editor (not the grid-view hover toolbar).
3. Click it to open the format menu.
4. Read the interactive page structure (not `find`) — the menu appears as a `menu` node containing
   three `menuitem` entries in order: **1K Original, 2K Upscaled, 4K Upscaled** (a 4th "Upgrade"
   button is nested near the 4K item — never click it).
5. **Always click the second `menuitem`** (2K Upscaled) by its element reference from that structural
   read. Never use `find` to select this specific item, and never click by raw coordinates.
6. Confirm success via the toast text: "Upscaling your image, download will start automatically."
   followed by "Upscaling complete, your image has been downloaded!" — this toast is the only
   reliable success signal. If it never appears after a reasonable wait, the click missed; reopen the
   menu and retry from step 3.
7. Verify the newest file in the Downloads folder (`ls -t`) matches the expected image before
   processing it — cross-check against the edit view's displayed title. Generic filenames can look
   similar across images.
8. Convert to PNG (see project's existing processing script) and save into
   `Videos/[Topic]/Generated_Images/` under the batch's assigned filename.

## Failure modes and fixes

- **"Failed — We noticed some unusual activity" tile**: wait ~30s (e.g. three sequential 10s waits),
  then click the tile's circular Retry icon. This reliably succeeds on retry — don't skip the cooldown.
- **Bad/off-spec generation** (wrong art style, a text/title-card image instead of an actual
  illustration, or any other clear spec violation): open the tile, click "Move to trash" in the
  toolbar, navigate back to the project root, and resubmit the identical prompt fresh. This has a
  100% observed fix rate — don't try to edit/patch a bad generation in place.
- **CDP/screenshot timeouts** ("renderer may be frozen or unresponsive"): wait ~8s and retry the same
  screenshot call. No page reload needed.
- **Session/usage limits mid-batch**: if a tool call returns a rate-limit error mentioning a reset
  time, stop cleanly at the last fully-completed image (don't leave one half-downloaded/unprocessed)
  and report the stopping point plus the reset time. Resume from the next image once past the reset.

## Unattended-specific notes

For scheduled/unattended runs, there is no human watching to catch a subtly wrong image (right
technique, wrong content — e.g. style drift that doesn't trip the "unusual activity" or bad-generation
detectors above). Apply the mechanical checks in this doc rigorously, but still include a thumbnail
contact sheet of every generated image in the run's report email so a human reviews the actual content
before the video is considered final — mechanical QA here is not a substitute for a visual pass.

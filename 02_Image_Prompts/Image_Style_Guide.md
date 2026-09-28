# Image Prompt Instructions — Google Flow

Compact instruction set.

**Output format (all images):** 16:9, generated at **1920×1080** (Full HD). The video pipeline renders on a fixed 1920×1080 canvas, so anything smaller gets upscaled and softens under the Ken Burns zoom. Set Flow's aspect ratio to 16:9 and the highest resolution available; never ship sub-1080 scene art.

---

## 1. B-roll prompt template (every script-illustration image)

Fill these 6 fields, then write them out as one flowing prompt paragraph — not a labeled list.

- **Character(s):**
- **Background/location:**
- **Lighting:**
- **Camera:**
- **Color palette note:**
- **Style suffix:**

**Era:** before writing any prompt, identify which specific time period the script line describes (ancient/period-specific, a later historical decade, present-day, etc.). If the video's timeline spans more than one era, write that era's clothing, technology, and architecture explicitly into the Character(s) and Background/location fields for every single prompt — never default to one uniform "antique" or "modern" look across a batch that covers multiple periods.

---

## 1b. Explanatory graphic template (charts, maps, diagrams)

### Rules

- Use instead of Section 1 when the narrated line has a quantified/comparative claim: a percentage, a count, a before/after, a timeframe, a territorial share.
- Target mix: roughly 40–50% explanatory graphics against narrative scene shots. Scan the finished batch for this balance, same as shot-type repetition.
- Never texture or weather a diagram to match scene art — no stone, parchment, tilt, or photographed-object treatment. Flat, frontal, high-contrast only.
- Data points must be sourced only from `Research_Notes.md` or `Script.md` — never invented. If a script figure is flagged inaccurate, chart the direction/trend only and omit the exact number.
- No camera angle — diagrams are presented flat and frontal, never as a photographed object.
- Diagram labels (percentage, year, place name, phase name) are the one exemption to the zero-tolerance text rule in Section 4. Nothing else in the frame — no signage, no captions, no invented numbers.

### Instructions

Fill these fields, then write them out as one flowing prompt paragraph:

1. **Diagram type:** line chart, bar/split-comparison chart, map-highlight, cycle/phase diagram, stacked-layer diagram, or another layout that fits the specific claim.
2. **Data points:** exact real figures/labels from `Research_Notes.md`/`Script.md`.
3. **Layout:** flat, frontal, centered; generous negative space; one clear focal element.
4. **Rendering:** flat-color 2D vector shapes, crisp even-weight outlines, solid fills.
5. **Explanatory icons (optional):** one simple flat-vector icon per element, only where a label naturally maps to a concrete object (coin, crown, tree, sword and shield, crumbling column). Skip if nothing fits.
6. **Label style:** clean, bold, sans-serif; no chart-junk (gridlines, legends, tick marks, decorative borders).
7. **Color:** 2–3 tones from the video's chosen style file's color palette (see Section 2); one accent color for the focal point, flat neutrals elsewhere.
8. **Background:** flat solid color or simple gradient in a palette tone — never textured or weathered.
9. **Camera:** none.
10. **Style suffix:** "Rendered as a clean, flat 2D vector infographic — precise and instantly legible, like a well-made explainer-video chart. Not a photographed object, not a weathered or textured surface, not a UI or software dashboard screenshot."

Diagrams use this same template regardless of which visual style (A or B) the video is using — they never carry Style A's texture/lighting or Style B's line-drawing look, just the shared flat-infographic language above.

---

## 2. Visual style — pick one per video at intake

Two independent, locked visual styles are available. `New_Video_Workflow.md` asks which one at intake — pick one and use it for the entire video's B-roll, A-roll, and character work. Never mix styles within a batch.

- **Style A — Flat Vector:** `02_Image_Prompts/Styles/Style_A_FlatVector.md`
- **Style B — Simple Sketch:** `02_Image_Prompts/Styles/Style_B_SimpleSketch.md`

---

## 3. Consistency — what it means and doesn't mean

- Consistency = **style** consistency (the chosen style file's Character/Background/Lighting/Color sections), applied to every single prompt, every time. It does **not** mean generating near-duplicate images.
- Google Flow has no memory between prompts. A recurring location or character can never be referenced as "same as before" — re-write its fixed descriptor phrase in full, verbatim, every time it reappears (see the per-video Consistency System / recurring-descriptor list in that video's `Image_Prompt_Batch.md`).
- Character base anatomy is fully fixed per the chosen style file — never add new physical description beyond what that file's "role layer" rule allows. Role word only (scholar, soldier, pirate, farmer, etc.) — the specific role/era look (Roman soldier, Caribbean pirate, Renaissance scholar) is chosen per video based on what the script is actually about, not baked into the base character.
- **Clothing/gear consistency:** the first time a recurring character type appears, write a fixed clothing/gear descriptor phrase for it (e.g. "a diver in an old brass diving helmet and canvas suit") and reuse that exact phrase verbatim every time that character type reappears in the batch.
- Graphs/explanatory diagrams are the one deliberate exception to "same visual language everywhere": they share only the color palette with scene images (the chosen style file), not the environment treatment or camera-angle photography of a scene. Build them from the Section 1b template — consistency for diagrams means every diagram in the batch uses the same clean flat-vector infographic language as every other diagram, not that it matches the scene shots around it.

---

## 4. Rules

- Do not stray from the B-roll template (Section 1) or the chosen style file (Section 2).
- Every prompt must be grounded in the specific script line it illustrates — never a generic or irrelevant filler shot.
- Scan the finished batch for narrative/explanatory balance (Section 1b) in addition to shot-type repetition — a batch built entirely from mood/symbolic scene shots on a script full of quantified claims is a defect, not a style choice.
- Filename convention: `NN_short-beat-slug.png` — two-digit scene number, sequential in script order across all roll types, so alphabetical sort reproduces script order for `images.txt` and the ffmpeg concat step. Track roll type (B-roll / A-roll / Diagram) in its own column.
- On generation, rename each image to its assigned filename and save into `Videos/[Topic_Name]/Generated_Images/`.
- After the full batch is generated, showcase every image to the user without pre-screening, rejecting, or flagging any of them yourself. Generation is your job; deciding what needs a redo is the user's call.
- For each image the user flags, point out the specific issue you see against the chosen style file if asked — or, if nothing stands out, wait for the user to describe it — then fix it before moving on to the next pipeline step.

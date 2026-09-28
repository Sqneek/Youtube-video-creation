# Style B — Simple Sketch

**Flow project:** Footnote image creator. S2

> **Revision note:** this replaces Style B's original flat-vector/no-shading definition. The character stays simplified, but the render treatment (painted, textured, lit) is a deliberate departure — validate any style change like this via a small test batch (3-5 images spanning a character, an object close-up, and an environment) before adopting it across a whole video.

## Art style / medium
Semi-realistic painted illustration. The character stays simplified (circle head, slim clothed body, minimal face), but the whole image — character and background alike — is fully painted: soft cel-shaded blocking for volume and cloth folds, atmospheric depth, moody/directional lighting, and real material texture (grass, wood grain, cloth weave, stone, fur, ice). No flat, shadowless, single-color-fill rendering — that was the old Style B rule and no longer applies.

## Character
- Head: plain circle, pale off-white skin tone, one continuous base color.
- Hair: tousled, drawn with a handful of loose jagged strokes on top and sides, one dominant hair color (dark brown default, can shift per character), never covering the face.
- Face: thicker, angled eyebrows carrying real expression (serious, worried, determined — matched to the beat's mood), small round eyes with a subtle dark pupil (not a flat dot), one simple mouth line reflecting the same expression. No nose, no other detail.
- Body: a slim, fully clothed human figure — not a bare stick. Clothing (wraps, tunics, robes, layered leather/fur) rendered with visible cel-shaded fold lines and one accent (tied sash, strap, buckle) for volume and material read.
- Hands: simple pale mitten-like shapes gripping objects naturally — no individual fingers, no solid black blobs.
- Grounding: a soft contact shadow under the feet, consistent with the scene's lighting direction.
- One fixed character build for every human figure — no per-character redesign. A role (archer, hunter, trader, soldier) adds exactly one or two props/garments in the same painted language — never full realism or invented anatomy beyond what's specified above. Chosen fresh per video from the actual script.
- Every prompt must spell out the base build above in-line, not just the role/action.
- Secondary/background figures (a crowd, distant workers, silhouetted attackers) may render as simpler flat silhouettes or thin-line stick figures without full character detail — reserve the full painted character treatment for the beat's main subject.

## Background / scene
Fully painted, semi-realistic environment illustration — real texture throughout (individually-rendered grass blades, wood grain, tree bark, stone, fabric, ice, fur), atmospheric depth (haze, soft blur on distant elements), and a sky/ground or interior setting matching the beat. Weathering and mood detail (mist, dust, blood, rust, snow, firelight) are welcome where the narrative calls for it.

## Lighting
Moody and directional — dramatic overcast skies, fire/torch glow, sunset/sunrise color, rim lighting — chosen to match the beat's mood. Avoid flat/shadowless lighting; some sense of volume and light direction should always be present.

## Color palette
Muted, earthy, semi-realistic tones by default (warm browns/tans, cool greys, muted greens) with mood-driven accents (fire orange, blood red, ice blue, gold sunset) — richer and more varied than the old flat 3–4-color rule, but still cohesive, not oversaturated or cartoonish.

## Camera angles — exactly 3, pick one per prompt
- **Wide shot** — establishing/scale; camera distant, subject small in frame. Keep the human figure legible at this scale — don't let it shrink to an unreadable speck; favor a slightly closer wide or add foreground framing if the subject needs to register clearly.
- **Medium shot** — eye-level, one or a few figures; the default for most narrative beats.
- **Close-up** — single subject or detail, tight framing (a face, an object, a weapon).

**Composition:** object-study prompts naming more than one element (e.g. "a blade bound to a handle") must use a spatial relationship word ("resting on," "held above," "bound to") or Flow renders two disconnected icons instead of one scene.

---

## A-roll — Narrator
- **Tag:** `@Narrator` — pre-built character in the "Footnote image creator. S2" Flow project, no design description needed.
- Fixed design (reference only, never re-described in prompts): top hat, round head, one circular eye with a dot pupil, calm smile, thin stick body, blob hands/feet, flat brown coat.
- **Note:** this pre-built design may not visually match a fully painted Style B look. Keep using it as-is as a distinct "host" cutaway, but flag it to the user if it looks visually out of place once cut into a real video — it may need a redesign.
- **Use for:** host/cutaway moments, not script-illustration scenes.
- **Prompt template:** `@Narrator, [action/pose description].`
- **Sequence rule:** one image per narrator appearance — no burst/animation sequence.
- **Placement:** the Narrator appears 2-3 times total across the video, never in the hook. Distribute placements across the body/close rather than clustering them.

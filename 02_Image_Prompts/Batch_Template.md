# Prompt Batch — [Video Topic Name]

Save the filled-in copy of this template as `Videos/[Topic_Name]/Image_Prompt_Batch.md` — not here. This file is just the reusable starting point.

One row per scene, in script order. Duration is a rough guide for how many images that scene needs (scales with the number of images agreed at intake — see `00_Project_Overview/New_Video_Workflow.md`).

## Filename convention

Every scene gets a unique, descriptive filename up front: `NN_short-beat-slug.png` — two-digit scene number (keeps files in script order when sorted, and matches what FFmpeg expects) + a short kebab-case slug describing that beat's content. This is the filename to give the image when downloading/renaming it out of Google Flow — no manual figuring-out later which image belongs where.

Example: `03_singing-carries-across-no-mans-land.png`

| # | Script beat | Filename | Est. duration | Google Flow prompt |
|---|---|---|---|---|
| 1 | Hook | 01_ | | |
| 2 | Context | 02_ | | |
| 3 | Body beat 1 | 03_ | | |
| 4 | Body beat 2 | 04_ | | |
| 5 | Turning point | 05_ | | |
| 6 | Aftermath | 06_ | | |
| 7 | Close | 07_ | | |

Add/remove rows to match the actual number of images agreed at intake. Each prompt should follow the formula in `02_Image_Prompts/Image_Style_Guide.md`. Fill in the Filename slug for every row before generating — that's what makes renaming downloads from Flow trivial. Generated images get renamed to their assigned filename and saved into `Videos/[Topic_Name]/Generated_Images/`.

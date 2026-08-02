---
id: academic-figure-color-expert
name: Academic Figure Color Expert
version: 1.3.2
description: Make palette decisions for academic figures — choose between classic and pastel style families, then recommend a colorblind-safe scheme with exact hex values based on venue, domain, figure type, and module count. Use this skill whenever the user asks about colors, palettes, style for a figure, including "用什么配色", "推荐配色", "what palette for NeurIPS", "Nature Blue", "classic vs pastel", "色盲友好配色", or any color-related question about academic diagrams.
stages: [writing, research]
tools: [bash]
---

# Academic Figure Color Expert

Produce a reusable **Palette Decision**. Hex tables, venue maps, and **scene→style→palette** recipes live in one place:

→ Read `references/palettes.md` (presets + **Style family** + **Scene → palette decision** + recipes).

Always decide **style family** (classic vs pastel) before naming a classic preset.


## Principles

1. Color carries information, not decoration.
2. ≤ 3 chromatic colors + neutrals per figure.
3. Colorblind-safe by default; dual-encode categories.
4. ≥ 4 modules → monochrome (Nature Blue) beats polychrome busyness.

## Input Contract

- Prefer: venue, domain, figure type, module count, reference image, accessibility / print constraints
- Minimum: any one of venue / figure type / domain
- Missing info: follow `references/missing-info-policy.md`; still emit a conservative Palette Decision

## Output Contract — Palette Decision

Always include:

- recommended palette + one alternate
- primary / secondary / tertiary (+ neutrals) hex
- **semantic color binding** (Data/Input, Backbone, Loss, Output, Frozen roles mapped to consistent hex)
- reason (venue / domain / module count)
- accessibility note
- handoff block ready for prompt skills
## Steps

### Step 1: Collect constraints

Done when you have recorded (or marked missing): venue, domain, figure type, module count, colorblind/print needs, user color preference, reference image cues.

### Step 2: Decide style family + palette

1. Classic vs pastel — `references/palettes.md` **Style family first**
2. If pastel → hand off scheme P1/P2/P3 to `academic-figure-prompt-pastel` (hex from that skill)  
3. If classic → apply **Scene → palette decision** (hard constraints → figure type → venue → domain → vibe)  
4. Name primary + alternate; state branch (`user` / `scene` / `default`)

Done when: family + primary + alternate are explicit, with the decision checklist fields from `references/palettes.md`.


### Step 3: Emit hex + handoff

Load the chosen preset from `references/palettes.md`. Apply the **Semantic Color Binding Contract** to map structural domain roles (Data, Backbone, Loss, Output, Frozen) to consistent hex values across all paper panels. Output the Palette Decision format.

Done when: every role hex is filled, semantic binding stated, accessibility stated, and the handoff block is copy-ready for `academic-figure-prompt`.
## Sparse-input cases

| case | action |
|------|--------|
| no venue | infer from domain / reference; else Okabe-Ito (or Nature Blue if ≥ 4 modules) |
| accessibility unspecified | assume colorblind-safe required |
| only vibe words (“高级/科技/柔和”) | map to 1–2 presets with concrete hex |
| only reference image | extract hues; academicize if needed (white fill, border color, ≤ 3 chromatics) |
| figure type unknown | default framework advice; note module-detail vs comparison alternates |

## Stop

Stop when the user has a Palette Decision for the current figure, or when zero constraints and zero artifacts exist (then ask for venue / figure type / domain).

---
id: academic-figure-prompt
name: Academic Figure Prompt
version: 1.5.0
description: JSON figure spec for academic diagrams — exact_text layout control for framework, architecture, module, and comparison figures. Use when the user wants paper figure prompts, 架构图/框架图 specs, or academic-figure JSON (text prompts only as simple fallback).
stages: [writing, research, review]
tools: [bash]
---

# Academic Figure Prompt

Default deliverable: a **JSON figure spec** (`exact_*` text locks + layout blocks + rendering rules). Text prompts only for simple charts or explicit user request.

Schema and examples: → `json-schema.md`  
Palettes: → `references/palettes.md`  
Image prompt writing: → `references/image-prompt-guide.md`  
Icon vocabulary: → `references/architecture-icons.md`  
Prompt templates: → `references/prompt-templates.md`  
JSON→prompt conversion: → `references/json-to-prompt.md`  
Missing info: → `references/missing-info-policy.md`
## Text Budget (leading rule)

On-figure text is short labels and structure. Formulas, params, and long prose go to **Figure Caption**.

| element | limit |
|---------|-------|
| module title | ≤ 5 words |
| subcomponent | ≤ 3 words |
| pipeline step | ≤ 2 words primary + ≤ 2 secondary |
| formula on figure | ≤ 1 line core only |
| arrow label | ≤ 3 words |

**Label hierarchy:** Primary (must read at a glance) → Secondary (drop first under space pressure) → Caption (never on figure).

## Input Contract

- Prefer: figure type, paper/section content, modules, labels, formulas, dims, Palette Decision, reference image
- aspect_ratio (optional, from Figure Plan)
- Minimum: figure type + subject/method overview
- Missing: skeleton spec with placeholders; mark 推断 / 待确认

- Chinese figure name + type
- JSON spec (structured intermediate)
- **Image prompt** (200-400 word English visual brief for the image model)
- palette name + hex used
- caption reserve list
- completeness block (see missing info policy)

## Steps

### Step 1: Ground content

Read available paper/section material. Extract modules, dataflow, symbols, dims.

Done when: every claimed module has a source span or is marked placeholder.

### Step 2: Reference image (if any)

Extract palette, layout flow, box style, annotation density, special links.

Done when: reference constraints are listed or “no reference” is explicit.

### Step 3: Palette

Do not maintain a private palette table. This skill is **classic family** only (pastel → other skill).

1. User-specified palette / hex → use it  
2. Else existing Palette Decision from color-expert → use it  
3. Else run `references/palettes.md` **Scene → palette decision** (hard constraints → type → venue → domain); if still empty, safe default (≥4 modules → Nature Blue; else Okabe-Ito) and say so
4. Load hex from `references/palettes.md`
5. If user signals airy/pastel, **stop** and route to `academic-figure-prompt-pastel` instead of forcing classic borders

Done when: palette name + hex are fixed, family is classic, and the decision branch is stated.


### Step 4: Emit JSON spec

Load `json-schema.md`. Build `layout_and_content_blocks` with `exact_*` locks for every visible word. White fill + colored borders. Attach rendering rules and caption_note list.

Done when checklist passes:

- [ ] every on-figure string is in an `exact_*` field  
- [ ] aspect_ratio copied from Figure Plan when present  
- [ ] Text Budget respected  
- [ ] white fill / colored borders only  
- [ ] ≤ 3 chromatics from chosen palette  
- [ ] caption reserve lists off-figure content  
- [ ] no empty module shells  
- [ ] **every major block has an icon or visual anchor** (see `references/architecture-icons.md`)  
- [ ] weight status (frozen vs trainable) uses non-emoji pattern (dashed/solid borders, hatching, or pills)  
- [ ] explicit negative instructions included: `NO emojis, NO lock/fire/lightning icons, NO 3D rendering`

### Step 5: Write image prompt

Read `references/image-prompt-guide.md` and `references/json-to-prompt.md`. Convert the JSON spec into a 200-400 word English image prompt following the 8-slot structure:

1. Image type (lead with this)
2. Core subject (one sentence)
3. Composition/layout (spatial arrangement, flow, grouping)
4. Supporting modules (icons from `architecture-icons.md`, dimension labels, formulas, token pills, legends)
5. Visual tone (concrete descriptors, not vague words)
6. Material/texture (border width, fills, corner radius)
7. Typography (font, sizes, hierarchy)
8. Aspect ratio (last)

Use `references/prompt-templates.md` for the template matching the figure type. Every major block must have a visual anchor (icon, thumbnail, or geometric marker). Parameters and long formulas go in caption_note, not on the figure.

Done when: prompt is 200-400 words, all 8 slots present, every JSON block translated to spatial prose (not listed mechanically), and supporting modules included.

### Step 6: Fallback text prompt (rare)

Only if ≤ 3 modules without branches, pure data chart, or user demands prose prompt. Use four-layer skeleton in `json-schema.md` (Global Context → Section/Column Encapsulation → Annotations & Links → Style Specifications with hex & negative constraints).

## Stop

Stop when the Figure Spec Package (JSON spec + image prompt) for the requested figure(s) is delivered, or when figure type and subject are both missing (ask for those two only).

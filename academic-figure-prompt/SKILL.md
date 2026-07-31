---
id: academic-figure-prompt
name: Academic Figure Prompt
version: 1.4.0
description: JSON figure spec for academic diagrams — exact_text layout control for framework, architecture, module, and comparison figures. Use when the user wants paper figure prompts, 架构图/框架图 specs, or academic-figure JSON (text prompts only as simple fallback).
stages: [writing, research, review]
tools: [bash]
---

# Academic Figure Prompt

Default deliverable: a **JSON figure spec** (`exact_*` text locks + layout blocks + rendering rules). Text prompts only for simple charts or explicit user request.

Schema and examples: → `json-schema.md`  
Palettes: → `references/palettes.md`
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
- Minimum: figure type + subject/method overview
- Missing: skeleton spec with placeholders; mark 推断 / 待确认

## Output Contract — Figure Spec Package

- Chinese figure name + type
- JSON spec (default) **or** text prompt (fallback)
- palette name + hex used
- caption reserve list
- completeness block (see missing-info policy)

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
3. Else run `docs/palettes.md` **Scene → palette decision** (hard constraints → type → venue → domain); if still empty, safe default (≥4 modules → Nature Blue; else Okabe-Ito) and say so  
4. Load hex from `docs/palettes.md`  
5. If user signals airy/pastel, **stop** and route to `academic-figure-prompt-pastel` instead of forcing classic borders

Done when: palette name + hex are fixed, family is classic, and the decision branch is stated.


### Step 4: Emit JSON spec

Load `json-schema.md`. Build `layout_and_content_blocks` with `exact_*` locks for every visible word. White fill + colored borders. Attach rendering rules and caption_note list.

Done when checklist passes:

- [ ] every on-figure string is in an `exact_*` field  
- [ ] Text Budget respected  
- [ ] white fill / colored borders only  
- [ ] ≤ 3 chromatics from chosen palette  
- [ ] caption reserve lists off-figure content  
- [ ] no empty module shells  
- [ ] weight status (frozen vs trainable) uses non-emoji pattern (dashed/solid borders, hatching, or pills)  
- [ ] explicit negative instructions included: `NO emojis, NO lock/fire/lightning icons, NO 3D rendering`  

### Step 5: Fallback text prompt (rare)

Only if ≤ 3 modules without branches, pure data chart, or user demands prose prompt. Use four-layer skeleton in `json-schema.md` (Global Context → Section/Column Encapsulation → Annotations & Links → Style Specifications with hex & negative constraints).

## Stop

Stop when the Figure Spec Package for the requested figure(s) is delivered, or when figure type and subject are both missing (ask for those two only).

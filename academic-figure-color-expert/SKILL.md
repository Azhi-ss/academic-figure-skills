---
name: academic-figure-color-expert
description: Choose a reference-aware, accessible color and surface system for academic figures. Use for palette, visual-style, semantic-zone, print, or colorblind questions about classic technical diagrams, airy UI-like figures, and illustrated modular academic infographics.
metadata:
  version: "1.4.0"
---

# Academic Figure Color Expert

Produce a reusable **Palette Decision**. Read `references/palettes.md` for style profiles, paired semantic-zone tokens, classic presets, and scene recipes.

## Decision priorities

Apply these in order:

1. Explicit user requirements, including requested colors, style, print mode, or accessibility constraints.
2. A supplied reference image's **visual grammar**. Extract its composition, panel surfaces, outline strength, shadow treatment, typography character, icon style, nesting depth, density, arrow grammar, and fill/outline pairings. Match the grammar, not the reference's labels, branded assets, or method content.
3. Hard production constraints such as grayscale printing and text contrast.
4. Figure semantics and the number of distinct visual zones.
5. An existing paper-wide visual system or explicit submission rule.
6. A conservative default when no stronger evidence exists.

`module_count` is a density hint, not a palette switch. Do not choose monochrome merely because a repository exposes many modules.

## Style profiles

- **`classic-technical`**: restrained vector geometry, usually white or near-white modules, fine borders, compact technical labels.
- **`pastel-airy-ui`**: white cards, subtle separation, floating tokens and pills, generous whitespace.
- **`illustrated-modular`**: soft tinted semantic zones, strong same-hue outlines, no shadow, an asymmetric hero region, one-level subcards, controlled hand-drawn line icons, and rounded display headings with readable body text.
- **`reference-led`**: override defaults with observed reference grammar; this may remain technical, airy, illustrated, or mixed and must not default to hand-drawn panels.

Profiles are composable when a reference clearly combines their properties. Avoid accidental mixtures; state which properties came from the reference and which are defaults.

## Principles

1. Bind color to stable meaning rather than module order.
2. Use only as many chromatic zones as the figure needs; repeat colors for repeated roles.
3. Pair every colored zone with shape, label, border style, or iconography so meaning survives grayscale and color-vision differences.
4. Specify each illustrated zone as `{soft_fill, dark_outline, title_text, icon_accent}` rather than a bare list of hex values.
5. Keep small body text neutral (`#24323D` or another validated dark neutral). Reserve colored text for headings or validate it at the actual size and background.

## Input contract

- Prefer: reference image, explicit visual preference, figure type, semantic zones, existing paper-wide colors, and print/accessibility constraints.
- Treat module count only as a layout-density signal.
- Minimum: any one of reference image, visual preference, figure type, or concrete production constraint. Venue/domain names without a real constraint do not choose a palette.
- If information is missing, follow `references/missing-info-policy.md` and still emit a conservative decision.

## Output contract — Palette Decision

Always include:

- canonical style profile, optional named `style_preset`/layer, and decision branch (`user`, `reference`, `scene`, or `default`)
- a short reference-grammar summary, or `no reference supplied`
- recommended palette/token set and one alternate
- canvas, body text, arrow, and neutral-divider colors
- semantic-zone bindings using paired tokens when zones are tinted
- accessibility and grayscale notes
- a copy-ready handoff for the prompt skill

## Workflow

### 1. Record constraints and visual grammar

Record explicit user requirements first. If a reference exists, describe its observable grammar without copying its content. Do not seek or invent venue/domain stereotypes; record only concrete submission or paper-wide constraints.

### 2. Select profile and palette

Use `references/palettes.md`:

- `classic-technical` → choose a classic preset or a custom restrained set
- `pastel-airy-ui` → choose P1/P2/P3 or reference-derived token colors
- `illustrated-modular` → choose paired semantic-zone tokens, starting from I1 when no reference colors are available
- `reference-led` → derive the actual surface/composition grammar first, then choose only compatible tokens

Monochrome is appropriate when hierarchy is the main distinction, grayscale reproduction dominates, or the user/reference asks for it. Multiple low-saturation zones are appropriate when distinct subsystems must be scanned quickly.

### 3. Bind semantic zones

Map colors to the figure's actual roles. For agentic science, typical roles include reasoning/planning, evidence/context, deterministic execution, advisory/uncertainty, memory/provenance/recovery, output/report, and exception/stop. Do not force neural-network roles such as Backbone or Loss onto an agent workflow.

### 4. Emit the handoff

Include exact paired tokens, the intended carrier for each color (panel fill, outline, title, icon, arrow), contrast notes, and any reference-derived exceptions.

## Sparse-input cases

| Case | Action |
|---|---|
| No reference/style cue | Use figure semantics; otherwise choose Okabe-Ito for classic, P2 for airy UI, or I1 for illustrated modular |
| Accessibility unspecified | Use colorblind-aware dual encoding, validate text and graphical contrast, and inspect the rendered output |
| Only vibe words | Map to one or two profiles and explain the concrete surface/outline differences |
| Only reference image | Derive grammar and paired tokens from it; preserve academic legibility rather than forcing white modules |
| Figure type unknown | Offer a framework-oriented decision and identify what would change for a detail or comparison figure |

## Stop

Stop when the user has a complete Palette Decision, or when no constraint and no
artifact exists; in that case ask only for a reference, figure type/content
relationship, or concrete production/accessibility constraint. A domain name by
itself is not enough to choose color.

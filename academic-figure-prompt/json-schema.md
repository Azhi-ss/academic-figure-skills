# JSON Figure Spec Schema

Load when producing the default JSON output of `academic-figure-prompt`.

## Top level

```json
{
  "diagram_type": "string",
  "diagram_title_rendering": "None",
  "aspect_ratio": "16:9 | 3:2 | 4:3 | 1:1 | None",
  "physical_spec_and_typography": {
    "canvas_width": "89mm (single column) | 183mm (double column)",
    "font_family": "Arial, Helvetica, sans-serif",
    "font_hierarchy": {
      "title": "10-12pt bold",
      "primary_label": "8-9pt regular",
      "secondary_note": "7-8pt regular",
      "tensor_shape": "6-7pt monospace/italic"
    },
    "stroke_hierarchy": {
      "container_border": "1.5pt solid",
      "internal_divider": "1.0pt solid",
      "flow_arrow": "1.5pt solid with 4px head",
      "feedback_arrow": "1.0pt dashed"
    }
  },
  "style_and_colors": {},
  "layout_and_content_blocks": [],
  "RENDERING_RULES_AND_NEGATIVE_PROMPT_INSTRUCTIONS": []
}
```

aspect_ratio is optional; copy it from the Figure Plan when provided, else "None".

## Block fields

| field | purpose | example |
|-------|---------|---------|
| `relative_position` | placement | `"Top Left"` |
| `shape` | border/fill | `"Dark Navy Blue (#1B3A5C) 2px dashed border, white fill"` |
| `exact_title_to_render_inside` | module title | `"Module A: Name"` |
| `exact_label` | primary label ≤ 2 words | `"Input"` |
| `exact_text` | locked on-figure text | `"MMPolymer Transformer\\nPredicts Tg"` |
| `exact_floating_text` | arrow/side notes | `"Valid linear polymer"` |
| `secondary_note` | optional smaller text ≤ 2 words | `"(ETKDGv3)"` |
| `caption_note` | off-figure caption content | full formula / params |
| `icon` | monochrome line art only | `"Compass icon, thin grey line art"` |
| `flow` | outgoing arrow | `"Horizontal arrow pointing RIGHT to Module B"` |
| `failure_branch` / `success_branch` | conditional edges | fail red / pass green |
| `branch_yes` / `branch_no` | diamond decision | yes → out; no → loop |
| `internal_content.layout` | inner layout | `"Three equal-width vertical columns"` |

## Text locks

- Every visible word lives in an `exact_*` field.
- `exact_label` ≤ 2 words; `secondary_note` ≤ 2 words; each `exact_text` line ≤ 5 words.
- Full formulas and parameter lists go to `caption_note`, not on-figure.

## Required rendering rules

```json
[
  "Render text ONLY within designated exact_* fields.",
  "All container boxes use WHITE (#FFFFFF) fill with COLORED BORDERS ONLY.",
  "Adhere to typography hierarchy: titles 10-12pt bold, labels 8-9pt, tensor shapes 6-7pt.",
  "Adhere to stroke hierarchy: containers 1.5pt, dividers 1.0pt, arrows 1.5pt.",
  "Icons are monochrome thin grey line art. No colored icons.",
  "Weight status MUST use dashed/solid borders or subtle pill tags ([Fixed] vs [Tune]).",
  "NO emojis, NO lock/fire/lightning decorative symbols, NO 3D rendering.",
  "Feedback loop arrows are DASHED. Main forward flow arrows are SOLID.",
  "Flat vector style: no gradients, no 3D, no decorative shadows.",
  "Canvas is pure white (#FFFFFF)."
]
```

Do not ask the model to “never render JSON keys” as a primary instruction; instead structure the spec so only `exact_*` values are content.

## Minimal example

```json
{
  "diagram_type": "Scientific Closed-Loop System Architecture",
  "diagram_title_rendering": "None",
  "style_and_colors": {
    "background": "White (#FFFFFF)",
    "main_block_color_palette": {
      "Module_A": "Dark Navy Blue (#1B3A5C) dashed border, white fill",
      "Module_B": "Medium Blue (#2E6B9E) dashed border, white fill"
    },
    "flow_arrow_colors": {
      "main_forward_flow": "Dark Grey (#4D4D4D) straight arrows",
      "feedback_loop": "Dark Grey (#4D4D4D) dashed curved arrow"
    }
  },
  "layout_and_content_blocks": [
    {
      "relative_position": "Top Left",
      "shape": "Rounded rectangular box, Light Blue thin border, white fill",
      "exact_text": "BRICS Fragment Library\\n→ Initial Population",
      "flow": "Horizontal arrow pointing RIGHT to Main Module"
    },
    {
      "relative_position": "Top Center",
      "shape": "Large rectangular container, Dark Navy Blue 2px dashed border, white fill",
      "exact_title_to_render_inside": "Module A: Name",
      "internal_content": {
        "layout": "Three equal-width vertical columns",
        "column_1": {
          "exact_header": "Sub-A",
          "icon": "compass icon",
          "exact_text_below_icon": "Operation"
        }
      },
      "flow": "Horizontal arrow pointing RIGHT to Module B"
    }
  ],
  "RENDERING_RULES_AND_NEGATIVE_PROMPT_INSTRUCTIONS": [
    "Render text ONLY within designated exact_* fields.",
    "All boxes use WHITE fill with COLORED BORDERS only."
  ]
}
```

## Format choice

| scene | format |
|-------|--------|
| framework / architecture / flowchart / module / comparison | **JSON** (default) |
| need exact per-slot text control | **JSON** |
| ≤ 3 modules, no branches, user asks for a prose prompt | text prompt |
| pure data chart / heatmap / curve / scatter | text prompt |

## Text prompt fallback skeleton

Four layers when JSON is not used:

1. Global description (type, venue style, layout)
2. `=== SECTION ===` blocks: panel bg, labels, white boxes with colored borders, sub-structure, optional mono thumbnails, sparse formulas, arrows
3. Global annotations (dims, skip links, legend)
4. STYLE SPECIFICATIONS with hex from `references/palettes.md`

Every module box has internal content — no empty shells.

## Thumbnail vocabulary (optional)

| data | phrase |
|------|--------|
| time series | `small time-series waveform thumbnail` |
| spectrum | `small frequency spectrum bar chart thumbnail` |
| attention | `small monochrome attention heatmap grid thumbnail` |
| trajectory | `small 3D orbital trajectory curve thumbnail` |
| distribution | `small probability distribution bar chart thumbnail` |
| decision tree | `small decision tree branching diagram thumbnail` |
| confusion matrix | `small confusion matrix heatmap thumbnail` |
| loss curve | `small training loss convergence curve thumbnail` |
| ROC | `small ROC curve with AUC shading thumbnail` |
| heatmap | `small spatial heatmap overlay thumbnail` |

# JSON to Image Prompt Conversion

How to convert a JSON figure spec into a descriptive image prompt that image generation models can follow.

The JSON spec is structured for agents; image models need natural language. Do NOT dump JSON at the model. Translate it using these rules.

## Conversion process

### 1. Extract image type from `diagram_type`

| JSON value | Prompt opening |
|------------|---------------|
| `*Overall Framework*` | "Flat vector academic architecture diagram showing [system] overall framework" |
| `*Network Architecture*` | "Flat vector academic network architecture diagram of [network]" |
| `*Module Detail*` | "Flat vector academic module detail diagram showing [mechanism]" |
| `*Comparison*` | "Flat vector academic comparison diagram" |
| `*Data Behavior*` | "Flat vector academic data visualization figure" |

### 2. Convert `style_and_colors` to material instructions

```json
"main_block_color_palette": ["#0072B2", "#E69F00", "#009E73"]
```
→ "Color palette: primary #0072B2, secondary #E69F00, tertiary #009E73. All boxes white fill with 2px colored borders and 6px corner radius."

```json
"flow_arrow_colors": {"main_forward_flow": "...solid arrows", "feedback_loop": "...dashed curved arrow"}
```
→ "Forward flow arrows solid dark grey #4D4D4D. Feedback/skip arrows dashed curved."

If palette is monochrome (Nature Blue): state "Nature Blue monochrome: dark #1B3A5C, medium #2E6B9E, light #5BA0D0, pale #8EAEC4" and use these for border hierarchy.

### 3. Convert `layout_and_content_blocks` to spatial prose

Do NOT list blocks in JSON order. Group them by spatial relationship first.

**For each block, extract and translate:**

| JSON field | Prompt translation |
|-----------|-------------------|
| `relative_position` | spatial positioning ("at bottom center", "in the large central container", "on the left side") |
| `shape` | visual description ("rounded rectangle, 2.5px dark navy border, white fill") |
| `exact_title_to_render_inside` | block title, rendered as bold label |
| `exact_text` | secondary text inside block (keep ≤5 words per line) |
| `exact_label` | primary short label |
| `icon` | translate using `architecture-icons.md` vocabulary |
| `internal_content.layout` | describe internal arrangement ("vertical stack of 4 sub-blocks inside") |
| `internal_content.row_*` / `column_*` | describe each sub-element with its text and shape |
| `flow` | arrow connection, translate direction into natural language |
| `exact_status` | render as pill tag ("[Tune]" in accent color, "[Fixed]" in grey) |

**Group blocks by panel/section:**
- Blocks sharing a container → describe the container first, then its contents
- Sequential blocks → describe in flow order with arrows
- Parallel columns → "left column: ..., right column: ..."
- Disconnected blocks → explicitly state "separated by a gap, no connecting arrow"

### 4. Add supporting modules not in JSON

After describing all blocks, add:
- Dimension labels: infer from architecture (e.g., "(B,N,D)") and place in 9pt grey
- Token/pill representations where data flows
- A legend if border styles encode meaning
- Small icons for each major block (from architecture-icons.md)
- Side margin notes for model variants or sizes

### 5. Convert RENDERING_RULES to visual constraints

Take each rule and make it concrete:

```
"All container boxes use WHITE fill with COLORED BORDERS ONLY"
→ "All boxes white fill, no colored fills, 1.5-2px colored borders, 4-6px rounded corners"

"Icons are monochrome thin grey line art"
→ "Icons rendered as monochrome line art in the block's border color, no filled icons"

"Weight status MUST use dashed/solid borders or pill tags"
→ "Trainable modules solid borders with [Tune] pill; frozen modules dashed borders with [Fixed] pill"

"NO emojis, NO lock/fire/lightning decorative symbols, NO 3D"
→ "No emojis, no decorative icons, no gradients, no drop shadows, no 3D effects"
```

### 6. Add typography and closing

End with:
- "Font: clean sans-serif (Helvetica/Arial/Inter), titles 14-16pt bold, labels 11-12pt, dimension notes 9pt grey."
- "Aspect ratio [value from aspect_ratio field]."

## What NOT to do

1. **Do not include JSON in the prompt** — translate every field
2. **Do not list blocks mechanically** — describe spatial relationships and hierarchy
3. **Do not put long text on figure** — `caption_note` content stays off-figure; add "parameters and full formulas in figure caption, not rendered"
4. **Do not forget icons** — every major block needs a visual anchor
5. **Do not use vague style words** — "professional", "clean", "modern" must be followed by concrete instructions
6. **Do not exceed 400 words** — image prompts should be dense but not overwhelming

## Example conversion

JSON block:
```json
{
  "relative_position": "Center (large vertical container)",
  "shape": "Rounded rectangle, #1B3A5C 2.5px border, white fill",
  "exact_title_to_render_inside": "N x Block",
  "internal_content": {
    "row_1": {"exact_text": "LayerNorm"},
    "row_2": {"exact_text": "Causal Self-Attention", "secondary_note": "[Tune]"}
  },
  "flow": "Vertical arrow UP to Final LayerNorm"
}
```

Prompt translation:
> "Center: a large rounded rectangle container with 2.5px dark navy #1B3A5C border and white fill, titled 'N × Block' in bold. Inside, a vertical stack of sub-blocks: pale blue #8EAEC4 'LayerNorm', medium blue #2E6B9E 'Causal Self-Attention' with a small [Tune] pill and a tiny attention-heatmap icon, another 'LayerNorm', and 'MLP (4×)' with a small fan-out-fan-in icon. Two curved solid arrows run along the container's right edge, bypassing the first two and last two sub-blocks as residual connections."

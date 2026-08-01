# Image Prompt Guide for Academic Architecture Diagrams

How to turn a JSON figure spec into a production-grade image prompt for GPT-Image-2, Gemini NanoBanana, or similar models.

Adapted from the 8-slot structure of `gpt-image-2-prompting`: a strong prompt reads like a visual brief, not a pile of style words.

## The 8 slots, in order

1. **Image type** — always lead with this
2. **Core subject** — what architecture/system is shown
3. **Composition / layout** — spatial arrangement, flow direction, grouping
4. **Supporting modules** — icons, formulas, dimension labels, legends, token pills
5. **Visual tone** — concrete descriptors, not vague taste words
6. **Material / texture** — line weight, panel fills, border style
7. **Typography / labeling** — font family, size hierarchy, label placement
8. **Aspect ratio** — always last

## Slot-by-slot guidance

### 1. Image type

Start with the exact format. For academic figures:

- `flat vector academic architecture diagram`
- `scientific infographic, architecture overview`
- `academic network architecture diagram with panel grouping`
- `module detail diagram with formula annotations`

Do NOT start with style words ("professional", "beautiful"). The image type comes first.

### 2. Core subject

One sentence naming the system and its key contribution:

> "Decoder-only Transformer (nanoGPT/GPT-2 architecture) showing token embeddings through N repeated blocks to language model head."

> "Neural radiance field (NeRF) MLP with positional encoding, coarse-to-fine hierarchical sampling, and volume rendering."

### 3. Composition / layout

Describe the spatial arrangement concretely:

- Flow direction: `vertical bottom-to-top`, `horizontal left-to-right`, `two-column with encoder on left and decoder on right`
- Grouping: `grouped into colored panels`, `nested inside a large container`
- Visual hierarchy: `largest element is the central transformer stack`, `side panel shows GPT-2 size comparison`
- Connections: `residual arrows curve around the right edge`, `dashed weight-tying arrow loops from output back to embeddings`, `cross-attention arrows bridge horizontally between columns`

### 4. Supporting modules

This is what separates a diagram from a bunch of labeled boxes. Include:

| module | when to use | example prompt phrase |
|--------|-------------|----------------------|
| dimension labels | always | `small grey text "(B,N,D)" beneath each block` |
| formula | when ≤1 line core formula | `formula "x = x + attn(LN(x))" inside the residual arrow` |
| token/pill | data tokens, status tags | `black rounded pill "CLS", grey pills "SEP" "PAD", blue pill "[Tune]"` |
| icon/thumbnail | every major module | `small monochrome neural network node icon inside the embedding block` |
| legend | when colors encode meaning | `legend at bottom: blue=dashed=frozen, orange=solid=trainable` |
| parameter panel | side information | `right margin: small borderless text listing model sizes "124M / 350M / 774M / 1558M"` |
| data thumbnail | data types | `tiny mel spectrogram thumbnail`, `small attention heatmap grid`, `mini token sequence bar chart` |

### 5. Visual tone

Translate vague words into concrete instructions:

| vague | concrete |
|-------|----------|
| professional | clean grid alignment, consistent border radius, no overlapping elements |
| academic/scientific | thin 1.5px outlines, muted palette, sans-serif labels, generous but not empty spacing |
| publication-ready | 300dpi equivalent sharpness, no anti-aliasing artifacts, text readable at thumbnail size |
| modern | rounded 4-8px corners, subtle panel separation, grouped color coding |
| clean | no decorative elements, no gradients, no 3D, no shadows except panel grouping |

### 6. Material / texture

Specify exactly:

- `all boxes: white (#FFFFFF) fill with 1.5-2px colored borders, 4-6px corner radius`
- `panels: very light tinted fill (#F0F4FF or #F5F5F5) with 1px same-hue darker border`
- `arrows: dark grey (#4D4D4D), solid for forward flow, dashed for feedback/skip`
- `icons: monochrome line art in the block's border color, no filled color icons`
- `NO gradients, NO drop shadows on individual boxes, NO 3D effects`

### 7. Typography / labeling

- Font: `clean sans-serif (Helvetica/Arial/Inter), labels 12-14pt, titles 16-18pt semibold`
- Module titles inside boxes: ≤5 words
- Secondary labels (dimensions, notes): 9-10pt grey
- Every visible text string must be specified verbatim in the prompt
- Caption material (long formulas, parameter lists) should be noted as "not rendered — see caption"

### 8. Aspect ratio

Always end with: `Aspect ratio 16:9.` or `4:3.` etc.

## Common mistakes to avoid

1. **Listing boxes without layout** — "Box A, Box B, arrow" tells the model nothing about spatial arrangement
2. **Too much on-figure text** — parameters like `D=8 W=256 skip=[4]` go in caption, not on the figure
3. **No visual anchors** — every major block needs an icon, thumbnail, or distinct shape, not just a title
4. **Forgetting supporting modules** — dimension labels, legends, and token pills make the figure feel designed
5. **Vague style words** — "professional", "clean", "modern" must be translated to concrete visual instructions
6. **Nested box-in-box** — use panel backgrounds + grouped elements instead of one box containing another box containing another

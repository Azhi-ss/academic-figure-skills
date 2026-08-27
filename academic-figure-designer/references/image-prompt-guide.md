# Image Prompt Guide for Academic Figures

An image prompt is a rendering adapter for FigureSpec v1. It should preserve evidence-backed topology and a concrete visual grammar while avoiding production instructions that the model may draw as text.

## Before writing

Confirm:

- the figure's communication goal and hero element;
- the closed component and connection lists;
- exact visible strings and caption-only material;
- the selected style profile or extracted reference grammar;
- backend suitability for text density and topology complexity.

If the user supplied a reference image, pass that image directly to a capable renderer. The prose prompt describes what to transfer—composition, stroke, fill, typography, spacing, illustration level—and what not to copy—scientific content, labels, branding, or method topology.

## Prompt structure

Use this order when it helps; omit slots that add no information.

1. **Image type and communication goal**
2. **Hero composition and semantic regions**
3. **Required components and typed connections**
4. **Visible-text closed list**
5. **Style grammar and semantic color tokens**
6. **Typography, spacing, and publication-scale legibility**
7. **Observed-defect-oriented negative constraints**
8. **Aspect ratio**

### Image type and goal

Prefer precise descriptions:

- `illustrated modular academic systems framework`
- `technical vector network architecture`
- `editorial scientific mechanism infographic`
- `comparison figure with deterministic plots and a conceptual inset`

Do not lead with unsupported venue stereotypes such as “Nature style” or vague taste words such as “premium.” Default to no global canvas title because the figure title normally belongs in the paper's external caption. If the user, FigureSpec, or supplied reference explicitly requires one, render exactly one short title with reserved whitespace and never turn it into a full-width banner.

### Composition

Describe proportions, hierarchy, and reading order:

- `a research loop occupies the left 40%; two supporting regions stack on the right`;
- `a central mechanism is twice the visual weight of the context panels`;
- `three responsibility zones are separated by a labeled authority boundary`.

Use pipelines only for genuinely sequential executed flows. Loops, storyboards, asymmetric modular collages, layered boundaries, and central mechanisms are first-class layouts. Allow one level of nested subcards when the scientific hierarchy needs it.

### Components and topology

Describe only FigureSpec components. State connection endpoints and line semantics exactly, then say that no other inter-module connections should appear. Keep exception and no-budget branches visibly distinct from normal execution.

### Supporting visuals

Use an icon, mini-plot, token, formula, dimension, badge, or legend only when it explains sourced content. They are not mandatory decorations.

| Visual | Use when |
|---|---|
| Hero illustration | It communicates the main mechanism or loop faster than boxes |
| Line-art anchor | It disambiguates a major semantic role |
| Formula/dimension | It is essential, sourced, and readable at final scale |
| Legend | Two or more non-obvious encodings require decoding |
| Status pill or hatch | A state such as fixed/trainable or advisory/executed must be dual-encoded |

### Style grammar

Specify observable decisions instead of a palette name alone:

- composition and permitted nesting;
- flat/tinted/white fills and shadow policy;
- stroke weight, curvature, joins, and arrowheads;
- technical, rounded, or hand-drawn typography character;
- monochrome, limited-accent, or illustrated line art;
- paired region tokens: soft fill, dark outline/title, optional icon accent.

Examples:

- `illustrated modular: low-saturation region fills, 3px-equivalent same-hue dark outlines, rounded hand-lettered headings, no shadows`;
- `technical vector: mostly white modules, restrained tints for groups, 1.5px-equivalent strokes, neutral sans-serif labels`;
- `airy UI: white floating panels, restrained soft shadow, color carried by pills and curves`.

### Typography

Use a relative hierarchy and final-scale constraint instead of conflicting absolute point sizes:

- region headings clearly dominant;
- module labels readable at the intended 89 mm or 183 mm width;
- secondary notes omitted before they become sub-7pt equivalent;
- exact visible strings explicitly listed;
- no JSON keys, hex values, `WHITE FILL`, `300 DPI`, or production notes rendered.

An image model cannot guarantee exact text. RenderAudit must inspect it; text-heavy figures should use deterministic vector text or a hybrid overlay.

## Common failures

1. Equal-weight boxes erase the scientific focal point.
2. Directory order or JSON order is mistaken for narrative order.
3. Style is reduced to hex values while composition and marks remain generic.
4. Decorative icons, dimensions, legends, and formulas are added without evidence.
5. A reference image is summarized in prose but not supplied to the image tool.
6. Production instructions leak into visible labels.
7. Successful API return is mistaken for publication readiness.
8. An unintended, duplicated, or full-width title banner wastes vertical figure height or conflicts with the paper's LaTeX caption.

## Completion

A prompt is ready when it is the shortest lossless rendering brief for FigureSpec, the reference assets are attached appropriately, and RenderAudit has objective checks for topology, text, layout, background, accessibility, and style fidelity.

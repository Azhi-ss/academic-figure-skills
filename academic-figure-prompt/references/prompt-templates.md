# Prompt Templates for Academic Figures

Fill-in-the-blank templates for each figure type. Replace `[bracketed]` values with content from the analysis. All templates follow the 8-slot structure from `image-prompt-guide.md`.

## Template 1: Overall Framework (end-to-end pipeline)

```
Flat vector academic architecture diagram showing [system name] overall framework on a pure white #FFFFFF canvas, 16:9. [brief one-sentence description of what the system does].

Horizontal left-to-right flow, [N] main stages connected by solid dark grey #4D4D4D arrows: [stage 1] → [stage 2] → [stage 3] → [stage 4]. Each stage is a rounded rectangle (6px corner radius, 2px colored border, white fill) with a [monochrome line art icon] inside, title in bold 14pt sans-serif, and [short label] below.

Supporting elements: [dashed feedback arrow from X back to Y labeled "loss"], [dimension labels "(B,N,D)" in 9pt grey beneath relevant blocks], [legend at bottom explaining border styles].

Color palette: [primary #hex, secondary #hex, tertiary #hex], ≤3 chromatics. Panels grouped by very light tinted backgrounds (#F0F4FF for [group A], #F5F5F5 for [group B]).

Style: clean sans-serif (Helvetica/Arial), thin 1.5-2px outlines, no gradients, no shadows, no 3D, no emojis, no decorative elements. All text in designated label areas. Aspect ratio 16:9.
```

## Template 2: Network Architecture (internal structure)

```
Flat vector academic network architecture diagram of [network name] on a pure white #FFFFFF canvas, 16:9. [one sentence: e.g., "Decoder-only Transformer with token and position embeddings, N repeated blocks, and weight-tied language model head."]

[Vertical bottom-to-top / two-column left-right] layout. Main structure is a large rounded container with [2.5px primary color border] titled "[Container Name]", containing [N] vertically stacked sub-blocks:
- [sub-block 1]: [shape/color], icon: [icon phrase from architecture-icons.md], label "[name]"
- [sub-block 2]: ...
- residual connections: [two curved solid dark grey arrows on the right side, bypassing sub-blocks 1+2 and 3+4]

[Outside/above/below the container]: [input/output blocks with icons].
[Dashed curved arrow describing skip/weight-typing connection].

Supporting elements: dimension labels "(B,N,D)" in 9pt grey, [model size variants in right margin: "124M / 350M / 774M / 1558M"], [formula ≤1 line if core: "x = x + attn(LN(x))"].

Color palette: Nature Blue monochrome — dark #1B3A5C, medium #2E6B9E, light #5BA0D0, pale #8EAEC4, grey #4D4D4D for arrows. White fills, colored borders only. Font: Helvetica/Arial 12-14pt. No gradients, no shadows, no 3D. Aspect ratio 16:9.
```

## Template 3: Module Detail (mechanism zoom-in)

```
Flat vector academic module detail diagram showing [mechanism name] on a pure white #FFFFFF canvas, 4:3. [one sentence describing the mechanism and its role in the larger system].

Central composition: [large central block] showing [internal operation], with [inputs arriving from left/top] and [outputs exiting right/bottom]. The central mechanism is rendered as [specific visual: e.g., "a stack of layers with Q/K/V projections shown as three diverging arrows merging into attention weights"].

Surrounding annotations: [formula in italic serif: "Attention(Q,K,V) = softmax(QK^T/√d)V"], [dimension labels], [arrow labels "Q" "K" "V" in 10pt], [small inset showing the module's position in the full architecture with a highlighted region].

Supporting modules: [legend explaining color coding], [caption note area at bottom marked "see caption" for long formulas].

Color palette: [≤2 chromatics from selected palette], dark grey for text and arrows. Thin 1.5px outlines, 4px rounded corners, white fills. Monochrome icons in block border color. No gradients, no shadows, no 3D. Font: sans-serif titles 16pt, body 11pt, math in serif italic. Aspect ratio 4:3.
```

## Template 4: Comparison / Ablation

```
Flat vector academic comparison diagram on a pure white #FFFFFF canvas, 16:9. [N] variants of [system/module] shown side-by-side in a grid.

[N×M grid] with equal-sized panels, each panel has:
- title in bold 14pt: "[variant name]"
- simplified architecture thumbnail showing [the key difference]
- [metric or label] below in 11pt
- highlighted difference using [accent color #hex]

Ours panel: [thicker 2.5px border in accent color], small "ours" pill tag.
Baseline panels: [1px grey border].

Supporting modules: [arrow or bracket indicating the axis of variation], [shared legend], [horizontal axis label].

Color palette: primarily grey #CCCCCC for baselines, one accent [primary #hex] for ours, white fills. Clean sans-serif, thin outlines, no shadows or 3D. Aspect ratio 16:9.
```

## Template 5: Data Behavior (curves / heatmaps / embeddings)

```
Flat vector academic data behavior figure on a pure white #FFFFFF canvas, 4:3. [What data is shown: e.g., "Training and validation loss curves", "Cross-attention alignment heatmap", "t-SNE embedding clusters"].

Main plot area centered, [axes with labels in 11pt], [data rendered as curves/heatmap/scatter in palette colors]:
- [series 1]: [color, line style, label]
- [series 2]: ...
- [annotations: peak, convergence point, or highlighted region with arrow]

Supporting modules: legend at [top/right], axis labels "[X axis]" and "[Y axis]", [small schematic inset showing data source], [confidence interval shading if applicable].

Color palette: [≤3 chromatics], data lines 1.5-2px, grid lines 0.5px light grey. No chart junk, no 3D pie charts. Font: sans-serif 10-12pt. Aspect ratio 4:3.
```

## Quick fill checklist

Before finalizing any prompt, verify all 8 slots are present:

- [ ] Image type stated first ("flat vector academic ... diagram")
- [ ] Core subject named in one sentence
- [ ] Composition described (flow direction, grouping, hierarchy, connections)
- [ ] ≥2 supporting modules (icons, dimensions, formulas, pills, legend)
- [ ] Visual tone concretized (no "professional" without specifics)
- [ ] Material/texture specified (border width, fill, corner radius)
- [ ] Typography specified (font family, size, hierarchy)
- [ ] Aspect ratio stated last

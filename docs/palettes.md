# Academic Palettes — Single Source of Truth

This file defines **12 classic presets**, three pastel-airy schemes, and paired illustrated semantic-zone tokens. Skills that need hex values or style routing should load this file rather than maintaining private copies.

## Decision order

Apply evidence in this order:

1. explicit user colors, style, print, and accessibility requirements
2. supplied reference image grammar
3. hard production constraints such as grayscale output and text contrast
4. figure semantics and visual-zone relationships
5. an existing paper-wide visual system or explicit submission rule
6. conservative default

A reference image is the highest-priority inferred style source. Extract composition, panel surfaces, outline strength, shadow treatment, typography character, icon style, nesting depth, density, arrow grammar, and paired fill/outline colors. Match those properties without copying the reference's labels, branded assets, or method content.

`module_count` is a density clue only. It does not trigger monochrome. Choose hue count from the number and relationship of semantic zones shown in the figure.

| Missing evidence | Conservative default |
|---|---|
| No reference or style cue, classic technical figure | **Okabe-Ito** |
| Explicit airy UI/token figure | **P2 Cool Research** |
| Narrative framework or agent/scientific workflow | **I1 Illustrated Zones** |
| Accessibility unspecified | colorblind-aware dual encoding and validated text contrast |

Always state the branch (`user`, `reference`, `scene`, or `default`) and offer one alternate.

## Style profiles first

Palette values only make sense with a surface and line treatment. Select a profile before assigning tokens.

| Signals | Profile | Primary skill | Visual grammar |
|---|---|---|---|
| technical stack, compact network, classic vector, strict print | **`classic-technical`** | `academic-figure-designer` | restrained geometry, fine borders, white or near-white modules, compact sans labels |
| airy, token flow, interface-like, soft cards | **`pastel-airy-ui`** | `academic-figure-designer` | white cards, subtle border/shadow, floating pills and tokens, generous whitespace |
| hand-drawn academic infographic, modular narrative, agent/scientific workflow, tinted zones | **`illustrated-modular`** | `academic-figure-designer` | asymmetric hero layout, soft semantic-zone fills, strong same-hue outlines, no shadow, one-level subcards, controlled line illustrations |
| supplied reference does not fit one preset | **`reference-led`** | `academic-figure-designer` | override defaults with observed grammar; do not assume an illustrated surface |

Do not force a supplied reference into a binary classic/pastel label. A coherent figure may combine a classic flat canvas, tinted modular zones, and hand-drawn illustrations. State the observed properties so the combination is intentional rather than a style-word mixture.

### Pastel airy UI schemes

Small body text remains neutral `#24323D`. The colored values below are heading accents on white; validate them again before placing small text on a tinted token.

| Scheme | Scene | Soft fills | Accessible heading accents on white |
|---|---|---|---|
| **P1 Warm ML** | playful, teaching, human-centered | `#FFD0D0` `#BBDEFB` `#FFF3C4` `#E1BEE7` `#C8E6C9` | `#A93636` `#146C61` `#6A5ACD` `#2F7430` |
| **P2 Cool Research** | calm token-centric research figure | `#B3E5FC` `#C5CAE9` `#CFD8DC` `#B2DFDB` `#D1C4E9` | `#1565C0` `#3949AB` `#006F65` |
| **P3 Earthy Warm** | natural or embodied visual direction | `#FFE0B2` `#D7CCC8` `#C8E6C9` `#E0E0E0` `#EFEBE9` | `#6D4C41` `#827717` `#2E7D32` |

If a reference is present, derive its token pairs instead of snapping every soft figure to the nearest P1–P3 scheme.

---

## I1 Illustrated Zones — paired semantic tokens

Each token is a coordinated surface system rather than a standalone accent. `title_text` values meet normal-text contrast against their paired fills; small body text may use neutral `#24323D` throughout.

| Token | `soft_fill` | `dark_outline` | `title_text` | `icon_accent` |
|---|---|---|---|---|
| **I1 Blue** | `#EDF4FB` | `#194166` | `#163E64` | `#2E6B9E` |
| **I1 Green** | `#F3FBF0` | `#3B7D23` | `#2F681D` | `#4E8D36` |
| **I1 Peach** | `#FBE3D6` | `#A94417` | `#9E3F13` | `#C65A22` |
| **I1 Purple** | `#F5ECF5` | `#77206E` | `#65185E` | `#8B3B83` |
| **I1 Cyan** | `#DBF3FE` | `#236E96` | `#195876` | `#2F81A8` |
| **I1 Gold** | `#FBF1D1` | `#856B1B` | `#66500F` | `#9B7B1C` |
| **I1 Coral** | `#FDE8E5` | `#B83A2F` | `#8F2A24` | `#C94D42` |

Recommended material treatment: white canvas; 1.5–2.5px zone outlines; 6–14px corner radius scaled to output size; no drop shadows; white or lighter same-hue subcards; dark neutral arrows `#334155` unless the edge itself carries a zone meaning.

## Semantic color binding contract

Bind tokens to the roles present in the current paper and retain those bindings across its figures. The mappings below are customizable defaults across different scientific domains:

### 1) Standard Multi-Stage Pipeline & Modular Systems
| Domain Role / Stage | Suggested Illustrated Token | Classic/Airy Adaptation |
|---|---|---|
| **Stage 1: Input / Raw Data / Context** | I1 Green (`#F3FBF0` / `#3B7D23`) | Green accent / data pill |
| **Stage 2: Representation / Encoders** | I1 Blue (`#EDF4FB` / `#194166`) | Blue outline / primary container |
| **Stage 3: Core Mechanism / Transformation** | I1 Peach (`#FBE3D6` / `#A94417`) | Orange/peach hero zone |
| **Stage 4: Optimization / Supervision / Loss** | I1 Purple (`#F5ECF5` / `#77206E`) | Purple accent / dashed constraint |
| **Stage 5: Output / Evaluation / Benchmark** | I1 Gold (`#FBF1D1` / `#856B1B`) | Gold heading / output badge |

### 2) Deep Learning & Neural Architectures
| Architecture Component | Suggested Illustrated Token | Visual Metaphor / Shape |
|---|---|---|
| **Raw Input / Embeddings / Tokens** | I1 Green | Structured grid, token pill, or feature map |
| **Backbone / Feature Extractor** | I1 Blue | Layered orthogonal blocks or stacked cards |
| **Cross-Modal Fusion / Attention Core** | I1 Peach | Heatmap matrix or bipartite connection web |
| **Loss Function / Objective / Regularizer** | I1 Purple | Mathematical constraint box or curve |
| **Prediction Head / Downstream Task** | I1 Gold | Terminal prediction pill or task badge |

### 3) Agentic & Scientific Interactive Loops
| Agentic Role | Suggested Illustrated Token | Visual Metaphor / Shape |
|---|---|---|
| **Reasoning / Policy / Planner** | I1 Blue | Decision glyph, thought bubble, or planning box |
| **Evidence / Context / Observation** | I1 Green | Document icon, coordinate plot, or context card |
| **Deterministic Harness / Tool Execution**| I1 Peach | Solid process container or simulation box |
| **Advisory / Feedback / Uncertainty** | I1 Purple | Dashed feedback arrow or advisory pill |
| **Memory / Storage / Provenance** | I1 Cyan | Network graph or database/checkpoint cylinder |
| **Final Output / Report** | I1 Gold | Formatted report card or badge |
| **Exception / Guardrail / Stop** | I1 Coral | Warning badge or coral STOP boundary |

Repeated roles reuse a token; adjacent unrelated zones should also differ by label, geometry, or line style.

---

## Scene → profile and palette decision

After explicit user and reference-grammar requirements, apply production constraints and then choose from figure semantics. Venue and domain are suggestions, not guarantees of a single visual style.

### 1) Hard constraints

| Constraint | Choose | Alternate |
|------------|--------|-----------|
| Strict B&W / grayscale print only | **Print-Safe Gray** | Grayscale |
| Theory paper, no color budget | **Grayscale** | Print-Safe Gray |
| Color-vision accessibility required or prudent | Start from Okabe-Ito / ML TopConf Colorblind / a verified monochrome ramp, then dual-encode and test | Never treat a palette name as proof of accessibility |
| Must match existing Matplotlib Tab10 experiment plots | **ML TopConf Tab10** | ML TopConf Colorblind if a11y matters more than match |
| Reference has tinted zones and strong outlines | **Illustrated modular + derived pairs** | I1 Illustrated Zones |

### 2) Figure type

| Figure type | Prefer | Alternate | Why |
|-----------|--------|-----------|-----|
| Overall Framework, technical pipeline | Okabe-Ito | ML TopConf Colorblind | clear categorical accents |
| Overall Framework, modular narrative | **Illustrated modular + I1** | reference-derived pairs | semantic zones and hierarchy |
| Network Architecture | Okabe-Ito or Blue Monochrome | Nature Blue for a restrained single-family stack | structure > decoration |
| Module Detail | **Blue Monochrome** | Okabe-Ito | detail density; gray-print friendly |
| Comparison / Ablation (few panels) | Purple-Green | Okabe-Ito | category contrast |
| Dense multi-panel ablation | **ML TopConf Deep** | Purple-Green | softer multi-hue grid |
| Data Behavior (curves / heatmaps / t-SNE) | ML TopConf Colorblind | Okabe-Ito | series/categories stay separable |
| Qualitative image grids | Okabe-Ito accents only | Grayscale frames | color on labels, not photo washes |

### 3) Venue and domain constraints

Do not map a venue or research domain directly to a palette. Use venue/domain
information only when it supplies a concrete production constraint: an official
grayscale rule, an existing paper-wide color system, a required plot palette,
an accessibility requirement, or a reference figure. Otherwise choose from the
content relationships above. “Nature”, “CVPR”, “biology”, “materials”, or
“robotics” alone is not a color instruction.

### 4) Vibe words → concrete choice

| User says | Family | Palette / scheme |
|-----------|--------|------------------|
| 高级 / 克制 / 顶刊 | ask for observable traits or use a supplied reference | no venue-name palette default |
| 科技感 / 工程感 / 干净 | `classic-technical` | Blue Monochrome or Okabe-Ito |
| 柔和 / 空气感 / token 卡片 | `pastel-airy-ui` | P2 |
| 手绘 / 叙事 / 模块拼图 / agent 框架 | `illustrated-modular` | I1 or reference-derived pairs |
| 活泼 / 教学感 | `pastel-airy-ui` or `illustrated-modular` | P1 or reference-derived pairs |
| 自然 / 生物感 | classic Warm Earth, airy P3, or illustrated zones | state accessibility tradeoff |
| 不要花 | any coherent profile | reduce active semantic zones; monochrome only if hierarchy remains clear |
| 和实验曲线一个色 | `classic-technical` | ML TopConf Tab10 / Colorblind |
| 黑白印刷 | `classic-technical` | Print-Safe Gray / Grayscale |

---

## Worked decision recipes

| Scenario | Family | Palette | One-line reason |
|----------|--------|---------|-----------------|
| Technical three-stage method pipeline, no reference | `classic-technical` | Okabe-Ito | categorical accents and compact geometry |
| Modular agent/scientific framework, no reference | `illustrated-modular` | I1 Illustrated Zones | semantic zones plus asymmetric hierarchy |
| Reference with tinted panels and dark outlines | `reference-led` (observed illustrated grammar) | derived paired tokens | preserve observed visual grammar without assuming every reference is illustrated |
| Dense 2×3 ablation grid | `classic-technical` | ML TopConf Deep | multiple comparable panels |
| Token-flow explainer with white cards | `pastel-airy-ui` | P2 | token-centric surface grammar |
| Continuous single-family mechanism with an explicit restrained-blue preference | `classic-technical` | Nature Blue | user request and hierarchy support one hue family |
| Strict B&W journal output | `classic-technical` | Print-Safe Gray | hard print constraint |
| Human-centered concept diagram | `pastel-airy-ui` or reference-supported `illustrated-modular` | content/reference dependent | distinguish UI cards from narrative zones |
| High-density module detail with no reference | `classic-technical` | Blue Monochrome or accessible custom | detail density and print behavior |
| User: 配色随便 | profile from content; Okabe-Ito/P2/I1 | profile default | safe default branch |

---

## Decision checklist (emit with every Palette Decision)

1. Explicit user constraints recorded.
2. Reference grammar summarized, or `no reference supplied`.
3. Canonical profile: `classic-technical` / `pastel-airy-ui` / `illustrated-modular` / `reference-led`.
4. Hard constraint fired? (print / accessibility / match existing plots).
5. Semantic zones and color carriers identified.
6. Primary + alternate named with exact classic colors or paired tokens.
7. Small-text contrast and grayscale dual encoding checked.
8. Branch stated: `user` / `reference` / `scene` / `default`.


## Palette Decision handoff

Downstream skills consume:

```
style_profile: <classic-technical | pastel-airy-ui | illustrated-modular | reference-led>
style_preset: <named library variant | none>
reference_grammar: <summary | none>
palette_or_token_set: <name>
canvas / body_text / arrow / divider: <hex>
semantic_zone_tokens:
  <role>: {soft_fill: <hex>, dark_outline: <hex>, title_text: <hex>, icon_accent: <hex>}
reason: <one line>
accessibility: colorblind-aware-tested | needs dual encoding/testing | print-only
```

---

## 1. Okabe-Ito — default polychrome

**Use:** general categorical starting palette when several roles need distinct hues; always add non-color cues and test the rendered figure

| role | hex | use |
|------|-----|-----|
| primary | `#0072B2` | core module borders, section labels |
| secondary | `#E69F00` | secondary borders, alternate highlight |
| tertiary | `#009E73` | output / result (sparse) |
| text | `#333333` | body text |
| fill | `#FFFFFF` | canvas / boxes |
| section_bg | `#F7F7F7` | region grouping |
| border | `#767676` | semantic outline (4.54:1 on white) |
| arrow | `#4D4D4D` | arrows / lines |

---

## 2. Blue Monochrome

**Use:** module detail; grayscale-friendly journals

| role | hex |
|------|-----|
| primary | `#1565C0` |
| secondary | `#42A5F5` |
| tertiary | `#90CAF9` |
| text | `#212121` |
| fill | `#FFFFFF` |
| section_bg | `#F5F8FC` |
| border | `#607D8B` |
| arrow | `#37474F` |

---

## 3. Warm Earth

**Use:** explicit earth-toned user/reference direction. Dual-encode; do not infer this palette from a research domain alone.

| role | hex |
|------|-----|
| primary | `#C0392B` |
| secondary | `#E67E22` |
| tertiary | `#F39C12` |
| text | `#2C2C2C` |
| fill | `#FFFFFF` |
| section_bg | `#FDF6EC` |
| border | `#8D6E63` |
| arrow | `#5D4037` |

---

## 4. Purple-Green

**Use:** two-category comparison or ablation when purple/green fits the labels and reference; never bind a hue to “ours” without the spec

| role | hex |
|------|-----|
| primary | `#6A1B9A` |
| secondary | `#2E7D32` |
| tertiary | `#AB47BC` |
| text | `#1A1A1A` |
| fill | `#FFFFFF` |
| section_bg | `#F8F5FC` |
| border | `#7B1FA2` |
| arrow | `#4A148C` |

---

## 5. Grayscale

**Use:** explicit grayscale/print-only requirement or a user-selected austere monochrome treatment

| role | hex |
|------|-----|
| primary | `#212121` |
| secondary | `#616161` |
| tertiary | `#9E9E9E` |
| text | `#111111` |
| fill | `#FFFFFF` |
| section_bg | `#F5F5F5` |
| border | `#757575` |
| arrow | `#424242` |

Distinguish categories by shape / line weight, not hue.

---

## 6. Teal-Coral

**Use:** explicit teal/coral two-category contrast. Dual-encode and test for color-vision deficiencies.

| role | hex |
|------|-----|
| primary | `#00695C` |
| secondary | `#E64A19` |
| tertiary | `#26A69A` |
| text | `#212121` |
| fill | `#FFFFFF` |
| section_bg | `#F0F9F8` |
| border | `#00796B` |
| arrow | `#004D40` |

---

## 7. ML TopConf Tab10

**Use:** match an existing Matplotlib Tab10 experiment palette; do not choose from venue name alone

| role | hex |
|------|-----|
| primary | `#1F77B4` |
| secondary | `#FF7F0E` |
| tertiary | `#2CA02C` |
| text | `#1F2937` |
| fill | `#FFFFFF` |
| section_bg | `#F8FAFC` |
| border | `#64748B` |
| arrow | `#334155` |

---

## 8. ML TopConf Colorblind

**Use:** muted colorblind-aware categorical starting palette; still requires dual encoding and rendered-output checks

| role | hex |
|------|-----|
| primary | `#0173B2` |
| secondary | `#DE8F05` |
| tertiary | `#029E73` |
| text | `#1F2937` |
| fill | `#FFFFFF` |
| section_bg | `#F8FAFC` |
| border | `#64748B` |
| arrow | `#334155` |

---

## 9. ML TopConf Deep

**Use:** multi-panel ablation / dense comparison grids

| role | hex |
|------|-----|
| primary | `#4C72B0` |
| secondary | `#DD8452` |
| tertiary | `#55A868` |
| text | `#1F2937` |
| fill | `#FFFFFF` |
| section_bg | `#F8FAFC` |
| border | `#64748B` |
| arrow | `#334155` |

---

## 10. Print-Safe Gray

**Use:** explicit strict black-and-white print requirement

| role | hex |
|------|-----|
| primary | `#000000` |
| secondary | `#333333` |
| tertiary | `#666666` |
| text | `#333333` |
| fill | `#FFFFFF` |
| section_bg | `#F7F7F7` |
| border | `#666666` |
| arrow | `#4D4D4D` |

---

## 11. Journal Standard

**Use:** figures with several verified categories that genuinely need additional accents; not a journal-name default

| role | hex |
|------|-----|
| primary | `#1F77B4` |
| secondary | `#FF7F0E` |
| tertiary | `#2CA02C` |
| accent1 | `#D62728` |
| accent2 | `#9467BD` |
| accent3 | `#8C564B` |
| text | `#1F2937` |
| fill | `#FFFFFF` |
| section_bg | `#F8FAFC` |
| border | `#64748B` |
| arrow | `#334155` |

Activate only the category colors needed by the current comparison and repeat them consistently.

---

## 12. Nature Blue — restrained monochrome

**Use:** a continuous single-family hierarchy, an explicit restrained-blue direction, matching reference grammar, or verified grayscale-friendly output. Do not select it from module count, venue, or domain alone.

| role | hex |
|------|-----|
| primary | `#1B3A5C` |
| secondary | `#2E6B9E` |
| tertiary | `#5BA0D0` |
| gray | `#8EAEC4` |
| text | `#333333` |
| fill | `#FFFFFF` |
| section_bg | `#F7F7F7` |
| border | `#5B7890` |
| arrow | `#4D4D4D` |

---

## Monochrome vs semantic-zone color

| | monochrome (Blue Monochrome / Nature Blue) | semantic-zone color (Okabe-Ito / I1 / custom pairs) |
|---|---|---|
| visual unity | one hue family | coordinated role-based pairs |
| separation | lightness + border + label | fill/outline pair + label + shape |
| best when | hierarchy within one conceptual family | readers must scan distinct subsystems or decisions |
| print / colorblind | usually robust after value check | robust when dual-encoded and contrast-checked |

---

## Production checks

- Preserve explicit user constraints and reference-image grammar unless accessibility or print requirements require an explained adjustment.
- Use white, near-white, or soft tinted panel surfaces according to the selected profile; tinted semantic zones are valid academic material.
- Use the fewest semantic tokens that keep roles easy to scan, without an arbitrary module-count or three-hue cutoff.
- Dual-encode important categories with label, shape, border, icon, or line style in addition to color.
- Normal-size text and its actual background should meet a 4.5:1 contrast target; do not use pale accent colors for small text.
- Essential outlines, arrow shafts/heads, markers, and focus boundaries should meet a 3:1 graphical contrast target against adjacent colors. Lighter dividers may be decorative only and must not carry meaning.
- Avoid unintentional gradients, glossy 3D chrome, photorealistic decoration, and rainbow ordering. Follow a supplied reference when a different treatment is deliberate and legible.
- Check the downscaled figure and a grayscale preview before handoff.

## Custom palette minimum

```
style_profile: <name>
canvas: #XXXXXX
body_text: #XXXXXX
arrow: #XXXXXX
semantic_zone:
  soft_fill: #XXXXXX
  dark_outline: #XXXXXX
  title_text: #XXXXXX
  icon_accent: #XXXXXX
```

Add only the semantic zones the figure needs. Validate text contrast, colorblind distinguishability, and grayscale reproduction before handoff.

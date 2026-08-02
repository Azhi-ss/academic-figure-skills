# Academic Palettes — Single Source of Truth

**12 presets.** All skills that need hex values or venue mapping load this file. Do not copy tables into other skills.

## Default rule

Decision order: `user-specified` → `scene recommendation` → `safe default`.

| Condition | Default |
|-----------|---------|
| Framework / architecture with **≥ 4 modules** | **Nature Blue** |
| Otherwise, or unknown module count | **Okabe-Ito** |
| Accessibility unspecified | treat as colorblind-safe required |
| Pastel / ICLR airy style | use `academic-figure-prompt-pastel` schemes (P1–P3), not this file |

Always state which branch produced the choice and offer one alternate.

## Style family first (classic vs pastel)

Palette hex is useless until the **drawing style** is fixed. Choose family before preset.

| Signals from user / venue | Style family | Skill | Look |
|---------------------------|--------------|-------|------|
| NeurIPS / ICML / ICLR diagrams requested as “classic / box-border / JSON spec” | **Classic academic** | `academic-figure-prompt` | white fill, **colored borders only**, sans technical, flat vector |
| ICLR / NeurIPS / ICML "2024–2025 感觉" / pastel / airy / soft / token 流动 / 现代 ML | **Pastel airy** | `academic-figure-prompt-pastel` | white panels + soft shadow, rounded type, pastel **tokens/pills** (not border-only boxes) |
| User pastes a reference | Match reference family first | same as above | extract whether borders-or-tokens dominate |

Rules:

- Classic → pick one of the **12 presets below**.
- Pastel → pick **P1 / P2 / P3** in `academic-figure-prompt-pastel` (do not force Okabe-Ito hex onto pastel tokens).
- Never mix families in one figure (no Okabe-Ito borders + pastel token soup).

### Pastel scheme map (style family = airy only)

| Scene | Scheme | Why |
|-------|--------|-----|
| default modern ML / systems / NLP framework | **P2 Cool Research** | calm, research-poster default |
| teaching / playful / interactive HCI-ish ML | **P1 Warm ML** | warmer tokens + coral emphasis |
| robotics / embodied / natural / earthy | **P3 Earthy Warm** | muted browns/greens |
| user gives pastel reference | nearest of P1–P3 | state “matched reference” |

---
## Semantic Color Binding Contract (Cross-Figure Consistency)

To minimize cognitive load across multi-panel or paper-wide diagrams (Figure 1 to Figure N), map functional domain roles to consistent semantic colors regardless of palette family:

| Functional Role | Classic Family (Border / Line) | Pastel Family (Token / Accent Fill) |
|---|---|---|
| **Input / Token / Data** | Soft Sky Blue (`#4285F4` / `#1B3A5C`) | Soft Blue Pill (`#E8F0FE` / `#BBDEFB`) |
| **Backbone / Core Model / Encoder-Decoder** | Soft Indigo / Purple (`#6A5ACD` / `#7B1FA2`) | Soft Lavender Pill (`#F3E8FF` / `#D1C4E9`) |
| **Loss / Supervision / Feedback** | Soft Coral / Red (`#D95F02` / `#E05555`) | Soft Coral Badge (`#FEE2E2` / `#FFD0D0`) |
| **Output / Target / Prediction** | Soft Mint / Emerald (`#1B9E77` / `#2E7D32`) | Soft Mint Badge (`#DCFCE7` / `#C8E6C9`) |
| **Frozen / Pretrained / Adapter (LoRA)** | Neutral Slate Gray (`#7570B3` / `#616161`) | Neutral Gray Badge (`#F3F4F6` / `#E0E0E0`) |

Rule: When emitting a Palette Decision or Figure Spec, state the semantic binding so all modules across the paper retain identical color roles.

---

## Scene → palette decision (classic family)

Apply filters **in order**. Stop at the first hard constraint that fires; otherwise continue.

### 1) Hard constraints

| Constraint | Choose | Alternate |
|------------|--------|-----------|
| Strict B&W / grayscale print only | **Print-Safe Gray** | Grayscale |
| Theory paper, no color budget | **Grayscale** | Print-Safe Gray |
| Colorblind-safe required (default if unspecified) | Prefer Okabe-Ito / ML TopConf Colorblind / Nature Blue / Blue Monochrome | Avoid Warm Earth / Teal-Coral as sole encoding |
| ≥ 4 modules in one framework / “太花了” | **Nature Blue** | Blue Monochrome |
| Must match existing Matplotlib Tab10 experiment plots | **ML TopConf Tab10** | ML TopConf Colorblind if a11y matters more than match |

### 2) Figure type

| Figure type | Prefer | Alternate | Why |
|-----------|--------|-----------|-----|
| Overall Framework (≤3 stages) | Okabe-Ito | ML TopConf Colorblind | few hues, clear pipeline roles |
| Overall Framework (≥4 modules) | **Nature Blue** | Blue Monochrome | one hue ramp reduces clutter |
| Network Architecture | Okabe-Ito or Blue Monochrome | Nature Blue if deep stack | structure > decoration |
| Module Detail | **Blue Monochrome** | Okabe-Ito | detail density; gray-print friendly |
| Comparison / Ablation (few panels) | Purple-Green | Okabe-Ito | category contrast |
| Dense multi-panel ablation | **ML TopConf Deep** | Purple-Green | softer multi-hue grid |
| Data Behavior (curves / heatmaps / t-SNE) | ML TopConf Colorblind | Okabe-Ito | series/categories stay separable |
| Qualitative image grids | Okabe-Ito accents only | Grayscale frames | color on labels, not photo washes |

### 3) Venue

| Venue | Prefer | Alternate | Style family note |
|-------|--------|-----------|-------------------|
| CVPR / ICCV / ECCV | Okabe-Ito | ML TopConf Colorblind | classic default |
| NeurIPS / ICML / ICLR (classic diagrams) | ML TopConf Colorblind | Tab10 / Deep | classic **or** pastel if user wants airy |
| NeurIPS / ICML / ICLR (soft modern posters) | → pastel P2 | P1 | switch skill to prompt-pastel |
| Nature / Science / Cell | Okabe-Ito | Nature Blue / Journal Standard | classic; Journal Standard only if many categories |
| IEEE / ACM Transactions | Purple-Green or Blue Monochrome | Print-Safe Gray | often print-heavy |
| CHI / UIST / CSCW | Teal-Coral | Okabe-Ito | dual-encode; or pastel if “soft UI” ask |

### 4) Domain

| Domain | Prefer | Alternate |
|--------|--------|-----------|
| Generative CV / diffusion / vision systems | Okabe-Ito | Nature Blue if multi-module |
| NLP / LLM systems (classic boxes) | ML TopConf Colorblind | Okabe-Ito |
| NLP / LLM (token-centric modern) | pastel P2 | classic Okabe-Ito |
| Biology / ecology / medical imaging | Warm Earth | Okabe-Ito (safer a11y) |
| Materials / chemistry / physics | Nature Blue | Blue Monochrome |
| Robotics / control | Blue Monochrome | Okabe-Ito |
| HCI / interaction | Teal-Coral | pastel P1 if airy |
| Theory / algorithms / proofs-as-figures | Grayscale | Blue Monochrome |

### 5) Vibe words → concrete choice

| User says | Family | Palette / scheme |
|-----------|--------|------------------|
| 高级 / 克制 / 顶刊 / Nature 风 | classic | Nature Blue or Okabe-Ito |
| 科技感 / 工程感 / 干净 | classic | Blue Monochrome or Okabe-Ito |
| 柔和 / 现代 / 空气感 / ICLR 那种 | pastel | P2 (default) |
| 活泼 / 教学感 | pastel | P1 |
| 自然 / 生物感 | classic Warm Earth **or** pastel P3 | state a11y tradeoff for Warm Earth |
| 不要花 / 模块太多 | classic | Nature Blue |
| 和实验曲线一个色 | classic | ML TopConf Tab10 / Colorblind |
| 黑白印刷 | classic | Print-Safe Gray / Grayscale |

---

## Worked decision recipes

| Scenario | Family | Palette | One-line reason |
|----------|--------|---------|-----------------|
| CVPR method figure, 3-stage pipeline | classic | Okabe-Ito | venue default + few modules |
| CVPR framework with 6 blocks | classic | Nature Blue | ≥4 modules monochrome rule |
| NeurIPS ablation 2×3 panels | classic | ML TopConf Deep | dense multi-panel |
| NeurIPS token-flow explainer, “现代一点” | pastel | P2 | airy ML default |
| Nature materials multi-module system | classic | Nature Blue | domain + module count |
| IEEE journal, B&W print | classic | Print-Safe Gray | hard print constraint |
| CHI prototype concept diagram | classic Teal-Coral **or** pastel P1 | Teal-Coral if box UI; P1 if soft tokens |
| Medical imaging module detail | classic | Blue Monochrome (or Warm Earth if organic feel + dual-encode) | detail density |
| User: 配色随便 | classic | Okabe-Ito (or Nature Blue if ≥4 modules) | safe default branch |

---

## Decision checklist (emit with every Palette Decision)

1. Style family: classic / pastel — which skill?  
2. Hard constraint fired? (print / a11y / ≥4 modules / match plots)  
3. Figure type preference  
4. Venue / domain preference  
5. Primary + alternate named  
6. Hex loaded from this file (classic) or P1–P3 table (pastel)  
7. Branch stated: `user` / `scene` / `default`


## Palette Decision handoff

Downstream skills consume:

```
palette: <name>
primary / secondary / tertiary: <hex>
text / fill / section_bg / border / arrow: <hex>
reason: <one line>
accessibility: colorblind-safe | needs dual encoding | print-only
```

---

## 1. Okabe-Ito — default polychrome

**Use:** CVPR / NeurIPS / Nature / Science; general colorblind-safe

| role | hex | use |
|------|-----|-----|
| primary | `#0072B2` | core module borders, section labels |
| secondary | `#E69F00` | secondary borders, alternate highlight |
| tertiary | `#009E73` | output / result (sparse) |
| text | `#333333` | body text |
| fill | `#FFFFFF` | canvas / boxes |
| section_bg | `#F7F7F7` | region grouping |
| border | `#CCCCCC` | standard border |
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
| border | `#B0BEC5` |
| arrow | `#37474F` |

---

## 3. Warm Earth

**Use:** biology, ecology, medical imaging. Dual-encode (not strongest for colorblind).

| role | hex |
|------|-----|
| primary | `#C0392B` |
| secondary | `#E67E22` |
| tertiary | `#F39C12` |
| text | `#2C2C2C` |
| fill | `#FFFFFF` |
| section_bg | `#FDF6EC` |
| border | `#D5C5A1` |
| arrow | `#5D4037` |

---

## 4. Purple-Green

**Use:** comparison / ablation; IEEE; high contrast

| role | hex |
|------|-----|
| primary | `#6A1B9A` |
| secondary | `#2E7D32` |
| tertiary | `#AB47BC` |
| text | `#1A1A1A` |
| fill | `#FFFFFF` |
| section_bg | `#F8F5FC` |
| border | `#CE93D8` |
| arrow | `#4A148C` |

---

## 5. Grayscale

**Use:** print-only venues; theory papers

| role | hex |
|------|-----|
| primary | `#212121` |
| secondary | `#616161` |
| tertiary | `#9E9E9E` |
| text | `#111111` |
| fill | `#FFFFFF` |
| section_bg | `#F5F5F5` |
| border | `#BDBDBD` |
| arrow | `#424242` |

Distinguish categories by shape / line weight, not hue.

---

## 6. Teal-Coral

**Use:** HCI / CHI; modern ML. Dual-encode for red-weak vision.

| role | hex |
|------|-----|
| primary | `#00695C` |
| secondary | `#E64A19` |
| tertiary | `#26A69A` |
| text | `#212121` |
| fill | `#FFFFFF` |
| section_bg | `#F0F9F8` |
| border | `#80CBC4` |
| arrow | `#004D40` |

---

## 7. ML TopConf Tab10

**Use:** NeurIPS / ICML / ICLR when matching Matplotlib experiment plots

| role | hex |
|------|-----|
| primary | `#1F77B4` |
| secondary | `#FF7F0E` |
| tertiary | `#2CA02C` |
| text | `#1F2937` |
| fill | `#FFFFFF` |
| section_bg | `#F8FAFC` |
| border | `#CBD5E1` |
| arrow | `#334155` |

---

## 8. ML TopConf Colorblind

**Use:** NeurIPS / ICML / ICLR with colorblind safety (preferred over Tab10)

| role | hex |
|------|-----|
| primary | `#0173B2` |
| secondary | `#DE8F05` |
| tertiary | `#029E73` |
| text | `#1F2937` |
| fill | `#FFFFFF` |
| section_bg | `#F8FAFC` |
| border | `#CBD5E1` |
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
| border | `#CBD5E1` |
| arrow | `#334155` |

---

## 10. Print-Safe Gray

**Use:** strict B&W print (IEEE / ACM grayscale)

| role | hex |
|------|-----|
| primary | `#000000` |
| secondary | `#333333` |
| tertiary | `#666666` |
| text | `#333333` |
| fill | `#FFFFFF` |
| section_bg | `#F7F7F7` |
| border | `#CCCCCC` |
| arrow | `#4D4D4D` |

---

## 11. Journal Standard

**Use:** Nature / Science / Cell multi-category figures (more accents)

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
| border | `#CBD5E1` |
| arrow | `#334155` |

Keep accents sparse; prefer ≤ 3 active colors per figure.

---

## 12. Nature Blue — default monochrome for ≥ 4 modules

**Use:** multi-module frameworks; materials / chemistry / physics; “too busy” polychrome fix

| role | hex |
|------|-----|
| primary | `#1B3A5C` |
| secondary | `#2E6B9E` |
| tertiary | `#5BA0D0` |
| gray | `#8EAEC4` |
| text | `#333333` |
| fill | `#FFFFFF` |
| section_bg | `#F7F7F7` |
| border | `#CCCCCC` |
| arrow | `#4D4D4D` |

---

## Monochrome vs polychrome

| | monochrome (Blue Monochrome / Nature Blue) | polychrome (Okabe-Ito / Tab10) |
|---|---|---|
| visual unity | high | lower |
| module separation | lightness + border + label | hue + label |
| best when | ≥ 4 modules | ≤ 3 modules or strong contrast needed |
| print / colorblind | strong | depends on palette |

---

## Venue / domain quick map

| Venue / domain | Prefer | Alternate |
|----------------|--------|-----------|
| CVPR / ICCV / ECCV | Okabe-Ito | ML TopConf Colorblind |
| NeurIPS / ICML / ICLR | ML TopConf Colorblind | Tab10 / Deep |
| Nature / Science | Okabe-Ito | Nature Blue / Journal Standard |
| IEEE Transactions | Purple-Green | Blue Monochrome |
| HCI / CHI | Teal-Coral | Okabe-Ito |
| Biology / medicine | Warm Earth | Okabe-Ito |
| Materials / chemistry / physics | Nature Blue | Blue Monochrome |
| Theory / print-only | Grayscale | Print-Safe Gray |
| Robotics | Blue Monochrome | Okabe-Ito |
| Dense multi-panel ablation | ML TopConf Deep | Purple-Green |

---

## Hard rules (positive form)

- White canvas ≥ 70% of area; module fill white; color on borders only.
- At most 3 chromatic colors + neutrals per figure.
- Dual-encode categories (color + shape / label / line style).
- Text vs background contrast ≥ 4.5:1.
- Flat vector: solid fills, no gradients, no 3D chrome, no rainbow panels.

## Custom palette minimum

```
primary: #XXXXXX
secondary: #XXXXXX
tertiary: #XXXXXX   (optional)
fill: #FFFFFF
text: #333333
```

Validate contrast, colorblind distinguishability, and B&W print before handoff.

---
id: academic-figure-prompt-pastel
name: Academic Figure Prompt — Modern ML Airy Style
version: 4.1.1
description: Pastel airy figure prompts for modern ML papers — ICLR/NeurIPS/ICML soft-panel style with tokens, pills, and rounded type. Use when the user wants pastel academic figures, 现代ML论文配图, or 2024-2025 conference airy aesthetics.
stages: [writing, research, review]
tools: [bash]
---

# Academic Figure Prompt — Modern ML Airy Style

English **image prompts** in the soft pastel style common in recent ICLR / NeurIPS / ICML figures.

Missing info: → `references/missing-info-policy.md`  
Classic JSON specs: use `academic-figure-prompt` instead.

## Airy rules (all must hold)

1. **White canvas + white panels + soft shadow**  
   Canvas `#FFFFFF`. Panels `#FFFFFF`, ~20px radius, shadow `3px blur / 1px y / rgba(0,0,0,0.06)`. Separation by shadow only — no grey panel fills, no gradient canvas.

2. **Rounded geometric sans**  
   Nunito / Poppins / Quicksand / Comfortaa. Titles 600–700 ~16–18pt; body 400 ~10–11pt; math italic serif.

3. **Packed, not sparse**  
   Panels filled with tokens, curves, formulas, icons; 8–12px micro-gaps; ordered density without overlap or text walls.

4. **Floating elements**  
   Content sits on the panel surface. Pills for concept names. No box-in-box nesting.

5. **Color via tokens, text, and curves**  
   Panels stay white. Color lives in 10–14px rounded tokens (pastel fill + 1px darker border), semantic text (coral/teal/purple/green), curves, and dots.

## Pastel schemes

| id | name | tokens | emphasis text |
|----|------|--------|---------------|
| P1 | Warm ML | `#FFD0D0` `#BBDEFB` `#FFF3C4` `#E1BEE7` `#C8E6C9` | `#E05555` `#1A9988` `#6A5ACD` `#3A8F3A` |
| P2 | Cool Research (default) | `#B3E5FC` `#C5CAE9` `#CFD8DC` `#B2DFDB` `#D1C4E9` | `#1565C0` `#3949AB` `#00897B` |
| P3 | Earthy Warm | `#FFE0B2` `#D7CCC8` `#C8E6C9` `#E0E0E0` `#EFEBE9` | `#6D4C41` `#827717` `#2E7D32` |

Decision: user → scene (modern ML → P2; playful → P1; natural/robotics → P3) → default **P2**. Full classic-vs-pastel and venue recipes: `references/palettes.md` (**Style family first** + pastel map). If the user wants box-border Nature/CVPR classic, route to `academic-figure-prompt` instead.


## Input / Output

- Prefer: figure type, content, pastel preference, reference image, labels  
- Minimum: type + subject  
- Output **Prompt Package**: Chinese name, type, full English prompt, scheme + key hex, style note, completeness block  

## Steps

### Step 1: Ground content

Extract modules, flows, symbols from available material.

Done when: content list is sourced or placeholder-tagged.

### Step 2: Choose pastel scheme

Apply decision order; state branch.

Done when: P1/P2/P3 (or custom) fixed with token + emphasis hex.

### Step 3: Layout

2–5 panels sized by content (asymmetric OK). ~20px panel gaps. Prefer content-driven layouts over forced 2×2 symmetry.

Done when: panel count and roles are listed.

### Step 4: Write prompt

Layers:

1. Global: airy ICLR/NeurIPS style, white canvas/panels, rounded font, packed density, no nested boxes  
2. `=== PANEL: name ===` blocks with floating tokens / pills / curves / formulas  
3. `=== STYLE SPECIFICATIONS ===` with scheme hex  

Color carriers:

| carrier | form |
|---------|------|
| token | `soft blue #BBDEFB square with 1px #90CAF9 border, "s₁"` |
| colored text | `bold coral #E05555 text "Exciter"` |
| pill | `faint green-tinted pill badge "Random Forest"` |
| curve | `sigmoid in warm amber #DAA520` |
| dots | tiny category circles |

Done when checklist passes:

- [ ] pure white canvas and panels  
- [ ] rounded font named  
- [ ] packed micro-spacing (8-12px)  
- [ ] soft panel shadows (`rgba(0,0,0,0.05)`)  
- [ ] no nested boxes  
- [ ] tokens have borders  
- [ ] scheme hex present  
- [ ] weight status encoded via pill tags (`[Fixed]` vs `[Trainable]`) or dashed/solid borders (NO emojis)  
- [ ] negative constraints explicit: `NO emojis, NO lock/fire/lightning icons, NO 3D rendering`  

## Stop

Stop when the Prompt Package is delivered, or type+subject are both missing.

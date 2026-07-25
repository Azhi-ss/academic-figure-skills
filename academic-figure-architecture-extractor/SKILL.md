---
id: academic-figure-architecture-extractor
name: Academic Figure Architecture Extractor & Analyzer
version: 1.2.0
description: Architecture diagram analysis for academic PDFs or images — structure, components, and redraw parameters for prompt skills. Use when the user wants 架构图分析, extract figures from PDF, or architecture diagram breakdown.
stages: [research, writing]
tools: [bash]
---

# Academic Figure Architecture Extractor & Analyzer

Turn paper PDFs or existing architecture images into a structured **架构图分析结果** that handoffs cleanly to color-expert and prompt skills.

Palettes: → `../docs/palettes.md` (names only)  
Missing info: → `../docs/missing-info-policy.md`  
Extractor: → `scripts/extract_pdf_figures.py`

## Honest scope

- Prefer user-supplied figure images when available.
- PDF extraction is a **real local helper** (pdfimages / PyMuPDF / optional pdftoppm), not a trained detector.
- Size filter is heuristic only; architecture vs photo/table is **agent judgment**.
- Palette: recommend **names** from `docs/palettes.md`; hex via color-expert when needed.

## Input Contract

- Prefer: PDF path(s), figure images, domain, venue
- Minimum: one PDF **or** one architecture image
- Missing: analyze what exists; list blocked steps

## Output Contract — 架构图分析结果

- inventory (path/page, size, keep/drop reason)
- per-kept-figure structure (components, hierarchy, flow, type)
- recommended palette **names**
- redraw parameters for `academic-figure-prompt`

## Steps

### Step 1: Obtain images

**Images given** → index paths.

**PDF given** → run the helper (from skill dir or repo root):

```bash
python3 academic-figure-architecture-extractor/scripts/extract_pdf_figures.py \
  /path/to/paper.pdf -o /tmp/arch-extract/paper
```

Useful flags:

| flag | meaning |
|------|---------|
| `--backend auto\|pdfimages\|pymupdf` | embedded-image backend |
| `--min-side 300` | drop tiny icons (default) |
| `--min-pixels 90000` | drop low-res crops |
| `--pages 4` or `--pages 1-3` or `--pages all` | also rasterize pages via pdftoppm |
| `--dpi 150` | raster DPI |

Read `extract-report.json` in the out dir (`kept` / `dropped` / `tools`).

If both backends missing → ask user for exported figures; do not invent paths.

Done when: each candidate has a path or page reference, or a clear tool blocker is stated.

### Step 2: Filter to architecture-like figures

Start from `kept` (size-ok). Agent reclassifies:

| keep cues | drop cues |
|-----------|-----------|
| boxes + arrows, layered blocks | pure photos, scatter-only, dense tables |
| structured edges / modules | tiny icons already size-dropped |

Unsure → keep + `待确认`.

Done when: each image is keep / drop / uncertain with a one-line reason.

### Step 3: Structure analysis

For each kept figure:

1. components (core vs auxiliary)  
2. hierarchy / dataflow  
3. type: Overall Framework / Network Architecture / Module Detail / Comparison  
4. domain notes  

Done when: every kept figure has type + component list + flow summary.

### Step 4: Palette suggestion + redraw handoff

Map via `docs/palettes.md` (e.g. ≥4-module framework → Nature Blue; module detail → Blue Monochrome; comparison → ML TopConf Deep).

```
图类型: ...
核心组件: ...
配色方案名: ...
布局建议: 16:9 | 3:2 | 4:3
风格: white fill, colored borders, flat vector
标注要求: ...
```

Done when: each kept figure has redraw params + palette names (no hex tables).

## Stop

Stop when the report is delivered, extraction is blocked pending user images, or the user only wanted inventory.

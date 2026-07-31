# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## 2.9.0

- Real-repo benchmarks: six public repository clones plus the sparse fixture.
- Vendored `references/` in all skills, fixing broken `../docs/` links after install.
- Generalized repo-analyzer coverage for AI4Science and research code.
- Wired `module_count` and `aspect_ratio` end to end.
- Fixed example and schema drift.

## [2.8.0] - 2026-07-25

### Added
- 🛠 **architecture-extractor**: real `scripts/extract_pdf_figures.py` (pdfimages / PyMuPDF / optional pdftoppm) + size filter report
- 📘 **examples/**: aligned with Palette Decision handoff + JSON figure spec default
- 🗺 **docs/palettes.md**: scene→style family→palette decision guide (figure type / venue / domain / vibe recipes + checklist)


### Changed
- 🧹 **Skill rewrite (writing-great-skills pass)**: slim all 7 `SKILL.md` files; steps + checkable completion criteria; progressive disclosure of reference
- 🎨 **Palette SSOT**: single source of truth in `docs/palettes.md` (12 presets); removed duplicated hex tables from prompt / paper-analyzer / architecture-extractor / color-expert body
- 📐 **academic-figure-prompt**: schema/examples moved to `json-schema.md`; Text Budget + JSON-default kept in skill body
- 🔍 **academic-repo-analyzer**: keyword tables moved to `keywords.md`
- 🧭 **Defaults aligned**: ≥ 4 modules → Nature Blue; else Okabe-Ito (workflow, color-expert, prompt agree)
- 🧾 **architecture-extractor**: removed unverifiable performance claims (≥92%, ≤10s/PDF); scoped as agent-driven analysis with honest tool gaps
- 📝 **Descriptions**: shorter model-facing descriptions; leading words front-loaded
- 📚 **Shared policy**: `docs/missing-info-policy.md` for sparse-input handling
- 🔢 **Pack**: 2.7.0 → 2.8.0; skill versions bumped

### Fixed
- 🐛 Palette count inconsistency across README / color-expert / prompt (9 vs 10 vs 12 vs 13)
- 🐛 README badge version lag (2.5.0 vs manifest)

## [2.7.0] - 2026-05-11

### Changed
- 🔄 **academic-figure-prompt v1.3.0**: JSON spec is now the **default output format** — all framework/architecture/flowchart/module/comparison figures output JSON by default
- 🔄 **academic-figure-prompt**: Old text prompt template demoted to "备选" (fallback, simple scenes only)
- 🔄 **academic-figure-prompt**: Title changed from "学术论文配图提示词生成器" to "学术论文配图 JSON 规范生成器"
- 🔄 **academic-figure-workflow**: Routing updated to reflect JSON-first output
- 🔢 **Pack**: 2.6.0 → 2.7.0

## [2.6.0] - 2026-05-11

### Added
- 📐 **academic-figure-prompt**: JSON Structured Figure Spec output format — `exact_text_to_render`, `relative_position`, `layout_and_content_blocks`, label hierarchy, and `RENDERING_RULES` patterns for precise layout/text control
- 📝 **academic-figure-prompt**: Text Budget principle — per-element word limits (≤5 for titles, ≤3 for labels, ≤2 for pipeline steps) preventing cluttered figures
- 🏷️ **academic-figure-prompt**: Label Hierarchy (Primary/Secondary/Caption) — formulas and parameters go to figure captions, not on-figure
- 🎨 **academic-figure-color-expert**: Nature Blue / Deep Blue Monochrome scheme (#1B3A5C → #2E6B9E → #5BA0D0 → #8EAEC4) — field-validated for 4+ module framework diagrams
- 🎨 **academic-figure-color-expert**: Monochrome vs Polychrome philosophy section — when to use single-hue vs multi-hue

### Changed
- 🔄 **academic-figure-prompt**: Quality checklist rebalanced — "text restraint" replaces "max information density"; "caption separation" replaces "no simplification"
- 🔄 **academic-figure-prompt**: Core philosophy changed from "max information density at all costs" to "labels on figure, details in caption"
- 🔢 **academic-figure-prompt**: v1.1.0 → v1.2.0
- 🔢 **academic-figure-color-expert**: v1.1.0 → v1.2.0

### Fixed
- 🐛 Real-world validation: verbose descriptions in figure specs produce unreadable cluttered output — now prevented by Text Budget + exact_text_to_render pattern

## [2.5.0] - 2026-04-15

### Added
- ✨ **New Skill**: `academic-figure-architecture-extractor` - Extract and analyze architecture diagrams from PDFs, filter invalid images, analyze diagram structure, auto-match color schemes
- 🎨 **Color Schemes**: Added 3 new palettes (12 total):
  - Grayscale Print Friendly - IEEE-recommended, 100% black-and-white compatible
  - Nature/Science Standard - Official top-journal style
  - Biomaterials Cross-Disciplinary - For materials science + AI intersection
- 📚 **Documentation**: Added architecture extraction workflow to README
- 🔧 **Gitignore**: Added `.codex` to ignore list

### Changed
- 🔄 **Workflow**: Updated `academic-figure-workflow` to support architecture extraction stage
- 📝 **README**: Removed eval-team section, added architecture extractor usage examples
- 🔢 **Versioning**: Bumped pack version to `2.5.0`

### Removed
- ❌ **Deprecated**: `academic-skill-eval-team` (per user request)

## [2.4.0] - 2026-04-11

### Added
- **New Skill**: `academic-skill-eval-team` - Multi-agent evaluation team for reviewing a single skill or the whole skill pack before release
- **README**: Added usage entry for skill evaluation workflow

### Changed
- **Versioning**: Bumped pack version in `manifest.json` and `README.md` to `2.4.0`

## [2.3.1] - 2026-04-09

### Added
- 📚 **Documentation**: Added `CONTRIBUTING.md` - Complete contributing guide
- 📚 **Documentation**: Added `docs/academic-references.md` - Academic references and citations
- 📚 **Documentation**: Added `docs/best-practices.md` - 2024-2025 top conference best practices
- 📚 **Examples**: Added `examples/` directory with 4 complete end-to-end workflow examples
  - `01-repo-analyzer-example.md` - Repo analyzer output example
  - `02-paper-analyzer-example.md` - Paper analyzer output example
  - `03-figure-prompt-example.md` - Figure prompt output example
  - `04-end-to-end-workflow.md` - Complete conversation workflow

### Fixed
- 🔧 **Consistency**: Unified copyright holder in LICENSE (Azhi-ss)
- 🔧 **Consistency**: Fixed academic-figure-prompt version in manifest.json (1.0.0 → 1.1.0)
- 🔧 **Documentation**: Updated manifest.json description to reflect 9 palettes

## [2.3.0] - 2026-04-09

### Added
- ✨ **New Skill**: `academic-repo-analyzer` - Analyze ML/DL code repositories to understand what they do, identify model architecture, core algorithms, tech stack, and key innovations. Generates a "quick understanding document" that can be passed to paper-analyzer.
- 📚 **Documentation**: Added example architecture diagram in README
- 🔗 **Workflow**: Complete end-to-end workflow from repo analysis → figure planning → color selection → prompt generation

### Enhanced
- 🎨 **Color Expert**: Extended domain coverage (physics, chemistry, economics, life sciences)
- 📝 **Figure Prompt**: Added quick-start mode with default Okabe-Ito palette
- 🔄 **Paper Analyzer**: Updated to support 9 color schemes and extended domains

### Fixed
- 🔧 **Consistency**: Unified version numbers across all files
- 🔧 **Color Schemes**: Standardized to 9 palettes across all skills
- 🔧 **Manifest**: Fixed repository URL and author information

## [2.2.0] - 2026-04-09

### Added
- 🎨 **New Skill**: `academic-figure-color-expert` - Academic color palette expert with 9 preset schemes plus colorblind-safe design principles
- 📝 **New Skill**: `academic-figure-paper-analyzer` - Analyze academic papers to plan which figures to generate
- 🌈 **Color Schemes**: 9 preset palettes (Okabe-Ito, Blue Monochrome, Warm Earth, Purple-Green, Grayscale, Teal-Coral, ML TopConf Tab10, ML TopConf Colorblind, ML TopConf Deep)

### Enhanced
- 🎯 **Figure Prompt**: Expanded from 8 to 9 color schemes
- 📚 **README**: Complete rewrite with quick-start guide and usage examples

## [2.1.0] - 2026-04-09

### Added
- ✨ **New Skill**: `academic-figure-prompt-pastel` - Modern ML/RL paper-style figures matching ICLR/NeurIPS/ICML 2024-2025 aesthetics
- 🎨 **Pastel Style**: Pure white canvas, white panels with soft shadow, rounded fonts, pastel token squares, pill-shaped labels

### Enhanced
- 📝 **Figure Prompt**: Added cross-reference to pastel style
- 🔗 **Workflow**: Added pastel style as alternative to classic style

## [2.0.0] - 2026-04-09

### Added
- 🚀 **Initial Release**: Complete skill pack for academic figure generation
- ✨ **Core Skill**: `academic-figure-prompt` - Classic style (Okabe-Ito / Nature / CVPR) prompt generation
- 📚 **Documentation**: Full README with installation and usage instructions
- 🔧 **Manifest**: Complete skill registration with trigger phrases

## [1.0.0] - 2026-04-08

### Added
- 🌱 **Prototype**: Initial concept and single skill implementation

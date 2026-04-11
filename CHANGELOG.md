# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

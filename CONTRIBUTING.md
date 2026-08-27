# Contributing to Academic Figure Skills

First off, thanks for taking the time to contribute!

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

**Before creating bug reports**, please check the existing issues to make sure the bug hasn't been reported yet.

When you are creating a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps which reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed after following the steps
- Explain which behavior you expected to see instead and why
- Include screenshots if relevant

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

**Before creating enhancement suggestions**, please check the existing issues as you might find out that you don't need to create one.

When you are creating an enhancement suggestion, please include as many details as possible:

- Use a clear and descriptive title
- Provide a step-by-step description of the suggested enhancement
- Provide specific examples to demonstrate the steps
- Describe the current behavior and explain which behavior you want to see instead
- Explain why this enhancement would be useful to most users

### Your First Code Contribution

Unsure where to begin contributing? You can start by looking through these issues:

- `good first issue` - issues which should only require a few lines of code
- `help wanted` - issues which should be a bit more involved

### Pull Requests

The process described here has several goals:

- Maintain the project's quality
- Fix problems that are important to users
- Engage the community in working toward the best possible solution
- Enable a sustainable system for maintainers to review contributions

Please follow these steps to have your contribution considered:

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Synchronize vendored references and run the validation commands below
5. Ensure the test suite passes
6. Make sure your code lints
7. Issue that pull request!

## Skill Development Guide

### Adding a New Skill

To add a new skill to the pack:

1. Create a new directory under the root: `./your-new-skill/`
2. Create a `SKILL.md` file with the required frontmatter:

```yaml
---
name: your-new-skill
description: Describe the job and the situations that should trigger this skill.
metadata:
  version: "1.0.0"
---
```

Codex-compatible top-level fields are `name`, `description`, `license`,
`compatibility`, `metadata`, and `allowed-tools`. Keep pack-specific fields such
as display name, trigger phrases, stages, tags, and tool hints in
`manifest.json`; do not add them as unsupported top-level SKILL.md fields.

3. Add your skill to `manifest.json`:

```json
{
  "id": "your-new-skill",
  "name": "Your Skill Name",
  "version": "1.0.0",
  "description": "Skill description",
  "path": "./your-new-skill",
  "trigger_phrases": ["phrase 1", "phrase 2"],
  "stages": ["writing", "research"],
  "tools": ["bash"],
  "tags": ["academic", "figure"]
}
```

4. Add the skill id to `EXPECTED_SKILL_IDS` in
   `scripts/sync_shared_refs.py`, and to the relevant shared-reference groups if
   it consumes styles, RenderAudit, or the Codex image workflow
5. Run `python3 scripts/sync_shared_refs.py` to create self-contained vendored
   references; do not copy or symlink them manually
6. Update the README.md to include your new skill in the skill list
7. Add an entry to CHANGELOG.md

### Skill Structure Best Practices

A good skill should include:

1. **Input / Output Contract** — minimum inputs, deliverable shape
2. **Steps with completion criteria** — checkable done conditions per step
3. **Pointers to disclosed reference** — large tables/schemas live in sibling `.md` files (e.g. `docs/palettes.md`), not duplicated in every skill
4. **Stop conditions** — when to halt vs continue downstream
5. **Sparse-input cases** — partial results labeled `推断` / `待确认` (see `docs/missing-info-policy.md`)

Do **not** paste the full palette hex tables into new skills. The canonical
copies live under `docs/`; installable skills consume synchronized files under
their own `references/` directory. Never link to `../docs/`, which does not
exist after a standalone `npx skills` installation.
Keep descriptions short: one leading job + distinct trigger branches; no implementation counts (“13 presets”).

For rendering skills, preserve the execution contract:

- build and validate FigureSpec v1 before rendering;
- call Codex's native `image_gen.imagegen` capability directly when it is
  available instead of returning a prompt for the user to run;
- keep the prompt internal when `prompt_review` is `waived`;
- inspect the initial render, record RenderAudit v1, and use the current best
  image as the first reference for a bounded targeted edit;
- preserve revision files and audit every edit.

### Validation before a pull request

Run from the repository root:

```bash
python3 scripts/sync_shared_refs.py
python3 scripts/sync_shared_refs.py --check
python3 -B -m unittest discover -s tests -v
python3 scripts/validate_skill_pack.py
```

When changing FigureSpec, update the formal schema, the standard-library
validator, the prose contract, and tests together. A render-capable caller must
also run strict render-ready validation with its trusted workspace root before
calling an image model.

### Trigger Phrases

Include both Chinese and English trigger phrases:

- Chinese natural language phrases (e.g., "分析这篇论文需要哪些图")
- English natural language phrases (e.g., "paper figure planning")
- Technical terms (e.g., "repo analyzer")

## Styleguides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Markdown Styleguide

All Markdown files are rendered with GitHub Flavored Markdown.

- Use ATX-style headings (`# Heading`)
- Use reference-style links
- Use code blocks with language specification
- Wrap long lines at 80 characters

### Skill Documentation Styleguide

- Use Chinese for the main documentation (most users are Chinese)
- Include English terms where appropriate (technical terms, skill names)
- Provide code examples for common use cases
- Include a "快速开始" (Quick Start) section
- Include a "常见问题" (FAQ) section if applicable

## Community

### Getting Help

If you have questions, please:

- Check the README.md for documentation
- Check the existing issues for similar questions
- Create a new issue with the `question` label

### Code of Conduct

This project and everyone participating in it is governed by a Code of Conduct. By participating, you are expected to uphold this code.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

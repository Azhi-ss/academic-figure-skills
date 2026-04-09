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
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Skill Development Guide

### Adding a New Skill

To add a new skill to the pack:

1. Create a new directory under the root: `./your-new-skill/`
2. Create a `SKILL.md` file with the required frontmatter:

```yaml
---
id: your-new-skill
name: Your Skill Name
version: 1.0.0
description: When to trigger this skill, including trigger keywords
stages: [writing, research, review]
tools: [bash, glob, read, write]
---
```

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

4. Update the README.md to include your new skill in the skill list
5. Add an entry to CHANGELOG.md

### Skill Structure Best Practices

A good skill should include:

1. **核心理念** - Define the skill's values and principles
2. **工作流程** - Step-by-step operation guide
3. **模板/词汇表** - Reusable component library
4. **质量检查清单** - Validation standards
5. **输出格式** - Standard output template
6. **注意事项** - Boundary conditions and best practices
7. **与其他技能配合** - How it fits into the workflow

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

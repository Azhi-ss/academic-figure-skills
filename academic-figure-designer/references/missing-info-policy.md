# Missing-Info Policy

Shared by all academic-figure skills. Domain skills add only their own cases.

## Rule

When evidence is incomplete: ship a **conservative, useful** partial result. Label every claim beyond evidence as `推断` or `待确认`. Prefer placeholders over invention.

## Completeness block (every deliverable)

```
- 已分析材料: ...
- 当前输出类型: 完整 / 阶段性 / 局部 / 骨架
- 高置信信息: ...
- 待确认信息: ...
- 建议补充材料: 1–3 highest-value items
```

## Stop vs continue

| Situation | Action |
|-----------|--------|
| Core deliverable possible with placeholders | continue |
| Zero usable source (no paper, repo, figure type, or image) | stop; list minimum materials |
| User asked only this stage | stop after that stage |
| Next stage needs material user has not provided | stop; do not invent |

## Invention ban

Do not invent modules, losses, dimensions, experiment results, or architecture layers that never appear in the source. Rewrite unknowns as explicit placeholders (`[module_name]`, `R^(?×?)`).

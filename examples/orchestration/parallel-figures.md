# 并行编排示例：多张独立配图 + 一次独立复核

本示例只覆盖 skill 允许的委派范围：

- **可以委派**：彼此独立的配图（图 A / 图 B 各自成图）、彼此独立的来源分析（论文解析 / 仓库解析）。
- **要开**：彼此独立的来源分析、彼此独立的配图，以及一张已完成图的只读复核。运行时支持子 agent 时就开，不要为了留在一条线程里把这些工作收回主 agent。
- **不要委派**：风格菜单、单张图从设计到修图的顺序步骤、对一张已有图的局部修改。见 `fig1-draw/SKILL.md` 的 “When to open a sub-agent”。
- **没有子 agent 也能完成流程**。主 agent 自己做同样的步骤，缺子 agent 不阻塞交付。

## 两条铁律

1. **一次 workflow 调用，多个 child 只在该调用内部启动。**
2. **主 agent 独占交付路径。** child 只写自己的中间产物（图片、spec、audit）；
   `split_reports/`、论文目录、最终交付文件由主 agent 写。

## 可运行骨架

```js
const results = await runs.all([
  {
    key: 'figB',                     // 稳定 key，用于定位与续跑
    agent: 'worker',                 // 需要写文件时用 writer 角色
    task: `生成图 B。只允许写 fig/figB.png 与 .omx/figB_spec/ 下的文件，
           不要修改交付目录。完成后跑 validate_figure_spec.py 与 validate_render_audit.py，
           并逐字核对可见文字。`,
  },
  {
    key: 'reviewA',                  // 独立复核另一张已完成的图，只读
    agent: 'reviewer',
    task: `只读复核 fig/figA.png 与其 FigureSpec：逐节点、逐边、逐字核对，
           列出缺陷与证据。不要修改任何文件。`,
  },
]);

const figB = results[0];
const reviewA = results[1];
return {
  figB: { status: figB.status, summary: figB.output?.slice(0, 2000) },
  reviewA: { status: reviewA.status, summary: reviewA.output?.slice(0, 2000) },
};
```

## 常见错误

| 错误写法 | 后果 | 正确写法 |
|---|---|---|
| `const runs = await runs.all([...])` | `ReferenceError: Cannot access 'runs' before initialization`——`runs` 是注入的宿主对象，被 `const` 同名遮蔽（TDZ），**子 agent 一个都不会启动** | `const results = await runs.all([...])`，换个变量名 |
| 逐个 `await runs.run(...)` 串行 | 失去并行，且中途失败难定位 | 独立任务用 `runs.all([...])`，返回顺序与入参一致 |
| 子 agent 直接写交付目录 | 两个 writer 争同一路径 | 中间产物分开；主 agent 做集成与最终 RenderAudit |
| 把审核委派给同模型的同角色 | 没有独立视角 | 复核用只读 reviewer，且与写图角色分离 |

## 验收分工

| 环节 | 归属 |
|---|---|
| 术语、证据、跨图风格一致 | 主 agent |
| 单图渲染与自检（spec 校验 + 目检 + RenderAudit v2） | worker（主 agent 复核） |
| 独立复核（文字、拓扑、色板、可访问性） | reviewer（只读） |
| 最终 RenderAudit、文件集成、交付 | 主 agent |

`runs.all` 返回的是有序数组，不是 key 映射；每个 run 的产物路径请用返回的
`outputReference` / `artifactPaths` 绑定，不要靠 task 文本里的文件名推断。

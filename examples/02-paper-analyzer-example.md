# Example: Paper Analyzer Output

Output shape from `academic-figure-paper-analyzer` (Figure Plan). Palette = **names only**; hex comes later from color-expert / `docs/palettes.md`.

---

# 论文配图规划报告

## 论文概览

| 项目 | 内容 |
|-----|------|
| **论文主题** | 高效扩散模型的注意力机制优化 |
| **主要贡献** | 降低 cross-attn 计算成本，同时保持生成质量 |
| **目标会议** | NeurIPS 2024 |
| **推荐配图总数** | 6–8 |

## 信息完整度说明

- **已分析材料**：摘要 + Method + Experiments 草稿；repo quick-understanding doc
- **当前输出类型**：完整规划
- **高置信信息**：需要 framework / U-Net arch / attention module / ablation
- **待确认信息**：是否单独出 noise-schedule 图
- **建议补充材料**：最终实验表（FID/IS 列）

## 章节配图规划

### 1. Introduction
- **Overall Framework** × 1（must）— 噪声 → 去噪 → 图像；标出改进 attn 位置  
- 宽高比 16:9

### 2. Related Work
- 无独立图；对比并入 framework 或 ablation

### 3. Method
- **Network Architecture** × 1（must）— U-Net 层级 + attn 插入点  
- **Module Detail** × 1（must）— 改进注意力内部数据流  
- **Comparison** × 1（strong）— 计算图 ours vs standard

### 4. Experiments
- **Comparison / Ablation** × 1–2（strong）— 样本网格 + 消融多面板  
- **Data Behavior** × 1（nice）— 可选效率曲线

## 优先级

| 优先级 | 图 |
|--------|----|
| must | Framework, Network Architecture, Attention Module Detail |
| strong | Computation comparison, Qualitative grid, Ablation |
| nice | Extra metric charts |

## 配色 handoff（→ color-expert）

不要在本阶段展开 hex 表。

```
venue: NeurIPS
domain: generative CV
figure_types: framework, architecture, module, ablation
module_count_framework: 4+
hint: prefer ML TopConf Colorblind; alternate Tab10 / Deep
```

---

*Demonstration output only.*

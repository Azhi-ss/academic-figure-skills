> Benchmark golden — derived from facebookresearch/esm @ 2b369911 (license: MIT).
> URL: https://github.com/facebookresearch/esm.git
> Pinned commit: 2b369911
> License: MIT

# 仓库快速理解文档

## 仓库概览

| 项目 | 内容 |
|---|---|
| 仓库名称 | facebookresearch/esm |
| 任务类型 | 蛋白质语言建模、表征、折叠与逆折叠 |
| 核心框架 | PyTorch |
| 主要架构 | ESM-2 Transformer；ESMFold 将冻结 ESM 表征接入 folding trunk 与结构头 |
| 一句话描述 | 以蛋白质序列 Transformer 表征支持接触预测、变异效应、逆折叠和单序列 3D 结构预测。 |

## 信息完整度说明

- 完整度：高。读取了 `README.md`、`esm/model/esm2.py`、`esm/esmfold/v1/esmfold.py`、`esm/modules.py` 与 `scripts/fold.py`。
- 仓库包含多个模型家族；总体图以 README 推荐的 ESM-2 → ESMFold 主路径为中心，并明确其他任务是旁支。

## 技术栈详情

- PyTorch/`nn.Module` 是主框架；ESMFold 还依赖 OpenFold 的残基常量、几何与损失工具。
- 顶层架构相关区域为 `esm/`、`scripts/`、`examples/`，分别承载模型库、批量入口与下游任务。
- 输入包括 FASTA/氨基酸序列；输出包括 residue embeddings、attention contacts、variant scores 或 PDB 结构。

## 模型架构分析

1. `ESM2`：氨基酸 token embedding → 多层 `TransformerLayer`（rotary embeddings）→ LayerNorm → tied LM head；可聚合各层注意力预测接触图。
2. `ESMFold`：预训练 ESM 模型在构造时 `requires_grad_(False)`；逐层序列表征经可学习加权和及 MLP 投影。
3. Folding trunk 同时维护 sequence 与 pair states，并通过 recycling 迭代结构表示。
4. distogram、pTM、LM、pLDDT 头输出几何与置信度，最终转换成原子坐标/PDB。

## 工作流程

- ESM-2 推理：序列 tokenize → Transformer → residue/sequence embeddings + 可选接触图。
- ESMFold 推理：序列 → 冻结 ESM-2 表征 → folding trunk/recycles → structure module → 坐标与 pLDDT → PDB。
- 原仓库主要分发预训练权重和推理/应用代码；完整预训练循环未作为本图主路径声称。

## 配图建议（→ paper-analyzer）

- Overall Framework：蛋白质序列到 ESM 表征，再分流至 embeddings/contact 与 ESMFold/PDB。
- Network Architecture：ESM-2 Transformer 与 ESMFold sequence/pair trunk。
- Module Detail：冻结 ESM 多层表征加权、pair state 与 recycling。
- Data Behavior：attention contact map、pLDDT 与结构可视化。

## Handoff (→ paper-analyzer)
module_count: source: top_level_dirs; value: 3
domain: Protein/AI4Science
figure_types: Overall Framework, Network Architecture, Module Detail, Data Behavior
evidence: high

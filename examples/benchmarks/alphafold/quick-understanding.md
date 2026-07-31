> Benchmark golden — derived from google-deepmind/alphafold @ c77e5d2a (license: Apache-2.0).
> URL: https://github.com/google-deepmind/alphafold.git
> Pinned commit: c77e5d2a
> License: Apache-2.0

# 仓库快速理解文档

## 仓库概览

| 项目 | 内容 |
|---|---|
| 仓库名称 | google-deepmind/alphafold |
| 任务类型 | 蛋白质单体/多聚体 3D 结构预测 |
| 核心框架 | JAX + Haiku |
| 主要架构 | MSA/模板特征 → Evoformer → Structure Module → recycling 与置信度头 |
| 一句话描述 | 从 FASTA 和遗传数据库构建 MSA/模板特征，经 AlphaFold 推理与松弛输出排序后的 PDB 结构。 |

## 信息完整度说明

- 完整度：高。读取了 `README.md`、`run_alphafold.py`、`alphafold/model/model.py`、`alphafold/model/modules.py` 与模型目录。
- 此公开仓库明确提供 AlphaFold v2 推理管线；不把未随仓库提供的训练管线描述为可运行入口。

## 技术栈详情

- JAX 执行数组计算与 JIT；Haiku 定义模块；`ml_collections` 管理模型配置。
- 数据层调用 JackHMMER/HHblits/HHsearch/HMMsearch/Kalign，读取 UniRef、MGnify、BFD、PDB/mmCIF 等数据库。
- 顶层功能区域计为 `alphafold/`、`afdb/`、`docker/`、`docs/`、`notebooks/`、`scripts/`、`server/` 共 7 个。

## 模型架构分析

1. 数据管线由 FASTA 搜索 MSA 与模板，形成 sequence、MSA、pair 和 template features。
2. `EmbeddingsAndEvoformer` 生成 MSA、single 与 pair representations；`EvoformerIteration` 交替更新 MSA 与 pair 通道。
3. `StructureModule` 从 single/pair 表征生成骨架、侧链和原子坐标；模型在 recycling 迭代中回馈先前结果。
4. distogram、masked-MSA、pLDDT、predicted-aligned-error/pTM 等头提供预测与置信度；Amber relaxation 可后处理结构。

## 工作流程

- FASTA → 序列数据库搜索与 MSA → 模板检索/mmCIF → 特征处理 → 多模型 JAX/Haiku 推理 → pLDDT/pTM 排序 → 可选 Amber relaxation → PDB 与 JSON 结果。
- `RunModel.predict` 对 Haiku forward 做 JIT，随后计算 pLDDT、PAE、pTM/ipTM 等置信度。

## 配图建议（→ paper-analyzer）

- Overall Framework：FASTA、MSA/模板、Evoformer、Structure Module、recycling、排序/松弛。
- Network Architecture：MSA 与 pair 双通道 Evoformer 到结构模块。
- Module Detail：Evoformer block 或 recycling 反馈路径。
- Data Behavior：PAE/pLDDT 置信度图与预测结构。

## Handoff (→ paper-analyzer)
module_count: source: top_level_dirs; value: 7
domain: Protein/AI4Science
figure_types: Overall Framework, Network Architecture, Module Detail, Data Behavior
evidence: high

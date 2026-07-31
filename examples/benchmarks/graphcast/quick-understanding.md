> Benchmark golden — derived from google-deepmind/graphcast @ 08cf7362 (license: Apache-2.0).
> URL: https://github.com/google-deepmind/graphcast.git
> Pinned commit: 08cf7362
> License: Apache-2.0

# 仓库快速理解文档

## 仓库概览

| 项目 | 内容 |
|---|---|
| 仓库名称 | google-deepmind/graphcast |
| 任务类型 | 中期全球天气预报与自回归 rollout |
| 核心框架 | JAX + Haiku + Jraph |
| 主要架构 | 规则经纬网与多分辨率球面网格之间的 encoder–processor–decoder GNN |
| 一句话描述 | 将 ERA5 网格天气映射到 icosahedral mesh，消息传递后映回网格，并自回归生成多步预报。 |

## 信息完整度说明

- 完整度：高。读取了 `README.md`、`graphcast/graphcast.py`、`graphcast/typed_graph_net.py`、`graphcast/rollout.py` 与 `setup.py`。
- 仓库也包含 GenCast；本分析聚焦名称对应的 GraphCast 主模型，不把 GenCast diffusion/sparse-transformer 路径混入架构图。

## 技术栈详情

- JAX/Haiku 用于模型与变换，Jraph/TypedGraph 用于图结构；XArray 表达带坐标的天气张量。
- ERA5 提供表面与多气压层变量；太阳辐射、年/日周期及静态地形作为 forcing/static features。
- 顶层架构区域为 `graphcast/` 与 `docs/`，模块计数为 2。

## 模型架构分析

1. Grid2Mesh encoder 构造规则网格到球面 mesh 的二部图，并做一次消息传递。
2. Mesh processor 在多层 icosahedral mesh 上执行配置数量的 GNN message passing。
3. Mesh2Grid decoder 将 mesh latent 传回每个网格点，输出目标大气与地表变量。
4. `typed_graph_net.py` 先更新边、聚合消息再更新节点；`rollout.py` 将一步预测循环成多时刻 trajectory。

## 工作流程

- 历史天气 inputs + target-time forcings → normalization/feature packing → Grid2Mesh → Mesh GNN → Mesh2Grid → 一步天气增量/状态。
- 推理 rollout 将上一时刻输出反馈成下一步输入，拼接出中期 forecast trajectory；训练代码可通过可微 autoregressive wrapper 优化纬度加权损失。

## 配图建议（→ paper-analyzer）

- Overall Framework：天气网格 → Grid2Mesh encoder → Mesh processor → Mesh2Grid decoder → 自回归预报。
- Network Architecture：三种 TypedGraph 与节点/边集合。
- Module Detail：边更新—消息聚合—节点更新的 message passing。
- Data Behavior：多步 rollout 轨迹或全球误差/变量热图。

## Handoff (→ paper-analyzer)
module_count: source: top_level_dirs; value: 2
domain: GNN/ScientificComputing
figure_types: Overall Framework, Network Architecture, Module Detail, Data Behavior
evidence: high

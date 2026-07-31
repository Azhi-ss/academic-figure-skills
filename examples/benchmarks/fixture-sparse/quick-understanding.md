> Benchmark golden — derived from synthetic fixture-sparse @ N/A (license: —).
> URL: synthetic: academic-repo-analyzer/scripts/create_sparse_fixture.py
> Pinned commit: N/A
> License: —

# 仓库快速理解文档

## 仓库概览

| 项目 | 内容 |
|---|---|
| 仓库名称 | fixture-sparse / Sparse Scientific Simulator |
| 任务类型 | 非 ML 的玩具 N-body 科学模拟器 |
| 核心框架 | Python 标准库；无神经网络框架 |
| 主要架构 | CLI 入口 + Lennard-Jones 势函数 + 简化的积分步函数 |
| 一句话描述 | `simulate.py` 只解析步数并打印结果；两个科学组件存在于 `src/`，但当前入口未调用它们。 |

## 信息完整度说明

- 完整度：稀疏。仓库仅有 `README.md`、`simulate.py`、`src/lennard_jones.py`、`src/integrator.py` 四个文件。
- 已定位入口脚本 `simulate.py`，但没有依赖清单、测试、数据、训练/推理循环或组件编排。
- 流程结论标记为证据不足 / evidence insufficient；不把两个孤立函数虚构成已连通的模拟管线。

## 技术栈详情

- `argparse` 解析 `--steps`；其余仅使用 Python 算术、列表推导与 `zip`。
- `lennard_jones.py` 定义 `potential(r) = 4(r^-12 - r^-6)`。
- `integrator.py` 声称 Velocity-Verlet，但实现只做 `p + v*dt` 并原样返回速度，应按代码称为简化位置更新。

## 模型架构分析

- 无模型文件、神经网络或可学习参数。
- component_scan 得到两个命名科学组件：Lennard-Jones potential 与 integrator step。
- `simulate.py` 当前不 import `src`，因此只能绘制“现状组件清单”，不能声称存在运行时数据流。

## 工作流程

- 已证实入口：`python simulate.py --steps N` → 参数解析 → 打印 `simulated N steps`。
- 预期物理模拟流程（力/势 → 积分 → 状态更新）在代码中证据不足，未实现端到端连接。

## 配图建议（→ paper-analyzer）

- Overall Framework：现状代码地图，区分已连接 CLI 与未连接科学组件。
- Module Detail：Lennard-Jones 势函数及简化积分步。
- Comparison：已实现路径与完整 N-body 模拟尚缺环节。

## Handoff (→ paper-analyzer)
module_count: source: component_scan; value: 2
domain: ScientificComputing(non-ML)
figure_types: Overall Framework, Module Detail, Comparison
evidence: sparse

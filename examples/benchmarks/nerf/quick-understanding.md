> Benchmark golden — derived from bmild/nerf @ 14c55567 (license: MIT).
> URL: https://github.com/bmild/nerf.git
> Pinned commit: 14c55567
> License: MIT

# 仓库快速理解文档

## 仓库概览

| 项目 | 内容 |
|---|---|
| 仓库名称 | bmild/nerf |
| 任务类型 | 神经辐射场（Neural Radiance Fields）体渲染与新视角合成 |
| 核心框架 | TensorFlow 1.x（使用 `tf.compat.v1` 并禁用 v2 行为/eager） |
| 主要架构 | 位置编码 + 多层 MLP（coarse + fine）+ 沿射线体积积分 |
| 一句话描述 | NeRF 论文官方 TensorFlow 实现，将 5D 坐标映射为密度与 RGB 并通过体渲染合成图像。 |

## 信息完整度说明

- 完整度：高。读取了 `README.md`、`run_nerf.py`、`run_nerf_helpers.py`、`load_llff.py`、`load_blender.py`、`load_deepvoxels.py` 及若干 config。
- 仓库为扁平布局，没有顶层包目录；按 component_scan 计数为 4：NeRF MLP（`init_nerf_model`）、位置编码（`Embedder`/`get_embedder`）、体渲染射线管线（`render_rays`/`render`/`batchify_rays`）、数据加载器（LLFF/Blender/DeepVoxels）。

## 技术栈详情

- TensorFlow 1.15 风格 API：`tf.compat.v1`、`tf.train.AdamOptimizer`、`tf.estimator`/`tf.Summary`；`tf.config.experimental.set_visible_devices` 管理 GPU。
- 图像加载与相机处理使用 imageio、numpy、`load_llff.py` 中的位姿/视锥变换；可选 `tf.image.ssim`/`psnr` 指标。
- 入口为 `run_nerf.py`，子命令 `--config` 选择 llff/blender/deepvoxels 配置；notebook `tiny_nerf.ipynb`、`render_demo.ipynb` 提供精简演示。

## 模型架构分析

1. 输入为 3D 位置 $\mathbf{x}\in\mathbb{R}^3$ 与视角方向 $\mathbf{d}\in\mathbb{R}^3$，经 `get_embedder` 用正余弦位置编码映射到高维（默认 multires=10/4）。
2. `init_nerf_model(D=8, W=256, skips=[4])` 构建 MLP，输出 RGB 与密度 $\sigma$；按 hierarchical sampling 同时训练 coarse 与 fine 两个网络。
3. `render_rays` 对每条射线在近远平面间采样 $N_s$ 个点，查询网络后按 $\alpha$-compositing 累加 RGB 与深度；fine 网络通过 `sample_pdf` 按 coarse 权重重要性采样。
4. `render` 由相机位姿通过 `get_rays` 批量生成射线，`batchify_rays` 按 `chunk` 分片以适应显存；训练损失为 coarse+fine 的 MSE。

## 工作流程

- 数据加载（LLFF/Blender/DeepVoxels）→ 构建射线批次 → coarse MLP 前向 → PDF 采样 → fine MLP 前向 → 体渲染积分 → MSE 损失 → Adam 优化 → 周期渲染验证图与 PSNR/SSIM。
- 测试阶段 `render_path` 沿螺旋/插值相机轨迹渲染新视角并导出视频/图像。

## 配图建议（→ paper-analyzer）

- Overall Framework：位姿→射线→采样→coarse/fine MLP→体积积分→图像的闭环。
- Network Architecture：位置编码层、含 skip 连接的 MLP、RGB/密度双头。
- Module Detail：hierarchical sampling + `sample_pdf` 与 $\alpha$-compositing 公式。
- Data Behavior：训练 PSNR 曲线或 novel-view 渲染结果对比。

## Handoff (→ paper-analyzer)
module_count: source: component_scan; value: 4
domain: CV
figure_types: Overall Framework, Network Architecture, Module Detail, Data Behavior
evidence: high

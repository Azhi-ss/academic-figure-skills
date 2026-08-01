# Classic Repositories

经典深度学习仓库精选，作为 `academic-repo-analyzer` 技能的真实参考样例。

这些仓库通过 `examples/benchmarks/manifest.json` 浅克隆到 git 忽略的 `ref_repos/`，
对应的分析文档、配图规划和 JSON 配图规范提交在 [`../benchmarks/<id>/`](../benchmarks/)。

## 仓库列表

| 仓库 | 领域 | 许可证 | 看点 |
|---|---|---|---|
| [CompVis/stable-diffusion](https://github.com/CompVis/stable-diffusion) | 扩散 / 文生图 | CreativeML Open RAIL-M | 潜空间扩散、CLIP 条件、U-Net + VAE |
| [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) | NLP / 语言模型 | MIT | 单文件 GPT、最小训练/采样循环 |
| [facebookresearch/esm](https://github.com/facebookresearch/esm) | 蛋白质 / AI4Science | MIT | 蛋白质序列 Transformer、MSA |
| [google-deepmind/alphafold](https://github.com/google-deepmind/alphafold) | 蛋白质 / JAX | Apache-2.0 | Evoformer、Structure Module、JAX/Haiku |
| [google-deepmind/graphcast](https://github.com/google-deepmind/graphcast) | GNN / 气象 | Apache-2.0 | Encoder-processor-decoder、GNN rollout |
| [huggingface/transformers](https://github.com/huggingface/transformers) | 超大仓库 / 通用 | Apache-2.0 | 多架构集合、抽样上限压力测试 |
| [junyanz/pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix) | GAN / 图像翻译 | BSD-3-Clause | 双生成器/判别器、循环一致性、PatchGAN |
| [bmild/nerf](https://github.com/bmild/nerf) | 3D / 神经渲染 | MIT | NeRF MLP、位置编码、体渲染 |
| [facebookresearch/detr](https://github.com/facebookresearch/detr) | 目标检测 | Apache-2.0 | Transformer 检测、集合预测、二分匹配 |
| [openai/whisper](https://github.com/openai/whisper) | 语音 / ASR | MIT | 编码器-解码器、Mel 频谱前端 |

## 复现

```bash
# 1. 浅克隆全部仓库到 ref_repos/（git 忽略）
python3 academic-repo-analyzer/scripts/fetch_benchmark_repos.py \
  --manifest examples/benchmarks/manifest.json

# 2. 仅拉取经典仓库子集
python3 academic-repo-analyzer/scripts/fetch_benchmark_repos.py \
  --manifest examples/benchmarks/manifest.json \
  --repos cyclegan nerf detr whisper

# 3. 查看某个仓库的分析黄金样例
cat examples/benchmarks/nerf/quick-understanding.md
cat examples/benchmarks/nerf/figure-plan.md
cat examples/benchmarks/nerf/prompt-spec.json
```

实际拉取的 commit 记录在 `ref_repos/fetch-log.json`；每份黄金样例的头部记录了它所基于的短 SHA。

## 与 benchmarks 的关系

- `examples/benchmarks/` 是**机器可评分**的基准：脚本、manifest、评分器、黄金样例。
- `examples/classic-repos/`（本目录）是**人工浏览入口**：按主题分组的仓库清单和说明。

新增仓库时同时更新两个地方：
1. `examples/benchmarks/manifest.json` 加入仓库元数据
2. 本文件的表格加入一行

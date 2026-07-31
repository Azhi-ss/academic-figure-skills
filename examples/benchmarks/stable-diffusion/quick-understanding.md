> Benchmark golden — derived from CompVis/stable-diffusion @ 21f890f9 (license: CreativeML Open RAIL-M).
> URL: https://github.com/CompVis/stable-diffusion.git
> Pinned commit: 21f890f9
> License: CreativeML Open RAIL-M

# 仓库快速理解文档

## 仓库概览

| 项目 | 内容 |
|---|---|
| 仓库名称 | CompVis/stable-diffusion |
| 任务类型 | 文本条件潜空间扩散（text-to-image latent diffusion） |
| 核心框架 | PyTorch + PyTorch Lightning |
| 主要架构 | 冻结 CLIP 文本编码器 + AutoencoderKL + 带交叉注意力的 U-Net 去噪器 |
| 一句话描述 | 将图像压缩到潜空间，在文本条件下迭代去噪，再解码为 512×512 图像。 |

## 信息完整度说明

- 完整度：高。读取了 `README.md`、`configs/stable-diffusion/v1-inference.yaml`、`ldm/models/diffusion/ddpm.py`、`ldm/modules/diffusionmodules/openaimodel.py` 与 `scripts/txt2img.py`。
- 仓库同时含训练入口 `main.py` 与多种推理脚本；本分析聚焦 Stable Diffusion v1 文生图主路径。
- 软件仓库根 `LICENSE` 与已更正的 benchmark manifest 均记录 CreativeML Open RAIL-M。

## 技术栈详情

- `environment.yaml` 与 README 明示 PyTorch、torchvision、transformers、diffusers；训练封装使用 PyTorch Lightning。
- 配置通过 OmegaConf 实例化模型；`main.py` 负责训练，`scripts/txt2img.py` 负责 PLMS/DDIM 采样。
- 核心路径：`ldm/`（实现）、`configs/`（模型配置）、`models/`（权重目录结构）、`scripts/`（采样与工具）。

## 模型架构分析

1. `FrozenCLIPEmbedder` 将提示词变为 768 维上下文；`cond_stage_trainable: false`。
2. `AutoencoderKL` 以 8 倍下采样将像素图像映射到 4 通道潜变量，并负责最终解码。
3. `UNetModel` 由下采样块、中间块、上采样块和跳连组成；`SpatialTransformer` 接收文本上下文做交叉注意力。
4. `LatentDiffusion`/`DDPM` 注册噪声日程并以 epsilon 或 x0 参数化训练；推理可用 DDIM/PLMS 反向采样。

## 工作流程

- 训练：图像 → AutoencoderKL 潜变量 → 加噪 → 文本条件 U-Net 预测噪声 → 扩散损失；`main.py` 驱动 Lightning 训练。
- 推理：提示词 → 冻结 CLIP → 随机潜噪声 → 多步 U-Net 去噪（classifier-free guidance）→ AutoencoderKL 解码 → 安全检查/水印与保存。

## 配图建议（→ paper-analyzer）

- Overall Framework：文本条件、潜空间扩散、解码输出的端到端流程。
- Network Architecture：U-Net 编码器—瓶颈—解码器、跳连与交叉注意力位置。
- Module Detail：classifier-free guidance 与每步 DDIM/PLMS 更新。
- Data Behavior：不同 guidance scale 或采样步数的生成结果网格。

## Handoff (→ paper-analyzer)
module_count: source: top_level_dirs; value: 4
domain: Generative
figure_types: Overall Framework, Network Architecture, Module Detail, Data Behavior
evidence: high

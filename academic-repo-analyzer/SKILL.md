---
id: academic-repo-analyzer
name: Academic Repo Analyzer
version: 1.0.0
description: Use this skill whenever the user wants to analyze a deep learning/machine learning code repository to understand what it does, identify the model architecture, core algorithms, tech stack, and key innovations, then generate a "quick understanding document" that can be passed to the paper-analyzer skill. Trigger phrases: "分析代码仓库", "仓库分析", "repo analyzer", "analyze this repo", "理解这个代码库", "what does this repo do".
stages: [research, review]
tools: [bash]
---

# Academic Repo Analyzer — 学术代码仓库分析器

全面分析深度学习/机器学习代码仓库，自动识别任务类型、模型架构、核心算法、技术栈和创新点，生成"快速理解文档"。

## 核心理念

通过系统性地扫描代码仓库结构，提取关键信息，让用户在几分钟内理解一个陌生的 ML/DL 代码仓库。

## 工作流程

### Step 1: 仓库结构扫描

首先，获取仓库的完整目录结构：

```
仓库结构清单：
├── README.md（首要分析对象）
├── setup.py / requirements.txt / environment.yml（依赖分析）
├── main.py / train.py / eval.py / inference.py（入口文件）
├── configs/ / cfg/ / hparams/（配置文件）
├── models/ / model/ / networks/ / src/（模型定义）
├── utils/ / helpers/ / tools/（工具函数）
├── datasets/ / data/ / loader.py（数据加载）
└── 其他关键文件
```

**必须读取的文件：**
- README.md（项目介绍）
- 依赖文件（技术栈识别）
- 主要入口脚本（工作流理解）
- 模型定义文件（架构识别）

### Step 2: 任务类型识别

根据关键词和文件结构判断任务类型：

| 任务类型 | 关键词 | 文件特征 |
|---------|-------|---------|
| **计算机视觉（CV）** | `image`, `cv2`, `PIL`, `resnet`, `vit`, `unet`, `detection`, `segmentation`, `classification` | 数据集目录含图像，使用 torchvision, mmcv 等 |
| **自然语言处理（NLP）** | `text`, `token`, `bert`, `gpt`, `transformer`, `llm`, `sentence`, `corpus` | 使用 transformers, datasets, tokenizers 等 |
| **强化学习（RL）** | `policy`, `agent`, `environment`, `reward`, `ppo`, `dqn`, `sac`, `gym`, `env` | 环境交互循环，奖励函数定义 |
| **机器人（Robotics）** | `robot`, `kinematics`, `dynamics`, `simulation`, `gazebo`, `ros`, `control` | 物理模拟，机器人模型 |
| **多模态（Multimodal）** | `image-text`, `vision-language`, `clip`, `multimodal`, `cross-modal` | 同时处理图像和文本 |
| **时间序列（Time Series）** | `timeseries`, `forecast`, `temporal`, `sequence`, `lstm`, `gru` | 时间维度处理，预测任务 |
| **生成模型（Generative）** | `gan`, `diffusion`, `vae`, `generative`, `generation`, `synthesize` | 生成任务，对抗训练，扩散过程 |

### Step 3: 技术栈识别

分析依赖文件和代码导入：

| 框架 | 识别特征 |
|------|---------|
| **PyTorch** | `import torch`, `nn.Module`, `torch.nn`, `torch.utils.data` |
| **TensorFlow** | `import tensorflow`, `tf.keras`, `tf.layers` |
| **JAX/Flax** | `import jax`, `flax`, `haiku`, `optax` |
| **MxNet/Gluon** | `import mxnet`, `gluon` |
| **PaddlePaddle** | `import paddle` |

**辅助库识别：**
- 计算机视觉：`torchvision`, `mmcv`, `detectron2`, `albumentations`
- NLP：`transformers`, `datasets`, `tokenizers`, `nltk`, `spacy`
- 强化学习：`gym`, `stable-baselines3`, `ray[rllib]`
- 科学计算：`numpy`, `scipy`, `pandas`, `matplotlib`
- 实验管理：`wandb`, `mlflow`, `tensorboard`, `ignite`
- 分布式训练：`torch.distributed`, `deepspeed`, `accelerate`

### Step 4: 模型架构和核心算法提取

从模型定义文件中提取：

**架构关键词：**
- `Transformer`, `Attention`, `Self-Attention`, `Cross-Attention`
- `CNN`, `ResNet`, `ViT`, `Swin`, `U-Net`, `FPN`
- `RNN`, `LSTM`, `GRU`, `Seq2Seq`
- `GNN`, `GCN`, `GAT`, `Graph`
- `GAN`, `Diffusion`, `VAE`, `Flow`

**核心算法点：**
- 损失函数定义（搜索 `loss =`, `criterion =`）
- 新颖的模块或层（带注释或非标准命名）
- 数据增强策略
- 训练策略和技巧（学习率调度、优化器选择）

### Step 5: 生成快速理解文档

按照以下格式输出：

---

# 仓库快速理解文档

## 📊 仓库概览

| 项目 | 内容 |
|-----|------|
| **仓库名称** | [从目录名或 README 提取] |
| **任务类型** | [CV/NLP/RL/Robotics/多模态等] |
| **核心框架** | [PyTorch/TensorFlow/JAX 等] |
| **主要架构** | [识别的模型架构] |
| **一句话描述** | [用一句话概括这个仓库做什么] |

## 🏗️ 技术栈详情

**核心框架：**
- [框架 1]
- [框架 2]

**主要依赖：**
- [库 1] - [用途]
- [库 2] - [用途]

**实验管理：**
- [工具名，如有]

## 🧠 模型架构分析

**整体架构：**
[描述整体网络结构，如 encoder-decoder、堆叠 Transformer 等]

**关键组件：**
- [组件 1] - [功能描述]
- [组件 2] - [功能描述]

**核心创新点（推测）：**
1. [创新点 1]
2. [创新点 2]

## 📝 工作流程

**训练流程：**
1. 数据加载 → [描述]
2. 前向传播 → [描述]
3. 损失计算 → [描述]
4. 反向传播 → [描述]

**推理流程：**
[如适用，描述推理逻辑]

## 🎨 配图建议（传递给 paper-analyzer）

**推荐配图类型：**
- Overall Framework（总体框架图）× 1
- Network Architecture（网络架构图）× 1
- [关键模块] Module Detail（模块细节图）× [1-2]
- [其他推荐配图]

**核心贡献可视化建议：**
[描述如何最好地可视化这个仓库的核心思想]

---

## 与 paper-analyzer 配合

生成此文档后，建议用户：

> 提示：现在可以使用「Academic Paper Analyzer & Figure Planner」技能，基于这份快速理解文档来规划详细的论文配图。

## 输出格式

每次分析完成后，按照上述格式输出完整的 markdown 文档。

## 注意事项

1. **证据导向**：基于实际发现的文件和代码做出判断，不确定时注明"推测"
2. **优先级**：README > 入口脚本 > 模型定义 > 其他文件
3. **简洁性**：快速理解文档应控制在 1-2 页阅读量
4. **后续衔接**：确保"配图建议"部分与 paper-analyzer 的输入格式兼容

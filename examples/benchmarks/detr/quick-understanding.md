> Benchmark golden — derived from facebookresearch/detr @ 29901c51 (license: Apache-2.0).
> URL: https://github.com/facebookresearch/detr.git
> Pinned commit: 29901c51
> License: Apache-2.0

# 仓库快速理解文档

## 仓库概览

| 项目 | 内容 |
|---|---|
| 仓库名称 | facebookresearch/detr |
| 任务类型 | 端到端目标检测（DETR，集合预测）与全景/实例分割 |
| 核心框架 | PyTorch（含 detectron2 集成 `d2/`） |
| 主要架构 | CNN backbone + 位置编码 + Transformer encoder/decoder + object queries + 二分图匈牙利匹配 |
| 一句话描述 | 用 Transformer 直接输出检测集合，以 Hungarian matching 和 set prediction loss 去掉 NMS/anchor 的端到端检测器。 |

## 信息完整度说明

- 完整度：高。读取了 `README.md`、`main.py`、`engine.py`、`models/detr.py`、`models/transformer.py`、`models/backbone.py`、`models/matcher.py`、`models/position_encoding.py`、`models/segmentation.py`、`datasets/`、`d2/`、`util/`。
- 顶层包/模块目录共 4 个（`models/`、`datasets/`、`d2/`、`util/`），按 top_level_dirs 计数为 4；`engine.py`、`main.py`、`hubconf.py`、`run_with_submitit.py` 为入口/脚本，不计入模块。

## 技术栈详情

- PyTorch + torchvision；`models/backbone.py` 封装 ResNet-50 等 backbone 并附 `PositionEmbeddingSine`；`models/transformer.py` 实现标准 `TransformerEncoder`/`TransformerDecoder` 与多头注意力。
- `models/matcher.py` 的 `HungarianMatcher` 用 scipy `linear_sum_assignment` 在分类概率与 L1/GIoU 代价上做二分图匹配；`SetCriterion` 计算分类、边界框 L1、GIoU 损失（+ mask 损失用于分割）。
- `datasets/` 提供 COCO 与 panoptic 数据 transforms/coco_eval；`d2/` 是 detectron2 集成；`util/` 包含 box_ops、misc、`plot_utils`。
- 入口为 `main.py`（训练/验证 CLI，含分布式与 mixed precision），`engine.py` 实现 `train_one_epoch` 与 `evaluate`；`hubconf.py` 提供 torch.hub 模型加载。

## 模型架构分析

1. 输入图像经 CNN backbone 提取多尺度或最后一层特征，并加入 sine positional encoding。
2. `Transformer` encoder 在图像特征 token 上做自注意力；decoder 学习一组固定 object queries，交叉关注 encoder 输出。
3. 每个 query 经 `Linear` 头输出分类 logits 与边界框坐标（sigmoid 归一化的 cxcywh）。
4. `HungarianMatcher` 将预测与真值一对一匹配，`SetCriterion` 计算类别 ce/focal loss、bbox L1 与 GIoU loss；后处理直接取 top-k，无需 NMS。

## 工作流程

- 数据增强（RandomResize/Crop/Flip）→ COCO DataLoader → backbone → Transformer → prediction heads → Hungarian matching → set prediction loss → 反传（冻结/不冻结 backbone 由 lr 区分） → `evaluate` 用 pycocotools 计算 mAP。
- 推理：`detr.eval()` 前向 → `PostProcess` 将 cxcywh 转 xyxy → 按 score 过滤输出框与类别。

## 配图建议（→ paper-analyzer）

- Overall Framework：图像→backbone→Transformer encoder/decoder→object queries→二分图匹配→loss 的闭环。
- Network Architecture：backbone + positional encoding + Transformer encoder/decoder + FFN heads。
- Module Detail：Hungarian matching 代价矩阵与 L1/GIoU 集合损失。
- Data Behavior：训练 loss/mAP 曲线或 query-to-object 可视化。

## Handoff (→ paper-analyzer)
module_count: source: top_level_dirs; value: 4
domain: CV
figure_types: Overall Framework, Network Architecture, Module Detail, Data Behavior
evidence: high

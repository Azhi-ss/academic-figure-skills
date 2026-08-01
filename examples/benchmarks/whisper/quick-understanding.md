> Benchmark golden — derived from openai/whisper @ 5f86d1d8 (license: MIT).
> URL: https://github.com/openai/whisper.git
> Pinned commit: 5f86d1d8
> License: MIT

# 仓库快速理解文档

## 仓库概览

| 项目 | 内容 |
|---|---|
| 仓库名称 | openai/whisper |
| 任务类型 | 自动语音识别（ASR）与语音翻译（多语言） |
| 核心框架 | PyTorch |
| 主要架构 | log-mel 前端（Conv1d 下采样）+ Transformer audio encoder + Transformer text decoder（cross-attention） |
| 一句话描述 | OpenAI Whisper 官方 PyTorch 实现，弱监督训练的多语种语音识别/翻译 encoder-decoder Transformer。 |

## 信息完整度说明

- 完整度：高。读取了 `README.md`、`model-card.md`、`whisper/model.py`、`whisper/audio.py`、`whisper/decoding.py`、`whisper/transcribe.py`、`whisper/tokenizer.py`、`whisper/__init__.py`、`whisper/triton_ops.py`。
- 仓库所有可训练代码集中在单一顶层包 `whisper/`，按 top_level_dirs 计数为 1（与 nanoGPT 单一 `model.py` 的校准一致）；`tests/`、`notebooks/`、`data/` 不计入框架模块。

## 技术栈详情

- PyTorch + NumPy；`whisper/audio.py` 用 ffmpeg/`torch` STFT 计算 80-bin log-mel，`whisper/model.py` 定义 `AudioEncoder`、`TextDecoder`、`Whisper` 与 `sinusoids` 位置编码。
- `whisper/tokenizer.py` 基于 tiktoken 构建多语种 tokenizer；`whisper/decoding.py` 实现 greedy/beam/prefix/word-timestamps 解码；`whisper/transcribe.py` 提供高级 CLI/`transcribe` API。
- Triton 内核 `whisper/triton_ops.py` 可选加速 decoder attention；入口为 `python -m whisper`（`whisper/__main__.py`）和 `transcribe()`。

## 模型架构分析

1. `audio.py` 将波形 pad/trim 到 30s 后计算 80-bin log-mel spectrogram。
2. `AudioEncoder`：两层 Conv1d（第一层 kernel=3，第二层 stride=2）下采样后加 `sinusoids` 位置嵌入，再经过 N 个 `ResidualAttentionBlock`（multi-head self-attention + MLP），最后 LayerNorm。
3. `TextDecoder`：token + learned positional embedding，多层 masked self-attention + 对 encoder 输出的 cross-attention + MLP；输出接 tied embedding 的 LM head。
4. `Whisper` 容器组装 encoder/decoder，`logits` 通过 `detect_language` 与多语言 token 支持语种识别和翻译；`ModelDimensions` 决定 tiny→large 各尺寸。

## 工作流程

- 推理：ffmpeg 加载音频 → pad/trim → log-mel → `AudioEncoder` → `TextDecoder` 自回归生成 → tokenizer 解码为文本；`DecodingTask` 支持 beam search、temperature fallback、word timestamps。
- 训练（论文/mc 说明，仓库本身只含推理权重加载）：弱监督多语种语音-文本对，encoder-decoder 交叉熵 + 可选 X→En 翻译头。

## 配图建议（→ paper-analyzer）

- Overall Framework：音频波形 → log-mel → audio encoder → text decoder → 文本的端到端 ASR 流。
- Network Architecture：Conv1d 前端 + sinusoidal position + Transformer encoder/decoder with cross-attention。
- Module Detail：`ResidualAttentionBlock` 的 masked self-attention 与 cross-attention，或 log-mel 计算管线。
- Data Behavior：语种分布、WER 随模型尺寸曲线或解码温度 fallback 行为。

## Handoff (→ paper-analyzer)
module_count: source: top_level_dirs; value: 1
domain: Other
figure_types: Overall Framework, Network Architecture, Module Detail, Data Behavior
evidence: high

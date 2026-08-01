> Benchmark golden — derived from openai/whisper @ 5f86d1d8 (license: MIT).
> URL: https://github.com/openai/whisper.git
> Pinned commit: 5f86d1d8
> License: MIT

# Figure Plan

## Paper overview

- Topic: openai/whisper repository architecture for multilingual speech recognition and translation.
- Contribution focus: log-mel front-end, Transformer audio encoder, and Transformer text decoder with cross-attention.
- module_count_framework: 1
- palette: classic academic; venue: None; domain: Other

## Completeness

This system-centric plan is grounded in the pinned repository snapshot. Paper narrative, claims, and experimental priorities require separate manuscript review.

## Per-section recommendations

| # | figure type | aspect_ratio | must-appear elements / rationale | priority |
|---|---|---|---|---|
| 1 | Overall Framework | 16:9 | Waveform, log-mel, AudioEncoder, TextDecoder, autoregressive text output | must |
| 2 | Network Architecture | 16:9 | Conv1d front-end, sinusoidal position embedding, encoder blocks, decoder blocks with masked self-attention and cross-attention | must |
| 3 | Module Detail | 4:3 | ResidualAttentionBlock: masked self-attention plus encoder-decoder cross-attention | strong |
| 4 | Data Behavior | 4:3 | Language distribution or WER across model sizes and temperature fallback | nice |

## Priority summary

- Must: Overall Framework and Network Architecture when listed.
- Strong: module mechanism and behavior/comparison figures supported by code evidence.
- Nice: data-behavior comparisons when a manuscript or model card supports them.

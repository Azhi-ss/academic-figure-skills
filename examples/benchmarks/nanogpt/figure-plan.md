> Benchmark golden — derived from karpathy/nanoGPT @ 3adf61e1 (license: MIT).
> URL: https://github.com/karpathy/nanoGPT.git
> Pinned commit: 3adf61e1
> License: MIT

# Figure Plan

## Paper overview

- Topic: karpathy/nanoGPT repository architecture and executable research workflow.
- Contribution focus: evidence-backed modules and dataflow from the Quick Understanding Doc.
- module_count_framework: 1
- palette: classic academic; venue: None; domain: NLP

## Completeness

This system-centric plan is grounded in the pinned repository snapshot. Paper narrative, claims, and experimental priorities require separate manuscript review.

## Per-section recommendations

| # | figure type | aspect_ratio | must-appear elements / rationale | priority |
|---|---|---|---|---|
| 1 | Overall Framework | 16:9 | Token data, GPT training, checkpoint and text sampling | must |
| 2 | Network Architecture | 16:9 | Embeddings, repeated Transformer block and LM head | must |
| 3 | Module Detail | 4:3 | Causal attention with Flash or masked fallback | strong |
| 4 | Data Behavior | 4:3 | Training and validation loss | strong |

## Priority summary

- Must: Overall Framework and Network Architecture when listed.
- Strong: module mechanism and behavior/comparison figures supported by code evidence.
- Nice: none added without manuscript evidence.

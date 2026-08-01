> Benchmark golden — derived from junyanz/pytorch-CycleGAN-and-pix2pix @ 2a7afba2 (license: BSD-3-Clause).
> URL: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.git
> Pinned commit: 2a7afba2
> License: BSD-3-Clause

# Figure Plan

## Paper overview

- Topic: junyanz/pytorch-CycleGAN-and-pix2pix repository architecture and unpaired/paired image-translation training loop.
- Contribution focus: dual-generator/dual-discriminator CycleGAN with cycle-consistency loss, plus pix2pix paired baseline.
- module_count_framework: 6
- palette: classic academic; venue: None; domain: Generative

## Completeness

This system-centric plan is grounded in the pinned repository snapshot. Paper narrative, claims, and experimental priorities require separate manuscript review.

## Per-section recommendations

| # | figure type | aspect_ratio | must-appear elements / rationale | priority |
|---|---|---|---|---|
| 1 | Overall Framework | 16:9 | Domains A/B, G_A, G_B, D_A, D_B, cycle and identity losses, optimizer alternation | must |
| 2 | Network Architecture | 16:9 | ResnetGenerator (downsample, 9 residual blocks, upsample) and NLayerDiscriminator PatchGAN | must |
| 3 | Module Detail | 4:3 | Residual block with InstanceNorm and PatchGAN receptive-field stack | strong |
| 4 | Data Behavior | 4:3 | Real A/B vs translated and reconstructed sample grids across epochs | strong |

## Priority summary

- Must: Overall Framework and Network Architecture when listed.
- Strong: module mechanism and behavior/comparison figures supported by code evidence.
- Nice: none added without manuscript evidence.

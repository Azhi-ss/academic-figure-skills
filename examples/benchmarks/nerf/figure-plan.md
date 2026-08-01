> Benchmark golden — derived from bmild/nerf @ 14c55567 (license: MIT).
> URL: https://github.com/bmild/nerf.git
> Pinned commit: 14c55567
> License: MIT

# Figure Plan

## Paper overview

- Topic: bmild/nerf repository architecture and volume-rendering pipeline for novel view synthesis.
- Contribution focus: positional-encoded MLP (coarse + fine) with hierarchical ray sampling and alpha-compositing.
- module_count_framework: 4
- palette: classic academic; venue: None; domain: CV

## Completeness

This system-centric plan is grounded in the pinned repository snapshot. Paper narrative, claims, and experimental priorities require separate manuscript review.

## Per-section recommendations

| # | figure type | aspect_ratio | must-appear elements / rationale | priority |
|---|---|---|---|---|
| 1 | Overall Framework | 16:9 | Camera pose, ray generation, coarse MLP, PDF sampling, fine MLP, volume integration, rendered image | must |
| 2 | Network Architecture | 16:9 | Positional encoding, 8-layer MLP with skip at layer 4, RGB/density heads | must |
| 3 | Module Detail | 4:3 | Hierarchical sampling with sample_pdf and alpha-compositing accumulation | strong |
| 4 | Data Behavior | 4:3 | Training PSNR curve or novel-view renderings across poses | strong |

## Priority summary

- Must: Overall Framework and Network Architecture when listed.
- Strong: module mechanism and behavior/comparison figures supported by code evidence.
- Nice: none added without manuscript evidence.

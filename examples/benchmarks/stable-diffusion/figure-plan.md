> Benchmark golden — derived from CompVis/stable-diffusion @ 21f890f9 (license: CreativeML Open RAIL-M).
> URL: https://github.com/CompVis/stable-diffusion.git
> Pinned commit: 21f890f9
> License: CreativeML Open RAIL-M

# Figure Plan

## Paper overview

- Topic: CompVis/stable-diffusion repository architecture and executable research workflow.
- Contribution focus: evidence-backed modules and dataflow from the Quick Understanding Doc.
- module_count_framework: 4
- palette: classic academic; venue: None; domain: Generative

## Completeness

This system-centric plan is grounded in the pinned repository snapshot. Paper narrative, claims, and experimental priorities require separate manuscript review.

## Per-section recommendations

| # | figure type | aspect_ratio | must-appear elements / rationale | priority |
|---|---|---|---|---|
| 1 | Overall Framework | 16:9 | Prompt, frozen CLIP, latent diffusion, VAE decode and image output | must |
| 2 | Network Architecture | 16:9 | U-Net down/middle/up path, skip links and cross-attention | must |
| 3 | Module Detail | 4:3 | Classifier-free guidance and DDIM/PLMS update | strong |
| 4 | Data Behavior | 4:3 | Guidance-scale or sampling-step image grid | strong |

## Priority summary

- Must: Overall Framework and Network Architecture when listed.
- Strong: module mechanism and behavior/comparison figures supported by code evidence.
- Nice: none added without manuscript evidence.

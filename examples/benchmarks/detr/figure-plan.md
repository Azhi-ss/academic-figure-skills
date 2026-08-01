> Benchmark golden — derived from facebookresearch/detr @ 29901c51 (license: Apache-2.0).
> URL: https://github.com/facebookresearch/detr.git
> Pinned commit: 29901c51
> License: Apache-2.0

# Figure Plan

## Paper overview

- Topic: facebookresearch/detr repository architecture for end-to-end set-based object detection.
- Contribution focus: CNN + Transformer with object queries and Hungarian-matching set prediction loss.
- module_count_framework: 4
- palette: classic academic; venue: None; domain: CV

## Completeness

This system-centric plan is grounded in the pinned repository snapshot. Paper narrative, claims, and experimental priorities require separate manuscript review.

## Per-section recommendations

| # | figure type | aspect_ratio | must-appear elements / rationale | priority |
|---|---|---|---|---|
| 1 | Overall Framework | 16:9 | Image, CNN backbone, Transformer encoder/decoder, object queries, prediction heads, Hungarian matcher, set loss | must |
| 2 | Network Architecture | 16:9 | ResNet backbone + sine positional encoding + Transformer encoder/decoder + class and box FFN heads | must |
| 3 | Module Detail | 4:3 | Hungarian matching cost matrix and L1 + GIoU + classification set loss | strong |
| 4 | Data Behavior | 4:3 | Training loss and COCO mAP curves or query-to-object visualization | strong |

## Priority summary

- Must: Overall Framework and Network Architecture when listed.
- Strong: module mechanism and behavior/comparison figures supported by code evidence.
- Nice: none added without manuscript evidence.

# Luna — Multiframe Merge Proposal v1

**Phase**：`Phase-Multiframe-Merge-Proposal-v1-001`

## 目的

基于 Source Validation v2 after EP v3 的 **same-frame / same-region blocker**，生成跨帧 merge **规划**（proposal），说明未来如何获得 multiframe evidence。**不是** multiframe evidence，**不是**事实层。

## 边界

- 不抽新帧、不解码视频、不运行 OCR、不生成 crop / OCRRequest / EP / Semantic
- 不执行 Source Validation rerun、不进入 review approval、不写 WorldModel / Scene Delta
- same-frame blocker **不得**在本阶段解除；`fact_status=not_fact`，`write_allowed=false`

## 实现

- `capabilities/midplatform/multiframe_merge_proposal_v1.py`
- `tools/evaluation/midplatform/run_multiframe_merge_proposal_v1.py`
- `tools/evaluation/midplatform/verify_multiframe_merge_proposal_v1.py`

## 前置

- [LUNA_SOURCE_VALIDATION_V2_AFTER_EP_V3.md](./LUNA_SOURCE_VALIDATION_V2_AFTER_EP_V3.md)

## 评测

[LUNA_EVALUATION_MULTIFRAME_MERGE_PROPOSAL_V1.md](../evaluation/LUNA_EVALUATION_MULTIFRAME_MERGE_PROPOSAL_V1.md)

## 建议下一 phase

- [LUNA_BETTER_FRAME_EXTRACTION_DRYRUN_V1.md](./LUNA_BETTER_FRAME_EXTRACTION_DRYRUN_V1.md)（`Better-Frame-Extraction-DryRun-v1-001`）
- `Text-Region-Tracklet-DryRun-v1`
- `Multiframe-Crop-Execution-DryRun-v1`

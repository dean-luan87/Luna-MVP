# Luna — Better Frame Extraction DryRun v1

**Phase**：`Phase-Better-Frame-Extraction-DryRun-v1-001`

## 目的

基于 Multiframe Merge Proposal 的 target frame window，在已知视频路径与规划 offsets 内 **materialize** better frame candidate references / frame artifacts。**不是** OCR evidence，**不是** multiframe consensus 完成层。

## 边界

- 允许 `known_index_frame_materialization`（cv2 POS_FRAMES）；禁止 video scan / 新帧发现
- 不运行 OCR、不生成 crop / OCRRequest / EP / Semantic、不 SV rerun
- same-frame blocker **不得**解除；`fact_status=not_fact`

## 实现

- `capabilities/midplatform/better_frame_extraction_dryrun_v1.py`
- `tools/evaluation/midplatform/run_better_frame_extraction_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_better_frame_extraction_dryrun_v1.py`

## 前置

- [LUNA_MULTIFRAME_MERGE_PROPOSAL_V1.md](./LUNA_MULTIFRAME_MERGE_PROPOSAL_V1.md)

## 评测

[LUNA_EVALUATION_BETTER_FRAME_EXTRACTION_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_BETTER_FRAME_EXTRACTION_DRYRUN_V1.md)

## 建议下一 phase

- [LUNA_TEXT_REGION_TRACKLET_DRYRUN_V1.md](./LUNA_TEXT_REGION_TRACKLET_DRYRUN_V1.md)（`Text-Region-Tracklet-DryRun-v1-001`）— 已完成
- `Multiframe-Crop-Execution-DryRun-v1` — **OCR/multiframe 主线已暂停**；恢复前勿接主 runtime

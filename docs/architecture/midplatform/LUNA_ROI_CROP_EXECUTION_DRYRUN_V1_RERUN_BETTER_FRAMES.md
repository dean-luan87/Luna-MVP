# Luna — ROI Crop Execution DryRun v1 Rerun With Better Frames

**Phase**：`Phase-ROI-Crop-Execution-DryRun-v1-Rerun-With-Better-Frames-001`

## 目的

消费 Better Frame Selection 中 **12** 个 `selected_candidate` + `existing_scan_frame`（ready_later），使用候选帧 linebox bbox 重新执行 ROI crop dry-run。

## 边界

- 仅 rerun ready_later 分支；`future_detector_required`×8、`multiframe_required`×7 进入 deferred report
- 不解码新视频、不抽新帧；不 OCR、不 OCRRequest、不写事实

## 实现

- `capabilities/midplatform/roi_crop_execution_dryrun_v1_rerun_better_frames.py`
- `tools/evaluation/midplatform/run_roi_crop_execution_dryrun_v1_rerun_better_frames.py`
- `tools/evaluation/midplatform/verify_roi_crop_execution_dryrun_v1_rerun_better_frames.py`

## 前置

- [LUNA_BETTER_FRAME_SELECTION_RUNTIME_V1.md](./LUNA_BETTER_FRAME_SELECTION_RUNTIME_V1.md)
- [LUNA_ROI_CROP_EXECUTION_DRYRUN_V1.md](./LUNA_ROI_CROP_EXECUTION_DRYRUN_V1.md)

## 评测

[LUNA_EVALUATION_ROI_CROP_EXECUTION_DRYRUN_V1_RERUN_BETTER_FRAMES.md](../evaluation/LUNA_EVALUATION_ROI_CROP_EXECUTION_DRYRUN_V1_RERUN_BETTER_FRAMES.md)

## 建议下一 phase

- [LUNA_ROI_TO_OCRREQUEST_REFERENCE_V1.md](./LUNA_ROI_TO_OCRREQUEST_REFERENCE_V1.md)（已完成 smoke：12 reference）
- `OCRRequest-Gated-Submission-from-ROI-v1`

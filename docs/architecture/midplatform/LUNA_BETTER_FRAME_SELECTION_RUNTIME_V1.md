# Luna — Better Frame Selection Runtime v1

**Phase**：`Phase-Better-Frame-Selection-Runtime-v1-001`

## 目的

在 ROI Crop 全部 defer 后，基于已有 scan / linebox / source quality / frame refs 做 **better frame selection planning**：

- 生成 `better_frame_candidate`（非 evidence、非 crop artifact、非事实）
- 不解码新视频、不抽新帧、不 crop、不 OCR

## 边界

- `selection_planning_only=true`
- SQ_E 不得标 crop-ready；null bbox 不得伪造

## 实现

- `capabilities/midplatform/better_frame_selection_runtime_v1.py`
- `tools/evaluation/midplatform/run_better_frame_selection_runtime_v1.py`
- `tools/evaluation/midplatform/verify_better_frame_selection_runtime_v1.py`

## 前置

- [LUNA_ROI_CROP_EXECUTION_DRYRUN_V1.md](./LUNA_ROI_CROP_EXECUTION_DRYRUN_V1.md)
- [LUNA_ROI_RETRY_PROPOSAL_RUNTIME_V1.md](./LUNA_ROI_RETRY_PROPOSAL_RUNTIME_V1.md)

## 评测

[LUNA_EVALUATION_BETTER_FRAME_SELECTION_RUNTIME_V1.md](../evaluation/LUNA_EVALUATION_BETTER_FRAME_SELECTION_RUNTIME_V1.md)

## 后续

- [LUNA_ROI_CROP_EXECUTION_DRYRUN_V1_RERUN_BETTER_FRAMES.md](./LUNA_ROI_CROP_EXECUTION_DRYRUN_V1_RERUN_BETTER_FRAMES.md)

## 建议下一 phase

- `ROI-to-OCRRequest-Reference-v1`

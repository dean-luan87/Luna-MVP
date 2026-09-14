# Luna — ROI Crop Execution DryRun v1

**Phase**：`Phase-ROI-Crop-Execution-DryRun-v1-001`

## 目的

消费 ROI Retry Proposal Runtime v1 的 proposal，生成 **crop dry-run artifact**（含 metadata；有合法 bbox 且 policy 允许时可写 PNG）：

- bbox 缺失 / `better_frame_required` / SQ_E → **deferred**
- 不运行 OCR、不生成 OCRRequest、不写事实层

## 边界

- crop artifact **不是** OCR evidence，**不是**事实
- 仅为下一阶段 `ROI-to-OCRRequest-Reference-v1` 准备输入

## 实现

- `capabilities/midplatform/roi_crop_execution_dryrun_v1.py`
- `tools/evaluation/midplatform/run_roi_crop_execution_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_roi_crop_execution_dryrun_v1.py`

## 前置

- [LUNA_ROI_RETRY_PROPOSAL_RUNTIME_V1.md](./LUNA_ROI_RETRY_PROPOSAL_RUNTIME_V1.md)

## 评测

[LUNA_EVALUATION_ROI_CROP_EXECUTION_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_ROI_CROP_EXECUTION_DRYRUN_V1.md)

## 后续

- [LUNA_BETTER_FRAME_SELECTION_RUNTIME_V1.md](./LUNA_BETTER_FRAME_SELECTION_RUNTIME_V1.md)

## 建议下一 phase

- `Better-Frame-Extraction-DryRun-v1` 或 `ROI-Crop-Execution-DryRun-v1-rerun`

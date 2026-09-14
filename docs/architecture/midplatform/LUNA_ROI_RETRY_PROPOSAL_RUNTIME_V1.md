# Luna — ROI Retry Proposal Runtime v1

**Phase**：`Phase-ROI-Retry-Proposal-Runtime-v1-001`

## 目的

消费 Source Validation v1 中 `require_roi_retry` 分支（及 scan hint / review queue roi_retry_queue），生成 **ROI retry proposal**：

- 输出候选 ROI 类型、重试原因、推荐裁剪策略、来源链、优先级与下一步计划
- **只生成 proposal**，不执行真实裁剪、不运行 OCR、不调用 provider

## 边界

- 不执行 ROI crop；不生成 `OCRRequest`；不调用 RapidOCR / PaddleOCR / Vision provider
- 不生成 Evidence Pack / Semantic Candidate；不写 fact / WorldModel / Scene Delta
- 不自动批准；不改 runtime routing；不做 benchmark / provider 比较

## 实现

- `capabilities/midplatform/roi_retry_proposal_runtime_v1.py`
- `tools/evaluation/midplatform/run_roi_retry_proposal_runtime_v1.py`
- `tools/evaluation/midplatform/verify_roi_retry_proposal_runtime_v1.py`

## 前置

- [LUNA_OCR_SOURCE_VALIDATION_DRYRUN_V1.md](./LUNA_OCR_SOURCE_VALIDATION_DRYRUN_V1.md)
- [LUNA_OCR_REVIEW_QUEUE_RUNTIME_DRYRUN_V1.md](./LUNA_OCR_REVIEW_QUEUE_RUNTIME_DRYRUN_V1.md)
- [LUNA_MIXEDVIDEO_OCR_SCAN_LINEBOX_TRACE_SOURCE_QUALITY_GATE_V0.md](./LUNA_MIXEDVIDEO_OCR_SCAN_LINEBOX_TRACE_SOURCE_QUALITY_GATE_V0.md)

## 评测

[LUNA_EVALUATION_ROI_RETRY_PROPOSAL_RUNTIME_V1.md](../evaluation/LUNA_EVALUATION_ROI_RETRY_PROPOSAL_RUNTIME_V1.md)

## 后续

- [LUNA_ROI_CROP_EXECUTION_DRYRUN_V1.md](./LUNA_ROI_CROP_EXECUTION_DRYRUN_V1.md)

## 建议下一 phase

- `ROI-to-OCRRequest-Reference-v1`
- `VisualSymbolRegistry-DryRun`（7 项 visual route）

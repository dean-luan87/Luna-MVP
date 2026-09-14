# Luna — OCR Source Validation DryRun v1

**Phase**：`Phase-OCR-Source-Validation-DryRun-v1-001`

## 目的

对 TTL Gate / Review Policy / Semantic v1 各分支做 **来源链完整性** 与 **可靠性** dry-run 规划：

- gated OCR、TTL hold、scan hint、visual route、SQ_E blocked、unresolved later
- `validation_satisfied=false`；`source_validation_passed_count=0`

## 边界

不查真实 registry/地图/人工审核；不批准、不写 fact/WM/Scene Delta

## 实现

- `capabilities/midplatform/ocr_source_validation_dryrun_v1.py`
- `tools/evaluation/midplatform/run_ocr_source_validation_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_ocr_source_validation_dryrun_v1.py`

## 前置

- [LUNA_OCR_TTL_GATE_V1.md](./LUNA_OCR_TTL_GATE_V1.md)
- [LUNA_OCR_REVIEW_QUEUE_RUNTIME_DRYRUN_V1.md](./LUNA_OCR_REVIEW_QUEUE_RUNTIME_DRYRUN_V1.md)

## 评测

[LUNA_EVALUATION_OCR_SOURCE_VALIDATION_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_OCR_SOURCE_VALIDATION_DRYRUN_V1.md)

## 后续

- [LUNA_ROI_RETRY_PROPOSAL_RUNTIME_V1.md](./LUNA_ROI_RETRY_PROPOSAL_RUNTIME_V1.md)（`require_roi_retry` → ROI proposal only）

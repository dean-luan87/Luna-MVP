# Luna — Source Validation v2 after EP v3

**Phase**：`Phase-Source-Validation-v2-after-EP-v3-001`

## 目的

对 Semantic Candidate v3 / Evidence Pack v3 做 **Source Validation v2 dry-run**：评估是否具备来源验证条件，**不是**验证通过阶段。预期 `source_validation_passed_count=0`，以 pending/blocked 为主。

## 边界

- 不运行 OCR、不调用 LLM/VLM、地图/POI、VisualSymbolRegistry、真实 multiframe/repeated observation
- same-frame / strategy-repeat / noisy segment 必须阻断实体确认与事实验证
- source chain complete 仅允许进入 validation review，≠ validation passed

## 实现

- `capabilities/midplatform/source_validation_v2_after_ep_v3.py`
- `tools/evaluation/midplatform/run_source_validation_v2_after_ep_v3.py`
- `tools/evaluation/midplatform/verify_source_validation_v2_after_ep_v3.py`

## 前置

- [LUNA_SEMANTIC_CANDIDATE_V3_BBOX_EXPANSION_AWARE.md](./LUNA_SEMANTIC_CANDIDATE_V3_BBOX_EXPANSION_AWARE.md)

## 评测

[LUNA_EVALUATION_SOURCE_VALIDATION_V2_AFTER_EP_V3.md](../evaluation/LUNA_EVALUATION_SOURCE_VALIDATION_V2_AFTER_EP_V3.md)

## 建议下一 phase

- [LUNA_MULTIFRAME_MERGE_PROPOSAL_V1.md](./LUNA_MULTIFRAME_MERGE_PROPOSAL_V1.md)（`Multiframe-Merge-Proposal-v1-001`）
- `Better-Frame-Extraction-DryRun-v1`（multiframe proposal 之后）
- `Semantic-Candidate-v3-Review-Policy`（需 multiframe evidence 之后）
- `Source-Validation-v2-Rerun-after-External-Support`

# Luna — GO / NO_GO: CrossModal Vision OCR Reference Only v0

## GO

- `matched_reference_count > 0`，按 `frame_id + roi_id` 对齐。
- `reference_scope=reference_only`，`fusion_status=not_fused`，`fact_status=not_fact`。
- `forbidden_actions` 齐全；audit 无越界；verifier = **GO**。

## CONDITIONAL_GO

- 部分 ROI 未匹配但 `unmatched_vision_roi_rows` 完整；无越界。

## NO_GO

- 融合结论、文本解释、事实写入、导航、AI、真实 provider 调用；audit 缺失。

# Luna — GO / NO_GO: Vision-triggered OCR Evidence ReadOnly Consumer v0

## GO

- 只读消费 Vision-triggered OCR submission collection。
- `evidence_by_candidate` / `evidence_by_frame` / `evidence_by_roi` 非空。
- `fusion_status=not_fused`，`fact_status=not_fact`，无事实写入、无融合、无导航。
- verifier = **GO**。

## CONDITIONAL_GO

- 部分 submission 失败但 matrix / error 完整；无越界。

## NO_GO

- 做 Vision+OCR 融合或解释文本。
- 写事实层 / Scene Delta / WorldModel / 导航。
- 调用真实 OCR provider；audit 缺失。

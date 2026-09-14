# Luna Evaluation — OCR Mainline Minimal Bridge Smoke GO / NO_GO Pack v0

## GO

- `status=success`；`ocr_evidence` 与 `bridge_pack`（`ocr_evidence_pack_candidate_v0`）齐全。  
- `audit` 中 `paddleocr_invoked`、`rapidocr_replaced`、`ocr_routing_changed`、`midplatform_invoked`、`world_model_written` 均为 **false**。  
- `request_id` / `trace_id` 存在；`input_gate` 非空。  
- 若 `oversized` 且 `allow_full_image=false`，则 `recommended_input_strategy` **不得**为 `full_image_allowed`。  
- Verifier **GO**。

## CONDITIONAL_GO

- `status=rejected`（例如故意用大图测 gate）但 request / gate / audit 记录完整且无越界。  
- 或 bridge pack 字段不完整但可定位原因（仅评测用途）。

## NO_GO

- 任一 audit 禁止项为 **true**。  
- 调用真实 Paddle / 改 routing / 进入 MidPlatform / 写 WorldModel。  
- 缺失 `request_id` / `trace_id` / `audit`。  
- oversized 且未允许 full image 却标记为 `full_image_allowed`。

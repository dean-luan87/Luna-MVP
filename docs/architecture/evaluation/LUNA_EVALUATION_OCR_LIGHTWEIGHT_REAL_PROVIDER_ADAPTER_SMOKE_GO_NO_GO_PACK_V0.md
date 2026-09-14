# OCR Lightweight Real Provider Adapter Smoke — GO / CONDITIONAL_GO / NO_GO Pack v0

**Phase**: `Phase-OCR-Lightweight-Real-Provider-Adapter-001`

## GO

- **Case A**：`status=success`，`selected_provider=ocr_stub`，Paddle runtime flag 为 false。  
- **Case B**：`status=success`，`bridge_pack` 合法；若 `real_provider_invoked=true` 则 `selected_provider=rapidocr_candidate` 且 `provider_result.real_provider_invoked=true`；若为 stub 回退，则 `provider_selection_reason_codes` 含 **unavailable / import / input_reject** 等可解释原因（**不得**无原因静默冒充成功）。  
- **Case C**：强制 unavailable 后仍为 **success + stub**，`real_provider_invoked=false`，reason 含 `provider_runtime_unavailable`。  
- **Case D**：`real_provider_invoked=false`，且（reason 含 `edge_exceeds_lightweight_cap` **或** `status=rejected`）。  
- 禁止项：`paddleocr_invoked`、`rapidocr_replaced`、`ocr_routing_changed`、`midplatform_invoked`、`world_model_written` 均不得为 true。  
- Verifier：`verdict=GO`，`blockers=[]`。

## CONDITIONAL_GO

- 本机 **未安装** RapidOCR 依赖：Case B 稳定走 **stub + unavailable/import 原因**，其余用例仍满足；文档注明「依赖可选」。

## NO_GO

- Paddle runtime candidate **enabled**，或 `paddleocr_invoked=true`。  
- 无 flag 却 `real_provider_invoked=true`。  
- 超大原图尺寸 **未经拒绝**却 `real_provider_invoked=true`。  
- Case C/D 约束失败；缺少 audit / selection report；伪造成功（unavailable 却宣称真实 OCR 成功）。

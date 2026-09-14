# OCR Lightweight Provider Text Smoke — GO / CONDITIONAL_GO / NO_GO Pack v0

**Phase**: `Phase-OCR-Lightweight-Provider-Text-Smoke-001`

## GO

- 输入图存在且 **宽高均 ≤512**（本 smoke 默认）。  
- `selected_provider=rapidocr_candidate` 且 `real_provider_invoked=true`。  
- `status=success`；`text_joined` **非空**；`text_items` **≥1**。  
- `bridge_pack` 合法，`provider_trace.provider=rapidocr_candidate`。  
- 禁止项：`paddleocr_invoked`、`rapidocr_replaced`、`ocr_routing_changed`、`midplatform_invoked`、`world_model_written` 均为 **非 true**。  
- Verifier：`verdict=GO`，`blockers=[]`。

## CONDITIONAL_GO

- `selected_provider=ocr_stub`，`real_provider_invoked=false`，且 selection reason 含 **unavailable / import / engine_init / lightweight reject** 等可解释 token；**未**伪造非空 Rapid 结果。  
- Verifier：`verdict=CONDITIONAL_GO`；退出码 **0**。

## NO_GO

- Rapid 被选中但 **text 为空** 或 **无 text_items**（链路异常或假成功）。  
- Rapid 选中但 `real_provider_invoked=false`。  
- Paddle 被调用或禁止 audit 为 true。  
- 输入图超过 512 边长仍跑本 smoke。  
- 缺关键产物或 audit 缺失。

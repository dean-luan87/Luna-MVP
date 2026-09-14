# OCR Provider Selection Smoke — GO / CONDITIONAL_GO / NO_GO Pack v0

**Phase**: `Phase-OCR-Real-Provider-Adapter-Selection-001`

## GO

- Registry 快照存在且包含 **`ocr_stub`（enabled）** 与 **`rapidocr_candidate` / `paddleocr_candidate`（disabled）**。
- **Case A**: `status=success`，`selected_provider=ocr_stub`，存在 `provider_selection_report`，禁止类 audit 字段全为 **非 true**。
- **Case B**: `status=success`，`audit.fallback_to_stub=true`，`real_provider_invoked` 仍为 false。
- **Case C**: `status=error`，`error=misconfiguration_paddle_runtime_without_real_provider`，`audit.paddleocr_runtime_provider_enabled=true`，且 **`paddleocr_invoked` 等禁止项仍为 false**（未调用真实引擎）。
- Verifier 输出 `verdict=GO`，`blockers=[]`。

## CONDITIONAL_GO

- Registry 或 selection 报告字段有小幅演进，但 **语义不变**（仍仅 stub 可执行、真实候选默认 disabled），且 verifier 已同步更新。

## NO_GO

- 任一用例出现 **`real_provider_invoked` / `paddleocr_invoked` / `rapidocr_replaced` / `ocr_routing_changed` / `midplatform_invoked` / `world_model_written`** 为 true。
- 默认 registry 误将 **paddle/rapid 候选标为 enabled**。
- Case A 非 success，或 Case C 未按误配置拒绝。
- 缺少 `provider_selection_report` 或缺少 registry 快照产物。

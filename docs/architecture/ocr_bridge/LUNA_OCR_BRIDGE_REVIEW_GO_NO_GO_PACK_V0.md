# LUNA OCR Bridge — Review Go/No-Go Pack v0 (Phase-OCRBridge-Review-001)

## GO

- `LUNA_OCR_MIDPLATFORM_INTERFACE_FREEZE_V0.md` 等评审冻结文档已落地。
- 最小必填字段、事实层准入、`forwarding_mode` 判定、未来 runtime refs 已在文档与矩阵产物中写明。
- `review_ocr_bridge_interface_freeze_v0.py` 生成完整 review 产物，`verify_ocr_bridge_interface_freeze_v0.py` verdict **GO**。
- 示例 pack 的 `hard_audit` 清洁：`midplatform_invoked=false`、`runtime_integration=false`、`whitebox_integration=false`、`mainline_routing_changed=false`。

## CONDITIONAL_GO

- 示例 `source_*_ref` 仍为 **`eval:*`**；实现阶段再绑定真实引用。
- `forwarding_mode` 在示例数据上多为 **`conditional_evidence`**（保守），不宣称生产已达成 `eligible_text_only`。

## NO_GO

- 文档或工具暗示 **MidPlatform 可直接接收 `raw_text_joined`**。
- 允许 **non-OCR / symbol / glyph / layout / conditional** 写入事实文本层且无候选守卫。
- 将 **`eval:`** 占位 **伪装** 为生产 `trace_ref` / `replay_ref`。
- 工具链调用 **MidPlatform / SceneDelta / WorldContext**，或修改主线 OCR routing / 接 runtime。

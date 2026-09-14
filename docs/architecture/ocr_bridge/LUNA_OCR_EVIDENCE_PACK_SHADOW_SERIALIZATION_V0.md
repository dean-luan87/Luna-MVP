# LUNA OCR Bridge — OcrEvidencePack Shadow Serialization v0（Phase-OCRBridge-Implementation-001）

## 目的

在 **不接 MidPlatform**、**不调 OCR provider**、**不改变主线 routing** 的前提下，将 OCR-007 routing pack + Evaluation 边界产物 **序列化为** `OcrEvidencePackV0` 的 **shadow JSON**，并生成 **trace / replay / audit** 行与 **forwarding 阻断报告**。

## 边界（硬）

- **仅** `eval:` / `shadow:` / `offline_trial:` 类 source ref；**禁止伪造** `runtime:`、`production:`、`midplatform:`、`scene_delta:`、`world_context:` 前缀。  
- **不**把 shadow pack 当 runtime 事实输入；**不**开启 fact text layer；**不**自动转发中台。  
- 工具：`tools/ocr_bridge/run_ocr_evidence_pack_shadow_serialization_v0.py`、`tools/ocr_bridge/verify_ocr_evidence_pack_shadow_serialization_v0.py`。  
- 实现模块：`capabilities/ocr_bridge/ocr_evidence_pack_shadow_serializer_v0.py`。

## 产物

见 `~/LunaRuntime/logs/ocr_bridge_shadow_serialization_001_*` 下的 `ocr_evidence_pack_shadow.json`（`shadow_envelope` + `pack`）、`ocr_evidence_pack_shadow_*_report.json` 与 `ocr_bridge_shadow_*.jsonl`。

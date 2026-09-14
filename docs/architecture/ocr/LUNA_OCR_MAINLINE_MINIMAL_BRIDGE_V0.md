# Luna OCR Mainline Minimal Bridge v0

**Phase**: `Phase-OCR-Mainline-Minimal-Bridge-001`  
**目标**: 打通 **OCRRequest → ImageInputGate（最小）→ STCM deadline 占位 → stub provider → 最小 evidence → bridge pack candidate → audit** 的可观测骨架；**不**追求完整生产能力。

## 边界（必须）

- **不**把 PaddleOCR 设为默认 provider；**不**把评测 provider 直接升格为生产 provider。  
- **不**替换 RapidOCR；**不**改变现有 OCR routing。  
- **不**绕过 OCR Bridge 语义（本阶段输出 **pack candidate**）；**不**进入 MidPlatform 语义解释；**不**写 WorldModel。  
- **不**对大图做整图实时 OCR；stub **不**调用真实 OCR。  
- 环境开关：`LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0`（默认 `false`）、`LUNA_ENABLE_OCR_STUB_PROVIDER_V0`（默认 `true`）、`LUNA_ENABLE_OCR_REAL_PROVIDER_V0` / `LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0` / `LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0`（默认 `false`）。未开 bridge 时入口必须拒绝。  
- **误配置**：`LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0=true` 且 `LUNA_ENABLE_OCR_REAL_PROVIDER_V0=false` 时，主线在 **校验请求后** 直接 `error` 返回（不跑 gate / normalization / stub），详见 [LUNA_OCR_RUNTIME_PROVIDER_ADAPTER_SELECTION_V0.md](./LUNA_OCR_RUNTIME_PROVIDER_ADAPTER_SELECTION_V0.md)。

## 代码位置

- `capabilities/ocr_runtime/ocr_request_contract_v0.py` — `OCRRequestV0`  
- `capabilities/ocr_runtime/ocr_image_input_gate_v0.py` — 元数据 + 像素预算  
- `capabilities/ocr_runtime/ocr_provider_stub_v0.py` — stub  
- `capabilities/ocr_runtime/ocr_mainline_bridge_v0.py` — 编排（含 provider selection；见 Adapter Selection 文档）  
- `tools/evaluation/ocr/run_ocr_mainline_bridge_smoke_v0.py` — 小图 ALLOW + stub smoke  
- `tools/evaluation/ocr/verify_ocr_mainline_bridge_smoke_v0.py` — 校验上述 smoke  
- `tools/evaluation/ocr/run_ocr_mainline_bridge_reject_smoke_v0.py` — **超限图 REJECT** smoke（生成大图 PNG）  
- `tools/evaluation/ocr/verify_ocr_mainline_bridge_reject_smoke_v0.py` — 校验 REJECT 路径  

## 与前置规范的关系

输入预算读取 `configs/ocr/ocr_image_input_governance_v0.example.json`；与 **OCR Input Size Governance** 文档一致，后续可逐步把 downscale/tiling 实装入 Gate（本阶段不做）。

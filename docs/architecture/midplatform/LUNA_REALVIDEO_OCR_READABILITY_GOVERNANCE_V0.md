# Luna — RealVideo OCR Readability Governance v0

**Phase**：`Phase-RealVideo-OCR-Readability-Governance-001`

## 目的

定义 RealVideo OCR **可读性治理**：ROI 质量分级（A–E）、遮挡/角度/模糊/压缩等风险因子、partial evidence、OCR enhancement 边界、VisualSymbol fallback、PublicFacility semantic-first、多帧恢复策略。

**不读视频、不跑 OCR、不修改 OCR 原始输出、不写事实层。**

## 核心原则

- OCR 是视觉治理后的执行器，不是独立事实源
- `raw_ocr_text` 必须保留；enhancement 仅产出 candidate
- 遮挡/残缺 → partial evidence；Logo/GAP → VisualSymbolEvidence
- 公共设施 → semantic-first（继承 PublicFacility dry-run）

## 实现

- Capability：`capabilities/midplatform/realvideo_ocr_readability_governance_v0.py`
- Runner：`tools/evaluation/midplatform/run_realvideo_ocr_readability_governance_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_realvideo_ocr_readability_governance_v0.py`

## 评测

[LUNA_EVALUATION_REALVIDEO_OCR_READABILITY_GOVERNANCE_V0.md](../evaluation/LUNA_EVALUATION_REALVIDEO_OCR_READABILITY_GOVERNANCE_V0.md)

## 建议下一跳

**Readability score stub** 或 **Text-Bearing FrameSample Smoke**（带 readability 标签，且 gate 消费 grade）。

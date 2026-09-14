# Luna — OCR Poster Layout Segmentation Governance v0

**Phase**：`Phase-OCR-Poster-Layout-Segmentation-Governance-001`

## 目的

建立海报/公告/广告类图文的**输入治理与版面分区候选**（governance-only stub）。默认 `full_image_ocr_allowed=false`，策略 `segment_first`。

## 并列治理线

**公共设施**（semantic_first，OCR 辅助）见 [LUNA_PUBLIC_FACILITY_SEMANTIC_CORRECTION_GOVERNANCE_V0.md](../midplatform/LUNA_PUBLIC_FACILITY_SEMANTIC_CORRECTION_GOVERNANCE_V0.md)。

## 原则

- 不运行 RapidOCR / PaddleOCR / Vision provider / VLM
- 不写事实层 / Scene Delta / WorldModel
- Logo / QR / 商品装饰区不进入普通 OCR 文本链
- VisualSymbolEvidence 与 OCR TextEvidence 分流

## 产物

Synthetic poster fixture + layout/text/non-text/visual-symbol 候选 + `ocr_region_plan` + reading order stub + risk/gate/audit。

## 评测

[LUNA_EVALUATION_OCR_POSTER_LAYOUT_SEGMENTATION_GOVERNANCE_V0.md](../evaluation/LUNA_EVALUATION_OCR_POSTER_LAYOUT_SEGMENTATION_GOVERNANCE_V0.md)

## 建议下一跳

**Phase-OCR-Poster-Region-OCR-Plan-Stub-001** — 见 [LUNA_OCR_POSTER_REGION_OCR_PLAN_STUB_V0.md](./LUNA_OCR_POSTER_REGION_OCR_PLAN_STUB_V0.md)

## 建议下一跳（Region Plan GO 后）

**Phase-OCR-Poster-VisualSymbolEvidence-Stub-001**

# LUNA Evaluation Tools — OCR Validation Framework v0 (Phase-EvaluationTools-Foundation-001)

## Layered architecture (6 layers)

### Layer 1 — Dataset Quality Gate

- 字体可见性（中文 tofu / fallback）
- ground truth 一致性（manifest vs gt 文件）
- 图片有效性（尺寸/sha256/可读性）
- 样本分类与 manifest 完整性

### Layer 2 — Character Recognition Evaluation

- CER / WER
- 中文召回
- 空串率
- 乱码率
- 数字/符号错误率

### Layer 3 — Layout / Reading Order Evaluation

- bbox coverage
- reading order accuracy
- group-level text consistency
- 多列/多行/竖排等结构样本支持（预留）

### Layer 4 — Symbol / Glyph Evaluation

- 图标误识别率
- 边框/斜杠/装饰线误识别率
- 艺术字/异形数字漏检率
- visual_symbol / visual_glyph 归类正确性（预留）

### Layer 5 — Provider A/B Evaluation

- RapidOCR / PaddleOCR / CnOCR / future OCR-VL
- 同样本、同指标、同报告 schema
- 允许多 provider 对照，但不得自动影响主线决策

### Layer 6 — Stress / Regression Evaluation

- 批量样本压力（吞吐/延迟/失败率）
- 长时间运行（内存/稳定性）
- 低质量输入（噪声/模糊/倾斜/低对比）
- failure case replay（预留）

## Report schema

所有评测输出应映射到统一 `EvaluationReportV0`（见 `LUNA_EVALUATION_REPORT_SCHEMA_V0.md`）。


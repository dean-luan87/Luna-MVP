# LUNA Evaluation Tools — OCR Capability Boundary Test Matrix v0 (Phase-EvaluationTools-OCR-006)

## Goal

建立 **OCR Capability Boundary Map**（evaluation-only），回答：

- 哪类内容适合 RapidOCR（稳定/弱/不可用）
- 哪类内容应转交 PaddleOCR/CnOCR/OCR-VL（候选）或 layout/symbol/glyph 分支
- 哪类内容应被前置过滤为 low_quality/unreadable/manual_review
- 输入质量扰动（字太小/模糊/低对比/倾斜/压缩）对成功率的影响

> 本阶段结果 **不得自动改变** 主线 provider 选择或 routing，只能供人工评审参考。

## Core acceptance principle

- OCR 不负责识别一切视觉内容。
- OCR 只负责识别经过 **输入质量门控、内容类型门控、版面归属门控** 后，适合 OCR 的文字证据。
- **OCR 的失败可以接受；OCR 的错误自信不可接受。**

## Hard boundaries

- Evaluation Tools only；不接入 runtime / whitebox
- 不进入 MidPlatform / SceneDelta / WorldContextEvidence / semantic / 语音链路
- 不做 PaddleOCR provider trial（v0 eval 仅 rapidocr）

## Taxonomy

- 内容类型：见 `LUNA_EVALUATION_OCR_CONTENT_TYPE_TAXONOMY_V0.md`
- 质量扰动：见 `LUNA_EVALUATION_OCR_QUALITY_PERTURBATION_MATRIX_V0.md`
- 路由草案：见 `LUNA_EVALUATION_OCR_PROVIDER_ROUTING_POLICY_DRAFT_V0.md`

## Tools

- 生成：`tools/evaluation/ocr/generate_ocr_capability_boundary_cases_v0.py`
- 数据集 verifier：`tools/evaluation/ocr/verify_ocr_capability_boundary_dataset_v0.py`
- 评测（RapidOCR）：`tools/evaluation/ocr/evaluate_ocr_capability_boundary_v0.py`
- 评测 verifier：`tools/evaluation/ocr/verify_ocr_capability_boundary_eval_v0.py`

## Key metrics (v0)

- **False Text Risk**：非适用域（non-ocr）内容被 OCR 输出为非空文本的风险（应尽量接近 0；否则必须分流/拦截，防信息失真）。
- **Eligibility Accuracy（proxy）**：expected routing/eligibility 与实际“是否输出文本/是否高误差”的一致度（v0 为 proxy；后续主线 router 才能给真正 accuracy）。


# LUNA Evaluation Tools — OCR Chinese Font Validation v0 (Phase-EvaluationTools-OCR-002)

## Goal

解决 synthetic 中文数据集中 **中文不可见（tofu block 方框）** 问题，在生成中文样本前先完成字体可见性验证，避免把数据质量问题误判为 OCR provider 能力问题。

## Hard boundaries

- **Evaluation Tools only**：不属于 Luna runtime 主线，不接入 runtime。
- **Not whitebox**：不接入 whitebox。
- **No OCR provider invocation**：本阶段不调用 RapidOCR/PaddleOCR/Tesseract/macOS Vision 等任何 OCR provider。
- **No MidPlatform / SceneDelta / WorldContextEvidence / semantic / Qwen / TTS / playback / world write / hive upload**。

## Inputs

- 系统字体目录（macOS 常见）：
  - `/System/Library/Fonts`
  - `/System/Library/Fonts/Supplemental`
  - `/Library/Fonts`
  - `~/Library/Fonts`

## Outputs

工具 `tools/evaluation/ocr/validate_chinese_fonts_for_ocr_synthetic_v0.py` 输出到 `--output-root`：

- `chinese_font_registry.json`：候选字体扫描结果
- `chinese_font_selection_report.json`：选择结果（selected font）
- `chinese_font_visibility_report.json`：probe 验证报告
- `chinese_font_probe_images/`：probe 渲染图（人工抽查）
- `font_validation_summary.json`：汇总 + hard_audit
- `font_validation_notes.md`：说明与边界声明

## GO / NO_GO

- **GO**：存在至少一个可加载并通过 CJK 可见性 probe 的字体，且 tofu_suspected=false。
- **NO_GO**：找不到可用字体，或 CJK 仍渲染为 tofu。


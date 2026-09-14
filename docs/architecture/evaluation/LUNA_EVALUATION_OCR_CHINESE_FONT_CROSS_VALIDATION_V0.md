# LUNA Evaluation Tools — OCR Chinese Font Cross Validation v0 (Phase-EvaluationTools-OCR-002)

## Why

单一 verifier（尤其验证对象本身是“字体是否真的可见中文”）容易形成“自证正确”的闭环。  
因此在 OCR-002 中追加 **Cross Validation**，用独立策略复核“图片里是否真的存在可见中文”。

## Hard boundaries

- Evaluation Tools only；不接入 runtime / whitebox。
- Cross validation 不改变数据集 ground truth，不作为 OCR 主线 provider 决策依据。
- 不进入 MidPlatform / SceneDelta / WorldContextEvidence / semantic / 语音链路。

## Cross validation pack (v0)

工具：`tools/evaluation/ocr/cross_validate_ocr_chinese_font_quality_gate_v0.py`

包含三类交叉验证：

1. **Glyph diversity cross-check（像素级）**
   - 渲染多个中文字符为 mask
   - 计算差异度与重复签名占比，检测“多字符渲染为同一占位符 glyph”
2. **Tofu similarity report（图像级，弱检测）**
   - 在实际生成图片中抽样
   - 检测近似方形组件与重复 patch 比例，输出 tofu_suspected_rate
3. **RapidOCR probe cross-check（可选）**
   - 仅用于 Evaluation Tools 内部抽查“是否能读出至少部分中文”
   - 即使 RapidOCR 全空，也 **不直接判字体失败**，只记为 provider_followup

并生成：

- `human_review_contact_sheet.png`：10 张抽样 contact sheet + gt 标签
- `human_review_index.json`：抽样索引（sample_id / gt / category / font_path）
- `cross_validation_trace.jsonl` / `cross_validation_replay.jsonl`：evaluation-only 审计

## GO / CONDITIONAL_GO / NO_GO（cross verifier）

- **GO**：glyph diversity = GO 且 tofu similarity = GO；RapidOCR probe 仅作为补充
- **CONDITIONAL_GO**：任一项为 CONDITIONAL_GO（通常是 RapidOCR probe 或弱检测不确定），要求人工看 contact sheet
- **NO_GO**：glyph diversity = NO_GO 或 tofu suspected rate 过高


# LUNA Evaluation Tools — OCR Quality Perturbation Matrix v0 (Phase-EvaluationTools-OCR-006)

质量扰动维度（v0）：

- `size_scale`: tiny/small/normal/large/oversized_image_small_text
- `blur`: none/mild/medium/heavy
- `contrast`: high/normal/low/very_low
- `brightness`: normal/underexposed/overexposed
- `compression`: none_png/mild_jpeg/heavy_jpeg
- `skew_angle`: 0/5/15/30
- `background`: white/textured/photo_background/gradient/noisy（v0 以合成近似为主）
- `layout_complexity`: single_line/multi_line/multi_column/grid/artistic_order/mixed_icon_text

用途：

- 与 OCR-004 输入质量门控联动，形成 “quality × accuracy” 边界地图。


# LUNA Evaluation — OCR Real-World Taxonomy Coverage v0

## 必备五类（OCR-006 placeholder 对齐）

1. `icon_text_mix`  
2. `multi_panel_layout`  
3. `artistic_text`  
4. `stylized_digits`  
5. `decorative_graphic_non_text`

## 报告字段

`taxonomy_coverage_report.json`：

- `per_type.<type>.real`：非 `placeholder` 的样本数。  
- `per_type.<type>.placeholder`：`sample_source=placeholder` 数。  
- `required_types_all_present`：五类是否均至少有一条 manifest。

## 可选扩展

`product_label`、`signboard`、`vertical_text`、`low_quality_text` 可在额外真实 fixture 中循环分配。

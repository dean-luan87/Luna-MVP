# LUNA OCR Provider Input Pack v0

**Schema 常量**：`ocr_provider_input_pack_v0`（见 `capabilities/ocr_runtime/ocr_provider_input_pack_v0.py`）

## 设计意图

OCR Provider **只消费**「标准化输入包」，不直接依赖原始磁盘路径的偶然形态。包内携带 **input_units**、**坐标变换**、**source_chain** 与 **audit** 标记，便于回放与合规审计。

在中台总纲下，本 pack 可视为 **BestAvailableInputSource** 在 OCR 消费侧的 **v0 载体**（多模态扩展见 [LUNA_MIDPLATFORM_INPUT_SOURCE_GOVERNANCE_V0.md](../LUNA_MIDPLATFORM_INPUT_SOURCE_GOVERNANCE_V0.md)）。

## 顶层字段（摘要）

| 字段 | 说明 |
|------|------|
| `schema_version` | 固定为 `ocr_provider_input_pack_v0`。 |
| `pack_id` | 唯一包 ID。 |
| `source_image_ref` | 原始输入图像绝对路径。 |
| `normalized_image_ref` | 规范化后（或策略允许的源图引用）路径。 |
| `image_fingerprint` | 源文件内容指纹（SHA256，截断读取策略由实现定义）。 |
| `input_units[]` | 每个单元描述一类 provider 输入（整图 / 降采样整图 / ROI / tile 等）。 |
| `processing_policy` | `strategy` + `reason_codes`（与闸门理由对齐）。 |
| `source_chain` | 人类可读处理步骤序列。 |
| `coordinate_transform` | 包级聚合变换（与单元内 JSON 字符串一致的数据子集）。 |
| `stcm_deadline_hint` | 与 STCM 期限类提示（本阶段为占位级）。 |
| `audit` | 归一化与「禁止动作」类布尔标记（全部为 false 表示未越界）。 |

## `input_units[]` 单元字段（摘要）

- `unit_id`, `unit_type`：`full_image` \| `downscaled_full_image` \| `roi` \| `tile`  
- `image_ref`, `bbox_in_original`, `scale_ratio`  
- `coordinate_transform`：JSON 字符串，可解析为 `original_*` / `transformed_*` / `scale_*`  
- `width`, `height`, `megapixels`  
- `provider_level_hint`, `ocr_allowed`

## 校验

运行时轻量校验：`validate_provider_input_pack_v0()`。

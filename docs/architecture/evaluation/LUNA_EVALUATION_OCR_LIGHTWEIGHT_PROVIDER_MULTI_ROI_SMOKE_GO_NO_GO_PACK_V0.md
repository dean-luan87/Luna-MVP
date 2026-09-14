# Luna Evaluation — OCR Lightweight Provider Multi-ROI Smoke GO / NO_GO Pack v0

**Phase**: `Phase-OCR-Lightweight-Provider-Multi-ROI-Smoke-001`  
**Verifier**: `tools/evaluation/ocr/verify_ocr_lightweight_provider_multi_roi_smoke_v0.py`

## 语义边界

- **GO** 表示：至少 **2** 个 ROI unit；RapidOCR 路径下 **`text_joined` 非空**；`per_roi_provider_status` 可区分 **≥2** 个 `source_unit_ref`；禁止项 audit 为 false；有 provider 几何时抬升完整。  
- **不等于** Scene Delta、空间锚点消费、多 ROI 语义合并策略已定稿、或 Paddle 可接入。

## GO

- `input_pack.processing_policy.strategy == roi_list`；`input_units` 数量 ≥ 2；每 unit `unit_type=roi`，含 `unit_id`、`roi_id`、`bbox_in_original`、`image_ref`。  
- 每条 evidence `text_item` 含合法 `source_unit_ref`，且可归因到某一 input unit 的 `image_ref`。  
- `paddleocr_invoked`、`rapidocr_replaced`、`ocr_routing_changed`、`midplatform_invoked`、`world_model_written` 不为 true。  
- `audit.multi_roi_processed == true`（且 `roi_unit_count` 与 units 一致）。

## CONDITIONAL_GO

- 部分 ROI 识别为空，但 **`per_roi_provider_status`** 等可解释；或 `text_joined` 为空但链路未越界（例如 Rapid 不可用回退 stub 且记录完整）。  
- `eligible_text_evidence` 或 bridge 形态与预期略有偏差但记录在 `soft_notes`。

## NO_GO

- units 少于 2、strategy 非 `roi_list`、缺失 `roi_id`/`unit_id`/bbox。  
- evidence **混归**（`source_unit_ref` 无法匹配任何 unit）。  
- 有几何却未抬升（`coordinate_lift_applied` 与 original 几何矛盾）。  
- Paddle 被调用、改 routing、进 MidPlatform / WorldModel、禁止 audit 为 true。

# OCR Lightweight Provider Normalized Input Smoke — GO / CONDITIONAL_GO / NO_GO Pack v0

**Phase**: `Phase-OCR-Lightweight-Provider-Normalized-Input-Smoke-001`

## GO

- 原图边长大于 lightweight cap（默认 512），且 **normalized unit 宽高均 ≤ cap**。  
- `downscale_applied=true`，`original_image_used_directly=false`，`coordinate_transform_recorded=true`。  
- `input_pack.input_units[0].unit_type=downscaled_full_image`。  
- `image_ref` **不等于**原 oversized PNG 路径（必须指向归一化产物）。  
- `selected_provider=rapidocr_candidate`，`real_provider_invoked=true`，`status=success`。  
- `text_joined` **非空** 且 `text_items` **≥1**；`bridge_pack` 合法。  
- 禁止类 audit：`paddleocr_invoked`、`rapidocr_replaced`、`ocr_routing_changed`、`midplatform_invoked`、`world_model_written` 均非 true。

## CONDITIONAL_GO

- 上述归一化 / pack / audit / 原图不直通条件均满足，且 **RapidOCR 已调用** 但 **`text_joined` 为空**（不伪造非空）。  
- 或 Rapid **不可用** 且 stub 回退 **reason 可解释**（与 text smoke 语义一致）。

## NO_GO

- 原图路径被当作 **唯一** `image_ref` 直通真实 provider（未归一化）。  
- `downscale_applied` 非 true 或 `unit_type` 非 `downscaled_full_image`（本 smoke 预期路径）。  
- normalized 尺寸仍 **超过** cap。  
- Paddle 调用、禁止 audit 为 true、缺产物、unavailable 却宣称 GO。

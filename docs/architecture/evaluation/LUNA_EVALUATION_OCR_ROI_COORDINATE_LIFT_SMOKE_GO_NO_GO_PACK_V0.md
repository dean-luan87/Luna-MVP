# Luna Evaluation — OCR ROI Coordinate Lift Smoke GO / NO_GO Pack v0

**Phase**: `Phase-OCR-ROI-Evidence-Coordinate-Lift-001`  
**Verifier**: `tools/evaluation/ocr/verify_ocr_roi_coordinate_lift_smoke_v0.py`

## 语义边界

- **GO** 表示：RapidOCR 返回了可用的 **local** 几何，且按 `coordinate_transform` 成功生成 **original** 几何，并出现在 evidence 与 `eligible_text_evidence` 中；禁止项 audit 为 false。  
- **不等于** 多 ROI、tile 真实 OCR、Scene Delta 已接线、或 OCR 质量验收。

## GO

- Summary 中 `input_pack_processing_policy.strategy == roi`，且 `coordinate_transform` 含 `offset_x` / `offset_y` / `scale_x` / `scale_y`。  
- `audit.roi_coordinate_lift_applied`、`provider_geometry_available`、`original_geometry_recorded` 为 true；`provider_geometry_unavailable` 为 false。  
- 每条 `coordinate_lift_applied=true` 的 `text_item` 具备 `original_bbox` 或 `original_polygon`。  
- `bridge_pack.eligible_text_evidence` 中对应项保留 **original** 几何。  
- `paddleocr_invoked`、`rapidocr_replaced`、`ocr_routing_changed`、`midplatform_invoked`、`world_model_written` 不为 true。

## CONDITIONAL_GO

- RapidOCR 有文本但 **无可靠 polygon/box**（`provider_geometry_unavailable=true`），且 **未伪造** original 几何。  
- 或 lift 审计字段与 evidence 部分一致但仍可解释（见 verifier `soft_notes`）。

## NO_GO

- 缺 transform 字段仍声称已抬升；`coordinate_lift_applied=true` 但无 original 几何。  
- 伪造 geometry（lift 与几何不一致）。  
- Paddle 被调用、routing 被改、进 MidPlatform / WorldModel。  
- 禁止 audit 项为 true。

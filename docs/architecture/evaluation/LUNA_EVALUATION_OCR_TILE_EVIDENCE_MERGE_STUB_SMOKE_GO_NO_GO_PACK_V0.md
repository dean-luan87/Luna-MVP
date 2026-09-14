# OCR Tile Evidence Merge Stub Smoke — GO / NO_GO Pack v0

## GO

1. `tile_evidence_items` 数量等于 `materialized_tile_count`。  
2. 每条含 `tile_id`、`source_unit_ref`、`original_bbox` 或 `original_polygon`、`coordinate_transform_applied=true`。  
3. `coverage_complete=false` 时：`evidence_scope=partial_image`，`full_image_claim_allowed=false`，`text_joined` 以 `[PARTIAL_TILE_EVIDENCE]` 开头。  
4. `bridge_pack.tile_evidence_summary` 存在。  
5. `source_chain` 含 `tile_evidence_merged` 与 `coordinate_reconstruction_applied`。  
6. `audit.tile_evidence_generated` 与 `coordinate_reconstruction_applied` 为 true；禁止类 audit 为 false。  
7. `verdict=GO`。

## CONDITIONAL_GO

- `reading_order_candidate` 仍为低置信占位；  
- 未实现真实 duplicate merge / 阅读顺序治理。

## NO_GO

- 多 tile 仅一条无 `tile_id` 的证据；  
- 丢失原图几何或 `coordinate_transform_applied`；  
- partial 被标为整图全文；  
- 调用真实 OCR 或改 routing 或进入 MidPlatform / WorldModel。

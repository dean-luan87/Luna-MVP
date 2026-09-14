# OCR Tile Planner Smoke — GO / NO_GO Pack v0

## GO

1. `ocr_tile_plan.json` 存在且含 `schema_version: ocr_tile_plan_v0`。  
2. `ocr_provider_input_pack.json` 通过 `validate_provider_input_pack_v0`。  
3. `processing_policy.strategy == tile`。  
4. `input_units` 数量 **> 1**，且每条 `unit_type == tile`。  
5. 每个 tile 具备 `bbox_in_original`、`overlap_ratio`、可解析的 `coordinate_transform`（含 `tile_bbox_in_original`、`offset_x/y`、`scale_x/y`、`original_width/height`）。  
6. `source_chain` 含 `original_image_ref:`、`tile_plan_created`、`tile_generated`、`coordinate_transform_recorded`。  
7. `audit.original_image_used_directly == false`，`tile_applied == true`，`coordinate_transform_recorded == true`，禁止类标记均为 false。  
8. stub `input_pack_id` 非空，`input_unit_count` 与 pack 一致，`first_unit_type == tile`，`unit_type_counts["tile"] >= 2`。  
9. `ocr_mainline_bridge_result.json` 中 `status == success`。  
10. `verdict == GO`。

## CONDITIONAL_GO

- `truncated_to_max_tile_count_sync == true` 但截断说明完整、其余检查通过。  
- 或仅生成逻辑 unit、tile 图未落盘（本仓库实现默认 **落盘**；若未来支持逻辑-only，文档保留此条）。

## NO_GO

- 大图仍以单 `full_image` 直通 provider。  
- 缺坐标回填或缺 `source_chain` 关键节点。  
- stub 无法消费多 `input_units`。  
- 调用真实 OCR、修改 routing、进入 MidPlatform / WorldModel。

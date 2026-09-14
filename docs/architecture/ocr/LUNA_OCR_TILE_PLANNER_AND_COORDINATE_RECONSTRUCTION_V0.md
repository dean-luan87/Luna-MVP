# LUNA OCR Tile Planner and Coordinate Reconstruction v0

**阶段**：`Phase-OCR-Tile-Planner-And-Coordinate-Reconstruction-001`  
**实现入口**：`capabilities/ocr_runtime/ocr_tile_planner_v0.py`（由 `ocr_image_normalization_pipeline_v0` 在 **tile** 策略下调用）

## 目的

在 **不调用真实 OCR**、**不改 routing**、**不进入 MidPlatform / WorldModel** 的前提下，对满足治理阈值的超大图生成 **多个 `unit_type=tile` 的 `input_units`**，落盘各 tile 裁剪图，并为每个 tile 记录 **原图 bbox**、**overlap_ratio** 与 **tile_local→original** 的坐标元数据（`coordinate_transform` JSON），使下游（含 stub）可消费 **多 unit** 的 `ocr_provider_input_pack_v0`。

## 触发条件（闸门 + 环境）

- 治理配置 `size_limits.max_megapixels_requires_tiling`（与 `megapixels >=` 比较）及 `tiling_policy` 生效时，若 **`LUNA_ENABLE_OCR_TILE_PLANNER_V0=true`**，则 `ImageInputGate` 对超大图返回 **`recommended_input_strategy=tile`**（`CONDITIONAL_ALLOW`）。  
- **`LUNA_ENABLE_OCR_TILE_PLANNER_V0=false`**（默认）时，超大图仍走既有 **downscale 兜底**（与 `Phase-OCR-ImageInput-Normalization-Pipeline-001` 一致），避免静默改变行为。

## Tile 规划参数（来自治理 JSON）

- `tiling_policy.tile_max_side`  
- `tiling_policy.tile_overlap_ratio`  
- `tiling_policy.max_tile_count_sync` / `max_tile_count_async`  
- `tiling_policy.requires_coordinate_reconstruction`

当理论 tile 数超过 `max_tile_count_sync` 时，规划器 **截断** tile 列表并在 `ocr_tile_plan_v0` 中标记 `truncated_to_max_tile_count_sync=true`。**覆盖率、partial 证据语义与「不得冒充整图 OCR」** 见 [LUNA_OCR_TILE_COVERAGE_AND_TRUNCATION_POLICY_V0.md](./LUNA_OCR_TILE_COVERAGE_AND_TRUNCATION_POLICY_V0.md)（`Phase-OCR-Tile-Coverage-And-Truncation-Policy-001`）。

## 每个 tile unit 必备字段（摘要）

`unit_id`, `unit_type=tile`, `image_ref`, `bbox_in_original`, `tile_index`, `tile_row`, `tile_col`, `overlap_ratio`, `width`, `height`, `megapixels`, `scale_ratio`, `coordinate_transform`（含 `original_*`、`tile_bbox_in_original`、`offset_*`、`scale_*`、`tile_local_to_original_transform`）, `provider_level_hint`, `ocr_allowed`。

## Provider Input Pack

- `processing_policy.strategy` 必须为 **`tile`**。  
- `source_chain` 含：`original_image_ref:...`、`tile_plan_created`、`tile_generated`、`coordinate_transform_recorded` 等节点。  
- 包级 `coordinate_transform` 使用 `mode=multi_tile` 聚合摘要；逐 tile 几何以各 unit 内 JSON 为准。

## 相关评测文档

- `docs/architecture/evaluation/LUNA_EVALUATION_OCR_TILE_PLANNER_SMOKE_V0.md`  
- `docs/architecture/evaluation/LUNA_EVALUATION_OCR_TILE_PLANNER_SMOKE_GO_NO_GO_PACK_V0.md`

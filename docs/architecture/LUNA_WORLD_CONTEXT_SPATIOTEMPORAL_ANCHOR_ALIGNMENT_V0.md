# LUNA — WorldContextEvidence Spatiotemporal Anchor Alignment v0

## Phase

- **Phase-WorldModel-ContextEvidence-003**

## Purpose

为 `WorldContextEvidenceCandidate` 严格对齐与透传“它属于哪里”的信息，确保：

- 不伪造 GPS/POI
- 优先继承 SceneDelta 的 `SpatiotemporalDeltaAnchor`
- 当锚点缺失时诚实降级（revalidation + trust 降权 + no/low write）

## Observed Where 透传优先级

### 1) SceneDelta SpatiotemporalDeltaAnchor（最高优先级）

当输入为 `scene_delta_root` 且 trace/decision 可提供：

- `spatiotemporal_anchor_ref`
- `anchor_type`
- `spatial_signature`
- `spatial_scope`（scene_local）

则：

- `observed_where_source="scene_delta_anchor"`
- `observed_where.spatial_anchor_type` 至少为 `visual_landmark`（或 `unknown`）
- `anchor_status="present"`
- `spatial_anchor_confidence` 赋予较高占位值（例如 0.8）

### 2) MidPlatform OCR Evidence observed_where（次优先级）

当输入为 `midplatform_ocr_bridge_root`：

- 不得编造 `lat/lng`
- 可透传 `image_ref`（frame_id / source_evidence_id）
- 可透传 `crop_region`（OCR bbox union）

则：

- `observed_where_source="midplatform_ocr_evidence"`
- `anchor_status="missing_or_unresolved"`（直到后续 anchor 解算阶段）
- `spatial_anchor_confidence` 保守占位（例如 0.3）

### 3) YOLO×OCR Bridge source attribution（本阶段仅占位）

若上游输入中真实存在 YOLO bbox / detection refs，则可作为 observed_where 的补充来源。
本阶段不新增 runtime 获取逻辑，不得猜测。

### 4) Fallback unknown（最低）

当无锚点输入：

- `observed_where.spatial_anchor_type="unknown"`
- `anchor_status="missing_or_unresolved"`
- `lifecycle.requires_revalidation=true`

## Hard rules

- 不得在没有真实地图/GPS输入时生成 `lat/lng`
- 不得把“处理层”（midplatform/scene_delta）当作感知来源（感知来源应在 `source_modalities` 体现）


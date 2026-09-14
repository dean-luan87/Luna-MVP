# LUNA — MapAnchor Observability Requirements v0

## Phase

- **Phase-WorldModel-MapAnchor-001**

## Purpose

定义 MapAnchor 的 trace/replay/whitebox 最小可观测要求（只定义，不接真实地图 API）。

## Trace（must include）

- `map_anchor_evidence_id`
- `source_type`
- geo availability（是否有 lat/lng/accuracy）
- `accuracy_m`
- `poi_context`（poi_id/poi_type/distance/poi_confidence）
- `spatial_scope`（scope_type/radius/polygon_ref/scope_confidence）
- `anchor_status`
- `spatial_anchor_grade`
- `conflict_status`
- governance flags（navigation_action=null 等）

## Replay（must include）

- raw provider response ref（若存在，仅引用，不落真实数据）
- gps fix ref（若存在）
- map query ref（若存在）
- visual alignment ref（若存在）
- user correction ref（若存在）
- conflict decision ref（若存在）

## Whitebox（must include）

- `why_bound`
- `why_weakly_bound`
- `why_unresolved`
- `why_contradicted`
- `why_map_not_treated_as_fact`
- `why_requires_revalidation`
- `why_no_navigation_action`


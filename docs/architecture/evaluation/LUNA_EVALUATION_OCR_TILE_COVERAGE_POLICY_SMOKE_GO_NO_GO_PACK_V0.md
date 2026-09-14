# OCR Tile Coverage Policy Smoke — GO / NO_GO Pack v0

## GO

1. `raw_tile_count` / `materialized_tile_count` 存在。  
2. 当 `materialized < raw`：`coverage_complete=false`，`truncated_to_budget=true`，`evidence_scope=partial_image`，`full_image_claim_allowed=false`。  
3. `ocr_evidence` / `bridge_pack` 含 `evidence_scope=partial_image`，`text_joined` 以 `[PARTIAL_TILE_EVIDENCE_STUB]` 开头。  
4. `source_chain` 含 `tile_plan_raw_count:`、`tile_materialized_count:`、`tile_truncated_to_budget:`、`coverage_complete:`。  
5. `audit`：`partial_evidence_scope_recorded=true`，`tile_truncated_to_budget=true`（partial 场景），禁止类标记为 false。  
6. `verdict=GO`。

## CONDITIONAL_GO

- `coverage_ratio_estimate` 为面积启发式（重叠 double-count），但截断语义完整。  
- `uncovered_regions` 仅为未物化 slot 的 bbox，未做几何求差并集。

## NO_GO

- `materialized < raw` 却 `coverage_complete=true`。  
- partial 场景 `full_image_claim_allowed=true` 或缺少 `evidence_scope`。  
- 未记录截断或缺少上述 `source_chain` 节点。  
- 调用真实 OCR、改 routing、进入 MidPlatform / WorldModel。

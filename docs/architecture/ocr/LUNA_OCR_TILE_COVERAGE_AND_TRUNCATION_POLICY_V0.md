# LUNA OCR Tile Coverage and Truncation Policy v0

**阶段**：`Phase-OCR-Tile-Coverage-And-Truncation-Policy-001`  
**前置**：`Phase-OCR-Tile-Planner-And-Coordinate-Reconstruction-001` = GO

## 问题陈述

同步 tile 上限（`max_tile_count_sync`）会导致 **物化 tile 数 < 理论网格 tile 数**。此时系统若仍把 stub/OCR 输出当作「整图全文结果」，会在公告、长图、说明书等场景产生 **漏读下半部却不可见** 的风险。

## 设计原则

1. **截断必须显式**：`truncated_to_budget=true`，`source_chain` 记录 raw/materialized 计数与截断布尔。  
2. **不得伪装全覆盖**：`materialized_tile_count < raw_tile_count` ⇒ `coverage_complete=false`，`evidence_scope=partial_image`，`full_image_claim_allowed=false`。  
3. **覆盖率可解释**：输出 `covered_regions[]`、`uncovered_regions[]`（未物化 slot 的 bbox 列表）、`coverage_ratio_estimate`（本阶段为 **物化 tile 面积之和 / 图像面积** 的上限估计，重叠会 double-count，见 `coverage_ratio_method`）。  
4. **证据文本披露**：partial 时 `text_joined` 前缀 `[PARTIAL_TILE_EVIDENCE_STUB]`，`ocr_evidence` / `bridge_pack` 携带 `evidence_scope` 与 `text_coverage_disclosure`。  
5. **异步补全接口**：`async_completion_available` 依据 `max_tile_count_async` 与当前物化数粗判，供后续 STCM/async 路径接线。

## 字段位置

| 位置 | 字段 |
|------|------|
| `ocr_tile_plan_v0` | `raw_tile_count`, `materialized_tile_count`, `truncated_to_budget`, `coverage_complete`, `coverage_ratio_estimate`, `covered_regions`, `uncovered_regions`, `max_tile_count_applied`, `tile_budget_type`, `async_completion_available` |
| `ocr_provider_input_pack_v0.tile_coverage` | 上述摘要子集（`schema_version: ocr_tile_coverage_summary_v0`） |
| `processing_policy` | `evidence_scope`, `full_image_claim_allowed`, `reading_order_confidence`, `async_completion_available` |
| `ocr_runtime_audit_v0` | `tile_coverage_complete`, `tile_truncated_to_budget`, `full_image_claim_allowed`, `partial_evidence_scope_recorded` |

## 评测

- `docs/architecture/evaluation/LUNA_EVALUATION_OCR_TILE_COVERAGE_POLICY_SMOKE_V0.md`  
- `docs/architecture/evaluation/LUNA_EVALUATION_OCR_TILE_COVERAGE_POLICY_SMOKE_GO_NO_GO_PACK_V0.md`

## 一句话

**同步截断下的 partial tile 证据只能标为 partial_image，不得冒充整图 OCR 结果**；覆盖率与未覆盖区域必须可审计、可解释。

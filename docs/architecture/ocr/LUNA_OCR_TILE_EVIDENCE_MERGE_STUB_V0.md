# LUNA OCR Tile Evidence Merge Stub v0

**阶段**：`Phase-OCR-Tile-Evidence-Merge-Stub-001`  
**实现入口**：`capabilities/ocr_runtime/ocr_tile_evidence_merge_stub_v0.py`（由 `ocr_mainline_bridge_v0` 在 **tile** 全量 `input_units` 为 tile 时调用）

## 目的

在 **不运行真实 OCR**、**不改 routing**、**不进入 MidPlatform / WorldModel** 的前提下：

1. **Stub** 对每个 `unit_type=tile` 生成一条 mock 证据（`MOCK_TEXT_TILE_<n>`、`local_bbox` / `original_bbox`、`original_polygon`、`coordinate_transform_applied`、`source_unit_ref`）。  
2. **Merge stub** 将多条 tile 证据合并为统一 **`text_joined`**、**`tile_evidence_items`**、**`reading_order_candidate`**（低置信占位），并保留 **`tile_coverage`** 语义。  
3. **Bridge pack** 增加 **`tile_evidence_summary`**、**`eligible_text_evidence`**、**`tile_coverage`**、**`source_reference_chain`** 等字段，**`raw_text_joined`** 为无披露前缀的拼接串。

## Partial 披露

当 `processing_policy.evidence_scope=partial_image`（通常与 `coverage_complete=false` 一致）：

- `text_joined` 以 **`[PARTIAL_TILE_EVIDENCE]`** 前缀开头；  
- `full_image_claim_allowed=false`；  
- `reading_order_candidate.confidence=low`，`reason` 标明 provider 顺序占位、无 duplicate merge。

## Source chain（bridge 结果）

在 pack 自带 `source_chain` 之后追加：**`tile_evidence_merged`**、**`coordinate_reconstruction_applied`**。

## Audit（顶层）

- `tile_evidence_generated=true`  
- `tile_evidence_item_count` = 物化 tile 数  
- `coordinate_reconstruction_applied=true`  

## 与 Partial Evidence Completion 的衔接

本 merge stub 在输出中附带 **`partial_evidence_completion`**（`ocr_partial_evidence_completion_policy_stub_v0`）：仅 **占位与风险闸门**，不生成任何补全候选文本。语义与硬边界见 [LUNA_OCR_PARTIAL_EVIDENCE_COMPLETION_POLICY_V0.md](./LUNA_OCR_PARTIAL_EVIDENCE_COMPLETION_POLICY_V0.md)（`Phase-OCR-Partial-Evidence-Completion-Policy-001`）。

## 评测

见 `docs/architecture/evaluation/LUNA_EVALUATION_OCR_TILE_EVIDENCE_MERGE_STUB_SMOKE_V0.md`。

## 一句话

**多 tile stub 证据在 evidence / bridge_pack 层显式可合并、可回溯坐标，且 partial 场景不冒充整图 OCR。**

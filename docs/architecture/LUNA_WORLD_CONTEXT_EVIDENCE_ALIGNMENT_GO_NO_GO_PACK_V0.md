# LUNA — WorldContextEvidence Alignment Go/No-Go Pack v0

## Phase

- **Phase-WorldModel-ContextEvidence-003**

## Scope

仅对齐与增强 `WorldContextEvidenceCandidate`：

- observed_where / spatiotemporal_anchor_ref 透传
- source_evidence_refs 直接引用格式
- source_reference_chain 完整引用链（允许 partial，但不得伪造）
- 缺失锚点/缺失引用链的降级策略

仍然：

- candidate-only
- 不写世界模型、不上传蜂巢、不推荐、不导航、不播报

## GO conditions

- 三类输入均跑通（midplatform/scenedelta/sample_matrix）
- W–AF 检查全部通过
- governance 禁止项全为 false/null
- trace/replay/whitebox 非空

## CONDITIONAL_GO

- 上游输入本身缺少 anchor（例如 midplatform 不含 SceneDelta anchor），但能 **honest degrade**：
  - `anchor_status="missing_or_unresolved"`
  - `observed_where_source="midplatform_ocr_evidence"` 或 `fallback_unknown`
  - `requires_revalidation=true`
  - `source_ref_integrity_status` 不是 complete 时有 `missing_source_refs`

## NO_GO

任意一条即 NO_GO：

- 伪造 GPS（lat/lng 非 null 且上游无 gps 输入）
- `source_evidence_refs` 为空仍生成候选（AE hard gate）
- `source_reference_chain` 缺失或为空
- unknown anchor 未触发 requires_revalidation
- 触发任何 runtime/写入/蜂巢/导航/TTS/推荐


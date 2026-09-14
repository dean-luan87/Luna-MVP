# LUNA — WorldContextEvidence Candidate Closure Review v0

## Phase

- **Phase-WorldModel-ContextEvidence-004**

## Closure scope（收口对象）

本次 closure 将以下阶段冻结为 `closed_v0`（candidate-only offline skeleton）：

- Phase-WorldModel-ContextEvidence-001（Spatiotemporal & Trust Evidence Contract v0）— **GO**
- Phase-WorldModel-ContextEvidence-001-Fix（Field Mapping Alignment v0）— **GO**
- Phase-WorldModel-ContextEvidence-002（WorldContextEvidence Candidate Skeleton v0）— **GO**
- Phase-WorldModel-ContextEvidence-003（Spatiotemporal Anchor & Source Reference Alignment v0）— **GO**

## What is frozen（冻结内容）

- `WorldContextEvidenceCandidate` 的最小可用结构：
  - observed_at / observed_where / spatiotemporal_anchor_ref
  - source_evidence_refs（direct refs）
  - source_reference_chain（full chain）
  - trust / lifecycle / world_model_policy
  - trace / replay / whitebox
- “缺失不得伪造”的底线：
  - 无 GPS 不伪造 GPS
  - 链不完整记录 `missing_source_refs`
  - 缺锚点 honest degrade（unknown anchor + requires_revalidation）
- governance 禁止项全冻结为 false/null

## What is NOT claimed（不宣称）

- 不宣称已具备真实世界模型写入 readiness
- 不宣称已接入 runtime 或下游 SceneTask/Fusion/Output
- 不宣称可用于推荐/导航/播报

## Frozen status（建议冻结状态）

```json
{
  "world_context_evidence_status": "closed_v0",
  "scope": "candidate_only_offline_skeleton",
  "spatiotemporal_contract": "done",
  "field_alignment": "done",
  "candidate_skeleton": "done",
  "anchor_source_alignment": "done",
  "real_world_model_write_allowed": false,
  "hive_upload_allowed": false,
  "recommendation_allowed": false,
  "navigation_action_allowed": false,
  "real_tts_allowed": false,
  "runtime_allowed": false
}
```


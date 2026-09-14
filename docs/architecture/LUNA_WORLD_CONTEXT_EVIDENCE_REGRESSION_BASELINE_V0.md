# LUNA — WorldContextEvidence Regression Baseline v0

## Phase

- **Phase-WorldModel-ContextEvidence-004**

## Baseline roots（固定）

- `logs/world_context_evidence_003_midplatform_20260430_1103`
- `logs/world_context_evidence_003_scenedelta_20260430_1103`
- `logs/world_context_evidence_003_sample_20260430_1103`

## Hard gates（不允许波动）

- fabricated GPS（lat/lng 非 null）
- `source_evidence_refs` 为空
- 缺 `observed_where_source`
- 缺 trust/lifecycle/world_model_policy
- trace/replay/whitebox 任意缺失或为空
- 任意 governance 禁止项为 true / non-null（world write / hive / recommendation / nav / tts）

## Allowed fluctuations（允许波动）

- candidate count
- commercial candidate count
- world_change_event count
- trust_score 数值
- lifecycle 状态分布
- observed_where.spatial_anchor_type 分布
- source_reference_chain 深度分布


# LUNA — WorldContextEvidence Candidate Regression v0

## Phase

- **Phase-WorldModel-ContextEvidence-004**

## Purpose

对 ContextEvidence-003 的三类 output_root 进行只读回归验收，产出回归汇总、矩阵、边界与审计摘要，为 closure 提供证据。

## Inputs（Regression roots）

- `logs/world_context_evidence_003_midplatform_20260430_1103`
- `logs/world_context_evidence_003_scenedelta_20260430_1103`
- `logs/world_context_evidence_003_sample_20260430_1103`

## Tools

- `tools/run_world_context_evidence_regression_v0.py`
- `tools/verify_world_context_evidence_regression_v0.py`

## Outputs（Regression output_root）

在回归 output_root 下输出：

- `world_context_evidence_regression_summary.json`
- `world_context_evidence_root_matrix.json`
- `world_context_evidence_candidate_matrix.json`
- `world_context_anchor_alignment_summary.json`
- `world_context_source_reference_chain_summary.json`
- `world_context_trust_lifecycle_policy_summary.json`
- `world_context_boundary_summary.json`
- `world_context_trace_replay_whitebox_summary.json`
- `regression_notes.md`

## Hard gates（必须满足）

- roots readable
- each root verifier=GO
- candidates count > 0
- observed_at/observed_where/observed_where_source present
- source_evidence_refs non-empty
- source_reference_chain present
- source_ref_integrity_status present
- no fabricated GPS
- trust/lifecycle/world_model_policy present
- trace/replay/whitebox non-empty
- governance 禁止项成立（不写世界模型/不上传蜂巢/不推荐/不导航/不播报）


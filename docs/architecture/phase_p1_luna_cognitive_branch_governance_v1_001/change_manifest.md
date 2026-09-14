# Change Manifest

## Added

- `capabilities/midplatform/core/cognitive_flow/cognitive_branch_governance_v1.py`
  - `CognitiveBranchGovernanceDecisionV1`
  - `CognitiveBranchGovernanceInputV1`
  - `CognitiveBranchGovernanceResultV1`
  - `govern_cognitive_branches`
- `capabilities/evaluation/cognitive_branch_governance/`
  - controlled fixtures
  - evaluation engine
  - user-terminal Runner
  - Verifier
- this phase documentation set。

## Modified

- `capabilities/midplatform/core/cognitive_flow/__init__.py`
  - exports Branch Governance contract and function。
- `docs/architecture/README.md`
  - records this Phase as GO — VERIFIED — PHASE CLOSED。
- existing Cognitive Flow growth-boundary documentation
  - distinguishes Branch Governance decisions from deferred Branch Lifecycle。
- previous Branch Formation phase relation/next-step documentation
  - records the new Governance handoff without changing its historical verification result。

## Explicitly not modified semantically

- Branch Formation algorithm and Candidate contract；
- Hypothesis / Information Need / Required Condition ownership；
- Sufficiency / Stop / Re-observation；
- Current World / Field；
- Resource, Observation, Capability, Task or Action runtime；
- Memory / PCN / Provider / Model / B Route runtime。

## Status

`GO — VERIFIED — PHASE CLOSED`

## Terminal verification closure

- `all_checks_passed=true`
- `cognitive_logic_result=PASS`
- `operational_result=PASS`
- `failed_checks=[]`
- `final_decision=GO`
- `COGNITIVE_BRANCH_GOVERNANCE_GAP=CLOSED`

用户终端确认多个有效 Branch 可同时 `ADMITTED`，无 winner-take-all；invalid
basis 局部 rejected；currently-not-needed / satisfied Need 相关 Branch 为
deferred；Candidate immutable；无 canonical equivalence 时保留 distinct
candidates；资源变化不影响治理。Formation、Resource、Observation、Lifecycle、
Decision、Task、Action、Provider、Model、Memory、PCN、Field、Current World 和
Truth 边界均未越过。

## Evaluation harness runtime repair

用户终端首次执行发现 `branch_candidates` collection-shape mismatch：
`BASIS_REMOVED:changed` 的单 Branch fixture 缺少 singleton tuple comma，导致
Runner 在 candidate immutability snapshot 前将单个 `CognitiveBranchCandidateV1`
当作 iterable 消费并崩溃。

已将该 fixture 修正为 canonical one-element collection。Verifier 的
`FileNotFoundError` 是 Runner 未生成 summary 的 downstream symptom；Runner
output path 与 Verifier default summary path 均为：

`_eval_out/cognitive_branch_governance_v1/runner_summary_v1.json`

本修复只统一 evaluation input collection shape，不改变 Governance cognition
semantics、Decision statuses 或 Candidate contract。

## Next boundary

`NEXT_BOUNDARY = GOVERNED_BRANCH_TO_INFORMATION_ACQUISITION_CONTINUITY`

后续已进入单独的 Information Acquisition Strategy Candidate Formation 与
Strategy Coordination 实现边界：
显式 governed acquisition basis 可为 admitted Branch 形成一个或多个 candidate-only
strategy representations。Strategy Coordination 已进入独立 controlled
implementation，但本 Phase 不拥有该语义。Resource Need/Merge、Priority、
Scheduling、Attention 与 Observation Demand 仍未实现，且不属于本 Phase closure。

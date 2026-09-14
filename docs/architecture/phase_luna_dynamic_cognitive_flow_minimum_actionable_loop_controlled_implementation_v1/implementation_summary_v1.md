# Dynamic Cognitive Flow minimum actionable loop

## Owner and reuse

The canonical lifecycle and re-entry owner remains **Cognitive Flow Governance**. The implementation reuses the existing B2 Cognitive State / Cognitive Flow contracts, B3 Intent/Decision/Task boundaries, B4 `ReconsiderationCandidateV1` handoff, the Cognitive Need → Capability Requirement bridge, Capability Scope / Resolution / Invocation candidates, Capability Experience outcome dimensions, FPO / Observation Gateway references, and the Brain Golden Baseline boundaries.

No parallel Planner, Decision, Intent, Capability, Task, or Observation owner is introduced. Existing canonical dataclasses are not changed. The new types are narrow candidate-only loop envelopes.

## Loop contract

`Cognitive Goal → Provisional Plan Candidates → Current Minimum Necessary Need → Capability Requirement → Governed Capability Candidate → Evidence / Outcome → Updated Cognitive State Version → Sufficiency / Reconsideration → STOP / CONTINUE / REPLAN / DEFER`.

Thought and plan remain non-binding. A plan is a set of candidate references, not an execution queue. Only the current minimum Need may be selected for downstream demand. The engine records the selected Need and keeps the remaining plan references non-binding.

## State transition and sufficiency

Each accepted evidence update creates a candidate state version with parent, evidence reference, current disposition, hypothesis lineage, and minimum Need reference. `SUFFICIENT` creates a `GoalSufficiencyCandidateV1` with `STOP_SUFFICIENT`; remaining plan candidates are not materialized and are not failures. A later candidate after sufficiency is ignored by the candidate loop.

`STOP_SUFFICIENT` is successful cognitive termination. It does not mean every plan candidate executed, and it does not require a successful capability call.

## Reconsideration and decision boundaries

Hypothesis invalidation, unavailable/degraded capability, or successful execution with an unsatisfied Requirement produces a `ReconsiderationCandidateV1`. `DEFER` and `REQUEST_MORE_EVIDENCE` are cognitive continuation boundaries only. They do not invoke providers, retry runtime work, activate camera, bypass Scope/authority, or mutate Decision/Task/Intent.

## Capability Experience relationship

Execution outcome, Requirement satisfaction, Task contribution, and cognitive sufficiency are four independent dimensions. In particular, capability `SUCCESS` does not imply Requirement `SATISFIED`; Requirement `SATISFIED` does not imply Goal `SUFFICIENT`; and Goal `SUFFICIENT` does not require complete plan execution. Capability failure is not automatically Task failure. Skipped or not-required calls are not capability failures.

Requirement candidates retain the state version that generated them. After a new state version, old Requirements are reassessed; stale Requirements can be `SUPERSEDED` and cannot force an Invocation Candidate downstream.

## Scenario coverage

There are 36 controlled scenarios in groups A-F. A03 is the primary seven-point exit search: two insufficient observations, third observation finds the exit, `STOP_SUFFICIENT`, and candidates 4-7 remain non-materialized. B covers hypothesis-changing evidence and replan. C covers unavailable/degraded capability. D separates capability outcome, Requirement satisfaction, Task contribution, and sufficiency. E covers capability failure alongside successful cognitive termination. F covers state-version reassessment and stale invocation blocking.

## Negative guards and deferred work

This phase does not implement runtime execution, model/provider invocation, camera, automatic acquisition/install/optimization, Action execution, Learning, Memory mutation, Hive learning, SRSK, semantic folding/expansion, World Truth escalation, Field mutation, or Capability Scope bypass. The runner and verifier are provided as user-terminal artifacts only.

## Verifier contract and status

Runner: `capabilities/midplatform/core/cognitive_flow/run_dynamic_cognitive_flow_controlled_implementation_v1.py`.

Verifier: `capabilities/midplatform/core/cognitive_flow/verify_dynamic_cognitive_flow_controlled_implementation_v1.py`.

Neither was executed in this turn. Current phase status remains `WAITING_FOR_USER_TERMINAL_VERIFICATION`.

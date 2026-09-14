# Result Comparison / Outcome Evaluation Architecture Planning v1

## Scope

This package plans the missing A Route feedback semantics only. It does not implement a runtime comparator, Prediction Engine, Learning runtime, Dynamic Cognitive Function, Emotion Engine, B Route, persistence, provider execution, or semantic compression.

## Inventory conclusion and owner decision

Current canonical assets provide result candidates, action/task/runtime lifecycle candidates, expectation feedback contracts, controlled reconsideration, trace/provenance and Learning input types. No canonical executable Result Comparison / Outcome Evaluation owner was found.

The decision is `D_NO_CANONICAL_OWNER_FOUND`. The recommended future narrow owner is `Outcome Evaluation Governance`. It owns comparability, structured deviation, outcome evaluation and candidate attribution/handoffs. It does not own Reality, Field, Context, Decision, Task, Action, Learning, Memory, Self, Personality, Emotion, or provider execution.

Historical `cognitive_action_outcome_evaluation_architecture_v1` assets are valuable B-class reference contracts. They are not treated as current implementation or as automatic owner authority.

## Core semantic boundaries

The following are frozen:

- Expected Outcome != Actual Result
- Expected State != Current World
- Comparison != Decision
- Comparison != Learning
- Deviation != Error
- Failure != Execution Error
- Unexpected Outcome != Wrong Decision
- Current World != External Reality Truth
- Result Comparison != Field Mutation
- Outcome Evaluation != Task Mutation
- Learning Signal Candidate != Learning Execution
- Reconsideration Candidate != Intent Mutation
- Provenance != Authority
- Confidence != Correctness
- Model Confidence != Outcome Success

Comparison produces candidates about relationships between references. It never declares Reality truth or mutates any owner.

## Expected Outcome and Actual Result

Expected inputs may reference a decision expected outcome, task completion criterion, action expected effect, expected observation, expected world/Field change, temporal result, user-visible result or safety condition. Declared expectation, predicted outcome, task completion criterion and desired outcome remain distinct.

Actual Result may reference Runtime Executor, Action, Task, Observation Gateway, Context/Current World, Field State, user confirmation/correction, system event or capability/provider evidence. It carries source, time, validity, uncertainty, contradiction, correction, trace and provenance. It is not automatically external reality truth.

## Comparability Gate

Before deviation, the future owner checks target/entity, attribute/relation, temporal window, spatial scope, schema/units, evidence sufficiency, contradiction, uncertainty, source validity and correction/revocation state. The gate can return `COMPARABLE`, `PARTIALLY_COMPARABLE`, `NOT_COMPARABLE`, `INSUFFICIENT_EVIDENCE`, `STALE_ACTUAL`, `STALE_EXPECTATION`, `CONTESTED` or `NEEDS_CONFIRMATION`.

No forced success/error conclusion is allowed for non-comparable inputs.

## Deviation and Outcome Evaluation

Deviation is structured across semantic, state, value, temporal, spatial, completion, safety, uncertainty, missing-effect, unexpected-side-effect and partial-completion dimensions. Statuses are `MATCH`, `PARTIAL_MATCH`, `MISMATCH`, `UNKNOWN` and `CONTESTED`. There is no single opaque success score.

Outcome Evaluation Candidate answers whether intended outcome, task criterion, action effect and expected world change were observed; whether evidence is sufficient; whether uncertainty remains; and whether observation, confirmation, reconsideration or learning signal candidates are appropriate. It remains `candidate_only=true`, `truth_declared=false`, `mutation_authority=false`.

## Attribution and uncertainty

The taxonomy distinguishes observation error, world-model error, prediction error, decision error, task-planning error, execution error, capability error, temporal-validity error, stale information, external world change, user correction, insufficient evidence and unresolved attribution. Attribution is candidate-only and never declares that a specific owner is wrong.

Multiple causes, competing causes, partial causes, counterevidence and unresolved causes remain concurrently traceable. For example, a navigation outcome can retain stale Field information, insufficient observation and execution deviation candidates together.

## Reconsideration, Learning and Observation feedback

Outcome Evaluation emits candidate recommendations such as `REOBSERVE`, `RECONSIDER_HYPOTHESIS`, `RECONSIDER_DECISION`, `REPLAN_TASK`, `RETRY_EXECUTION`, `REQUEST_USER_CONFIRMATION`, `DEFER`, `FAIL_CYCLE` or `START_NEXT_CYCLE`. A Route Orchestration/Cognitive Flow remains the control authority and existing depth/idempotency guards apply.

Learning receives a Learning Signal Candidate only. It does not execute Learning, mutate parameters, Memory, Personality, Self or Regulation.

When evidence is insufficient or contested, the handoff is an Observation Need Candidate to Field Perception Orchestrator/Active Observation Control. Result Comparison never invokes YOLO/OCR/SLAM directly. Provider availability, frame arrival and Observation Gateway admission do not grant continuation authority.

## Temporal and correction semantics

Immediate effects, delayed effects, windows, stale/expired inputs, early/late results, post-window observations and superseded expectations are distinct. No scheduler-driven mutation is planned.

User correction has high precedence for subsequent candidates but never erases prior evaluation lineage. Corrections produce revised/superseded/revoked evaluation candidates and remain reverse-locatable.

## Trace, provenance and idempotency

Reverse lookup must work from Evaluation to Comparison to Expected Outcome to Decision/Task/Action, and from Evaluation to Actual Result to Runtime/Observation/Current World/Field to Evidence to Provider/User Input. Attribution, Reconsideration and Learning Signal candidates are also linked. Provenance does not grant authority.

Guards cover duplicate result/comparison/evaluation/attribution/reconsideration/learning signal, correction/revocation/supersession replay and mutation of completed evaluation. A completed evaluation is immutable; revision creates lineage.

## Scenario baseline

O01-O36 cover exact match, partial completion, execution failure, missing/stale/contradictory evidence, user confirmation/correction, temporal validity, incomparability, multiple attribution, reconsideration, Learning boundary, idempotency, safety, provider confidence, Observation Gateway admission, no direct provider invocation, A Route next-cycle feedback and all deferred/no-side-effect boundaries.

## A/B/C/D result

A: Runtime result candidates, Cognitive Execution Chain feedback/idempotency/reconsideration.

B: Action Outcome Evaluation contracts, Expectation Feedback contracts, Decision/Task/Action/Observation/Field/Current World references and Cognitive Learning input boundary.

C: Provider-driven success/truth claims and single-score/opaque outcome simplifications that conflict with canonical boundaries.

D: Emotion Engine, Advanced Emotion Governance, B Route, semantic compression, affective memory compression, Personality-memory fusion, cross-user transfer, and real runtime/persistence/model/provider execution in this phase.

## Stop condition

This phase stops after planning assets and static verifier creation. No implementation change is authorized. Final status: `WAITING_FOR_USER_TERMINAL_VERIFICATION`.

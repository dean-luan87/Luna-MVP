# Field State Reducer Controlled Policy Evaluation Technical Planning v1

## Current Work Description

This phase defines technical planning contracts for controlled policy evaluation under Planning Only mode. It does not implement evaluation engine, selection, execution, or mutation.

## Phase Position

Phase-Luna-Field-State-Reducer-Behavior-Policy-Controlled-DryRun-v1-001
-> Phase-Luna-Field-State-Reducer-Behavior-Policy-Controlled-Policy-Evaluation-Technical-Planning-v1-001
-> Phase-Luna-Field-State-Reducer-Controlled-Policy-Evaluation-Controlled-Skeleton-Implementation-v1-001

## Evaluation Layer Positioning

Evaluation is a contract layer that determines candidate eligibility readiness per policy, with deterministic and replayable evidence-based outputs.

## Evaluation vs Selection

Evaluation computes per-policy eligibility status and reasons. Selection chooses among eligible candidates. Evaluation pass is necessary but not sufficient for final selection.

## Evaluation vs Execution

Evaluation does not execute policy functions, does not mutate state, and does not trigger actions. All execution fields remain false.

## Input Contract

Input schema includes policy/state identifiers, admitted events, snapshots, provenance, and locked versions. Runtime/provider/external/model/state-write/action-trigger requests are explicitly false.

## Condition Model

Condition model defines condition types, operators, required inputs, deterministic requirement, and trace behavior. Condition evaluation is candidate-only.

## Evidence Sufficiency

Evidence sufficiency supports statuses: sufficient, insufficient, contradictory, missing_required_source, missing_provenance, stale_evidence, synthetic_only_not_production_fact. No evidence fabrication is allowed.

## Temporal Evaluation

Temporal statuses include: not_yet_valid, active, expiring, expired, suspended, revoked, superseded, unknown. Unknown cannot auto-pass.

## Confidence Evaluation

Confidence planning is state-type specific across 12 state types, with threshold bounds, reliability weighting, diversity treatment, contradiction penalty, temporal decay, and owner-correction treatment. No simple average default and no automatic 100 confidence.

## Conflict Evaluation

Conflict planning preserves unresolved conflicts and forbids winner fabrication. Unresolved conflict keeps policy out of eligible candidate status.

## Owner Correction Evaluation

Owner correction remains governed candidate only and can return governance_review_required when review dependencies are pending.

## Overlay Evaluation

Overlay evaluation is separated from substrate evaluation and does not allow substrate mutation.

## Governance Evaluation

Governance evaluation checks review, admission dependencies, protocol versions, provenance, change control, and runtime boundary constraints. Evaluation has no fact-admission authority.

## Result Contract

Evaluation result includes status, satisfied/unsatisfied/blocked/skipped rules, missing inputs, evidence/temporal/confidence/conflict/governance statuses, rejection reasons, trace reference, replay key, and evaluated versions.

## Rejection Reasons

Rejection reason registry defines contract-level blocking and remediation guidance for unknown policy/state, missing inputs, temporal invalidity, confidence failures, conflict unresolved, governance dependencies, and forbidden external/runtime requests.

## Trace / Replay

Trace records ordered/evaluated rules, short-circuit steps, referenced evidence snapshots, and replay key. Replay contract locks all required snapshots and forbids runtime/provider/external/model dependencies.

## Failure Policy

Any contract drift, missing snapshots, or unresolved blocking conditions yields ineligible/blocked status. No fallback to fabricated eligibility is allowed.

## Non-Goals

- No evaluation engine implementation.
- No operator runtime implementation.
- No real eligibility execution.
- No policy selection.
- No policy execution.
- No precedence/composition execution.
- No confidence calculation execution.
- No conflict resolution execution.
- No active state creation.
- No state mutation/fact promotion/action trigger.
- No provider/external/model/database/scheduler/queue/event-consumer/runtime loop.
- No training/migration/production execution.

## Enough Condition

All required final files are complete, structurally valid, and aligned with planning-only boundaries.

## Stop Condition

After one centralized V0 static check, stop at WAITING_FOR_USER_TERMINAL_VERIFICATION.

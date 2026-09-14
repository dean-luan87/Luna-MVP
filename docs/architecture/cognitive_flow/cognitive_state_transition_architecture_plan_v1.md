# Cognitive State Transition Architecture Plan v1

## Phase

`Phase-Cognitive-State-Transition-Architecture-Planning-v1-001`

## Stage and execution governance

- Stage: Controlled Skeleton Implementation and Controlled DryRun.
- Execution Mode: `Controlled Skeleton Implementation` for code/static checks and `Controlled DryRun` for named synthetic component validation.
- Previous Phase: `Phase-Cognitive-Foundation-Controlled-Execution-v1-001`.
- Previous Phase Decision: `COGNITIVE_FOUNDATION_CONTROLLED_EXECUTION_READY_WITH_NOTES`.
- Verification Authority: V0 agent; V1 agent under the selected controlled modes; V2 user terminal only; V3 ChatGPT only.
- Agent Stop Point: `WAITING_FOR_USER_TERMINAL_VERIFICATION`.

## Position

```text
Retention Candidate -> Activation Candidate -> State Transition Candidate
  -> Next Cognitive Snapshot Candidate -> New Cognitive Tick Candidate
```

This is the A-route Cognitive Runtime Continuity Layer. It preserves candidate continuity and proposes the next cognitive observation window; it is not a fixed State Machine.

## Scope

The layer interprets a current snapshot with new candidates and produces Context, Goal, Attention, Schema, Workspace, Unknown, Hypothesis, and Reasoning Mode Transition Candidates. It can reference retained and activated objects, then provide a Next Cognitive Snapshot Candidate to a future tick.

## Execution boundary

The associated V1 component validation is synthetic-only and deterministic. It tests continuity, replay, and authority boundaries for task continuity, environment change, and error recovery.

## Input assets and target directories

Inputs are `cognitive/contracts/candidate.py`, `cognitive/contracts/signal.py`, `cognitive/contracts/snapshot.py`, `cognitive/runtime/tick.py`, `cognitive/governance/reducer_boundary.py`, the Cognitive Foundation module baseline, and the Retention, Activation, Orchestration, Runtime Environment, and Controlled Execution architecture plans.

Outputs are restricted to `cognitive/runtime/`, `cognitive/validation/`, and `docs/architecture/cognitive_flow/`.

## Required final assets

- `cognitive/runtime/state_transition.py`
- `cognitive/validation/cognitive_state_transition_runner_v1.py`
- `cognitive/validation/cognitive_state_transition_validator_v1.py`
- `cognitive/validation/cognitive_state_transition_trace_schema_v1.json`
- the fifteen architecture documents named by this phase instruction.

## Required checks and negative guards

- V0: required-file, JSON-parse, compilation/import, trace-field, and boundary-contract checks.
- V1: replay task continuity, environment change, and error-recovery synthetic traces.
- no hardcoded pass and no weakened checks;
- no State Machine, real Runtime, Decision, Action, Permission, State/Memory/Experience mutation, B Route Runtime, or Final Phase Verifier execution.

## User terminal reproduction

```bash
PYTHONPATH=. python3 cognitive/validation/cognitive_state_transition_runner_v1.py --scenario task_continuity --output _tmp_eval_out/cognitive_state_transition/task_continuity.json
PYTHONPATH=. python3 cognitive/validation/cognitive_state_transition_runner_v1.py --scenario task_continuity --output _tmp_eval_out/cognitive_state_transition/task_continuity_replay.json
PYTHONPATH=. python3 cognitive/validation/cognitive_state_transition_validator_v1.py --input _tmp_eval_out/cognitive_state_transition/task_continuity.json --replay _tmp_eval_out/cognitive_state_transition/task_continuity_replay.json
```

## Expected outcome and stop condition

Expected success decision: `COGNITIVE_STATE_TRANSITION_ARCHITECTURE_PLANNING_READY_WITH_NOTES`.

Expected failure decision: `BLOCKED_BEFORE_USER_TERMINAL_VERIFICATION`, followed only by a scoped remediation phase.

Stop after V0/V1 evidence is recorded. No Final Phase Verifier or GO declaration is authorized.

## Exclusions

No State Machine, real Runtime, Decision, Action, Permission, Reality mutation, Memory mutation, Learning, Evolution, World Model, Simulation Engine, Emotion, Hive, or B Route Runtime.

`final_candidate_decision: COGNITIVE_STATE_TRANSITION_ARCHITECTURE_PLANNING_READY_WITH_NOTES`

`status: WAITING_FOR_USER_TERMINAL_VERIFICATION`

# Cognitive Foundation Skeleton Implementation Plan v1

## Phase contract

- Phase: `Phase-Cognitive-Foundation-Skeleton-Implementation-v1-001`
- Stage: Controlled Skeleton Implementation
- Execution Mode: Controlled Skeleton Implementation
- Previous Phase: `Phase-Cognitive-Foundation-Closure-Architecture-Review-v1-001`
- Previous Phase Decision: `COGNITIVE_FOUNDATION_CLOSURE_ARCHITECTURE_REVIEW_READY_WITH_NOTES`

## In scope

Implement and validate immutable Candidate, Signal, Snapshot, Tick, and candidate-only Reducer Boundary Adapter contracts. The V1 runner is synthetic-only and validates one `FieldChangedEvent -> CognitiveTick -> Candidate -> Signal -> Snapshot` contract path.

## Required final files

- `cognitive/contracts/candidate.py`
- `cognitive/contracts/signal.py`
- `cognitive/contracts/snapshot.py`
- `cognitive/runtime/tick.py`
- `cognitive/governance/reducer_boundary.py`
- `cognitive/validation/run_cognitive_foundation_skeleton_controlled_v1.py`
- `cognitive/validation/verify_cognitive_foundation_skeleton_controlled_result_v1.py`
- `docs/architecture/cognitive_flow/cognitive_foundation_skeleton_module_baseline_v1.md`
- `docs/architecture/cognitive_flow/cognitive_foundation_skeleton_go_no_go_v1.md`

## Out of scope

No real Runtime/scheduler, Field integration, Reducer modification, Decision Engine, Action, permission, model invocation, external network, memory write, learning, evolution, Emotion, World Model, Language, or trace-product implementation.

## Verification authority

- V0: Agent may run file, import, and compile checks.
- V1: Agent may run only `python3 -m cognitive.validation.run_cognitive_foundation_skeleton_controlled_v1` and its result verifier with a synthetic output path.
- V2: User Terminal only; no final phase verifier is created or run by Agent in this skeleton phase.
- V3: ChatGPT only.

## Negative guards

- Candidate != Fact, Decision, Action, Permission, or State mutation.
- Signal != direct module call, command, or executor request.
- Snapshot != Field State or Reducer State.
- Tick != scheduler, Runtime loop, or State transition.
- CandidateOnlyEmitter != Reducer and exposes no State mutation operation.
- Synthetic validation != production/runtime validation.

## Agent stop point

After V0 and the explicitly authorized V1 controlled validation, stop at `WAITING_FOR_USER_TERMINAL_VERIFICATION`. Neither check grants GO.

## Reproducible controlled validation commands

```bash
python3 -m cognitive.validation.run_cognitive_foundation_skeleton_controlled_v1 --output _tmp_eval_out/cognitive_foundation_skeleton_controlled_v1/result.json
python3 -m cognitive.validation.verify_cognitive_foundation_skeleton_controlled_result_v1 --input _tmp_eval_out/cognitive_foundation_skeleton_controlled_v1/result.json
```

These commands are synthetic V1 component validation only. They are not a V2 Final Phase Verifier and cannot grant GO.

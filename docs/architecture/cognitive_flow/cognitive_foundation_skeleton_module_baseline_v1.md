# Cognitive Foundation Skeleton Module Baseline v1

## Baseline scope

The first Cognitive Foundation code baseline is deliberately isolated at repository root `cognitive/`. Existing `runtime/`, Field Kernel, Reducer, Decision, Action, Model Manager, diagnostics, and capability modules remain outside this baseline.

## Baseline assets

- `cognitive/contracts/candidate.py`: immutable Candidate contract.
- `cognitive/contracts/signal.py`: decoupled CognitiveSignal contract.
- `cognitive/contracts/snapshot.py`: shared immutable CognitiveSnapshot view.
- `cognitive/runtime/tick.py`: event-to-tick contract only.
- `cognitive/governance/reducer_boundary.py`: candidate-only emission boundary.
- `cognitive/validation/`: synthetic-only controlled runner and result verifier.
- `cognitive/validation/run_cognitive_foundation_mock_loop_dryrun_v1.py`: synthetic complete-loop dry-run.
- `cognitive/validation/cognitive_trace_schema_v1.json` and `cognitive_trace_validator_v1.py`: controlled trace/replay contract.
- `cognitive/validation/cognitive_dynamic_loop_runner_v1.py` and `cognitive_dynamic_loop_validator_v1.py`: synthetic dynamic-loop and replay validation.
- `cognitive/runtime/controlled_execution.py`: deterministic, synthetic-only controlled execution skeleton; no scheduler, Decision, Action, or State mutation capability.
- `cognitive/validation/cognitive_execution_runner_v1.py`, `cognitive_execution_validator_v1.py`, and `cognitive_execution_failure_injection_v1.py`: controlled trace, replay, and six-case failure-attribution validation.
- `cognitive/validation/cognitive_execution_trace_schema_v1.json`: execution-trace contract for the controlled skeleton.
- `cognitive/runtime/state_transition.py`: deterministic, synthetic snapshot-continuity skeleton; not a State Machine or persistent state owner.
- `cognitive/validation/cognitive_state_transition_runner_v1.py`, `cognitive_state_transition_validator_v1.py`, and `cognitive_state_transition_trace_schema_v1.json`: synthetic continuous-transition trace, replay, and boundary validation.
- `cognitive/kernel/`: Candidate-only Kernel skeleton producing constraint, consistency, and arbitration candidates; no decision, execution, or State authority.
- `cognitive/attention/`: Candidate-only Attention Controller skeleton producing allocation candidates; no sensor, model, or module invocation.
- `cognitive/process/`: Candidate-only Process Composer skeleton producing bounded cognitive process candidates; no planner or executor.
- `cognitive/organization/organization.py`: deterministic synthetic organization loop that composes Kernel, Attention, Process, and Runtime Instance candidates without becoming a scheduler.
- `cognitive/runtime/instance.py`: immutable Runtime Instance Record exposed as a candidate; not persistent State or a runtime executor.
- `cognitive/validation/run_cognitive_kernel_skeleton_v1.py` and `verify_cognitive_kernel_skeleton_v1.py`: controlled synthetic Airport Navigation trace/replay validation for the extension.
- `cognitive/validation/cognitive_stress_validation_runner_v1.py`, `cognitive_stress_validation_validator_v1.py`, and five `cognitive_*_scenario_v1.json` fixtures: synthetic governance stress validation for attention conflict, Kernel arbitration, multi-process isolation, interrupt recovery/lifecycle, and failure attribution.
- `cognitive/evidence/`: immutable synthetic EvidenceCandidate and Evidence Admission skeletons; evidence cannot confirm truth or mutate State.
- `cognitive/adapters/`: synthetic Visual, Language, and Audio adapters that only emit Evidence Candidates.
- `cognitive/validation/run_cognitive_real_input_skeleton_v1.py`, `verify_cognitive_real_input_skeleton_v1.py`, and `cognitive_real_input_skeleton_scenario_v1.json`: controlled synthetic Evidence -> Input Attention -> Admission -> Cognitive Skeleton trace/replay validation.

## Non-goals

This baseline contains no scheduler, Runtime loop, model call, Field adapter, Decision Engine, Action executor, memory/evolution implementation, production trace product, or State mutation route. Its controlled trace is synthetic-only diagnostic output. Kernel, Attention, Process, Organization, and Runtime Instance components are controlled candidate skeletons only, not runtime services. It must be read before later Cognitive Foundation skeleton work unless exceptional recalibration is required.

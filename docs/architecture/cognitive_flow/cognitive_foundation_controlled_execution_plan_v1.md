# Cognitive Foundation Controlled Execution Plan v1

## Phase

`Phase-Cognitive-Foundation-Controlled-Execution-v1-001`

## Stage

Controlled Skeleton Implementation and V1 Controlled Component Validation.

## Execution Mode

`Controlled Skeleton Implementation` for implementation and static checks; `Controlled DryRun` for the explicitly scoped synthetic runner and result validator.

## Current Work Description

Implement a deterministic, synthetic-only A-route cognitive-flow skeleton that emits immutable Candidates, records a Cognitive Execution Trace, supports replay, and attributes six injected failures. It has no external capability, real Runtime, Decision, Action, Memory, or State mutation path.

## Previous Phase

`Phase-Cognitive-Foundation-Integration-Validation-v1-001`

## Previous Phase Decision

`COGNITIVE_FOUNDATION_INTEGRATION_VALIDATION_READY_WITH_NOTES`

## Input Assets

- `cognitive/contracts/candidate.py`
- `cognitive/contracts/signal.py`
- `cognitive/contracts/snapshot.py`
- `cognitive/runtime/tick.py`
- `cognitive/governance/reducer_boundary.py`
- `docs/architecture/cognitive_flow/cognitive_foundation_integration_validation_plan_v1.md`
- `docs/architecture/cognitive_flow/cognitive_foundation_integration_boundary_contract_v1.md`
- `docs/architecture/cognitive_flow/cognitive_foundation_skeleton_module_baseline_v1.md`

## Required Pre-Read

The repository governance assets named in `AGENTS.md`, the module baseline above, and the input contracts above.

## Target Directory

- `cognitive/runtime/`
- `cognitive/validation/`
- `docs/architecture/cognitive_flow/`

## Scope

```text
Synthetic Input -> Candidate Flow -> Cognitive Execution Trace -> Validation
```

The execution path is: synthetic event, perception, information field, representation, schema, attention, workspace, simulation, operation, evaluation, outcome observation, and feedback.

## Out Of Scope

Camera, OCR, SLAM, LLM, external model, real input, Scheduler, real Runtime, B-route execution, Decision, Action, Memory/Hive/Emotion, automatic Learning, Genome/Culture change, and State mutation.

## Implementation Principles

- Candidate First and immutable contracts;
- Reality First: synthetic representations cannot alter Reality;
- Minimum Sufficient execution: deterministic, bounded scenarios only;
- B interface may be represented but must not execute;
- minimal, isolated additions to the established `cognitive/` baseline.

## Required Final Files

- `cognitive/runtime/controlled_execution.py`
- `cognitive/validation/cognitive_execution_trace_schema_v1.json`
- `cognitive/validation/cognitive_execution_runner_v1.py`
- `cognitive/validation/cognitive_execution_validator_v1.py`
- `cognitive/validation/cognitive_execution_failure_injection_v1.py`
- `docs/architecture/cognitive_flow/cognitive_execution_runtime_skeleton_v1.md`
- `docs/architecture/cognitive_flow/cognitive_execution_replay_model_v1.md`
- `docs/architecture/cognitive_flow/cognitive_execution_boundary_contract_v1.md`
- `docs/architecture/cognitive_flow/cognitive_execution_go_no_go_v1.md`

## Required Checks

- V0: file existence, JSON parse, Python compilation, import, static boundary checks.
- V1: familiar fast-loop execution/replay, uncertain B-interface-only execution/replay, six-case failure injection, and deterministic result validation.
- V2: user terminal only; no V2 final phase verifier is created or run in this phase.
- V3: ChatGPT only after any user-terminal V2 verification.

## Negative Guards

- no check weakening or hardcoded pass;
- no Observation -> Decision -> Action shortcut;
- no mutation of Reality, Reducer State, Memory, Genome, or Culture;
- no B Route execution;
- no Final Phase Verifier execution by the agent.

## Verification Authority

V0: agent. V1: agent under the selected controlled modes. V2: user terminal only. V3: ChatGPT only.

## Allowed Agent Checks

Static checks plus the named synthetic component runner, validator, and failure-injection runner.

## Allowed Agent Execution

Synthetic candidate-trace execution only; no real Runtime execution.

## Prohibited Agent Execution

Final phase verification, real Runtime, model/device/network/database execution, State mutation, Decision execution, Action execution, and automatic learning.

## Agent Stop Point

`WAITING_FOR_USER_TERMINAL_VERIFICATION`

## User Terminal Commands

```bash
PYTHONPYCACHEPREFIX=_tmp_eval_out/pycache python3 -m py_compile cognitive/runtime/controlled_execution.py cognitive/validation/cognitive_execution_runner_v1.py cognitive/validation/cognitive_execution_validator_v1.py cognitive/validation/cognitive_execution_failure_injection_v1.py
PYTHONPATH=. python3 cognitive/validation/cognitive_execution_runner_v1.py --scenario familiar --output _tmp_eval_out/cognitive_execution/familiar.json
PYTHONPATH=. python3 cognitive/validation/cognitive_execution_runner_v1.py --scenario familiar --output _tmp_eval_out/cognitive_execution/familiar_replay.json
PYTHONPATH=. python3 cognitive/validation/cognitive_execution_validator_v1.py --input _tmp_eval_out/cognitive_execution/familiar.json --replay _tmp_eval_out/cognitive_execution/familiar_replay.json
```

## Expected Success Decision

`COGNITIVE_FOUNDATION_CONTROLLED_EXECUTION_READY_WITH_NOTES`

## Expected Next

`WAITING_FOR_USER_TERMINAL_VERIFICATION`

## Expected Failure Decision

`BLOCKED_BEFORE_USER_TERMINAL_VERIFICATION`

## Expected Failure Next

`Phase-Cognitive-Foundation-Controlled-Execution-Remediation-v1-001`

## Stop Condition

Stop after V0/V1 component evidence is recorded. Do not declare GO.

## Blocker Conditions

Missing candidate-only boundary, non-deterministic replay, failed failure attribution, attempted state/action mutation, B-route execution, or unavailable controlled validation assets.

## Completion Report Format

Report changed files, V0/V1 evidence, blocker_count, warning_count, final candidate decision, and user-terminal status.

## Current Status Contract

`WAITING_FOR_USER_TERMINAL_VERIFICATION`

# Luna Cognitive Architecture Reassessment — Code Inventory v1

## Scope and execution mode

- Phase: `Phase-Cognitive-Architecture-Reassessment-Code-Inventory-v1-001`
- Execution mode: Audit / V0 read-only.
- Scope: repository assets reachable from `cognitive/`, `capabilities/`, `runtime/`, `validation/`, `whitebox/`, `frontend/`, `backend/`, `tools/`, and `docs/`.
- Exclusions: no source modification, module creation, protocol change, model invocation, runtime execution, or directory refactor occurred.

## Top-level inventory

| Requested scope | Resolved location | Observed structure | Assessment |
|---|---|---|---|
| `cognitive/` | workspace-local | 48 Python files: contracts, governance, runtime records, kernel, attention, organization, process, evidence/adapters, validation | A-route controlled skeleton is present. |
| `capabilities/` | symlink to `Luna-Core/capabilities` | 6,412 files; 3,372 Python files | Large legacy/midplatform/capability estate; mixed planning, dry-run, and limited execution assets. |
| `runtime/` | symlink to `Luna-Core/runtime` | 10 Python files | Legacy/sibling operational runtime, separate from `cognitive/runtime/`. |
| `validation/` | no top-level directory | Validation is distributed under `cognitive/validation/`, `tools/evaluation/`, and capability test boards | Do not create a second validation root before an approved migration. |
| `whitebox/` | no top-level directory | Main assets live under `capabilities/midplatform/model_test_lens/` | Existing Model Test Lens is the practical whitebox base. |
| `frontend/` | no top-level directory | Static web UI is under Model Test Lens | No canonical frontend root found. |
| `backend/` | no top-level directory | Local runner bridge and Python services are capability-local | No canonical backend root found. |
| `tools/` | symlink to `Luna-Core/tools` | 2,359 files; 2,280 Python files | Evaluation, runner, verification, and engineering tools. |
| `docs/` | symlink to `Luna-Core/docs` | 4,890 files | Architecture, governance, phase records, and verification assets. |

## Existing A-route code baseline

| A-route concern | Code location | Current state | Boundary observed |
|---|---|---|---|
| Candidate contract | `cognitive/contracts/candidate.py` | Present | Immutable, candidate-only structure; documented as neither fact, command, decision, permission, action, memory, nor State mutation. |
| Signal contract | `cognitive/contracts/signal.py` | Present | Immutable signal envelope with source, target, context, provenance, confidence, and trace. |
| Snapshot contract | `cognitive/contracts/snapshot.py` | Present | Current cognitive view only; not persistent State. |
| Event tick | `cognitive/runtime/tick.py` | Present | Trigger enum is field, goal, risk, and information-gap driven. |
| Reducer boundary | `cognitive/governance/reducer_boundary.py` | Present | Candidate-only emitter rejects requested State mutation. |
| Evidence / adapter skeleton | `cognitive/evidence/`, `cognitive/adapters/` | Present | Synthetic-only evidence and adapters; no truth confirmation or external invocation. |
| Kernel | `cognitive/kernel/` | Present | Emits constraint, consistency, and arbitration candidates only. |
| Attention controller | `cognitive/attention/` | Present | Produces bounded allocation candidates only; no sensor/model invocation. |
| Organization / process | `cognitive/organization/`, `cognitive/process/` | Present | Deterministic synthetic composition; explicitly not scheduler or executor. |
| Runtime instance | `cognitive/runtime/instance.py` | Present | Immutable temporary record, exposed as a candidate; not State or executor. |
| Trace, replay, stress validation | `cognitive/validation/` | Present | Synthetic controlled traces, validators, stress fixtures, and replay checks. |

## Legacy/sibling runtime finding

`runtime/main_loop.py` is materially different from the new cognitive skeleton. It uses a fixed 100 ms `while` loop, calls `c.controller.decide`, then creates an execution intent through `execution.c_veto_adapter.apply_c_veto`. This is an operational decision/execution chain. It must remain isolated from the event-driven, Candidate-only A-route skeleton unless a future approved migration explicitly introduces an execution boundary adapter.

## Structural conclusion

The repository can host the A-route skeleton today, but it contains parallel architectural generations. The root `cognitive/` package is the only inspected area that already enforces the intended Candidate-only controlled-skeleton boundary. Existing `capabilities/` and `runtime/` assets should be treated as sources of perception capability, policy, diagnostics, or migration candidates—not as implicit Cognitive Foundation authorities.

**Current inventory status: `MIGRATE` (architecture mapping required before any live integration).**

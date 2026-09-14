# Negative Guards

The Runner exercises exactly two Action Governance safety negatives using the
existing canonical synthetic fixtures:

| Fixture | Canonical input | Expected result | Runtime Executor |
| --- | --- | --- | --- |
| `action_without_permission` | `A03_PERMISSION_REVOKED_TO_BLOCKED` | `NEEDS_PERMISSION`, `blocked`, not execution-eligible | Not invoked |
| `action_fails_safety` | `A04_SAFETY_VETO_TO_BLOCKED` | `BLOCKED`, `blocked`, not execution-eligible | Not invoked |

The negative path still produces a candidate-only governance output where the
canonical Action engine does so, but it is not admitted as execution-eligible.
It does not bypass permission/safety validation.

The verifier also requires all of these to remain false:

`real_action_execution`, `device_control`, `runtime_dispatch_executed`,
Task/Decision/Brain/Cognitive-State-Formation Action execution,
model/provider invocation, live observation, Field/Memory/Experience/Learning
mutation, and World Truth declaration.


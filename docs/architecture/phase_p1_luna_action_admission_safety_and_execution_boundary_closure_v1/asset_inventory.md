# Asset Inventory

## Reused canonical assets

| Asset | Classification | Use |
| --- | --- | --- |
| `action_governance_engine_v1.py` | Canonical implementation | Forms Action Candidate, validates permission/safety inputs, derives state/readiness, and emits candidate-only handoffs. |
| `action_io_types_v1.py` | Canonical contract | `ActionGovernanceInputV1` and `ActionGovernanceOutputV1`. |
| `action_core_types_v1.py` | Canonical contract | `ActionCandidateV1` and read-only `SourceRefV1`. |
| `action_permission_safety_types_v1.py` | Canonical contract | Permission/safety status vocabulary and recheck semantics. |
| `action_readiness_types_v1.py` | Canonical contract | `ExecutionReadinessCandidateV1`; readiness is not execution. |
| `action_handoff_types_v1.py` | Canonical contract | `ActionToRuntimeExecutorHandoffCandidateV1`. |
| `action_static_validators_v1.py` | Canonical validators | Candidate, trace, handoff, ownership, and no-side-effect checks. |
| `task_to_action_boundary_controlled_handoff` | Verified integration | Supplies the valid planned Task, Decision provenance, Action request, and positive Case A/Case B results. |
| Runtime Executor controlled contracts | Canonical downstream boundary | Consumer identity and candidate-only handoff semantics; Runtime Executor is not invoked. |

No missing canonical Action Governance or Runtime Executor implementation was
worked around, and no parallel Action Manager was created.

The reused `ActionGovernanceInputV1` has no separately named risk-reference
field. The integration therefore preserves the canonical `safety_valid` gate,
precondition/dependency constraints, and resource state, while reporting a
separate risk signal as `NOT_INSTRUMENTED` rather than fabricating risk refs.

# Luna Governance Execution Context Design v1

## Position

`CapabilityExecutionContext` is a future governance-injection design for a Capability execution request. It does not execute, authorize, register, persist, or mutate. It is not a Python type, token, Runtime object, Registry record, or Permission Engine implementation.

## Planned Fields

| field | purpose | boundary |
| --- | --- | --- |
| `capability_id` | governed Capability identity | Capability cannot supply self-authorizing identity |
| `protocol_version` | selected compatible protocol version | must remain L0/L1 compatible; no local override |
| `permission_scope` | existing Permission/Admission reference and bounded scope | reference only, never a permission grant |
| `input_contract` | required input Contract identity/version | requires evidence/context/provenance/trace as applicable |
| `output_contract` | declared candidate output Contract identity/version | cannot allow Fact, Decision, Action, State, or Memory by implication |
| `trace_requirement` | required traceability lineage | cannot be removed, replaced, or silently completed |
| `denied_operations` | explicit forbidden operations | Capability cannot weaken or remove entries |

## Governance Decision Flow

```text
Capability Request
        ↓
Governance Evaluation
  Constitution compatibility
  → Protocol compatibility
  → Permission/Admission eligibility
  → Registry/lifecycle reference
        ↓
CapabilityExecutionContext (reference-only plan)
        ↓
Capability Execution (future, separately authorized)
        ↓
Output Validation
  Contract + provenance + trace + candidate boundary + diagnostics
```

## A3 Example Boundaries

For Translation, `denied_operations` includes Fact creation, Decision/Action generation, Context/Snapshot/Field State/Memory mutation, Model/Network/Database invocation, and Runtime activation. For Cognitive Analysis, it additionally preserves Reducer-only State authority and separate Decision/learning handoff governance.

## Design Limits

This plan does not define evaluation algorithms, a permission engine, a protocol manager, a registry writer, diagnostics runtime, Capability adapter, or real execution behavior.


# Luna Capability Contextual Governance v1

## Principle

Capability availability is not determined by Capability lifecycle alone. A lifecycle marker describes governance standing; actual future use also depends on contextual evaluation and a separately authorized Capability Execution Context.

## Contextual Inputs

| factor | governance question | boundary |
| --- | --- | --- |
| Context | is the supplied context reference compatible, traceable, and within declared scope? | no raw State/Snapshot write handle |
| Task | does the declared task/question fit the Capability purpose and output Contract? | no Decision/Action command substitution |
| Risk | is the requested use within tolerated boundary, provenance, and failure constraints? | high risk cannot weaken L0/L1 restrictions |
| User requirement | is the requested behavior explicit, governed, and consistent with output/consumer boundaries? | user request cannot grant prohibited authority |
| Permission scope | does an existing Permission/Admission reference permit this bounded request? | reference is not self-issued or inferred from Active state |

## Contextual Decision Shape

```text
Capability Standing
        + Context + Task + Risk + User Requirement + Permission Scope
        ↓
Governance Evaluation (future)
        ↓
bounded CapabilityExecutionContext or explicit denial/defer
```

This is not an evaluation engine. It does not score users, execute a Capability, or authorize Runtime. An `Active` Capability may still be unavailable, limited, deferred, or denied for a given context.

## Capability Boundary

Capabilities own transformation and candidate generation within a granted future context. They do not own Permission, Protocol change, State authority, Decision authority, lifecycle transition, or contextual eligibility evaluation. Contextual governance must preserve uncertainty, provenance, trace, Contract references, and denied operations.


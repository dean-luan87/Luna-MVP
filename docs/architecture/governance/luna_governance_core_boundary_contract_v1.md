# Luna Governance Core Boundary Contract v1

## Capability Boundary

A Capability may only perform its declared business transformation within a governed execution scope. For example, Translation may normalize references and emit a Cognitive Primitive Candidate. A Capability may not decide its own permission, elevate Evidence to Fact, admit itself to a lifecycle, grant consumer access, replace provenance, or write Field State.

## Governance Boundary

Governance owns:

- whether a Capability is eligible to execute;
- whether input Contract, references, trace, provenance, and permission context are valid;
- whether output stays inside its declared Candidate/Fact and authority boundary;
- Capability lifecycle and Registry ownership;
- admission eligibility for future handoff, without conflating eligibility with activation;
- boundary diagnostics, Contract drift, and verification evidence.

Governance does not perform domain transformation, create semantic conclusions, become a model, or mutate a Field State on behalf of a Capability.

## Future Capability Execution Context

Before any future controlled Capability execution, Governance may supply a reference-only `CapabilityExecutionContext` with:

| field | governance meaning | boundary |
| --- | --- | --- |
| `capability_ref` | registered/candidate capability identity | no activation implied |
| `contract_refs` | required L0/L1 contract identities and versions | no parallel contract |
| `permission_ref` | existing Permission/Admission request reference | not a permission grant |
| `input_admission_ref` | input eligibility evidence | no raw data replacement |
| `trace_ref` | governed trace lineage | must remain visible |
| `provenance_refs` | producer/source lineage | cannot be removed or converted to Fact |
| `lifecycle_ref` | Registry-owned lifecycle reference | Capability cannot self-promote |
| `diagnostics_ref` | Protocol Manager / Permission diagnostics binding | no private diagnostic authority |
| `boundary_flags` | declared forbidden operations | cannot be overridden by Capability |

This is a planning shape only. It is not a Python type, Runtime input, database record, Registry write, permission token, or execution authorization.

## Non-Negotiable A3 Boundary

For Translation and Cognitive Analysis, outputs remain candidates; Fact, Decision, Action, State, Context/Snapshot, Memory, Learning admission, model invocation, external calls, and Runtime activation require separate governance and are not permitted by this contract.


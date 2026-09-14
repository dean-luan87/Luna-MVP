# Luna Governance Authority Matrix v1

| authority layer | owns | allows | denies | cannot override |
| --- | --- | --- | --- | --- |
| L0 Constitution | immutable cognitive and authority principles | only constitution-compatible governance | Fact/Decision/Action/State/Memory shortcuts; mutation-authority bypass | specific admission decision, Registry record, Capability result |
| L1 Protocol Governance | Contract identity/version, I/O symmetry, traceability, Guard inventory | contract-compatible Capability route | schema drift, trace loss, undeclared output, private protocol | L0, denied admission, Registry lifecycle, domain semantics |
| L1 Permission / Admission | eligibility and permission-scope references | bounded request and future handoff eligibility | self-grant, consumer overreach, ungoverned input/output | L0/L1 Protocol, Registry lifecycle, Reducer authority |
| L1 Capability Registry | identity, owner, lifecycle, dependencies | governed discoverability/lifecycle eligibility | duplicate/self-promoted/undeclared Capability | L0, Protocol, Permission/Admission, Capability domain authority |
| L1 Diagnostics | drift, validation, violation, lifecycle evidence | reviewable governance visibility | silent failure through required diagnostics | any decision or permission grant |
| Capability | declared business transformation, computation, candidate output | transform/compute/generate candidate only | N/A — it must reject operations outside its Contract | any Governance layer or Reducer mutation authority |

## Capability Authority Boundary

A Capability may transform governed inputs, compute within its declared Contract, and generate a candidate output with required provenance and trace. It may not grant permission, modify a Protocol, bypass Admission, write State, redefine a Contract, alter Registry lifecycle, promote Fact, execute Decision/Action, or erase uncertainty/provenance.


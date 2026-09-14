# Capability Selection Boundary v1

## Requirement-to-capability boundary

The Cognitive Field emits an `Observation Requirement`, not an implementation
command. The Capability Registry maps the information need to a
`Capability Candidate` by contract:

```text
Observation Requirement
    ↓
Capability Registry
    ↓
Capability Candidate
    ↓
Capability Admission
```

The requirement may ask for Object Evidence, Text Evidence, Spatial Evidence,
Audio Evidence, or Human Feedback. It must remain provider-neutral. It must not
say `call YOLO`, `call OCR`, `call SLAM`, or invoke a hardware API.

## Admission constraints

Admission checks capability type, input contract, output Evidence Contract,
confidence boundary, limitation, resource requirement, provenance, failure
namespace, and authority scope. A capability may provide Evidence only.

It cannot:

- create a Field;
- interpret Reality;
- modify Reality State;
- modify Self, Goal, or Intent;
- create a Decision;
- trigger Action.

Capability selection is a governance candidate. It is not a Decision and not
an automatic Provider execution.

## Replacement boundary

Multiple Providers may satisfy one capability. Provider Replacement means
replacing Provider A with Provider B and must preserve the Observation
Requirement and all cognitive
interfaces. Only Evidence Quality Candidate, confidence, resource profile, or
failure diagnostics may differ.

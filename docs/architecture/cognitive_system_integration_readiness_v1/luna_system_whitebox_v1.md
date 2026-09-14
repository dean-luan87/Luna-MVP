# Luna System Integration Whitebox v1

```text
External World
    ↓ Evidence
Reality Workspace / Reducer
    ↓
Cognitive Field
    ↓
Attention Global Bus
    ↓
Situation + Goal / Task Check
    ↓
A Route Option / Decision Candidate
    ↓
Brain Review
    ↓
Action Boundary / Outcome Evidence
    ↓
Experience Candidate / Future Adaptation
```

## Control questions

- Who creates a Field? Brain Intent, Neural Detection, User Request, or
  External Event through Field Admission; never a Provider.
- Who creates a Capability Requirement? Attention/Observation Governance and
  Field or Task context; never a Model.
- Who approves activation? Governance Admission and Authority boundaries.
- Who modifies Reality? Only the Reality Reducer after Evidence Gateway
  validation; no Model, Provider, Field, Runtime, or Brain direct write.
- Who owns Goal and final Decision? Brain.
- Who allocates finite resources? Attention and Resource Governance candidates.
- Who observes health? Diagnostics, producing Diagnostic Candidate.
- Who may revoke? Authority and Governance processes, not a Provider.

## Separation invariants

Capability → Model / Hardware → Evidence remains the only external capability
direction. Evidence → Reality Update → Field Update → Attention → Situation is
the return direction. Model → Decision, Model → Goal, Model → Action, Provider →
Brain, and Runtime → Judgment paths are forbidden.

## Boundary status

This whitebox is a Planning Only architecture artifact. It does not implement
Runtime, Scheduler, Model, Hardware, Camera, OCR, SLAM, Action, Emotion,
Social, or B behavior.

Provider → Brain is forbidden. No Runtime, No Scheduler, No Model, No Hardware,
No Camera, No OCR, No SLAM, No Action, No Emotion, No Social, and No B are
implemented.

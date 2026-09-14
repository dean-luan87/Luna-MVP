# Observation Cycle Whitebox v1

```text
Cognitive Field
      ↓
Observation Requirement
      ↓
Created → Qualified → Allocated
      ↓
Executing Candidate
      ↓
Evidence Received
      ↓
Evaluated
      ↓
Completed / Suspended
      ↓
Reality Update Candidate
      ↓
Field Reassessment
```

Priority and budget side path:

```text
Survival / Goal / Uncertainty / Information Value / Resource Cost
      ↓
Observation Priority Candidate
      ↓
Observation Budget
      ↓
Allocation Candidate
```

Failure side path:

```text
Capability Failure
      ↓
Evidence Quality Decline
      ↓
Observation Retry Candidate
      ↓
Alternative Capability Candidate
```

The whitebox preserves `Observation Requirement ≠ Observation Execution`,
`Reducer remains the sole State mutation authority`, and the boundary that no
observation directly creates a Decision or Action. No Camera, No OCR, No SLAM,
and No Hardware are present; no real model runtime is present.

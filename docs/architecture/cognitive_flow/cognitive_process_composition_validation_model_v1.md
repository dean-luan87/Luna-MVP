# Cognitive Process Composition Validation Model v1

## Purpose

Process validation verifies whether a Cognitive Process Candidate is coherent enough to enter future runtime admission. It does not execute that process.

## Lifecycle

```text
Process Candidate Generation
  -> Process Validation
  -> Process Admission Candidate
  -> Runtime Execution Candidate
  -> Outcome Observation Candidate
  -> Feedback Candidate
```

`Runtime Execution Candidate` is a future-runtime handoff representation only; it must not cause real execution in this planning phase.

## Validation dimensions

- goal consistency;
- context consistency;
- evidence/reality consistency;
- attention allocation consistency;
- capability applicability;
- resource-budget compatibility;
- safety, uncertainty, and recovery boundaries.

## Outputs

- Validated Process Candidate;
- Adjustment Candidate;
- Deferral Candidate;
- Rejection Candidate;
- Future Runtime Admission Candidate.

## Boundary

Validation cannot make the process true, invoke a capability, call a model, activate a sensor, decide an option, or mutate State.


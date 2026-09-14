# Cognitive Interrupt Candidate Model v1

## Definition

An Interrupt Candidate signals that current cognitive allocation may need review because new information has higher urgency, risk, conflict, or survival relevance.

## Sources

- Constitution / Survival Candidate;
- Risk Increase Candidate;
- Unexpected Evidence Candidate;
- Candidate Conflict Candidate;
- Self State Degradation Candidate;
- Attention Expiration Candidate.

## Flow

```text
Current Cognition Candidate
  -> Interrupt Candidate
  -> Attention Arbitration Candidate
  -> Reallocation / Continue / Defer Candidate
```

## Required fields

- source and provenance;
- affected cognitive process or workspace reference;
- urgency, risk, uncertainty, and expected value;
- requested scope/depth/duration;
- conflict and recovery references.

## Frozen boundaries

Interrupt is not Action. Interrupt is not Decision. Interrupt is not an unconditional attention override. It asks Attention Governance to arbitrate; it cannot execute a module, control a device, or mutate State.


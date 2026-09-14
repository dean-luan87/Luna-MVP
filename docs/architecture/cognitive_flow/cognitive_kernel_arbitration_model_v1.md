# Cognitive Kernel Arbitration Model v1

## Definition

Kernel arbitration organizes conflicts across candidate sources without becoming a decision maker or controller override.

## Supported conflict classes

- Attention Conflict;
- Capability Conflict;
- Resource Conflict;
- Goal Conflict;
- Evidence / Experience Consistency Conflict;
- Interrupt Scope Conflict.

## Arbitration flow

```text
Conflicting Candidates
  -> Kernel Arbitration Candidate
  -> Attention Governance / Organization Evaluation
  -> Adjustment, Deferral, or Admission Candidate
```

## Arbitration basis

- Survival and safety boundary;
- current evidence scope and reliability;
- active context and goal relevance;
- resource budget and reliability constraint;
- uncertainty and reversibility;
- candidate provenance and expiry.

## Boundary

Arbitration proposes an ordered, constrained candidate view. It cannot choose an action, force an allocation, invoke a capability, modify State, or override the Reducer.


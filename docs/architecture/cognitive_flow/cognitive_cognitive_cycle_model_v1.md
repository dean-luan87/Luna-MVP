# Cognitive Cognitive Cycle Model v1

## Definition

A Cognitive Cycle is an event-driven, bounded candidate-processing interval. It is not a fixed timer loop, a scheduler time slice, or a guarantee that every cognitive capability runs.

## Trigger candidates

- New Evidence Candidate;
- Context Change Candidate;
- Goal Change Candidate;
- Risk Change Candidate;
- Unknown Increase Candidate;
- Self State Change Candidate;
- Attention Expiration Candidate.

Each trigger may produce a `Cognitive Tick Candidate`. Trigger admission remains subject to Attention Governance and resource constraints.

## Cycle model

```text
Trigger Candidate
  -> Cognitive Tick Candidate
  -> Attention Candidate Pool
  -> Attention Governance
  -> Allocation / Composition / Modulation Candidates
  -> Workspace Formation Candidate
  -> Cognitive Process Execution Candidate
  -> Outcome Observation Candidate
  -> Feedback Candidate
  -> Attention Evolution Candidate
```

## Required properties

- A tick records provenance, context scope, uncertainty, and candidate boundaries.
- A tick can be deferred, narrowed, interrupted, or closed by candidates.
- A tick does not assert reality, decide a choice, invoke a model, or execute an action.
- No fixed frequency is implied. An absence of meaningful triggers may produce no tick.

## Fast and slow relationship

Fast cycles organize current evidence and cognitive candidates. Slow feedback/evolution remains separate and can only produce future adjustment candidates after validation. A single tick cannot mutate Experience, Genome, Culture, or persistent State.


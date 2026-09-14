# Cognitive Runtime Cycle Architecture Plan v1

## Purpose

This Planning Only Runtime Mental Model defines how a future Luna cognitive cycle may be organized in time. It does not implement Runtime, scheduler, tick loop, model invocation, Decision, Action, permission, Reducer integration, or State mutation.

## Cognitive cycle candidate view

```text
Field Change / Cognitive Need / Goal Change / Risk Change
  -> Observation Update Candidate
  -> Situation Update Candidate
  -> Context Update Candidate
  -> Attention Allocation Candidate
  -> Sufficiency Assessment Candidate
  -> Route Selection Candidate
  -> Pattern Match / Reasoning Candidate
  -> Candidate Formation
  -> Evaluation Candidate
  -> Commitment Candidate
  -> Outcome Observation Candidate
  -> Experience Update Candidate
```

Every step remains candidate-only. `Route Selection Candidate` is not Route Decision, `Commitment Candidate` is not Future Decision, and no step performs Action or State mutation.

# Cognitive Execution Runtime Skeleton v1

## Purpose

`ControlledCognitiveExecutionSkeleton` is a deterministic component-level skeleton. It creates one bounded, synthetic Cognitive Tick and only emits immutable Candidate objects through the existing Candidate-only boundary.

## Flow

```text
Synthetic Reality Event Candidate
 -> Perception Candidate
 -> Information Field Candidate
 -> Representation Candidate
 -> Schema Candidate
 -> Attention Candidate
 -> Workspace Candidate
 -> Simulation Candidate
 -> Operation Candidate
 -> Evaluation Candidate
 -> Outcome Observation Candidate
 -> Feedback Candidate
```

## Scenarios

- `familiar`: fast A-route / minimum-sufficient candidate flow; simulation is not expanded.
- `uncertain`: high-unknown interface flow; emits a B-interface candidate and Simulation Candidates but does not execute Route B.

## Non-authority

The skeleton is not a scheduler, World Model, Decision engine, Action executor, Reducer, Memory system, or learning/evolution runtime. It constructs a JSON-safe trace only.

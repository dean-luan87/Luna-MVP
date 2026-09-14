# Cognitive Capability Composition Lifecycle v1

## Purpose

Capability Composition describes a candidate combination of cognitive capabilities appropriate for a bounded cognitive need. It is not an Agent Plan, Task Planner, tool call, or execution plan.

## Lifecycle

```text
Generate
  -> Evaluate
  -> Adopt Candidate
  -> Execute Candidate
  -> Outcome Candidate
  -> Feedback Candidate
```

`Execute Candidate` means that a future runtime could consider the bundle for bounded cognitive processing. It does not invoke a capability, model, sensor, device, decision, or action in this phase.

## Bundle candidate example

```text
Goal context: reach_gate
Capability bundle candidate:
  - visual evidence interpretation
  - text evidence interpretation
  - spatial-context candidate
  - experience guidance candidate
Constraints:
  - offline map unavailable
  - resource budget medium
```

## Lifecycle controls

- generation follows information gap, context, goal, risk, self state, and resource candidates;
- evaluation checks relevance, reliability, expected information value, cost, and conflicts;
- adoption remains a candidate and requires future runtime admission;
- outcome produces feedback, never automatic learning or capability upgrade.

## Frozen boundaries

Capability Composition is not Task Planning. Capability Bundle Candidate is not capability invocation. Capability Execute Candidate is not Action Execution.


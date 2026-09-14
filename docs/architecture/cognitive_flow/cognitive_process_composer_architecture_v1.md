# Cognitive Process Composer Architecture v1

## Purpose

The Cognitive Process Composer upgrades capability composition into a bounded cognitive-process organization candidate.

## Capability versus process

```text
Capability: Vision + OCR + Map
Process: understand current location, evaluate route evidence,
         observe risk, and provide navigation-support candidates
```

Capabilities identify what could contribute. A process candidate identifies how a bounded cognitive activity could be organized around a goal and context.

## Composition input

```text
Goal Candidate
  + Context Candidate
  + Attention Allocation Candidate
  + Capability Bundle Candidate
  + Resource Budget Candidate
  + Kernel Constraint Candidate
  -> Cognitive Process Candidate
```

## Process candidate contents

- process objective and bounded expected output;
- context, goal, attention, capability, resource, and workspace references;
- unknown, risk, evidence, and consistency constraints;
- proposed lifecycle and feedback references;
- provenance, confidence, and uncertainty.

## Boundary

The Composer produces a Candidate only. It is not a planner, scheduler, runtime executor, decision engine, action executor, or State owner.


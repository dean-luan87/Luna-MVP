# Dynamic Cognitive Architecture Migration Plan

## Migration principles

Use mapping-first, owner-first, adapter-first migration. Do not move or rewrite
passed assets. Every implementation step needs a separate authorized phase and
must preserve candidate, evidence, trace, replay, admission, and rollback
boundaries.

## Sequence

### P0 — Canonical owner and terminology freeze

- Review this v2 candidate against Architecture Baseline v2.
- Freeze Personal Cognitive Network as projection/topology owner only.
- Freeze Intent Governance, Causal Reasoning Governance, Memory System, Task
  Manager, Decision Arbitration, and Action Runtime as distinct owners.
- Register duplicate-owner risks before any implementation.

### P1 — Contract and adapter planning

- Define a Field State → Field Context projection adapter.
- Separate perceptual attention output from cognitive attention allocation input.
- Align existing Intent Architecture contracts to Intent Processing and the
  evaluation-gate output.
- Align existing causality schemas to candidate network edges.
- Define Memory/Experience Compression → network evolution candidate interfaces.

### P2 — Personal Cognitive Network technical architecture

- Define typed nodes, typed edges, activation projections, source references,
  temporal validity, evidence, revision, and revocation.
- Reuse Luna V2 Cognitive Object Model envelopes.
- Prohibit the network from owning source truth or persistence without admission.

### P3 — Controlled skeletons

- Implement contract-only adapters in isolated controlled-skeleton phases.
- Keep Runtime, model/provider calls, database writes, Action, and automatic
  learning disabled.
- Validate deterministic trace/replay and owner boundaries.

### P4 — Runtime integration candidates

- Only after P0–P3 verification, prepare controlled Runtime integration planning.
- Integrate one bounded flow at a time: Field activation, Intent qualification,
  causal candidate projection, gate recommendation, feedback compression.
- Require user-terminal verification and V3 audit for each phase.

## Explicitly deferred

No directory migration, old-document rewrite, Memory replacement, Emotion Runtime,
causal graph execution, autonomous network evolution, B Route simulation, model
integration, or production activation is part of this plan phase.


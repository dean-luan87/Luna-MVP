# Luna Dynamic Cognitive System v2 — Canonical Freeze Candidate

## Status and scope

This document is the canonical **candidate** produced by
`Phase-Luna-Dynamic-Cognitive-Architecture-Realignment-Planning-v1-001`.
It consolidates the new cognitive model and maps it to existing Luna owners.
It does not replace Architecture Baseline v2, activate Runtime, or authorize
code migration. Promotion to an active baseline requires a later governed
baseline-integration decision.

## System flow

```text
External World
    ↓
Environment Understanding (Perception / Evidence)
    ↓
Field System (current cognitive context)
    ↓
Personal Cognitive Network (typed connection and activation projection)
    ├── Self references
    ├── Role references
    ├── Relationship references
    ├── Experience / Memory references
    └── Belief / Schema / attachment references
    ↓
Causal Network (candidate personal world model)
    ↓
Intent Processing
    ↓
Intent Evaluation Gate
    ├── Direct Response Candidate
    └── Cognitive Expansion Candidate → A/B Route boundary
    ↓
Decision Candidate / Arbitration
    ↓
Action Boundary / Action Runtime
    ↓
Feedback Collection and Reality Validation
    ↓
Experience Compression
    ↓
Cognitive Network Evolution Candidate
    ↓
Self Review / Learning and governance boundaries
```

The flow is candidate-based. Evidence is not meaning, a causal relation is not
fact, intent is not decision, decision is not action, and experience compression
does not directly mutate Memory or the Personal Cognitive Network.

## Canonical ownership

The v2 candidate adds an integration model without replacing established owners:

| Concern | Canonical owner | v2 position |
| --- | --- | --- |
| Evidence intake | Observation Manager / Reality Evidence Pipeline | Environment Understanding |
| Current context | Field System | Field Context Management |
| Self identity and boundaries | Self Governance | referenced by the network |
| Role lifecycle | Social Self / Role System | referenced and projected by the network |
| Relationship lifecycle | Social Self / Relationship System | referenced and projected by the network |
| Memory persistence and activation | Memory System | supplies governed historical influence |
| Cross-object typed links and activation projections | Personal Cognitive Network Governance | new integration responsibility |
| Causal candidates | Causal Reasoning Governance | reuses existing causality plans and object schemas |
| Intent candidates | Intent Governance | reuses Cognitive Intent Architecture v1 |
| Goal and value | Goal Governance / Value Utility Governance | constrain intent and decision candidates |
| Decision arbitration | Decision Arbitration | selects a candidate; does not execute |
| Task lifecycle and routing | Task Manager | downstream orchestration, not action execution |
| Action execution | Action Boundary / Action Runtime | only execution path |
| Emotion context | Cognitive Integration | network projection only; no Value ownership |
| Model assets | Capability Governance / Model Manager | capability layer; no cognitive authority |

## Personal Cognitive Network

The Personal Cognitive Network is Luna's context-sensitive integration substrate.
It owns the topology, typed link candidates, activation weights, and projections
needed to assemble a personal cognitive view. It does not own the source objects.

This distinction prevents a new central component from swallowing the established
owners of Self, Role, Relationship, Memory, Emotion, or Value. Network edges keep
source references, field scope, temporal validity, confidence, evidence,
counter-evidence, candidate status, and revision history.

## Field activation

Field is upgraded from a state label to the activation entry for the cognitive
network. A field context may activate several related fields and projections—for
example Work, Family, Financial, Self Growth, and Emotion Context—while preserving
their separate owners. The existing Field State Reducer remains the formal
candidate-only state-reduction mainline; a future adapter may expose a Field
Context projection without rewriting that reducer.

## Intent and expansion gate

Intent Processing qualifies and binds Intent Candidates to Field, Self, Role,
Relationship, Goal, Task, Value, risk, and unknowns. The Intent Evaluation Gate
does not own decisions. It recommends either:

- a bounded Direct Response Candidate when evidence and sufficiency permit; or
- a Cognitive Expansion Candidate when uncertainty, risk, causal depth, conflict,
  or future-space analysis requires more cognition.

The Brain and Decision Arbitration retain candidate evaluation and selection.
The A/B Route boundary cannot mutate the live A-route state.

## Causality and experience

The Causal Network represents candidate relationships among people, events,
roles, states, goals, time, benefit, and cost. Existing cognitive causality plans
and subjective causality object schemas are reused. Causal output remains
evidence-bound, revisable, and explicitly not fact.

Experience evolves through outcome observation, validation, compression, and
governed network-update candidates. Memory remains the owner of storage,
consolidation, activation, and retention. Experience Compression produces reusable
patterns and guidance candidates rather than writing Memory or network edges.

## Architecture-only boundary

This phase performs no code change, Runtime activation, data migration, file move,
model/provider integration, automatic learning, automatic network update, causal
graph execution, Emotion Runtime, B Route simulation, Decision execution, or
Action execution.


# Luna Cognitive Core Integration Baseline v1.0

## Purpose

This baseline consolidates the completed Cognitive Core contracts into one
reviewable subject model. It is an architecture contract, not a Runtime
implementation.

## Canonical master flow

```text
Observation → Evidence → Field → Context → Workspace → Attention
→ Hypothesis → Belief → Expectation → Global State → Brain
→ Decision Candidate → Commitment → Action Request → Action
→ Outcome → Feedback → Learning → Self Evolution → Self Regulation
→ State Update
```

Each stage has a declared producer, consumer, ownership boundary, and
lifecycle. Feedback is an event re-entry path; it is not a permission cycle.

## Authority baseline

- Brain owns context integration, candidate evaluation, decision candidate
  generation, and decision trace.
- Brain does not execute actions, own capabilities, directly mutate Memory,
  modify Constitution, or rewrite Identity.
- Action Boundary owns the execution gate. Action Runtime is outside the
  Cognitive Core and remains unimplemented in this phase.
- Memory System owns admitted long-term records. Workspace may hold working
  context but does not become long-term Memory.
- Learning and Self Evolution emit candidates. Governance and Brain review are
  required before a candidate changes an active rule or profile.
- Self Regulation observes and proposes stability-preserving adjustments. It
  cannot rewrite Identity, Value, Goal, Constitution, or Brain rules.

## Capability boundary

```text
Brain / Cognitive Need
  ↓ Capability Request
  ↓ Capability Governance
  ↓ Capability Runtime
  ↓ Evidence Gateway
  ↓ Evidence / Reality Update Candidate
```

Provider, Model, and Hardware remain evidence-producing implementation
boundaries. They do not become Cognitive Core authorities.

## Future interfaces

Emotion remains interface-only. Social Runtime, Model Integration, Provider
Integration, Hardware Integration, Action Execution, and automatic Learning are
future extensions requiring separate admission and review.

## Baseline status

This is a consolidation baseline pending user-terminal V2 verification and
ChatGPT V3 audit. It does not grant Runtime readiness or GO.

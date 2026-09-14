# Architecture Baseline v2 Whitebox

The baseline is a read-only canonical map. It answers what each layer and module is, who owns it, what it may read, and which dependencies are forbidden. It deliberately does not claim that every mapped concept has an executable implementation.

## Questions every entry must answer

- What is the canonical identity?
- Which layer and owner apply?
- What state or candidate does it produce?
- Which readers are allowed?
- Which writes are forbidden?
- Is the asset implemented, planned, conceptual, or missing?

## Boundary invariants

- Constitution constrains all layers and is not owned by Self.
- Brain evaluates cognitive candidates but does not execute actions.
- Self Regulation protects stability but cannot rewrite Identity, Value, Goal, or Constitution.
- Social Self provides contextual roles and relationships but cannot rewrite Self Identity.
- Capability Governance selects admissible implementations but cannot create goals.
- Providers return evidence candidates through the evidence boundary only.
- Emotion, World Model, Embodiment, and external LLM entries remain future boundaries.

## Read-only planning contract

This phase creates registries and mappings only. No file move, delete, rename, code migration, runtime activation, provider call, model call, hardware call, or automatic learning is performed.

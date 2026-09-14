# Intent Governance Controlled Implementation v1

Status: CONTROLLED_IMPLEMENTATION_CANDIDATE

This phase implements a controlled, candidate-only Intent Governance module based on the passed planning assets in docs/architecture/luna_intent_architecture_planning_v1.

Implemented scope:
- Intent core candidate types
- Intent input/output envelopes
- Lifecycle candidate states
- Coexistence and competition interaction candidates
- Temporary dominance candidate semantics
- Cross-field/context carryover candidates
- Resource degradation candidates
- Provenance/trace candidate structures
- Ownership and mutation boundary guards
- Intent-to-Causal handoff candidate
- Structured error namespace
- Fixture-driven controlled runner

Boundary guarantees:
- candidate_only = true
- synthetic_fixture_only = true
- runtime_executed = false
- source_mutation_executed = false
- no Decision/Action/Task/Causal truth output
- no active schema or contract activation

The implementation reuses existing controlled skeleton conventions from Context Foundation and PCN: immutable dataclasses, pure static validators, source-owner reference handling, and deterministic trace output.

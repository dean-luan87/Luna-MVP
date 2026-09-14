# A3 Cognitive Analysis Runtime Capability Assessment Plan v1

## Scope

This assessment declares the future analysis-capability boundary of A3 Runtime. It is an inventory-only skeleton: it does not perform analysis, invoke Runtime, invoke a model, infer evidence, generate hypotheses, or produce a Decision.

## Candidate Analysis Types

1. **Context Interpretation Candidate** — a possible reading of an already supplied Context reference.
2. **Evidence Relationship Candidate** — a possible declared relationship among supplied Evidence references.
3. **Hypothesis Candidate** — a candidate-level assessment of already supplied Hypothesis references; it is not Fact.
4. **Uncertainty Assessment Candidate** — an explicit account of coverage, conflict, unknown, stale, revoked, or insufficient conditions.
5. **Semantic Explanation Candidate** — a possible explanation expressed with provenance and uncertainty; it is not a causal conclusion.

## Permanent Capability Boundaries

None of these candidates may generate Fact, generate Decision, plan Action, mutate State, update Memory, mutate Context/Snapshot/Event/Evidence, or become an authority override. The Field State Reducer remains the sole State mutation authority.

## Assessment Runner Boundary

The Runner produces only a fixed capability assessment report. It receives no Context, Evidence, Hypothesis, model output, or runtime output; it does not call Runtime `execute()` or resolve any reference.

## Authorization

`runtime_authorized=false` remains true. This assessment states what future candidate categories may be considered only after separately governed Runtime authorization; it does not implement them.

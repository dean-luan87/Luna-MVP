# Capability ↔ Model ↔ Provider Binding Controlled Implementation v1

This package implements only candidate-only, synthetic declaration binding
seams for the frozen Luna flow.

- Capability ↔ Model binding lifecycle: Capability Governance.
- Model ↔ Provider binding lifecycle: Provider Governance.
- Model identity and declarations remain Model Governance authority.
- Runtime Admission, Provider Admission, loading, probing and invocation are
  downstream and are not implemented here.

All records are synthetic, versioned, provenance-aware and non-mutating.


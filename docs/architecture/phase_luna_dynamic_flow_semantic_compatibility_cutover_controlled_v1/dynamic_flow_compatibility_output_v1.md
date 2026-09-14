# Dynamic Flow compatibility output

`DynamicFlowCompatibilityOutputV1` preserves:

- computed Need reference;
- computed sufficiency status;
- computed reconsideration references;
- computed next-step disposition;
- state, evidence, trace, and provenance references.

It explicitly carries `compatibility_only=true`, `semantic_authority=false`, and `source_owner_ref=COGNITIVE_FLOW_GOVERNANCE`. These fields describe the computational source, not an authority transfer to Dynamic Flow.

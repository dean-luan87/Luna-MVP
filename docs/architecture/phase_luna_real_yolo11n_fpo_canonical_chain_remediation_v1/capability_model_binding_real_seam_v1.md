# Capability↔Model Binding Real Seam v1

`CanonicalYOLO11nBindingContextV1` accepts an existing
`CapabilityModelBindingCandidateV1` by reference.

Validation requires:

- Capability Governance ownership and lifecycle ownership;
- Model asset and model-version continuity;
- `COMPATIBLE` model declaration status;
- no binding invalidation;
- trace, provenance, and source-version lineage.

The adapter never creates, updates, supersedes, or retires the binding.


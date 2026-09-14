# FPO Authority Narrowing v1

FPO retains:

- bounded frame/ROI and Observation request adaptation;
- provider-session and invocation bookkeeping;
- deduplication and result correlation;
- acquisition trace/provenance propagation;
- adaptation of canonical binding/admission references into the existing
  Provider input.

FPO does not own:

- Capability Resolution;
- model identity or model lifecycle;
- Capability↔Model binding lifecycle;
- Runtime Admission;
- Model↔Provider binding lifecycle;
- Provider semantic fallback or replanning.

The new seam validates references; it does not issue any of these authorities.


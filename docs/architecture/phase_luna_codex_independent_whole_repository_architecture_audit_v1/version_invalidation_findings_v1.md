# Version / Invalidation Findings v1

## Evidence

- Dynamic loop advances explicit state refs and rejects evidence whose source version does not equal the current state (`cognitive_dynamic_loop_engine_v1.py:42-43,131-137`).
- Observation Gateway has explicit version mismatch/superseded handling (`observation_gateway_engine_v1.py:184-219`).
- Field Event admission checks temporal order/expiry and emits reducer eligibility without invoking the reducer.
- Binding adapters reject stale model/provider declarations and preserve invalidation refs.
- The real-capability compatibility adapter constructs Runtime Admission candidates with source, model, integrity, provider-compatibility, trace and provenance refs (`real_capability_runtime_admission_compatibility_adapter_v1.py:131-163`).

## Gap

These chains are proven locally or synthetically. The direct YOLO11n path has a different provisioning/admission shape, and the repository-wide audit found no single caller-aware assertion that an old Capability↔Model or Model↔Provider binding cannot reach every real execution entrypoint. Classification: `BROKEN_CHAIN` for the real execution seam, severity `P1` under F-001; `IMPLEMENTED` for controlled candidate seams.


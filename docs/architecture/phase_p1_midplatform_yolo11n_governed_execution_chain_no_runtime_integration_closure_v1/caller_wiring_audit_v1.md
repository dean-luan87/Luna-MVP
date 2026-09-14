# Targeted caller wiring audit

The real entrypoint accepts `CanonicalYOLO11nBindingContextV1` and passes it
to `build_canonical_yolo11n_provider_admission_v1`.

The A-Route path constructs context from supplied
`CanonicalYOLO11nUpstreamRecordsV1`; absent context results in a non-authorized
Provider Admission candidate. The shared Provider adapter checks
`canonical_chain_validated` and canonical invalidation refs before real
invocation.

The existing caller-aware verifier remains evidence and is reported as a
separate result; this closure harness does not overwrite or hide its checks.

# End-to-end no-runtime chain

The Runner starts from `produce_yolo11n_governed_execution_records_v1`, which
reads the repository declaration registries. It then invokes the existing
translation, context builder, and Provider Admission seam.

The final object is a `VisionProviderAdmissionCandidateV1`. The Runner does
not call `run_authorized_vision_provider_v1` and does not invoke YOLO.

Provider admission authorization and Provider invocation are distinct:

- `provider_admission_candidate_created = true` is allowed;
- `provider_invocation = false` is mandatory.

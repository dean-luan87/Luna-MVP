# Governed bundle and YOLO context integration

The integration is:

```text
repository-backed declarations
  → RuntimeAdmissionProductionInputV1
  → RuntimeAdmissionAssessmentCandidateV1
  → ExecutableCapabilityCandidateV1
  → GovernedExecutionRecordBundleV1
  → CanonicalYOLO11nUpstreamRecordsV1
  → existing canonical YOLO context builder
```

The bundle carries source versions, Grant/constraint refs, trace/provenance,
and empty invalidation refs. The context builder remains the consumer-side
validation boundary; it is not moved into Runtime Admission.

# Runtime Observation Contract

`RuntimeObservationEnvelopeV1` is the reference-only boundary for an external
capability result that is already available to Luna. It preserves:

- observation identity and execution-instance identity;
- provider and capability refs;
- modality (`VISION`, `OCR`, or `SLAM_SPATIAL` in the phase fixtures);
- source and raw-result refs;
- temporal, confidence, quality, spatial, trace, and provenance refs;
- provider/capability availability and candidate-only/truth flags.

`ObservationIngressRequestV1.runtime_observation` carries the envelope to the
existing Gateway. The Gateway produces `ObservationGatewayRuntimeAdmissionV1`,
which is the only live-mode admission proof consumed by A-Route. The proof
contains the Gateway admission ref, runtime observation ref, observation/evidence
refs, execution identity, trace/provenance, and cognition information refs.

The envelope is not a Fact and does not declare World Truth. Gateway output is
`PerceptionEvidenceV1` with `candidate_only=true` and `fact_declared=false`.
Unavailable or malformed envelopes are rejected before Evidence formation.

The missing-information fixture is intentionally partial: its active need and
required set contain document location and operational state, while admitted
evidence coverage supplies document location only. The explicit availability
projection prevents the empty-availability fallback from treating the case as
an unqualified evidence-derived projection. The canonical sufficiency status
for this path is `INSUFFICIENT`; `INSUFFICIENT_EVIDENCE` is a hypothesis state
label and is not substituted for the sufficiency result.

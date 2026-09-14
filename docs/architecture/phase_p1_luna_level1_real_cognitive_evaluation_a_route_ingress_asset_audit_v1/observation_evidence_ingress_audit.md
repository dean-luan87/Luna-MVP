# Observation and Evidence Ingress Audit

## Existing boundaries

- `ObservationDemandCandidateV1`, `ObservationRequestCandidateV1`, and `CapabilityRequirementCandidateV1` belong to the FPO/Observation planning boundary.
- `PerceptionIngressCandidateV1`, raw-frame/session candidates, and visual provider admission/evidence types are candidate-only boundaries.
- `VisualDetectionEvidenceCandidateV1` and `ObservationGatewayEvidenceHandoffCandidateV1` terminate provider-specific output before semantic cognition.
- RF-DETR real smoke demonstrates actual provider response → normalized Evidence → Gateway candidate → Current World/Hypothesis/Sufficiency candidates for one narrow PoC.

## Four paths

1. Live real: supported by a narrow Roboflow/YOLO precedent, not a general A-Route ingress.
2. Recorded/replay: deterministic replay refs exist in `field_perception_trace_replay_v1.py`; replay-to-A cognition is not connected.
3. Synthetic: existing controlled FPO and White-box fixtures support candidate-only checks.
4. Evaluation-controlled: run boundary can supply refs, but must not create Evidence truth or cognition.

The first legitimate ingress should be an admitted or explicitly candidate-scoped Observation/Evidence handoff consumed by A-Route ingress. Evaluation should not bypass this boundary by constructing Current World, Hypothesis, Sufficiency, or Information Gap.


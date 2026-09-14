# B1 Real Visual Evidence → Context / Current World Planning Summary

## Decision

The canonical route is **D: reuse the existing canonical ingestion boundary**:

`YOLO11n VisualDetectionEvidenceCandidateV1`
→ `ObservationGatewayEvidenceHandoffCandidateV1`
→ Observation Gateway canonical evidence/observation admission
→ existing Context World State Controlled Integration boundary
→ Context Foundation reference-only candidate
→ optional Field Event Admission / reducer-eligibility branch
→ CurrentWorldCandidateV1 referencing Context and Field State.

This is not a new Evidence→World owner. The existing C01-C36 controlled
integration is the synthetic reference path and already encodes the required
ownership boundaries.

## Inventory conclusion

The real YOLO11 provider path produces provider-native detections, structured
visual evidence, and a gateway handoff candidate. The handoff is still a
candidate (`gateway_admission=false`, `semantic_authority=false`); it is not
yet a canonical Observation Gateway result. Observation Gateway owns
normalization, evidence governance, admission/routing candidates, and trace
lineage. Context Foundation assembles immutable reference projections.

Field Event Admission is the temporal/structural gate for field-relevant event
candidates. The Field State Reducer is the sole Field State mutation authority
and accepts admitted field events only. Current World is a derived candidate,
not a raw evidence sink or second Field writer.

## B1 boundary

The minimum future implementation is a narrow adapter/extension that maps the
real visual evidence handoff into the existing gateway contract while
preserving detection fields, frame/source references, temporal references,
uncertainty, contradiction, provenance, and trace. The admitted observation
then enters the existing Context World State Controlled Integration boundary.

YOLO detection must not itself infer field relevance, create a field event,
declare an object truth, or write Current World. A field-event branch requires
an explicit governed field relevance/scope candidate and Field Event Admission.

## Blockers

The current Observation Gateway runner/engine is controlled around
`ObservationIngressRequestV1` and enforces synthetic-only input. A real-evidence
gateway adapter or narrowly versioned gateway input extension is therefore
required before B1 runtime integration can be implemented. This planning phase
does not alter that implementation.

## Status

Planning assets created only. No implementation, provider, runner, verifier, or
model execution was performed.

`WAITING_FOR_USER_REVIEW`

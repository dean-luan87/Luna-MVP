# Change Manifest

## Phase

`Phase-P1-Luna-Real-Cognitive-Entity-To-Field-Relation-Candidate-Integration-v1-001`

## Implementation changes

- Added a thin evaluation integration package for real visual
  `EntityCandidateV1 → RelationCandidateV1` projection.
- Reused the existing Cognitive Primitive `RelationCandidateV1` and builder;
  no canonical Relation schema was added or changed.
- Reused the existing real YOLO, runtime observation, visual evidence, and L1
  subject-candidate path.
- Added bounded positive and negative relation guards, including independent
  relations for same-class detections.
- Added the user-terminal runner and fail-closed verifier.

## Preserved semantics

- `OBSERVED_IN_FIELD` remains candidate-only and does not imply
  `belongs_to`, ownership, function, persistent presence, or Field meaning.
- `field:visual-frame:v1` remains a controlled context candidate.
- Identity remains unresolved; L2/L3 layers, Target Binding, Memory, and PCN
  are not entered.
- Evidence Sufficiency remains 2 events / 2 sources.
- Visual confidence remains observation/evidence confidence; RelationCandidateV1
  has no relation-confidence field.
- `POLICY_TRACE_COMPATIBILITY_GAP` remains a known, non-blocking, independent
  debt and is not repaired here.
- Field Reducer, Field Event Admission, Provider Runtime, OCR, and cognitive
  semantics are not modified.

## Documentation status

`WAITING_FOR_USER_TERMINAL_VERIFICATION`.

The canonical Field-Conditioned Entity Semantics & Cross-Field Information
Reuse principle is referenced as the architectural boundary. This phase is
its first runtime relation-level integration, not meaning resolution.

## Runtime verification repair

First user-terminal verification reached Runtime and produced 12 detections,
12 Evidence candidates, 12 EntityCandidates, and 12 RelationCandidates. All
relation semantics and negative guards passed; the only blocker was
`relation_traceable`.

Classification: `RELATION_TRACEABILITY_INTEGRATION_GAP`.

The Relation Trace previously selected
`capability-governance:object-detection-yolo11n-binding:v1` by filtering
provenance text. The repair maps `source_detection_refs` from the canonical
`VisualDetectionEvidenceCandidateV1.detection_ref`, selected by the matching
EntityCandidate Evidence reference. The verifier continues to require
Runtime Observation, Evidence, Detection, EntityCandidate, Subject Binding,
RelationCandidate, and Field reference consistency; no check was weakened.

No relation semantics, cognitive semantics, canonical Relation contract,
Provider Runtime, Field Reducer, or policy debt was changed. Status remains
`WAITING_FOR_USER_TERMINAL_VERIFICATION` pending user re-verification.

## Second Runtime verification repair

The second user-terminal Runtime verified the previous real
`source_detection_refs` mapping repair. The only remaining failure was
`relation_traceable`.

Classification: `VERIFIER_TRACE_PROJECTION_GAP`.

The positive semantic event places `relation_candidate_ref` under
`semantic_trace.payload`; the verifier incorrectly read the event top level.
The minimal repair reads the canonical payload location. Positive semantic
traceability remains strict, while guard-only negative cases are not required
to provide a semantic trace. No Runtime mapping, relation semantics,
canonical contract, or other verifier strength was changed.

Status remains `WAITING_FOR_USER_TERMINAL_VERIFICATION`.

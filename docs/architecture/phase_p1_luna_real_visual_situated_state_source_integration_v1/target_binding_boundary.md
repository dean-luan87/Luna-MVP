# Target Binding Boundary

Static audit found no single canonical Target Selection/Binding contract that
can safely assert that a YOLO class is the requested transit-sign target.
The implementation therefore uses `VisualTargetBindingCandidateV1` as an
evaluation-level correlation candidate:

- `target_requirement_ref`: `target-requirement:visual-detection-candidate:v1`
- `target_ref`: existing candidate target `target:visible-transit-sign:v1`
- `detection_ref`: the real native detection identity
- `semantic_target_resolved`: `false`
- `candidate_only`: `true`

This preserves the existing precondition target namespace for the controlled
cognitive context without claiming that the detected object is a station sign.
Target selection and semantic target governance remain outside this phase.

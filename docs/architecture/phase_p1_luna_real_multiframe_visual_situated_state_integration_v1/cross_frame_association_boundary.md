# Cross-Frame Association Boundary

`CrossFrameTargetAssociationCandidateV1` is an evaluation-level correlation
candidate. Its basis is limited to class compatibility, bbox geometry and the
controlled target binding context.

It explicitly sets:

- `candidate_only=true`
- `semantic_identity_resolved=false`
- `physical_identity_declared=false`

Equal class labels across frames do not prove that the detections are the same
physical object. The contract is not a tracker, identity resolver, or World
Truth writer.

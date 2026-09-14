# Stability Semantics

Static audit found no canonical threshold or tolerance that maps visual
temporal metrics to `condition:stable-relation:v1`. The existing condition is
stronger than a single geometric comparison: it belongs to a situated
temporal relation assessment.

Accordingly, `VisualRelationStabilityCandidateV1` retains the temporal metric
lineage but has:

- `status=UNKNOWN`;
- `threshold_ref=null`;
- candidate-only provenance.

The phase must not turn equal class labels, similar bboxes, or a case/cycle
number into `STABLE`. An unknown required stability condition remains
fail-closed through existing Situated Capability Preconditions.

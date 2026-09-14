# Attention to Observation Handoff v1

## Conceptual candidate

An AttentionFocusCandidate should carry refs to:

- originating Cognitive Requirement;
- focus target/object/region;
- modality preference;
- urgency and temporal validity;
- bounded budget;
- safety/permission/resource constraints;
- expected evidence type;
- source versions;
- trace and provenance.

This is a conceptual contract only. No type is created in this phase.

Observation/FPO decides whether the candidate is admissible, how acquisition is
performed and which evidence is returned. Capability Governance resolves the
functional capability; Runtime Admission and Provider Governance remain in
force.

The handoff must not contain an implicit Provider invocation or a direct
camera/OCR/YOLO/SLAM command.

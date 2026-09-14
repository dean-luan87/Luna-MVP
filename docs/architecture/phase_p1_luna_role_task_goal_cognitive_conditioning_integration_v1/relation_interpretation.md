# Relation interpretation

`CognitiveRelationInterpretationCandidateV1` is the minimum candidate-only
surface needed for role-conditioned relation meaning. It references a stable
Field relation and records the Role/Task/Goal/Need-conditioned interpretation.
It is exposed in Cognitive State Formation output and A-Route execution proof;
it is not a relation store and does not mutate Field state.

An optional typed form may be supplied by a read-only Field State projection.
It preserves the governed subject, predicate, Field object, relation candidate,
semantic kind, evidence/source/provenance refs, and unresolved identity
status. This is semantic input preservation, not identity resolution or Truth
promotion.

The typed form is now passed through the existing Cognitive State Formation
Role/Task/Goal/Information Need conditioning path. The conditioning rebuilds a
candidate interpretation and attaches the active conditioning references; it
does not change `subject_ref`, `predicate`, `object_ref`, relation kind, or
Field State. Opaque Context references remain reference-only unless a governed
semantic signal exists.

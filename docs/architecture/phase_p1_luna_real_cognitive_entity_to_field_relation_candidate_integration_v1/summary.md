# Summary

## Current status

`WAITING_FOR_USER_TERMINAL_VERIFICATION`

## Implemented chain

```text
Real YOLO
→ Runtime Observation
→ Visual Evidence
→ EntityCandidateV1
→ L1 Subject Binding Candidate
→ RelationCandidateV1
→ Field Semantic Event / Cognitive Trace
```

The relation uses `OBSERVED_IN_FIELD` with the observation-linked entity
candidate as subject and the current controlled Field context as object. Each
same-class detection retains its own observation-linked EntityCandidate ID and
its own relation ID.

## Frozen boundaries

```text
Entity Candidate != Physical Entity Identity
Observed In Field != Belongs To Field
Candidate Binding != Identity Resolution
Entity Candidate != Target Binding
Entity Candidate != Memory Identity
Relation Candidate != Fact
Relation Candidate != Field Truth
Relation Candidate != World Truth
Relation Candidate != Evidence Source
```

The Field reference is
`field:visual-frame:v1 / CONTROLLED_CONTEXT_CANDIDATE`; it is not a physical
Field identity. The relation has no confidence field, so relation confidence is
unavailable rather than copied from YOLO confidence.

The existing 2-event/2-source Evidence Sufficiency contract and the known
`POLICY_TRACE_COMPATIBILITY_GAP` are preserved. A relation candidate does not
make the current evidence sufficient and does not alter Reducer authority.

This phase is the first runtime relation-level integration of
[Field-Conditioned Entity Semantics & Cross-Field Information Reuse](../field_conditioned_entity_semantics_and_cross_field_information_reuse_v1.md),
not cross-Field meaning resolution.

## Current verification status

The first Runtime verification reached the intended real YOLO relation path
and produced 12 detections, 12 Evidence candidates, 12 EntityCandidates, and
12 RelationCandidates. The only failed check was `relation_traceable`.

The blocker was `RELATION_TRACEABILITY_INTEGRATION_GAP`: a capability/model
binding provenance ref was projected as `source_detection_refs`. The static
repair uses the canonical visual Evidence `detection_ref` reached through the
EntityCandidate's evidence ref, then validates the complete lineage. Current
status remains `WAITING_FOR_USER_TERMINAL_VERIFICATION`; the phase is not
closed.

## Second Runtime verification status

The second Runtime confirmed that the prior `source_detection_refs` mapping
repair is correct, including the canonical real detection reference and the
independent same-class chair lineages. The sole failure remained
`relation_traceable`.

The cause was verifier projection: `relation_candidate_ref` is stored in the
positive semantic trace payload, not at the event top level. This is
`VERIFIER_TRACE_PROJECTION_GAP`, fixed by reading the existing payload field.
Guard-only negative cases remain allowed to have `semantic_trace=null`; the
positive semantic integration trace remains strictly checked. Current status
is still `WAITING_FOR_USER_TERMINAL_VERIFICATION`.

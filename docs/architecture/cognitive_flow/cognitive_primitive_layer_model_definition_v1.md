# Luna Cognitive Primitive Layer Model Definition v1

## Common Primitive Candidate Envelope

Every future Primitive Candidate is planned to retain:

- `primitive_id` and `primitive_type`;
- `source_refs`, `context_refs`, provenance, and `trace_ref`;
- confidence and explicit uncertainty;
- `candidate_status`, `candidate_only=true`, and `fact_status=not_fact`; and
- declared attributes/relations without implied mutation or truth.

This is a planning model, not a new executable schema or Fact model.

## Primitive Families

| primitive | expresses | examples | never means |
| --- | --- | --- | --- |
| Entity Primitive | possible object/person/place/facility/physical item | person candidate, entrance candidate, device candidate | confirmed identity or final Entity |
| Relation Primitive | possible spatial, temporal, social, or causal-candidate relation | near, before, associated-with, possible-cause | causal truth or permission to act |
| State Primitive | possible object/environment/relation condition | closed candidate, noisy candidate, connected candidate | Field State or Reducer write |
| Event Primitive | possible state/behavior/environment change | movement candidate, opening-change candidate, temperature-shift candidate | admitted Event or State transition |
| Situation Primitive | possible current scene/environment/task-relevant configuration | crowded-area candidate, blocked-entry candidate | world understanding, Decision, or action plan |

## Composition Rules

Primitives may reference other candidates, Evidence, Context, and Translation output. They must retain competing/unknown alternatives and cannot silently fuse separate sources into a Fact. A Situation Primitive is a candidate expression, not a Field Snapshot or world model.


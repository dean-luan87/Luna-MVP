# A3 Evidence Context Translation Layer Contract v1

## Input

The Translation Request Envelope contains only:

- Evidence references;
- Context references;
- provenance references;
- source-capability references;
- requested primitive type; and
- a trace reference.

No raw model payload, database handle, Field State, Snapshot, Fact, Decision instruction, Action command, or Memory handle is accepted.

## Output

The Cognitive Primitive Candidate contains:

- `candidate_id`
- `primitive_type`
- `source_refs`
- `context_refs`
- `confidence`
- `uncertainty`
- `provenance`
- `trace_ref`
- `candidate_status`

Allowed primitive types are `entity_candidate`, `relation_candidate`, `semantic_candidate`, `spatial_candidate`, and `temporal_candidate`. All outputs remain `candidate_only=true`, `fact_status=not_fact`, and `translation_not_executed` in this skeleton.

## Negative Guards

1. Evidence must not become Fact.
2. Evidence must not become Decision/Action.
3. Translation output must retain provenance and trace.
4. An external model/provider identity remains provenance; it cannot become a Cognitive Entity.
5. Translation must not modify Context, Snapshot, or Field State.

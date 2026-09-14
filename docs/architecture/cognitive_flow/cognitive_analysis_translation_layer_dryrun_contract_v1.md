# A3 Evidence Context Translation Layer Controlled DryRun Contract v1

## Input

Every fixture supplies only `evidence_reference`, `context_reference`, `provenance_reference`, `source_capability_reference`, and `trace_reference` through the existing Translation Request Envelope.

## Output

Every serialized Cognitive Primitive Candidate contains:

- `candidate_id`
- `primitive_type`
- `source_refs`
- `context_refs`
- `confidence`
- `uncertainty`
- `provenance`
- `trace_ref`
- `candidate_status`

The only valid DryRun status is `translation_not_executed`, with `candidate_only=true` and `fact_status=not_fact`.

## Fixed Flags

`translation_executed=false`, `simulation_only=true`, `model_invoked=false`, `external_call=false`, `fact_created=false`, `decision_created=false`, `action_created=false`, `state_writeback=false`, and `memory_updated=false`.

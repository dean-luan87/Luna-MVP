# A3 Evidence Context Translation Layer Validation Contract v1

## Contract Subject

The subject is a serialized Translation Candidate Envelope produced only by the existing controlled Skeleton and fixture-based DryRun path.

## Required Input Evidence

- Evidence reference
- Context reference
- provenance/source reference
- source-capability reference
- trace reference
- requested candidate primitive type

## Required Output Evidence

Every Cognitive Primitive Candidate must retain:

- `candidate_id`
- `primitive_type`
- `source_refs`
- `context_refs`
- `confidence`
- `uncertainty`
- `provenance`
- `trace_ref`
- `candidate_status=translation_not_executed`
- `candidate_only=true`
- `fact_status=not_fact`

## Boundary Assertions

`translation_executed=false`, `simulation_only=true`, `model_invoked=false`, `external_call=false`, `fact_created=false`, `decision_created=false`, `action_created=false`, `state_writeback=false`, `context_mutated=false`, `snapshot_mutated=false`, `memory_updated=false`, and `learning_candidate_admitted=false`.

The Validator and DryRun Verifier must validate serialized evidence independently of Skeleton invocation. Validation success is not Fact admission, Runtime authorization, consumer permission, or learning admission.

# Cognitive Concept Layer DryRun Contract v1

## Input

Each frozen fixture supplies only `primitive_refs`, `pattern_refs`, `context_refs`, a non-final semantic description, provenance references, and a trace reference. No raw provider payload, model response, database record, or Field State handle is an input.

## Output

Every output is a `CognitiveConceptCandidateV1` envelope with `concept_id`, `concept_type`, `primitive_refs`, `context_refs`, `pattern_refs`, `confidence`, `uncertainty`, `provenance`, and `trace_ref`.

It must carry `candidate_only=true` and `fact_status=not_fact`. It must not contain `fact_id`, `decision_id`, `action_id`, `state_write_target`, or `memory_target`.

## Execution boundary

The DryRun record requires `runtime_executed=false`, `simulation_only=true`, `fixture_only=true`, and all external, mutation, decision, action, memory, learning, and language-encoding flags false.

## Provenance closure

Candidate provenance must retain source references, Translation references, the source-capability reference, and a provenance trace equal to the candidate `trace_ref`.

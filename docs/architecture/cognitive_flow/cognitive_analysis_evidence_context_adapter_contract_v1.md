# A3 Cognitive Analysis Evidence Context Adapter Contract v1

## Input Candidate

`CognitiveAnalysisEvidenceContextAdapterCandidateV1` requires:

- `adapter_request_id`
- `input_reference`
- one or more `evidence_references`
- `context_reference`
- `provenance.source_refs`
- `provenance.trace_ref`
- `normalized_reference_mapping`
- explicit permission flags

The object has no raw observation payload, model output payload, database handle, State handle, Fact claim, Decision command, or Memory handle.

## Normalization Contract

Normalization is limited to stable reference mapping. It may map known Evidence/Context identifiers into the A3 input vocabulary and preserve their order. It must not add semantic labels, remove uncertainty, replace provenance, or construct a Fact.

## Permission and Authority Contract

The following must be explicitly false: `runtime_execution`, `model_invocation`, `fact_admission`, `semantic_finalization`, `decision_generation`, `action_execution`, `state_mutation`, and `memory_update`.

The Adapter remains `candidate_only=true`, `fact_status=not_fact`, and `runtime_authorized=false`.

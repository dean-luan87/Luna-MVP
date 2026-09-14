# A3 Cognitive Analysis Runtime Prototype Contract v1

## Input

`CognitiveAnalysisRuntimePrototypeRequestV1` requires:

- `analysis_id`
- `context_ref`
- `evidence_refs`
- `analysis_question_ref`
- `fixture_id`

All are references or fixed fixture identifiers. No raw Field State, observation payload, database handle, or mutation handle is accepted.

## Output

The prototype returns a `CognitiveAnalysisRuntimePrototypeResultV1` containing:

- complete input trace;
- an `Analysis Result Candidate` compliant with the existing result contract;
- a prototype execution envelope; and
- a deterministic-output declaration.

The candidate remains `candidate_only=true`, `fact_status=not_fact`, and all candidate authority flags remain false. The execution envelope alone reports `runtime_executed=true`, `fixture_only=true`, and `simulation_only=true`.

## Forbidden Operations

`model_invoked=false`  
`network_invoked=false`  
`database_written=false`  
`fact_write=false`  
`decision_execute=false`  
`action_execute=false`  
`state_writeback=false`  
`memory_update=false`  
`model_training=false`  
`runtime_authorized=false`

No flag may be used to infer formal Runtime admission, Fact admission, or consumer permission.

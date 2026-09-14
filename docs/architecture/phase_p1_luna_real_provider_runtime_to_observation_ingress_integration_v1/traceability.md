# Traceability

The controlled bridge preserves this chain:

`observation_demand_ref`
→ `capability_requirement_ref`
→ `capability_ref` / `provider_ref` / `model_ref`
→ `provider_request_ref`
→ `provider_result_ref`
→ `runtime_observation_ref`
→ `gateway_admission_ref`
→ `evidence_refs`
→ `a_route_execution_ref`
→ Cognitive State Formation
→ `sufficiency_ref`, `information_gap_ref`, or `stop_ref`.

Provider request/result trace and provenance refs are carried into the runtime
observation envelope. Existing Gateway and A-Route identity rules remain the
source of downstream execution refs.

For re-observation, the trace continues through
`next_cycle_ingress_ref` → `reobservation_request_ref` → candidate
`provider_request_ref`; the bridge stops there until a later provider runtime
executor supplies a result.

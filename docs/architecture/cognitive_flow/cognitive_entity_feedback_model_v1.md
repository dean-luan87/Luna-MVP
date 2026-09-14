# Entity Feedback Model v1

## Definition

Entity Feedback is the bounded return path by which an embodiment node reports local capability outputs and operating conditions. It keeps local execution facts and limitations visible without allowing direct Brain mutation.

```text
EntityFeedbackCandidate {
  entity_ref,
  work_objective_ref,
  capability_result_ref,
  evidence_ref,
  resource_status,
  connection_status,
  failure_candidate,
  degradation_candidate,
  unknown_candidate,
  local_cache_scope,
  trace
}
```

## Feedback categories

| Category | Example | Boundary |
|---|---|---|
| Capability result | A local capability returned bounded output. | Result is not truth. |
| Evidence | Local output packaged as evidence candidate. | Does not enter Brain directly. |
| Resource status | Battery, compute, latency, or storage limitation. | Does not alter Goal/Attention. |
| Failure / degradation | Provider unavailable, sensor degraded, protocol mismatch. | Does not cancel work itself. |
| Unknown | Local coverage gap or unavailable input. | Unknown is not a failure or decision. |
| Local-cache scope | Transient retention reference needed for trace/retry boundary. | Not long-term Memory/Experience. |

## Return path

`Entity → Entity-local Middleware Report → Entity Governance → Neural Feedback Package → Brain Update Candidate`

No Entity feedback artifact may directly modify Brain state, Context, Goal, Attention, Memory, Value, Decision, or Reality state. Reducer remains the only state-mutation authority.

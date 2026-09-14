# Change Manifest

## Added

- Typed `EntityFieldRelationStateValueV1` in the existing Field State
  reduction area.
- Minimal evaluation Runner and fail-closed Verifier.
- Controlled two-source relation-state reduction case.
- Phase documentation.

## Modified

- Existing reduction handoff now carries admitted events for semantic
  reduction.
- Existing Field Event Admission preserves optional source identity needed by
  the unchanged evidence-diversity evaluator.
- Minimal Field state/event registry mappings for
  `entity_field_observation_relation_state` and
  `entity_field_relation_observed`.

## Preserved

- `FieldStateCandidate` remains the only state envelope.
- Evidence thresholds remain 2 events / 2 sources.
- `OBSERVED_IN_FIELD` remains distinct from `BELONGS_TO_FIELD`.
- Fact, Field Truth, World Truth, persistent relation, identity, Target,
  Memory, PCN, and A-Route boundaries remain closed.
- `POLICY_TRACE_COMPATIBILITY_GAP` is not repaired.

## Runtime verification repair history

The first user-terminal verification was blocked before the intended reducer
assertions could be evaluated. Both the real single-source event and the two
controlled events were rejected as `expired_event`, yielding zero admitted
events and zero evidence sources. The failure is recorded as
`FIELD_EVENT_TEMPORAL_ADMISSION_TEST_INTEGRATION_GAP`; downstream typed-value
and insufficient-evidence observations were not treated as independent
failures.

The integration engine now derives one current UTC test timestamp per run and
uses it consistently for event `occurred_at`, `observed_at`, `received_at`,
and the Admission Policy `evaluated_at`. This is a test-time lineage repair
only. The canonical Field Event Admission expiration/freshness policy was not
modified, admission is not bypassed, and the 2-event/2-source evidence
contract is unchanged.

## Policy eligibility repair history

The subsequent user-terminal run showed valid temporal admission and the
expected `1/1` real single-source versus `2/2` controlled multi-source
distinction, but the controlled reducer still produced no eligible policy.
The common evidence evaluator reads required provenance fields at the
top-level of `provenance_snapshot`; the integration request had exposed only
the corresponding `available_keys` list and `source_ids`. This caused a
`FIELD_RELATION_REDUCER_POLICY_ELIGIBILITY_INTEGRATION_GAP` before the existing
`multi_event_consensus` path could be selected.

The minimal repair supplies `source_id`, `event_id`, `event_time`, and
`admission_id` from the admitted-event lineage. It does not alter the policy
registry, evidence evaluator thresholds, temporal admission, or reducer
policy semantics. The single-source path therefore remains fail-closed, while
the controlled two-source path can reach the already-existing typed relation
reduction branch.

## Third verification repair: policy selection applicability

The third user-terminal run showed valid `2 events / 2 distinct sources` and an
eligible `multi_event_consensus`, but selected
`temporary_overlay_separation`. The canonical registry already excludes the
overlay policy from `entity_field_observation_relation_state`; the selection
filter had not enforced that existing `eligible_state_types` mapping. This
caused `FIELD_RELATION_REDUCER_POLICY_SELECTION_INTEGRATION_GAP`.

The repair is limited to the existing Policy Selection candidate filter and
rejects policies whose registry applicability does not contain the requested
state type. It does not modify the Runner, precedence matrix, overlay
semantics, evidence sufficiency thresholds, or the relation-state candidate
boundaries. The real `1 event / 1 source` case remains insufficient; the
controlled `2 events / 2 sources` case is allowed to reach the existing
`multi_event_consensus` typed relation reduction branch.

## Final user-terminal closure

The final user-terminal verification passed with:

- `all_checks_passed=true`
- `failed_checks=[]`
- `cognitive_logic_result=PASS`
- `operational_result=PASS`
- `final_decision=GO`

The live Real YOLO/provider path was verified and recorded provider output was
not used. The real case remained `1 event / 1 source` and
`insufficient_evidence`. The controlled case reached `2 admitted events / 2
distinct sources`, selected only `multi_event_consensus`, and produced the
typed `EntityFieldRelationStateValueV1` inside the existing
`FieldStateCandidate` envelope.

The candidate preserves the Entity↔Field observation relation and its
lineage while remaining `candidate_only=true`, `fact_admitted=false`,
`truth_declared=false`, `persistent_relation_declared=false`, and
`identity_resolution_status=UNRESOLVED`. No Field store mutation, Field Truth,
World Truth, A-Route, Memory, PCN, Decision, Task, Action, or device control
was introduced. `OBSERVED_IN_FIELD` remains distinct from
`BELONGS_TO_FIELD`.

ROUTE C — `FIELD_STATE_RELATION_REPRESENTATION_GAP` is now closed.
`POLICY_TRACE_COMPATIBILITY_GAP` remains a known, non-blocking, independent
debt. ROUTE D remains deferred.

## Status

`GO — VERIFIED — PHASE CLOSED`.

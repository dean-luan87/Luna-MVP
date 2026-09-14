# Verification

## Scope

The user-terminal Runner/Verifier must validate one real single-source case
and one controlled two-source reducer case.

Expected distinction:

`Event Admission != Evidence Sufficiency != Relation State Candidate != Fact Admission != Field Truth`.

## Required cases

### `REAL_SINGLE_SOURCE_FAIL_CLOSED`

The existing real YOLO path is invoked once. Its admitted relation event has
one provider source, so the existing 2-event/2-source contract produces
`insufficient_evidence` and no sufficiently-supported typed relation state.

### `CONTROLLED_MULTI_SOURCE_RELATION_STATE`

Two explicitly controlled admitted events use two distinct controlled source
references while preserving the same candidate subject, Field object,
predicate, and relation kind. The existing `multi_event_consensus` path must
produce a typed `FieldStateCandidate.candidate_value`.

## Required assertions

- Real provider/model execution is verified and recorded results are unused.
- `entity_field_relation_observed` is explicitly consumed by the relation
  state mapping.
- The typed value preserves subject, predicate, Field object, relation ref,
  relation kind, evidence, source, trace, and provenance lineage.
- `candidate_only=true`, `fact_admitted=false`, `truth_declared=false`.
- `persistent_relation_declared=false` and identity remains unresolved.
- Entity, Binding, and Relation Candidate do not count as evidence sources.
- `OBSERVED_IN_FIELD != BELONGS_TO_FIELD`.
- No Field/World Truth, Memory/PCN mutation, A-Route, Action, Task, or Device
  execution occurs.
- `POLICY_TRACE_COMPATIBILITY_GAP` remains an independent known debt.

## First user-terminal verification failure

The first user-terminal execution reached the Field Event Admission boundary,
but both cases produced `expired_event`:

- `real_single_source.admission_statuses = ["expired_event"]`
- `controlled_multi_source.admission_statuses = ["expired_event", "expired_event"]`
- admitted event count: `0`
- evidence source count: `0`

The later typed relation candidate, candidate value, policy selection, and
`insufficient_evidence` observations were therefore downstream effects of the
temporal admission result. This was classified as
`FIELD_EVENT_TEMPORAL_ADMISSION_TEST_INTEGRATION_GAP`, not as a cognitive
logic, relation-state, or reducer semantic failure.

The direct cause was test integration time lineage: the copied event retained
the prior projection's historical `2026-08-13T00:00:00Z` timestamps while the
current integration evaluated admission later. The canonical admission API
was correctly applying its existing freshness policy.

The repair uses one UTC timestamp generated for the current user-terminal
integration run for `occurred_at`, `observed_at`, and `received_at`, and passes
that same timestamp as `AdmissionPolicyV1.evaluated_at`. Controlled events keep
distinct event/source references and remain the explicitly labeled
`CONTROLLED_MULTI_SOURCE_SEMANTIC_REDUCER_TEST`. The canonical expiration,
freshness window, admission boundary, evidence thresholds, and reducer
semantics are unchanged; expired events are not bypassed or relabeled.

## Second user-terminal verification failure

After temporal admission was repaired, the user-terminal run confirmed:

- real case: `1 admitted event / 1 source`, correctly fail-closed;
- controlled case: `2 admitted events / 2 distinct sources`;
- nevertheless, every policy evaluation returned `insufficient_evidence`,
  with no eligible or selected policy and no typed relation value.

Static tracing found that the common evidence evaluator requires
`source_id`, `event_id`, `event_time`, and `admission_id` as top-level
provenance snapshot fields. This integration request supplied only
`available_keys` and `source_ids`, so the evaluator reported missing
provenance even when the event and source counts were sufficient. The
relation state and `multi_event_consensus` state-type mapping were already
present; this was a reducer policy eligibility input-shape integration gap,
classified as `FIELD_RELATION_REDUCER_POLICY_ELIGIBILITY_INTEGRATION_GAP`.

The repair populates those required provenance fields from the admitted event
lineage, preserving scalar values for the single-event case and lists for the
two-event controlled case. Evidence sufficiency remains exactly 2 events / 2
distinct sources; no event or source is fabricated, and the real single-source
case remains insufficient.

## Third user-terminal verification failure

The next user-terminal run confirmed that temporal admission and evidence
provenance were both correct: the real case remained `1 event / 1 source`, and
the controlled case had `2 admitted events / 2 distinct sources`. The
`multi_event_consensus` candidate was eligible, but selection chose
`temporary_overlay_separation`, so reduction produced a generic overlay value
instead of `EntityFieldRelationStateValueV1`. The phase remained `NO-GO`.

Static tracing found that the canonical policy registry already includes
`entity_field_observation_relation_state` for `multi_event_consensus` and
excludes it for `temporary_overlay_separation`. The selection candidate filter
checked policy identity, evaluation status, and the selection flag, but did not
enforce the registry's `eligible_state_types`. Generic overlay inputs could
therefore enter precedence and win through the overlay-high precedence class.
This was classified as
`FIELD_RELATION_REDUCER_POLICY_SELECTION_INTEGRATION_GAP`, not a relation
semantic or cognitive-logic failure.

The minimal repair applies the existing registry applicability mapping at the
Policy Selection candidate boundary using the request's state type. An
inapplicable policy is rejected with `state_type_not_applicable`; no policy is
forced by the Runner and no precedence rule is changed. For the relation state,
`temporary_overlay_separation` is now excluded and the existing
`multi_event_consensus` path can select the typed relation reduction when
`2 events / 2 sources` are satisfied. The real `1 event / 1 source` path
continues to fail closed without a supported typed relation state.

## Final user-terminal verification and closure

The final user-terminal verification passed:

- `all_checks_passed=true`
- `failed_checks=[]`
- `cognitive_logic_result=PASS`
- `operational_result=PASS`
- `final_decision=GO`

The real provider path verified live Real YOLO/model execution, with recorded
provider results unused. The real single-source case remained one admitted
event and one source, so it remained `insufficient_evidence` and did not
produce a supported typed relation state. The controlled case contained two
admitted events and two distinct sources; the existing `multi_event_consensus`
policy was the sole selected policy and built a completed candidate.

The resulting `FieldStateCandidate` has state type
`entity_field_observation_relation_state` and a typed
`EntityFieldRelationStateValueV1` preserving subject, `OBSERVED_IN_FIELD`, the
Field object reference, relation candidate/kind, evidence/source lineage, and
provenance. It remains candidate-only: fact admission, truth declaration,
persistent relation declaration, identity resolution, Field store mutation,
and World Truth promotion remain false or unresolved.

The following boundaries were verified and remain frozen:

- `OBSERVED_IN_FIELD != BELONGS_TO_FIELD`.
- Event admission is not fact admission or Field Truth promotion.
- Relation/entity/binding candidates do not add evidence source diversity.
- No A-Route, Memory, PCN, Decision, Task, Action, camera, device, or
  movement execution occurred.
- `POLICY_TRACE_COMPATIBILITY_GAP` remains a known, non-blocking,
  independent debt and was not repaired.

ROUTE C — `FIELD_STATE_RELATION_REPRESENTATION_GAP` is closed. ROUTE D is not
part of this closure and remains deferred pending its own static integration
work.

Final status: `GO — VERIFIED — PHASE CLOSED`.

"""Candidate-only adapters for result return and Outcome→Brain input."""

from __future__ import annotations

from typing import Optional, Tuple

from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)

from .types_v1 import (
    AdapterFailureV1,
    AuthorityGuardsV1,
    BrainAdjudicationInputCandidateV1,
    BrainInputReturnOutputV1,
    CurrentWorldUpdateCandidateV1,
    EdgeObservabilityCandidateV1,
    FieldEventCandidateAdapterV1,
    OutcomeSourceInputV1,
    ResultSourceInputV1,
    SourceStateHandoffCandidateV1,
    SourceStateReturnOutputV1,
)


STALE_MARKERS = ("STALE", "REVOKED", "INVALID", "VERSION_MISMATCH", "EXPIRED")


def _guards() -> AuthorityGuardsV1:
    return AuthorityGuardsV1()


def _failure(
    ref: str,
    classification: str,
    reason: str,
    owner: str,
    next_target: str,
    source_refs: Tuple[str, ...],
    trace_refs: Tuple[str, ...],
    provenance_refs: Tuple[str, ...],
) -> AdapterFailureV1:
    return AdapterFailureV1(
        failure_ref=ref,
        classification=classification,
        reason=reason,
        responsible_owner=owner,
        next_target=next_target,
        source_refs=source_refs,
        trace_refs=trace_refs,
        provenance_refs=provenance_refs,
    )


def _edge(
    *,
    transition_id: str,
    trace_id: str,
    concern_ref: Optional[str],
    producer: str,
    consumer: str,
    authority_owner: str,
    responsibility_owner: str,
    transition_class: str,
    input_refs: Tuple[str, ...],
    input_versions: Tuple[str, ...],
    output_refs: Tuple[str, ...],
    output_versions: Tuple[str, ...],
    status: str,
    evidence_refs: Tuple[str, ...],
    provenance_refs: Tuple[str, ...],
    invalidation_refs: Tuple[str, ...],
    failure_classification: Optional[str],
    next_target: str,
) -> EdgeObservabilityCandidateV1:
    # The edge record has its own adapter provenance even when the source
    # candidate is intentionally rejected for missing provenance. The source
    # omission remains visible through failure_classification/reason; this
    # record-level provenance closes the adapter-owned trace lineage only.
    edge_provenance_refs = provenance_refs or (f"prov:edge:{transition_id}:adapter",)
    return EdgeObservabilityCandidateV1(
        transition_id=transition_id,
        trace_id=trace_id,
        parent_transition_refs=(),
        concern_ref=concern_ref,
        reasoning_cycle_ref=None,
        producer=producer,
        consumer=consumer,
        authority_owner=authority_owner,
        responsibility_owner=responsibility_owner,
        transition_class=transition_class,
        input_refs=input_refs,
        input_versions=input_versions,
        output_refs=output_refs,
        output_versions=output_versions,
        admission_or_validation_status=status,
        constraint_refs=(),
        evidence_refs=evidence_refs,
        provenance_refs=edge_provenance_refs,
        invalidation_refs=invalidation_refs,
        failure_classification=failure_classification,
        blocker_refs=(),
        next_target=next_target,
    )


def _result_failure(result: ResultSourceInputV1, expected_concern_ref: Optional[str]) -> Optional[AdapterFailureV1]:
    if not result.synthetic_only or not result.candidate_only:
        return _failure("failure:non-synthetic", "NON_SYNTHETIC_INPUT", "input is not synthetic candidate-only data", "return-path adapter", "caller", (result.source_result_ref,), result.trace_refs, result.provenance_refs)
    if result.provider_invocation_executed or result.action_execution_executed:
        return _failure("failure:runtime-execution", "RUNTIME_EXECUTION_DETECTED", "runtime execution flag is not permitted", "return-path adapter", "caller", (result.source_result_ref,), result.trace_refs, result.provenance_refs)
    if not result.provenance_refs:
        return _failure("failure:provenance", "PROVENANCE_INVALID", "result has no provenance", "Evidence/result adapter", "A", (result.source_result_ref,), result.trace_refs, result.provenance_refs)
    if result.result_kind == "PROVIDER_RESULT" and not result.evidence_refs:
        return _failure("failure:evidence", "EVIDENCE_MAPPING_FAILED", "Provider Result has no Evidence refs", "Provider Result→Evidence adapter", "Observation Gateway/A", (result.source_result_ref,), result.trace_refs, result.provenance_refs)
    if not result.source_version_refs:
        return _failure("failure:source-version", "SOURCE_VERSION_MISSING", "result has no source-version lineage", "source-state handoff adapter", "A", (result.source_result_ref,), result.trace_refs, result.provenance_refs)
    if expected_concern_ref and result.concern_ref and result.concern_ref != expected_concern_ref:
        return _failure("failure:concern", "CROSS_CONCERN_CONTAMINATION", "result Concern does not match requested Concern", "source-state handoff adapter", "A/Brain", (result.source_result_ref,), result.trace_refs, result.provenance_refs)
    if result.invalidation_refs:
        return _failure("failure:invalidation", "SOURCE_VERSION_MISMATCH", "result carries invalidation refs and cannot form a downstream source candidate", "source-state handoff adapter", "A/refresh", (result.source_result_ref,), result.trace_refs, result.provenance_refs)
    if not result.source_valid or result.status_candidate.upper() in STALE_MARKERS:
        return _failure("failure:stale", "SOURCE_VERSION_MISMATCH", "source result is stale or invalid", "source-state handoff adapter", "A/refresh", (result.source_result_ref,), result.trace_refs, result.provenance_refs)
    return None


def _current_world_candidate(result: ResultSourceInputV1, handoff: SourceStateHandoffCandidateV1) -> str:
    """Construct the existing CurrentWorldCandidateV1 as a candidate only."""
    candidate = CurrentWorldCandidateV1(
        current_world_id=f"current-world:{handoff.handoff_id}",
        attention_refs=(),
        active_hypothesis_refs=(),
        alternative_hypothesis_refs=(),
        context_refs=(),
        field_state_refs=(),
        pcn_refs=(),
        intent_refs=(),
        observation_refs=result.evidence_refs,
        uncertainty_refs=result.uncertainty_refs,
        conflict_refs=(),
        temporal_refs=tuple(ref for ref in (result.effective_time_ref,) if ref),
        source_versions=tuple(
            (f"source_{index}", value)
            for index, value in enumerate(result.source_version_refs)
        ),
        world_state_kind_candidate="EVIDENCE_RETURN_CANDIDATE",
        world_stability_candidate=result.status_candidate,
        trace_ref=result.trace_refs[0],
        provenance_refs=result.provenance_refs,
    )
    assert candidate.candidate_only is True
    assert candidate.field_mutation is False
    assert candidate.field_truth_declaration is False
    return candidate.current_world_id


def adapt_result_to_source_state(
    result: ResultSourceInputV1,
    *,
    target_boundary: str,
    expected_concern_ref: Optional[str] = None,
    expected_target_version_ref: Optional[str] = None,
    adapter_kind: str = "Evidence/result",
) -> SourceStateReturnOutputV1:
    """Build independent Current World and/or Field candidates without mutation."""
    trace_id = result.trace_refs[0] if result.trace_refs else f"trace:{result.source_result_ref}"
    failure = _result_failure(result, expected_concern_ref)
    valid_targets = {"CURRENT_WORLD", "FIELD", "BOTH"}
    if target_boundary not in valid_targets and failure is None:
        failure = _failure("failure:target", "TARGET_BOUNDARY_INVALID", "unsupported target boundary", "source-state handoff adapter", "caller", (result.source_result_ref,), result.trace_refs, result.provenance_refs)
    input_refs = (result.source_result_ref,) + result.evidence_refs
    if failure is not None:
        edge = _edge(
            transition_id=f"transition:{result.source_result_ref}:blocked",
            trace_id=trace_id,
            concern_ref=result.concern_ref,
            producer=adapter_kind,
            consumer="Field / Current World",
            authority_owner="Field / Current World candidate boundary",
            responsibility_owner=failure.responsible_owner,
            transition_class="VALIDATION",
            input_refs=input_refs,
            input_versions=result.source_version_refs,
            output_refs=(),
            output_versions=(),
            status="BLOCKED",
            evidence_refs=result.evidence_refs,
            provenance_refs=result.provenance_refs,
            invalidation_refs=result.invalidation_refs,
            failure_classification=failure.classification,
            next_target=failure.next_target,
        )
        return SourceStateReturnOutputV1(None, None, None, None, edge, _guards(), failure)

    handoff = SourceStateHandoffCandidateV1(
        handoff_id=f"handoff:{result.source_result_ref}",
        handoff_version="v1",
        source_result_refs=(result.source_result_ref,),
        evidence_refs=result.evidence_refs,
        target_boundary=target_boundary,
        target_ref=result.target_ref,
        source_version_refs=result.source_version_refs,
        expected_target_version_ref=expected_target_version_ref,
        effective_time_ref=result.effective_time_ref,
        observed_time=result.observed_time,
        uncertainty_refs=result.uncertainty_refs,
        confidence_candidate=result.confidence_candidate,
        status_candidate=result.status_candidate,
        provenance_refs=result.provenance_refs,
        trace_refs=result.trace_refs,
        invalidation_refs=result.invalidation_refs,
        authority_owner="Field / Current World candidate boundary",
        responsibility_owner="source-state handoff adapter",
    )
    if result.result_kind == "ACTION_RESULT" and not result.evidence_refs:
        edge = _edge(
            transition_id=f"transition:{handoff.handoff_id}:unverified",
            trace_id=trace_id,
            concern_ref=result.concern_ref,
            producer=adapter_kind,
            consumer="Task / A / Outcome Evaluation",
            authority_owner="Action/Task/Outcome boundaries",
            responsibility_owner="source-state handoff adapter",
            transition_class="FORMATION",
            input_refs=input_refs,
            input_versions=result.source_version_refs,
            output_refs=(handoff.handoff_id,),
            output_versions=(handoff.handoff_version,),
            status="RESULT_RETURNED_NO_EFFECT_EVIDENCE",
            evidence_refs=(),
            provenance_refs=result.provenance_refs,
            invalidation_refs=result.invalidation_refs,
            failure_classification=None,
            next_target="Task / A / Outcome Evaluation",
        )
        return SourceStateReturnOutputV1(handoff, None, None, None, edge, _guards(), None)
    current_world_update = None
    current_world_ref = None
    field_event = None
    output_refs = []
    if target_boundary in {"CURRENT_WORLD", "BOTH"}:
        current_world_ref = _current_world_candidate(result, handoff)
        current_world_update = CurrentWorldUpdateCandidateV1(
            update_ref=f"current-world-update:{handoff.handoff_id}",
            handoff_ref=handoff.handoff_id,
            current_world_candidate_ref=current_world_ref,
            evidence_refs=result.evidence_refs,
            source_version_refs=result.source_version_refs,
            trace_refs=result.trace_refs,
            provenance_refs=result.provenance_refs,
            status_candidate=result.status_candidate,
        )
        output_refs.append(current_world_ref)
    if target_boundary in {"FIELD", "BOTH"}:
        event_ref = f"field-event-candidate:{handoff.handoff_id}"
        field_event = FieldEventCandidateAdapterV1(
            event_candidate_ref=event_ref,
            handoff_ref=handoff.handoff_id,
            field_ref=result.target_ref,
            evidence_refs=result.evidence_refs,
            source_version_refs=result.source_version_refs,
            effective_time_ref=result.effective_time_ref,
            trace_refs=result.trace_refs,
            provenance_refs=result.provenance_refs,
            status_candidate=result.status_candidate,
        )
        output_refs.append(event_ref)
    edge = _edge(
        transition_id=f"transition:{handoff.handoff_id}",
        trace_id=trace_id,
        concern_ref=result.concern_ref,
        producer=adapter_kind,
        consumer="Field / Current World candidate boundary",
        authority_owner="Field / Current World candidate boundary",
        responsibility_owner="source-state handoff adapter",
        transition_class="FORMATION",
        input_refs=input_refs,
        input_versions=result.source_version_refs,
        output_refs=tuple(output_refs),
        output_versions=(handoff.handoff_version,),
        status="CANDIDATE_READY",
        evidence_refs=result.evidence_refs,
        provenance_refs=result.provenance_refs,
        invalidation_refs=result.invalidation_refs,
        failure_classification=None,
        next_target="A / Field admission" if target_boundary == "FIELD" else "A / Current World consumption",
    )
    return SourceStateReturnOutputV1(handoff, current_world_update, field_event, current_world_ref, edge, _guards(), None)


def build_brain_adjudication_input(
    outcome: OutcomeSourceInputV1,
    *,
    expected_concern_ref: Optional[str] = None,
) -> BrainInputReturnOutputV1:
    """Map an Outcome Candidate to a Brain input candidate only."""
    trace_id = outcome.trace_refs[0] if outcome.trace_refs else f"trace:{outcome.outcome_candidate_ref}"
    failure: Optional[AdapterFailureV1] = None
    if not outcome.candidate_only:
        failure = _failure("failure:outcome-authority", "OUTCOME_NOT_CANDIDATE", "Outcome input is not candidate-only", "Outcome→Brain input adapter", "Outcome Evaluation", (outcome.outcome_candidate_ref,), outcome.trace_refs, outcome.provenance_refs)
    elif outcome.brain_adjudication_executed or outcome.brain_state_mutation:
        failure = _failure("failure:brain-execution", "BRAIN_EXECUTION_DETECTED", "Brain execution or mutation flag is not permitted", "Outcome→Brain input adapter", "Outcome Evaluation", (outcome.outcome_candidate_ref,), outcome.trace_refs, outcome.provenance_refs)
    elif not outcome.concern_ref or not outcome.grant_ref:
        failure = _failure("failure:missing-scope", "MISSING_CONCERN_OR_GRANT", "Concern and Grant refs are required", "Outcome Evaluation", "A/Brain", (outcome.outcome_candidate_ref,), outcome.trace_refs, outcome.provenance_refs)
    elif expected_concern_ref and outcome.concern_ref != expected_concern_ref:
        failure = _failure("failure:outcome-concern", "CROSS_CONCERN_CONTAMINATION", "Outcome Concern does not match expected Concern", "Outcome→Brain input adapter", "A/Brain", (outcome.outcome_candidate_ref,), outcome.trace_refs, outcome.provenance_refs)
    elif not outcome.provenance_refs:
        failure = _failure("failure:outcome-provenance", "PROVENANCE_INVALID", "Outcome has no provenance", "Outcome Evaluation", "A/Brain", (outcome.outcome_candidate_ref,), outcome.trace_refs, outcome.provenance_refs)
    elif not outcome.source_version_refs:
        failure = _failure("failure:outcome-version", "SOURCE_VERSION_MISSING", "Outcome has no source-version lineage", "Outcome Evaluation", "A/Brain", (outcome.outcome_candidate_ref,), outcome.trace_refs, outcome.provenance_refs)
    elif outcome.invalidation_refs or "revoked" in (outcome.grant_ref or "").lower() or "stale" in (outcome.grant_ref or "").lower():
        failure = _failure("failure:outcome-stale", "OUTCOME_SOURCE_STALE", "Outcome source refs require invalidation handling", "Outcome Evaluation", "A/Brain", (outcome.outcome_candidate_ref,), outcome.trace_refs, outcome.provenance_refs)
    input_refs = (outcome.outcome_candidate_ref,) + outcome.action_result_refs + outcome.field_refs + outcome.current_world_refs
    if failure is not None:
        edge = _edge(
            transition_id=f"transition:{outcome.outcome_candidate_ref}:blocked",
            trace_id=trace_id,
            concern_ref=outcome.concern_ref,
            producer="Outcome Evaluation",
            consumer="Brain Governance",
            authority_owner="Brain Governance",
            responsibility_owner=failure.responsible_owner,
            transition_class="VALIDATION",
            input_refs=input_refs,
            input_versions=outcome.source_version_refs,
            output_refs=(),
            output_versions=(),
            status="BLOCKED",
            evidence_refs=(),
            provenance_refs=outcome.provenance_refs,
            invalidation_refs=outcome.invalidation_refs,
            failure_classification=failure.classification,
            next_target=failure.next_target,
        )
        return BrainInputReturnOutputV1(None, edge, _guards(), failure)
    candidate = BrainAdjudicationInputCandidateV1(
        input_ref=f"brain-input:{outcome.outcome_candidate_ref}",
        input_version="v1",
        outcome_candidate_ref=outcome.outcome_candidate_ref,
        outcome_version=outcome.outcome_version,
        goal_refs=outcome.goal_refs,
        concern_ref=outcome.concern_ref,
        grant_ref=outcome.grant_ref,
        decision_refs=outcome.decision_refs,
        task_refs=outcome.task_refs,
        action_result_refs=outcome.action_result_refs,
        a_local_evaluation_refs=outcome.a_local_evaluation_refs,
        field_refs=outcome.field_refs,
        current_world_refs=outcome.current_world_refs,
        evaluation_status=outcome.evaluation_status,
        partiality=outcome.partiality,
        uncertainty_refs=outcome.uncertainty_refs,
        safety_refs=outcome.safety_refs,
        permission_refs=outcome.permission_refs,
        resource_refs=outcome.resource_refs,
        followup_candidate_refs=outcome.followup_candidate_refs,
        source_version_refs=outcome.source_version_refs,
        invalidation_refs=outcome.invalidation_refs,
        trace_refs=outcome.trace_refs,
        provenance_refs=outcome.provenance_refs,
    )
    edge = _edge(
        transition_id=f"transition:{candidate.input_ref}",
        trace_id=trace_id,
        concern_ref=candidate.concern_ref,
        producer="Outcome Evaluation",
        consumer="Brain Governance",
        authority_owner="Brain Governance",
        responsibility_owner="Outcome→Brain input adapter",
        transition_class="BINDING",
        input_refs=input_refs,
        input_versions=outcome.source_version_refs,
        output_refs=(candidate.input_ref,),
        output_versions=(candidate.input_version,),
        status="CANDIDATE_READY",
        evidence_refs=(),
        provenance_refs=outcome.provenance_refs,
        invalidation_refs=outcome.invalidation_refs,
        failure_classification=None,
        next_target="Brain adjudication input queue",
    )
    return BrainInputReturnOutputV1(candidate, edge, _guards(), None)

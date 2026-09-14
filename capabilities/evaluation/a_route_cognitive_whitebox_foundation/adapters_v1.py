from __future__ import annotations

from typing import Any, Iterable, Mapping, Tuple

from .types_v1 import (
    CognitiveWhiteBoxTraceV1,
    LunaCognitiveExecutionProfileV1,
    ProfileValueV1,
)


def _nodes(trace: CognitiveWhiteBoxTraceV1, kind: str):
    return tuple(node for node in trace.nodes if node.node_kind == kind)


def _refs(trace: CognitiveWhiteBoxTraceV1, kind: str) -> Tuple[str, ...]:
    return tuple(node.source_ref for node in _nodes(trace, kind))


def _observed(value: Any, refs: Iterable[str], notes: str = "") -> ProfileValueV1:
    return ProfileValueV1(value=value, availability="observed", source_refs=tuple(refs), notes=notes)


def _not_observed(notes: str = "") -> ProfileValueV1:
    return ProfileValueV1(value=None, availability="not_observed", notes=notes)


def _unavailable(notes: str = "") -> ProfileValueV1:
    return ProfileValueV1(value=None, availability="unavailable", notes=notes)


def _measure_count(trace: CognitiveWhiteBoxTraceV1, kind: str, *, not_observed: bool = False) -> ProfileValueV1:
    nodes = _nodes(trace, kind)
    if not nodes or not_observed:
        return _not_observed(f"no explicit {kind} observation")
    return _observed(len(nodes), (node.trace_node_id for node in nodes))


def build_luna_cognitive_execution_profile_v1(
    trace: CognitiveWhiteBoxTraceV1,
    *,
    role_ref: str | None = None,
    environment_ref: str | None = None,
    context_refs: Tuple[str, ...] = (),
    field_refs: Tuple[str, ...] = (),
    prior_cognition_refs: Tuple[str, ...] = (),
    outcome_candidate: ProfileValueV1 | None = None,
    execution_identity_ref: str | None = None,
) -> LunaCognitiveExecutionProfileV1:
    cycle_indexes = tuple(
        node.observation_cycle_index
        for node in trace.nodes
        if node.observation_cycle_index is not None
    )
    cycle_measure = (
        _observed(max(cycle_indexes) + 1, tuple(node.trace_node_id for node in trace.nodes if node.observation_cycle_index is not None))
        if cycle_indexes
        else _not_observed("observation cycle index unavailable")
    )
    sufficiency_nodes = _nodes(trace, "SUFFICIENCY")
    stop_nodes = _nodes(trace, "STOP_REASON")
    handoff_nodes = _nodes(trace, "DECISION_GOVERNANCE_HANDOFF")
    missing_nodes = _nodes(trace, "EVIDENCE_MISSING")
    return LunaCognitiveExecutionProfileV1(
        execution_profile_id=(
            f"execution-profile:{execution_identity_ref}"
            if execution_identity_ref
            else f"execution-profile:{trace.test_case_ref}"
        ),
        test_case_ref=trace.test_case_ref,
        task_ref=trace.task_ref,
        goal_ref=trace.goal_ref,
        concern_ref=trace.concern_ref,
        role_ref=role_ref,
        environment_ref=environment_ref,
        context_refs=context_refs,
        field_refs=field_refs,
        prior_cognition_refs=prior_cognition_refs,
        attention_node_refs=tuple(node.trace_node_id for node in _nodes(trace, "ATTENTION")),
        attention_transition_count=_not_observed("transition count requires explicit transition instrumentation"),
        selected_target_refs=tuple(node.source_ref for node in _nodes(trace, "ATTENTION")),
        ignored_target_refs=_not_observed("ignored targets are not observable in this foundation"),
        information_need_refs=_refs(trace, "INFORMATION_NEED"),
        observation_demand_refs=_refs(trace, "OBSERVATION_DEMAND"),
        observation_request_refs=_refs(trace, "OBSERVATION_REQUEST"),
        capability_requirement_refs=_refs(trace, "CAPABILITY_REQUIREMENT"),
        observation_cycle_count=cycle_measure,
        roi_refs=tuple(
            str(node.bounded_metadata["roi_ref"])
            for node in trace.nodes
            if "roi_ref" in node.bounded_metadata
        ),
        total_evidence_count=_measure_count(trace, "EVIDENCE"),
        relevant_evidence_count=_measure_count(trace, "EVIDENCE_RELEVANCE"),
        irrelevant_evidence_count=_measure_count(trace, "EVIDENCE_RELEVANCE", not_observed=True),
        conflicting_evidence_count=_measure_count(trace, "EVIDENCE_CONFLICT"),
        uncertain_evidence_count=_measure_count(trace, "EVIDENCE_UNCERTAINTY"),
        missing_evidence_refs=tuple(node.source_ref for node in missing_nodes),
        current_world_candidate_refs=_refs(trace, "CURRENT_WORLD_CANDIDATE"),
        hypothesis_refs=_refs(trace, "HYPOTHESIS") + _refs(trace, "HYPOTHESIS_REVISION"),
        hypothesis_revision_count=_measure_count(trace, "HYPOTHESIS_REVISION"),
        sufficiency_refs=_refs(trace, "SUFFICIENCY"),
        sufficiency_transition_history=tuple(node.summary for node in sufficiency_nodes),
        information_gap_refs=_refs(trace, "INFORMATION_GAP"),
        reobservation_count=_measure_count(trace, "REOBSERVATION"),
        reobservation_reason_refs=tuple(
            str(node.bounded_metadata["reason_ref"])
            for node in _nodes(trace, "REOBSERVATION")
            if "reason_ref" in node.bounded_metadata
        ),
        reobservation_target_refs=tuple(
            str(node.bounded_metadata["target_ref"])
            for node in _nodes(trace, "REOBSERVATION")
            if "target_ref" in node.bounded_metadata
        ),
        capability_change_refs=_not_observed("capability changes require explicit comparison refs"),
        roi_change_refs=_not_observed("ROI changes require explicit comparison refs"),
        stop_reason=(
            _observed(stop_nodes[-1].summary, (stop_nodes[-1].trace_node_id,))
            if stop_nodes
            else _not_observed("stop reason not observed")
        ),
        decision_governance_handoff_ref=(
            _observed(handoff_nodes[-1].source_ref, (handoff_nodes[-1].trace_node_id,))
            if handoff_nodes
            else _not_observed("Decision Governance handoff not observed")
        ),
        outcome_candidate=outcome_candidate or _not_observed("outcome candidate not produced by this foundation"),
        cognitive_transition_count=_observed(len(trace.transition_refs), trace.transition_refs),
        latency=_unavailable("latency instrumentation is outside this foundation"),
        resource_usage=_unavailable("resource instrumentation is outside this foundation"),
        cognitive_trace_ref=trace.trace_id,
        provenance_refs=trace.provenance_refs,
        source_version_refs=trace.source_version_refs,
        invalidation_refs=trace.invalidation_refs,
        test_board_refs=trace.test_board_refs,
        candidate_only=True,
        cognition_mutation=False,
        field_mutation=False,
        current_world_authoritative_write=False,
        world_truth_declared=False,
        model_invocation=False,
        provider_invocation=False,
        observation_execution=False,
        action_execution=False,
        dataset_download=False,
    )

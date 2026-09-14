"""Fixed data constructors for Current Cognitive Context v1 scenarios.

These functions are not runners and are not invoked during module import.
They make no model, network, database, Field Snapshot, or system-time call.
"""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.cognitive_flow.current_cognitive_context.context_builder_v1 import build_current_cognitive_context_v1
from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import AttentionContextV1, GoalContextV1, SubjectContextV1, TaskContextV1, TemporalContextV1
from capabilities.cognitive_flow.current_cognitive_context.context_records_v1 import ContextExclusionRecordV1, ContextInclusionRecordV1
from capabilities.cognitive_flow.current_cognitive_context.context_sufficiency_v1 import ContextSufficiencyResultV1
from capabilities.cognitive_flow.current_cognitive_context.current_cognitive_context_v1 import CurrentCognitiveContextV1
from capabilities.cognitive_flow.current_cognitive_context.information_gap_v1 import InformationGapV1


def _inputs(
    subject_ref: str,
    role: str,
    task_ref: str,
    task_type: str,
    goal_ref: str,
    primary_goal: str,
    attention_targets: Tuple[str, ...],
    trace: str,
) -> Tuple[SubjectContextV1, TaskContextV1, GoalContextV1, TemporalContextV1, AttentionContextV1]:
    return (
        SubjectContextV1(subject_ref, role, f"location:{subject_ref}", (), ("field:read",), {"fixture": True}, trace),
        TaskContextV1(task_ref, task_type, "current", "normal", (), "active", {"fixture": True}, trace),
        GoalContextV1(goal_ref, primary_goal, (), (), (), {"fixture": True}, trace),
        TemporalContextV1("2026-01-01T00:00:00Z", {"scope": "current"}, None, {}, (), {"fixture": True}, trace),
        AttentionContextV1("field:local", attention_targets, "normal", (), ("attention-reason:fixture",), {"fixture": True}, trace),
    )


def _inclusion(snapshot_ref: str, object_ref: str, record_id: str, trace: str) -> ContextInclusionRecordV1:
    return ContextInclusionRecordV1(record_id, snapshot_ref, object_ref, "fixture_required_for_declared_scope", "fixture_scope", "normal", (), {"fixture": True}, trace)


def _exclusion(snapshot_ref: str, object_ref: str, record_id: str, reason: str, trace: str) -> ContextExclusionRecordV1:
    return ContextExclusionRecordV1(record_id, snapshot_ref, object_ref, reason, True, True, snapshot_ref, {"fixture": True}, trace)


def airport_pickup_context_v1() -> CurrentCognitiveContextV1:
    """Construct fixed airport-pickup context without explaining flight status."""

    snapshot_ref = "snapshot:airport:shared:v1"
    trace = "trace:context:airport:pickup:v1"
    subject, task, goal, temporal, attention = _inputs("subject:pickup", "arrival_meeter", "task:pickup", "pickup", "goal:arrival_exit", "reach_arrival_exit", ("unit:terminal", "unit:arrivals", "unit:arrival_exit"), trace)
    selected_units = ("unit:terminal", "unit:arrivals", "unit:arrival_exit", "unit:parking")
    selected_relations = ("relation:arrival_path",)
    selected_states = ("state:flight", "state:arrival_exit", "state:time")
    inclusions = tuple(_inclusion(snapshot_ref, ref, f"record:pickup:include:{index}", trace) for index, ref in enumerate(selected_units + selected_relations + selected_states))
    exclusions = (
        _exclusion(snapshot_ref, "unit:commercial_area", "record:pickup:exclude:1", "irrelevant_to_current_task", trace),
        _exclusion(snapshot_ref, "unit:departures", "record:pickup:exclude:2", "outside_attention_scope", trace),
    )
    sufficiency = ContextSufficiencyResultV1("sufficient", ("fixture_scope_complete",), (), (), "context:airport:pickup:v1", {"fixture": True}, trace)
    return build_current_cognitive_context_v1(context_id="context:airport:pickup:v1", context_version="v1", previous_context_ref=None, superseded_by_ref=None, lifecycle_status="built", field_ref="field:airport:v1", snapshot_ref=snapshot_ref, subject_context=subject, task_context=task, goal_context=goal, temporal_context=temporal, attention_context=attention, schema_refs=("schema:airport:v1",), selected_field_unit_refs=selected_units, selected_relation_refs=selected_relations, selected_state_refs=selected_states, selected_history_refs=(), selected_evidence_refs=("evidence:flight",), inclusion_records=inclusions, exclusion_records=exclusions, information_gaps=(), sufficiency_result=sufficiency, context_boundary={"fixture": "airport_pickup"}, invalidation_reasons=(), refresh_required=False, provenance={"fixture": True}, trace=trace, created_from_refs=(snapshot_ref, "evidence:flight"))


def shopping_mall_observation_context_v1() -> CurrentCognitiveContextV1:
    """Construct fixed shop-status context without business interpretation."""

    snapshot_ref = "snapshot:shopping_mall:v1"
    trace = "trace:context:shopping_mall:v1"
    subject, task, goal, temporal, attention = _inputs("subject:observer", "observer", "task:mall_observation", "observation", "goal:need_for_observation", "assess_context_completeness", ("unit:closed_shop", "unit:renovating_shop"), trace)
    selected_units = ("unit:closed_shop", "unit:renovating_shop")
    selected_relations = ("relation:regional_distribution",)
    selected_states = ("state:foot_traffic",)
    selected_history = ("history:shop_status",)
    selected_evidence = ("evidence:mall_notice",)
    inclusions = tuple(_inclusion(snapshot_ref, ref, f"record:mall:include:{index}", trace) for index, ref in enumerate(selected_units + selected_relations + selected_states + selected_history + selected_evidence))
    gaps = (
        InformationGapV1("gap:mall:closure_time", "missing_time", "unit:closed_shop", "partial closure time unavailable", "material", "goal:need_for_observation", "task:mall_observation", {"scope_ref": "unit:closed_shop"}, (), {"fixture": True}, trace),
        InformationGapV1("gap:mall:notice_stale", "stale_information", "evidence:mall_notice", "notice freshness is uncertain", "material", "goal:need_for_observation", "task:mall_observation", {"scope_ref": "evidence:mall_notice"}, ("evidence:mall_notice",), {"fixture": True}, trace),
    )
    sufficiency = ContextSufficiencyResultV1("conditionally_sufficient", ("fixture_time_gap_retained",), tuple(gap.gap_id for gap in gaps), ("condition:retain_temporal_uncertainty",), "context:mall:observation:v1", {"fixture": True}, trace)
    return build_current_cognitive_context_v1(context_id="context:mall:observation:v1", context_version="v1", previous_context_ref=None, superseded_by_ref=None, lifecycle_status="built", field_ref="field:shopping_mall:v1", snapshot_ref=snapshot_ref, subject_context=subject, task_context=task, goal_context=goal, temporal_context=temporal, attention_context=attention, schema_refs=("schema:shopping_mall:v1",), selected_field_unit_refs=selected_units, selected_relation_refs=selected_relations, selected_state_refs=selected_states, selected_history_refs=selected_history, selected_evidence_refs=selected_evidence, inclusion_records=inclusions, exclusion_records=(), information_gaps=gaps, sufficiency_result=sufficiency, context_boundary={"fixture": "shopping_mall_observation"}, invalidation_reasons=(), refresh_required=False, provenance={"fixture": True}, trace=trace, created_from_refs=(snapshot_ref, "evidence:mall_notice"))


def blind_navigation_context_v1() -> CurrentCognitiveContextV1:
    """Construct fixed indoor-navigation context without navigation instruction."""

    snapshot_ref = "snapshot:indoor_navigation:v1"
    trace = "trace:context:blind_navigation:v1"
    subject, task, goal, temporal, attention = _inputs("subject:blind_user", "pedestrian", "task:indoor_navigation", "navigation", "goal:reach_exit", "reach_exit", ("unit:current_location", "unit:exit", "unit:crossing"), trace)
    selected_units = ("unit:current_location", "unit:exit", "unit:crossing")
    selected_relations = ("relation:passable_path",)
    selected_states = ("state:obstacle", "state:path_access")
    selected_evidence = ("evidence:wayfinding",)
    inclusions = tuple(_inclusion(snapshot_ref, ref, f"record:navigation:include:{index}", trace) for index, ref in enumerate(selected_units + selected_relations + selected_states + selected_evidence))
    exclusions = (_exclusion(snapshot_ref, "unit:commercial_ad", "record:navigation:exclude:1", "irrelevant_to_current_task", trace), _exclusion(snapshot_ref, "unit:distant_shop", "record:navigation:exclude:2", "outside_spatial_scope", trace))
    gaps = (
        InformationGapV1("gap:navigation:obstacle", "stale_information", "state:obstacle", "crossing obstacle state is stale", "material", "goal:reach_exit", "task:indoor_navigation", {"scope_ref": "unit:crossing"}, (), {"fixture": True}, trace),
        InformationGapV1("gap:navigation:wayfinding", "insufficient_resolution", "evidence:wayfinding", "wayfinding text resolution is insufficient", "material", "goal:reach_exit", "task:indoor_navigation", {"scope_ref": "evidence:wayfinding"}, ("evidence:wayfinding",), {"fixture": True}, trace),
    )
    sufficiency = ContextSufficiencyResultV1("insufficient", ("fixture_navigation_gaps",), tuple(gap.gap_id for gap in gaps), (), "context:navigation:v1", {"fixture": True}, trace)
    return build_current_cognitive_context_v1(context_id="context:navigation:v1", context_version="v1", previous_context_ref=None, superseded_by_ref=None, lifecycle_status="built", field_ref="field:indoor_navigation:v1", snapshot_ref=snapshot_ref, subject_context=subject, task_context=task, goal_context=goal, temporal_context=temporal, attention_context=attention, schema_refs=("schema:indoor_navigation:v1",), selected_field_unit_refs=selected_units, selected_relation_refs=selected_relations, selected_state_refs=selected_states, selected_history_refs=(), selected_evidence_refs=selected_evidence, inclusion_records=inclusions, exclusion_records=exclusions, information_gaps=gaps, sufficiency_result=sufficiency, context_boundary={"fixture": "blind_navigation"}, invalidation_reasons=(), refresh_required=False, provenance={"fixture": True}, trace=trace, created_from_refs=(snapshot_ref, "evidence:wayfinding"))


def shared_airport_multi_context_v1() -> Tuple[CurrentCognitiveContextV1, CurrentCognitiveContextV1, CurrentCognitiveContextV1]:
    """Construct three different Contexts using the same fixed airport Snapshot reference."""

    pickup = airport_pickup_context_v1()
    snapshot_ref = pickup.snapshot_ref
    trace = "trace:context:airport:multi:v1"
    staff_inputs = _inputs("subject:staff", "safety_staff", "task:safety_check", "inspection", "goal:restricted_area", "inspect_restricted_area", ("unit:restricted_area",), trace)
    navigation_inputs = _inputs("subject:airport_blind_user", "pedestrian", "task:airport_navigation", "navigation", "goal:airport_exit", "reach_arrival_exit", ("unit:arrivals", "unit:arrival_exit"), trace)

    def assemble(
        context_id: str,
        inputs: Tuple[SubjectContextV1, TaskContextV1, GoalContextV1, TemporalContextV1, AttentionContextV1],
        units: Tuple[str, ...],
        relations: Tuple[str, ...],
        states: Tuple[str, ...],
        evidence: Tuple[str, ...],
        gap: InformationGapV1,
    ) -> CurrentCognitiveContextV1:
        subject, task, goal, temporal, attention = inputs
        inclusions = tuple(_inclusion(snapshot_ref, ref, f"record:{context_id}:include:{index}", trace) for index, ref in enumerate(units + relations + states + evidence))
        sufficiency = ContextSufficiencyResultV1("conditionally_sufficient", ("fixture_multi_context",), (gap.gap_id,), (), context_id, {"fixture": True}, trace)
        return build_current_cognitive_context_v1(context_id=context_id, context_version="v1", previous_context_ref=None, superseded_by_ref=None, lifecycle_status="built", field_ref="field:airport:v1", snapshot_ref=snapshot_ref, subject_context=subject, task_context=task, goal_context=goal, temporal_context=temporal, attention_context=attention, schema_refs=("schema:airport:v1",), selected_field_unit_refs=units, selected_relation_refs=relations, selected_state_refs=states, selected_history_refs=(), selected_evidence_refs=evidence, inclusion_records=inclusions, exclusion_records=(), information_gaps=(gap,), sufficiency_result=sufficiency, context_boundary={"fixture": "shared_airport"}, invalidation_reasons=(), refresh_required=False, provenance={"fixture": True}, trace=trace, created_from_refs=(snapshot_ref,) + evidence)

    staff = assemble("context:airport:safety:v1", staff_inputs, ("unit:restricted_area",), ("relation:restricted_entry",), ("state:restricted_entry",), ("evidence:restricted_notice",), InformationGapV1("gap:airport:restricted", "conflicting_evidence", "unit:restricted_area", "restricted-area evidence needs review", "material", "goal:restricted_area", "task:safety_check", {"scope_ref": "unit:restricted_area"}, ("evidence:restricted_notice",), {"fixture": True}, trace))
    navigation = assemble("context:airport:navigation:v1", navigation_inputs, ("unit:arrivals", "unit:arrival_exit"), ("relation:accessible_arrival_path",), ("state:arrival_path",), ("evidence:airport_wayfinding",), InformationGapV1("gap:airport:path", "stale_information", "state:arrival_path", "arrival path state is stale", "material", "goal:airport_exit", "task:airport_navigation", {"scope_ref": "relation:accessible_arrival_path"}, ("evidence:airport_wayfinding",), {"fixture": True}, trace))
    return pickup, staff, navigation

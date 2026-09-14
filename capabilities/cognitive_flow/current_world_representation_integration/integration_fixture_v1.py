"""Fixed, deterministic fixtures for CWR integration DryRun v1."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Mapping, Tuple

from capabilities.cognitive_flow.current_cognitive_context.context_builder_v1 import (
    build_current_cognitive_context_v1,
)
from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import (
    AttentionContextV1,
    GoalContextV1,
    SubjectContextV1,
    TaskContextV1,
    TemporalContextV1,
)
from capabilities.cognitive_flow.current_cognitive_context.context_records_v1 import (
    ContextExclusionRecordV1,
    ContextInclusionRecordV1,
)
from capabilities.cognitive_flow.current_cognitive_context.context_sufficiency_v1 import (
    ContextSufficiencyResultV1,
)
from capabilities.cognitive_flow.current_cognitive_context.current_cognitive_context_v1 import (
    CurrentCognitiveContextV1,
)
from capabilities.cognitive_flow.current_cognitive_context.information_gap_v1 import InformationGapV1
from capabilities.cognitive_flow.field_kernel.core.field_identity_v1 import FieldIdentityV1
from capabilities.cognitive_flow.field_kernel.core.field_relation_v1 import FieldRelationV1
from capabilities.cognitive_flow.field_kernel.core.field_snapshot_v1 import FieldSnapshotV1
from capabilities.cognitive_flow.field_kernel.core.field_state_v1 import (
    FieldStateV1 as FieldKernelStateV1,
    field_state_from_reducer_output_v1,
)
from capabilities.cognitive_flow.field_kernel.core.field_unit_v1 import FieldUnitV1
from capabilities.cognitive_flow.field_kernel.temporal_evolution.history_projection_v1 import (
    FieldHistoryProjectionV1,
    build_field_history_projection_v1,
)
from capabilities.cognitive_flow.field_kernel.temporal_evolution.state_version_v1 import StateVersionV1
from capabilities.cognitive_flow.field_kernel.temporal_evolution.transition_record_v1 import TransitionRecordV1
from capabilities.midplatform.core.field_state_read_model.module.field_state_read_model_module_types_v1 import (
    FieldStateReadResultV1,
    get_default_boundary_flags_v1,
)
from capabilities.midplatform.core.field_state_reducer.field_state_reducer_types_v1 import (
    FieldStateReducerOutputV1,
    FieldStateV1 as ReducerFieldStateV1,
)

from .current_world_representation_envelope_v1 import CurrentWorldRepresentationEnvelopeV1
from .integration_types_v1 import INTEGRATION_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class IntegrationCaseFixtureV1:
    case_id: str
    case_name: str
    admitted_event: Mapping[str, Any]
    reducer_output: FieldStateReducerOutputV1
    field_identity: FieldIdentityV1
    field_units: Tuple[FieldUnitV1, ...]
    field_relations: Tuple[FieldRelationV1, ...]
    field_state: FieldKernelStateV1
    state_versions: Tuple[StateVersionV1, ...]
    transitions: Tuple[TransitionRecordV1, ...]
    history_projection: FieldHistoryProjectionV1
    snapshot: FieldSnapshotV1
    read_model_result: FieldStateReadResultV1
    contexts: Tuple[CurrentCognitiveContextV1, ...]
    active_context_ref: str | None
    envelope: CurrentWorldRepresentationEnvelopeV1
    expected_failure_codes: Tuple[str, ...]
    expected_warning_codes: Tuple[str, ...]
    expected_analysis_boundary_admission: bool


def _provenance(case_id: str) -> Mapping[str, str]:
    return {"fixture": "fixed", "case_id": case_id, "simulation_only": "true"}


def context_reference_v1(context: CurrentCognitiveContextV1) -> str:
    """Return the immutable fixture reference for one Context version."""

    return f"{context.context_id}@{context.context_version}"


def _admitted_event(case_id: str) -> Mapping[str, Any]:
    return {
        "event_ref": f"admitted_event:{case_id}",
        "event_id": f"event:{case_id}",
        "field_ref": "field:airport:terminal_a",
        "admission_status": "admitted_event",
        "reducer_eligible": True,
        "evidence_refs": ("evidence:A",),
        "source_chain": ("fixture:admission",),
        "trace_ref": f"trace:{case_id}",
        "temporal_assessment": {"status": "valid", "reference": "time:fixed:2026-07-22T00:00:00Z"},
    }


def _structure(case_id: str) -> tuple[FieldIdentityV1, Tuple[FieldUnitV1, ...], Tuple[FieldRelationV1, ...]]:
    identity = FieldIdentityV1(
        field_id="field:airport:terminal_a",
        field_type="airport_terminal",
        parent_field_ref=None,
        physical_context={"anchor": "fixture:terminal_a"},
        social_context={"public_access": "governed_candidate"},
        task_context={"scope": "fixture_only"},
        provenance=_provenance(case_id),
    )
    entrance = FieldUnitV1("unit:airport:entrance", "entrance", identity.field_id, {"label": "A"}, (), _provenance(case_id))
    arrival = FieldUnitV1("unit:airport:arrivals", "arrival_area", identity.field_id, {"label": "arrivals"}, (), _provenance(case_id))
    service_desk = FieldUnitV1("unit:airport:service_desk", "service_desk", identity.field_id, {"label": "service"}, (), _provenance(case_id))
    relation = FieldRelationV1("relation:airport:contains", identity.field_id, "contains", entrance.unit_id, _provenance(case_id))
    return identity, (entrance, arrival, service_desk), (relation,)


def _reducer_output(case_id: str, valid_from: str | None) -> tuple[FieldStateReducerOutputV1, FieldKernelStateV1]:
    reducer_state = ReducerFieldStateV1(
        state_id=f"state:{case_id}",
        field_id="field:airport:terminal_a",
        state_type="accessibility_state",
        state_value={"status": "open_candidate"},
        state_status="candidate",
        confidence=0.7,
        effective_from=valid_from,
        effective_until=None,
        source_event_ids=(f"event:{case_id}",),
        provenance_chain=("fixture:reducer_output",),
        created_at="time:fixed:2026-07-22T00:00:00Z",
        updated_at="time:fixed:2026-07-22T00:00:00Z",
    )
    output = FieldStateReducerOutputV1(
        resulting_state=reducer_state,
        reduction_decision="fixture_reducer_output_only",
        applied_event_ids=(f"event:{case_id}",),
        rejected_event_ids=(),
        ignored_event_ids=(),
        conflict_ids=(),
        unresolved_conditions=(),
        reducer_trace={"trace_ref": f"trace:{case_id}", "fixture_only": True},
        deterministic_replay_key=f"replay:{case_id}",
        state_change_type="placeholder_only",
    )
    state = field_state_from_reducer_output_v1(
        {
            "produced_by": "field_state_reducer",
            "reducer_output_ref": f"reducer_output:{case_id}",
            "state_id": reducer_state.state_id,
            "target_ref": "unit:airport:entrance",
            "state_type": reducer_state.state_type,
            "value": reducer_state.state_value,
            "valid_time": {"effective_from": valid_from, "effective_until": None},
            "evidence_refs": ("evidence:A",),
            "source_chain": (f"admitted_event:{case_id}",),
            "trace_ref": f"trace:{case_id}",
            "provenance": _provenance(case_id),
        }
    )
    return output, state


def _temporal(case_id: str, state: FieldKernelStateV1, valid_from: str | None, unknown_time: bool) -> tuple[Tuple[StateVersionV1, ...], Tuple[TransitionRecordV1, ...], FieldHistoryProjectionV1]:
    version_ref = f"state_version:{case_id}:v1"
    version = StateVersionV1(
        state_version_id=version_ref,
        field_ref="field:airport:terminal_a",
        field_state_ref=state.state_id,
        previous_state_version_ref=None,
        state_type=state.state_type,
        state_value=state.value,
        valid_from=valid_from,
        valid_until=None,
        transition_record_ref=f"transition:{case_id}:created",
        provenance=_provenance(case_id),
        created_at="time:fixed:2026-07-22T00:00:00Z",
        trace_ref=f"trace:{case_id}",
        temporal_uncertainty={"valid_from_status": "unknown" if unknown_time else "known"},
    )
    transition = TransitionRecordV1(
        transition_id=f"transition:{case_id}:created",
        source_state_version=None,
        target_state_version=version_ref,
        event_ref=f"admitted_event:{case_id}",
        transition_type="created",
        transition_time=None if unknown_time else "time:fixed:2026-07-22T00:00:00Z",
        provenance=_provenance(case_id),
        trace_ref=f"trace:{case_id}",
        transition_time_status="unknown" if unknown_time else "known",
    )
    history = build_field_history_projection_v1(
        "field:airport:terminal_a", (version,), (transition,), "time:fixed:2026-07-22T00:00:00Z", _provenance(case_id), f"trace:{case_id}"
    )
    return (version,), (transition,), history


def _snapshot(case_id: str, units: Tuple[FieldUnitV1, ...], relations: Tuple[FieldRelationV1, ...], state: FieldKernelStateV1, snapshot_id: str) -> FieldSnapshotV1:
    return FieldSnapshotV1(snapshot_id, "field:airport:terminal_a", units, relations, (state,), "time:fixed:2026-07-22T00:00:00Z", _provenance(case_id))


def _read_model_result(case_id: str, state: FieldKernelStateV1, version_ref: str, snapshot_ref: str) -> FieldStateReadResultV1:
    return FieldStateReadResultV1(
        query_id=f"read_query:{case_id}",
        read_status="read_ready",
        projection={"snapshot_ref": snapshot_ref, "state_ref": state.state_id, "status": "open_candidate"},
        state_version=version_ref,
        source_state_ref=state.state_id,
        provenance_refs=(f"reducer_output:{case_id}", "evidence:A"),
        trace_ref=f"trace:{case_id}",
        replay_key=f"replay:{case_id}",
        boundary_flags=get_default_boundary_flags_v1(),
        runtime_executed=False,
    )


def _context(case_id: str, snapshot_ref: str, context_id: str, version: str, *, status: str, previous: str | None, refresh_required: bool, selected_units: Tuple[str, ...], selected_evidence: Tuple[str, ...], gaps: Tuple[InformationGapV1, ...], sufficiency: str, invalidations: Tuple[str, ...] = (), subject_location: str | None = "unit:airport:entrance") -> CurrentCognitiveContextV1:
    trace = f"trace:{case_id}:{context_id}"
    subject = SubjectContextV1("subject:fixture", "fixture_subject", subject_location, (), ("field:airport:terminal_a",), _provenance(case_id), trace)
    task = TaskContextV1(f"task:{context_id}", "fixture_task", "active", "normal", (), "active", _provenance(case_id), trace)
    goal = GoalContextV1(f"goal:{context_id}", "fixture_goal", (), (), (), _provenance(case_id), trace)
    temporal = TemporalContextV1("time:fixed:2026-07-22T00:00:00Z", {"status": "fixed"}, None, {}, (), _provenance(case_id), trace)
    attention = AttentionContextV1("field_scope", selected_units, "normal", (), (), _provenance(case_id), trace)
    selected_states = (f"state:{case_id}",)
    selected_history = (f"history:{case_id}",)
    inclusion = ContextInclusionRecordV1(f"inclusion:{context_id}", snapshot_ref, selected_units[0], "fixture_scope", "fixture", "normal", selected_evidence, _provenance(case_id), trace)
    exclusion_target = {
        "unit:airport:entrance": "unit:airport:arrivals",
        "unit:airport:arrivals": "unit:airport:service_desk",
        "unit:airport:service_desk": "unit:airport:entrance",
    }[selected_units[0]]
    exclusion = ContextExclusionRecordV1(f"exclusion:{context_id}", snapshot_ref, exclusion_target, "outside_attention_scope", True, True, snapshot_ref, _provenance(case_id), trace)
    sufficiency_result = ContextSufficiencyResultV1(sufficiency, (f"sufficiency:{sufficiency}",), tuple(gap.gap_id for gap in gaps), (), f"context:{context_id}:{version}", _provenance(case_id), trace)
    return build_current_cognitive_context_v1(
        context_id=f"context:{context_id}", context_version=version, previous_context_ref=previous, superseded_by_ref=None,
        lifecycle_status=status, field_ref="field:airport:terminal_a", snapshot_ref=snapshot_ref,
        subject_context=subject, task_context=task, goal_context=goal, temporal_context=temporal, attention_context=attention,
        schema_refs=("schema:fixture",), selected_field_unit_refs=selected_units, selected_relation_refs=("relation:airport:contains",),
        selected_state_refs=selected_states, selected_history_refs=selected_history, selected_evidence_refs=selected_evidence,
        inclusion_records=(inclusion,), exclusion_records=(exclusion,), information_gaps=gaps, sufficiency_result=sufficiency_result,
        context_boundary={"fixture": "fixed"}, invalidation_reasons=invalidations, refresh_required=refresh_required,
        provenance=_provenance(case_id), trace=trace, created_from_refs=(snapshot_ref, f"history:{case_id}", *selected_evidence),
    )


def _gap(case_id: str, gap_id: str, gap_type: str, text: str) -> InformationGapV1:
    return InformationGapV1(gap_id, gap_type, "unit:airport:entrance", text, "critical", "goal:fixture", "task:fixture", {"field_ref": "field:airport:terminal_a"}, ("evidence:A",), _provenance(case_id), f"trace:{case_id}:{gap_id}")


def _case(case_id: str, case_name: str, *, unknown_time: bool = False, status: str = "complete", failures: Tuple[str, ...] = (), warnings: Tuple[str, ...] = (), contexts: Tuple[CurrentCognitiveContextV1, ...] | None = None, active_context_ref: str | None = None, analysis_allowed: bool = True, envelope_evidence: Tuple[str, ...] = ("evidence:A",)) -> IntegrationCaseFixtureV1:
    identity, units, relations = _structure(case_id)
    output, state = _reducer_output(case_id, None if unknown_time else "time:fixed:2026-07-22T00:00:00Z")
    versions, transitions, history = _temporal(case_id, state, None if unknown_time else "time:fixed:2026-07-22T00:00:00Z", unknown_time)
    snapshot = _snapshot(case_id, units, relations, state, f"snapshot:{case_id}:v1")
    read_result = _read_model_result(case_id, state, versions[0].state_version_id, snapshot.snapshot_id)
    default_context = _context(case_id, snapshot.snapshot_id, case_id, "v1", status="active", previous=None, refresh_required=False, selected_units=(units[0].unit_id,), selected_evidence=("evidence:A",), gaps=(), sufficiency="sufficient")
    final_contexts = contexts if contexts is not None else (default_context,)
    final_active = active_context_ref if active_context_ref is not None else context_reference_v1(final_contexts[-1])
    envelope = CurrentWorldRepresentationEnvelopeV1(
        INTEGRATION_SCHEMA_VERSION_V1, f"envelope:{case_id}", identity.field_id, identity.field_id,
        tuple([unit.unit_id for unit in units] + [relation.relation_id for relation in relations]), (state.state_id,),
        tuple(version.state_version_id for version in versions), f"history:{case_id}", snapshot.snapshot_id,
        tuple(context_reference_v1(context) for context in final_contexts), final_active, (f"admitted_event:{case_id}",), envelope_evidence,
        {"time_status": "unknown" if unknown_time else "known"}, status, failures, _provenance(case_id), f"trace:{case_id}",
    )
    return IntegrationCaseFixtureV1(case_id, case_name, _admitted_event(case_id), output, identity, units, relations, state, versions, transitions, history, snapshot, read_result, final_contexts, final_active, envelope, failures, warnings, analysis_allowed)


def build_integration_fixtures_v1() -> Tuple[IntegrationCaseFixtureV1, ...]:
    complete = _case("case_01_complete", "complete_reference_chain")
    unknown = _case("case_02_unknown_time", "unknown_time_preserved", unknown_time=True, status="incomplete", failures=("state_version_chain_incomplete", "temporal_order_unknown"), warnings=("unknown_time_preserved",), analysis_allowed=True)

    stale_base = _case("case_03_snapshot_refresh", "snapshot_refresh_context_stale")
    snap_v2 = _snapshot("case_03_snapshot_refresh", stale_base.field_units, stale_base.field_relations, stale_base.field_state, "snapshot:case_03_snapshot_refresh:v2")
    context_v1 = _context("case_03_snapshot_refresh", stale_base.snapshot.snapshot_id, "refresh", "v1", status="active", previous=None, refresh_required=False, selected_units=("unit:airport:entrance",), selected_evidence=("evidence:A",), gaps=(), sufficiency="sufficient")
    context_v2 = _context("case_03_snapshot_refresh", snap_v2.snapshot_id, "refresh", "v2", status="active", previous=context_reference_v1(context_v1), refresh_required=False, selected_units=("unit:airport:entrance",), selected_evidence=("evidence:A",), gaps=(), sufficiency="sufficient")
    stale = _case("case_03_snapshot_refresh", "snapshot_refresh_context_stale", contexts=(context_v1, context_v2), active_context_ref=context_reference_v1(context_v2), failures=("context_stale",), warnings=("context_v1_refresh_required",), analysis_allowed=True)
    stale = replace(
        stale,
        snapshot=snap_v2,
        read_model_result=_read_model_result("case_03_snapshot_refresh", stale.field_state, stale.state_versions[0].state_version_id, snap_v2.snapshot_id),
        envelope=replace(stale.envelope, snapshot_ref=snap_v2.snapshot_id),
    )

    multi_base = _case("case_04_multi_context", "same_snapshot_multiple_contexts")
    pickup = _context("case_04_multi_context", multi_base.snapshot.snapshot_id, "pickup", "v1", status="active", previous=None, refresh_required=False, selected_units=("unit:airport:entrance",), selected_evidence=("evidence:A",), gaps=(_gap("case_04_multi_context", "gap:pickup", "missing_location", "arrival exit unknown"),), sufficiency="conditionally_sufficient")
    security = _context("case_04_multi_context", multi_base.snapshot.snapshot_id, "security", "v1", status="active", previous=None, refresh_required=False, selected_units=("unit:airport:arrivals",), selected_evidence=("evidence:A",), gaps=(_gap("case_04_multi_context", "gap:security", "missing_state", "restricted state unknown"),), sufficiency="unknown")
    access = _context("case_04_multi_context", multi_base.snapshot.snapshot_id, "accessibility", "v1", status="active", previous=None, refresh_required=False, selected_units=("unit:airport:service_desk",), selected_evidence=("evidence:A",), gaps=(_gap("case_04_multi_context", "gap:access", "missing_relation", "accessible route unknown"),), sufficiency="conditionally_sufficient")
    multi = _case("case_04_multi_context", "same_snapshot_multiple_contexts", contexts=(pickup, security, access), active_context_ref=context_reference_v1(pickup))

    insufficient_base = _case("case_05_context_insufficient", "context_insufficient_blocks_analysis")
    insufficient_context = _context("case_05_context_insufficient", insufficient_base.snapshot.snapshot_id, "insufficient", "v1", status="active", previous=None, refresh_required=True, selected_units=("unit:airport:entrance",), selected_evidence=("evidence:A",), gaps=(_gap("case_05_context_insufficient", "gap:critical", "missing_location", "subject location unknown"),), sufficiency="insufficient", subject_location=None)
    insufficient = _case("case_05_context_insufficient", "context_insufficient_blocks_analysis", status="incomplete", failures=("context_insufficient",), contexts=(insufficient_context,), active_context_ref=context_reference_v1(insufficient_context), analysis_allowed=False)

    revoked_base = _case("case_06_evidence_revoked", "evidence_revoked_refresh_required")
    revoked_context = _context("case_06_evidence_revoked", revoked_base.snapshot.snapshot_id, "revoked", "v1", status="active", previous=None, refresh_required=True, selected_units=("unit:airport:entrance",), selected_evidence=("evidence:A",), gaps=(_gap("case_06_evidence_revoked", "gap:revoked", "conflicting_evidence", "source evidence revoked"),), sufficiency="unknown", invalidations=("critical_evidence_revoked",))
    revoked = _case("case_06_evidence_revoked", "evidence_revoked_refresh_required", status="stale", failures=("evidence_revoked",), warnings=("refresh_required",), contexts=(revoked_context,), active_context_ref=context_reference_v1(revoked_context), analysis_allowed=False)
    return (complete, unknown, stale, multi, insufficient, revoked)

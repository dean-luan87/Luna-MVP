"""Controlled temporal authority sandbox engine for Architecture Stability Gate B.

The engine creates each scenario through real owner APIs, performs one real
owner lifecycle transition, and then reuses the original Runtime Grant at a
controlled effect seam.  It never invokes a real provider or mutates a
production source record directly.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

from capabilities.midplatform.core.action_governance.action_admission_governance_v1 import (
    ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1,
    query_current_admitted_action_v1,
    revoke_admitted_action_v1,
)
from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    invalidate_runtime_safety_prerequisite_v1,
    query_current_runtime_safety_prerequisite_v1,
)
from capabilities.midplatform.core.brain_governance.concern_governance_v1 import (
    BRAIN_CONTROLLED_PROFILE_REF,
    close_concern,
    query_current_concern,
    supersede_concern,
)
from capabilities.midplatform.core.brain_governance.cognitive_grant_governance_v1 import (
    query_current_cognitive_grant,
    revoke_cognitive_grant,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.working_envelope_governance_v1 import (
    WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1,
    invalidate_working_envelope_v1,
    query_current_working_envelope_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_evidence_types_v1 import (
    CAPABILITY_KIND,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_provider_adapter_v1 import (
    build_vision_provider_admission_candidate_v1,
    run_authorized_vision_provider_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.raw_camera_stream_types_v1 import (
    RawFrameRecordV1,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_authorization_state_v1 import (
    query_active_authorization_for_grant,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    invalidate_runtime_authorization_state,
)

from .fixtures_v1 import TemporalAuthorityFixtureV1, build_temporal_authority_fixture


SCENARIO_IDS = (
    "B01_STABLE_AUTHORIZED_EFFECT",
    "B02_ACTION_REVOKED_AFTER_AUTHORIZATION",
    "B03_WORKING_ENVELOPE_INVALIDATED_AFTER_AUTHORIZATION",
    "B04_COGNITIVE_GRANT_REVOKED_AFTER_AUTHORIZATION",
    "B05_CONCERN_SUPERSEDED_AFTER_AUTHORIZATION",
    "B06_SAFETY_INVALIDATED_AFTER_AUTHORIZATION",
    "B07_RUNTIME_AUTHORIZATION_INVALIDATED",
)


def _state(value: Any) -> str:
    if value is None:
        return "NOT_CURRENT"
    return str(
        getattr(
            value,
            "status",
            getattr(value, "state", getattr(value, "lifecycle_status", "CURRENT")),
        )
    )


def _event(
    *,
    scenario_id: str,
    order: int,
    step: str,
    canonical_fact_type: str,
    canonical_ref: str,
    owner: str,
    owner_state_before: str,
    owner_transition: str,
    owner_state_after: str,
    grant: Any,
    authorization_state: str,
    effect_boundary_result: str,
    reason: str,
) -> Dict[str, Any]:
    return {
        "scenario_id": scenario_id,
        "step": step,
        "order": order,
        "canonical_fact_type": canonical_fact_type,
        "canonical_ref": canonical_ref,
        "owner": owner,
        "owner_state_before": owner_state_before,
        "owner_transition": owner_transition,
        "owner_state_after": owner_state_after,
        "runtime_grant_ref": getattr(grant, "grant_ref", ""),
        "runtime_authorization_ref": getattr(grant, "authorization_ref", ""),
        "authorization_state": authorization_state,
        "effect_boundary_result": effect_boundary_result,
        "reason": reason,
    }


def _initial_trace(fixture: TemporalAuthorityFixtureV1) -> list[Dict[str, Any]]:
    scenario_id = fixture.scenario_id
    grant = fixture.grant
    records = (
        ("Concern", fixture.concern.concern_ref, "Brain Governance", _state(fixture.concern)),
        (
            "CognitiveGrant",
            fixture.cognitive_grant.grant_ref,
            "Brain Governance",
            _state(fixture.cognitive_grant),
        ),
        (
            "CognitiveStateVersion",
            fixture.state_version.version_ref,
            "Cognitive State Formation Governance",
            "CURRENT",
        ),
        (
            "WorkingEnvelope",
            fixture.envelope.envelope_ref,
            "Working Envelope Governance",
            _state(fixture.envelope),
        ),
        (
            "AdmittedAction",
            fixture.admitted_action.admitted_action_ref,
            "Action Governance",
            _state(fixture.admitted_action),
        ),
        (
            "RuntimeAuthorization",
            grant.authorization_ref,
            "Permission / Admission Manager",
            "AUTHORIZED",
        ),
    )
    return [
        _event(
            scenario_id=scenario_id,
            order=index,
            step="OWNER_ISSUANCE",
            canonical_fact_type=fact_type,
            canonical_ref=canonical_ref,
            owner=owner,
            owner_state_before="NONE",
            owner_transition="ISSUE",
            owner_state_after=state,
            grant=grant,
            authorization_state="AUTHORIZED",
            effect_boundary_result="NOT_REACHED",
            reason="real owner-issued setup",
        )
        for index, (fact_type, canonical_ref, owner, state) in enumerate(records)
    ]


def _frame(scenario_id: str) -> RawFrameRecordV1:
    return RawFrameRecordV1(
        frame_id=f"phase-b-frame:{scenario_id}",
        stream_session_id=f"phase-b-stream:{scenario_id}",
        source_type="IMAGE_FILE",
        source_ref=f"synthetic://phase-b/{scenario_id}",
        device_ref=None,
        frame_index=0,
        captured_at=1,
        width=1,
        height=1,
        pixel_format="SYNTHETIC",
        frame_payload_ref=f"phase-b-payload:{scenario_id}",
        content_hash=f"phase-b-hash:{scenario_id}",
        temporal_validity={"stale": False, "expired": False},
        sensitivity="LOW",
        trace_ref=f"trace:phase-b-frame:{scenario_id}",
        provenance_refs=(f"provenance:phase-b-frame:{scenario_id}",),
    )


def _admission(fixture: TemporalAuthorityFixtureV1):
    scenario_id = fixture.scenario_id
    grant = fixture.grant
    return build_vision_provider_admission_candidate_v1(
        observation_demand_ref=f"phase-b:demand:{scenario_id}",
        observation_request_ref=f"phase-b:request:{scenario_id}",
        capability_requirement_ref=f"capability-requirement:phase-b:{scenario_id}",
        provider_session_ref=f"phase-b:provider-session:{scenario_id}",
        provider_candidate_ref=grant.provider_candidate_ref,
        model_candidate_ref=f"phase-b:model:{scenario_id}",
        model_admission_ref=f"phase-b:model-admission:{scenario_id}",
        region_scope_candidate="bounded-frame",
        expected_evidence=(CAPABILITY_KIND,),
        bounded=True,
        provider_admitted=True,
        trace_ref=f"trace:phase-b-admission:{scenario_id}",
        provenance_refs=(f"provenance:phase-b-admission:{scenario_id}",),
        canonical_capability_model_binding_ref=f"phase-b:capability-binding:{scenario_id}",
        canonical_capability_model_binding_version="v1",
        canonical_runtime_admission_ref=f"phase-b:runtime-admission:{scenario_id}",
        canonical_runtime_admission_version="v1",
        canonical_model_provider_binding_ref=f"phase-b:provider-binding:{scenario_id}",
        canonical_model_provider_binding_version="v1",
        canonical_chain_validated=True,
        require_canonical_chain=True,
    )


def _controlled_effect_boundary(fixture: TemporalAuthorityFixtureV1) -> Dict[str, Any]:
    """Use the real bounded eligibility query, then stop at a controlled provider failure."""

    grant = fixture.grant
    active = query_active_authorization_for_grant(grant)
    if active is None:
        return {
            "final_boundary_result": "DENY",
            "authorization_query_state": "NOT_CURRENT",
            "adapter_error_code": "RUNTIME_AUTHORIZATION_NOT_CURRENT",
            "real_final_authorization_query_used": True,
            "real_effect_executed": False,
            "controlled_effect_used": False,
        }

    # execute_real_provider=True reaches the adapter's real authorization
    # predicate. provider_failure=True returns before model/file/provider work,
    # so the effect is controlled and no external effect is executed.
    adapter_result = run_authorized_vision_provider_v1(
        _frame(fixture.scenario_id),
        _admission(fixture),
        execute_real_provider=True,
        model_path="/phase-b/no-op-provider-model.pt",
        runtime_authorization_grant=grant,
        provider_failure=True,
    )
    effect_allowed = adapter_result.error_code == "PROVIDER_INVOCATION_FAILED"
    return {
        "final_boundary_result": "ALLOW" if effect_allowed else "DENY",
        "authorization_query_state": "AUTHORIZED",
        "adapter_error_code": adapter_result.error_code,
        "real_final_authorization_query_used": True,
        "real_effect_executed": False,
        "controlled_effect_used": effect_allowed,
    }


def _transition_action(fixture: TemporalAuthorityFixtureV1) -> Dict[str, Any]:
    transitioned = revoke_admitted_action_v1(
        fixture.admitted_action.admitted_action_ref,
        reason_ref=f"phase-b:action-revoked:{fixture.scenario_id}",
        profile_ref=ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1,
    )
    current = query_current_admitted_action_v1(fixture.admitted_action.admitted_action_ref)
    return {
        "owner": "Action Governance",
        "transition": "REVOKE_ADMITTED_ACTION",
        "transition_ref": fixture.admitted_action.admitted_action_ref,
        "transition_result": _state(transitioned),
        "owner_requery": _state(current),
        "reason": "real Action owner transition",
    }


def _transition_envelope(fixture: TemporalAuthorityFixtureV1) -> Dict[str, Any]:
    transitioned = invalidate_working_envelope_v1(
        fixture.envelope.envelope_ref,
        reason_ref=f"phase-b:envelope-invalidated:{fixture.scenario_id}",
        profile_ref=WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1,
    )
    current = query_current_working_envelope_v1(fixture.envelope.envelope_ref)
    return {
        "owner": "Working Envelope Governance",
        "transition": "INVALIDATE_WORKING_ENVELOPE",
        "transition_ref": fixture.envelope.envelope_ref,
        "transition_result": _state(transitioned),
        "owner_requery": _state(current),
        "reason": "real Working Envelope owner transition",
    }


def _transition_grant(fixture: TemporalAuthorityFixtureV1) -> Dict[str, Any]:
    transitioned = revoke_cognitive_grant(
        fixture.cognitive_grant.grant_ref,
        revocation_ref=f"phase-b:grant-revoked:{fixture.scenario_id}",
        profile_ref=BRAIN_CONTROLLED_PROFILE_REF,
    )
    current = query_current_cognitive_grant(fixture.cognitive_grant.grant_ref)
    return {
        "owner": "Brain Governance",
        "transition": "REVOKE_COGNITIVE_GRANT",
        "transition_ref": fixture.cognitive_grant.grant_ref,
        "transition_result": _state(transitioned),
        "owner_requery": _state(current),
        "reason": "real Cognitive Grant owner transition",
    }


def _transition_concern(fixture: TemporalAuthorityFixtureV1) -> Dict[str, Any]:
    replacement = supersede_concern(
        fixture.concern.concern_ref,
        request_ref=f"phase-b:replacement-request:{fixture.scenario_id}",
        goal_ref=f"phase-b:replacement-goal:{fixture.scenario_id}",
        intent_ref=f"phase-b:replacement-intent:{fixture.scenario_id}",
        scope_ref=f"phase-b:replacement-scope:{fixture.scenario_id}",
        basis_refs=(f"phase-b:replacement-basis:{fixture.scenario_id}",),
        policy_refs=(f"phase-b:replacement-policy:{fixture.scenario_id}",),
        profile_ref=BRAIN_CONTROLLED_PROFILE_REF,
    )
    current = query_current_concern(fixture.concern.concern_ref)
    return {
        "owner": "Brain Governance",
        "transition": "SUPERSEDE_CONCERN",
        "transition_ref": fixture.concern.concern_ref,
        "replacement_ref": getattr(replacement, "concern_ref", ""),
        "transition_result": _state(replacement),
        "owner_requery": _state(current),
        "reason": "real Concern owner transition",
    }


def _transition_safety(fixture: TemporalAuthorityFixtureV1) -> Dict[str, Any]:
    transitioned = invalidate_runtime_safety_prerequisite_v1(
        binding_key=fixture.runtime_safety_binding_key,
        reason=f"phase-b:safety-invalidated:{fixture.scenario_id}",
    )
    current = query_current_runtime_safety_prerequisite_v1(
        binding_key=fixture.runtime_safety_binding_key,
        result_ref=fixture.runtime_safety.result_ref,
    )
    return {
        "owner": "Action Governance / Runtime Safety",
        "transition": "INVALIDATE_RUNTIME_SAFETY_PREREQUISITE",
        "transition_ref": fixture.runtime_safety.result_ref,
        "transition_result": _state(transitioned),
        "owner_requery": _state(current),
        "reason": "real Safety owner transition",
    }


def _transition_runtime_authorization(fixture: TemporalAuthorityFixtureV1) -> Dict[str, Any]:
    transitioned = invalidate_runtime_authorization_state(
        authorization_ref=fixture.grant.authorization_ref,
        subject_ref=fixture.grant.source_execution_instance_preparation_ref,
        reason=f"phase-b:runtime-auth-invalidated:{fixture.scenario_id}",
    )
    current = query_active_authorization_for_grant(fixture.grant)
    return {
        "owner": "Permission / Admission Manager",
        "transition": "INVALIDATE_RUNTIME_AUTHORIZATION",
        "transition_ref": fixture.grant.authorization_ref,
        "transition_result": _state(transitioned),
        "owner_requery": _state(current),
        "reason": "real Runtime Authorization owner transition",
    }


_TRANSITIONS: dict[str, Callable[[TemporalAuthorityFixtureV1], Dict[str, Any]]] = {
    "B02_ACTION_REVOKED_AFTER_AUTHORIZATION": _transition_action,
    "B03_WORKING_ENVELOPE_INVALIDATED_AFTER_AUTHORIZATION": _transition_envelope,
    "B04_COGNITIVE_GRANT_REVOKED_AFTER_AUTHORIZATION": _transition_grant,
    "B05_CONCERN_SUPERSEDED_AFTER_AUTHORIZATION": _transition_concern,
    "B06_SAFETY_INVALIDATED_AFTER_AUTHORIZATION": _transition_safety,
    "B07_RUNTIME_AUTHORIZATION_INVALIDATED": _transition_runtime_authorization,
}


def run_scenario(scenario_id: str) -> Dict[str, Any]:
    fixture = build_temporal_authority_fixture(scenario_id)
    trace = _initial_trace(fixture)
    auth_before = query_active_authorization_for_grant(fixture.grant)
    trace.append(
        _event(
            scenario_id=scenario_id,
            order=len(trace),
            step="RUNTIME_AUTHORIZATION_CURRENT_BEFORE_TRANSITION",
            canonical_fact_type="RuntimeAuthorization",
            canonical_ref=fixture.grant.authorization_ref,
            owner="Permission / Admission Manager",
            owner_state_before="AUTHORIZED",
            owner_transition="NONE",
            owner_state_after=_state(auth_before),
            grant=fixture.grant,
            authorization_state=_state(auth_before),
            effect_boundary_result="NOT_REACHED",
            reason="original Runtime Authorization is retained unchanged",
        )
    )

    transition = None
    if scenario_id in _TRANSITIONS:
        transition = _TRANSITIONS[scenario_id](fixture)
        trace.append(
            _event(
                scenario_id=scenario_id,
                order=len(trace),
                step="OWNER_LIFECYCLE_TRANSITION",
                canonical_fact_type=transition["owner"],
                canonical_ref=transition["transition_ref"],
                owner=transition["owner"],
                owner_state_before="CURRENT",
                owner_transition=transition["transition"],
                owner_state_after=transition["transition_result"],
                grant=fixture.grant,
                authorization_state=_state(auth_before),
                effect_boundary_result="NOT_REACHED",
                reason=transition["reason"],
            )
        )
        trace.append(
            _event(
                scenario_id=scenario_id,
                order=len(trace),
                step="OWNER_REQUERY_AFTER_TRANSITION",
                canonical_fact_type=transition["owner"],
                canonical_ref=transition["transition_ref"],
                owner=transition["owner"],
                owner_state_before=transition["transition_result"],
                owner_transition="REF_ONLY_REQUERY",
                owner_state_after=transition["owner_requery"],
                grant=fixture.grant,
                authorization_state=_state(auth_before),
                effect_boundary_result="NOT_REACHED",
                reason="real owner query after authoritative transition",
            )
        )

    auth_after = query_active_authorization_for_grant(fixture.grant)
    effect = _controlled_effect_boundary(fixture)
    trace.append(
        _event(
            scenario_id=scenario_id,
            order=len(trace),
            step="CONTROLLED_EFFECT_AUTHORIZATION_BOUNDARY",
            canonical_fact_type="RuntimeAuthorization",
            canonical_ref=fixture.grant.authorization_ref,
            owner="Permission / Admission Manager",
            owner_state_before=_state(auth_after),
            owner_transition="FINAL_AUTHORIZATION_QUERY",
            owner_state_after=effect["authorization_query_state"],
            grant=fixture.grant,
            authorization_state=effect["authorization_query_state"],
            effect_boundary_result=effect["final_boundary_result"],
            reason=effect["adapter_error_code"],
        )
    )
    if scenario_id == "B01_STABLE_AUTHORIZED_EFFECT":
        expected = "ALLOW"
    elif scenario_id == "B07_RUNTIME_AUTHORIZATION_INVALIDATED":
        expected = "DENY"
    else:
        expected = "DYNAMIC_PROBE"
    interpretation = "STABLE_CONTROL" if scenario_id == "B01_STABLE_AUTHORIZED_EFFECT" else (
        "EXPLICIT_RUNTIME_AUTHORIZATION_INVALIDATION_DENIED"
        if scenario_id == "B07_RUNTIME_AUTHORIZATION_INVALIDATED"
        else (
            "STALE_AUTHORITY_CONSUMPTION_CANDIDATE"
            if effect["final_boundary_result"] == "ALLOW"
            else "DOWNSTREAM_BOUNDARY_DENIED_AFTER_OWNER_TRANSITION"
        )
    )
    return {
        "scenario_id": scenario_id,
        "trace": trace,
        "upstream_owner_transition": transition["transition"] if transition else "NONE",
        "owner_requery_after_transition": transition["owner_requery"] if transition else "CURRENT",
        "runtime_authorization_state_before": _state(auth_before),
        "runtime_authorization_state_after": _state(auth_after),
        "runtime_authorization_ref": fixture.grant.authorization_ref,
        "runtime_grant_ref": fixture.grant.grant_ref,
        "final_boundary_result": effect["final_boundary_result"],
        "expected_by_current_contract": expected,
        "architectural_interpretation": interpretation,
        **effect,
        "real_owner_transition_used": transition is not None,
        "runtime_authorization_object_reused": True,
    }


def run_phase_b_scenarios() -> Dict[str, Dict[str, Any]]:
    """Run the seven controlled scenario definitions when called by the user."""

    return {scenario_id: run_scenario(scenario_id) for scenario_id in SCENARIO_IDS}


__all__ = ["SCENARIO_IDS", "run_phase_b_scenarios", "run_scenario"]

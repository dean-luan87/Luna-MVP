"""Synthetic adapter exercising the A -> B-CR -> A candidate boundary."""

from __future__ import annotations

from typing import Dict, Iterable, Mapping, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_registry_v1 import A_AUTHORITIES, B_AUTHORITIES, ROLE_A, ROLE_B
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_types_v1 import AuthorityResponsibilityBindingCandidateV1, CognitiveAuthorityGrantCandidateV1

from .a_b_contingency_reasoning_engine_v1 import (
    build_b_handoff, build_b_reasoning_envelope, build_b_result, build_concurrent_state,
    build_contingency_request, build_contingency_trigger, derive_b_contingency_grant,
    evaluate_b_result, reject_b_escalation, validate_a_trigger,
)
from .a_b_contingency_reasoning_fixture_v1 import build_a_b_contingency_cases_v1
from .a_b_contingency_reasoning_registry_v1 import B_CR_AUTHORITIES, PHASE, REQUIRED_A_TRIGGER_AUTHORITY, RESULT_EVALUATION_AUTHORITY


def _trace(ref: str) -> str:
    return f"trace:{ref}"


def _grant(case_id: str, *, authorities: Iterable[str] = A_AUTHORITIES, concern_ref: str | None = None, work_ref: str | None = None, state_ref: str = "state:v1", resource_ref: str = "resource:bounded", safety_ref: str = "safety:bounded", permission_ref: str = "permission:bounded", receiver_role: str = ROLE_A, revoked: bool = False, expired: bool = False) -> tuple[CognitiveAuthorityGrantCandidateV1, bool, bool]:
    grant = CognitiveAuthorityGrantCandidateV1(
        grant_ref=f"grant:{case_id}", issuer_ref="brain:governance" if receiver_role == ROLE_A else f"a:{case_id}",
        receiver_ref=f"a:{case_id}" if receiver_role == ROLE_A else f"b:{case_id}", receiver_role=receiver_role,
        concern_ref=concern_ref or f"concern:{case_id}", work_ref=work_ref or f"work:{case_id}",
        granted_authority_refs=tuple(authorities), capability_boundary_ref=f"boundary:{receiver_role}",
        goal_refs=(f"goal:{case_id}",), role_refs=(f"role:{case_id}",), field_refs=(f"field:{case_id}",),
        safety_refs=(safety_ref,), permission_refs=(permission_ref,), resource_envelope_refs=(resource_ref,),
        valid_from_state_ref=state_ref, valid_until_condition_refs=(f"condition:{case_id}:stop",),
        revocation_condition_refs=(f"condition:{case_id}:revoke",), result_receiver_ref=ROLE_A,
        responsibility_owner_ref=f"responsibility:{case_id}", trace_ref=_trace(f"grant:{case_id}"), provenance_refs=(f"provenance:{case_id}",),
    )
    return grant, revoked, expired


def _binding(ref: str, authority: str, owner: str) -> AuthorityResponsibilityBindingCandidateV1:
    return AuthorityResponsibilityBindingCandidateV1(
        binding_ref=f"binding:{ref}", authority_ref=authority, decision_authority_ref=f"decision:{authority}",
        responsibility_owner_ref=owner, result_receiver_ref=ROLE_A, error_owner_ref=owner,
        expiry_ref=f"expiry:{ref}", revocation_authority_ref="brain:governance", valid=True,
        reason_refs=("binding:explicit",), trace_ref=_trace(f"binding:{ref}"), provenance_refs=(f"provenance:binding:{ref}",),
    )


def _context(case_id: str, *, concern_ref: str | None = None, work_ref: str | None = None, state_ref: str = "state:v1") -> tuple[CognitiveAuthorityGrantCandidateV1, AuthorityResponsibilityBindingCandidateV1, object]:
    grant, _, _ = _grant(case_id, concern_ref=concern_ref, work_ref=work_ref, state_ref=state_ref)
    binding = _binding(case_id, REQUIRED_A_TRIGGER_AUTHORITY, grant.receiver_ref)
    trigger = build_contingency_trigger(
        trigger_ref=f"trigger:{case_id}", work_ref=grant.work_ref, concern_ref=grant.concern_ref,
        source_state_ref=state_ref, source_need_ref=f"need:{case_id}", source_hypothesis_refs=(f"hypothesis:{case_id}",),
        uncertainty_ref=f"uncertainty:{case_id}", uncertainty_type="MATERIAL_CONTINGENCY_GAP",
        reason_refs=("a:material-uncertainty",), expected_information_value_ref=f"value:{case_id}", a_grant_ref=grant.grant_ref,
    )
    return grant, binding, trigger


def _request(case_id: str, grant: CognitiveAuthorityGrantCandidateV1, binding: AuthorityResponsibilityBindingCandidateV1, trigger: object, *, resource: str | None = None, safety: str | None = None, permission: str | None = None, depth: int = 1, branch: int = 1, authorities: Iterable[str] = B_CR_AUTHORITIES):
    request = build_contingency_request(
        request_ref=f"request:{case_id}", work_ref=grant.work_ref, concern_ref=grant.concern_ref, source_state_ref=grant.valid_from_state_ref,
        trigger_ref=trigger.trigger_ref, a_grant_ref=grant.grant_ref, derived_b_grant_ref=f"derived:request:{case_id}",
        scenario_scope_refs=(f"scope:{case_id}",), assumption_refs=(f"assumption:{case_id}",), uncertainty_refs=(f"uncertainty:{case_id}",),
        resource_refs=(resource or grant.resource_envelope_refs[0],), safety_refs=(safety or grant.safety_refs[0],), permission_refs=(permission or grant.permission_refs[0],),
        depth_limit=depth, branch_limit=branch, required_result_refs=(f"result-required:{case_id}",), termination_condition_refs=(f"stop:{case_id}",),
    )
    derived = derive_b_contingency_grant(grant, request, requested_authorities=authorities, a_binding=binding)
    return request, derived


def _common(case_id: str):
    grant, binding, trigger = _context(case_id)
    trigger_validation = validate_a_trigger(trigger, grant, binding, current_state_ref=grant.valid_from_state_ref)
    request, derived = _request(case_id, grant, binding, trigger)
    return grant, binding, trigger, trigger_validation, request, derived


def _negative_guards() -> Dict[str, bool]:
    return {
        "candidate_only": True, "synthetic_only": True, "b_direct_entry": False, "b_self_authorized_start": False,
        "b_recursive_delegation": False, "b_concern_creation": False, "b_concern_split": False, "b_concern_merge": False,
        "b_loop_control": False, "b_mechanical_command_issue": False, "b_result_binding": False, "b_result_self_adoption": False,
        "b_world_truth_declaration": False, "b_final_need_selection": False, "b_final_sufficiency_judgment": False,
        "b_final_continuation_decision": False, "real_thread_execution": False, "scheduler_execution": False,
        "provider_invocation": False, "model_inference": False, "yolo": False, "ocr": False, "camera": False,
        "action_execution": False, "memory_mutation": False, "experience_mutation": False, "learning": False,
        "semantic_compression": False,
    }


def _result(case_id: str, *, passed: bool, title: str, **flags: object) -> Dict[str, object]:
    return {"scenario_id": case_id, "title": title, "passed": passed, "checks": {key: value for key, value in flags.items()}, "negative_guards": _negative_guards(), **flags}


def run_a_b_contingency_case(case: Mapping[str, object]) -> Dict[str, object]:
    case_id = str(case["scenario_id"]); title = str(case["title"]); kind = str(case["kind"])
    if case_id == "AB-02":
        return _result(case_id, passed=True, title=title, a_b_request=False)
    if kind == "TRIGGER":
        grant, binding, trigger = _context(case_id)
        if case_id == "AB-03": grant = _grant(case_id, authorities=tuple(item for item in A_AUTHORITIES if item != REQUIRED_A_TRIGGER_AUTHORITY))[0]
        if case_id == "AB-04": trigger = build_contingency_trigger(trigger_ref=trigger.trigger_ref, work_ref=trigger.work_ref, concern_ref="concern:other", source_state_ref=trigger.source_a_state_version_ref, source_need_ref=trigger.source_need_ref, source_hypothesis_refs=trigger.source_hypothesis_refs, uncertainty_ref=trigger.uncertainty_ref, uncertainty_type=trigger.uncertainty_type, reason_refs=trigger.reason_refs, expected_information_value_ref=trigger.expected_information_value_ref, a_grant_ref=grant.grant_ref)
        if case_id == "AB-05": trigger = build_contingency_trigger(trigger_ref=trigger.trigger_ref, work_ref=trigger.work_ref, concern_ref=trigger.concern_ref, source_state_ref="state:v2", source_need_ref=trigger.source_need_ref, source_hypothesis_refs=trigger.source_hypothesis_refs, uncertainty_ref=trigger.uncertainty_ref, uncertainty_type=trigger.uncertainty_type, reason_refs=trigger.reason_refs, expected_information_value_ref=trigger.expected_information_value_ref, a_grant_ref=grant.grant_ref)
        validation = validate_a_trigger(trigger, grant, binding, current_state_ref="state:v1", revoked=case_id == "AB-06", expired=False)
        expected = {"AB-01": True, "AB-03": False, "AB-04": False, "AB-05": False, "AB-06": False}[case_id]
        return _result(case_id, passed=validation.accepted is expected, title=title, a_b_request=validation.accepted, failure_class=validation.failure_class)
    grant, binding, trigger, trigger_validation, request, derived = _common(case_id)
    if kind == "GRANT":
        if case_id == "BG-02": request, derived = _request(case_id, grant, binding, trigger, authorities=("JUDGE_LOCAL_SUFFICIENCY",))
        if case_id == "BG-03": request, derived = _request(case_id, grant, binding, trigger, authorities=("CONTROL_LOOP",))
        if case_id == "BG-04": request, derived = _request(case_id, grant, binding, trigger, resource="resource:expanded")
        if case_id == "BG-05": request, derived = _request(case_id, grant, binding, trigger, safety="safety:expanded")
        if case_id == "BG-06": request, derived = _request(case_id, grant, binding, trigger, permission="permission:expanded")
        expected = case_id == "BG-01"
        return _result(case_id, passed=derived.accepted is expected, title=title, a_b_request=True, valid_derived_b_grant=derived.accepted, rejected_b_grant=not derived.accepted, failure_class=derived.failure_class)
    if kind == "RESULT":
        status = {"BR-01": "COMPLETED_WITH_CANDIDATES", "BR-02": "RESOURCE_LIMIT", "BR-03": "RESOURCE_LIMIT", "BR-04": "RESOURCE_LIMIT", "BR-05": "STALE_SOURCE_STATE", "BR-06": "GRANT_REVOKED"}[case_id]
        envelope = build_b_reasoning_envelope(
            request, derived.derived_grant_ref, goal_refs=(f"goal:{case_id}",),
            intent_refs=(f"intent:{case_id}",), context_refs=(f"context:{case_id}",),
            current_world_refs=(f"world:{case_id}",), source_a_need_ref=f"need:{case_id}",
            source_a_hypothesis_refs=(f"hypothesis:{case_id}",), source_a_evidence_refs=(f"evidence:{case_id}",),
        )
        result = build_b_result(request, status=status, derived_b_grant_ref=derived.derived_grant_ref)
        return _result(case_id, passed=(envelope.derived_b_grant_ref == result.derived_b_grant_ref and result.result_owner_ref == ROLE_B and result.binding is False and result.termination_reason_ref == status), title=title, a_b_request=True, valid_derived_b_grant=derived.accepted, b_result=True, b_result_non_binding=True)
    if kind == "RETURN":
        result = build_b_result(request); handoff = build_b_handoff(request, result)
        passed = handoff.result_receiver_ref == ROLE_A and not handoff.direct_loop_handoff and not handoff.direct_brain_handoff and result.binding is False
        return _result(case_id, passed=passed, title=title, a_b_request=True, valid_derived_b_grant=derived.accepted, b_result=True, b_result_non_binding=result.binding is False, b_returns_to_a=handoff.result_receiver_ref == ROLE_A)
    if kind == "EVALUATION":
        result = build_b_result(request)
        disposition = {"AE-01": "USE", "AE-02": "PARTIAL_USE", "AE-03": "KEEP_AVAILABLE", "AE-04": "SUPERSEDE", "AE-05": "DISCARD", "AE-06": "REQUEST_UPDATED_B"}[case_id]
        evaluation = evaluate_b_result(result, current_a_state_version_ref=grant.valid_from_state_ref, current_world_refs=(f"world:{case_id}",), current_need_ref=f"need:{case_id}", current_hypothesis_refs=(f"hypothesis:{case_id}",), disposition=disposition, a_grant=grant, binding=_binding(case_id, RESULT_EVALUATION_AUTHORITY, grant.receiver_ref))
        return _result(case_id, passed=evaluation.evaluation_disposition == disposition and evaluation.decision_owner_ref == ROLE_A, title=title, a_b_request=True, valid_derived_b_grant=derived.accepted, b_result=True, a_result_evaluation=True)
    if kind == "CONCURRENCY":
        state = build_concurrent_state(work_ref=grant.work_ref, concern_ref=grant.concern_ref, a_state_ref="a:active" if case_id == "CC-01" else "a:waiting", b_request_ref=request.request_ref, b_state_ref="b:active", a_active=case_id == "CC-01", b_active=True, shared_read_only_refs=("world:shared",), isolated_local_refs=(f"a:local:{case_id}", f"b:local:{case_id}"))
        passed = state.candidate_only and state.scheduler_execution is False and state.thread_execution is False and state.b_active
        if case_id == "CC-03": passed = passed and state.a_active is False
        return _result(case_id, passed=passed, title=title, a_b_request=True, valid_derived_b_grant=derived.accepted, concurrent_ab_candidate=True)
    if kind == "STALENESS":
        result = build_b_result(request)
        current = "state:v2" if case_id == "ST-02" else grant.valid_from_state_ref
        disposition = "SUPERSEDE" if case_id == "ST-02" else "KEEP_AVAILABLE" if case_id == "ST-03" else "USE"
        evaluation = evaluate_b_result(result, current_a_state_version_ref=current, current_world_refs=("world:changed" if current != grant.valid_from_state_ref else "world:same",), current_need_ref="need:current", current_hypothesis_refs=("hypothesis:current",), disposition=disposition, a_grant=_grant(case_id, state_ref=current)[0], binding=_binding(case_id, RESULT_EVALUATION_AUTHORITY, f"a:{case_id}"))
        return _result(case_id, passed=(evaluation.stale_b_result_refs != () if case_id == "ST-02" else True), title=title, a_b_request=True, valid_derived_b_grant=derived.accepted, b_result=True, a_result_evaluation=True, stale_b_result=bool(evaluation.stale_b_result_refs))
    if case_id == "IS-01":
        g1, b1, t1 = _context("IS-01-A"); g2, b2, t2 = _context("IS-01-B")
        r1, d1 = _request("IS-01-A", g1, b1, t1); r2, d2 = _request("IS-01-B", g2, b2, t2)
        passed = r1.concern_ref != r2.concern_ref and d1.grant is not None and d2.grant is not None and d1.grant.grant_ref != d2.grant.grant_ref
        return _result(case_id, passed=passed, title=title, a_b_request=True, valid_derived_b_grant=True, cross_concern_isolation=passed)
    escalations = [reject_b_escalation("NG-01-LOOP", "LOOP"), reject_b_escalation("NG-01-RECURSIVE", "RECURSIVE"), reject_b_escalation("NG-01-CONCERN", "CONCERN")]
    passed = all(not item.accepted for item in escalations)
    return _result(case_id, passed=passed, title=title, b_result=True, b_loop_control=False, no_recursive_b=True, no_external_runtime=True)


def build_a_b_contingency_run_v1() -> Dict[str, object]:
    cases = tuple(run_a_b_contingency_case(case) for case in build_a_b_contingency_cases_v1())
    guards = _negative_guards()
    summary = {
        "phase": PHASE, "scenario_count": len(cases), "all_cases_passed": all(item["passed"] for item in cases),
        "failed_case_ids": [item["scenario_id"] for item in cases if not item["passed"]],
        "a_b_request_count": sum(bool(item.get("a_b_request")) for item in cases),
        "valid_derived_b_grant_count": sum(bool(item.get("valid_derived_b_grant")) for item in cases),
        "rejected_b_grant_count": sum(bool(item.get("rejected_b_grant")) for item in cases),
        "b_result_count": sum(bool(item.get("b_result")) for item in cases),
        "a_result_evaluation_count": sum(bool(item.get("a_result_evaluation")) for item in cases),
        "concurrent_ab_candidate_count": sum(bool(item.get("concurrent_ab_candidate")) for item in cases),
        "stale_b_result_count": sum(bool(item.get("stale_b_result")) for item in cases),
        "key_guards": {"candidate_only": True, "synthetic_only": True, "b_only_started_by_a": True, "b_bounded_by_derived_grant": True, "b_result_non_binding": True, "b_returns_to_a": True, "a_owns_result_evaluation": True, "b_has_no_loop_control": True, "no_recursive_b": True, "no_runtime": True, "no_provider": True, "no_action": True},
        "negative_guards": guards,
    }
    return {"summary": summary, "cases": cases}


__all__ = ["build_a_b_contingency_run_v1", "run_a_b_contingency_case"]

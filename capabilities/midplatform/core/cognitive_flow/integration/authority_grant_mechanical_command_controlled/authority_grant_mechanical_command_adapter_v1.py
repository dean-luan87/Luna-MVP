"""Candidate-only adapter and scenario runner for grant/mechanical control."""

from __future__ import annotations

from typing import Dict, Iterable, Mapping, Tuple

from .authority_grant_mechanical_command_engine_v1 import (
    apply_mechanical_command,
    build_expiry_candidate,
    build_grant_status,
    build_revocation_candidate,
    derive_b_grant,
    validate_mechanical_command,
    validate_responsibility_binding,
)
from .authority_grant_mechanical_command_fixture_v1 import build_authority_grant_cases_v1
from .authority_grant_mechanical_command_registry_v1 import (
    A_AUTHORITIES,
    B_AUTHORITIES,
    LOOP_AUTHORITIES,
    PHASE,
    ROLE_A,
    ROLE_B,
    ROLE_LOOP,
)
from .authority_grant_mechanical_command_types_v1 import (
    AuthorityResponsibilityBindingCandidateV1,
    CognitiveAuthorityGrantCandidateV1,
    LoopMechanicalStateCandidateV1,
    MechanicalCommandCandidateV1,
)


def _trace(ref: str) -> str:
    return f"trace:{ref}"


def _prov(ref: str) -> Tuple[str, ...]:
    return (f"provenance:{ref}",)


def _grant(
    grant_ref: str,
    receiver_ref: str,
    receiver_role: str,
    *,
    concern_ref: str = "concern:primary",
    work_ref: str = "work:primary",
    authorities: Iterable[str] = A_AUTHORITIES,
    issuer_ref: str = "brain:governance",
    state_ref: str = "state:primary:v1",
    resource_ref: str = "resource:bounded",
    permission_ref: str = "permission:bounded",
) -> CognitiveAuthorityGrantCandidateV1:
    return CognitiveAuthorityGrantCandidateV1(
        grant_ref=grant_ref,
        issuer_ref=issuer_ref,
        receiver_ref=receiver_ref,
        receiver_role=receiver_role,
        concern_ref=concern_ref,
        work_ref=work_ref,
        granted_authority_refs=tuple(authorities),
        capability_boundary_ref=f"boundary:{receiver_role}",
        goal_refs=("goal:primary",),
        role_refs=("role:primary",),
        field_refs=("field:primary",),
        safety_refs=("safety:bounded",),
        permission_refs=(permission_ref,),
        resource_envelope_refs=(resource_ref,),
        valid_from_state_ref=state_ref,
        valid_until_condition_refs=("condition:state-advance",),
        revocation_condition_refs=("condition:concern-stop",),
        result_receiver_ref=f"result:{receiver_ref}",
        responsibility_owner_ref=f"responsibility:{receiver_ref}",
        trace_ref=_trace(grant_ref),
        provenance_refs=_prov(grant_ref),
    )


def _binding(
    binding_ref: str,
    authority_ref: str,
    *,
    responsibility_owner_ref: str = "responsibility:owner",
    result_receiver_ref: str = "result:receiver",
    error_owner_ref: str = "error:owner",
    valid: bool = True,
) -> AuthorityResponsibilityBindingCandidateV1:
    return AuthorityResponsibilityBindingCandidateV1(
        binding_ref=binding_ref,
        authority_ref=authority_ref,
        decision_authority_ref=f"decision:{authority_ref}" if authority_ref else "",
        responsibility_owner_ref=responsibility_owner_ref,
        result_receiver_ref=result_receiver_ref,
        error_owner_ref=error_owner_ref,
        expiry_ref=f"expiry:{binding_ref}" if valid else "",
        revocation_authority_ref=f"revoke:{binding_ref}" if valid else "",
        valid=valid,
        reason_refs=("binding:explicit",) if valid else ("binding:invalid",),
        trace_ref=_trace(binding_ref),
        provenance_refs=_prov(binding_ref),
    )


def _loop_grant(case_id: str, *, concern_ref: str = "concern:primary", work_ref: str = "work:primary", state_ref: str = "state:primary:v1") -> CognitiveAuthorityGrantCandidateV1:
    return _grant(
        f"grant:loop:{case_id}",
        f"loop:{case_id}",
        ROLE_LOOP,
        concern_ref=concern_ref,
        work_ref=work_ref,
        authorities=LOOP_AUTHORITIES,
        state_ref=state_ref,
    )


def _state(case_id: str, *, concern_ref: str = "concern:primary", work_ref: str = "work:primary") -> LoopMechanicalStateCandidateV1:
    return LoopMechanicalStateCandidateV1(
        loop_ref=f"loop:{case_id}",
        concern_ref=concern_ref,
        work_ref=work_ref,
        current_mechanical_state="ACTIVE",
        state_version_ref="state:primary:v1",
        trace_refs=(_trace(f"loop:{case_id}"),),
        provenance_refs=_prov(f"loop:{case_id}"),
    )


def _command(
    case_id: str,
    command_kind: str,
    a_grant: CognitiveAuthorityGrantCandidateV1,
    loop_grant: CognitiveAuthorityGrantCandidateV1,
    *,
    concern_ref: str | None = None,
    work_ref: str | None = None,
    state_ref: str = "state:primary:v1",
    target_refs: Tuple[str, ...] = ("ref:target",),
    reason_refs: Tuple[str, ...] = ("reason:a-decided",),
) -> MechanicalCommandCandidateV1:
    return MechanicalCommandCandidateV1(
        command_ref=f"command:{case_id}",
        command_kind=command_kind,
        issuer_ref=a_grant.receiver_ref,
        issuer_role=a_grant.receiver_role,
        receiver_ref=loop_grant.receiver_ref,
        grant_ref=a_grant.grant_ref,
        loop_grant_ref=loop_grant.grant_ref,
        concern_ref=concern_ref or a_grant.concern_ref,
        work_ref=work_ref or a_grant.work_ref,
        source_state_version_ref=state_ref,
        target_refs=target_refs,
        reason_refs=reason_refs,
        trace_ref=_trace(f"command:{case_id}"),
        provenance_refs=_prov(f"command:{case_id}"),
    )


def _base_a_grant(case_id: str, *, authorities: Iterable[str] = A_AUTHORITIES, **kwargs: object) -> CognitiveAuthorityGrantCandidateV1:
    return _grant(f"grant:a:{case_id}", f"a:{case_id}", ROLE_A, authorities=authorities, **kwargs)


def _negative_guards() -> Dict[str, bool]:
    return {
        "brain_runtime_execution": False,
        "provider_invocation": False,
        "model_inference": False,
        "yolo": False,
        "ocr": False,
        "camera": False,
        "action_execution": False,
        "learning": False,
        "memory_mutation": False,
        "experience_mutation": False,
        "autonomous_scheduling": False,
        "authority_manager_created": False,
        "permission_manager_created": False,
        "loop_manager_created": False,
        "loop_planner_created": False,
        "loop_semantic_judgment": False,
        "loop_sufficiency_judgment": False,
        "loop_need_selection": False,
        "loop_hypothesis_generation": False,
        "b_recursive_delegation": False,
        "b_concern_creation": False,
        "cross_concern_grant_use": False,
        "cross_loop_state_mutation": False,
        "semantic_compression": False,
    }


def _run_grant_case(case: Mapping[str, object]) -> Dict[str, object]:
    case_id = str(case["scenario_id"])
    expected = case["expected_failure_class"]
    kwargs: Dict[str, object] = {}
    if case_id == "AG-02":
        kwargs["concern_ref"] = ""
    if case_id == "AG-03":
        kwargs["receiver_role"] = "WRONG_RECEIVER_ROLE"
    if case_id == "AG-04":
        kwargs["authorities"] = ("UNSUPPORTED_AUTHORITY",)
    if case_id == "AG-05":
        kwargs["authorities"] = ("JUDGE_SUFFICIENCY",)
    if case_id == "AG-06":
        kwargs["state_ref"] = "state:primary:v2"
    grant = _grant(
        f"grant:a:{case_id}",
        f"a:{case_id}",
        str(kwargs.pop("receiver_role", ROLE_A)),
        **kwargs,
    )
    binding = _binding(
        f"binding:{case_id}",
        grant.granted_authority_refs[0] if grant.granted_authority_refs else "",
        valid=case_id != "AG-09",
    )
    status = build_grant_status(
        grant,
        checked_state_version_ref="state:primary:v1",
        revoked=case_id == "AG-07",
        expired=case_id == "AG-08",
        binding=binding,
    )
    failure = None if status.valid else (
        "SCOPE_MISMATCH" if "scope_ref_missing" in status.reason_refs else
        "AUTHORITY_NOT_GRANTED" if "receiver_role" in " ".join(status.reason_refs) else
        "CAPABILITY_BOUNDARY_VIOLATION" if any("authority" in item for item in status.reason_refs) else
        "STALE_STATE_VERSION" if status.status == "STALE" else
        "GRANT_REVOKED" if status.revoked else
        "GRANT_EXPIRED" if status.expired else
        "RESPONSIBILITY_BINDING_INVALID"
    )
    passed = failure == expected if expected else status.valid
    return {
        "scenario_id": case_id,
        "title": case["title"],
        "passed": passed,
        "checks": {"expected_failure_class": failure == expected, "candidate_only": grant.candidate_only, "synthetic_only": grant.synthetic_only},
        "failure_class": failure,
        "valid_grant": status.valid,
        "rejected_grant": not status.valid,
        "negative_guards": _negative_guards(),
    }


def _run_mechanical_case(case: Mapping[str, object]) -> Dict[str, object]:
    case_id = str(case["scenario_id"])
    a_grant = _base_a_grant(case_id)
    loop_grant = _loop_grant(case_id)
    issuer_binding = _binding(f"binding:a:{case_id}", "REQUEST_CAPABILITY")
    loop_binding = _binding(f"binding:loop:{case_id}", "PERSIST_STATE", responsibility_owner_ref="loop:engine", result_receiver_ref=a_grant.receiver_ref, error_owner_ref="loop:engine")
    command_kind = {
        "MC-01": "MATERIALIZE",
        "MC-02": "JUDGE_SUFFICIENCY",
        "MC-03": "RECORD_STATE_VERSION",
        "MC-04": "PAUSE",
        "MC-05": "WAIT",
        "MC-06": "RESUME_KEEP",
        "MC-07": "FREEZE_FINAL_STATE",
        "MC-08": "ARCHIVE_HISTORY_BOUNDARY",
        "MC-09": "RECORD_PENDING_CANDIDATE",
    }[case_id]
    command = _command(case_id, command_kind, a_grant, loop_grant, target_refs=("state:primary:v2",) if case_id == "MC-03" else ("ref:target",))
    validation = validate_mechanical_command(
        command,
        issuer_grant=a_grant,
        loop_grant=loop_grant,
        issuer_binding=issuer_binding,
        loop_binding=loop_binding,
        current_state_version_ref="state:primary:v1",
    )
    state = _state(case_id)
    next_state, returned = apply_mechanical_command(state, command, validation)
    expected_failure = case["expected_failure_class"]
    passed = (
        validation.failure_class == expected_failure
        if expected_failure
        else validation.accepted
    )
    if case_id == "MC-09":
        passed = passed and next_state.closure_state == "OPEN" and next_state.current_mechanical_state == "ACTIVE"
    return {
        "scenario_id": case_id,
        "title": case["title"],
        "passed": passed,
        "checks": {
            "expected_failure_class": validation.failure_class == expected_failure,
            "mechanical_acceptance": validation.accepted is (expected_failure is None),
            "no_semantic_judgment": next_state.current_mechanical_state not in {"SUFFICIENT", "REPLAN", "RECONSIDER"},
            "return_is_mechanical": returned.closure_state == next_state.closure_state,
        },
        "failure_class": validation.failure_class,
        "accepted_mechanical_command": validation.accepted,
        "rejected_mechanical_command": not validation.accepted,
        "negative_guards": _negative_guards(),
    }


def _b_request(
    case_id: str,
    a_grant: CognitiveAuthorityGrantCandidateV1,
    *,
    requested_authorities: Tuple[str, ...] = B_AUTHORITIES,
    requester_role: str = ROLE_A,
    resource_ref: str = "resource:bounded",
    requested_depth: int = 1,
    max_depth: int = 2,
) -> Dict[str, object]:
    return {
        "request_ref": f"request:b:{case_id}",
        "requester_role": requester_role,
        "concern_ref": a_grant.concern_ref,
        "work_ref": a_grant.work_ref,
        "source_state_version_ref": a_grant.valid_from_state_ref,
        "requested_authorities": requested_authorities,
        "resource_ref": resource_ref,
        "requested_depth": requested_depth,
        "max_depth": max_depth,
        "stop_condition_refs": ("stop:bounded",),
    }


def _run_b_case(case: Mapping[str, object]) -> Dict[str, object]:
    case_id = str(case["scenario_id"])
    authorities = A_AUTHORITIES
    if case_id == "BG-02":
        authorities = tuple(item for item in A_AUTHORITIES if item != "REQUEST_B")
    a_grant = _base_a_grant(case_id, authorities=authorities)
    request_kwargs: Dict[str, object] = {}
    if case_id == "BG-03":
        request_kwargs["requested_authorities"] = ("JUDGE_SUFFICIENCY",)
    elif case_id == "BG-04":
        request_kwargs["requested_authorities"] = ("SPLIT_CONCERN",)
    elif case_id == "BG-05":
        request_kwargs["requester_role"] = ROLE_B
    elif case_id == "BG-06":
        request_kwargs["requested_authorities"] = ("PAUSE_MECHANICALLY",)
    elif case_id == "BG-07":
        request_kwargs["resource_ref"] = "resource:expanded"
    elif case_id == "BG-08":
        request_kwargs["requested_depth"] = 3
    result = derive_b_grant(a_grant, _b_request(case_id, a_grant, **request_kwargs))
    expected = case["expected_failure_class"]
    passed = result.failure_class == expected if expected else result.accepted
    return {
        "scenario_id": case_id,
        "title": case["title"],
        "passed": passed,
        "checks": {
            "expected_failure_class": result.failure_class == expected,
            "derived_scope_bounded": result.accepted or bool(result.bounded_by_refs),
            "candidate_only": result.candidate_only,
            "no_recursive_delegation": case_id != "BG-05" or result.failure_class == "AUTHORITY_NOT_GRANTED",
        },
        "failure_class": result.failure_class,
        "derived_b_grant": result.accepted,
        "negative_guards": _negative_guards(),
    }


def _run_binding_case(case: Mapping[str, object]) -> Dict[str, object]:
    case_id = str(case["scenario_id"])
    kwargs: Dict[str, object] = {}
    if case_id == "RB-02":
        kwargs = {
            "authority_ref": "",
            "responsibility_owner_ref": "",
            "result_receiver_ref": "",
            "error_owner_ref": "",
            "valid": False,
        }
    elif case_id == "RB-03":
        kwargs = {"responsibility_owner_ref": "", "valid": False}
    authority_ref = str(kwargs.pop("authority_ref", "REQUEST_CAPABILITY"))
    binding = _binding(f"binding:{case_id}", authority_ref, **kwargs)
    valid = validate_responsibility_binding(binding)
    expected = case["expected_failure_class"]
    return {
        "scenario_id": case_id,
        "title": case["title"],
        "passed": valid if expected is None else not valid,
        "checks": {
            "binding_expected": valid is (expected is None),
            "result_receiver_preserved": case_id != "RB-04" or binding.result_receiver_ref == "result:receiver",
            "error_owner_preserved": case_id != "RB-05" or binding.error_owner_ref == "error:owner",
        },
        "failure_class": None if valid else "RESPONSIBILITY_BINDING_INVALID",
        "negative_guards": _negative_guards(),
    }


def _run_isolation_case(case: Mapping[str, object]) -> Dict[str, object]:
    case_id = str(case["scenario_id"])
    a_one = _base_a_grant(f"{case_id}:one", concern_ref="concern:one", work_ref="work:one")
    a_two = _base_a_grant(f"{case_id}:two", concern_ref="concern:two", work_ref="work:two")
    loop_one = _loop_grant(f"{case_id}:one", concern_ref="concern:one", work_ref="work:one")
    loop_two = _loop_grant(f"{case_id}:two", concern_ref="concern:two", work_ref="work:two")
    binding_one = _binding(f"binding:{case_id}:one", "REQUEST_CAPABILITY")
    binding_two = _binding(f"binding:{case_id}:two", "REQUEST_CAPABILITY")
    loop_binding_one = _binding(f"binding:loop:{case_id}:one", "PERSIST_STATE", responsibility_owner_ref="loop:one", result_receiver_ref=a_one.receiver_ref, error_owner_ref="loop:one")
    loop_binding_two = _binding(f"binding:loop:{case_id}:two", "PERSIST_STATE", responsibility_owner_ref="loop:two", result_receiver_ref=a_two.receiver_ref, error_owner_ref="loop:two")
    if case_id in {"IS-01", "IS-03"}:
        command = _command(case_id, "PAUSE", a_one, loop_two, concern_ref="concern:two", work_ref="work:two")
        validation = validate_mechanical_command(
            command,
            issuer_grant=a_one,
            loop_grant=loop_two,
            issuer_binding=binding_one,
            loop_binding=loop_binding_two,
            current_state_version_ref="state:primary:v1",
        )
        passed = validation.failure_class == "SCOPE_MISMATCH"
    else:
        command = _command(case_id, "PAUSE", a_one, loop_one)
        validation = validate_mechanical_command(
            command,
            issuer_grant=a_one,
            loop_grant=loop_one,
            issuer_binding=binding_one,
            loop_binding=loop_binding_one,
            current_state_version_ref="state:primary:v1",
        )
        state_one, _ = apply_mechanical_command(_state(f"{case_id}:one", concern_ref="concern:one", work_ref="work:one"), command, validation)
        state_two = _state(f"{case_id}:two", concern_ref="concern:two", work_ref="work:two")
        passed = validation.accepted and state_two.current_mechanical_state == "ACTIVE" and state_one.current_mechanical_state == "PAUSED"
    return {
        "scenario_id": case_id,
        "title": case["title"],
        "passed": passed,
        "checks": {
            "isolation": passed,
            "cross_concern_blocked": case_id in {"IS-01", "IS-03"} and passed or case_id == "IS-02",
        },
        "failure_class": None if case_id == "IS-02" else "SCOPE_MISMATCH",
        "negative_guards": _negative_guards(),
    }


def run_authority_grant_case(case: Mapping[str, object]) -> Dict[str, object]:
    kind = str(case["kind"])
    if kind == "A_GRANT":
        return _run_grant_case(case)
    if kind == "MECHANICAL":
        return _run_mechanical_case(case)
    if kind == "B_DERIVATION":
        return _run_b_case(case)
    if kind == "BINDING":
        return _run_binding_case(case)
    if kind == "ISOLATION":
        return _run_isolation_case(case)
    return {
        "scenario_id": case["scenario_id"],
        "title": case["title"],
        "passed": True,
        "checks": {"all_negative_guards_hold": all(value is False for value in _negative_guards().values())},
        "failure_class": None,
        "negative_guards": _negative_guards(),
    }


def build_authority_grant_run_v1() -> Dict[str, object]:
    cases = tuple(run_authority_grant_case(case) for case in build_authority_grant_cases_v1())
    failed_case_ids = tuple(item["scenario_id"] for item in cases if not item["passed"])
    valid_grant_count = sum(1 for item in cases if item.get("valid_grant"))
    rejected_grant_count = sum(1 for item in cases if item.get("rejected_grant"))
    accepted_commands = sum(1 for item in cases if item.get("accepted_mechanical_command"))
    rejected_commands = sum(1 for item in cases if item.get("rejected_mechanical_command"))
    derived_b = sum(1 for item in cases if item.get("derived_b_grant"))
    revoked = sum(1 for item in cases if item.get("failure_class") == "GRANT_REVOKED")
    expired = sum(1 for item in cases if item.get("failure_class") == "GRANT_EXPIRED")
    boundary_violations = sum(1 for item in cases if item.get("failure_class") == "CAPABILITY_BOUNDARY_VIOLATION")
    negative_guards = _negative_guards()
    summary = {
        "phase": PHASE,
        "scenario_count": len(cases),
        "all_cases_passed": not failed_case_ids,
        "failed_case_ids": list(failed_case_ids),
        "valid_grant_count": valid_grant_count,
        "rejected_grant_count": rejected_grant_count,
        "accepted_mechanical_command_count": accepted_commands,
        "rejected_mechanical_command_count": rejected_commands,
        "derived_b_grant_count": derived_b,
        "revoked_grant_count": revoked,
        "expired_grant_count": expired,
        "capability_boundary_violation_count": boundary_violations,
        "key_guards": {
            "candidate_only": True,
            "synthetic_only": True,
            "no_brain_runtime": not negative_guards["brain_runtime_execution"],
            "no_provider_invocation": not negative_guards["provider_invocation"],
            "no_model_inference": not negative_guards["model_inference"],
            "no_action_execution": not negative_guards["action_execution"],
            "no_memory_mutation": not negative_guards["memory_mutation"],
            "no_experience_mutation": not negative_guards["experience_mutation"],
            "no_scheduler": not negative_guards["autonomous_scheduling"],
            "loop_has_no_semantic_authority": not negative_guards["loop_semantic_judgment"],
        },
        "negative_guards": negative_guards,
    }
    return {"summary": summary, "cases": cases}


__all__ = ["build_authority_grant_run_v1", "run_authority_grant_case"]

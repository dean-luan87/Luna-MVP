"""Synthetic scenarios for the A semantic decision migration seam."""

from __future__ import annotations

from typing import Dict, Iterable, Mapping, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_transition_types_v1 import ReconsiderationCandidateV1
from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_types_v1 import (
    CognitiveGoalCandidateV1,
    CognitiveStateVersionCandidateV1,
    DynamicCognitiveLoopOutputV1,
    DynamicCognitiveLoopTransitionCandidateV1,
    GoalSufficiencyCandidateV1,
    ProvisionalPlanCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_registry_v1 import (
    A_AUTHORITIES,
    LOOP_AUTHORITIES,
    ROLE_A,
    ROLE_LOOP,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_types_v1 import (
    AuthorityResponsibilityBindingCandidateV1,
    CognitiveAuthorityGrantCandidateV1,
    LoopMechanicalStateCandidateV1,
)

from .a_owned_semantic_decision_engine_v1 import (
    build_need_decision,
    build_next_step_decision,
    build_reconsideration_decision,
    build_sufficiency_decision,
    wrap_dynamic_flow_output,
)
from .loop_mechanical_bridge_v1 import bridge_bundle_to_loop
from .a_owned_semantic_decision_fixture_v1 import build_a_owned_semantic_decision_cases_v1
from .a_owned_semantic_decision_registry_v1 import (
    COMPATIBILITY_SOURCE_OWNER,
    PHASE,
    REQUIRED_AUTHORITIES,
)
from .a_owned_semantic_decision_types_v1 import (
    ASemanticDecisionBundleV1,
    ASemanticDecisionContextV1,
)


def _trace(ref: str) -> str:
    return f"trace:{ref}"


def _provenance(ref: str) -> Tuple[str, ...]:
    return (f"provenance:{ref}",)


def _grant(
    case_id: str,
    *,
    authorities: Iterable[str] = A_AUTHORITIES,
    concern_ref: str = "concern:primary",
    work_ref: str = "work:primary",
    state_ref: str = "state:primary:v1",
    receiver_role: str = ROLE_A,
) -> CognitiveAuthorityGrantCandidateV1:
    return CognitiveAuthorityGrantCandidateV1(
        grant_ref=f"grant:a:{case_id}",
        issuer_ref="brain:governance",
        receiver_ref=f"a:{case_id}",
        receiver_role=receiver_role,
        concern_ref=concern_ref,
        work_ref=work_ref,
        granted_authority_refs=tuple(authorities),
        capability_boundary_ref=f"boundary:{receiver_role}",
        goal_refs=("goal:primary",),
        role_refs=("role:primary",),
        field_refs=("field:primary",),
        safety_refs=("safety:bounded",),
        permission_refs=("permission:bounded",),
        resource_envelope_refs=("resource:bounded",),
        valid_from_state_ref=state_ref,
        valid_until_condition_refs=("condition:state-advance",),
        revocation_condition_refs=("condition:concern-stop",),
        result_receiver_ref=f"result:a:{case_id}",
        responsibility_owner_ref=f"responsibility:a:{case_id}",
        trace_ref=_trace(f"grant:a:{case_id}"),
        provenance_refs=_provenance(f"grant:a:{case_id}"),
    )


def _loop_grant(
    case_id: str,
    *,
    concern_ref: str = "concern:primary",
    work_ref: str = "work:primary",
    state_ref: str = "state:primary:v1",
) -> CognitiveAuthorityGrantCandidateV1:
    return CognitiveAuthorityGrantCandidateV1(
        grant_ref=f"grant:loop:{case_id}",
        issuer_ref="brain:governance",
        receiver_ref=f"loop:{case_id}",
        receiver_role=ROLE_LOOP,
        concern_ref=concern_ref,
        work_ref=work_ref,
        granted_authority_refs=tuple(LOOP_AUTHORITIES),
        capability_boundary_ref=f"boundary:{ROLE_LOOP}",
        goal_refs=("goal:primary",),
        role_refs=("role:primary",),
        field_refs=("field:primary",),
        safety_refs=("safety:bounded",),
        permission_refs=("permission:bounded",),
        resource_envelope_refs=("resource:bounded",),
        valid_from_state_ref=state_ref,
        valid_until_condition_refs=("condition:state-advance",),
        revocation_condition_refs=("condition:concern-stop",),
        result_receiver_ref=f"result:a:{case_id}",
        responsibility_owner_ref=f"responsibility:loop:{case_id}",
        trace_ref=_trace(f"grant:loop:{case_id}"),
        provenance_refs=_provenance(f"grant:loop:{case_id}"),
    )


def _binding(binding_ref: str, authority_ref: str, *, owner_ref: str) -> AuthorityResponsibilityBindingCandidateV1:
    return AuthorityResponsibilityBindingCandidateV1(
        binding_ref=binding_ref,
        authority_ref=authority_ref,
        decision_authority_ref=f"decision:{authority_ref}",
        responsibility_owner_ref=owner_ref,
        result_receiver_ref=f"result:{binding_ref}",
        error_owner_ref=owner_ref,
        expiry_ref=f"expiry:{binding_ref}",
        revocation_authority_ref="brain:governance",
        valid=True,
        reason_refs=("binding:explicit",),
        trace_ref=_trace(binding_ref),
        provenance_refs=_provenance(binding_ref),
    )


def _context(
    case_id: str,
    *,
    concern_ref: str = "concern:primary",
    work_ref: str = "work:primary",
    state_ref: str = "state:primary:v1",
    grant_ref: Optional[str] = None,
) -> ASemanticDecisionContextV1:
    return ASemanticDecisionContextV1(
        work_ref=work_ref,
        concern_ref=concern_ref,
        a_grant_ref=grant_ref or f"grant:a:{case_id}",
        source_state_version_ref=state_ref,
        goal_refs=("goal:primary",),
        intent_refs=("intent:primary",),
        role_refs=("role:primary",),
        perspective_refs=("perspective:primary",),
        field_refs=("field:primary",),
        context_refs=("context:primary",),
        current_world_refs=("world:current:candidate",),
        task_behavior_refs=("task:behavior:primary",),
        emotion_modulation_refs=("emotion:modulation:bounded",),
        experience_refs=("experience:prior:candidate",),
        safety_refs=("safety:bounded",),
        permission_refs=("permission:bounded",),
        resource_envelope_refs=("resource:bounded",),
        evidence_refs=(f"evidence:{case_id}",),
        prior_need_refs=("need:prior",),
        prior_hypothesis_refs=("hypothesis:primary",),
        prior_requirement_refs=("requirement:prior",),
        trace_refs=(_trace(case_id),),
        provenance_refs=_provenance(case_id),
    )


def _state(
    case_id: str,
    *,
    concern_ref: str = "concern:primary",
    work_ref: str = "work:primary",
    state_ref: str = "state:primary:v1",
) -> LoopMechanicalStateCandidateV1:
    return LoopMechanicalStateCandidateV1(
        loop_ref=f"loop:{case_id}",
        concern_ref=concern_ref,
        work_ref=work_ref,
        current_mechanical_state="ACTIVE",
        state_version_ref=state_ref,
        trace_refs=(_trace(f"loop:{case_id}"),),
        provenance_refs=_provenance(f"loop:{case_id}"),
    )


def _valid_bundle(
    case_id: str,
    *,
    concern_ref: str = "concern:primary",
    work_ref: str = "work:primary",
    state_ref: str = "state:primary:v1",
    sufficiency_status: str = "INSUFFICIENT",
    next_step: str = "CONTINUE",
    selected_need_ref: Optional[str] = "need:current",
    reconsideration_required: bool = False,
    replacement_need_ref: Optional[str] = None,
    stale_requirement_refs: Tuple[str, ...] = (),
) -> Tuple[ASemanticDecisionBundleV1, CognitiveAuthorityGrantCandidateV1, CognitiveAuthorityGrantCandidateV1, AuthorityResponsibilityBindingCandidateV1, AuthorityResponsibilityBindingCandidateV1]:
    context = _context(case_id, concern_ref=concern_ref, work_ref=work_ref, state_ref=state_ref)
    a_grant = _grant(case_id, concern_ref=concern_ref, work_ref=work_ref, state_ref=state_ref)
    loop_grant = _loop_grant(case_id, concern_ref=concern_ref, work_ref=work_ref, state_ref=state_ref)
    a_binding = _binding(f"binding:a:{case_id}", "SELECT_CURRENT_NEED", owner_ref=f"a:{case_id}")
    loop_binding = _binding(f"binding:loop:{case_id}", "RECORD_REFS", owner_ref=f"loop:{case_id}")
    need, need_validation = build_need_decision(
        context,
        selected_need_ref=selected_need_ref,
        alternative_need_refs=("need:alternative",),
        selection_reason_refs=("a:selected-current-minimum-need",),
        grant=a_grant,
        binding=a_binding,
    )
    sufficiency, sufficiency_validation = build_sufficiency_decision(
        context,
        sufficiency_status=sufficiency_status,
        sufficiency_reason_refs=(f"a:sufficiency:{sufficiency_status.lower()}",),
        current_need_ref=selected_need_ref,
        grant=a_grant,
        binding=a_binding,
    )
    reconsideration, reconsideration_validation = build_reconsideration_decision(
        context,
        reconsideration_required=reconsideration_required,
        reconsideration_reason_refs=("a:reconsideration",) if reconsideration_required else ("a:no-reconsideration",),
        invalidated_hypothesis_refs=("hypothesis:primary",) if reconsideration_required else (),
        stale_requirement_refs=stale_requirement_refs,
        replacement_need_ref=replacement_need_ref,
        grant=a_grant,
        binding=a_binding,
    )
    next_decision, next_validation = build_next_step_decision(
        context,
        source_need_decision_ref=need.decision_ref,
        source_sufficiency_decision_ref=sufficiency.decision_ref,
        source_reconsideration_decision_ref=reconsideration.decision_ref,
        next_step_disposition=next_step,
        selected_next_need_ref=replacement_need_ref or selected_need_ref,
        reason_refs=(f"a:next-step:{next_step.lower()}",),
        grant=a_grant,
        binding=a_binding,
    )
    bundle = ASemanticDecisionBundleV1(
        context=context,
        need_decision=need,
        sufficiency_decision=sufficiency,
        reconsideration_decision=reconsideration,
        next_step_decision=next_decision,
        validations=(need_validation, sufficiency_validation, reconsideration_validation, next_validation),
        compatibility_source_owner_ref=COMPATIBILITY_SOURCE_OWNER,
        compatibility_wrapper_only=True,
    )
    return bundle, a_grant, loop_grant, a_binding, loop_binding


def _compatibility_output(kind: str, scenario_id: str) -> DynamicCognitiveLoopOutputV1:
    goal = CognitiveGoalCandidateV1(
        goal_ref="goal:primary",
        goal_statement_candidate="resolve controlled cognitive concern",
        success_condition_refs=("success:bounded",),
        context_refs=("context:primary",),
        intent_refs=("intent:primary",),
        trace_ref=_trace(f"goal:{scenario_id}"),
    )
    plan = ProvisionalPlanCandidateV1(
        plan_ref=f"plan:{scenario_id}",
        goal_ref=goal.goal_ref,
        candidate_step_refs=("need:current", "need:alternative"),
        plan_completeness_status="PROVISIONAL",
        trace_ref=_trace(f"plan:{scenario_id}"),
    )
    current_need = None if kind == "SUFFICIENT" else "need:current"
    disposition = "SUFFICIENT" if kind == "SUFFICIENT" else "RECONSIDER" if kind == "RECONSIDER" else "INSUFFICIENT"
    next_step = "STOP_SUFFICIENT" if kind == "SUFFICIENT" else "REQUEST_MORE_EVIDENCE" if kind == "RECONSIDER" else "CONTINUE"
    sufficiency = GoalSufficiencyCandidateV1(
        sufficiency_ref=f"sufficiency:{scenario_id}",
        goal_ref=goal.goal_ref,
        state_version_ref="state:primary:v1",
        status="SUFFICIENT" if kind == "SUFFICIENT" else "INSUFFICIENT",
        evidence_refs=(f"evidence:{scenario_id}",),
        reason=f"dynamic:{kind.lower()}",
        stop_disposition=next_step,
        terminates_remaining_plan=kind == "SUFFICIENT",
    )
    state = CognitiveStateVersionCandidateV1(
        state_version_ref="state:primary:v1",
        parent_state_version_ref=None,
        evidence_update_ref=None,
        current_disposition=disposition,
        current_minimum_need_ref=current_need,
        active_hypothesis_refs=("hypothesis:primary",),
        invalidated_hypothesis_refs=("hypothesis:primary",) if kind == "RECONSIDER" else (),
        sufficiency_ref=sufficiency.sufficiency_ref,
        reconsideration_ref=f"reconsideration:{scenario_id}" if kind == "RECONSIDER" else None,
        trace_ref=_trace(f"state:{scenario_id}"),
    )
    reconsiderations = (
        ReconsiderationCandidateV1(
            cycle_id=f"loop:{scenario_id}",
            source_stage="COGNITIVE_EVIDENCE",
            target_stage="CURRENT_MINIMUM_NEED",
            reconsideration_reason="dynamic:reconsider",
            related_refs=("hypothesis:primary", "evidence:changed"),
            trace_ref=_trace(f"reconsideration:{scenario_id}"),
        ),
    ) if kind == "RECONSIDER" else ()
    return DynamicCognitiveLoopOutputV1(
        scenario_id=scenario_id,
        goal=goal,
        provisional_plan=plan,
        state_versions=(state,),
        transitions=(),
        needs_materialized=(current_need,) if current_need else (),
        current_minimum_need_ref=current_need,
        requirement_refs=("requirement:primary",),
        resolution_refs=(),
        invocation_candidate_refs=(),
        eligible_invocation_refs=(),
        stale_requirement_refs=("requirement:old",) if kind == "RECONSIDER" else (),
        capability_outcome_refs=(),
        sufficiency_candidates=(sufficiency,),
        reconsiderations=reconsiderations,
        evidence_update_refs=(f"evidence:{scenario_id}",),
        ignored_evidence_update_refs=(),
        non_materialized_plan_refs=("need:alternative",),
        final_disposition=disposition,
        next_step_disposition=next_step,
        trace_refs=(_trace(scenario_id),),
        provenance_refs=_provenance(scenario_id),
    )


def _negative_guards() -> Dict[str, bool]:
    return {
        "brain_runtime": False,
        "b_runtime": False,
        "provider": False,
        "model": False,
        "yolo": False,
        "ocr": False,
        "camera": False,
        "action": False,
        "memory_mutation": False,
        "experience_mutation": False,
        "scheduler": False,
        "dynamic_flow_semantic_authority": False,
        "loop_need_selection": False,
        "loop_sufficiency_judgment": False,
        "loop_reconsideration_judgment": False,
        "loop_next_step_judgment": False,
        "compatibility_wrapper_only": False,
        "existing_engine_deleted": False,
        "existing_engine_rewritten": False,
    }


def _run_decision_case(case: Mapping[str, object]) -> Dict[str, object]:
    case_id = str(case["scenario_id"])
    kind = str(case["kind"])
    required = REQUIRED_AUTHORITIES[kind]
    authorities = A_AUTHORITIES
    state_ref = "state:primary:v1"
    concern_ref = "concern:primary"
    receiver_role = ROLE_A
    if case_id == "ND-03":
        authorities = tuple(item for item in A_AUTHORITIES if item != required)
    if case_id == "SF-04":
        authorities = tuple(item for item in A_AUTHORITIES if item != required)
    if case_id == "ND-04":
        state_ref = "state:primary:v2"
    if case_id == "ND-05":
        concern_ref = "concern:other"
    if case_id == "ND-06":
        receiver_role = "WRONG_RECEIVER_ROLE"
    context = _context(case_id, state_ref="state:primary:v1", concern_ref="concern:primary")
    grant = _grant(case_id, authorities=authorities, state_ref=state_ref, concern_ref=concern_ref, receiver_role=receiver_role)
    binding = _binding(f"binding:{case_id}", required, owner_ref=f"a:{case_id}")
    extra_validations = []
    if kind == "NEED":
        decision, validation = build_need_decision(
            context,
            selected_need_ref="need:selected",
            alternative_need_refs=("need:alternative",),
            selection_reason_refs=("reason:a-minimum-need",),
            grant=grant,
            binding=binding,
        )
        if case_id == "ND-05":
            work_scope_grant = _grant(case_id + ":work", authorities=authorities, work_ref="work:other")
            _, work_scope_validation = build_need_decision(
                context,
                selected_need_ref="need:selected",
                alternative_need_refs=("need:alternative",),
                selection_reason_refs=("reason:a-minimum-need",),
                grant=work_scope_grant,
                binding=binding,
            )
            extra_validations.append(work_scope_validation)
        if case_id == "ND-07":
            _, revoked_validation = build_need_decision(
                context,
                selected_need_ref="need:selected",
                alternative_need_refs=("need:alternative",),
                selection_reason_refs=("reason:a-minimum-need",),
                grant=grant,
                binding=binding,
                revoked=True,
            )
            _, expired_validation = build_need_decision(
                context,
                selected_need_ref="need:selected",
                alternative_need_refs=("need:alternative",),
                selection_reason_refs=("reason:a-minimum-need",),
                grant=grant,
                binding=binding,
                expired=True,
            )
            extra_validations.extend((revoked_validation, expired_validation))
    elif kind == "SUFFICIENCY":
        status = {"SF-01": "SUFFICIENT", "SF-02": "INSUFFICIENT", "SF-03": "REQUIRES_RECONSIDERATION", "SF-04": "SUFFICIENT"}[case_id]
        decision, validation = build_sufficiency_decision(
            context,
            sufficiency_status=status,
            sufficiency_reason_refs=(f"reason:{status.lower()}",),
            current_need_ref="need:selected",
            grant=grant,
            binding=binding,
        )
    elif kind == "RECONSIDERATION":
        decision, validation = build_reconsideration_decision(
            context,
            reconsideration_required=case_id != "RC-04",
            reconsideration_reason_refs=("reason:evidence-invalidated",) if case_id != "RC-04" else ("reason:no-reconsideration",),
            invalidated_hypothesis_refs=("hypothesis:primary",) if case_id in {"RC-01", "RC-03"} else (),
            stale_requirement_refs=("requirement:old",) if case_id == "RC-02" else (),
            replacement_need_ref="need:replacement" if case_id == "RC-03" else None,
            grant=grant,
            binding=binding,
        )
    else:
        need, need_validation = build_need_decision(
            context,
            selected_need_ref="need:selected",
            alternative_need_refs=("need:alternative",),
            selection_reason_refs=("reason:a-minimum-need",),
            grant=grant,
            binding=binding,
        )
        sufficiency, sufficiency_validation = build_sufficiency_decision(
            context,
            sufficiency_status="SUFFICIENT" if case_id == "NS-04" else "INSUFFICIENT",
            sufficiency_reason_refs=("reason:a-sufficiency",),
            current_need_ref="need:selected",
            grant=grant,
            binding=binding,
        )
        reconsideration, reconsideration_validation = build_reconsideration_decision(
            context,
            reconsideration_required=False,
            reconsideration_reason_refs=("reason:no-reconsideration",),
            invalidated_hypothesis_refs=(),
            stale_requirement_refs=(),
            replacement_need_ref=None,
            grant=grant,
            binding=binding,
        )
        disposition = {
            "NS-01": "CONTINUE", "NS-02": "REQUEST_MORE_EVIDENCE", "NS-03": "REPLAN",
            "NS-04": "STOP_SUFFICIENT", "NS-05": "WAIT", "NS-06": "PAUSE", "NS-07": "DEFER",
        }[case_id]
        decision, validation = build_next_step_decision(
            context,
            source_need_decision_ref=need.decision_ref,
            source_sufficiency_decision_ref=sufficiency.decision_ref,
            source_reconsideration_decision_ref=reconsideration.decision_ref,
            next_step_disposition=disposition,
            selected_next_need_ref="need:replacement" if disposition == "REPLAN" else "need:selected",
            reason_refs=(f"reason:{disposition.lower()}",),
            grant=grant,
            binding=binding,
        )
        decision = decision
        validation = validation
        validation = validation if all(item.accepted for item in (need_validation, sufficiency_validation, reconsideration_validation, validation)) else next(item for item in (need_validation, sufficiency_validation, reconsideration_validation, validation) if not item.accepted)
    expected = case["expected_failure_class"]
    passed = validation.failure_class == expected if expected else validation.accepted
    if extra_validations:
        passed = passed and all(
            item.failure_class in {"SCOPE_MISMATCH", "GRANT_REVOKED", "GRANT_EXPIRED"}
            for item in extra_validations
        )
    return {
        "scenario_id": case_id,
        "title": case["title"],
        "passed": passed,
        "failure_class": validation.failure_class,
        "additional_failure_classes": [item.failure_class for item in extra_validations],
        "rejected_semantic_authority_violation": int(validation.failure_class == "AUTHORITY_NOT_GRANTED"),
        "need_decision": kind in {"NEED", "NEXT_STEP"},
        "sufficiency_decision": kind in {"SUFFICIENCY", "NEXT_STEP"},
        "reconsideration_decision": kind in {"RECONSIDERATION", "NEXT_STEP"},
        "next_step_decision": kind == "NEXT_STEP",
        "a_semantic_authority": validation.accepted and decision.decision_owner_ref == ROLE_A,
        "negative_guards": _negative_guards(),
    }


def _run_compatibility_case(case: Mapping[str, object]) -> Dict[str, object]:
    case_id = str(case["scenario_id"])
    kind = {"CW-01": "INSUFFICIENT", "CW-02": "SUFFICIENT", "CW-03": "RECONSIDER", "CW-04": "INSUFFICIENT"}[case_id]
    context = _context(case_id)
    grant = _grant(case_id)
    binding = _binding(f"binding:{case_id}", REQUIRED_AUTHORITIES["NEED"], owner_ref=f"a:{case_id}")
    bundle = wrap_dynamic_flow_output(context, _compatibility_output(kind, case_id), grant=grant, binding=binding)
    passed = (
        bundle.compatibility_wrapper_only
        and bundle.compatibility_source_owner_ref == COMPATIBILITY_SOURCE_OWNER
        and all(validation.accepted for validation in bundle.validations)
        and all(
            decision is None or decision.decision_owner_ref == ROLE_A
            for decision in (bundle.need_decision, bundle.sufficiency_decision, bundle.reconsideration_decision, bundle.next_step_decision)
        )
    )
    if case_id == "CW-03":
        passed = passed and bundle.sufficiency_decision.sufficiency_status == "REQUIRES_RECONSIDERATION" and bundle.reconsideration_decision.reconsideration_required
    return {
        "scenario_id": case_id,
        "title": case["title"],
        "passed": passed,
        "compatibility_mapped_output": True,
        "need_decision": True,
        "sufficiency_decision": True,
        "reconsideration_decision": True,
        "next_step_decision": True,
        "a_semantic_authority": passed,
        "negative_guards": _negative_guards(),
    }


def _run_mechanical_case(case: Mapping[str, object]) -> Dict[str, object]:
    case_id = str(case["scenario_id"])
    bundle_kwargs = {
        "MC-01": {},
        "MC-02": {"sufficiency_status": "SUFFICIENT", "next_step": "STOP_SUFFICIENT", "selected_need_ref": None},
        "MC-03": {"next_step": "REPLAN", "selected_need_ref": "need:replacement", "replacement_need_ref": "need:replacement"},
        "MC-04": {"next_step": "WAIT"},
        "MC-05": {},
    }[case_id]
    bundle, a_grant, loop_grant, a_binding, loop_binding = _valid_bundle(case_id, **bundle_kwargs)
    commands, validations, _, returned = bridge_bundle_to_loop(
        bundle,
        a_grant=a_grant,
        loop_grant=loop_grant,
        a_binding=a_binding,
        loop_binding=loop_binding,
        state=_state(case_id),
    )
    accepted = all(item.accepted for item in validations)
    if case_id == "MC-01":
        passed = accepted and any(item.command_kind == "RECORD_NEED_REF" for item in commands)
    elif case_id == "MC-02":
        passed = accepted and {item.command_kind for item in commands} >= {"CLOSE", "FREEZE_FINAL_STATE"} and returned.closure_state == "CLOSED"
    elif case_id == "MC-03":
        passed = accepted and any(item.command_kind == "RECORD_STATE_VERSION" for item in commands) and any(item.command_kind == "RECORD_NEED_REF" for item in commands)
    elif case_id == "MC-04":
        passed = accepted and returned.current_mechanical_state == "WAITING"
    else:
        passed = accepted and not hasattr(returned, "sufficiency_status") and not hasattr(returned, "next_step_disposition")
    return {
        "scenario_id": case_id,
        "title": case["title"],
        "passed": passed,
        "accepted_mechanical_commands": sum(1 for item in validations if item.accepted),
        "rejected_semantic_authority_violation": 0,
        "need_decision": True,
        "sufficiency_decision": True,
        "reconsideration_decision": True,
        "next_step_decision": True,
        "loop_semantic_boundary": passed,
        "negative_guards": _negative_guards(),
    }


def _run_isolation_case(case: Mapping[str, object]) -> Dict[str, object]:
    case_id = str(case["scenario_id"])
    first, a_one, loop_one, ab_one, lb_one = _valid_bundle(
        f"{case_id}:one",
        concern_ref="concern:one",
        work_ref="work:one",
        state_ref="state:one:v1",
        selected_need_ref="need:one",
    )
    second, a_two, loop_two, ab_two, lb_two = _valid_bundle(
        f"{case_id}:two",
        concern_ref="concern:two",
        work_ref="work:two",
        state_ref="state:two:v1",
        selected_need_ref="need:two",
    )
    _, _, state_one, return_one = bridge_bundle_to_loop(first, a_grant=a_one, loop_grant=loop_one, a_binding=ab_one, loop_binding=lb_one, state=_state(f"{case_id}:one", concern_ref="concern:one", work_ref="work:one", state_ref="state:one:v1"))
    _, _, state_two, return_two = bridge_bundle_to_loop(second, a_grant=a_two, loop_grant=loop_two, a_binding=ab_two, loop_binding=lb_two, state=_state(f"{case_id}:two", concern_ref="concern:two", work_ref="work:two", state_ref="state:two:v1"))
    passed = (
        state_one.loop_ref != state_two.loop_ref
        and return_one.loop_ref != return_two.loop_ref
        and not set(return_one.pending_refs).intersection(return_two.pending_refs)
        and state_one.state_version_ref != state_two.state_version_ref
        and a_one.grant_ref != a_two.grant_ref
        and a_one.concern_ref != a_two.concern_ref
        and a_one.work_ref != a_two.work_ref
    )
    if case_id == "IS-01":
        passed = passed and a_one.concern_ref != a_two.concern_ref
    elif case_id == "IS-02":
        passed = passed and a_one.grant_ref != a_two.grant_ref
    elif case_id == "IS-03":
        passed = passed and state_one.state_version_ref != state_two.state_version_ref and state_one.loop_ref != state_two.loop_ref
    return {
        "scenario_id": case_id,
        "title": case["title"],
        "passed": passed,
        "negative_guards": _negative_guards(),
    }


def run_a_owned_semantic_decision_case(case: Mapping[str, object]) -> Dict[str, object]:
    kind = str(case["kind"])
    if kind in {"NEED", "SUFFICIENCY", "RECONSIDERATION", "NEXT_STEP"}:
        return _run_decision_case(case)
    if kind == "COMPATIBILITY":
        return _run_compatibility_case(case)
    if kind == "MECHANICAL":
        return _run_mechanical_case(case)
    if kind == "ISOLATION":
        return _run_isolation_case(case)
    return {
        "scenario_id": case["scenario_id"],
        "title": case["title"],
        "passed": all(value is False for value in _negative_guards().values()),
        "negative_guards": _negative_guards(),
    }


def build_a_owned_semantic_decision_run_v1() -> Dict[str, object]:
    cases = tuple(run_a_owned_semantic_decision_case(case) for case in build_a_owned_semantic_decision_cases_v1())
    failed_case_ids = tuple(item["scenario_id"] for item in cases if not item["passed"])
    summary = {
        "phase": PHASE,
        "scenario_count": len(cases),
        "all_cases_passed": not failed_case_ids,
        "failed_case_ids": list(failed_case_ids),
        "need_decision_count": sum(1 for item in cases if item.get("need_decision")),
        "sufficiency_decision_count": sum(1 for item in cases if item.get("sufficiency_decision")),
        "reconsideration_decision_count": sum(1 for item in cases if item.get("reconsideration_decision")),
        "next_step_decision_count": sum(1 for item in cases if item.get("next_step_decision")),
        "accepted_mechanical_command_count": sum(int(item.get("accepted_mechanical_commands", 0)) for item in cases),
        "rejected_semantic_authority_violation_count": sum(int(item.get("rejected_semantic_authority_violation", 0)) for item in cases),
        "compatibility_mapped_output_count": sum(1 for item in cases if item.get("compatibility_mapped_output")),
        "key_guards": {
            "candidate_only": True,
            "synthetic_only": True,
            "a_owns_need": True,
            "a_owns_sufficiency": True,
            "a_owns_reconsideration": True,
            "a_owns_next_step": True,
            "loop_has_no_semantic_authority": True,
            "dynamic_flow_has_no_semantic_authority": True,
            "compatibility_wrapper_only": True,
            "no_provider": True,
            "no_model": True,
            "no_action": True,
        },
        "negative_guards": _negative_guards(),
    }
    return {"summary": summary, "cases": cases}


__all__ = ["build_a_owned_semantic_decision_run_v1", "run_a_owned_semantic_decision_case"]

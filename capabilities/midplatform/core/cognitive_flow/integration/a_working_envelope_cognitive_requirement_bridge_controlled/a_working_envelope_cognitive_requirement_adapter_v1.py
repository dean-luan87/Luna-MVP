"""Controlled scenario adapter for the A working-envelope bridge."""

from __future__ import annotations

from typing import Dict, Iterable, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_engine_v1 import (
    build_need_decision,
    build_reconsideration_decision,
    build_sufficiency_decision,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_types_v1 import (
    ASemanticDecisionContextV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_registry_v1 import (
    A_AUTHORITIES,
    ROLE_A,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_types_v1 import (
    AuthorityResponsibilityBindingCandidateV1,
    CognitiveAuthorityGrantCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.capability_scope_resolution_fixture_v1 import (
    build_scope_modules,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
    CognitiveNeedCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_governance_v1 import (
    assess_official_module_admission,
    assess_slot_compatibility,
    build_binding_candidate,
    govern_binding,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_types_v1 import (
    UniversalCapabilitySlotV1,
)

from .a_working_envelope_cognitive_requirement_engine_v1 import (
    assess_environment_impact,
    bridge_to_existing_capability_requirement,
    build_a_cognitive_requirement,
    build_envelope_version,
    build_evidence_return,
    build_invalidation,
    build_observation_candidate,
    build_working_envelope,
    resolve_existing_capability_requirement,
)
from .a_working_envelope_cognitive_requirement_fixture_v1 import build_scenarios
from .a_working_envelope_cognitive_requirement_registry_v1 import (
    NEGATIVE_GUARDS,
    SUPPORTED_REQUESTS,
)


def _binding(ref: str, authority: str) -> AuthorityResponsibilityBindingCandidateV1:
    return AuthorityResponsibilityBindingCandidateV1(
        binding_ref=ref,
        authority_ref=authority,
        decision_authority_ref=ROLE_A,
        responsibility_owner_ref=ROLE_A,
        result_receiver_ref=ROLE_A,
        error_owner_ref=ROLE_A,
        expiry_ref=f"expiry:{ref}",
        revocation_authority_ref="brain:governance",
        valid=True,
        reason_refs=("a-working-envelope-controlled-binding",),
        trace_ref=f"trace:{ref}",
        provenance_refs=(f"provenance:{ref}",),
    )


def _grant(
    work_ref: str,
    concern_ref: str,
    state_ref: str,
    *,
    grant_ref: Optional[str] = None,
    grant_state_ref: Optional[str] = None,
    authorities: Iterable[str] = A_AUTHORITIES,
) -> Tuple[CognitiveAuthorityGrantCandidateV1, AuthorityResponsibilityBindingCandidateV1]:
    actual_grant_ref = grant_ref or f"grant:{work_ref}"
    grant = CognitiveAuthorityGrantCandidateV1(
        grant_ref=actual_grant_ref,
        issuer_ref="brain:governance",
        receiver_ref=f"a:{work_ref}",
        receiver_role=ROLE_A,
        concern_ref=concern_ref,
        work_ref=work_ref,
        granted_authority_refs=tuple(authorities),
        capability_boundary_ref="boundary:A_REASONING_ROLE",
        goal_refs=(f"goal:{concern_ref}",),
        role_refs=("role:default",),
        field_refs=(f"field:{work_ref}",),
        safety_refs=("safety:controlled",),
        permission_refs=("permission:controlled",),
        resource_envelope_refs=("resource:controlled",),
        valid_from_state_ref=grant_state_ref or state_ref,
        valid_until_condition_refs=(f"valid-until:{actual_grant_ref}",),
        revocation_condition_refs=(f"revoke:{actual_grant_ref}",),
        result_receiver_ref="brain:assimilation-boundary",
        responsibility_owner_ref=ROLE_A,
        trace_ref=f"trace:{actual_grant_ref}",
        provenance_refs=(f"provenance:{actual_grant_ref}",),
    )
    return grant, _binding(f"binding:{actual_grant_ref}", "REQUEST_CAPABILITY")


def _context(envelope, state_ref: str) -> ASemanticDecisionContextV1:
    return ASemanticDecisionContextV1(
        work_ref=envelope.work_ref,
        concern_ref=envelope.concern_ref,
        a_grant_ref=envelope.authority_grant_ref,
        source_state_version_ref=state_ref,
        goal_refs=envelope.goal_refs,
        intent_refs=(f"intent:{envelope.concern_ref}",),
        role_refs=envelope.role_refs,
        perspective_refs=envelope.perspective_refs,
        field_refs=envelope.field_refs,
        context_refs=envelope.context_refs,
        current_world_refs=envelope.current_world_refs,
        task_behavior_refs=envelope.task_refs + envelope.behavior_refs,
        emotion_modulation_refs=envelope.emotion_modulation_refs,
        experience_refs=envelope.experience_prior_refs,
        safety_refs=envelope.safety_refs,
        permission_refs=envelope.permission_refs,
        resource_envelope_refs=envelope.resource_envelope_refs,
        evidence_refs=(f"evidence:{envelope.work_ref}:prior",),
        prior_need_refs=(),
        prior_hypothesis_refs=(f"hypothesis:{envelope.concern_ref}:prior",),
        prior_requirement_refs=(),
        trace_refs=envelope.trace_refs,
        provenance_refs=envelope.provenance_refs,
    )


def _slot(module, slot_id: str) -> UniversalCapabilitySlotV1:
    empty = UniversalCapabilitySlotV1(
        slot_id=slot_id,
        slot_version="v1",
        lifecycle_state="EMPTY",
        current_module_binding=None,
        compatibility_refs=("compatibility:universal-slot-v1",),
        resource_refs=("resource:controlled",),
        permission_refs=("permission:capability-governance",),
        health_refs=(f"health:{slot_id}",),
        provenance_refs=(f"provenance:{slot_id}",),
        history_refs=(),
        recovery_refs=(),
        trace_refs=(f"trace:{slot_id}",),
        self_visibility="EMPTY",
    )
    admission = assess_official_module_admission(module)
    compatibility = assess_slot_compatibility(empty, module, admission)
    candidate = build_binding_candidate(empty, module, admission, compatibility)
    return govern_binding(empty, module, candidate).projected_slot


def _base(case_id: str) -> Dict[str, object]:
    work_ref = f"work:{case_id}"
    concern_ref = f"concern:{case_id}"
    state_ref = f"state:{case_id}:v1"
    grant_state = f"state:{case_id}:v0" if case_id == "NR-05" else state_ref
    grant_concern = f"concern:{case_id}:other" if case_id == "NR-04" else concern_ref
    grant, binding = _grant(work_ref, grant_concern, state_ref, grant_state_ref=grant_state)
    envelope = build_working_envelope(
        work_ref=work_ref,
        concern_ref=concern_ref,
        authority_grant_ref=grant.grant_ref,
        source_state_version_ref=state_ref,
        goal_refs=(f"goal:{case_id}",),
        role_refs=(f"role:{case_id}",),
        perspective_refs=(f"perspective:{case_id}",),
        field_refs=(f"field:{case_id}",),
        context_refs=(f"context:{case_id}",),
        current_world_refs=(f"world:{case_id}:v1",),
        task_refs=(f"task:{case_id}",),
        behavior_refs=(f"behavior:{case_id}",),
        emotion_modulation_refs=(f"emotion:{case_id}",),
        experience_prior_refs=(f"experience:{case_id}",),
        attention_refs=(f"attention:{case_id}",),
        safety_refs=(f"safety:{case_id}",),
        permission_refs=(f"permission:{case_id}",),
        resource_envelope_refs=(f"resource:{case_id}",),
    )
    version = build_envelope_version(
        envelope,
        version_ref=f"envelope-version:{case_id}:v1",
        parent_version_ref=None,
        changed_source_refs=(),
        unchanged_source_refs=("role", "field", "context", "current_world", "task", "emotion", "safety", "permission", "resource"),
        change_reason_refs=("initial-working-envelope",),
    )
    context = _context(envelope, state_ref)
    need = CognitiveNeedCandidateV1(
        need_id=f"need:{case_id}",
        source_intent_ref=f"intent:{case_id}",
        source_context_ref=envelope.context_refs[0],
        source_field_ref=envelope.field_refs[0],
        source_hypothesis_ref=f"hypothesis:{case_id}:prior",
        source_attention_ref=envelope.attention_refs[0],
        problem_description="bounded missing information for current concern",
        missing_information_class="OBJECT_DETECTION",
        required_evidence_class="VISUAL_EVIDENCE_CANDIDATE",
        urgency="NORMAL",
        safety_relevance="NONE",
        trace_ref=f"trace:need:{case_id}",
        state_version_ref=state_ref,
    )
    need_decision, need_validation = build_need_decision(
        context,
        selected_need_ref=need.need_id,
        alternative_need_refs=(f"need:{case_id}:alternative",),
        selection_reason_refs=("current-minimum-information-gap",),
        grant=grant,
        binding=binding,
    )
    return {
        "case_id": case_id,
        "work_ref": work_ref,
        "concern_ref": concern_ref,
        "state_ref": state_ref,
        "grant": grant,
        "binding": binding,
        "envelope": envelope,
        "version": version,
        "context": context,
        "need": need,
        "need_decision": need_decision,
        "need_validation": need_validation,
    }


def _pipeline(case_id: str, request_type: str = "OBJECT_DETECTION", *, admitted: bool = True) -> Dict[str, object]:
    data = _base(case_id)
    cognitive_requirement = build_a_cognitive_requirement(
        need_decision=data["need_decision"],
        need=data["need"],
        work_ref=data["work_ref"],
        concern_ref=data["concern_ref"],
        source_state_version_ref=data["state_ref"],
        requested_information_type=request_type,
        information_gap_ref=f"gap:{case_id}",
        priority_ref=f"priority:{case_id}",
        required_evidence_characteristics_refs=("candidate-only", "traceable", "evidence-only"),
        resource_constraint_refs=("resource:controlled",),
        safety_refs=("safety:controlled",),
        permission_refs=("permission:controlled",),
        grant=data["grant"],
        binding=data["binding"],
    )
    formation = bridge_to_existing_capability_requirement(
        cognitive_requirement,
        data["need"],
        task_context="A working-envelope controlled bridge",
    )
    modules = build_scope_modules()
    slots = tuple(_slot(module, f"slot:{case_id}:{module.module_id}") for module in modules)
    scope, resolution, gap = resolve_existing_capability_requirement(formation, modules, slots)
    observation = build_observation_candidate(
        observation_ref=f"observation:{case_id}",
        evidence_refs=(f"evidence:{case_id}:candidate",),
        admitted=admitted,
        trace_ref=f"trace:observation:{case_id}",
    )
    evidence_return = build_evidence_return(
        work_ref=data["work_ref"],
        concern_ref=data["concern_ref"],
        cognitive_requirement=cognitive_requirement,
        formation=formation,
        scope_ref=f"scope:{formation.requirement_ref}",
        resolution_ref=f"resolution:{formation.requirement_ref}",
        observation_ref=observation.observation_id,
        admission_ref=f"admission:{observation.observation_id}",
        evidence_refs=observation.evidence_refs,
        state_version_ref=data["state_ref"],
    )
    data.update({
        "cognitive_requirement": cognitive_requirement,
        "formation": formation,
        "modules": modules,
        "slots": slots,
        "scope": scope,
        "resolution": resolution,
        "gap": gap,
        "observation": observation,
        "evidence_return": evidence_return,
    })
    return data


def run_case(case: Dict[str, object]) -> Dict[str, object]:
    case_id = str(case["case_id"])
    title = str(case["title"])
    try:
        if case_id.startswith("WE-"):
            data = _base(case_id)
            envelope = data["envelope"]
            checks = (
                envelope.candidate_only,
                envelope.synthetic_only,
                not envelope.authoritative_state_duplicated,
                envelope.source_owner_preserved,
                bool(envelope.role_refs and envelope.field_refs and envelope.context_refs),
                bool(envelope.task_refs and envelope.behavior_refs and envelope.emotion_modulation_refs),
                bool(envelope.experience_prior_refs and envelope.attention_refs),
            )
            passed = all(checks)
            details = {"working_envelope": envelope, "checks": checks}
        elif case_id.startswith("EI-"):
            data = _base(case_id)
            disposition = {
                "EI-01": "NO_MATERIAL_IMPACT",
                "EI-02": "REASSESS_HYPOTHESIS",
                "EI-03": "REASSESS_CURRENT_NEED",
                "EI-04": "REPLAN",
                "EI-05": "REASSESS_SUFFICIENCY",
                "EI-06": "PAUSE",
            }[case_id]
            changed = {
                "EI-01": (),
                "EI-02": ("role",),
                "EI-03": ("field",),
                "EI-04": ("task",),
                "EI-05": ("emotion", "resource"),
                "EI-06": ("current_world", "permission"),
            }[case_id]
            version = build_envelope_version(
                data["envelope"],
                version_ref=f"envelope-version:{case_id}:v2",
                parent_version_ref=data["version"].version_ref,
                changed_source_refs=changed,
                unchanged_source_refs=(),
                change_reason_refs=(f"change:{case_id}",),
            )
            impact = assess_environment_impact(
                data["envelope"], version, grant=data["grant"], binding=data["binding"],
                disposition=disposition, reason_refs=(f"reason:{case_id}",),
            )
            passed = impact.accepted and impact.impact_disposition == disposition and impact.changed_source_refs == changed
            details = {"impact": impact}
        elif case_id.startswith("NR-"):
            request_type = "TEXT_RECOGNITION" if case_id == "NR-02" else "OBJECT_DETECTION"
            data = _base(case_id)
            if case_id in {"NR-01", "NR-02", "NR-03"}:
                data = _pipeline(case_id, request_type)
                cognitive_requirement = data["cognitive_requirement"]
                passed = (
                    cognitive_requirement.issuing_owner_ref == ROLE_A
                    and not hasattr(cognitive_requirement, "provider_identity_ref")
                    and not hasattr(cognitive_requirement, "model_identity_ref")
                    and data["formation"].provider_selected is False
                )
                details = {"cognitive_requirement": cognitive_requirement, "formation": data["formation"]}
            else:
                if case_id == "NR-04":
                    data["grant"] = _grant(data["work_ref"], f"concern:{case_id}:other", data["state_ref"])[0]
                try:
                    _pipeline(case_id)
                    passed = False
                    details = {"blocked": False}
                except ValueError as error:
                    passed = True
                    details = {"blocked": True, "error": str(error)}
        elif case_id.startswith("CB-"):
            data = _pipeline(case_id)
            if case_id == "CB-02":
                text_module = data["modules"][0]
                scope, resolution, gap = resolve_existing_capability_requirement(data["formation"], (text_module,), (data["slots"][0],))
                passed = not scope.in_scope and gap is not None and resolution.status == "UNAVAILABLE_CANDIDATE"
                details = {"scope": scope, "resolution": resolution, "gap": gap}
            elif case_id == "CB-03":
                passed = data["scope"].in_scope and data["resolution"].status == "READY_CANDIDATE"
                details = {"scope": data["scope"], "resolution": data["resolution"]}
            else:
                passed = (
                    data["formation"].technical_implementation_selected is False
                    and data["formation"].model_selected is False
                    and data["formation"].provider_selected is False
                    and not hasattr(data["cognitive_requirement"], "provider_identity_ref")
                )
                details = {"formation": data["formation"]}
        elif case_id.startswith("OB-"):
            data = _pipeline(case_id, admitted=case_id != "OB-02")
            observation = data["observation"]
            passed = (
                observation.admission_state == ("REJECTED" if case_id == "OB-02" else "ADMITTED_OBSERVATION")
                and observation.candidate_only
                and not observation.truth_declared
                and not NEGATIVE_GUARDS["provider_invocation"]
            )
            if case_id == "OB-04":
                passed = not hasattr(observation, "need_authority") and observation.candidate_only
            details = {"observation": observation}
        elif case_id.startswith("ER-"):
            data = _pipeline(case_id)
            context = data["context"]
            if case_id == "ER-02":
                sufficiency, validation = build_sufficiency_decision(
                    context, sufficiency_status="INSUFFICIENT", sufficiency_reason_refs=("evidence-insufficient",),
                    current_need_ref=data["need"].need_id, grant=data["grant"], binding=data["binding"],
                )
                passed = data["evidence_return"].target_owner_ref == ROLE_A and validation.accepted and sufficiency.sufficiency_status == "INSUFFICIENT"
                details = {"evidence_return": data["evidence_return"], "sufficiency": sufficiency}
            elif case_id == "ER-03":
                sufficiency, validation = build_sufficiency_decision(
                    context, sufficiency_status="SUFFICIENT", sufficiency_reason_refs=("evidence-sufficient",),
                    current_need_ref=data["need"].need_id, grant=data["grant"], binding=data["binding"],
                )
                passed = data["evidence_return"].target_owner_ref == ROLE_A and validation.accepted and sufficiency.sufficiency_status == "SUFFICIENT"
                details = {"evidence_return": data["evidence_return"], "sufficiency": sufficiency}
            elif case_id == "ER-04":
                reconsideration, validation = build_reconsideration_decision(
                    context, reconsideration_required=True, reconsideration_reason_refs=("evidence-uncertain",),
                    invalidated_hypothesis_refs=context.prior_hypothesis_refs,
                    stale_requirement_refs=(data["formation"].requirement_ref,),
                    replacement_need_ref=f"need:{case_id}:replacement", grant=data["grant"], binding=data["binding"],
                )
                passed = data["evidence_return"].target_owner_ref == ROLE_A and validation.accepted and reconsideration.reconsideration_required
                details = {"evidence_return": data["evidence_return"], "reconsideration": reconsideration, "b_cr_candidate": "b-cr-request:synthetic"}
            else:
                passed = data["evidence_return"].target_owner_ref == ROLE_A and data["evidence_return"].candidate_only
                details = {"evidence_return": data["evidence_return"]}
        elif case_id.startswith("IV-"):
            data = _base(case_id)
            changed = {
                "IV-01": ("current_world",),
                "IV-02": ("role", "field"),
                "IV-03": ("current_world",),
            }[case_id]
            invalidation = build_invalidation(
                invalidation_ref=f"invalidation:{case_id}", source_change_refs=changed,
                envelope_ref=f"envelope:{data['envelope'].work_ref}", affected_state_version_ref=data["state_ref"],
                affected_grant_refs=(data["grant"].grant_ref,),
            )
            if case_id == "IV-03":
                passed = not hasattr(invalidation, "impact_disposition") and not hasattr(invalidation, "semantic_decision")
            else:
                passed = invalidation.candidate_only and invalidation.affected_grant_refs == (data["grant"].grant_ref,)
            details = {"invalidation": invalidation}
        elif case_id == "IS-01":
            first = _pipeline("IS-01-A")
            second = _pipeline("IS-01-B", "TEXT_RECOGNITION")
            first_refs = {first["work_ref"], first["concern_ref"], first["grant"].grant_ref, first["evidence_return"].return_ref}
            second_refs = {second["work_ref"], second["concern_ref"], second["grant"].grant_ref, second["evidence_return"].return_ref}
            passed = first_refs.isdisjoint(second_refs) and first["formation"].requirement_ref != second["formation"].requirement_ref
            details = {"first_refs": first_refs, "second_refs": second_refs}
        else:
            raise ValueError(f"unknown working-envelope scenario: {case_id}")
        return {"case_id": case_id, "title": title, "passed": bool(passed), "details": details}
    except Exception as error:
        return {"case_id": case_id, "title": title, "passed": False, "details": {"error": f"{type(error).__name__}: {error}"}}


def build_runner_result() -> Dict[str, object]:
    cases = tuple(run_case(case) for case in build_scenarios())
    failed = tuple(case["case_id"] for case in cases if not case["passed"])
    return {
        "phase": "Phase-Luna-A-Working-Envelope-And-Cognitive-Requirement-Bridge-Controlled-Implementation-v1-001",
        "scenario_count": len(cases),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "cases": cases,
        "negative_guards": dict(NEGATIVE_GUARDS),
    }

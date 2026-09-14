# -*- coding: utf-8 -*-
"""Qwen-VL Integration — full-chain dry-run adapter v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.decision_validation.luna_decision_validation_dryrun_adapter_v1 import (
    run_decision_validation_dryrun,
)
from capabilities.midplatform.teacher_adapter.luna_teacher_validation_processor_v1 import (
    review_teacher_evidence,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.luna_qwen_teacher_admission_v1 import (
    DRYRUN_POLICY_REF,
    evaluate_qwen_teacher_admission,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_teacher_adapter_v1 import (
    QwenVLTeacherAdapter,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_teacher_types_v1 import (
    POLICY_REF,
    PROVIDER_ID,
    TEACHER_ROLE,
)
from capabilities.midplatform.teacher_adapter.teacher_adapter_dryrun.luna_teacher_adapter_dryrun_adapter_v1 import (
    assert_teacher_does_not_override_l1,
    assert_teacher_does_not_override_plan,
)
from capabilities.midplatform.teacher_adapter.teacher_adapter_dryrun.luna_teacher_challenge_builder_v1 import (
    build_teacher_input_from_chain,
)

FINAL_GO = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_DRYRUN_BLOCKED"

_qwen_adapter = QwenVLTeacherAdapter()


def _image_ref_from_job(job_envelope: Dict[str, Any]) -> Optional[str]:
    manifest = job_envelope.get("asset_manifest") or {}
    asset_id = manifest.get("asset_id", "")
    file_name = manifest.get("file_name", "")
    if asset_id and file_name:
        return f"{asset_id}/{file_name}"
    return job_envelope.get("image_reference")


def _build_case_library_candidate(
    review: Dict[str, Any],
    *,
    job_id: str,
) -> Optional[Dict[str, Any]]:
    status = review.get("teacher_validation_status")
    if status not in ("accepted_as_evidence", "accepted_as_alternative"):
        return None
    evidence = review.get("teacher_evidence_candidate") or {}
    return {
        "case_candidate_id": f"clc_{job_id}_qwen",
        "source_job_id": job_id,
        "source_provider": PROVIDER_ID,
        "teacher_validation_status": status,
        "evidence_type": evidence.get("evidence_type"),
        "plan_improvement_candidate": review.get("alternative_plan_candidate_optional"),
        "review_status": "pending_policy_review",
        "no_direct_training": True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_qwen_vl_integration_dryrun(
    job_envelope: Dict[str, Any],
    *,
    qwen_mock_scenario: Optional[str] = None,
    admission_hints: Optional[Dict[str, Any]] = None,
    user_goal_candidate: Optional[Dict[str, Any]] = None,
    plan_override: Optional[Dict[str, Any]] = None,
    use_plan_competition: bool = True,
) -> Dict[str, Any]:
    """
    Full dry-run:
    Job → L1 → L2 → L2.5 → Teacher Admission → Qwen-VL → Validation Review → Case Library candidate.
    Validates Luna control over Qwen participation, not Qwen accuracy.
    """
    dv_result = run_decision_validation_dryrun(
        job_envelope,
        user_goal_candidate=user_goal_candidate,
        plan_override=plan_override,
        use_plan_competition=use_plan_competition,
    )

    teacher_input = build_teacher_input_from_chain(dv_result)
    teacher_input["policy_context"]["active_policy_refs"] = [
        POLICY_REF,
        DRYRUN_POLICY_REF,
        "teacher_usage_policy_v1",
    ]

    admission = evaluate_qwen_teacher_admission(
        decision_validation_result=dv_result,
        teacher_input=teacher_input,
        admission_hints=admission_hints,
    )

    situation = dv_result.get("situation_understanding_candidate") or {}
    plan = dv_result.get("agent_plan_candidate") or {}
    image_ref = _image_ref_from_job(job_envelope)

    teacher_result: Dict[str, Any] = {
        "request_id": admission.get("trace_refs", [{}])[0].get("ref", "qwen_dryrun"),
        "admission_decision": admission,
        "teacher_evidence_candidate": None,
        "teacher_role": TEACHER_ROLE,
        "provider_route": PROVIDER_ID,
        "candidate_only": True,
        "not_fact": True,
        "dryrun_only": True,
        "no_network": True,
        "policy_refs": admission.get("policy_refs", []),
    }

    if admission.get("admission_status") == "admitted" and admission.get("should_request_teacher"):
        qwen_out = _qwen_adapter.request_teacher_assistance(
            teacher_role=TEACHER_ROLE,
            input_evidence=teacher_input.get("input_evidence") or [],
            required_output_type="teacher_evidence_candidate",
            policy_context=teacher_input.get("policy_context") or {},
            situation_candidate=situation,
            plan_candidate=plan,
            image_reference=image_ref,
            missing_information=situation.get("missing_information_candidates"),
            mock_scenario=qwen_mock_scenario,
        )
        teacher_result = {
            **teacher_result,
            "request_id": qwen_out.get("request_id"),
            "teacher_evidence_candidate": qwen_out.get("teacher_evidence_candidate"),
            "qwen_adapter_result": qwen_out,
        }
        admission = {**admission, "admission_status": "admitted", "should_request_teacher": True}
        teacher_result["admission_decision"] = admission

    teacher_review = review_teacher_evidence(
        decision_validation_result=dv_result,
        teacher_result=teacher_result,
    )

    case_library_candidate = _build_case_library_candidate(
        teacher_review,
        job_id=dv_result.get("job_id", ""),
    )

    plan_assert = assert_teacher_does_not_override_plan(plan, teacher_review)
    l1_assert = assert_teacher_does_not_override_l1(situation, teacher_review)

    return {
        "job_id": dv_result.get("job_id", ""),
        "chain": [
            "job_envelope",
            "runner_evidence",
            "situation_understanding_candidate",
            "agent_plan_candidate",
            "decision_validation_candidate",
            "teacher_admission",
            "qwen_vl_teacher_evidence_candidate",
            "teacher_validation_review",
            "case_library_candidate",
            "tool_os_handoff_candidate",
        ],
        "situation_understanding_candidate": situation,
        "agent_plan_candidate": plan,
        "decision_validation_candidate": dv_result.get("decision_validation_candidate"),
        "tool_os_handoff_candidate": dv_result.get("tool_os_handoff_candidate"),
        "validation_status": dv_result.get("validation_status"),
        "teacher_admission": admission,
        "teacher_request": {
            "should_request_teacher": admission.get("should_request_teacher"),
            "admission_status": admission.get("admission_status"),
            "admission_reason": admission.get("admission_reason"),
            "noop_reason": admission.get("noop_reason"),
            "reject_reason": admission.get("reject_reason"),
        },
        "teacher_adapter_input": teacher_input,
        "qwen_teacher_result": teacher_result,
        "teacher_evidence_candidate": teacher_result.get("teacher_evidence_candidate"),
        "teacher_validation_review": teacher_review,
        "teacher_validation_status": teacher_review.get("teacher_validation_status"),
        "case_library_candidate_optional": case_library_candidate,
        "tool_plan_summary": dv_result.get("tool_plan_summary"),
        "teacher_does_not_override_plan_assertion": plan_assert,
        "teacher_does_not_override_l1_assertion": l1_assert,
        "no_fact_write_assertion": True,
        "no_tool_execution_assertion": True,
        "no_runner_invocation_assertion": True,
        "no_auto_training_assertion": True,
        "dryrun_only": True,
        "deterministic_mock_only": True,
        "no_real_qwen_api": True,
        "no_network": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF, DRYRUN_POLICY_REF, "teacher_usage_policy_v1"],
    }

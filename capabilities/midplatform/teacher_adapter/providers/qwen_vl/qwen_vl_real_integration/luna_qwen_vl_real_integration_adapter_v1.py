# -*- coding: utf-8 -*-
"""Qwen-VL Real Provider Integration — full-chain adapter v1."""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.midplatform.decision_validation.luna_decision_validation_dryrun_adapter_v1 import (
    run_decision_validation_dryrun,
)
from capabilities.midplatform.teacher_adapter.luna_teacher_validation_processor_v1 import (
    review_teacher_evidence,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.luna_qwen_teacher_admission_v1 import (
    evaluate_qwen_teacher_admission,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_real_provider_v1 import (
    invoke_qwen_vl_real_provider,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_teacher_types_v1 import (
    POLICY_REF,
    PROVIDER_ID,
    TEACHER_ROLE,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.teacher_usage_metrics_v1 import (
    get_teacher_usage_metrics,
)
from capabilities.midplatform.teacher_adapter.teacher_adapter_dryrun.luna_teacher_adapter_dryrun_adapter_v1 import (
    assert_teacher_does_not_override_l1,
    assert_teacher_does_not_override_plan,
)
from capabilities.midplatform.teacher_adapter.teacher_adapter_dryrun.luna_teacher_challenge_builder_v1 import (
    build_teacher_input_from_chain,
)

REAL_PROVIDER_POLICY_REF = "qwen_vl_real_provider_policy_v1"
FINAL_GO = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_BLOCKED"


def _image_ref_from_job(job_envelope: Dict[str, Any]) -> Optional[str]:
    manifest = job_envelope.get("asset_manifest") or {}
    asset_id = manifest.get("asset_id", "")
    file_name = manifest.get("file_name") or manifest.get("local_file_name", "")
    if asset_id and file_name:
        return f"{asset_id}/{file_name}"
    return job_envelope.get("image_reference")


def _build_case_library_candidate(review: Dict[str, Any], *, job_id: str) -> Optional[Dict[str, Any]]:
    status = review.get("teacher_validation_status")
    if status not in ("accepted_as_evidence", "accepted_as_alternative"):
        return None
    evidence = review.get("teacher_evidence_candidate") or {}
    return {
        "case_candidate_id": f"clc_{job_id}_qwen_real",
        "source_job_id": job_id,
        "source_provider": PROVIDER_ID,
        "teacher_validation_status": status,
        "evidence_type": evidence.get("evidence_type"),
        "review_status": "pending_policy_review",
        "no_direct_training": True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_qwen_vl_real_provider_integration(
    job_envelope: Dict[str, Any],
    *,
    recorded_fixture_id: Optional[str] = None,
    admission_hints: Optional[Dict[str, Any]] = None,
    case_id: Optional[str] = None,
    user_goal_candidate: Optional[Dict[str, Any]] = None,
    plan_override: Optional[Dict[str, Any]] = None,
    use_plan_competition: bool = True,
) -> Dict[str, Any]:
    """
    Job → L1 → L2 → L2.5 → Admission → Qwen API → Raw Response → Normalize → Validation.
    """
    metrics = get_teacher_usage_metrics()
    dv_result = run_decision_validation_dryrun(
        job_envelope,
        user_goal_candidate=user_goal_candidate,
        plan_override=plan_override,
        use_plan_competition=use_plan_competition,
    )

    teacher_input = build_teacher_input_from_chain(dv_result)
    teacher_input["policy_context"]["active_policy_refs"] = [
        POLICY_REF,
        REAL_PROVIDER_POLICY_REF,
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
        "admission_decision": admission,
        "teacher_evidence_candidate": None,
        "raw_teacher_response": None,
        "parsed_teacher_response": None,
        "teacher_role": TEACHER_ROLE,
        "provider_route": PROVIDER_ID,
        "candidate_only": True,
        "not_fact": True,
    }

    if admission.get("admission_status") == "admitted" and admission.get("should_request_teacher"):
        provider_out = invoke_qwen_vl_real_provider(
            situation_candidate=situation,
            plan_candidate=plan,
            job_envelope=job_envelope,
            image_ref=image_ref,
            recorded_fixture_id=recorded_fixture_id,
        )
        teacher_result = {
            **teacher_result,
            "teacher_request_built": provider_out.get("teacher_request"),
            "raw_teacher_response": provider_out.get("raw_teacher_response"),
            "parsed_teacher_response": provider_out.get("parsed_teacher_response"),
            "teacher_evidence_candidate": provider_out.get("teacher_evidence_candidate"),
            "provider_pipeline": provider_out,
            "raw_separated_from_evidence": provider_out.get("raw_separated_from_evidence"),
            "live_call": provider_out.get("live_call"),
        }
    else:
        metrics.record_noop(
            case_id=case_id or dv_result.get("job_id", "unknown"),
            reason=admission.get("noop_reason", "noop"),
        )

    teacher_review = review_teacher_evidence(
        decision_validation_result=dv_result,
        teacher_result=teacher_result,
    )

    if teacher_result.get("raw_teacher_response"):
        metrics.record_admitted(
            case_id=case_id or dv_result.get("job_id", "unknown"),
            raw_envelope=teacher_result["raw_teacher_response"],
            validation_status=teacher_review.get("teacher_validation_status", ""),
        )

    case_library_candidate = _build_case_library_candidate(
        teacher_review,
        job_id=dv_result.get("job_id", ""),
    )

    plan_assert = assert_teacher_does_not_override_plan(plan, teacher_review)
    l1_assert = assert_teacher_does_not_override_l1(situation, teacher_review)

    return {
        "job_id": dv_result.get("job_id", ""),
        "case_id": case_id,
        "chain": [
            "job_envelope",
            "situation_understanding_candidate",
            "agent_plan_candidate",
            "decision_validation_candidate",
            "teacher_admission",
            "qwen_vl_api",
            "raw_teacher_response",
            "evidence_normalization",
            "teacher_validation_review",
            "case_library_candidate",
        ],
        "situation_understanding_candidate": situation,
        "agent_plan_candidate": plan,
        "decision_validation_candidate": dv_result.get("decision_validation_candidate"),
        "validation_status": dv_result.get("validation_status"),
        "teacher_admission": admission,
        "teacher_request": {
            "should_request_teacher": admission.get("should_request_teacher"),
            "admission_status": admission.get("admission_status"),
            "admission_reason": admission.get("admission_reason"),
            "noop_reason": admission.get("noop_reason"),
        },
        "raw_teacher_response": teacher_result.get("raw_teacher_response"),
        "parsed_teacher_response": teacher_result.get("parsed_teacher_response"),
        "teacher_evidence_candidate": teacher_result.get("teacher_evidence_candidate"),
        "raw_separated_from_evidence": teacher_result.get("raw_separated_from_evidence", True),
        "teacher_validation_review": teacher_review,
        "teacher_validation_status": teacher_review.get("teacher_validation_status"),
        "case_library_candidate_optional": case_library_candidate,
        "teacher_usage_metrics": metrics.to_dict(),
        "teacher_does_not_override_plan_assertion": plan_assert,
        "teacher_does_not_override_l1_assertion": l1_assert,
        "no_fact_write_assertion": True,
        "no_tool_execution_assertion": True,
        "no_runner_invocation_assertion": True,
        "no_auto_training_assertion": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF, REAL_PROVIDER_POLICY_REF, "teacher_usage_policy_v1"],
    }

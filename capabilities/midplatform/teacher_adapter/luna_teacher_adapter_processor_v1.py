# -*- coding: utf-8
"""Luna Teacher Adapter — deterministic processor stub v1 (planning only)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.teacher_adapter.luna_teacher_adapter_types_v1 import POLICY_REF
from capabilities.midplatform.teacher_adapter.providers import PROVIDER_REGISTRY

FORBIDDEN_TEACHER_SUGGESTIONS = (
    "slam_for_text",
    "vlm_for_shopfront_text_when_ocr_available",
    "override_selected_plan",
    "write_fact_directly",
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _situation(input_data: Dict[str, Any]) -> Dict[str, Any]:
    return input_data.get("situation_understanding_candidate") or {}


def _scene_type(situation: Dict[str, Any]) -> str:
    return (situation.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")


def _missing_types(situation: Dict[str, Any]) -> List[str]:
    return [m.get("info_type", "") for m in situation.get("missing_information_candidates", [])]


def _uncertainty_high(situation: Dict[str, Any]) -> bool:
    unc = situation.get("uncertainty") or {}
    scene_conf = float((situation.get("scene_profile_candidate") or {}).get("confidence") or 1.0)
    return bool(
        unc.get("needs_manual_review")
        or unc.get("needs_user_goal")
        or scene_conf < 0.5
        or _scene_type(situation) == "unknown_scene"
    )


def _cap_available(input_data: Dict[str, Any], cap: str) -> bool:
    for c in input_data.get("available_capabilities") or []:
        if c.get("capability_type") == cap:
            return c.get("availability", "available") != "unavailable"
    return False


def _teacher_payload_conflict(payload: Dict[str, Any]) -> Optional[str]:
    """Detect policy conflicts in teacher stub payloads (e.g. SLAM for text)."""
    planning = payload.get("planning_output") or {}
    alt = planning.get("alternative_plan_candidate") or {}
    tools = alt.get("tools_suggested") or []
    summary = (alt.get("suggested_steps_summary") or "").lower()
    if "slam" in tools and ("text" in summary or "ocr" in summary or "文字" in summary):
        return "slam_for_text"
    if payload.get("teacher_suggests") == "slam_for_text":
        return "slam_for_text"
    if payload.get("override_selected_plan"):
        return "override_selected_plan"
    return None


def evaluate_teacher_admission(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Teacher Admission Policy — deterministic planning stub."""
    situation = _situation(input_data)
    scene = _scene_type(situation)
    missing = _missing_types(situation)
    task_type = input_data.get("task_type", "scene_hypothesis")
    required_output = input_data.get("required_output_type", "teacher_evidence_candidate")
    agent_plan = input_data.get("agent_plan_candidate_optional")
    teacher_role = "perception_teacher"
    preferred_provider = "gemini"

    # Explicit bad teacher request (Case D)
    for ev in input_data.get("input_evidence") or []:
        if ev.get("teacher_suggests") in FORBIDDEN_TEACHER_SUGGESTIONS:
            return {
                "should_request_teacher": False,
                "admission_status": "rejected",
                "teacher_role": teacher_role,
                "preferred_provider": preferred_provider,
                "noop_reason": "",
                "reject_reason": f"policy_conflict_{ev.get('teacher_suggests')}",
                "candidate_only": True,
                "not_fact": True,
                "policy_refs": [POLICY_REF, "bad_teacher_tool_conflict_reject"],
                "trace_refs": [{"stage": "teacher_admission_reject", "reason": ev.get("teacher_suggests")}],
            }

    # Learning teacher (Case E) — explicit task type takes priority
    if task_type == "learning_case" or required_output == "learning_candidate":
        return {
            "should_request_teacher": True,
            "admission_status": "admitted",
            "teacher_role": "learning_teacher",
            "preferred_provider": "internvl",
            "noop_reason": "",
            "reject_reason": "",
            "candidate_only": True,
            "not_fact": True,
            "policy_refs": [POLICY_REF, "learning_requires_policy_review"],
            "trace_refs": [{"stage": "teacher_admission_learning"}],
        }

    # Planning alternative (Case C)
    if task_type == "alternative_plan" or required_output == "alternative_plan_candidate":
        teacher_role = "planning_teacher"
        preferred_provider = "gpt_vision"
        if agent_plan:
            return {
                "should_request_teacher": True,
                "admission_status": "admitted",
                "teacher_role": teacher_role,
                "preferred_provider": preferred_provider,
                "noop_reason": "",
                "reject_reason": "",
                "candidate_only": True,
                "not_fact": True,
                "policy_refs": [POLICY_REF, "alternative_plan_only"],
                "trace_refs": [{"stage": "teacher_admission_planning", "agent_plan_id": agent_plan.get("plan_id")}],
            }

    # Case A: shopfront + text_content + OCR available → noop
    if (
        scene == "shopfront_sign"
        and "text_content" in missing
        and _cap_available(input_data, "ocr")
        and task_type in ("scene_hypothesis", "visual_evidence", "uncertainty_reduction")
    ):
        return {
            "should_request_teacher": False,
            "admission_status": "noop",
            "teacher_role": "perception_teacher",
            "preferred_provider": preferred_provider,
            "noop_reason": "OCR preferred over VLM for text_content; specialized tool available",
            "reject_reason": "",
            "candidate_only": True,
            "not_fact": True,
            "policy_refs": [POLICY_REF, "shopfront_text_ocr_no_vlm", "specialized_tool_preferred_over_vlm"],
            "trace_refs": [{"stage": "teacher_admission_noop", "scene": scene, "missing": missing}],
        }

    # Case B: unknown_scene + high uncertainty → admit perception teacher
    if scene == "unknown_scene" and _uncertainty_high(situation) and missing:
        return {
            "should_request_teacher": True,
            "admission_status": "admitted",
            "teacher_role": "perception_teacher",
            "preferred_provider": preferred_provider,
            "noop_reason": "",
            "reject_reason": "",
            "candidate_only": True,
            "not_fact": True,
            "policy_refs": [POLICY_REF, "unknown_scene_high_uncertainty_allows_vlm"],
            "trace_refs": [{"stage": "teacher_admission_admit", "scene": scene}],
        }

    # OCR unavailable fallback → VLM advisor allowed
    if "text_content" in missing and not _cap_available(input_data, "ocr"):
        return {
            "should_request_teacher": True,
            "admission_status": "admitted",
            "teacher_role": "perception_teacher",
            "preferred_provider": preferred_provider,
            "noop_reason": "",
            "reject_reason": "",
            "candidate_only": True,
            "not_fact": True,
            "policy_refs": [POLICY_REF],
            "trace_refs": [{"stage": "teacher_admission_ocr_unavailable_fallback"}],
        }

    return {
        "should_request_teacher": False,
        "admission_status": "noop",
        "teacher_role": teacher_role,
        "preferred_provider": preferred_provider,
        "noop_reason": "no_teacher_admission_trigger_matched",
        "reject_reason": "",
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF],
        "trace_refs": [{"stage": "teacher_admission_default_noop"}],
    }


def route_teacher_provider(
    provider_id: str,
    *,
    teacher_role: str,
    task_type: str,
    input_evidence: List[Dict[str, Any]],
    situation: Dict[str, Any],
    agent_plan: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    fn = PROVIDER_REGISTRY.get(provider_id)
    if not fn:
        return {
            "provider_id": "teacher_stub",
            "teacher_role": teacher_role,
            "stub_only": True,
            "no_network": True,
            "candidate_only": True,
            "not_fact": True,
        }
    return fn(
        teacher_role=teacher_role,
        task_type=task_type,
        input_evidence=input_evidence,
        situation=situation,
        agent_plan=agent_plan,
    )


def build_teacher_evidence_candidate(
    input_data: Dict[str, Any],
    admission: Dict[str, Any],
    provider_payload: Dict[str, Any],
) -> Dict[str, Any]:
    eid = _uid("tec")
    role = admission.get("teacher_role", "perception_teacher")
    output_type = {
        "perception_teacher": "scene_hypothesis_candidate",
        "planning_teacher": "alternative_plan_candidate",
        "learning_teacher": "learning_candidate",
    }.get(role, "teacher_evidence_candidate")

    return {
        "evidence_id": eid,
        "teacher_role": role,
        "provider_id": provider_payload.get("provider_id", admission.get("preferred_provider")),
        "task_type": input_data.get("task_type", "scene_hypothesis"),
        "output_type": output_type,
        "perception_output_optional": provider_payload.get("perception_output"),
        "planning_output_optional": provider_payload.get("planning_output"),
        "learning_output_optional": provider_payload.get("learning_output"),
        "confidence": float(provider_payload.get("confidence") or 0.5),
        "candidate_only": True,
        "not_fact": True,
        "requires_policy_review": True,
        "does_not_override_l1_scene": True,
        "does_not_override_l2_selected_plan": True,
        "no_runner_invocation": True,
        "no_fact_write": True,
        "trace_refs": [
            {"stage": "teacher_evidence_candidate", "ref": eid},
            {"stage": "admission", "status": admission.get("admission_status")},
        ],
        "policy_refs": admission.get("policy_refs", [POLICY_REF]),
    }


def request_teacher_assistance(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Unified Teacher Adapter interface — planning stub only."""
    admission = evaluate_teacher_admission(input_data)
    status = admission.get("admission_status")

    result: Dict[str, Any] = {
        "request_id": _uid("tar"),
        "admission_decision": admission,
        "teacher_evidence_candidate": None,
        "teacher_role": admission.get("teacher_role"),
        "provider_route": admission.get("preferred_provider"),
        "candidate_only": True,
        "not_fact": True,
        "planning_only": True,
        "no_network": True,
        "no_runner_invocation": True,
        "no_fact_write": True,
        "policy_refs": admission.get("policy_refs", [POLICY_REF]),
    }

    if status != "admitted":
        return result

    situation = _situation(input_data)
    agent_plan = input_data.get("agent_plan_candidate_optional")
    provider_payload = route_teacher_provider(
        admission.get("preferred_provider", "gemini"),
        teacher_role=admission.get("teacher_role", "perception_teacher"),
        task_type=input_data.get("task_type", "scene_hypothesis"),
        input_evidence=input_data.get("input_evidence") or [],
        situation=situation,
        agent_plan=agent_plan,
    )

    conflict = _teacher_payload_conflict(provider_payload)
    if conflict:
        result["admission_decision"] = {
            **admission,
            "should_request_teacher": False,
            "admission_status": "rejected",
            "reject_reason": f"policy_conflict_{conflict}",
            "trace_refs": admission.get("trace_refs", []) + [{"stage": "post_provider_reject", "conflict": conflict}],
        }
        result["teacher_evidence_candidate"] = None
        return result

    evidence = build_teacher_evidence_candidate(input_data, admission, provider_payload)
    result["teacher_evidence_candidate"] = evidence
    result["provider_payload_stub"] = provider_payload
    return result


def build_learning_chain_from_teacher(
    teacher_result: Dict[str, Any],
) -> Dict[str, Any]:
    """Bridge to network_assisted_learning — returns learning_candidate envelope."""
    evidence = teacher_result.get("teacher_evidence_candidate") or {}
    learning_out = evidence.get("learning_output_optional") or {}
    lc_id = _uid("slc")
    return {
        "learning_candidate_id": lc_id,
        "source_type": "teacher_model",
        "source_ref": evidence.get("evidence_id"),
        "provenance_ref": teacher_result.get("request_id"),
        "review_status": learning_out.get("review_status", "pending_policy_review"),
        "evidence_summary": learning_out.get("learning_summary", ""),
        "candidate_only": True,
        "not_fact": True,
        "no_direct_training": True,
        "policy_refs": [POLICY_REF, "learning_requires_policy_review"],
        "trace_refs": [{"stage": "learning_teacher_chain", "ref": lc_id}],
    }

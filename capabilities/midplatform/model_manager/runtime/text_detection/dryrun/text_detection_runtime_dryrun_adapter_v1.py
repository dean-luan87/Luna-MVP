# -*- coding: utf-8 -*-
"""Text Detection Runtime DryRun Adapter — full governance loop v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.text_detection.dryrun.text_detection_collaboration_adapter_v1 import (
    build_capability_match_record,
    decide_collaboration_next_slot,
)
from capabilities.midplatform.model_manager.runtime.text_detection.dryrun.text_detection_evidence_builder_v1 import (
    assert_no_recognized_text,
    build_text_detection_evidence,
)
from capabilities.midplatform.model_manager.runtime.text_detection.dryrun.text_detection_execution_simulator_v1 import (
    simulate_text_detection_execution,
)
from capabilities.midplatform.model_manager.runtime.text_detection.dryrun.text_detection_runtime_metrics_v1 import (
    get_runtime_usage_metrics,
    record_handoff,
    record_slot_noop,
    record_slot_selected,
    reset_runtime_metrics,
)
from capabilities.midplatform.model_manager.runtime.text_detection.text_detection_request_builder_v1 import (
    build_text_detection_request,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_DRYRUN_BLOCKED"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _situation(scene: str, missing: Optional[list] = None) -> Dict[str, Any]:
    return {
        "situation_id": _uid("sit"),
        "scene_profile_candidate": {"scene_type": scene},
        "missing_information_candidates": [{"info_type": m} for m in (missing or ["text_content"])],
        "candidate_only": True,
    }


def _plan(goal: str = "identify_place") -> Dict[str, Any]:
    return {
        "plan_id": _uid("plan"),
        "plan_goal_candidate": {"goal_type": goal},
        "collaboration_plan": {"slot_1": "text_detection"},
        "candidate_only": True,
    }


def _validation_review(evidence: Dict[str, Any], collaboration: Dict[str, Any]) -> Dict[str, Any]:
    etype = evidence.get("evidence_type", "")
    if collaboration.get("validation_status") == "needs_review":
        status = "needs_review"
    elif etype == "runtime_error_candidate":
        status = "runtime_error_acknowledged"
    elif etype == "no_text_candidate":
        status = "no_text_acknowledged"
    elif etype == "low_confidence_text_candidate":
        status = "needs_review"
    else:
        status = "accepted_as_region_candidate"
    return {
        "validation_id": _uid("val"),
        "validation_status": status,
        "not_fact_admission": True,
        "candidate_only": True,
    }


def run_text_detection_governance_dryrun(
    *,
    fixture_key: str,
    scenario: str,
    situation: Dict[str, Any],
    plan: Dict[str, Any],
) -> Dict[str, Any]:
    """Full L1 → L2 → Slot → MM Match → Runtime → Evidence → Collaboration → Validation."""
    record_slot_selected()
    capability_match = build_capability_match_record(situation=situation, plan=plan)
    request = build_text_detection_request(situation=situation, plan=plan)
    execution = simulate_text_detection_execution(
        fixture_key=fixture_key,
        request_id=request.get("request_id"),
    )
    evidence = build_text_detection_evidence(execution=execution, scenario=scenario)
    collaboration = decide_collaboration_next_slot(evidence=evidence, plan=plan, situation=situation)
    validation = _validation_review(evidence, collaboration)

    handoff_ok = collaboration.get("next_slot_candidate") is not None
    quality = (evidence.get("confidence") or 0.0) if evidence.get("regions") else 0.0
    record_handoff(success=handoff_ok, evidence_quality=quality)

    return {
        "l1_situation": situation,
        "l2_plan": plan,
        "capability_match": capability_match,
        "collaboration_slot": {"slot_id": "slot_1", "capability": "text_detection"},
        "runtime_request": request,
        "runtime_execution": execution,
        "evidence_package": evidence,
        "collaboration_next_slot": collaboration,
        "validation_review": validation,
        "governance_loop_complete": True,
        "detector_did_not_decide_next": collaboration.get("detector_did_not_decide") is True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_case_a_shopfront_dryrun() -> Dict[str, Any]:
    """Case A: shopfront — region only, no text, next_slot OCR."""
    reset_runtime_metrics()
    situation = _situation("shopfront_sign")
    plan = _plan("identify_place")
    result = run_text_detection_governance_dryrun(
        fixture_key="shopfront_sign",
        scenario="shopfront",
        situation=situation,
        plan=plan,
    )
    evidence = result.get("evidence_package") or {}
    collab = result.get("collaboration_next_slot") or {}
    return {
        "case": "case_a_shopfront_text_region_dryrun",
        **result,
        "evidence_type_correct": evidence.get("evidence_type") == "text_region_candidate",
        "no_recognized_text": assert_no_recognized_text(evidence),
        "has_region_type": evidence.get("region_type") == "text_region_candidate",
        "next_slot_ocr": (collab.get("next_slot_candidate") or {}).get("capability") == "text_recognition",
        "forbidden_text_absent": "text" not in str(evidence.get("regions") or []),
        "runtime_metrics": get_runtime_usage_metrics(),
    }


def run_case_b_subway_dryrun() -> Dict[str, Any]:
    """Case B: subway — direction_text_region_candidate, not station fact."""
    reset_runtime_metrics()
    situation = _situation("subway_platform")
    plan = _plan("identify_place")
    result = run_text_detection_governance_dryrun(
        fixture_key="subway_platform",
        scenario="metro_direction",
        situation=situation,
        plan=plan,
    )
    evidence = result.get("evidence_package") or {}
    return {
        "case": "case_b_subway_direction_dryrun",
        **result,
        "direction_region": evidence.get("evidence_type") == "direction_text_region_candidate",
        "not_station_fact": evidence.get("not_output") == "station_name_fact",
        "ocr_worthwhile": (result.get("collaboration_next_slot") or {}).get("next_slot_candidate") is not None,
        "runtime_metrics": get_runtime_usage_metrics(),
    }


def run_case_c_no_text_dryrun() -> Dict[str, Any]:
    """Case C: corridor — no_text, no forced OCR even with understand_environment goal."""
    reset_runtime_metrics()
    situation = _situation("corridor", missing=["scene_identity"])
    plan = _plan("understand_environment")
    result = run_text_detection_governance_dryrun(
        fixture_key="corridor_no_text",
        scenario="shopfront",
        situation=situation,
        plan=plan,
    )
    evidence = result.get("evidence_package") or {}
    collab = result.get("collaboration_next_slot") or {}
    record_slot_noop()
    return {
        "case": "case_c_no_text_environment_dryrun",
        **result,
        "no_text_candidate": evidence.get("evidence_type") == "no_text_candidate",
        "no_forced_ocr": collab.get("no_forced_ocr") is True,
        "next_slot_none": collab.get("next_slot_candidate") is None,
        "runtime_metrics": get_runtime_usage_metrics(),
    }


def run_case_d_low_confidence_dryrun() -> Dict[str, Any]:
    """Case D: ad texture — needs_review, no direct OCR."""
    reset_runtime_metrics()
    situation = _situation("shopfront_sign")
    plan = _plan("identify_place")
    result = run_text_detection_governance_dryrun(
        fixture_key="ad_texture_low_conf",
        scenario="shopfront",
        situation=situation,
        plan=plan,
    )
    evidence = result.get("evidence_package") or {}
    collab = result.get("collaboration_next_slot") or {}
    validation = result.get("validation_review") or {}
    return {
        "case": "case_d_false_detection_dryrun",
        **result,
        "low_confidence": evidence.get("evidence_type") == "low_confidence_text_candidate",
        "needs_review": validation.get("validation_status") == "needs_review",
        "not_direct_ocr": collab.get("not_direct_ocr") is True,
        "next_slot_none": collab.get("next_slot_candidate") is None,
        "runtime_metrics": get_runtime_usage_metrics(),
    }


def run_case_e_runtime_failure_dryrun() -> Dict[str, Any]:
    """Case E: runtime unavailable — replan, no silent Qwen/SAM."""
    reset_runtime_metrics()
    situation = _situation("shopfront_sign")
    plan = _plan("identify_place")
    result = run_text_detection_governance_dryrun(
        fixture_key="runtime_unavailable",
        scenario="shopfront",
        situation=situation,
        plan=plan,
    )
    evidence = result.get("evidence_package") or {}
    collab = result.get("collaboration_next_slot") or {}
    return {
        "case": "case_e_runtime_failure_dryrun",
        **result,
        "runtime_error": evidence.get("evidence_type") == "runtime_error_candidate",
        "l2_replan": collab.get("l2_replan_candidate") is True,
        "not_silent_qwen": collab.get("not_silent_fallback_qwen") is True,
        "not_silent_sam": collab.get("not_silent_fallback_sam") is True,
        "runtime_metrics": get_runtime_usage_metrics(),
    }

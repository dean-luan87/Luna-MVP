# -*- coding: utf-8 -*-
"""Real Chain Orchestrator — Slot → Fill → Runtime → Fusion → Validation v1 (planning)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.collaboration.real_chain.evidence_fusion_adapter_v1 import (
    build_chain_fusion_candidate,
    build_evidence_package,
    build_fact_admission_candidate,
)
from capabilities.midplatform.model_manager.collaboration.real_chain.slot_provider_binding_v1 import (
    bind_slot_providers,
    get_shopfront_chain_slots,
    validate_slot_bindings,
)

CHAIN_ID = "shopfront_text_detection_ocr_qwen_context_v1"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _mock_detector_output() -> Dict[str, Any]:
    return {"regions": [{"bbox": [120, 80, 340, 160], "label": "text_region"}], "summary": "检测到招牌文字区域"}


def _mock_ocr_output(text: str = "阿叔阿姨的店") -> Dict[str, Any]:
    return {"text": text, "confidence": 0.92, "summary": text}


def _mock_qwen_context(ocr_text: str) -> Dict[str, Any]:
    return {
        "interpretation": f"该文字「{ocr_text}」可能对应店铺招牌区域",
        "summary": "上下文解释：招牌文字区域",
        "not_ocr": True,
    }


def build_execution_trace(
    *,
    bound_slots: List[Dict[str, Any]],
    slot_statuses: Dict[str, str],
) -> Dict[str, Any]:
    executions = []
    for slot in bound_slots:
        sid = slot.get("slot_id", "")
        executions.append({
            "slot_id": sid,
            "capability": slot.get("capability"),
            "provider_id": slot.get("filled_provider_id"),
            "output_type": slot.get("output_type"),
            "status": slot_statuses.get(sid, "pending"),
            "depends_on": slot.get("depends_on", []),
        })
    return {
        "trace_id": _uid("tr"),
        "chain_id": CHAIN_ID,
        "goal_type": "identify_place",
        "scene_type": "shopfront_sign",
        "slot_executions": executions,
        "candidate_only": True,
        "not_fact": True,
    }


def run_normal_shopfront_chain() -> Dict[str, Any]:
    """Case A: Detector + OCR + Qwen context — full chain."""
    slots = get_shopfront_chain_slots()
    bound = bind_slot_providers(slots)
    binding_check = validate_slot_bindings(bound)

    detector_pkg = build_evidence_package(
        slot_id="slot_1", provider_id="detection_v1",
        evidence_type="text_region_candidate", payload=_mock_detector_output(),
    )
    ocr_pkg = build_evidence_package(
        slot_id="slot_2", provider_id="ocr_v1",
        evidence_type="ocr_text_candidate", payload=_mock_ocr_output(),
    )
    qwen_pkg = build_evidence_package(
        slot_id="slot_3", provider_id="qwen_vl",
        evidence_type="context_evidence_candidate",
        payload=_mock_qwen_context("阿叔阿姨的店"),
    )
    packages = [detector_pkg, ocr_pkg, qwen_pkg]
    fusion = build_chain_fusion_candidate(evidence_packages=packages)
    validation = {
        "review_id": _uid("vr"),
        "validation_status": "accepted_as_evidence_collection",
        "not_fact_admission": False,
        "fact_admission_candidate": True,
        "candidate_only": True,
    }
    trace = build_execution_trace(
        bound_slots=bound,
        slot_statuses={"slot_1": "completed", "slot_2": "completed", "slot_3": "completed"},
    )

    return {
        "scenario": "case_a_normal_shopfront_chain",
        "bound_slots": bound,
        "binding_check": binding_check,
        "execution_trace": trace,
        "evidence_packages": packages,
        "fusion_candidate": fusion,
        "validation_review": validation,
        "all_slots_completed": True,
        "qwen_not_ocr": True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_ocr_failure_chain() -> Dict[str, Any]:
    """Case B: OCR failure → failure evidence → challenge → request_more_evidence."""
    slots = get_shopfront_chain_slots()
    bound = bind_slot_providers(slots)

    detector_pkg = build_evidence_package(
        slot_id="slot_1", provider_id="detection_v1",
        evidence_type="text_region_candidate", payload=_mock_detector_output(),
    )
    ocr_failure = build_evidence_package(
        slot_id="slot_2", provider_id="ocr_v1",
        evidence_type="ocr_failure_candidate",
        payload={"failure_reason": "text_blurry", "confidence": 0.12, "summary": "文字模糊无法识别"},
        status="failed",
    )
    challenge = {
        "challenge_id": _uid("ch"),
        "trigger": "ocr_failure",
        "qwen_challenge_candidate": {
            "hypothesis": "可能不是店招，而是活动海报",
            "evidence_type": "alternative_hypothesis_candidate",
            "not_ocr_substitute": True,
            "not_guessing_text": True,
        },
        "override_plan": False,
        "candidate_only": True,
    }
    validation = {
        "review_id": _uid("vr"),
        "validation_status": "request_more_evidence",
        "ocr_failure_acknowledged": True,
        "not_auto_qwen_ocr": True,
        "l2_replan_candidate": True,
        "candidate_only": True,
    }

    return {
        "scenario": "case_b_ocr_failure_challenge",
        "bound_slots": bound,
        "detector_package": detector_pkg,
        "ocr_failure_candidate": ocr_failure,
        "qwen_challenge": challenge,
        "validation_review": validation,
        "not_auto_model_replacement": True,
        "no_qwen_text_guess": challenge.get("qwen_challenge_candidate", {}).get("not_guessing_text") is True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_qwen_unsupported_claim_chain() -> Dict[str, Any]:
    """Case C: Qwen Starbucks claim without OCR evidence → reject."""
    ocr_pkg = build_evidence_package(
        slot_id="slot_2", provider_id="ocr_v1",
        evidence_type="ocr_text_candidate",
        payload={"text": "阿叔阿姨的店", "confidence": 0.90, "summary": "阿叔阿姨的店"},
    )
    qwen_claim = {
        "provider_id": "qwen_vl",
        "claimed_brand": "Starbucks",
        "claimed_text": "这是星巴克",
        "evidence_type": "context_evidence_candidate",
    }
    unsupported = {
        "check_id": _uid("uc"),
        "has_unsupported_claim": True,
        "claim": "Starbucks",
        "ocr_evidence": "阿叔阿姨的店",
        "ocr_contains_claim": False,
        "unsupported_claim": True,
        "teacher_does_not_override_ocr": True,
    }
    validation = {
        "review_id": _uid("vr"),
        "validation_status": "rejected_by_policy",
        "rejection_reason": "unsupported_claim",
        "not_fact_admission": True,
        "candidate_only": True,
    }

    return {
        "scenario": "case_c_qwen_unsupported_claim_reject",
        "ocr_package": ocr_pkg,
        "qwen_claim": qwen_claim,
        "unsupported_claim_check": unsupported,
        "validation_review": validation,
        "rejected": validation.get("validation_status") == "rejected_by_policy",
        "teacher_not_fact_owner": True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_detector_unavailable_degradation() -> Dict[str, Any]:
    """Case D: Detector unavailable → collaboration_degradation → replan."""
    slots = get_shopfront_chain_slots()
    bound = bind_slot_providers(slots)

    degradation = {
        "degradation_id": _uid("cdg"),
        "resource_constraint": "detection_v1_unavailable",
        "original_chain": CHAIN_ID,
        "lost_capability": ["text_detection"],
        "collaboration_degradation_candidate": True,
        "not_silent_degradation": True,
        "suggested_action": "l2_replanning_candidate",
        "candidate_only": True,
    }
    replan = {
        "replan_id": _uid("rpc"),
        "trigger": "collaboration_degradation",
        "suggested_actions": [
            {"action": "retry_with_alternative_detector"},
            {"action": "request_user_closer_image"},
            {"action": "defer_identify_place"},
        ],
        "owned_by": "L2_Agent_Planning",
        "candidate_only": True,
    }

    return {
        "scenario": "case_d_detector_unavailable_degradation",
        "bound_slots": bound,
        "collaboration_degradation": degradation,
        "l2_replan_candidate": replan,
        "lost_capability_recorded": "text_detection" in (degradation.get("lost_capability") or []),
        "not_silent": degradation.get("not_silent_degradation") is True,
        "candidate_only": True,
        "not_fact": True,
    }

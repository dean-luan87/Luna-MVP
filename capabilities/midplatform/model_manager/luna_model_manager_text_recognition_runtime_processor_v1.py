# -*- coding: utf-8 -*-
"""Luna Model Manager OCR Recognition Runtime — planning processor v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.mixed_region.mixed_region_understanding_adapter_v1 import (
    run_mixed_region_understanding,
)
from capabilities.midplatform.model_manager.runtime.text_recognition.text_recognition_runtime_adapter_v1 import (
    run_text_recognition_slot,
)
from capabilities.midplatform.model_manager.runtime.text_recognition.text_recognition_runtime_metrics_v1 import (
    reset_ocr_runtime_metrics,
)


def _situation(scene_type: str) -> Dict[str, Any]:
    return {
        "scene_profile_candidate": {"scene_type": scene_type},
        "candidate_only": True,
    }


def _plan(goal: str = "identify_place") -> Dict[str, Any]:
    return {
        "plan_goal_candidate": {"goal_type": goal},
        "collaboration_plan": {
            "slot_1": "text_detection",
            "slot_2a": "text_recognition",
            "slot_2b": "visual_understanding",
            "slot_3": "evidence_fusion",
        },
        "candidate_only": True,
    }


def _text_region(region_id: str = "region_001", bbox: list | None = None) -> Dict[str, Any]:
    return {
        "evidence_id": "ev_region_upstream",
        "evidence_type": "text_region_candidate",
        "regions": [{"region_id": region_id, "bbox": bbox or [120, 80, 340, 160], "confidence": 0.91}],
        "region_ids": [region_id],
        "candidate_only": True,
    }


def _direction_region(region_id: str = "region_001") -> Dict[str, Any]:
    return {
        "evidence_id": "ev_direction_upstream",
        "evidence_type": "direction_text_region_candidate",
        "regions": [{"region_id": region_id, "bbox": [50, 200, 400, 260], "confidence": 0.88}],
        "region_ids": [region_id],
        "candidate_only": True,
    }


def run_shopfront_ocr() -> Dict[str, Any]:
    """Case A: 店招 — ocr_text_candidate + fusion identify_place_candidate."""
    reset_ocr_runtime_metrics()
    situation = _situation("shopfront_sign")
    plan = _plan("identify_place")
    result = run_text_recognition_slot(
        situation=situation,
        plan=plan,
        text_region_evidence=_text_region(),
        fixture_key="shopfront_ashu",
        scenario="shopfront",
    )
    evidence = result.get("evidence_package") or {}
    fusion = result.get("fusion_candidate") or {}
    return {
        **result,
        "scenario": "case_a_shopfront_ocr_text_candidate",
        "ocr_text_candidate": evidence.get("evidence_type") == "ocr_text_candidate",
        "candidate_text_correct": evidence.get("candidate_text") == "阿叔阿姨的店",
        "source_region_bound": evidence.get("source_region_id") == "region_001",
        "not_location_fact": evidence.get("not_location_fact") is True,
        "fusion_identify_place": fusion.get("fusion_type") == "identify_place_candidate",
        "not_fact_admission": fusion.get("not_fact_admission") is True,
    }


def run_metro_direction_ocr() -> Dict[str, Any]:
    """Case B: 地铁导视 — ocr_text_candidate, find_direction ok, not current_station."""
    reset_ocr_runtime_metrics()
    situation = _situation("subway_platform")
    plan = _plan("identify_place")
    result = run_text_recognition_slot(
        situation=situation,
        plan=plan,
        text_region_evidence=_direction_region(),
        fixture_key="metro_jiahui_direction",
        scenario="metro_direction",
    )
    evidence = result.get("evidence_package") or {}
    return {
        **result,
        "scenario": "case_b_metro_direction_ocr",
        "ocr_text_candidate": evidence.get("evidence_type") == "ocr_text_candidate",
        "direction_text": "嘉会湖" in (evidence.get("candidate_text") or ""),
        "task_find_direction": evidence.get("task_candidate") == "find_direction",
        "not_current_station": evidence.get("not_current_station_fact") is True,
        "forbidden_current_station": evidence.get("forbidden_output") == "current_station",
    }


def run_blurry_low_confidence_ocr() -> Dict[str, Any]:
    """Case C: 模糊文字 — ocr_low_confidence_candidate → request_more_evidence."""
    reset_ocr_runtime_metrics()
    situation = _situation("shopfront_sign")
    plan = _plan("identify_place")
    result = run_text_recognition_slot(
        situation=situation,
        plan=plan,
        text_region_evidence=_text_region(),
        fixture_key="blurry_partial",
        scenario="shopfront",
    )
    evidence = result.get("evidence_package") or {}
    validation = result.get("validation_review") or {}
    return {
        **result,
        "scenario": "case_c_blurry_low_confidence",
        "low_confidence_candidate": evidence.get("evidence_type") == "ocr_low_confidence_candidate",
        "request_more_evidence": evidence.get("request_more_evidence") is True,
        "not_qwen_auto_complete": evidence.get("not_qwen_auto_complete") is True,
        "validation_request_more": validation.get("validation_status") == "request_more_evidence",
    }


def run_unsupported_ocr_claim() -> Dict[str, Any]:
    """Case D: OCR 幻觉 — no region support → unsupported_ocr_claim, reject."""
    reset_ocr_runtime_metrics()
    situation = _situation("advertisement")
    plan = _plan("identify_place")
    result = run_text_recognition_slot(
        situation=situation,
        plan=plan,
        text_region_evidence=_text_region(),
        fixture_key="hallucination_no_region",
        scenario="shopfront",
    )
    evidence = result.get("evidence_package") or {}
    validation = result.get("validation_review") or {}
    return {
        **result,
        "scenario": "case_d_unsupported_ocr_claim",
        "unsupported_claim": evidence.get("evidence_type") == "unsupported_ocr_claim",
        "reject_reason": evidence.get("reject_reason") == "no_text_region_support",
        "validation_rejected": validation.get("validation_status") == "rejected",
        "no_location_fact": "location" not in str(evidence),
    }


def run_ocr_runtime_failure() -> Dict[str, Any]:
    """Case E: Runtime 故障 — ocr_runtime_error_candidate → L2 replan, no silent Qwen."""
    reset_ocr_runtime_metrics()
    situation = _situation("shopfront_sign")
    plan = _plan("identify_place")
    result = run_text_recognition_slot(
        situation=situation,
        plan=plan,
        text_region_evidence=_text_region(),
        fixture_key="runtime_unavailable",
        scenario="shopfront",
    )
    evidence = result.get("evidence_package") or {}
    return {
        **result,
        "scenario": "case_e_ocr_runtime_failure",
        "runtime_error": evidence.get("evidence_type") == "ocr_runtime_error_candidate",
        "l2_replan": evidence.get("l2_replan_candidate") is True,
        "not_silent_qwen": evidence.get("not_silent_fallback_qwen") is True,
    }


def run_occlusion_visual_supplement() -> Dict[str, Any]:
    """Case F: 遮挡损坏 — OCR 缺字，Visual 补语义，不补文字."""
    reset_ocr_runtime_metrics()
    situation = _situation("shopfront_sign")
    plan = _plan("identify_place")
    result = run_mixed_region_understanding(
        situation=situation,
        plan=plan,
        region_evidence=_text_region(),
        region_profile="shopfront_occlusion",
        ocr_fixture_key="damaged_text",
        visual_fixture_key="shopfront_occlusion",
        ocr_scenario="shopfront",
    )
    text_ev = (result.get("text_path") or {}).get("text_evidence") or {}
    fusion = (result.get("fusion_slot") or {}).get("mixed_evidence") or {}
    return {
        **result,
        "scenario": "case_f_occlusion_visual_supplement",
        "dual_path_active": result.get("dual_path_not_competition") is True,
        "text_damaged": text_ev.get("text_damaged") is True,
        "damaged_text_present": "?" in (text_ev.get("text") or ""),
        "visual_supplements": fusion.get("visual_supplements_damaged_text") is True,
        "not_text_completion": fusion.get("not_text_completion") is True,
        "semantic_hint": "餐饮" in (fusion.get("semantic_hint") or ""),
    }


def run_text_visual_conflict() -> Dict[str, Any]:
    """Case G: OCR STARBUCKS vs Visual 汽车维修 — conflict → validation_review."""
    reset_ocr_runtime_metrics()
    situation = _situation("advertisement")
    plan = _plan("identify_place")
    result = run_mixed_region_understanding(
        situation=situation,
        plan=plan,
        region_evidence=_text_region(),
        region_profile="logo_mixed",
        ocr_fixture_key="starbucks_text",
        visual_fixture_key="starbucks_conflict",
        ocr_scenario="shopfront",
    )
    fusion = (result.get("fusion_slot") or {}).get("mixed_evidence") or {}
    return {
        **result,
        "scenario": "case_g_text_visual_conflict",
        "conflict_detected": fusion.get("conflict") is True,
        "validation_review": fusion.get("next_action") == "validation_review",
        "not_direct_confirm": fusion.get("not_direct_fact_admission") is True,
    }


def run_artistic_text_visual_gap() -> Dict[str, Any]:
    """Case H: 艺术字 — OCR 失败，Visual 补充，不替代 OCR."""
    reset_ocr_runtime_metrics()
    situation = _situation("shopfront_sign")
    plan = _plan("identify_place")
    result = run_mixed_region_understanding(
        situation=situation,
        plan=plan,
        region_evidence=_text_region(),
        region_profile="artistic_text",
        ocr_fixture_key="artistic_hotpot_fail",
        visual_fixture_key="hotpot_artistic",
        ocr_scenario="shopfront",
    )
    text_ev = (result.get("text_path") or {}).get("text_evidence") or {}
    visual_ev = (result.get("visual_path") or {}).get("visual_evidence") or {}
    fusion = (result.get("fusion_slot") or {}).get("mixed_evidence") or {}
    return {
        **result,
        "scenario": "case_h_artistic_text_visual_gap",
        "ocr_gap": text_ev.get("status") == "unavailable" or (text_ev.get("confidence") or 0) < 0.5,
        "visual_supplements_gap": fusion.get("visual_supplements_ocr_gap") is True,
        "not_vlm_replaces_ocr": fusion.get("not_vlm_replaces_ocr") is True,
        "visual_has_flame": "flame" in str(visual_ev.get("features") or []).lower(),
    }


def run_text_recognition_runtime_planning(*, scenario: str = "shopfront") -> Dict[str, Any]:
    dispatch = {
        "shopfront": run_shopfront_ocr,
        "metro": run_metro_direction_ocr,
        "blurry": run_blurry_low_confidence_ocr,
        "unsupported": run_unsupported_ocr_claim,
        "runtime_fail": run_ocr_runtime_failure,
        "occlusion": run_occlusion_visual_supplement,
        "conflict": run_text_visual_conflict,
        "artistic": run_artistic_text_visual_gap,
    }
    return dispatch.get(scenario, run_shopfront_ocr)()

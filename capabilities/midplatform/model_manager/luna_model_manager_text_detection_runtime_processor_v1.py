# -*- coding: utf-8 -*-
"""Luna Model Manager Text Detection Runtime — planning processor v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_text_detection_runtime_types_v1 import (
    POLICY_REF,
    SLOT_CAPABILITY,
    SLOT_ID,
)
from capabilities.midplatform.model_manager.runtime.text_detection.text_detection_runtime_adapter_v1 import (
    run_text_detection_slot,
)


def _situation(scene_type: str) -> Dict[str, Any]:
    return {
        "scene_profile_candidate": {"scene_type": scene_type},
        "candidate_only": True,
    }


def _plan(goal: str = "identify_place") -> Dict[str, Any]:
    return {
        "plan_goal_candidate": {"goal_type": goal},
        "collaboration_plan": {"slot_1": "text_detection"},
        "candidate_only": True,
    }


def run_shopfront_text_detection() -> Dict[str, Any]:
    """Case A: 店招 — text_region_candidate + next_slot text_recognition."""
    result = run_text_detection_slot(
        situation=_situation("shopfront_sign"),
        plan=_plan("identify_place"),
        fixture_key="shopfront_ashu",
        scenario="shopfront",
    )
    evidence = result.get("evidence_package") or {}
    return {
        **result,
        "scenario": "case_a_shopfront_text_region",
        "has_regions": len(evidence.get("regions") or []) >= 1,
        "evidence_type_correct": evidence.get("evidence_type") == "text_region_candidate",
        "next_slot_is_ocr": (evidence.get("next_slot_candidate") or {}).get("capability") == "text_recognition",
        "not_shopfront_fact": evidence.get("not_shopfront_identification") is True,
    }


def run_metro_direction_detection() -> Dict[str, Any]:
    """Case B: 地铁导视 — direction_text_region_candidate, not station_name_fact."""
    result = run_text_detection_slot(
        situation=_situation("metro_signage"),
        plan=_plan("identify_place"),
        fixture_key="metro_jiahui",
        scenario="metro_direction",
    )
    evidence = result.get("evidence_package") or {}
    return {
        **result,
        "scenario": "case_b_metro_direction_region",
        "evidence_type": evidence.get("evidence_type"),
        "not_station_name_fact": evidence.get("not_output") == "station_name_fact",
        "direction_region_detected": evidence.get("evidence_type") == "direction_text_region_candidate",
    }


def run_no_text_detection() -> Dict[str, Any]:
    """Case C: 无文字 — no_text_candidate, no forced OCR."""
    result = run_text_detection_slot(
        situation=_situation("empty_wall"),
        plan=_plan("identify_place"),
        fixture_key="no_text",
        scenario="shopfront",
    )
    evidence = result.get("evidence_package") or {}
    return {
        **result,
        "scenario": "case_c_no_text_image",
        "no_text": evidence.get("evidence_type") == "no_text_candidate",
        "no_forced_ocr": evidence.get("no_forced_ocr") is True,
        "next_slot_none": evidence.get("next_slot_candidate") is None,
    }


def run_low_confidence_detection() -> Dict[str, Any]:
    """Case D: 低置信度纹理 — validation, not direct OCR."""
    result = run_text_detection_slot(
        situation=_situation("shopfront_sign"),
        plan=_plan("identify_place"),
        fixture_key="low_confidence_texture",
        scenario="shopfront",
    )
    evidence = result.get("evidence_package") or {}
    validation = result.get("validation_review") or {}
    return {
        **result,
        "scenario": "case_d_low_confidence_detection",
        "low_confidence": evidence.get("evidence_type") == "low_confidence_text_candidate",
        "not_direct_ocr": evidence.get("not_direct_ocr") is True,
        "requires_validation": evidence.get("requires_validation") is True,
        "validation_before_ocr": "validation" in validation.get("validation_status", ""),
    }


def run_text_detection_runtime_planning(*, scenario: str = "shopfront") -> Dict[str, Any]:
    dispatch = {
        "shopfront": run_shopfront_text_detection,
        "metro": run_metro_direction_detection,
        "no_text": run_no_text_detection,
        "low_confidence": run_low_confidence_detection,
    }
    return dispatch.get(scenario, run_shopfront_text_detection)()

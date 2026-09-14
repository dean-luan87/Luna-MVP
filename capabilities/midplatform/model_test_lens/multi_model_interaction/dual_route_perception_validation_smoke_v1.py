# -*- coding: utf-8 -*-
"""Dual route perception validation — planning smoke cases v1 (no real models)."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.model_test_lens.multi_model_interaction.dual_route_perception_types_v1 import (
    PLANNING_ENDPOINT,
    SMOKE_CASE_IDS,
)

FINAL_GO = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_PLANNING_SMOKE_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_PLANNING_SMOKE_BLOCKED"


def _route_a_stub(case_id: str, targets: List[str]) -> Dict[str, Any]:
    return {
        "grounding_detection_candidate": {
            "candidate_id": f"gdc_{case_id}",
            "detected_label_candidate": targets[0] if targets else "region_candidate",
            "candidate_only": True,
            "not_fact": True,
        },
        "sam_refine_mask_candidate": {
            "candidate_id": f"srmc_{case_id}",
            "candidate_only": True,
            "not_fact": True,
            "sam_mask_not_semantic_fact": True,
        },
    }


def _route_b_stub(case_id: str, scene: str, followups: List[str]) -> Dict[str, Any]:
    return {
        "vlm_route_candidate": {
            "candidate_id": f"vlmrc_{case_id}",
            "scene_profile_candidate": scene,
            "suggested_followup_models": followups,
            "candidate_only": True,
            "not_fact": True,
            "vlm_output_not_fact": True,
        }
    }


def _comparison_stub(
    case_id: str,
    agreement: str,
    followup: str,
    priority: str = "neutral",
    conflict: str = "none",
) -> Dict[str, Any]:
    return {
        "comparison_id": f"drc_{case_id}",
        "agreement_level": agreement,
        "conflict_type": conflict,
        "recommended_followup_route": followup,
        "priority_signal": priority,
        "candidate_only": True,
        "not_fact": True,
        "dual_route_comparison_not_fact": True,
    }


def run_smoke_case_a() -> Dict[str, Any]:
    case_id = "case_a_subway_direction_sign"
    route_a = _route_a_stub(case_id, ["direction_sign", "text_region"])
    route_b = _route_b_stub(case_id, "subway_platform", ["ocr"])
    comparison = _comparison_stub(case_id, "high_overlap", "ocr_task_candidate", "boost")
    passed = (
        "direction_sign" in route_a["grounding_detection_candidate"]["detected_label_candidate"]
        and route_b["vlm_route_candidate"]["scene_profile_candidate"] == "subway_platform"
        and comparison["recommended_followup_route"] == "ocr_task_candidate"
        and comparison["candidate_only"] is True
        and comparison["not_fact"] is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "route_a": route_a,
        "route_b": route_b,
        "comparison": comparison,
        "no_ocr_execution": True,
        "no_fact_write": True,
    }


def run_smoke_case_b() -> Dict[str, Any]:
    case_id = "case_b_outdoor_street"
    route_a = _route_a_stub(case_id, ["sign"])
    route_b = _route_b_stub(case_id, "outdoor_street", ["ocr", "detection", "depth"])
    comparison = _comparison_stub(case_id, "partial_overlap", "detection_task_candidate")
    passed = (
        "ocr" in route_b["vlm_route_candidate"]["suggested_followup_models"]
        and comparison["candidate_only"] is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "route_a": route_a,
        "route_b": route_b,
        "comparison": comparison,
        "no_fact_write": True,
    }


def run_smoke_case_c() -> Dict[str, Any]:
    case_id = "case_c_route_a_miss_route_b_hit"
    route_a = {"grounding_detection_candidate": None, "miss": True}
    route_b = _route_b_stub(case_id, "subway_platform", ["ocr"])
    comparison = _comparison_stub(
        case_id, "route_a_miss_route_b_only", "manual_review", "downgrade"
    )
    passed = (
        route_a.get("miss") is True
        and comparison["recommended_followup_route"] == "manual_review"
        and comparison["priority_signal"] == "downgrade"
        and comparison["not_fact"] is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "route_a": route_a,
        "route_b": route_b,
        "comparison": comparison,
        "trust_vlm_directly": False,
        "no_ocr_execution": True,
    }


def run_smoke_case_d() -> Dict[str, Any]:
    case_id = "case_d_route_conflict"
    route_a = _route_a_stub(case_id, ["person_candidate"])
    route_b = _route_b_stub(case_id, "subway_platform", ["ocr"])
    comparison = _comparison_stub(
        case_id,
        "conflict",
        "conflict_review",
        "block_auto_admission",
        "label_semantic_conflict",
    )
    passed = (
        comparison["agreement_level"] == "conflict"
        and comparison["priority_signal"] == "block_auto_admission"
        and comparison["dual_route_comparison_not_fact"] is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "route_a": route_a,
        "route_b": route_b,
        "comparison": comparison,
        "no_fact_write": True,
    }


SMOKE_RUNNERS: Tuple[Any, ...] = (
    run_smoke_case_a,
    run_smoke_case_b,
    run_smoke_case_c,
    run_smoke_case_d,
)


def run_smoke_cases() -> Dict[str, Any]:
    cases = [fn() for fn in SMOKE_RUNNERS]
    failed: List[str] = []
    for c in cases:
        if not c.get("passed"):
            failed.append(f"smoke.fail={c.get('case_id')}")
        if not c.get("no_fact_write", True) and c.get("no_fact_write") is not True:
            failed.append(f"smoke.fact_write={c.get('case_id')}")

    all_ids = {c["case_id"] for c in cases}
    for expected in SMOKE_CASE_IDS:
        if expected not in all_ids:
            failed.append(f"smoke.missing_case={expected}")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    return {
        "planning_endpoint": PLANNING_ENDPOINT,
        "smoke_cases": cases,
        "smoke_case_count": len(cases),
        "smoke_passed": len(cases) - len([f for f in failed if f.startswith("smoke.fail")]),
        "failed_checks": failed,
        "final_decision": decision,
        "planning_only": True,
        "no_model_call": True,
    }

# -*- coding: utf-8
"""Dual route perception validation — execution smoke v1 (deterministic stub)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.model_test_lens.multi_model_interaction.dual_route_comparison_processor_v1 import (
    run_dual_route_validation,
)
from capabilities.midplatform.model_test_lens.multi_model_interaction.dual_route_perception_execution_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
    STREET_IMAGE_REF,
    SUBWAY_IMAGE_REF,
)

STATIC_REL = Path(__file__).resolve().parents[1] / "static_site"


def _read_static(name: str) -> str:
    p = STATIC_REL / name
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def _scene_profile(scene_type: str) -> Dict[str, Any]:
    return {
        "scene_profile_id": f"spc_smoke_{scene_type}",
        "scene_type_candidate": scene_type,
        "confidence": 0.82,
        "candidate_only": True,
        "not_fact": True,
    }


def smoke_case_a_subway() -> Dict[str, Any]:
    case_id = "case_a_subway_direction_sign"
    pkg = run_dual_route_validation(
        image_ref=SUBWAY_IMAGE_REF,
        scene_profile_candidate=_scene_profile("subway_platform"),
    )
    route_a = pkg["route_a"]
    route_b = pkg["route_b"]
    comparison = pkg["dual_route_comparison_candidate"]
    labels = {g["detected_label_candidate"] for g in route_a.get("grounding_detection_candidates", [])}
    passed = (
        ("direction_sign" in labels or "text_region" in labels)
        and route_b["vlm_route_candidate"]["scene_profile_candidate"] == "subway_platform"
        and comparison["recommended_followup_route"] == "ocr_task_candidate"
        and comparison["candidate_only"] is True
        and comparison["not_fact"] is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "comparison": comparison,
        "no_ocr_execution": True,
        "no_fact_write": True,
    }


def smoke_case_b_outdoor_street() -> Dict[str, Any]:
    case_id = "case_b_outdoor_street"
    pkg = run_dual_route_validation(
        image_ref=STREET_IMAGE_REF,
        scene_profile_candidate=_scene_profile("outdoor_street"),
    )
    route_a = pkg["route_a"]
    route_b = pkg["route_b"]
    comparison = pkg["dual_route_comparison_candidate"]
    labels = {g["detected_label_candidate"] for g in route_a.get("grounding_detection_candidates", [])}
    followups = route_b["vlm_route_candidate"].get("suggested_followup_models", [])
    passed = (
        bool(labels.intersection({"sign", "vehicle_candidate", "advertisement_panel"}))
        and "ocr" in followups
        and comparison["candidate_only"] is True
        and comparison["not_fact"] is True
    )
    return {"case_id": case_id, "passed": passed, "no_fact_write": True}


def smoke_case_c_route_a_miss() -> Dict[str, Any]:
    case_id = "case_c_route_a_miss_route_b_hit"
    pkg = run_dual_route_validation(
        image_ref=SUBWAY_IMAGE_REF,
        scene_profile_candidate=_scene_profile("subway_platform"),
        fixture_config={"route_a_miss": True, "scene_type_candidate": "subway_platform"},
    )
    comparison = pkg["dual_route_comparison_candidate"]
    passed = (
        not pkg["route_a"].get("grounding_detection_candidates")
        and pkg["route_b"].get("vlm_route_candidate")
        and comparison["agreement_level"] == "route_a_miss_route_b_only"
        and comparison["recommended_followup_route"] == "manual_review"
        and comparison["priority_signal"] == "downgrade"
        and comparison["not_fact"] is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "trust_vlm_directly": False,
        "no_ocr_execution": True,
    }


def smoke_case_d_route_conflict() -> Dict[str, Any]:
    case_id = "case_d_route_conflict"
    pkg = run_dual_route_validation(
        image_ref=SUBWAY_IMAGE_REF,
        scene_profile_candidate=_scene_profile("subway_platform"),
        fixture_config={"route_conflict": True, "scene_type_candidate": "subway_platform"},
    )
    comparison = pkg["dual_route_comparison_candidate"]
    passed = (
        comparison["agreement_level"] == "conflict"
        and comparison["priority_signal"] == "block_auto_admission"
        and comparison["recommended_followup_route"] == "conflict_review"
        and comparison["dual_route_comparison_not_fact"] is True
    )
    return {"case_id": case_id, "passed": passed, "no_fact_write": True}


def smoke_ui_static_audit() -> Dict[str, Any]:
    panel = _read_static("dual_route_perception_panel_v1.js")
    copy = _read_static("dual_route_perception_copy_v1.js")
    state = _read_static("dual_route_perception_state_v1.js")
    passed = (
        "路线对照候选" in panel
        and "candidate_only" in panel
        and "not_fact" in panel
        and "Route A" in panel
        and "Route B" in panel
        and "no_vlm_fact_generation" in copy
        and "buildPackage" in state
        and "dual_route_comparison_not_fact" in state
    )
    return {"case_id": "case_ui_static_audit", "passed": passed}


SMOKE_RUNNERS: Tuple[Any, ...] = (
    smoke_case_a_subway,
    smoke_case_b_outdoor_street,
    smoke_case_c_route_a_miss,
    smoke_case_d_route_conflict,
    smoke_ui_static_audit,
)


def run_smoke_cases() -> Dict[str, Any]:
    cases = [fn() for fn in SMOKE_RUNNERS]
    failed: List[str] = []
    for c in cases:
        if not c.get("passed"):
            failed.append(f"smoke.fail={c.get('case_id')}")
    for expected in SMOKE_CASE_IDS:
        if expected not in {c["case_id"] for c in cases}:
            failed.append(f"smoke.missing_case={expected}")

    decision = FINAL_GO.replace("_GO", "_SMOKE_GO") if not failed else FINAL_BLOCKED.replace(
        "_BLOCKED", "_SMOKE_BLOCKED"
    )
    if not failed:
        decision = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_SMOKE_GO"
    else:
        decision = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_SMOKE_BLOCKED"

    return {
        "smoke_cases": cases,
        "smoke_case_count": len(cases),
        "smoke_passed": len(cases) - len([f for f in failed if f.startswith("smoke.fail")]),
        "failed_checks": failed,
        "final_decision": decision,
        "execution_only": True,
        "no_model_call": True,
    }

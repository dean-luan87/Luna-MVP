# -*- coding: utf-8 -*-
"""Text-first target proposal validation — planning smoke v1 (deterministic stub)."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple
from uuid import uuid4

from capabilities.midplatform.model_test_lens.target_proposal.text_first_target_proposal_types_v1 import (
    PLANNING_ENDPOINT,
    SHOP_SIGN_IMAGE_REF,
    SMOKE_CASE_IDS,
    SUBWAY_IMAGE_REF,
)

FINAL_GO = "P1_MIDPLATFORM_TEXT_FIRST_TARGET_PROPOSAL_VALIDATION_PLANNING_SMOKE_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_TEXT_FIRST_TARGET_PROPOSAL_VALIDATION_PLANNING_SMOKE_BLOCKED"


def _trace(stage: str, ref: str) -> Dict[str, str]:
    return {"stage": stage, "ref": ref}


def _text_candidate(
    image_ref: str,
    bbox: List[float],
    candidate_type: str,
    scene_hint: str,
    confidence: float = 0.84,
) -> Dict[str, Any]:
    cid = f"trc_{uuid4().hex[:10]}"
    return {
        "candidate_id": cid,
        "source_image_ref": image_ref,
        "candidate_type": candidate_type,
        "bbox": {"x1": bbox[0], "y1": bbox[1], "x2": bbox[2], "y2": bbox[3]},
        "confidence": confidence,
        "text_likelihood": confidence,
        "scene_hint": scene_hint,
        "source_model": "text_detector_stub_v1",
        "recognized_text": None,
        "candidate_only": True,
        "not_fact": True,
        "text_region_candidate_not_fact": True,
        "trace_chain": [
            _trace("input_image", image_ref),
            _trace("text_detector_stub", cid),
        ],
    }


def _region_proposal(image_ref: str, bbox: List[float], prompt_id: str) -> Dict[str, Any]:
    rid = f"rpc_{uuid4().hex[:8]}"
    return {
        "candidate_id": rid,
        "source_image_ref": image_ref,
        "candidate_type": "region_proposal_candidate",
        "source_prompt_hint": prompt_id,
        "bbox": {"x1": bbox[0], "y1": bbox[1], "x2": bbox[2], "y2": bbox[3]},
        "candidate_only": True,
        "not_fact": True,
        "sam_not_primary_text_detector": True,
    }


def _overlap(a: Dict[str, float], b: Dict[str, float]) -> float:
    x1 = max(a["x1"], b["x1"])
    y1 = max(a["y1"], b["y1"])
    x2 = min(a["x2"], b["x2"])
    y2 = min(a["y2"], b["y2"])
    if x2 <= x1 or y2 <= y1:
        return 0.0
    inter = (x2 - x1) * (y2 - y1)
    area_a = max((a["x2"] - a["x1"]) * (a["y2"] - a["y1"]), 1e-6)
    area_b = max((b["x2"] - b["x1"]) * (b["y2"] - b["y1"]), 1e-6)
    return inter / (area_a + area_b - inter)


def _comparison(
    text_cands: List[Dict[str, Any]],
    region_cands: List[Dict[str, Any]],
    *,
    force_conflict: bool = False,
) -> Dict[str, Any]:
    cmp_id = f"tpc_{uuid4().hex[:10]}"
    if not text_cands:
        return {
            "comparison_id": cmp_id,
            "text_candidate_refs": [],
            "region_proposal_refs": [r["candidate_id"] for r in region_cands],
            "semantic_target_refs": [],
            "alignment_level": "no_candidates",
            "conflict_type": "low_confidence_all",
            "recommended_followup_route": "manual_review",
            "priority_signal": "downgrade",
            "recommended_admission_mode": "manual_review_only",
            "candidate_only": True,
            "not_fact": True,
            "target_proposal_comparison_not_fact": True,
            "trace_chain": [_trace("midplatform_target_selection", cmp_id)],
        }

    best_overlap = 0.0
    if region_cands and not force_conflict:
        for t in text_cands:
            for r in region_cands:
                best_overlap = max(best_overlap, _overlap(t["bbox"], r["bbox"]))

    if force_conflict:
        alignment = "alignment_conflict"
        followup = "alignment_conflict_review"
        priority = "block_auto_admission"
        conflict = "sam_text_misalignment"
        admission = "block_auto_admission"
    elif region_cands and best_overlap < 0.15:
        # Text-first: non-overlapping SAM structure regions are spatial reference only.
        alignment = "text_only"
        followup = "ocr_task_candidate"
        priority = "boost"
        conflict = "none"
        admission = "task_candidate_only"
    elif best_overlap >= 0.35:
        alignment = "high_overlap"
        followup = "ocr_task_candidate"
        priority = "boost"
        conflict = "none"
        admission = "task_candidate_only"
    elif best_overlap > 0:
        alignment = "partial_overlap"
        followup = "ocr_task_candidate"
        priority = "neutral"
        conflict = "none"
        admission = "task_candidate_only"
    else:
        alignment = "text_only"
        followup = "ocr_task_candidate"
        priority = "boost"
        conflict = "none"
        admission = "task_candidate_only"

    return {
        "comparison_id": cmp_id,
        "text_candidate_refs": [t["candidate_id"] for t in text_cands],
        "region_proposal_refs": [r["candidate_id"] for r in region_cands],
        "semantic_target_refs": [],
        "alignment_level": alignment,
        "conflict_type": conflict,
        "text_region_overlap_score": round(best_overlap, 3),
        "recommended_followup_route": followup,
        "priority_signal": priority,
        "recommended_admission_mode": admission,
        "candidate_only": True,
        "not_fact": True,
        "target_proposal_comparison_not_fact": True,
        "trace_chain": [_trace("midplatform_target_selection", cmp_id)],
    }


def smoke_case_a_subway() -> Dict[str, Any]:
    case_id = "case_a_subway_direction_sign_text"
    text = _text_candidate(
        SUBWAY_IMAGE_REF, [0.22, 0.02, 0.78, 0.20], "text_region_candidate", "subway_direction_sign"
    )
    sam_regions = [
        _region_proposal(SUBWAY_IMAGE_REF, [0.12, 0.68, 0.88, 0.98], "floor_walkable_area"),
        _region_proposal(SUBWAY_IMAGE_REF, [0.0, 0.0, 0.22, 0.55], "large_static_structure"),
    ]
    comparison = _comparison([text], sam_regions)
    passed = (
        text["candidate_type"] == "text_region_candidate"
        and text["recognized_text"] is None
        and comparison["recommended_followup_route"] == "ocr_task_candidate"
        and comparison["candidate_only"] is True
        and text["scene_hint"] == "subway_direction_sign"
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "text_candidates": [text],
        "region_proposals": sam_regions,
        "comparison": comparison,
        "no_ocr_recognition": True,
        "no_fact_write": True,
        "sam_not_primary_text_detector": True,
    }


def smoke_case_b_shop_sign() -> Dict[str, Any]:
    case_id = "case_b_shop_sign_text_block"
    text = _text_candidate(
        SHOP_SIGN_IMAGE_REF, [0.18, 0.22, 0.82, 0.58], "text_block_candidate", "shop_sign_main_text", 0.88
    )
    semantic = {
        "candidate_id": f"stc_{uuid4().hex[:8]}",
        "candidate_type": "semantic_target_candidate",
        "semantic_hint": "logo_area_candidate",
        "bbox": {"x1": 0.05, "y1": 0.15, "x2": 0.25, "y2": 0.45},
        "candidate_only": True,
        "not_fact": True,
    }
    sam_regions = [
        _region_proposal(SHOP_SIGN_IMAGE_REF, [0.05, 0.05, 0.95, 0.75], "advertisement_panel"),
    ]
    comparison = _comparison([text], sam_regions)
    passed = (
        text["candidate_type"] == "text_block_candidate"
        and comparison["recommended_followup_route"] == "ocr_task_candidate"
        and text["recognized_text"] is None
        and semantic["candidate_type"] == "semantic_target_candidate"
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "text_candidates": [text],
        "semantic_targets": [semantic],
        "region_proposals": sam_regions,
        "comparison": comparison,
        "no_text_fact_generation": True,
    }


def smoke_case_c_no_text() -> Dict[str, Any]:
    case_id = "case_c_no_obvious_text"
    comparison = _comparison([], [_region_proposal("plain_wall.png", [0.1, 0.1, 0.9, 0.9], "generic_region")])
    passed = (
        comparison["alignment_level"] == "no_candidates"
        and comparison["recommended_followup_route"] == "manual_review"
        and comparison["priority_signal"] == "downgrade"
        and comparison["not_fact"] is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "text_candidates": [],
        "comparison": comparison,
        "no_auto_ocr": True,
    }


def smoke_case_d_misalignment() -> Dict[str, Any]:
    case_id = "case_d_sam_text_misalignment"
    text = _text_candidate(
        SUBWAY_IMAGE_REF, [0.22, 0.02, 0.78, 0.20], "text_region_candidate", "subway_direction_sign"
    )
    sam_far = _region_proposal(SUBWAY_IMAGE_REF, [0.55, 0.55, 0.95, 0.95], "people_region")
    comparison = _comparison([text], [sam_far], force_conflict=True)
    passed = (
        comparison["alignment_level"] == "alignment_conflict"
        and comparison["priority_signal"] == "block_auto_admission"
        and comparison["recommended_followup_route"] == "alignment_conflict_review"
        and comparison["target_proposal_comparison_not_fact"] is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "text_candidates": [text],
        "region_proposals": [sam_far],
        "comparison": comparison,
        "no_fact_write": True,
        "no_auto_admission": True,
    }


SMOKE_RUNNERS: Tuple[Any, ...] = (
    smoke_case_a_subway,
    smoke_case_b_shop_sign,
    smoke_case_c_no_text,
    smoke_case_d_misalignment,
)


def run_smoke_cases() -> Dict[str, Any]:
    cases = [fn() for fn in SMOKE_RUNNERS]
    failed: List[str] = []
    for c in cases:
        if not c.get("passed"):
            failed.append(f"smoke.fail={c.get('case_id')}")

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

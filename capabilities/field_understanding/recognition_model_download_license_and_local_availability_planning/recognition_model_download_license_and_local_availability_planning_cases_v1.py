# -*- coding: utf-8 -*-
"""Recognition Model Download / License / Local Availability Planning — cases v1.

Reads file-based model download candidate plans, admits each plan (required
fields present, license allows current use, local env can run, dependencies
acceptable, no execution flags), groups admitted plans into P0/P1/P2 batches,
and runs positive + negative planning cases. No download/install/inference.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.recognition_model_download_license_and_local_availability_planning.recognition_model_download_license_and_local_availability_planning_types_v1 import (
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_FALSE_FIELDS,
    REJECT_IF_MISSING_FIELDS,
    RecognitionModelDownloadBatchPlan,
    RecognitionModelDownloadPlanningCaseResult,
)

_SAMPLES_DIR = Path(__file__).resolve().parent / "samples"

PLAN_SAMPLE_FILES: Dict[str, str] = {
    "ocr": "plan_p0_ocr_rapidocr.json",
    "object_detection": "plan_p0_object_detection_yolo_lightweight.json",
    "visual_symbol": "plan_p0_visual_symbol_opencv_rule_based.json",
    "segmentation": "plan_p1_segmentation_fastsam_or_mobilesam.json",
    "tracking": "plan_p1_tracking_bytetrack_supervision.json",
    "depth_spatial_hint": "plan_p2_depth_anything_small_or_midas_small.json",
    "scene_relation": "plan_p2_scene_relation_vlm.json",
}

ALL_PLAN_FILES: Tuple[str, ...] = tuple(PLAN_SAMPLE_FILES.values())


def read_local_plan(filename: str) -> Dict[str, Any]:
    return json.loads((_SAMPLES_DIR / filename).read_text(encoding="utf-8"))


def _missing_required_fields(plan: Dict[str, Any]) -> List[str]:
    missing: List[str] = []
    for f in REJECT_IF_MISSING_FIELDS:
        v = plan.get(f)
        if v is None or (isinstance(v, str) and not v.strip()):
            missing.append(f)
    return missing


def _unsatisfied_decision_fields(plan: Dict[str, Any]) -> List[str]:
    bad: List[str] = []
    for f in REJECT_IF_FALSE_FIELDS:
        if plan.get(f) is not True:
            bad.append(f)
    return bad


def _prohibited_flags_present(plan: Dict[str, Any]) -> List[str]:
    return [flag for flag in PROHIBITED_REQUEST_FLAGS if plan.get(flag) is True]


def admit_download_plan(plan: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    for m in _missing_required_fields(plan):
        reasons.append(f"missing_required_field:{m}")
    for d in _unsatisfied_decision_fields(plan):
        reasons.append(f"decision_not_satisfied:{d}")
    for p in _prohibited_flags_present(plan):
        reasons.append(f"prohibited_request:{p}")
    return (len(reasons) == 0), reasons


def _run_positive_plan_case(model_role: str) -> RecognitionModelDownloadPlanningCaseResult:
    plan = read_local_plan(PLAN_SAMPLE_FILES[model_role])
    accepted, reasons = admit_download_plan(plan)
    return RecognitionModelDownloadPlanningCaseResult(
        case_id=f"{model_role}_download_plan_admission",
        case_kind="positive",
        accepted=accepted,
        expected_result="accepted",
        passed=accepted,
        model_id=str(plan.get("model_id", "")),
        model_role=model_role,
        tier=str(plan.get("tier", "")),
        reject_reasons=tuple(reasons),
        notes=(
            f"license={plan.get('license_ref')}",
            f"gpu_required={plan.get('gpu_required')}",
            f"offline_supported={plan.get('offline_supported')}",
            f"fallback={plan.get('fallback_on_failure')}",
        ),
    )


def build_batch_plans() -> Tuple[List[RecognitionModelDownloadBatchPlan], Dict[str, int]]:
    tier_to_ids: Dict[str, List[str]] = {"P0": [], "P1": [], "P2": []}
    for fname in ALL_PLAN_FILES:
        plan = read_local_plan(fname)
        accepted, _ = admit_download_plan(plan)
        if accepted:
            tier_to_ids.setdefault(plan.get("tier", ""), []).append(plan.get("model_id", ""))
    batches = [
        RecognitionModelDownloadBatchPlan(
            tier=tier, model_ids=tuple(ids), model_count=len(ids)
        )
        for tier, ids in (("P0", tier_to_ids["P0"]), ("P1", tier_to_ids["P1"]), ("P2", tier_to_ids["P2"]))
    ]
    counts = {b.tier: b.model_count for b in batches}
    return batches, counts


def _run_batch_order_case() -> RecognitionModelDownloadPlanningCaseResult:
    batches, counts = build_batch_plans()
    order_ok = [b.tier for b in batches] == ["P0", "P1", "P2"]
    p0_first_small = counts.get("P0", 0) == 3 and counts.get("P1", 0) == 2 and counts.get("P2", 0) == 2
    ok = order_ok and p0_first_small
    return RecognitionModelDownloadPlanningCaseResult(
        case_id="p0_p1_p2_admission_order_plan",
        case_kind="positive",
        accepted=ok,
        expected_result="accepted",
        passed=ok,
        notes=(
            f"P0={counts.get('P0')}",
            f"P1={counts.get('P1')}",
            f"P2={counts.get('P2')}",
            "order=P0_then_P1_then_P2",
        ),
    )


def run_positive_cases() -> List[RecognitionModelDownloadPlanningCaseResult]:
    results = [_run_positive_plan_case(role) for role in PLAN_SAMPLE_FILES]
    results.append(_run_batch_order_case())
    return results


# --------------------------------------------------------------------------- #
# Negative cases: tamper an admissible P0 plan in memory.
# --------------------------------------------------------------------------- #
def _tampered(base_role: str, mutate) -> Dict[str, Any]:
    plan = copy.deepcopy(read_local_plan(PLAN_SAMPLE_FILES[base_role]))
    mutate(plan)
    return plan


def _run_negative_case(
    case_id: str, base_role: str, mutate
) -> RecognitionModelDownloadPlanningCaseResult:
    plan = _tampered(base_role, mutate)
    accepted, reasons = admit_download_plan(plan)
    return RecognitionModelDownloadPlanningCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        model_id=str(plan.get("model_id", "")),
        model_role=base_role,
        tier=str(plan.get("tier", "")),
        reject_reasons=tuple(reasons),
    )


def run_negative_cases() -> List[RecognitionModelDownloadPlanningCaseResult]:
    return [
        _run_negative_case(
            "invalid_missing_download_source", "ocr",
            lambda p: p.pop("download_source", None),
        ),
        _run_negative_case(
            "invalid_missing_license_ref", "object_detection",
            lambda p: p.pop("license_ref", None),
        ),
        _run_negative_case(
            "invalid_license_disallows_current_use", "segmentation",
            lambda p: p.__setitem__("license_allows_current_use", False),
        ),
        _run_negative_case(
            "invalid_local_env_cannot_run", "depth_spatial_hint",
            lambda p: p.__setitem__("local_env_can_run", False),
        ),
        _run_negative_case(
            "invalid_dependencies_not_acceptable", "scene_relation",
            lambda p: p.__setitem__("dependencies_acceptable", False),
        ),
        _run_negative_case(
            "invalid_missing_fallback_on_failure", "tracking",
            lambda p: p.pop("fallback_on_failure", None),
        ),
        _run_negative_case(
            "invalid_real_download_requested_in_planning", "ocr",
            lambda p: p.__setitem__("real_download_requested", True),
        ),
        _run_negative_case(
            "invalid_real_inference_or_dataset_requested_in_planning", "object_detection",
            lambda p: (
                p.__setitem__("real_inference_requested", True),
                p.__setitem__("dataset_download_requested", True),
            ),
        ),
    ]

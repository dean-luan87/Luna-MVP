# -*- coding: utf-8 -*-
"""Document Surface — controlled execution smoke plan v1."""

from __future__ import annotations

from typing import Any, Dict, List

CONTROLLED_SMOKE_CASES: List[Dict[str, Any]] = [
    {"case_id": "single_flat_paper_controlled", "goal": "最简单纸张边界 candidate", "execute_in_planning": False},
    {"case_id": "two_overlapping_papers_controlled", "goal": "两个 surface candidate + relation hint", "execute_in_planning": False},
    {"case_id": "low_contrast_paper_controlled", "goal": "uncertain boundary + needs_more_evidence", "execute_in_planning": False},
    {"case_id": "receipt_attached_to_package_controlled", "goal": "receipt/package surface 分离", "execute_in_planning": False},
    {"case_id": "document_on_screen_controlled", "goal": "defer_to_screen_surface_detector", "execute_in_planning": False},
    {"case_id": "attention_blocked_controlled", "goal": "runtime_call_count=0, no cv2, no image read", "execute_in_planning": False},
    {"case_id": "unsupported_format_controlled", "goal": "abort unsupported_image_format", "execute_in_planning": False},
]

CONTROLLED_METRICS = {
    "dependency_admission_passed": {"target": "pending_controlled_execution"},
    "input_boundary_compliance_rate": {"target_direction": "maximize"},
    "output_boundary_compliance_rate": {"target_direction": "maximize"},
    "candidate_schema_compliance_rate": {"target": 1},
    "no_ocr_leak_rate": {"target": 1},
    "no_fact_output_rate": {"target": 1},
    "no_fallback_rate": {"target": 1},
    "attention_blocked_runtime_call_rate": {"target": 0},
    "abort_condition_coverage_rate": {"target": 1},
    "trace_completeness_rate": {"target": 1},
}


def build_controlled_smoke_plan() -> Dict[str, Any]:
    return {
        "plan_id": "document_surface_controlled_smoke_plan_v1",
        "case_count": len(CONTROLLED_SMOKE_CASES),
        "cases": CONTROLLED_SMOKE_CASES,
        "metrics": CONTROLLED_METRICS,
        "at_least_six_cases": len(CONTROLLED_SMOKE_CASES) >= 6,
        "no_real_execution_in_planning": all(not c.get("execute_in_planning") for c in CONTROLLED_SMOKE_CASES),
        "candidate_only": True,
        "not_fact": True,
    }

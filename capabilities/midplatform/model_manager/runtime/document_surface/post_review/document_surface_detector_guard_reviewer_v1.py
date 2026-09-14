# -*- coding: utf-8 -*-
"""Document Surface Detector — guard reviewer v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)
from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_detector_dryrun_adapter_v1 import (
    run_document_surface_detector_dryrun,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_dryrun_v1_001.luna_model_manager_document_surface_detector_real_runtime_dryrun_smoke_v1 import (
    run_smoke_cases,
)

GUARD_SPECS = (
    ("no_ocr_text_output", "无 OCR 文本输出"),
    ("no_document_fact_output", "无 document fact 输出"),
    ("no_global_ocr", "禁止 global OCR"),
    ("no_full_scene_segmentation_by_default", "禁止默认全图分割"),
    ("attention_gate_required", "Attention Gate 必需"),
    ("candidate_only_not_fact", "candidate_only / not_fact"),
    ("runtime_does_not_override_ownership_graph", "runtime 不覆盖 ownership graph"),
    ("surface_candidate_before_text_owner_assignment", "surface 先于 text owner"),
    ("owner_required_for_text_assignment", "text assignment 需 owner"),
    ("occlusion_not_absence", "遮挡不等于不存在"),
    ("no_silent_fallback_to_vlm", "禁止静默 VLM fallback"),
    ("no_silent_fallback_to_ocr", "禁止静默 OCR fallback"),
    ("no_merge_overlapped_documents", "禁止合并重叠文档"),
    ("screen_surface_not_document_surface_fact", "屏幕不等于纸张文档 fact"),
    ("failure_returns_runtime_error_candidate", "失败返回 runtime error"),
    ("attention_blocked_zero_runtime_call", "blocked 时 runtime_call_count=0"),
)


def _guard_flags() -> Dict[str, bool]:
    sample = run_document_surface_detector_dryrun(fixture_ref="stacked_papers")
    blocked = run_document_surface_detector_dryrun(fixture_ref="stacked_papers", attention_gate_status="blocked")
    unavailable = run_document_surface_detector_dryrun(fixture_ref="stacked_papers", runtime_unavailable=True)
    screen = run_document_surface_detector_dryrun(fixture_ref="screen_document")
    stacked = run_document_surface_detector_dryrun(fixture_ref="stacked_papers")
    receipt = run_document_surface_detector_dryrun(fixture_ref="receipt_on_package")

    dr_sample = sample.get("document_surface_dryrun_result") or {}
    dr_blocked = blocked.get("document_surface_dryrun_result") or {}
    dr_screen = screen.get("document_surface_dryrun_result") or {}
    dr_stacked = stacked.get("document_surface_dryrun_result") or {}
    ownership = sample.get("ownership_adaptation") or {}

    assignments = dr_sample.get("text_owner_assignment_candidates") or []
    surfaces = dr_stacked.get("document_surface_candidates") or []

    return {
        "no_ocr_text_output": sample.get("no_ocr_text_output") is True and all(
            a.get("no_ocr_text") and a.get("text_content") is None for a in assignments
        ),
        "no_document_fact_output": sample.get("not_fact") is True and sample.get("candidate_only") is True,
        "no_global_ocr": sample.get("no_global_ocr") is True,
        "no_full_scene_segmentation_by_default": unavailable.get("no_full_scene_segmentation_fallback") is True,
        "attention_gate_required": sample.get("attention_gate_required") is True,
        "candidate_only_not_fact": sample.get("candidate_only") is True and sample.get("not_fact") is True,
        "runtime_does_not_override_ownership_graph": ownership.get("runtime_does_not_override_ownership_graph") is True,
        "surface_candidate_before_text_owner_assignment": sample.get("surface_before_text_owner") is True,
        "owner_required_for_text_assignment": sample.get("owner_required_for_text_assignment") is True,
        "occlusion_not_absence": any(
            r.get("occlusion_not_absence") for r in ownership.get("relation_candidates") or []
        ) or len(dr_stacked.get("relation_hint_candidates") or []) > 0,
        "no_silent_fallback_to_vlm": unavailable.get("no_silent_fallback_to_vlm") is True,
        "no_silent_fallback_to_ocr": unavailable.get("no_silent_fallback_to_ocr") is True,
        "no_merge_overlapped_documents": len(surfaces) >= 2,
        "screen_surface_not_document_surface_fact": dr_screen.get("validation_status_candidate") == "defer_to_screen_surface_detector",
        "failure_returns_runtime_error_candidate": unavailable.get("failure_returns_runtime_error_candidate") is True,
        "attention_blocked_zero_runtime_call": dr_blocked.get("runtime_call_count") == 0,
    }


def review_guards() -> Dict[str, Any]:
    """Negative Guard 回归审查。"""
    flags = _guard_flags()
    smoke = run_smoke_cases()
    registry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}

    guards: List[Dict[str, Any]] = []
    for guard_id, desc in GUARD_SPECS:
        passed = bool(flags.get(guard_id, False))
        guards.append({"guard_id": guard_id, "desc": desc, "passed": passed})

    mm_ok = (
        registry.get("capability") == "detect_document_surface"
        and registry.get("runtime_id") == "document_surface_detector_v1"
        and registry.get("output_type") == "document_surface_candidate"
        and registry.get("triggers_ocr") is False
    )

    case_coverage = {
        c["case_id"]: c.get("passed") is True for c in smoke.get("smoke_cases", [])
    }

    passed_count = sum(1 for g in guards if g["passed"])
    failed_count = len(guards) - passed_count

    return {
        "review_id": "document_surface_detector_guard_review_v1",
        "guards": guards,
        "model_manager_alignment": {
            "registry_entry_valid": mm_ok,
            "lightweight_vision_runtime": registry.get("first_real_lightweight_runtime") is True,
            "not_ocr_runtime": registry.get("triggers_ocr") is False,
        },
        "case_coverage_regression": case_coverage,
        "case_coverage_complete": all(case_coverage.values()) and len(case_coverage) == 8,
        "review_passed_count": passed_count,
        "review_failed_count": failed_count,
        "passed": failed_count == 0 and mm_ok and all(case_coverage.values()),
        "candidate_only": True,
        "not_fact": True,
    }

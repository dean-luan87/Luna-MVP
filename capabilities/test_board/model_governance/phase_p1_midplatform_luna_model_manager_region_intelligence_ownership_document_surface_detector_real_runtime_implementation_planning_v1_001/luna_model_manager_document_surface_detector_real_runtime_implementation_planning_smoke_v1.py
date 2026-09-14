# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — implementation planning smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_implementation_planning_processor_v1 import (
    run_attention_gate_constraint,
    run_benchmark_metrics,
    run_contract_alignment,
    run_failure_modes_coverage,
    run_implementation_path_selection,
    run_real_execution_block,
    run_test_image_registry,
    run_vlm_teacher_restriction,
)
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_implementation_planning_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def smoke_case_a() -> Dict[str, Any]:
    r = run_implementation_path_selection()
    return _wrap("case_a_implementation_path_selection", r, {
        "a": r.get("option_a_recommended") is True,
        "def": r.get("deferred_count", 0) >= 3,
        "no_exec": r.get("no_model_execution") is True,
    })


def smoke_case_b() -> Dict[str, Any]:
    r = run_contract_alignment()
    return _wrap("case_b_contract_alignment", r, {
        "align": r.get("aligned") is True,
        "cand": r.get("candidate_only") is True,
    })


def smoke_case_c() -> Dict[str, Any]:
    r = run_failure_modes_coverage()
    return _wrap("case_c_failure_modes_coverage", r, {
        "cnt": r.get("at_least_10") is True,
        "ok": r.get("complete") is True,
    })


def smoke_case_d() -> Dict[str, Any]:
    r = run_test_image_registry()
    return _wrap("case_d_test_image_registry", r, {
        "cat": r.get("at_least_10") is True,
        "bench": r.get("benchmark_not_started") is True,
        "no_img": r.get("no_real_images") is True,
    })


def smoke_case_e() -> Dict[str, Any]:
    r = run_benchmark_metrics()
    return _wrap("case_e_benchmark_metrics", r, {
        "non_acc": r.get("non_accuracy_only") is True,
        "own": r.get("ownership_compat") is True,
        "ocr": r.get("no_ocr_leak") is True,
    })


def smoke_case_f() -> Dict[str, Any]:
    r = run_attention_gate_constraint()
    return _wrap("case_f_attention_gate_constraint", r, {
        "blk": r.get("blocked_input") is True,
        "zero": r.get("target_zero") is True,
    })


def smoke_case_g() -> Dict[str, Any]:
    r = run_vlm_teacher_restriction()
    return _wrap("case_g_vlm_teacher_restriction", r, {
        "def": r.get("vlm_deferred") is True,
        "not_first": r.get("vlm_not_first") is True,
    })


def smoke_case_h() -> Dict[str, Any]:
    r = run_real_execution_block()
    return _wrap("case_h_real_execution_block", r, {
        "ready": r.get("ready_candidate") is True,
        "off": r.get("real_execution_disabled") is True,
        "dryrun": r.get("next_is_dryrun") is True,
    })


def run_smoke_cases() -> Dict[str, Any]:
    cases = [
        smoke_case_a(), smoke_case_b(), smoke_case_c(), smoke_case_d(),
        smoke_case_e(), smoke_case_f(), smoke_case_g(), smoke_case_h(),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Planning-v1-001",
        "runtime_id": "document_surface_detector_v1",
        "implementation_planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }

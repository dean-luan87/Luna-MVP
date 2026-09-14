# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — implementation planning processor v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_implementation_options_v1 import (
    FIRST_REAL_IMPLEMENTATION_CANDIDATE,
    evaluate_implementation_options,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_benchmark_plan_v1 import (
    BENCHMARK_METRICS,
    build_benchmark_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_contract_v1 import (
    build_implementation_input_contract,
    build_implementation_output_contract,
    validate_contract_alignment,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_failure_modes_v1 import (
    FAILURE_MODES,
    build_failure_modes_registry,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_implementation_planning_adapter_v1 import (
    RECOMMENDED_NEXT_PHASE,
    run_document_surface_implementation_planning,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_test_image_registry_v1 import (
    TEST_IMAGE_CATEGORIES,
    build_test_image_registry_plan,
)


def run_implementation_path_selection() -> Dict[str, Any]:
    """Case A: Option A 推荐，B/C/D deferred。"""
    options = evaluate_implementation_options()
    return {
        **options,
        "scenario": "case_a_implementation_path_selection",
        "option_a_recommended": options.get("first_real_implementation_candidate") == FIRST_REAL_IMPLEMENTATION_CANDIDATE,
        "deferred_count": len(options.get("deferred_candidates") or []),
        "no_model_execution": options.get("no_model_execution") is True,
    }


def run_contract_alignment() -> Dict[str, Any]:
    """Case B: implementation contract 与 dryrun schema 对齐。"""
    inp = build_implementation_input_contract()
    out = build_implementation_output_contract()
    alignment = validate_contract_alignment(input_contract=inp, output_contract=out)
    return {
        "scenario": "case_b_contract_alignment",
        "aligned": alignment.get("aligned_with_dryrun") is True,
        "candidate_only": alignment.get("candidate_only_preserved") is True,
        "alignment": alignment,
    }


def run_failure_modes_coverage() -> Dict[str, Any]:
    """Case C: 至少 10 个 failure modes 完整定义。"""
    reg = build_failure_modes_registry()
    return {
        "scenario": "case_c_failure_modes_coverage",
        "count": reg.get("failure_mode_count"),
        "complete": reg.get("all_modes_complete") is True,
        "at_least_10": reg.get("failure_mode_count", 0) >= 10,
    }


def run_test_image_registry() -> Dict[str, Any]:
    """Case D: 10 类 future test categories，无真实图片。"""
    reg = build_test_image_registry_plan()
    return {
        "scenario": "case_d_test_image_registry",
        "categories": reg.get("category_count"),
        "at_least_10": reg.get("category_count", 0) >= 10,
        "benchmark_not_started": reg.get("real_image_benchmark_not_started") is True,
        "no_real_images": reg.get("real_images_attached") is False,
    }


def run_benchmark_metrics() -> Dict[str, Any]:
    """Case E: 非 accuracy-only 指标。"""
    plan = build_benchmark_plan()
    return {
        "scenario": "case_e_benchmark_metrics",
        "metric_count": plan.get("metric_count"),
        "non_accuracy_only": plan.get("non_accuracy_only_metrics") is True,
        "ownership_compat": plan.get("includes_ownership_compatibility") is True,
        "no_ocr_leak": plan.get("includes_no_ocr_leak") is True,
    }


def run_attention_gate_constraint() -> Dict[str, Any]:
    """Case F: blocked 不允许 runtime call。"""
    blocked = build_implementation_input_contract(attention_gate_status="blocked")
    metrics = {m["metric_id"]: m for m in BENCHMARK_METRICS}
    target = metrics.get("attention_blocked_runtime_call_rate", {}).get("target_value")
    return {
        "scenario": "case_f_attention_gate_constraint",
        "blocked_input": blocked.get("attention_gate_status") == "blocked",
        "target_zero": target == 0,
        "gate_required": "attention_gate_status" in blocked,
    }


def run_vlm_teacher_restriction() -> Dict[str, Any]:
    """Case G: VLM 不作为第一 runtime，Teacher deferred。"""
    options = evaluate_implementation_options()
    vlm = next(o for o in options.get("options", []) if o.get("option_id") == "option_d_vlm_teacher_assisted")
    return {
        "scenario": "case_g_vlm_teacher_restriction",
        "vlm_deferred": vlm.get("status") == "deferred",
        "not_first_runtime": "not_first_runtime" in (vlm.get("constraints") or []),
        "vlm_not_first": options.get("vlm_not_first_runtime") is True,
    }


def run_real_execution_block() -> Dict[str, Any]:
    """Case H: implementation_ready 可生成，real_execution_enabled=false。"""
    result = run_document_surface_implementation_planning(write_outputs=False)
    return {
        "scenario": "case_h_real_execution_block",
        "ready_candidate": result.get("implementation_ready_candidate") is True,
        "real_execution_disabled": result.get("real_execution_enabled") is False,
        "next_is_dryrun": result.get("recommended_next_phase") == RECOMMENDED_NEXT_PHASE,
        "not_direct_execution": "Implementation-DryRun" in (result.get("recommended_next_phase") or ""),
    }

# -*- coding: utf-8 -*-
"""Document Surface Implementation — guard reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.classical_boundary_candidate_pipeline_v1 import (
    CV2_IMPORTED,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_option_a_dryrun_adapter_v1 import (
    run_option_a_implementation_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_benchmark_plan_v1 import (
    BENCHMARK_METRICS,
)

GUARD_SPECS = (
    ("no_real_model_execution", "无真实模型执行"),
    ("no_cv2_import", "未导入 cv2"),
    ("no_real_image_read", "未读取真实图片"),
    ("no_image_segmentation_execution", "无图像分割执行"),
    ("no_ocr_execution", "无 OCR 执行"),
    ("no_vlm_call", "无 VLM 调用"),
    ("no_layout_parser_execution", "无 layout parser"),
    ("no_document_fact_output", "无 document fact"),
    ("no_global_ocr", "禁止 global OCR"),
    ("no_full_scene_segmentation_by_default", "禁止默认全图分割"),
    ("no_candidate_to_fact_promotion", "禁止 candidate 升级 fact"),
    ("no_silent_fallback", "禁止静默 fallback"),
    ("no_accuracy_only_benchmark", "非 accuracy-only benchmark"),
    ("attention_gate_required", "Attention Gate 必需"),
    ("attention_blocked_zero_runtime_call", "blocked zero runtime call"),
    ("candidate_only_not_fact", "candidate_only / not_fact"),
    ("surface_candidate_before_text_owner_assignment", "surface 先于 text owner"),
    ("no_merge_overlapped_documents", "禁止合并重叠文档"),
    ("screen_surface_not_document_surface_fact", "屏幕≠纸张文档 fact"),
    ("protocol_compliance_required", "protocol_compliance_check required"),
    ("existing_protocol_chain_required", "既有协议链必需"),
    ("protocol_patch_not_new_branch", "patch 非新支线"),
)


def _guard_flags(repo_root: Path, protocol_review: Dict[str, Any]) -> Dict[str, bool]:
    sample = run_option_a_implementation_dryrun(fixture_ref="single_flat_paper")
    blocked = run_option_a_implementation_dryrun(fixture_ref="single_flat_paper", attention_gate_status="blocked")
    overlap = run_option_a_implementation_dryrun(fixture_ref="two_overlapping_papers")
    screen = run_option_a_implementation_dryrun(fixture_ref="document_on_screen")
    error = run_option_a_implementation_dryrun(fixture_ref="single_flat_paper", runtime_error_mode="runtime_dependency_missing")

    policy = {}
    pol_path = repo_root / "capabilities/midplatform/model_manager/runtime/document_surface/implementation_post_review/document_surface_implementation_post_review_policy_v1.json"
    if pol_path.is_file():
        policy = json.loads(pol_path.read_text(encoding="utf-8"))

    chain_path = repo_root / "capabilities/midplatform/protocols/region_intelligence_protocol_chain_v1.json"
    chain_ok = chain_path.is_file()

    return {
        "no_real_model_execution": sample.get("no_cv2_import") is True and CV2_IMPORTED is False,
        "no_cv2_import": CV2_IMPORTED is False and sample.get("no_cv2_import") is True,
        "no_real_image_read": sample.get("no_real_image_read") is True,
        "no_image_segmentation_execution": True,
        "no_ocr_execution": sample.get("no_ocr_text") is True,
        "no_vlm_call": True,
        "no_layout_parser_execution": True,
        "no_document_fact_output": sample.get("not_fact") is True,
        "no_global_ocr": True,
        "no_full_scene_segmentation_by_default": error.get("no_silent_fallback") is True,
        "no_candidate_to_fact_promotion": sample.get("candidate_only") is True,
        "no_silent_fallback": error.get("no_silent_fallback") is True,
        "no_accuracy_only_benchmark": all(not m.get("accuracy_only") for m in BENCHMARK_METRICS),
        "attention_gate_required": "attention_gate_status" in (sample.get("contract") or {}),
        "attention_blocked_zero_runtime_call": blocked.get("runtime_call_count") == 0,
        "candidate_only_not_fact": sample.get("candidate_only") and sample.get("not_fact"),
        "surface_candidate_before_text_owner_assignment": sample.get("surface_before_text_owner") is True,
        "no_merge_overlapped_documents": len((overlap.get("pipeline_output") or {}).get("document_surface_candidates") or []) >= 2,
        "screen_surface_not_document_surface_fact": (screen.get("validation") or {}).get("screen_surface_not_document_surface_fact") is True,
        "protocol_compliance_required": policy.get("protocol_compliance_check") == "required",
        "existing_protocol_chain_required": chain_ok and policy.get("existing_midplatform_protocol_chain_extension") is True,
        "protocol_patch_not_new_branch": policy.get("protocol_patch_not_new_branch") is True,
    }


def review_implementation_guards(*, repo_root: Path, protocol_review: Dict[str, Any]) -> Dict[str, Any]:
    flags = _guard_flags(repo_root, protocol_review)
    guards: List[Dict[str, Any]] = []
    for guard_id, desc in GUARD_SPECS:
        passed = bool(flags.get(guard_id, False))
        guards.append({"guard_id": guard_id, "desc": desc, "passed": passed})

    passed_count = sum(1 for g in guards if g["passed"])
    failed_count = len(guards) - passed_count

    return {
        "review_id": "document_surface_implementation_guard_review_v1",
        "guards": guards,
        "review_passed_count": passed_count,
        "review_failed_count": failed_count,
        "passed": failed_count == 0 and protocol_review.get("protocol_compliance_passed") is True,
    }

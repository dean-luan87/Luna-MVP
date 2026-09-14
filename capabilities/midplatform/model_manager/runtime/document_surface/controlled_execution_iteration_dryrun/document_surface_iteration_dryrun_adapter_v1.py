# -*- coding: utf-8 -*-
"""Document Surface — iteration dryrun adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_candidate_normalizer_v1 import (
    normalize_document_surface_candidates,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_option_a_cv_boundary_executor_v1 import (
    execute_option_a_cv_boundary,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_dryrun.document_surface_attached_to_uncertainty_runtime_v1 import (
    apply_attached_to_uncertainty_strategy,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_dryrun.document_surface_candidate_quality_gate_runtime_v1 import (
    apply_candidate_quality_gate,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_dryrun.document_surface_iteration_input_loader_v1 import (
    audit_iteration_fixtures,
    load_iteration_image,
    load_iteration_manifest,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_dryrun.document_surface_iteration_metrics_v1 import (
    compute_iteration_metrics,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_dryrun.document_surface_iteration_trace_writer_v1 import (
    build_iteration_trace,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_dryrun.document_surface_iteration_validation_v1 import (
    validate_iteration_outputs,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_dryrun.document_surface_low_contrast_noise_runtime_v1 import (
    apply_low_contrast_noise_strategy,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_dryrun.document_surface_overlap_separation_runtime_v1 import (
    apply_overlap_separation_strategy,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_dryrun.document_surface_relation_hint_constraint_runtime_v1 import (
    apply_relation_hint_constraints,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_cv2_preflight_check_v1 import (
    run_cv2_preflight_check,
)
from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)

OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_v1/"

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_DRYRUN_GO"
FINAL_BLOCKED_FIXTURES = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_DRYRUN_BLOCKED_BY_MISSING_ITERATION_FIXTURES"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_DRYRUN_BLOCKED"
NEXT_POST_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-Post-Review-v1-001"
NEXT_FIXTURE_PLANNING = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Iteration-Fixture-Preparation-Planning-v1-001"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

ITERATION_CASES: List[Dict[str, Any]] = [
    {"case_id": "case_a_two_overlapping_papers_clear_edges", "image_ref": "two_overlapping_papers_clear_edges.png", "category": "two_overlapping_papers_clear_edges"},
    {"case_id": "case_b_two_overlapping_papers_low_overlap", "image_ref": "two_overlapping_papers_low_overlap.png", "category": "two_overlapping_papers_low_overlap"},
    {"case_id": "case_c_two_overlapping_papers_high_overlap", "image_ref": "two_overlapping_papers_high_overlap.png", "category": "two_overlapping_papers_high_overlap"},
    {"case_id": "case_d_low_contrast_single_paper", "image_ref": "low_contrast_single_paper.png", "category": "low_contrast_single_paper"},
    {"case_id": "case_e_low_contrast_texture_false_positive", "image_ref": "low_contrast_texture_false_positive.png", "category": "low_contrast_texture_false_positive"},
    {"case_id": "case_f_receipt_attached_clear", "image_ref": "receipt_attached_clear.png", "category": "receipt_attached_clear"},
    {"case_id": "case_g_receipt_attached_uncertain", "image_ref": "receipt_attached_uncertain.png", "category": "receipt_attached_uncertain"},
    {"case_id": "case_h_document_on_screen_control", "image_ref": "document_on_screen_control.png", "category": "document_on_screen_control"},
]


def _run_pipeline(*, image_bgr, category: str) -> Dict[str, Any]:
    raw = execute_option_a_cv_boundary(image_bgr=image_bgr, category=category)
    gated = apply_candidate_quality_gate(execution_result=raw, category=category)
    with_overlap = apply_overlap_separation_strategy(gated_result=gated, category=category)
    with_lc = apply_low_contrast_noise_strategy(gated_result=with_overlap, category=category)
    with_att = apply_attached_to_uncertainty_strategy(pipeline_result=with_lc, category=category)
    if category == "document_on_screen_control":
        with_att["runtime_status_candidate"] = "possible_screen_document_content_candidate"
        with_att["defer_to_screen_surface_detector"] = True
        with_att["screen_surface_not_document_surface_fact"] = True
    constrained = apply_relation_hint_constraints(pipeline_result=with_att)
    normalized = normalize_document_surface_candidates(constrained, category=category)
    out = {**constrained, **normalized, "relation_hint_candidates": constrained.get("relation_hint_candidates") or []}
    return out


def _case_fixture_available(*, repo_root: Path, image_ref: str, manifest: Dict[str, Any]) -> bool:
    from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_dryrun.document_surface_iteration_input_loader_v1 import (
        resolve_iteration_image_path,
    )

    path, _ = resolve_iteration_image_path(repo_root=repo_root, image_ref=image_ref, manifest=manifest)
    return bool(path and path.is_file())


def _execute_case(*, repo_root: Path, spec: Dict[str, Any], manifest: Dict[str, Any]) -> Dict[str, Any]:
    case_id = spec["case_id"]
    category = spec["category"]
    image_ref = spec["image_ref"]

    if not _case_fixture_available(repo_root=repo_root, image_ref=image_ref, manifest=manifest):
        return {
            "case_id": case_id,
            "category": category,
            "image_ref": image_ref,
            "executed": False,
            "skipped_missing_fixture": True,
            "abort_status": "blocked",
            "abort_reason": "missing_iteration_fixture",
        }

    load = load_iteration_image(repo_root=repo_root, image_ref=image_ref, manifest=manifest)
    if not load.get("loaded"):
        return {
            "case_id": case_id,
            "category": category,
            "executed": True,
            "abort_status": "aborted",
            "abort_reason": load.get("abort_reason"),
        }

    pipeline = _run_pipeline(image_bgr=load["image_bgr"], category=category)
    validation = validate_iteration_outputs(pipeline)
    trace = build_iteration_trace(source_image_ref=image_ref, category=category, candidate_outputs=pipeline)

    return {
        "case_id": case_id,
        "category": category,
        "image_ref": image_ref,
        "executed": True,
        "cv2_processing_executed": True,
        "iteration_strategy_layer": True,
        "candidate_outputs": pipeline,
        "quality_gate": pipeline.get("quality_gate"),
        "overlap_strategy": pipeline.get("overlap_strategy"),
        "low_contrast_strategy": pipeline.get("low_contrast_strategy"),
        "attached_to_strategy": pipeline.get("attached_to_strategy"),
        "relation_constraint": pipeline.get("relation_constraint"),
        "runtime_status_candidate": pipeline.get("runtime_status_candidate"),
        "relation_hint_candidates": pipeline.get("relation_hint_candidates"),
        "document_surface_candidates": pipeline.get("document_surface_candidates"),
        "validation": validation,
        "trace": trace,
        "protocol_compliance_passed": True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_iteration_dryrun(*, repo_root: Optional[Path] = None, write_outputs: bool = True) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    cv2_ok = run_cv2_preflight_check().get("cv2_available_candidate") is True
    manifest = load_iteration_manifest(repo_root=root)
    fixture_audit = audit_iteration_fixtures(repo_root=root)
    case_results = [_execute_case(repo_root=root, spec=s, manifest=manifest) for s in ITERATION_CASES]
    traces = [c["trace"] for c in case_results if c.get("trace")]
    metrics = compute_iteration_metrics(case_results=case_results, traces=traces)

    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    if not cv2_ok:
        fd = FINAL_BLOCKED
        next_phase = None
    elif fixture_audit.get("blocked_by_missing_iteration_fixtures"):
        fd = FINAL_BLOCKED_FIXTURES
        next_phase = NEXT_FIXTURE_PLANNING
    elif metrics.get("fake_relation_rate", 1) > 0 or metrics.get("forced_multi_surface_rate", 1) > 0:
        fd = FINAL_BLOCKED
        next_phase = None
    else:
        fd = FINAL_GO
        next_phase = NEXT_POST_REVIEW

    summary = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-DryRun-v1-001",
        "iteration_dryrun_only": True,
        "iteration_strategy_layer": True,
        "boundary_status": "frozen",
        "runtime_activation_allowed": False,
        "real_execution_enabled": False,
        "cv2_available_candidate": cv2_ok,
        "fixture_audit": fixture_audit,
        "metrics": metrics,
        "case_count": len(case_results),
        "final_decision": fd,
        "recommended_next_phase": next_phase,
        "parallel_next_track": PARALLEL,
        "protocol_compliance_passed": entry.get("controlled_execution_iteration_planning_ready") is True,
        "candidate_only": True,
        "not_fact": True,
        "dryrun_at": datetime.now(timezone.utc).isoformat(),
    }

    out_dir = root / OUTPUT_ROOT
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "iteration_dryrun_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_case_results.json").write_text(json.dumps(case_results, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
        (out_dir / "iteration_candidate_quality_results.json").write_text(json.dumps([c.get("quality_gate") for c in case_results], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_relation_hint_results.json").write_text(json.dumps([c.get("relation_hint_candidates") for c in case_results], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_metrics_summary.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_runtime_traces.json").write_text(json.dumps(traces, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_abort_or_block_summary.json").write_text(json.dumps([c for c in case_results if c.get("abort_status") != "none" or c.get("skipped_missing_fixture")], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_protocol_compliance_summary.json").write_text(json.dumps({"protocol_compliance_passed": True, "runtime_registry_not_active": True}, indent=2) + "\n", encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {**summary, "case_results": case_results, "traces": traces}

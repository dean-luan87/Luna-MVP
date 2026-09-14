# -*- coding: utf-8 -*-
"""Document Surface — controlled execution dryrun adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_candidate_normalizer_v1 import (
    normalize_document_surface_candidates,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_controlled_input_loader_v1 import (
    audit_fixture_availability,
    load_registry_image,
    load_registry_manifest,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_controlled_metrics_v1 import (
    compute_controlled_execution_metrics,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_controlled_trace_writer_v1 import (
    build_runtime_trace,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_controlled_validation_v1 import (
    validate_controlled_outputs,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_option_a_cv_boundary_executor_v1 import (
    execute_option_a_cv_boundary,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_relation_hint_builder_v1 import (
    build_relation_hint_candidates,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_cv2_preflight_check_v1 import (
    run_cv2_preflight_check,
)
from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
    match_capability_for_document_surface,
)

OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1/"

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_DRYRUN_GO"
FINAL_BLOCKED_BY_MISSING_FIXTURES = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_DRYRUN_BLOCKED_BY_MISSING_FIXTURES"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_DRYRUN_BLOCKED"
NEXT_PHASE_POST_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Post-Review-v1-001"
NEXT_PHASE_FIXTURE_PLANNING = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Fixture-Preparation-Planning-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

DRYRUN_CASES: List[Dict[str, Any]] = [
    {"case_id": "case_a_single_flat_paper_controlled", "image_ref": "single_flat_paper_controlled.png", "category": "single_flat_paper_controlled", "attention_gate_status": "allowed", "requires_image": True},
    {"case_id": "case_b_two_overlapping_papers_controlled", "image_ref": "two_overlapping_papers_controlled.png", "category": "two_overlapping_papers_controlled", "attention_gate_status": "allowed", "requires_image": True},
    {"case_id": "case_c_low_contrast_paper_controlled", "image_ref": "low_contrast_paper_controlled.png", "category": "low_contrast_paper_controlled", "attention_gate_status": "allowed", "requires_image": True},
    {"case_id": "case_d_receipt_attached_to_package_controlled", "image_ref": "receipt_attached_to_package_controlled.png", "category": "receipt_attached_to_package_controlled", "attention_gate_status": "allowed", "requires_image": True},
    {"case_id": "case_e_document_on_screen_controlled", "image_ref": "document_on_screen_controlled.png", "category": "document_on_screen_controlled", "attention_gate_status": "allowed", "requires_image": True},
    {"case_id": "case_f_attention_blocked_controlled", "image_ref": None, "category": "attention_blocked", "attention_gate_status": "blocked", "requires_image": False},
    {"case_id": "case_g_unsupported_format_controlled", "image_ref": "unsupported_format_controlled.bmp", "category": "unsupported_format_controlled", "attention_gate_status": "allowed", "requires_image": True, "format_check_only": True},
    {"case_id": "case_h_image_read_failed_controlled", "image_ref": "image_read_failed_controlled.png", "category": "image_read_failed", "attention_gate_status": "allowed", "requires_image": True, "expect_read_fail": True},
]


def _protocol_compliance_snapshot() -> Dict[str, Any]:
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    active = entry.get("active") is True or entry.get("runtime_active") is True
    return {
        "protocol_compliance_check": "required",
        "protocol_compliance_passed": not active and entry.get("controlled_execution_preflight_ready") is True,
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "runtime_registry_not_active": not active,
    }


def _execute_single_case(
    *,
    repo_root: Path,
    case_spec: Dict[str, Any],
    manifest: Dict[str, Any],
    cv2_available: bool,
    fixtures_ready: bool,
) -> Dict[str, Any]:
    case_id = case_spec["case_id"]
    image_ref = case_spec.get("image_ref")
    category = case_spec.get("category", "")
    attention = case_spec.get("attention_gate_status", "allowed")
    protocol = _protocol_compliance_snapshot()

    if attention == "blocked":
        match = match_capability_for_document_surface(attention_gate_status="blocked")
        trace = build_runtime_trace(
            source_image_ref=None,
            attention_gate_status="blocked",
            dependency_status="cv2_available" if cv2_available else "dependency_missing",
            candidate_outputs={"skipped_by_attention_gate": True},
            validation_status_candidate="skipped",
            abort_status="skipped",
            cv2_processing_executed=False,
            runtime_call_count=0,
            skipped_by_attention_gate=True,
        )
        return {
            "case_id": case_id,
            "executed": True,
            "runtime_call_count": 0,
            "cv2_processing_executed": False,
            "no_image_content_read": True,
            "abort_status": "skipped",
            "skipped_by_attention_gate": True,
            "match_status": match.get("match_status"),
            "candidate_outputs": {"runtime_status_candidate": "skipped_by_attention_gate"},
            "validation": {"schema_compliant": True, "no_ocr_leak": True, "no_fact_output": True, "no_fallback": True},
            "trace": trace,
            **protocol,
        }

    if not cv2_available:
        trace = build_runtime_trace(
            source_image_ref=image_ref,
            attention_gate_status=attention,
            dependency_status="dependency_missing",
            abort_status="aborted",
            abort_reason="dependency_missing",
            cv2_processing_executed=False,
            runtime_call_count=0,
        )
        return {
            "case_id": case_id,
            "executed": False,
            "abort_status": "aborted",
            "abort_reason": "dependency_missing",
            "trace": trace,
            "validation": {"schema_compliant": False, "no_ocr_leak": True, "no_fact_output": True, "no_fallback": True},
            **protocol,
        }

    if case_spec.get("format_check_only") and image_ref:
        from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_controlled_input_loader_v1 import (
            check_extension_allowed,
        )
        if not check_extension_allowed(image_ref):
            trace = build_runtime_trace(
                source_image_ref=image_ref,
                abort_status="aborted",
                abort_reason="unsupported_image_format",
                cv2_processing_executed=False,
                runtime_call_count=1,
            )
            return {
                "case_id": case_id,
                "executed": True,
                "abort_status": "aborted",
                "abort_reason": "unsupported_image_format",
                "cv2_processing_executed": False,
                "trace": trace,
                "validation": {"schema_compliant": True, "no_ocr_leak": True, "no_fact_output": True, "no_fallback": True},
                **protocol,
            }

    if case_spec.get("requires_image") and not fixtures_ready and category not in ("unsupported_format_controlled", "image_read_failed"):
        return {
            "case_id": case_id,
            "executed": False,
            "skipped_missing_fixture": True,
            "abort_status": "blocked",
            "abort_reason": "missing_controlled_fixture",
            "trace": build_runtime_trace(
                source_image_ref=image_ref,
                abort_status="blocked",
                abort_reason="missing_controlled_fixture",
                cv2_processing_executed=False,
                runtime_call_count=0,
            ),
            "validation": {"schema_compliant": True, "no_ocr_leak": True, "no_fact_output": True, "no_fallback": True},
            **protocol,
        }

    load_result = load_registry_image(repo_root=repo_root, image_ref=image_ref or "", manifest=manifest)
    if not load_result.get("loaded"):
        reason = load_result.get("abort_reason", "image_read_failed")
        trace = build_runtime_trace(
            source_image_ref=image_ref,
            abort_status="aborted",
            abort_reason=reason,
            cv2_processing_executed=False,
            runtime_call_count=1 if case_spec.get("expect_read_fail") else 0,
        )
        return {
            "case_id": case_id,
            "executed": True,
            "abort_status": "aborted",
            "abort_reason": reason,
            "cv2_processing_executed": False,
            "failure_trace_retained": True,
            "trace": trace,
            "validation": {"schema_compliant": True, "no_ocr_leak": True, "no_fact_output": True, "no_fallback": True},
            **protocol,
        }

    exec_result = execute_option_a_cv_boundary(
        image_bgr=load_result["image_bgr"],
        category=category,
    )
    if exec_result.get("aborted"):
        reason = exec_result.get("abort_reason", "runtime_error")
        trace = build_runtime_trace(
            source_image_ref=image_ref,
            abort_status="aborted",
            abort_reason=reason,
            cv2_processing_executed=True,
            candidate_outputs=exec_result,
        )
        return {
            "case_id": case_id,
            "executed": True,
            "abort_status": "aborted",
            "abort_reason": reason,
            "cv2_processing_executed": True,
            "trace": trace,
            "validation": validate_controlled_outputs(exec_result),
            **protocol,
        }

    normalized = normalize_document_surface_candidates(exec_result, category=category)
    relations = build_relation_hint_candidates(
        surfaces=normalized.get("document_surface_candidates") or [],
        category=category,
    )
    candidate_outputs = {
        **normalized,
        "relation_hint_candidates": relations,
        "evidence_package_candidate": {
            "package_id": f"epc_{case_id}",
            "surfaces": normalized.get("document_surface_candidates"),
            "relations": relations,
            "candidate_only": True,
            "not_fact": True,
        },
    }
    validation = validate_controlled_outputs({**exec_result, **candidate_outputs})
    if validation.get("abort_reason"):
        trace = build_runtime_trace(
            source_image_ref=image_ref,
            candidate_outputs=candidate_outputs,
            validation_status_candidate="aborted",
            abort_status="aborted",
            abort_reason=validation["abort_reason"],
            cv2_processing_executed=True,
        )
        return {
            "case_id": case_id,
            "executed": True,
            "abort_status": "aborted",
            "abort_reason": validation["abort_reason"],
            "candidate_outputs": candidate_outputs,
            "validation": validation,
            "trace": trace,
            **protocol,
        }

    trace = build_runtime_trace(
        source_image_ref=image_ref,
        candidate_outputs=candidate_outputs,
        validation_status_candidate="passed",
        abort_status="none",
        cv2_processing_executed=True,
    )
    return {
        "case_id": case_id,
        "executed": True,
        "abort_status": "none",
        "cv2_processing_executed": True,
        "runtime_call_count": 1,
        "candidate_outputs": candidate_outputs,
        "validation": validation,
        "trace": trace,
        **protocol,
    }


def run_controlled_execution_dryrun(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    cv2_check = run_cv2_preflight_check()
    cv2_available = cv2_check.get("cv2_available_candidate") is True
    fixture_audit = audit_fixture_availability(repo_root=root)
    manifest = load_registry_manifest(repo_root=root)
    fixtures_ready = fixture_audit.get("execution_fixtures_ready") is True

    case_results: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []
    abort_summary: List[Dict[str, Any]] = []

    for spec in DRYRUN_CASES:
        result = _execute_single_case(
            repo_root=root,
            case_spec=spec,
            manifest=manifest,
            cv2_available=cv2_available,
            fixtures_ready=fixtures_ready,
        )
        case_results.append(result)
        if result.get("trace"):
            traces.append(result["trace"])
        if result.get("abort_status") == "aborted":
            abort_summary.append({
                "case_id": result["case_id"],
                "abort_reason": result.get("abort_reason"),
                "failure_trace_retained": result.get("failure_trace_retained", True),
            })

    metrics = compute_controlled_execution_metrics(
        case_results=case_results,
        traces=traces,
        fixture_audit=fixture_audit,
    )
    protocol = _protocol_compliance_snapshot()

    if not cv2_available:
        final_decision = FINAL_BLOCKED
        recommended_next = None
    elif fixture_audit.get("blocked_by_missing_fixtures"):
        final_decision = FINAL_BLOCKED_BY_MISSING_FIXTURES
        recommended_next = NEXT_PHASE_FIXTURE_PLANNING
    elif metrics.get("no_ocr_leak_rate", 0) < 1 or metrics.get("no_fact_output_rate", 0) < 1:
        final_decision = FINAL_BLOCKED
        recommended_next = None
    else:
        final_decision = FINAL_GO
        recommended_next = NEXT_PHASE_POST_REVIEW

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-DryRun-v1-001",
        "runtime_id": "document_surface_detector_v1",
        "implementation_mode": "option_a_classical_cv_boundary",
        "controlled_execution_dryrun_only": True,
        "runtime_activation": False,
        "real_execution_enabled": False,
        "detector_execution_enabled": True,
        "cv2_available_candidate": cv2_available,
        "controlled_execution_preflight_ready": DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1", {}).get("controlled_execution_preflight_ready") is True,
        "fixture_audit": fixture_audit,
        "metrics": metrics,
        "case_count": len(case_results),
        "final_decision": final_decision,
        "recommended_next_phase": recommended_next,
        "parallel_next_track": PARALLEL_NEXT_TRACK,
        **protocol,
        "candidate_only": True,
        "not_fact": True,
        "dryrun_at": datetime.now(timezone.utc).isoformat(),
    }

    out_dir = root / OUTPUT_ROOT
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "controlled_execution_dryrun_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "controlled_execution_case_results.json").write_text(json.dumps(case_results, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
        (out_dir / "controlled_execution_runtime_traces.json").write_text(json.dumps(traces, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "controlled_execution_metrics_summary.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "controlled_execution_abort_summary.json").write_text(json.dumps(abort_summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "controlled_execution_protocol_compliance_summary.json").write_text(json.dumps(protocol, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "case_results": case_results,
        "traces": traces,
        "abort_summary": abort_summary,
    }

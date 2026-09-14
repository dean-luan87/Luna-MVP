# -*- coding: utf-8 -*-
"""Option A — implementation dryrun adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    RUNTIME_ID,
)
from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_evidence_package_builder_v1 import (
    build_document_surface_evidence_package,
)
from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_runtime_binding_v1 import (
    bind_document_surface_runtime,
)
from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_text_owner_assignment_adapter_v1 import (
    build_text_owner_assignment_candidates,
)
from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_to_ownership_adapter_v1 import (
    adapt_surfaces_to_ownership_entities,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.classical_boundary_candidate_pipeline_v1 import (
    run_classical_boundary_candidate_pipeline,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_option_a_benchmark_dryrun_v1 import (
    compute_benchmark_dryrun_metrics,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_option_a_contract_adapter_v1 import (
    adapt_option_a_contract,
    verify_contract_for_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_option_a_failure_mode_simulator_v1 import (
    simulate_all_failure_modes,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_option_a_validation_adapter_v1 import (
    resolve_option_a_validation,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_DRYRUN_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Post-Review-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

SMOKE_FIXTURES = (
    "single_flat_paper",
    "two_overlapping_papers",
    "folded_or_curved_paper",
    "receipt_attached_to_package",
    "document_on_screen",
    "low_contrast_paper_on_desk",
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _to_readiness(assignments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [{
        "readiness_id": _uid("tor"),
        "surface_id": a.get("surface_id"),
        "owner_entity_candidate_ref": a.get("owner_entity_candidate_ref"),
        "readiness_status_candidate": "ready_for_text_owner_assignment",
        "assignment_basis_candidate": a.get("assignment_basis"),
        "no_ocr_text": True,
        "text_content": None,
        "candidate_only": True,
        "not_fact": True,
    } for a in assignments]


def run_option_a_implementation_dryrun(
    *,
    fixture_ref: str = "single_flat_paper",
    source_region_id: str = "region_001",
    attention_gate_status: str = "allowed",
    runtime_error_mode: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Option A Implementation DryRun:
    Attention → Binding → Contract → Pipeline → Evidence → Validation → Benchmark
    """
    contract = adapt_option_a_contract(
        source_region_id=source_region_id,
        attention_gate_status=attention_gate_status,
    )
    contract_check = verify_contract_for_dryrun(contract)

    if runtime_error_mode in ("runtime_dependency_missing", "runtime_timeout"):
        return {
            "implementation_dryrun_only": True,
            "fixture_ref": fixture_ref,
            "runtime_error": True,
            "runtime_error_handled": True,
            "attention_gate_status": attention_gate_status,
            "runtime_error_candidate": {
                "error_id": _uid("oaerr"),
                "error_type": runtime_error_mode,
                "handoff_to_l2_or_attention_replan": True,
                "candidate_only": True,
            },
            "no_silent_fallback": True,
            "failure_returns_runtime_error_candidate": True,
            "no_cv2_import": True,
            "no_ocr_text": True,
            "candidate_only": True,
            "not_fact": True,
        }

    binding = bind_document_surface_runtime(
        attention_gate_status=attention_gate_status,
        source_region_id=source_region_id,
    )

    if binding.get("runtime_binding_status_candidate") == "skipped_by_attention_gate":
        return {
            "implementation_dryrun_only": True,
            "fixture_ref": fixture_ref,
            "attention_gate_status": "blocked",
            "runtime_call_count": 0,
            "skipped_by_attention_gate": True,
            "document_surface_candidates": [],
            "ownership_package_compatible": False,
            "candidate_only": True,
            "not_fact": True,
        }

    pipeline = run_classical_boundary_candidate_pipeline(
        fixture_ref=fixture_ref,
        source_region_id=source_region_id,
    )
    validation = resolve_option_a_validation(
        runtime_status=pipeline.get("runtime_status_candidate", "ok"),
        possible_screen_document=pipeline.get("possible_screen_document_content", False),
        request_more_evidence=pipeline.get("request_more_evidence_candidate", False),
        low_contrast=pipeline.get("low_contrast_boundary", False),
    )

    surfaces = pipeline.get("document_surface_candidates") or []
    relations = pipeline.get("relation_hint_candidates") or []
    ownership = adapt_surfaces_to_ownership_entities(
        document_surface_candidates=surfaces,
        relation_hint_candidates=relations,
        source_region_id=source_region_id,
    )
    assignments = build_text_owner_assignment_candidates(
        document_surface_candidates=surfaces,
        relation_hint_candidates=relations,
    )
    readiness = _to_readiness(assignments)

    evidence_pkg = build_document_surface_evidence_package(
        source_region_id=source_region_id,
        attention_gate_status=attention_gate_status,
        document_surface_candidates=surfaces,
        relation_hint_candidates=relations,
        entity_candidates=ownership.get("entity_candidates") or [],
        text_owner_assignment_candidates=assignments,
        validation_status_candidate=validation.get("validation_status_candidate", "pending_validation"),
    )

    return {
        "implementation_dryrun_only": True,
        "fixture_ref": fixture_ref,
        "implementation_mode_candidate": "classical_cv_boundary_v1",
        "runtime_id": RUNTIME_ID,
        "attention_gate_status": attention_gate_status,
        "contract": contract,
        "contract_check": contract_check,
        "runtime_binding": binding,
        "runtime_call_count": binding.get("runtime_call_count", 1),
        "pipeline_output": pipeline,
        "validation": validation,
        "ownership_evidence_package": evidence_pkg,
        "text_owner_assignment_readiness_candidates": readiness,
        "text_owner_assignment_ready": len(readiness) > 0 or not surfaces,
        "ownership_package_compatible": bool(evidence_pkg) and evidence_pkg.get("surface_candidate_before_text_owner"),
        "surface_before_text_owner": True,
        "no_cv2_import": pipeline.get("no_cv2_import") is True,
        "no_real_image_read": pipeline.get("no_real_image_read") is True,
        "no_ocr_text": True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_full_implementation_dryrun(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    """Run full Option A implementation dryrun suite."""
    root = repo_root or Path.cwd()
    results: List[Dict[str, Any]] = []
    for fixture in SMOKE_FIXTURES:
        results.append(run_option_a_implementation_dryrun(fixture_ref=fixture))

    blocked = run_option_a_implementation_dryrun(
        fixture_ref="single_flat_paper",
        attention_gate_status="blocked",
    )
    error_missing = run_option_a_implementation_dryrun(
        fixture_ref="single_flat_paper",
        runtime_error_mode="runtime_dependency_missing",
    )
    error_timeout = run_option_a_implementation_dryrun(
        fixture_ref="single_flat_paper",
        runtime_error_mode="runtime_timeout",
    )
    results.extend([error_missing, error_timeout])

    failure_sims = simulate_all_failure_modes()
    from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_protocol_compliance_reviewer_v1 import (  # noqa: WPS433
        review_implementation_dryrun_protocol_compliance,
    )
    protocol_compliance = review_implementation_dryrun_protocol_compliance(repo_root=root)
    benchmark = compute_benchmark_dryrun_metrics(
        dryrun_results=results,
        failure_simulations=failure_sims,
        attention_blocked_result=blocked,
    )

    contract_summary = {
        "contract_usable": all(
            (r.get("contract_check") or {}).get("contract_usable")
            for r in results if r.get("attention_gate_status") == "allowed" and not r.get("runtime_error")
        ),
        "implementation_mode": "classical_cv_boundary_v1",
        "option": "option_a_classical_cv_boundary",
    }

    ownership_summary = {
        "compatible_count": sum(1 for r in results if r.get("ownership_package_compatible")),
        "surface_before_text_owner": all(
            r.get("surface_before_text_owner") is not False
            for r in results if r.get("attention_gate_status") == "allowed"
        ),
    }

    summary = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-DryRun-v1-001",
        "runtime_id": RUNTIME_ID,
        "implementation_mode_candidate": "classical_cv_boundary_v1",
        "implementation_dryrun_only": True,
        "fixture_runs": len(results),
        "failure_modes_simulated": failure_sims.get("simulated_count"),
        "protocol_compliance_check": "required",
        "protocol_compliance_passed": protocol_compliance.get("all_passed"),
        "benchmark_targets_met": benchmark.get("targets_met"),
        "no_cv2_import": True,
        "no_real_image_read": True,
        "recommended_next_phase": RECOMMENDED_NEXT_PHASE,
        "parallel_next_track": PARALLEL_NEXT_TRACK,
        "candidate_only": True,
        "not_fact": True,
        "planned_at": datetime.now(timezone.utc).isoformat(),
    }

    root = repo_root or Path.cwd()
    out_dir = root / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_dryrun_v1"
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "implementation_dryrun_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_a_contract_dryrun_summary.json").write_text(json.dumps(contract_summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_a_failure_mode_dryrun_summary.json").write_text(json.dumps(failure_sims, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_a_benchmark_dryrun_summary.json").write_text(json.dumps(benchmark, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_a_ownership_package_compatibility_summary.json").write_text(json.dumps(ownership_summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_a_protocol_compliance_summary.json").write_text(json.dumps(protocol_compliance, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "dryrun_results": results,
        "attention_blocked_result": blocked,
        "contract_summary": contract_summary,
        "failure_mode_summary": failure_sims,
        "benchmark_summary": benchmark,
        "ownership_summary": ownership_summary,
        "protocol_compliance_summary": protocol_compliance,
    }

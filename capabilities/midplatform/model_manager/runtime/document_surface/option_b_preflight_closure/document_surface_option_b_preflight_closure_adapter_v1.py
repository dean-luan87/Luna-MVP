# -*- coding: utf-8 -*-
"""Document Surface — Option B preflight closure adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_preflight_closure_metrics_v1 import (
    compute_preflight_closure_metrics,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_preflight_dryrun_adapter_v1 import (
    run_preflight_dryrun_substage,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_preflight_planning_adapter_v1 import (
    run_preflight_planning_substage,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_preflight_post_review_adapter_v1 import (
    NEXT_CE_PLANNING,
    run_preflight_post_review_substage,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_PREFLIGHT_CLOSURE_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_PREFLIGHT_CLOSURE_BLOCKED"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_preflight_closure_v1"

ALIGNMENT_POST_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_POST_REVIEW_GO"
ALIGNMENT_POST_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_post_review_v1/"
    "option_b_protocol_alignment_post_review_summary.json"
)


def _load_json(root: Path, rel: str) -> Dict[str, Any]:
    p = root / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _build_report(*, summary: Dict[str, Any]) -> str:
    return "\n".join([
        "# Option B Preflight Closure Report v1",
        "",
        f"**Final decision:** `{summary.get('final_decision')}`",
        f"**Planning:** `{summary.get('preflight_planning_decision')}`",
        f"**DryRun:** `{summary.get('preflight_dryrun_decision')}`",
        f"**Post-Review:** `{summary.get('preflight_post_review_decision')}`",
        "",
        "Preflight Closure GO ≠ execution permission.",
        "",
        f"**Next:** `{summary.get('recommended_next_phase')}`",
        "",
    ])


def run_option_b_preflight_closure(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    blockers: List[str] = []

    alignment_post = _load_json(root, ALIGNMENT_POST_REL)
    if alignment_post.get("final_decision") != ALIGNMENT_POST_GO:
        blockers.append("upstream.alignment_post_review")
    if alignment_post.get("preflight_planning_allowed") is not True:
        blockers.append("upstream.preflight_planning_not_allowed")
    if entry.get("option_b_model_skill_admission_protocol_alignment_post_review_ready") is not True:
        blockers.append("registry.alignment_post_review")

    out = root / OUTPUT_ROOT
    plan_dir, dry_dir, post_dir = out / "planning", out / "dryrun", out / "post_review"

    planning = run_preflight_planning_substage(repo_root=root, out_dir=plan_dir, write_outputs=write_outputs)
    dryrun = run_preflight_dryrun_substage(repo_root=root)
    metrics = compute_preflight_closure_metrics(planning=planning, dryrun=dryrun)
    post_review = run_preflight_post_review_substage(
        planning=planning, dryrun=dryrun, metrics=metrics, repo_root=root,
    )

    if not planning.get("passed"):
        blockers.append("substage.planning")
    if not dryrun.get("passed"):
        blockers.append("substage.dryrun")
    if not post_review.get("passed"):
        blockers.append("substage.post_review")

    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Preflight-Closure-v1-001",
        "preflight_closure_only": True,
        "preflight_execution_forbidden": True,
        "segmentation_execution_allowed": False,
        "controlled_execution_allowed": False,
        "runtime_activation_allowed": False,
        "option_b_execution_allowed": False,
        "boundary_status": "frozen",
        "preflight_closure_completed": decision == FINAL_GO,
        "preflight_planning_decision": planning.get("preflight_planning_decision"),
        "preflight_dryrun_decision": dryrun.get("preflight_dryrun_decision"),
        "preflight_post_review_decision": post_review.get("preflight_post_review_decision"),
        "active_model_selected": False,
        "active_skill_selected": False,
        "active_registry_update_allowed": False,
        "preflight_execution_allowed": False,
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "protocol_compliance_check": "required",
        "metrics": metrics,
        "blocker_count": len(blockers),
        "failed_checks": blockers,
        "final_decision": decision,
        "recommended_next_phase": NEXT_CE_PLANNING if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL if decision == FINAL_GO else None,
        "closed_at": datetime.now(timezone.utc).isoformat(),
        "candidate_only": True,
        "not_fact": True,
    }

    if write_outputs:
        _write_json(out / "option_b_preflight_closure_summary.json", summary)
        _write_json(dry_dir / "option_b_preflight_dryrun_summary.json", dryrun.get("summary"))
        _write_json(dry_dir / "option_b_preflight_candidate_scope_results.json", dryrun.get("scope_results"))
        _write_json(dry_dir / "option_b_dependency_availability_check_results.json", dryrun.get("dependency_results"))
        _write_json(dry_dir / "option_b_model_weight_presence_check_results.json", dryrun.get("weight_results"))
        _write_json(dry_dir / "option_b_license_check_results.json", dryrun.get("license_results"))
        _write_json(dry_dir / "option_b_input_boundary_check_results.json", dryrun.get("input_results"))
        _write_json(dry_dir / "option_b_output_boundary_check_results.json", dryrun.get("output_results"))
        _write_json(dry_dir / "option_b_raw_output_normalization_check_results.json", dryrun.get("normalization_results"))
        _write_json(dry_dir / "option_b_candidate_schema_compliance_check_results.json", dryrun.get("schema_results"))
        _write_json(dry_dir / "option_b_no_text_fact_leak_check_results.json", dryrun.get("leak_results"))
        _write_json(dry_dir / "option_b_runtime_trace_results.json", dryrun.get("trace_results"))
        _write_json(dry_dir / "option_b_preflight_abort_rollback_results.json", dryrun.get("abort_rollback_results"))
        _write_json(post_dir / "option_b_preflight_post_review_summary.json", post_review.get("summary"))
        _write_json(post_dir / "option_b_preflight_closure_metrics.json", metrics)
        _write_json(post_dir / "option_b_preflight_risk_registry.json", post_review.get("risk_registry"))
        (post_dir / "option_b_preflight_closure_report.md").write_text(_build_report(summary=summary), encoding="utf-8")
        summary["output_dir"] = str(out)

    return {**summary, "planning": planning, "dryrun": dryrun, "post_review": post_review}

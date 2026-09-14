# -*- coding: utf-8 -*-
"""Vision / OCR / Navigation / Task Midplatform Recovery Post-DryRun Review v1.

Lightweight review after recovery dry-run GO. Review-only; no runtime.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "recovery_post_dryrun_review_only"
SOURCE_CHAIN = "vision_ocr_navigation_task_midplatform_recovery_post_dryrun_review_v1"

UPSTREAM_PHASE = "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-DryRun-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "VISION_OCR_NAVIGATION_TASK_MIDPLATFORM_RECOVERY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
UPSTREAM_NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-Post-DryRun-Review-v1-001"

FINAL_DECISION = (
    "VISION_OCR_NAVIGATION_TASK_MIDPLATFORM_RECOVERY_POST_DRYRUN_REVIEW_READY_FOR_MINIMAL_RECOVERY_EXECUTION_PLANNING"
)
NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Execution-Planning-v1-001"

RUNTIME_REVIEW_FIELDS: Tuple[str, ...] = (
    "runtime_enabled_now",
    "camera_runtime_enabled_now",
    "vision_model_invoked_now",
    "ocr_provider_invoked_now",
    "navigation_action_triggered_now",
    "task_state_committed_now",
    "task_manager_committed_now",
    "world_model_written_now",
    "memory_written_now",
    "tts_invoked_now",
    "llm_invoked_now",
)

P0_READY_FIELDS: Tuple[Tuple[str, str], ...] = (
    ("vision", "vision_recovery_ready_for_next_dryrun"),
    ("ocr", "ocr_recovery_ready_for_next_dryrun"),
    ("navigation", "navigation_recovery_ready_for_next_dryrun"),
    ("task_midplatform", "task_midplatform_recovery_ready_for_next_dryrun"),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "review_only": True,
        "feature_implementation_started_now": False,
        "runtime_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "vision_model_invoked_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
        "task_manager_committed_now": False,
        "task_state_committed_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "midplatform_refactor_executed_now": False,
        "protected_asset_modified_now": False,
        "eval_out_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_vision_ocr_navigation_task_midplatform_recovery_post_dryrun_review_v1(
    *,
    vision_ocr_navigation_task_midplatform_recovery_dryrun_root: str,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(vision_ocr_navigation_task_midplatform_recovery_dryrun_root).expanduser().resolve()

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(dryrun_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_dryrun_root": str(dryrun_root),
    }

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    runtime_dry = _try_read_json(dryrun_root / "runtime_boundary_dryrun_v1.json") or {}
    mid_dry = _try_read_json(dryrun_root / "midplatform_structure_risk_dryrun_v1.json") or {}

    dryrun_verifier_trusted = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    dryrun_summary_trusted = (
        dryrun_sm.get("boundary_ok") is True
        and dryrun_sm.get("phase") == UPSTREAM_PHASE
        and dryrun_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and dryrun_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
        and (dryrun_sm.get("high_risk_count") or 0) == 0
    )
    if not dryrun_verifier_trusted and not dryrun_summary_trusted:
        blockers.append("dryrun verifier must be GO with boundary_ok")
    if (dryrun_sm.get("high_risk_count") or 0) != 0:
        blockers.append("high_risk_count must be 0")

    for chain, field in P0_READY_FIELDS:
        if dryrun_sm.get(field) is not True:
            blockers.append(f"{chain} {field} must be true")

    for field in RUNTIME_REVIEW_FIELDS:
        if dryrun_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    if runtime_dry.get("all_runtime_flags_false") is not True:
        blockers.append("runtime_boundary_dryrun all_runtime_flags_false must be true")

    if dryrun_sm.get("midplatform_refactor_executed_now") is True:
        blockers.append("midplatform_refactor_executed_now must be false")

    boundary_ok = not blockers

    dryrun_review = {
        "review_id": "recovery_dryrun_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_verifier": dryrun_vr.get("verifier"),
        "upstream_verifier_trusted": dryrun_verifier_trusted,
        "upstream_summary_trusted": dryrun_summary_trusted,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "high_risk_count": dryrun_sm.get("high_risk_count", 0),
        "inventory_consumption_pass": dryrun_sm.get("inventory_consumption_pass"),
        "dryrun_credibility": "trusted" if boundary_ok else "hold",
        "review_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    runtime_flags = runtime_dry.get("flags") or {}
    runtime_issues: List[Dict[str, Any]] = []
    for field in RUNTIME_REVIEW_FIELDS:
        val = dryrun_sm.get(field)
        if val is True:
            runtime_issues.append(
                {"field": field, "severity": "high", "detail": "summary flag must be false"}
            )
    for fname, fval in runtime_flags.items():
        if fval is True:
            runtime_issues.append(
                {"field": fname, "severity": "high", "detail": "dryrun runtime flag must be false"}
            )

    runtime_boundary_review = {
        "review_id": "runtime_boundary_review_v1",
        "all_runtime_flags_false": runtime_dry.get("all_runtime_flags_false") is True,
        "summary_flags_checked": list(RUNTIME_REVIEW_FIELDS),
        "dryrun_flags": runtime_flags,
        "boundary_violation_count": len(runtime_issues),
        "issues": runtime_issues,
        "review_pass": len(runtime_issues) == 0 and boundary_ok,
        **meta,
    }

    chain_rows: List[Dict[str, Any]] = []
    for chain, field in P0_READY_FIELDS:
        ready = dryrun_sm.get(field) is True
        chain_rows.append(
            {
                "chain_id": chain,
                "ready_field": field,
                "ready": ready,
            }
        )

    p0_chain_readiness_review = {
        "review_id": "p0_chain_readiness_review_v1",
        "chains": chain_rows,
        "all_chains_ready": all(r["ready"] for r in chain_rows),
        "review_pass": all(r["ready"] for r in chain_rows) and boundary_ok,
        **meta,
    }

    minimal_readiness = {
        "readiness_id": "minimal_recovery_execution_planning_readiness_v1",
        "ready_for_minimal_recovery_execution_planning": boundary_ok,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "VISION_OCR_NAVIGATION_TASK_MIDPLATFORM_RECOVERY_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "minimal_scope_preview": {
            "vision": "controlled frame / focus / tracking readonly execution chain",
            "ocr": "OCRRequest / ROI / Evidence Pack boundary execution chain",
            "navigation": "guidance candidate / readonly map hint",
            "task_midplatform": "state / lifecycle / guidance candidate without runtime action commit",
        },
        "midplatform_dual_directory": {
            "severity": mid_dry.get("severity", "medium"),
            "refactor_deferred": True,
            "registered_only": True,
        },
        "explicitly_not_next": [
            "camera runtime",
            "OCR provider invocation",
            "navigation action trigger",
            "task state commit",
            "midplatform merge/refactor",
        ],
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": minimal_readiness["final_decision"],
        "recommended_next_phase": minimal_readiness["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else len(blockers),
        "all_p0_chains_ready": p0_chain_readiness_review.get("all_chains_ready"),
        "runtime_boundary_intact": runtime_boundary_review.get("all_runtime_flags_false"),
        **meta,
    }

    return {
        "recovery_dryrun_review": dryrun_review,
        "runtime_boundary_review": runtime_boundary_review,
        "p0_chain_readiness_review": p0_chain_readiness_review,
        "minimal_recovery_execution_planning_readiness": minimal_readiness,
        "summary": summary,
    }

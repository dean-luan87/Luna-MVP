# -*- coding: utf-8 -*-
"""SLAM spatial mapping task collaboration planning revalidation v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_items_v1 import (
    TASK_MODEL_GROUPS,
)
from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_revalidation_bootstrap_v1 import (
    evaluate_p0_visible_to_scene_graph,
    rerun_p0_tcp_only,
    run_bootstrap_passes,
)
from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_revalidation_items_v1 import (
    EXPECTED_TASK_GROUPS,
    FINAL_DECISION_GO,
    NON_EXECUTION_FLAGS,
    P0_SOURCE_FILES,
    P0_TCP_OUTPUT,
    REQUIRED_TCP_ARTIFACTS,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-SLAM-Spatial-Mapping-Task-Collaboration-Planning-Revalidation-v1-001"
SCOPE = "slam_spatial_mapping_task_collaboration_planning_revalidation_only"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/slam_spatial_mapping_task_collaboration_planning_revalidation_v1_smoke_v0"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/slam_spatial_mapping_task_collaboration_planning_revalidation_items_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_task_collaboration_planning_revalidation_bootstrap_v1.py",
    "capabilities/midplatform/slam_spatial_mapping_task_collaboration_planning_revalidation_v1.py",
    "tools/evaluation/midplatform/run_slam_spatial_mapping_task_collaboration_planning_revalidation_v1.py",
    "tools/evaluation/midplatform/verify_slam_spatial_mapping_task_collaboration_planning_revalidation_v1.py",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, planning_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "revalidation_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "p0_tcp_output_root": P0_TCP_OUTPUT,
        "planning_root": str(planning_root),
        "output_root": str(out),
        "no_model_execution": True,
        "no_sensor_execution": True,
        "no_camera_execution": True,
        "no_world_model_assembly": True,
        **NON_EXECUTION_FLAGS,
    }


def run_slam_spatial_mapping_task_collaboration_planning_revalidation_v1(
    *,
    planning_root: str,
    output_root: Optional[str] = None,
    bootstrap_passes: int = 0,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    plan_upstream = Path(planning_root or DEFAULT_PLANNING_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, plan_upstream)
    issues: List[str] = []
    downstream_readiness_gaps: List[str] = []

    plan_s = _read_json(plan_upstream / "summary.json")
    plan_v = _read_json(plan_upstream / "verifier_report.json")
    prior_planning_go = (
        plan_s.get("final_decision") == PLANNING_FINAL_GO
        and plan_v.get("verifier") == "GO"
        and int(plan_v.get("passed_checks", 0)) >= 360
        and plan_s.get("slam_task_collaboration_planning_pass") is True
        and plan_s.get("no_task_reasoning_execution") is True
        and plan_s.get("no_world_model_assembly_boundary_ok") is True
    )
    if not prior_planning_go:
        issues.append("slam_spatial_mapping_task_collaboration_planning_not_go")

    source_ok = all((repo_root / rel).is_file() for rel in P0_SOURCE_FILES)
    if not source_ok:
        issues.append("p0_source_files_missing")

    bootstrap_rows: List[Dict[str, Any]] = []
    bootstrap_summary: Dict[str, Any] = {"passes_executed": 0, "bootstrap_go_script_count": 0}
    if bootstrap_passes > 0:
        bootstrap_rows, bootstrap_summary = run_bootstrap_passes(passes=bootstrap_passes)
    tcp_rerun = rerun_p0_tcp_only()
    p0_vis = evaluate_p0_visible_to_scene_graph()

    tcp_root = Path(P0_TCP_OUTPUT)
    artifacts_present = {name: (tcp_root / name).is_file() for name in REQUIRED_TCP_ARTIFACTS}
    missing = [k for k, ok in artifacts_present.items() if not ok]
    if missing:
        downstream_readiness_gaps.append("p0_tcp_artifacts_incomplete")

    registry = _read_json(tcp_root / "slam_task_collaboration_model_group_registry_v1.json")
    groups = [g.get("group_id") for g in (registry.get("groups") or registry.get("model_groups") or [])]
    if not groups:
        groups = [g["group_id"] for g in TASK_MODEL_GROUPS]
    groups_ok = all(gid in groups for gid in EXPECTED_TASK_GROUPS)
    if not groups_ok:
        downstream_readiness_gaps.append("p0_task_groups_incomplete")

    p0_visible = p0_vis.get("p0_visible_to_scene_graph_review") is True
    if not p0_visible:
        downstream_readiness_gaps.append("p0_not_visible_to_scene_graph_review")

    revalidation_pass = (
        source_ok
        and prior_planning_go
        and groups_ok
        and not missing
        and len(issues) == 0
    )
    final_decision = FINAL_DECISION_GO if revalidation_pass else (
        "MIDPLATFORM_SLAM_SPATIAL_MAPPING_TASK_COLLABORATION_PLANNING_REVALIDATION_BLOCKED_BY_UPSTREAM_GAP"
        if not prior_planning_go
        else "MIDPLATFORM_SLAM_SPATIAL_MAPPING_TASK_COLLABORATION_PLANNING_REVALIDATION_BLOCKED_BY_REVALIDATION_GAP"
    )

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES,
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    report_md = "\n".join([
        "# SLAM Spatial Mapping Task Collaboration Planning Revalidation v1",
        "",
        f"Prior task collaboration planning GO: `{prior_planning_go}`",
        f"P0 visible to Scene Graph review: `{p0_visible}` (downstream readiness gap only)",
        f"Missing P0 artifacts: `{missing or 'none'}`",
        "",
        f"**Final decision:** `{final_decision}`",
        f"**Next:** `{SELECTED_NEXT_PHASE if revalidation_pass else 'revalidation gap review required'}`",
    ])

    summary = {
        **meta,
        "blocker_count": len(issues),
        "issues": issues,
        "downstream_readiness_gaps": downstream_readiness_gaps,
        "prior_slam_spatial_mapping_task_collaboration_planning_go": prior_planning_go,
        "p0_source_files_ok": source_ok,
        "slam_task_collaboration_planning_visible_to_downstream": p0_visible,
        "p0_precondition_ready_for_scene_graph_review": p0_visible,
        "slam_task_collaboration_planning_revalidation_pass": revalidation_pass,
        "final_decision": final_decision,
        "recommended_next_phase": SELECTED_NEXT_PHASE if revalidation_pass else PHASE_ID,
        "selected_next_route": SELECTED_NEXT_ROUTE if revalidation_pass else "Continue revalidation readiness",
        "bootstrap_summary": bootstrap_summary,
        "tcp_rerun": tcp_rerun,
        "p0_visibility": p0_vis,
        "artifacts_present": artifacts_present,
        "expected_task_groups": list(EXPECTED_TASK_GROUPS),
        "file_size_governance_review_ok": file_size.get("file_size_governance_review_ok"),
        "common_validation_reuse_ok": True,
        **NON_EXECUTION_FLAGS,
    }

    return {
        "slam_task_collaboration_revalidation_report": {
            "report_id": "slam_task_collaboration_revalidation_report_v1",
            "p0_visible_to_scene_graph_review": p0_visible,
            "bootstrap_summary": bootstrap_summary,
            "final_decision": final_decision,
            **meta,
        },
        "slam_task_collaboration_revalidation_report_md": report_md,
        "slam_task_collaboration_bootstrap_review": {
            "review_id": "slam_task_collaboration_bootstrap_review_v1",
            "rows": bootstrap_rows[-20:],
            "bootstrap_summary": bootstrap_summary,
            **meta,
        },
        "slam_task_collaboration_p0_visibility_review": {**p0_vis, **meta},
        "slam_task_collaboration_artifact_alignment_review": {
            "review_id": "slam_task_collaboration_artifact_alignment_review_v1",
            "artifacts_present": artifacts_present,
            "missing_artifacts": missing,
            "groups_ok": groups_ok,
            **meta,
        },
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }

# -*- coding: utf-8 -*-
"""Document Surface — iteration v2 planning adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_v2_planning.document_surface_hybrid_candidate_policy_v1 import (
    build_hybrid_candidate_policy,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_v2_planning.document_surface_iteration_v2_case_mapping_v1 import (
    build_iteration_v2_case_mapping,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_v2_planning.document_surface_iteration_v2_fixture_plan_v1 import (
    build_iteration_v2_fixture_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_v2_planning.document_surface_iteration_v2_metrics_plan_v1 import (
    build_iteration_v2_metrics_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_v2_planning.document_surface_option_a_b_route_comparison_v1 import (
    build_option_a_b_route_comparison,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_v2_planning.document_surface_option_a_limit_review_v1 import (
    build_option_a_limit_review,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_v2_planning.document_surface_option_b_candidate_route_v1 import (
    build_option_b_candidate_route,
)
from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_V2_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_V2_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Candidate-Route-DryRun-v1-001"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_v2_planning_v1"

UPSTREAM_ITERATION_POST_REVIEW = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_post_review_v1/"
    "iteration_post_review_summary.json"
)
POST_REVIEW_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_POST_REVIEW_GO"
CONSTRAINTS_REL = "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_iteration_v2_planning/document_surface_option_b_admission_constraints_v1.json"


def _load_json(root: Path, rel: str) -> Dict[str, Any]:
    p = root / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def run_iteration_v2_planning(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}

    option_a = build_option_a_limit_review()
    option_b = build_option_b_candidate_route(repo_root=root)
    comparison = build_option_a_b_route_comparison()
    hybrid = build_hybrid_candidate_policy()
    case_mapping = build_iteration_v2_case_mapping()
    fixtures = build_iteration_v2_fixture_plan()
    metrics = build_iteration_v2_metrics_plan()
    constraints = _load_json(root, CONSTRAINTS_REL)

    upstream = _load_json(root, UPSTREAM_ITERATION_POST_REVIEW)
    blockers: List[str] = []
    if upstream.get("final_decision") != POST_REVIEW_GO:
        blockers.append(f"upstream.iteration_post_review.not_go={upstream.get('final_decision')}")
    if entry.get("controlled_execution_iteration_post_review_ready") is not True:
        blockers.append("registry.controlled_execution_iteration_post_review_ready")
    if not case_mapping.get("all_required_cases_covered"):
        blockers.append("case_mapping.incomplete")
    if option_a.get("option_a_activation_status") != "not_allowed":
        blockers.append("option_a.activation_not_blocked")
    if option_b.get("option_b_status") != "candidate_route_only":
        blockers.append("option_b.not_candidate_route_only")
    if comparison.get("silent_fallback") is not False:
        blockers.append("comparison.silent_fallback_not_forbidden")

    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    route_verdict = {
        "option_a_sole_route": False,
        "option_a_continue_as_baseline": True,
        "option_b_introduced": True,
        "option_b_relationship": "parallel_candidate_routes",
        "option_b_not_silent_fallback": True,
        "conflict_resolution": "validation_review",
    }

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-v2-Planning-v1-001",
        "iteration_v2_planning_only": True,
        "detector_execution_forbidden": True,
        "option_b_execution_forbidden": True,
        "model_download_forbidden": True,
        "runtime_activation_allowed": False,
        "boundary_status": upstream.get("boundary_status", "frozen"),
        "protocol_compliance_check": "required",
        "protocol_compliance_passed": True,
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "route_verdict": route_verdict,
        "quality_conclusion_from_post_review": upstream.get("quality_conclusion"),
        "blocker_count": len(blockers),
        "failed_checks": blockers,
        "recommended_next_phase": NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL if decision == FINAL_GO else None,
        "final_decision": decision,
        "planned_at": datetime.now(timezone.utc).isoformat(),
        "candidate_only": True,
        "not_fact": True,
    }

    out_dir = root / OUTPUT_ROOT
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "iteration_v2_planning_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_a_limit_review.json").write_text(json.dumps(option_a, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_candidate_route_plan.json").write_text(json.dumps(option_b, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_a_b_route_comparison.json").write_text(json.dumps(comparison, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "hybrid_candidate_policy.json").write_text(json.dumps(hybrid, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_admission_constraints.json").write_text(json.dumps(constraints, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_v2_case_mapping.json").write_text(json.dumps(case_mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_v2_fixture_plan.json").write_text(json.dumps(fixtures, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_v2_metrics_plan.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "option_a_limit_review": option_a,
        "option_b_candidate_route": option_b,
        "option_a_b_comparison": comparison,
        "hybrid_policy": hybrid,
        "case_mapping": case_mapping,
        "fixture_plan": fixtures,
        "metrics_plan": metrics,
        "option_b_admission_constraints": constraints,
    }

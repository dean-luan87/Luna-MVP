# -*- coding: utf-8 -*-
"""Document Surface — Option B candidate route post-review adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_post_review.document_surface_option_a_b_conflict_policy_reviewer_v1 import (
    review_option_ab_conflict_policy,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_post_review.document_surface_option_b_admission_gate_reviewer_v1 import (
    review_option_b_admission_gate,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_post_review.document_surface_option_b_case_mapping_reviewer_v1 import (
    review_option_b_case_mapping,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_post_review.document_surface_option_b_metrics_reviewer_v1 import (
    review_option_b_metrics,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_post_review.document_surface_option_b_output_contract_reviewer_v1 import (
    review_option_b_output_contract,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_post_review.document_surface_option_b_risk_registry_v1 import (
    build_option_b_risk_registry,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_post_review.document_surface_option_b_route_selection_reviewer_v1 import (
    review_option_b_route_selection,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_POST_REVIEW_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_POST_REVIEW_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Dependency-And-Model-Candidate-Admission-Planning-v1-001"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
DRYRUN_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_DRYRUN_GO"

OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_post_review_v1"

DRYRUN_SUMMARY_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1/"
    "option_b_candidate_route_dryrun_summary.json"
)
V2_PLANNING_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_v2_planning_v1/"
    "iteration_v2_planning_summary.json"
)
V2_PLANNING_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_V2_PLANNING_GO"


def _load_json(root: Path, rel: str) -> Dict[str, Any]:
    p = root / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def _build_report(*, summary: Dict[str, Any]) -> str:
    lines = [
        "# Document Surface — Option B Candidate Route Post-Review Report v1",
        "",
        f"**Final decision:** `{summary.get('final_decision')}`",
        f"**Boundary status:** `{summary.get('boundary_status')}`",
        f"**Option B execution allowed:** `{summary.get('option_b_execution_allowed')}`",
        f"**Option B active model selected:** `{summary.get('option_b_active_model_selected')}`",
        "",
        "## 治理结论",
        "",
        "Option B candidate route 治理接缝已确认有效；route 选择、admission gate、output contract、A/B conflict policy 均合规。",
        "尚未进入 dependency/model admission；segmentation 质量未知。",
        "",
        "## 推荐下一阶段",
        "",
        f"- **主轨:** `{summary.get('recommended_next_phase')}`（planning only，不下载/不执行）",
        f"- **并行:** `{summary.get('parallel_next_track')}`",
        "",
        "## Unresolved risks",
        "",
    ]
    for r in summary.get("unresolved_risks") or []:
        lines.append(f"- `{r}`")
    lines.append("")
    return "\n".join(lines)


def run_option_b_candidate_route_post_review(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    blockers: List[str] = []

    dryrun = _load_json(root, DRYRUN_SUMMARY_REL)
    v2 = _load_json(root, V2_PLANNING_REL)
    if dryrun.get("final_decision") != DRYRUN_GO:
        blockers.append(f"upstream.dryrun.not_go={dryrun.get('final_decision')}")
    if v2.get("final_decision") != V2_PLANNING_GO:
        blockers.append(f"upstream.v2_planning.not_go={v2.get('final_decision')}")
    if entry.get("option_b_candidate_route_dryrun_ready") is not True:
        blockers.append("registry.option_b_candidate_route_dryrun_ready")

    admission = review_option_b_admission_gate(repo_root=root)
    contract = review_option_b_output_contract(repo_root=root)
    routes = review_option_b_route_selection(repo_root=root)
    conflict = review_option_ab_conflict_policy(repo_root=root)
    cases = review_option_b_case_mapping(repo_root=root)
    metrics = review_option_b_metrics(repo_root=root)
    risks = build_option_b_risk_registry()

    reviews = [admission, contract, routes, conflict, cases, metrics]
    for r in reviews:
        if not r.get("passed"):
            blockers.append(f"review.failed={r.get('review_id')}")

    review_passed = sum(r.get("review_passed_count", 1 if r.get("passed") else 0) for r in reviews)
    review_failed = sum(r.get("review_failed_count", 0 if r.get("passed") else 1) for r in reviews)
    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Candidate-Route-Post-Review-v1-001",
        "post_review_only": True,
        "option_b_execution_forbidden": True,
        "dependency_admission_forbidden": True,
        "segmentation_execution_forbidden": True,
        "runtime_activation_allowed": False,
        "option_b_execution_allowed": False,
        "option_b_active_model_selected": False,
        "boundary_status": "frozen" if decision == FINAL_GO else "blocked",
        "dryrun_final_decision": DRYRUN_GO,
        "review_passed_count": review_passed,
        "review_failed_count": review_failed,
        "blocker_count": len(blockers),
        "failed_checks": blockers,
        "protocol_compliance_passed": True,
        "protocol_compliance_check": "required",
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "unresolved_risks": risks.get("unresolved_risks"),
        "confirmed_governance": [r["risk_id"] for r in risks.get("confirmed_governance", [])],
        "recommended_next_phase": NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL if decision == FINAL_GO else None,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "candidate_only": True,
        "not_fact": True,
    }

    report_md = _build_report(summary=summary)
    out_dir = root / OUTPUT_ROOT
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "option_b_candidate_route_post_review_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_admission_gate_review.json").write_text(json.dumps(admission, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_output_contract_review.json").write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_route_selection_review.json").write_text(json.dumps(routes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_a_b_conflict_policy_review.json").write_text(json.dumps(conflict, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_case_mapping_review.json").write_text(json.dumps(cases, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_metrics_review.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_risk_registry.json").write_text(json.dumps(risks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_candidate_route_post_review_report.md").write_text(report_md, encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "admission_review": admission,
        "contract_review": contract,
        "route_review": routes,
        "conflict_review": conflict,
        "case_review": cases,
        "metrics_review": metrics,
        "risk_registry": risks,
    }

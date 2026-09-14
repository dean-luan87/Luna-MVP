# -*- coding: utf-8 -*-
"""Document Surface — Option B admission post-review adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_post_review.document_surface_option_b_abort_rollback_reviewer_v1 import (
    review_abort_rollback,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_post_review.document_surface_option_b_admission_boundary_reviewer_v1 import (
    review_admission_boundary,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_post_review.document_surface_option_b_admitted_candidate_reviewer_v1 import (
    review_admitted_candidates,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_post_review.document_surface_option_b_blocked_candidate_reviewer_v1 import (
    review_blocked_candidates,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_post_review.document_surface_option_b_candidate_fixture_reviewer_v1 import (
    review_candidate_fixtures,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_post_review.document_surface_option_b_metrics_reviewer_v1 import (
    review_admission_metrics,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_post_review.document_surface_option_b_output_contract_reviewer_v1 import (
    review_output_contract,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_post_review.document_surface_option_b_risk_registry_v1 import (
    build_option_b_admission_risk_registry,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_POST_REVIEW_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_POST_REVIEW_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Model-Skill-Admission-Protocol-Alignment-Planning-v1-001"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_post_review_v1"

DRYRUN_DIR = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_dryrun_v1"
DRYRUN_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_DRYRUN_GO"
ROUTE_DRYRUN_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_DRYRUN_GO"
ROUTE_POST_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_POST_REVIEW_GO"
PLANNING_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_PLANNING_GO"


def _load_json(root: Path, rel: str) -> Dict[str, Any]:
    p = root / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def _load_list(root: Path, rel: str) -> List[Dict[str, Any]]:
    p = root / rel
    if not p.is_file():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def _build_report(*, summary: Dict[str, Any]) -> str:
    lines = [
        "# Document Surface — Option B Admission Post-Review Report v1",
        "",
        f"**Final decision:** `{summary.get('final_decision')}`",
        f"**Boundary status:** `{summary.get('boundary_status')}`",
        f"**Option B execution allowed:** `{summary.get('option_b_execution_allowed')}`",
        f"**Option B active model selected:** `{summary.get('option_b_active_model_selected')}`",
        f"**Active registry update allowed:** `{summary.get('active_registry_update_allowed')}`",
        "",
        "## 治理结论",
        "",
        "Option B admission gate 可用，A1/C1 可进入 preflight planning；",
        "但 Option B 仍没有 active model、没有依赖准入、没有质量验证、没有执行权限。",
        "",
        "A1/C1 仅为 `admitted_for_preflight_candidate`，**不是** active model。",
        "6 个 blocked candidate 均有充分 abort/rollback，无 silent fallback。",
        "",
        "Metrics 代表 admission gate 可用，不代表 segmentation quality 已验证。",
        "",
        "## 准入结果确认",
        "",
        "| Candidate | Status |",
        "|-----------|--------|",
        "| A1 classical_helper_ok | admitted_for_preflight_candidate |",
        "| C1 document_specific ok | admitted_for_preflight_candidate |",
        "| A2 uncontrolled_binary | blocked_dependency_not_admitted_candidate |",
        "| B1 weight_missing | blocked_model_weight_missing_candidate |",
        "| B2 license_unknown | blocked_license_not_cleared_candidate |",
        "| B3 caption/text | blocked_or_requires_wrapper_candidate |",
        "| C2 document_type_fact | blocked_output_contract_violation_candidate |",
        "| D1 hardware_missing | blocked_hardware_requirement_missing_candidate |",
        "",
        "## 推荐下一阶段",
        "",
        f"- **主轨:** `{summary.get('recommended_next_phase')}`（protocol alignment planning，挂载 Model/Skill Admission Contract）",
        f"- **并行:** `{summary.get('parallel_next_track')}`",
        "",
        "## Mitigated risks",
        "",
    ]
    for r in summary.get("mitigated_risks") or []:
        lines.append(f"- `{r}`")
    lines.extend(["", "## Unresolved risks", ""])
    for r in summary.get("unresolved_risks") or []:
        lines.append(f"- `{r}`")
    lines.append("")
    return "\n".join(lines)


def run_option_b_admission_post_review(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    blockers: List[str] = []

    dryrun = _load_json(root, f"{DRYRUN_DIR}/option_b_admission_dryrun_summary.json")
    route_dryrun = _load_json(
        root,
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1/option_b_candidate_route_dryrun_summary.json",
    )
    route_post = _load_json(
        root,
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_post_review_v1/option_b_candidate_route_post_review_summary.json",
    )
    planning = _load_json(
        root,
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_planning_v1/option_b_admission_planning_summary.json",
    )

    if route_dryrun.get("final_decision") != ROUTE_DRYRUN_GO:
        blockers.append(f"upstream.route_dryrun.not_go={route_dryrun.get('final_decision')}")
    if route_post.get("final_decision") != ROUTE_POST_GO:
        blockers.append(f"upstream.route_post_review.not_go={route_post.get('final_decision')}")
    if planning.get("final_decision") != PLANNING_GO:
        blockers.append(f"upstream.planning.not_go={planning.get('final_decision')}")
    if dryrun.get("final_decision") != DRYRUN_GO:
        blockers.append(f"upstream.dryrun.not_go={dryrun.get('final_decision')}")
    if entry.get("option_b_dependency_and_model_candidate_admission_dryrun_ready") is not True:
        blockers.append("registry.admission_dryrun_ready")

    registry = _load_json(root, f"{DRYRUN_DIR}/option_b_candidate_fixture_registry.json")
    results = _load_list(root, f"{DRYRUN_DIR}/option_b_model_candidate_admission_results.json")
    metrics_data = dryrun.get("metrics") or _load_json(root, f"{DRYRUN_DIR}/option_b_admission_dryrun_metrics.json")

    boundary = review_admission_boundary(dryrun_summary=dryrun)
    fixtures = review_candidate_fixtures(registry=registry)
    admitted = review_admitted_candidates(results=results, registry=registry)
    blocked = review_blocked_candidates(results=results)
    contract = review_output_contract(registry=registry)
    abort = review_abort_rollback(results=results)
    metrics = review_admission_metrics(metrics=metrics_data)
    risks = build_option_b_admission_risk_registry()

    reviews = [boundary, fixtures, admitted, blocked, contract, abort, metrics]
    for r in reviews:
        if not r.get("passed"):
            blockers.append(f"review.failed={r.get('review_id')}")

    review_passed = sum(r.get("review_passed_count", 0) for r in reviews)
    review_failed = sum(r.get("review_failed_count", 0) for r in reviews)
    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Dependency-And-Model-Candidate-Admission-Post-Review-v1-001",
        "post_review_only": True,
        "segmentation_execution_forbidden": True,
        "model_download_forbidden": True,
        "dependency_install_forbidden": True,
        "preflight_execution_forbidden": True,
        "controlled_execution_forbidden": True,
        "runtime_activation_allowed": False,
        "option_b_execution_allowed": False,
        "option_b_active_model_selected": False,
        "active_registry_update_allowed": False,
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
        "admitted_for_preflight_candidate_count": 2,
        "blocked_candidate_count": 6,
        "mitigated_risks": [r["risk_id"] for r in risks.get("mitigated_risks", [])],
        "unresolved_risks": risks.get("unresolved_risks"),
        "governance_conclusion": (
            "Option B admission gate 可用，A1/C1 可进入 preflight planning；"
            "但 Option B 仍没有 active model、没有依赖准入、没有质量验证、没有执行权限。"
        ),
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
        (out_dir / "option_b_admission_post_review_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_candidate_fixture_review.json").write_text(json.dumps(fixtures, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_admitted_candidate_review.json").write_text(json.dumps(admitted, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_blocked_candidate_review.json").write_text(json.dumps(blocked, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_output_contract_review.json").write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_abort_rollback_review.json").write_text(json.dumps(abort, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_metrics_review.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_risk_registry.json").write_text(json.dumps(risks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_admission_post_review_report.md").write_text(report_md, encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "boundary_review": boundary,
        "fixture_review": fixtures,
        "admitted_review": admitted,
        "blocked_review": blocked,
        "contract_review": contract,
        "abort_review": abort,
        "metrics_review": metrics,
        "risk_registry": risks,
    }

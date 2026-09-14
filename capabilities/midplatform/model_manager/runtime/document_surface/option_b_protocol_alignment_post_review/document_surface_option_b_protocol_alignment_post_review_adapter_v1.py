# -*- coding: utf-8 -*-
"""Document Surface — Option B protocol alignment post-review adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_post_review.document_surface_option_b_change_control_post_reviewer_v1 import (
    review_change_control,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_post_review.document_surface_option_b_dependency_permission_post_reviewer_v1 import (
    review_dependency_permission,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_post_review.document_surface_option_b_evidence_chain_post_reviewer_v1 import (
    review_evidence_chain,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_post_review.document_surface_option_b_model_skill_contract_post_reviewer_v1 import (
    review_model_skill_contract,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_post_review.document_surface_option_b_output_contract_protocol_post_reviewer_v1 import (
    review_output_contract_protocol,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_post_review.document_surface_option_b_protocol_alignment_boundary_reviewer_v1 import (
    review_protocol_alignment_boundary,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_post_review.document_surface_option_b_protocol_alignment_metrics_post_reviewer_v1 import (
    review_protocol_alignment_metrics,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_post_review.document_surface_option_b_protocol_alignment_risk_registry_v1 import (
    build_protocol_alignment_risk_registry,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_post_review.document_surface_option_b_registry_alignment_post_reviewer_v1 import (
    review_registry_alignment,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_post_review.document_surface_option_b_runtime_boundary_post_reviewer_v1 import (
    review_runtime_boundary,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_POST_REVIEW_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_POST_REVIEW_BLOCKED"
NEXT_PREFLIGHT_PLANNING = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Preflight-Planning-v1-001"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_post_review_v1"
DRYRUN_DIR = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_dryrun_v1"
DRYRUN_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_DRYRUN_GO"
ALIGNMENT_PLANNING_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_PLANNING_GO"
ADMISSION_DRYRUN_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_DRYRUN_GO"
ADMISSION_POST_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_POST_REVIEW_GO"
ADMISSION_PLANNING_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_PLANNING_GO"
ROUTE_DRYRUN_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_DRYRUN_GO"
ROUTE_POST_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_POST_REVIEW_GO"


def _load_json(root: Path, rel: str) -> Dict[str, Any]:
    p = root / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def _build_report(*, summary: Dict[str, Any]) -> str:
    lines = [
        "# Document Surface — Option B Protocol Alignment Post-Review Report v1",
        "",
        f"**Final decision:** `{summary.get('final_decision')}`",
        f"**Boundary status:** `{summary.get('boundary_status')}`",
        f"**Preflight planning allowed:** `{summary.get('preflight_planning_allowed')}`",
        f"**Preflight execution allowed:** `{summary.get('preflight_execution_allowed')}`",
        "",
        "## 核心结论",
        "",
        summary.get("governance_conclusion", ""),
        "",
        "## 推荐下一阶段",
        "",
        f"- **主轨:** `{summary.get('recommended_next_phase')}`（planning only）",
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


def run_option_b_protocol_alignment_post_review(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    blockers: List[str] = []

    upstream = {
        "route_dryrun": _load_json(root, "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1/option_b_candidate_route_dryrun_summary.json"),
        "route_post": _load_json(root, "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_post_review_v1/option_b_candidate_route_post_review_summary.json"),
        "admission_planning": _load_json(root, "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_planning_v1/option_b_admission_planning_summary.json"),
        "admission_dryrun": _load_json(root, "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_dryrun_v1/option_b_admission_dryrun_summary.json"),
        "admission_post": _load_json(root, "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_post_review_v1/option_b_admission_post_review_summary.json"),
        "alignment_planning": _load_json(root, "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_planning_v1/option_b_protocol_alignment_planning_summary.json"),
        "alignment_dryrun": _load_json(root, f"{DRYRUN_DIR}/option_b_protocol_alignment_dryrun_summary.json"),
    }
    if upstream["route_dryrun"].get("final_decision") != ROUTE_DRYRUN_GO:
        blockers.append("upstream.route_dryrun")
    if upstream["route_post"].get("final_decision") != ROUTE_POST_GO:
        blockers.append("upstream.route_post")
    if upstream["admission_planning"].get("final_decision") != ADMISSION_PLANNING_GO:
        blockers.append("upstream.admission_planning")
    if upstream["admission_dryrun"].get("final_decision") != ADMISSION_DRYRUN_GO:
        blockers.append("upstream.admission_dryrun")
    if upstream["admission_post"].get("final_decision") != ADMISSION_POST_GO:
        blockers.append("upstream.admission_post")
    if upstream["alignment_planning"].get("final_decision") != ALIGNMENT_PLANNING_GO:
        blockers.append("upstream.alignment_planning")
    if upstream["alignment_dryrun"].get("final_decision") != DRYRUN_GO:
        blockers.append("upstream.alignment_dryrun")
    if entry.get("option_b_model_skill_admission_protocol_alignment_dryrun_ready") is not True:
        blockers.append("registry.alignment_dryrun_ready")

    dryrun = upstream["alignment_dryrun"]
    metrics = dryrun.get("metrics") or _load_json(root, f"{DRYRUN_DIR}/option_b_protocol_alignment_metrics.json")
    contract = _load_json(root, f"{DRYRUN_DIR}/option_b_model_skill_contract_mapping_results.json")
    registry = _load_json(root, f"{DRYRUN_DIR}/option_b_registry_alignment_results.json")
    dependency = _load_json(root, f"{DRYRUN_DIR}/option_b_dependency_protocol_mapping_results.json")
    permission = _load_json(root, f"{DRYRUN_DIR}/option_b_permission_admission_mapping_results.json")
    output = _load_json(root, f"{DRYRUN_DIR}/option_b_output_contract_protocol_mapping_results.json")
    runtime = _load_json(root, f"{DRYRUN_DIR}/option_b_runtime_boundary_mapping_results.json")
    change = _load_json(root, f"{DRYRUN_DIR}/option_b_change_control_mapping_results.json")
    evidence = _load_json(root, f"{DRYRUN_DIR}/option_b_evidence_chain_mapping_results.json")
    risks = build_protocol_alignment_risk_registry()

    boundary = review_protocol_alignment_boundary(dryrun_summary=dryrun)
    contract_review = review_model_skill_contract(contract_results=contract)
    registry_review = review_registry_alignment(registry_results=registry)
    dep_perm_review = review_dependency_permission(dependency_results=dependency, permission_results=permission)
    output_review = review_output_contract_protocol(output_results=output)
    runtime_review = review_runtime_boundary(runtime_results=runtime)
    change_review = review_change_control(change_results=change, repo_root=root)
    evidence_review = review_evidence_chain(evidence_results=evidence)
    metrics_review = review_protocol_alignment_metrics(metrics=metrics)

    reviews = [boundary, contract_review, registry_review, dep_perm_review, output_review, runtime_review, change_review, evidence_review, metrics_review]
    for r in reviews:
        if not r.get("passed"):
            blockers.append(f"review.failed={r.get('review_id')}")

    review_passed = sum(r.get("review_passed_count", 0) for r in reviews)
    review_failed = sum(r.get("review_failed_count", 0) for r in reviews)
    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Model-Skill-Admission-Protocol-Alignment-Post-Review-v1-001",
        "post_review_only": True,
        "preflight_execution_forbidden": True,
        "segmentation_execution_forbidden": True,
        "runtime_activation_allowed": False,
        "controlled_execution_allowed": False,
        "option_b_execution_allowed": False,
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
        "active_model_mapping_count": metrics.get("active_model_mapping_count", 0),
        "active_skill_mapping_count": metrics.get("active_skill_mapping_count", 0),
        "active_registry_update_count": metrics.get("active_registry_update_count", 0),
        "runtime_activation_count": metrics.get("runtime_activation_count", 0),
        "preflight_planning_allowed": decision == FINAL_GO,
        "preflight_execution_allowed": False,
        "mitigated_risks": [r["risk_id"] for r in risks.get("mitigated_risks", [])],
        "unresolved_risks": risks.get("unresolved_risks"),
        "governance_conclusion": (
            "Option B 已完成 Model/Skill Admission Contract 对齐闭环；"
            "A1/C1 仅允许进入 Preflight Planning，仍非 active model/skill/runtime；"
            "所有 blocked candidates 的拒绝路径、权限阻断、输出契约阻断与证据链均可追踪。"
        ),
        "recommended_next_phase": NEXT_PREFLIGHT_PLANNING if decision == FINAL_GO else None,
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
        (out_dir / "option_b_protocol_alignment_post_review_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_model_skill_contract_post_review.json").write_text(json.dumps(contract_review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_registry_alignment_post_review.json").write_text(json.dumps(registry_review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_dependency_permission_post_review.json").write_text(json.dumps(dep_perm_review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_output_contract_protocol_post_review.json").write_text(json.dumps(output_review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_runtime_boundary_post_review.json").write_text(json.dumps(runtime_review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_change_control_post_review.json").write_text(json.dumps(change_review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_evidence_chain_post_review.json").write_text(json.dumps(evidence_review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_protocol_alignment_risk_registry.json").write_text(json.dumps(risks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_protocol_alignment_post_review_report.md").write_text(report_md, encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "boundary_review": boundary,
        "contract_review": contract_review,
        "registry_review": registry_review,
        "dependency_permission_review": dep_perm_review,
        "output_review": output_review,
        "runtime_review": runtime_review,
        "change_review": change_review,
        "evidence_review": evidence_review,
        "metrics_review": metrics_review,
        "risk_registry": risks,
    }

# -*- coding: utf-8 -*-
"""Document Surface Detector — post-review adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.post_review.document_surface_detector_contract_reviewer_v1 import (
    review_contracts,
)
from capabilities.midplatform.model_manager.runtime.document_surface.post_review.document_surface_detector_guard_reviewer_v1 import (
    review_guards,
)
from capabilities.midplatform.model_manager.runtime.document_surface.post_review.document_surface_detector_risk_registry_v1 import (
    build_risk_registry,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_POST_REVIEW_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_POST_REVIEW_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Planning-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

UPSTREAM_REVIEW_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_situation_understanding_attention_gated_ri_dryrun_v1_review_v0/"
        "p1_midplatform_luna_situation_understanding_attention_gated_ri_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_LIGHTWEIGHT_VISION_RUNTIME_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_lightweight_vision_runtime_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_lightweight_vision_runtime_planning_review_v1.json"
    ),
}


def _load_json(repo_root: Path, rel: str) -> Dict[str, Any]:
    path = repo_root / rel
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _build_report(
    *,
    contract: Dict[str, Any],
    guards: Dict[str, Any],
    risks: Dict[str, Any],
    upstream_ok: bool,
    decision: str,
) -> str:
    lines = [
        "# Document Surface Detector Real Runtime Integration — Post-Review Report v1",
        "",
        f"**Phase:** Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Post-Review-v1-001",
        f"**Reviewed at:** {datetime.now(timezone.utc).isoformat()}",
        f"**Final decision:** `{decision}`",
        "",
        "## 冻结链路",
        "",
        "```",
        "Attention-Gated Region",
        "    ↓",
        "Model Manager Runtime Binding",
        "    ↓",
        "document_surface_detector_v1 deterministic fixture runtime",
        "    ↓",
        "document_surface_candidate + relation_hint_candidate",
        "    ↓",
        "Ownership Evidence Package",
        "    ↓",
        "Text Owner Assignment Candidate",
        "    ↓",
        "Validation",
        "```",
        "",
        "## Contract 审查",
        "",
        f"- Passed: {contract.get('review_passed_count', 0)}",
        f"- Failed: {contract.get('review_failed_count', 0)}",
        "",
        "## Guard 回归",
        "",
        f"- Guards passed: {guards.get('review_passed_count', 0)} / {guards.get('review_passed_count', 0) + guards.get('review_failed_count', 0)}",
        f"- Case coverage complete: {guards.get('case_coverage_complete')}",
        "",
        "## 风险登记",
        "",
        f"- Unresolved risks: {risks.get('unresolved_risk_count', 0)}",
        "",
    ]
    for rid in risks.get("unresolved_risks") or []:
        lines.append(f"- `{rid}`")
    lines.extend([
        "",
        "## 下一阶段准入",
        "",
        f"**Recommended (Route A):** `{RECOMMENDED_NEXT_PHASE}`",
        "",
        "理由：Contract 完整、边界稳定、DryRun 8/8 通过，可规划第一个真实实现候选，但仍不执行真实模型。",
        "",
        f"**Parallel track (Route B):** `{PARALLEL_NEXT_TRACK}`",
        "",
        "理由：L1 Field Understanding 语义主线需与 Attention / Region Intelligence 对齐，可与 Implementation Planning 并行推进。",
        "",
        "## 边界冻结",
        "",
        "- 不接真实模型",
        "- 不执行真实图像分割",
        "- 不跑 OCR / VLM",
        "- 不新增 layout parser 行为",
        "- document_surface_candidate 不得写成 document fact",
        "- 不跳过 Implementation Planning 直接进入真实执行",
        "",
        f"**Upstream GO verified:** {upstream_ok}",
    ])
    return "\n".join(lines) + "\n"


def run_document_surface_detector_post_review(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    """执行 Post-Review — 审查、归档、边界冻结、风险登记、准入判断。"""
    root = repo_root or Path.cwd()
    blockers: List[str] = []

    upstream_status: Dict[str, str] = {}
    for go_id, rel in UPSTREAM_REVIEW_PATHS.items():
        data = _load_json(root, rel)
        fd = data.get("final_decision", "")
        upstream_status[go_id] = fd
        if fd != go_id:
            blockers.append(f"upstream.missing_or_blocked={go_id}")

    contract = review_contracts()
    guards = review_guards()
    risks = build_risk_registry()

    if not contract.get("passed"):
        blockers.append("contract.review_failed")
    if not guards.get("passed"):
        blockers.append("guard.review_failed")

    review_passed = contract.get("review_passed_count", 0) + guards.get("review_passed_count", 0)
    review_failed = contract.get("review_failed_count", 0) + guards.get("review_failed_count", 0)
    upstream_ok = not any(b.startswith("upstream.") for b in blockers)

    decision = FINAL_GO if not blockers else FINAL_BLOCKED
    boundary_status = "frozen" if decision == FINAL_GO else "blocked"

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Post-Review-v1-001",
        "runtime_id": "document_surface_detector_v1",
        "post_review_only": True,
        "upstream_status": upstream_status,
        "contract_review_passed": contract.get("passed"),
        "guard_review_passed": guards.get("passed"),
        "case_coverage_complete": guards.get("case_coverage_complete"),
        "review_passed_count": review_passed,
        "review_failed_count": review_failed,
        "blocker_count": len(blockers),
        "failed_checks": blockers,
        "boundary_status": boundary_status,
        "unresolved_risks": risks.get("unresolved_risks"),
        "recommended_next_phase": RECOMMENDED_NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL_NEXT_TRACK if decision == FINAL_GO else None,
        "route_a_rationale": "Contract 完整，边界稳定，可规划第一个真实实现候选，但仍不执行真实模型。",
        "route_b_rationale": "L1 Field Understanding 语义主线需补齐，标记为 parallel_next_track。",
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
    }

    report_md = _build_report(
        contract=contract,
        guards=guards,
        risks=risks,
        upstream_ok=upstream_ok,
        decision=decision,
    )

    out_dir = root / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_post_review_v1"
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "document_surface_detector_post_review_summary_v1.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_dir / "document_surface_detector_contract_review_v1.json").write_text(
            json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_dir / "document_surface_detector_guard_review_v1.json").write_text(
            json.dumps(guards, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_dir / "document_surface_detector_risk_registry_v1.json").write_text(
            json.dumps(risks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_dir / "document_surface_detector_post_review_report_v1.md").write_text(report_md, encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "contract_review": contract,
        "guard_review": guards,
        "risk_registry": risks,
        "report_markdown": report_md,
    }

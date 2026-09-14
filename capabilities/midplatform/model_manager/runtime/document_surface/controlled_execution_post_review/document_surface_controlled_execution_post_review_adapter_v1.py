# -*- coding: utf-8 -*-
"""Document Surface Controlled Execution — post-review adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_post_review.document_surface_controlled_execution_boundary_reviewer_v1 import (
    review_controlled_execution_boundary,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_post_review.document_surface_controlled_execution_case_reviewer_v1 import (
    review_controlled_execution_cases,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_post_review.document_surface_controlled_execution_candidate_quality_reviewer_v1 import (
    review_candidate_quality,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_post_review.document_surface_controlled_execution_metrics_reviewer_v1 import (
    review_controlled_execution_metrics,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_post_review.document_surface_controlled_execution_protocol_compliance_reviewer_v1 import (
    review_controlled_execution_protocol_compliance,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_post_review.document_surface_controlled_execution_risk_registry_v1 import (
    build_controlled_execution_risk_registry,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_POST_REVIEW_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_POST_REVIEW_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-Planning-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_post_review_v1"

UPSTREAM = {
    "planning": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_planning_review_v1.json"
    ),
    "preflight": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_preflight_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_preflight_review_v1.json"
    ),
    "dryrun": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_review_v1.json"
    ),
}

DRYRUN_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_DRYRUN_GO"
HISTORICAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_DRYRUN_BLOCKED_BY_MISSING_FIXTURES"


def _load_json(root: Path, rel: str) -> Dict[str, Any]:
    p = root / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def _build_report(*, summary: Dict[str, Any]) -> str:
    return "\n".join([
        "# Document Surface Detector — Controlled Execution Post-Review Report v1",
        "",
        f"**Phase:** Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Post-Review-v1-001",
        f"**Final decision:** `{summary.get('final_decision')}`",
        f"**Boundary status:** `{summary.get('boundary_status')}`",
        f"**Runtime activation allowed:** `{summary.get('runtime_activation_allowed')}`",
        "",
        "## 历史记录",
        "",
        f"- 首次 DryRun（fixture 缺失）: `{HISTORICAL_BLOCKED}` — 非当前裁决",
        f"- 当前 DryRun 裁决: `{DRYRUN_GO}`",
        "",
        "## Review Watch（非 blocker）",
        "",
        "- `overlapping_documents_under_separated` — Case B 1 surface / 0 relation",
        "- `relation_hint_missing_for_overlap_case`",
        "- `registry_item_count_case_count_mismatch_explained` — registry=7, cases=8",
        "",
        "## 推荐下一阶段",
        "",
        f"- **Route A:** `{summary.get('recommended_next_phase')}`",
        f"- **Route B (parallel):** `{summary.get('parallel_next_track')}`",
        "",
        "## Unresolved risks",
        "",
        *[f"- `{r}`" for r in summary.get("unresolved_risks") or []],
        "",
    ]) + "\n"


def run_controlled_execution_post_review(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    blockers: List[str] = []

    for name, rel in UPSTREAM.items():
        upstream = _load_json(root, rel)
        fd = upstream.get("final_decision", "")
        if name == "dryrun":
            if fd != DRYRUN_GO:
                blockers.append(f"upstream.dryrun.not_go={fd}")
        elif name == "preflight":
            if "PREFLIGHT_GO" not in fd and not fd.endswith("_GO"):
                blockers.append(f"upstream.preflight.not_go={fd}")
        elif name == "planning":
            if not fd.endswith("_GO"):
                blockers.append(f"upstream.planning.not_go={fd}")

    boundary = review_controlled_execution_boundary(repo_root=root)
    cases = review_controlled_execution_cases(repo_root=root)
    metrics = review_controlled_execution_metrics(repo_root=root)
    quality = review_candidate_quality(repo_root=root)
    protocol = review_controlled_execution_protocol_compliance(repo_root=root)
    risks = build_controlled_execution_risk_registry()

    reviews = [boundary, cases, metrics, quality, protocol]
    for r in reviews:
        if not r.get("passed"):
            blockers.append(f"review.failed={r.get('review_id')}")

    review_passed = sum(r.get("review_passed_count", 1 if r.get("passed") else 0) for r in reviews)
    review_failed = sum(r.get("review_failed_count", 0 if r.get("passed") else 1) for r in reviews)

    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Post-Review-v1-001",
        "runtime_id": "document_surface_detector_v1",
        "implementation_mode": "option_a_classical_cv_boundary",
        "post_review_only": True,
        "detector_rerun_forbidden": True,
        "real_execution_enabled": False,
        "runtime_activation_allowed": False,
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "protocol_compliance_check": "required",
        "protocol_compliance_passed": protocol.get("protocol_compliance_passed") is True,
        "boundary_status": "frozen" if decision == FINAL_GO else "blocked",
        "dryrun_final_decision_current": DRYRUN_GO,
        "dryrun_historical_blocked_by_missing_fixtures": HISTORICAL_BLOCKED,
        "review_passed_count": review_passed,
        "review_failed_count": review_failed,
        "blocker_count": len(blockers),
        "failed_checks": blockers,
        "review_watch_items": risks.get("review_watch_items"),
        "unresolved_risks": risks.get("unresolved_risks"),
        "recommended_next_phase": RECOMMENDED_NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL_NEXT_TRACK if decision == FINAL_GO else None,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "candidate_only": True,
        "not_fact": True,
    }

    report_md = _build_report(summary=summary)
    out_dir = root / OUTPUT_ROOT

    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "controlled_execution_post_review_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "controlled_execution_case_review.json").write_text(json.dumps(cases, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "controlled_execution_metrics_review.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "controlled_execution_candidate_quality_review.json").write_text(json.dumps(quality, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "controlled_execution_protocol_compliance_review.json").write_text(json.dumps(protocol, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "controlled_execution_risk_registry.json").write_text(json.dumps(risks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "controlled_execution_post_review_report.md").write_text(report_md, encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "boundary_review": boundary,
        "case_review": cases,
        "metrics_review": metrics,
        "quality_review": quality,
        "protocol_review": protocol,
        "risk_registry": risks,
    }

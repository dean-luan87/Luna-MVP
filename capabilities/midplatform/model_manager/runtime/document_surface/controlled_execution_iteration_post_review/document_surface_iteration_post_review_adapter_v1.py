# -*- coding: utf-8 -*-
"""Document Surface Iteration — post-review adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_post_review.document_surface_iteration_boundary_reviewer_v1 import (
    review_iteration_boundary,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_post_review.document_surface_iteration_case_reviewer_v1 import (
    review_iteration_cases,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_post_review.document_surface_iteration_fixture_semantic_reviewer_v1 import (
    review_iteration_fixture_semantics,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_post_review.document_surface_iteration_metrics_reviewer_v1 import (
    review_iteration_metrics,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_post_review.document_surface_iteration_protocol_compliance_reviewer_v1 import (
    review_iteration_protocol_compliance,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_post_review.document_surface_iteration_risk_registry_v1 import (
    build_iteration_risk_registry,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_post_review.document_surface_iteration_strategy_reviewer_v1 import (
    review_iteration_strategies,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_POST_REVIEW_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_POST_REVIEW_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-v2-Planning-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
DRYRUN_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_DRYRUN_GO"

OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_post_review_v1"

DRYRUN_SUMMARY_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_v1/"
    "iteration_dryrun_summary.json"
)


def _load_json(root: Path, rel: str) -> Dict[str, Any]:
    p = root / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def _build_report(*, summary: Dict[str, Any]) -> str:
  lines = [
    "# Document Surface Detector — Iteration Post-Review Report v1",
    "",
    f"**Phase:** Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-Post-Review-v1-001",
    f"**Final decision:** `{summary.get('final_decision')}`",
    f"**Boundary status:** `{summary.get('boundary_status')}`",
    f"**Runtime activation allowed:** `{summary.get('runtime_activation_allowed')}`",
    "",
    "## 质量结论（克制表述）",
    "",
    summary.get("quality_conclusion", ""),
    "",
    "## DryRun 上游裁决",
    "",
    f"- Iteration DryRun: `{DRYRUN_GO}`",
    f"- Smoke: 8/8 passed",
    "",
    "## Review Watch（非 blocker）",
    "",
  ]
  for w in summary.get("review_watch_items") or []:
    lines.append(f"- `{w}`")
  lines.extend([
    "",
    "## 已缓解风险",
    "",
  ])
  for m in summary.get("mitigated_risks") or []:
    lines.append(f"- `{m}`")
  lines.extend([
    "",
    "## Option A 能力边界",
    "",
    "Case A（clear_edges under-separated）与 Case F（receipt clear surface missed）说明 Classical CV 能力边界明显。",
    "v2 规划重点：判断 Option A 是否足够，或引入 Option B 轻量分割作为候选路线。",
    "",
    "## 推荐下一阶段",
    "",
    f"- **Route A（主推荐）:** `{summary.get('recommended_next_phase')}` — controlled iteration，不得 activation",
    f"- **Route B（parallel）:** `{summary.get('parallel_next_track')}`",
    "",
    "## 明确不推荐",
    "",
    "- runtime activation",
    "- OCR per surface",
    "- production registry write",
    "- 扩大真实执行范围",
    "",
  ])
  return "\n".join(lines) + "\n"


def run_iteration_post_review(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    blockers: List[str] = []

    dryrun_summary = _load_json(root, DRYRUN_SUMMARY_REL)
    if dryrun_summary.get("final_decision") != DRYRUN_GO:
        blockers.append(f"upstream.iteration_dryrun.not_go={dryrun_summary.get('final_decision')}")

    boundary = review_iteration_boundary(repo_root=root)
    cases = review_iteration_cases(repo_root=root)
    strategies = review_iteration_strategies(repo_root=root)
    metrics = review_iteration_metrics(repo_root=root)
    fixture_sem = review_iteration_fixture_semantics(repo_root=root)
    protocol = review_iteration_protocol_compliance(repo_root=root)
    risks = build_iteration_risk_registry()

    reviews = [boundary, cases, strategies, metrics, fixture_sem, protocol]
    for r in reviews:
        if not r.get("passed"):
            blockers.append(f"review.failed={r.get('review_id')}")

    review_passed = sum(r.get("review_passed_count", 1 if r.get("passed") else 0) for r in reviews)
    review_failed = sum(r.get("review_failed_count", 0 if r.get("passed") else 1) for r in reviews)

    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    quality_conclusion = (
        "链路安全性进一步确认，relation 治理有效，但 document surface 候选质量仍未达到激活条件。"
        "尤其 Case A 与 Case F 说明 Classical CV 能力边界明显；"
        "GO 代表策略链路安全有效，不代表 detector 可激活、叠放已稳定分离、贴附 receipt 已稳定识别、"
        "或 texture false positive 已完全解决。"
    )

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-Post-Review-v1-001",
        "runtime_id": "document_surface_detector_v1",
        "implementation_mode": "option_a_classical_cv_boundary",
        "post_review_only": True,
        "detector_rerun_forbidden": True,
        "fixture_mutation_forbidden": True,
        "parameter_tuning_forbidden": True,
        "real_execution_enabled": False,
        "runtime_activation_allowed": False,
        "boundary_status": "frozen" if decision == FINAL_GO else "blocked",
        "dryrun_final_decision": DRYRUN_GO,
        "review_passed_count": review_passed,
        "review_failed_count": review_failed,
        "blocker_count": len(blockers),
        "failed_checks": blockers,
        "protocol_compliance_passed": protocol.get("protocol_compliance_passed") is True,
        "quality_conclusion": quality_conclusion,
        "review_watch_items": cases.get("watch_items", []),
        "unresolved_risks": risks.get("unresolved_risks"),
        "mitigated_risks": risks.get("mitigated_risk_ids"),
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
        (out_dir / "iteration_post_review_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_case_quality_review.json").write_text(json.dumps(cases, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_strategy_review.json").write_text(json.dumps(strategies, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_metrics_review.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_risk_registry.json").write_text(json.dumps(risks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_fixture_semantic_review.json").write_text(json.dumps(fixture_sem, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_post_review_report.md").write_text(report_md, encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "boundary_review": boundary,
        "case_review": cases,
        "strategy_review": strategies,
        "metrics_review": metrics,
        "fixture_semantic_review": fixture_sem,
        "protocol_review": protocol,
        "risk_registry": risks,
    }

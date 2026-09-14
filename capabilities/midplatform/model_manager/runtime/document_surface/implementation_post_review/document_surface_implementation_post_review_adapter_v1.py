# -*- coding: utf-8 -*-
"""Document Surface Implementation — post-review adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.implementation_post_review.document_surface_implementation_benchmark_reviewer_v1 import (
    review_implementation_benchmark,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_post_review.document_surface_implementation_contract_reviewer_v1 import (
    review_implementation_contract,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_post_review.document_surface_implementation_dryrun_reviewer_v1 import (
    review_implementation_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_post_review.document_surface_implementation_guard_reviewer_v1 import (
    review_implementation_guards,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_post_review.document_surface_implementation_planning_reviewer_v1 import (
    review_implementation_planning,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_post_review.document_surface_implementation_protocol_compliance_reviewer_v1 import (
    review_protocol_compliance,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_post_review.document_surface_implementation_risk_registry_v1 import (
    build_implementation_risk_registry,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_POST_REVIEW_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_POST_REVIEW_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Planning-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
LATER_PROTOCOL_ALIGNMENT = "Phase-P1-Midplatform-Luna-Region-Intelligence-Protocol-Alignment-Post-Review-v1-001"

UPSTREAM_REVIEW_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_POST_REVIEW_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_post_review_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_post_review_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_dryrun_review_v1.json"
    ),
}


def _load_json(repo_root: Path, rel: str) -> Dict[str, Any]:
    path = repo_root / rel
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _build_report(*, summary: Dict[str, Any], decision: str) -> str:
    return "\n".join([
        "# Document Surface Detector Implementation — Post-Review Report v1",
        "",
        f"**Phase:** Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Post-Review-v1-001",
        f"**Final decision:** `{decision}`",
        f"**Boundary status:** `{summary.get('boundary_status')}`",
        f"**Protocol compliance:** `{summary.get('protocol_compliance_passed')}`",
        "",
        "## 协议框架",
        "",
        "existing_midplatform_protocol_chain_extension=true",
        "protocol_patch_not_new_branch=true",
        "",
        f"**Recommended next:** `{summary.get('recommended_next_phase')}`",
        f"**Parallel track:** `{summary.get('parallel_next_track')}`",
        f"**Later protocol alignment:** `{summary.get('later_protocol_alignment_phase')}`",
        "",
        "## Unresolved risks",
        "",
        *[f"- `{r}`" for r in summary.get("unresolved_risks") or []],
        "",
    ]) + "\n"


def run_document_surface_implementation_post_review(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    blockers: List[str] = []

    for go_id, rel in UPSTREAM_REVIEW_PATHS.items():
        if _load_json(root, rel).get("final_decision") != go_id:
            blockers.append(f"upstream.missing={go_id}")

    planning = review_implementation_planning()
    dryrun = review_implementation_dryrun(repo_root=root)
    contract = review_implementation_contract()
    protocol = review_protocol_compliance(repo_root=root)
    benchmark = review_implementation_benchmark(repo_root=root)
    guards = review_implementation_guards(repo_root=root, protocol_review=protocol)
    risks = build_implementation_risk_registry()

    reviews = [planning, dryrun, contract, protocol, benchmark, guards]
    if not all(r.get("passed") for r in reviews):
        blockers.append("implementation.post_review_incomplete")
    if not protocol.get("protocol_compliance_passed"):
        blockers.append("protocol_compliance.failed")

    review_passed = sum(r.get("review_passed_count", 1 if r.get("passed") else 0) for r in reviews if "review_passed_count" in r)
    review_passed += sum(1 for r in reviews if r.get("passed") and "review_passed_count" not in r)
    review_failed = sum(r.get("review_failed_count", 0) for r in reviews)

    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Post-Review-v1-001",
        "runtime_id": "document_surface_detector_v1",
        "implementation_mode_candidate": "classical_cv_boundary_v1",
        "first_real_implementation_candidate": "option_a_classical_cv_boundary",
        "post_review_only": True,
        "real_execution_enabled": False,
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "protocol_compliance_check": "required",
        "protocol_compliance_passed": protocol.get("protocol_compliance_passed") is True,
        "planning_review_passed": planning.get("passed"),
        "dryrun_review_passed": dryrun.get("passed"),
        "contract_review_passed": contract.get("passed"),
        "benchmark_review_passed": benchmark.get("passed"),
        "guard_review_passed": guards.get("passed"),
        "review_passed_count": review_passed,
        "review_failed_count": review_failed,
        "blocker_count": len(blockers),
        "failed_checks": blockers,
        "boundary_status": "frozen" if decision == FINAL_GO else "blocked",
        "unresolved_risks": risks.get("unresolved_risks"),
        "recommended_next_phase": RECOMMENDED_NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL_NEXT_TRACK if decision == FINAL_GO else None,
        "later_protocol_alignment_phase": LATER_PROTOCOL_ALIGNMENT,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
    }

    report_md = _build_report(summary=summary, decision=decision)
    out_dir = root / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_post_review_v1"

    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "document_surface_implementation_post_review_summary_v1.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "document_surface_implementation_contract_review_v1.json").write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "document_surface_implementation_protocol_compliance_review_v1.json").write_text(json.dumps(protocol, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "document_surface_implementation_guard_review_v1.json").write_text(json.dumps(guards, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "document_surface_implementation_benchmark_review_v1.json").write_text(json.dumps(benchmark, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "document_surface_implementation_risk_registry_v1.json").write_text(json.dumps(risks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "document_surface_implementation_post_review_report_v1.md").write_text(report_md, encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {**summary, "planning_review": planning, "dryrun_review": dryrun, "contract_review": contract,
            "protocol_review": protocol, "benchmark_review": benchmark, "guard_review": guards, "risk_registry": risks}

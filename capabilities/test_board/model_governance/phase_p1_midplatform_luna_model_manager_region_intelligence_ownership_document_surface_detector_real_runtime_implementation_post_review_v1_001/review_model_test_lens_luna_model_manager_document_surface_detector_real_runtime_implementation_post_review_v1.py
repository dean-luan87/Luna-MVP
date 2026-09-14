# -*- coding: utf-8 -*-
"""P1 Document Surface Detector — implementation post-review v1."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[4]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Post-Review-v1-001"
IPR_REL = "capabilities/midplatform/model_manager/runtime/document_surface/implementation_post_review"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_post_review_v1_001"
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_POST_REVIEW_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_POST_REVIEW_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Planning-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{IPR_REL}/document_surface_implementation_post_review_policy_v1.json",
    f"{IPR_REL}/document_surface_implementation_post_review_adapter_v1.py",
    f"{IPR_REL}/document_surface_implementation_planning_reviewer_v1.py",
    f"{IPR_REL}/document_surface_implementation_dryrun_reviewer_v1.py",
    f"{IPR_REL}/document_surface_implementation_contract_reviewer_v1.py",
    f"{IPR_REL}/document_surface_implementation_protocol_compliance_reviewer_v1.py",
    f"{IPR_REL}/document_surface_implementation_benchmark_reviewer_v1.py",
    f"{IPR_REL}/document_surface_implementation_guard_reviewer_v1.py",
    f"{IPR_REL}/document_surface_implementation_risk_registry_v1.py",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_implementation_post_review_types_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_real_runtime_implementation_post_review_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_real_runtime_implementation_post_review_v1.py",
)

REVIEW_CHECKS: Tuple[Dict[str, str], ...] = tuple(
    {"check_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("adapter", "Post-Review Adapter"),
        ("planning", "Implementation Planning 审查"),
        ("dryrun", "Implementation DryRun 审查"),
        ("contract", "Contract 冻结审查"),
        ("protocol", "Protocol Compliance 审查"),
        ("benchmark", "Benchmark 审查"),
        ("guards", "Negative Guard 回归"),
        ("risks", "Risk Registry"),
        ("protocol_compliance_passed", "protocol_compliance_passed"),
        ("existing_protocol_chain", "existing_midplatform_protocol_chain_extension"),
        ("patch_not_new_branch", "protocol_patch_not_new_branch"),
        ("boundary_frozen", "boundary_status=frozen"),
        ("no_cv2", "无 cv2"),
        ("upstream_go", "上游 GO"),
        ("outputs", "输出文件齐全"),
        ("next_phase", "Controlled Execution Planning 推荐"),
    ], start=1)
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _audit() -> Dict[str, bool]:
    repo = _detect_repo_root()
    post: Dict[str, Any] = {}
    try:
        from capabilities.midplatform.model_manager.runtime.document_surface.implementation_post_review.document_surface_implementation_post_review_adapter_v1 import (  # noqa: WPS433
            run_document_surface_implementation_post_review,
        )
        from capabilities.midplatform.model_manager.runtime.document_surface.implementation_post_review.document_surface_implementation_risk_registry_v1 import (  # noqa: WPS433
            RISK_REGISTRY,
        )
        post = run_document_surface_implementation_post_review(repo_root=repo, write_outputs=True)
        risk_count = len(RISK_REGISTRY)
    except Exception:
        post = {"final_decision": FINAL_BLOCKED}
        risk_count = 0

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_post_review_v1"
    outputs_ok = all(
        (out_dir / f).is_file()
        for f in (
            "document_surface_implementation_post_review_summary_v1.json",
            "document_surface_implementation_contract_review_v1.json",
            "document_surface_implementation_protocol_compliance_review_v1.json",
            "document_surface_implementation_guard_review_v1.json",
            "document_surface_implementation_benchmark_review_v1.json",
            "document_surface_implementation_risk_registry_v1.json",
            "document_surface_implementation_post_review_report_v1.md",
        )
    )

    return {
        "adapter": "run_document_surface_implementation_post_review" in _read(f"{IPR_REL}/document_surface_implementation_post_review_adapter_v1.py"),
        "planning": post.get("planning_review_passed") is True,
        "dryrun": post.get("dryrun_review_passed") is True,
        "contract": post.get("contract_review_passed") is True,
        "protocol": post.get("protocol_compliance_passed") is True,
        "benchmark": post.get("benchmark_review_passed") is True,
        "guards": post.get("guard_review_passed") is True,
        "risks": risk_count >= 10,
        "protocol_compliance_passed": post.get("protocol_compliance_passed") is True,
        "existing_protocol_chain": post.get("existing_midplatform_protocol_chain_extension") is True,
        "patch_not_new_branch": post.get("protocol_patch_not_new_branch") is True,
        "boundary_frozen": post.get("boundary_status") == "frozen",
        "no_cv2": "import cv2" not in _read("capabilities/midplatform/model_manager/runtime/document_surface/implementation_dryrun/classical_boundary_candidate_pipeline_v1.py"),
        "upstream_go": post.get("blocker_count", 1) == 0,
        "outputs": outputs_ok,
        "next_phase": post.get("recommended_next_phase") == RECOMMENDED_NEXT_PHASE,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit()
    checks = []
    for spec in REVIEW_CHECKS:
        passed = bool(flags.get(spec["key"], False))
        checks.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"check.{spec['check_id']}.fail={spec['key']}")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_post_review_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    review_passed = sum(1 for c in checks if c["passed"])
    review_failed = len(checks) - review_passed

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "runtime_id": "document_surface_detector_v1",
        "post_review_only": True,
        "recommended_next_phase": RECOMMENDED_NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL_NEXT_TRACK if decision == FINAL_GO else None,
        "audit_flags": flags,
        "review_checks": checks,
        "review_passed_count": review_passed,
        "review_failed_count": review_failed,
        "blocker_count": len(failed),
        "boundary_status": "frozen" if decision == FINAL_GO else "blocked",
        "failed_checks": failed,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_post_review_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=root, module="model_governance", source_review_file=result.get("output_review_file"))
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=standin, module="model_governance", source_review_file=result.get("output_review_file"))
        result["test_board_root"] = str(tb.get("test_board_dir", TB_REL))

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "boundary_status": r.get("boundary_status"),
        "review_passed_count": r.get("review_passed_count"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "parallel_next_track": r.get("parallel_next_track"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

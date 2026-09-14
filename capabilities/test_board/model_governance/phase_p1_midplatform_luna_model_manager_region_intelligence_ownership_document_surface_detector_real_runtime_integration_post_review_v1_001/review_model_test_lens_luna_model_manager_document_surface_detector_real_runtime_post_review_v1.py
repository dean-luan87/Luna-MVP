# -*- coding: utf-8 -*-
"""P1 Document Surface Detector — real runtime integration post-review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Post-Review-v1-001"
PR_REL = "capabilities/midplatform/model_manager/runtime/document_surface/post_review"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_post_review_v1_001"
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_POST_REVIEW_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_POST_REVIEW_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Planning-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{PR_REL}/document_surface_detector_post_review_policy_v1.json",
    f"{PR_REL}/document_surface_detector_post_review_adapter_v1.py",
    f"{PR_REL}/document_surface_detector_contract_reviewer_v1.py",
    f"{PR_REL}/document_surface_detector_guard_reviewer_v1.py",
    f"{PR_REL}/document_surface_detector_risk_registry_v1.py",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_post_review_types_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_real_runtime_post_review_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_real_runtime_post_review_v1.py",
)

REVIEW_CHECKS: Tuple[Dict[str, str], ...] = tuple(
    {"check_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("post_review_adapter", "Post-Review Adapter"),
        ("contract_reviewer", "Contract Reviewer"),
        ("guard_reviewer", "Guard Reviewer"),
        ("risk_registry", "Risk Registry"),
        ("policy", "Post-Review Policy"),
        ("contract_pass", "Contract 审查通过"),
        ("guard_pass", "Guard 回归通过"),
        ("case_coverage", "8 Case 覆盖完整"),
        ("upstream_go", "上游 GO 齐全"),
        ("risk_registry_complete", "风险登记完整"),
        ("boundary_frozen", "边界冻结"),
        ("route_a_recommended", "Route A 推荐"),
        ("parallel_track_marked", "Route B parallel track"),
        ("no_real_model", "无真实模型接入"),
        ("output_artifacts", "输出文件齐全"),
    ], start=1)
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _audit(repo: Path) -> Dict[str, bool]:
    policy = json.loads(_read(f"{PR_REL}/document_surface_detector_post_review_policy_v1.json") or "{}")
    post_result: Dict[str, Any] = {}
    try:
        from capabilities.midplatform.model_manager.runtime.document_surface.post_review.document_surface_detector_post_review_adapter_v1 import (  # noqa: WPS433
            run_document_surface_detector_post_review,
        )
        from capabilities.midplatform.model_manager.runtime.document_surface.post_review.document_surface_detector_risk_registry_v1 import (  # noqa: WPS433
            RISK_REGISTRY,
        )
        post_result = run_document_surface_detector_post_review(repo_root=repo, write_outputs=True)
        risk_count = len(RISK_REGISTRY)
    except Exception:
        post_result = {"final_decision": FINAL_BLOCKED}
        risk_count = 0

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_post_review_v1"
    outputs = [
        "document_surface_detector_post_review_summary_v1.json",
        "document_surface_detector_contract_review_v1.json",
        "document_surface_detector_guard_review_v1.json",
        "document_surface_detector_risk_registry_v1.json",
        "document_surface_detector_post_review_report_v1.md",
    ]
    outputs_ok = all((out_dir / f).is_file() for f in outputs)

    return {
        "post_review_adapter": "run_document_surface_detector_post_review" in _read(f"{PR_REL}/document_surface_detector_post_review_adapter_v1.py"),
        "contract_reviewer": "review_contracts" in _read(f"{PR_REL}/document_surface_detector_contract_reviewer_v1.py"),
        "guard_reviewer": "review_guards" in _read(f"{PR_REL}/document_surface_detector_guard_reviewer_v1.py"),
        "risk_registry": "build_risk_registry" in _read(f"{PR_REL}/document_surface_detector_risk_registry_v1.py"),
        "policy": policy.get("schema_id") == "DocumentSurfaceDetectorPostReviewPolicyV1",
        "contract_pass": post_result.get("contract_review_passed") is True,
        "guard_pass": post_result.get("guard_review_passed") is True,
        "case_coverage": post_result.get("case_coverage_complete") is True,
        "upstream_go": post_result.get("blocker_count", 1) == 0 or all(
            not str(b).startswith("upstream.") for b in post_result.get("failed_checks", [])
        ),
        "risk_registry_complete": risk_count >= 7,
        "boundary_frozen": post_result.get("boundary_status") == "frozen",
        "route_a_recommended": post_result.get("recommended_next_phase") == RECOMMENDED_NEXT_PHASE,
        "parallel_track_marked": post_result.get("parallel_next_track") == PARALLEL_NEXT_TRACK,
        "no_real_model": policy.get("forbidden_actions", []) and "no_real_model_execution" in policy.get("forbidden_actions", []),
        "output_artifacts": outputs_ok,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    repo = _detect_repo_root()
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit(repo)
    checks = []
    for spec in REVIEW_CHECKS:
        passed = bool(flags.get(spec["key"], False))
        checks.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"check.{spec['check_id']}.fail={spec['key']}")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_post_review_v1_review_v0"
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
        "known_limits": ["post_review_only", "no_real_model", "no_ocr", "no_vlm"],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_post_review_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(repo))
        try:
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=root, module="model_governance", source_review_file=result.get("output_review_file"))
        except (OSError, PermissionError, TypeError):
            standin = repo / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=standin, module="model_governance", source_review_file=result.get("output_review_file"))
        result["test_board_root"] = str(tb.get("test_board_dir", TB_REL))

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "review_passed_count": r.get("review_passed_count"),
        "review_failed_count": r.get("review_failed_count"),
        "boundary_status": r.get("boundary_status"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "parallel_next_track": r.get("parallel_next_track"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

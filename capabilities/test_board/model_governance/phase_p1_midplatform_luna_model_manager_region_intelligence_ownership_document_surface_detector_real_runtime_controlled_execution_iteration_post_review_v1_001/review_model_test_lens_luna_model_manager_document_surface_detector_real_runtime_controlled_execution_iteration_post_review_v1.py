# -*- coding: utf-8 -*-
"""P1 Document Surface Detector — iteration post-review lens v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-Post-Review-v1-001"
IPR_REL = "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_iteration_post_review"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_post_review_v1_001"
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_POST_REVIEW_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_POST_REVIEW_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-v2-Planning-v1-001"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{IPR_REL}/document_surface_iteration_post_review_adapter_v1.py",
    f"{IPR_REL}/document_surface_iteration_boundary_reviewer_v1.py",
    f"{IPR_REL}/document_surface_iteration_case_reviewer_v1.py",
    f"{IPR_REL}/document_surface_iteration_strategy_reviewer_v1.py",
    f"{IPR_REL}/document_surface_iteration_metrics_reviewer_v1.py",
    f"{IPR_REL}/document_surface_iteration_fixture_semantic_reviewer_v1.py",
    f"{IPR_REL}/document_surface_iteration_risk_registry_v1.py",
    f"{IPR_REL}/document_surface_iteration_protocol_compliance_reviewer_v1.py",
    f"{IPR_REL}/document_surface_iteration_post_review_policy_v1.json",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_real_runtime_controlled_execution_iteration_post_review_v1.py",
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    repo = _detect_repo_root()
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_post_review.document_surface_iteration_post_review_adapter_v1 import (  # noqa: WPS433
        run_iteration_post_review,
    )

    result = run_iteration_post_review(repo_root=repo, write_outputs=True)
    if result.get("final_decision") != FINAL_GO:
        failed.append(f"post_review.not_go={result.get('final_decision')}")

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_post_review_v1"
    outputs_ok = all((out_dir / f).is_file() for f in (
        "iteration_post_review_summary.json",
        "iteration_case_quality_review.json",
        "iteration_strategy_review.json",
        "iteration_metrics_review.json",
        "iteration_risk_registry.json",
        "iteration_fixture_semantic_review.json",
        "iteration_post_review_report.md",
    ))
    if not outputs_ok:
        failed.append("outputs.incomplete")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_post_review_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    review_result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "post_review_only": True,
        "detector_rerun_forbidden": True,
        "runtime_activation_allowed": False,
        "boundary_status": result.get("boundary_status", "frozen"),
        "final_decision": decision,
        "post_review_final_decision": result.get("final_decision"),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "recommended_next_phase": NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL if decision == FINAL_GO else None,
        "quality_conclusion": result.get("quality_conclusion"),
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_post_review_review_v1.json"
        rp.write_text(json.dumps(review_result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        review_result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(repo))
        try:
            tb = write_test_board_records(review_result, test_mode="dry_run", repo_root=root, module="model_governance", source_review_file=review_result.get("output_review_file"))
        except (OSError, PermissionError, TypeError):
            standin = repo / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(review_result, test_mode="dry_run", repo_root=standin, module="model_governance", source_review_file=review_result.get("output_review_file"))
        review_result["test_board_root"] = str(tb.get("test_board_dir", TB_REL))

    return review_result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "post_review_final_decision": r.get("post_review_final_decision"),
        "blocker_count": r["blocker_count"],
        "boundary_status": r.get("boundary_status"),
        "runtime_activation_allowed": False,
        "recommended_next_phase": r.get("recommended_next_phase"),
        "parallel_next_track": r.get("parallel_next_track"),
        "quality_conclusion": r.get("quality_conclusion"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

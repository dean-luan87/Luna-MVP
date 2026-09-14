# -*- coding: utf-8 -*-
"""P1 Document Surface — controlled execution post-review lens v1."""

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


from capabilities.test_board.test_board_protocol_v1 import TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1, write_test_board_records  # noqa: E402

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Post-Review-v1-001"
CEPR_REL = "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_post_review"
FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_POST_REVIEW_GO"
RECOMMENDED_NEXT = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{CEPR_REL}/document_surface_controlled_execution_post_review_adapter_v1.py",
    f"{CEPR_REL}/document_surface_controlled_execution_boundary_reviewer_v1.py",
    f"{CEPR_REL}/document_surface_controlled_execution_case_reviewer_v1.py",
    f"{CEPR_REL}/document_surface_controlled_execution_metrics_reviewer_v1.py",
    f"{CEPR_REL}/document_surface_controlled_execution_candidate_quality_reviewer_v1.py",
    f"{CEPR_REL}/document_surface_controlled_execution_protocol_compliance_reviewer_v1.py",
    f"{CEPR_REL}/document_surface_controlled_execution_risk_registry_v1.py",
    f"{CEPR_REL}/document_surface_controlled_execution_post_review_policy_v1.json",
)


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    repo = _detect_repo_root()
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not (repo / rel).is_file():
            failed.append(f"file.missing={rel}")

    from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_post_review.document_surface_controlled_execution_post_review_adapter_v1 import (  # noqa: WPS433
        run_controlled_execution_post_review,
    )
    result = run_controlled_execution_post_review(repo_root=repo, write_outputs=True)
    if result.get("final_decision") != FINAL_GO:
        failed.append(f"post_review.not_go={result.get('final_decision')}")

    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_post_review_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)
    review_doc = {
        "phase_id": PHASE_ID,
        **{k: result[k] for k in (
            "final_decision", "boundary_status", "runtime_activation_allowed", "protocol_compliance_passed",
            "review_passed_count", "review_failed_count", "blocker_count", "failed_checks",
            "review_watch_items", "unresolved_risks", "recommended_next_phase", "parallel_next_track",
        ) if k in result},
        "dryrun_historical_note": "BLOCKED_BY_MISSING_FIXTURES is historical only",
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }
    rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_post_review_review_v1.json"
    if write_file:
        rp.write_text(json.dumps(review_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        review_doc["output_review_file"] = str(rp)

    if write_test_board and not failed:
        root = Path(test_board_root or str(repo))
        try:
            tb = write_test_board_records(review_doc, test_mode="dry_run", repo_root=root, module="model_governance", source_review_file=str(rp))
        except (OSError, PermissionError, TypeError):
            standin = repo / "_tmp_eval_out/board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(review_doc, test_mode="dry_run", repo_root=standin, module="model_governance", source_review_file=str(rp))
        review_doc["test_board_root"] = str(tb.get("test_board_dir", ""))

    review_doc["blocker_count"] = len(failed)
    review_doc["failed_checks"] = failed
    if failed:
        review_doc["final_decision"] = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_POST_REVIEW_BLOCKED"
    return review_doc


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "boundary_status": r.get("boundary_status"),
        "runtime_activation_allowed": r.get("runtime_activation_allowed"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "review_watch_items": r.get("review_watch_items"),
        "blocker_count": r.get("blocker_count"),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

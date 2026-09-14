# -*- coding: utf-8 -*-
"""P1 Document Surface — Option B preflight closure review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Preflight-Closure-v1-001"
CL_REL = "capabilities/midplatform/model_manager/runtime/document_surface/option_b_preflight_closure"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_preflight_closure_v1_001"
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_PREFLIGHT_CLOSURE_GO"
NEXT_CE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Controlled-Execution-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{CL_REL}/document_surface_option_b_preflight_closure_adapter_v1.py",
    f"{CL_REL}/document_surface_option_b_preflight_planning_adapter_v1.py",
    f"{CL_REL}/document_surface_option_b_preflight_dryrun_adapter_v1.py",
    f"{CL_REL}/document_surface_option_b_preflight_post_review_adapter_v1.py",
    f"{TB_REL}/luna_model_manager_document_surface_detector_option_b_preflight_closure_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_option_b_preflight_closure_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_option_b_preflight_closure_v1.py",
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

    from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_preflight_closure_adapter_v1 import (  # noqa: WPS433
        run_option_b_preflight_closure,
    )
    from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_preflight_closure_v1_001.luna_model_manager_document_surface_detector_option_b_preflight_closure_smoke_v1 import (  # noqa: E402
        run_smoke_cases,
    )

    result = run_option_b_preflight_closure(repo_root=repo, write_outputs=True)
    smoke = run_smoke_cases()
    if result.get("final_decision") != FINAL_GO:
        failed.append(f"closure.not_go={result.get('final_decision')}")

    out = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_preflight_closure_v1"
    required = [
        "option_b_preflight_closure_summary.json",
        "planning/option_b_preflight_planning_summary.json",
        "dryrun/option_b_preflight_dryrun_summary.json",
        "post_review/option_b_preflight_post_review_summary.json",
    ]
    if not all((out / p).is_file() for p in required):
        failed.append("outputs.incomplete")

    m = result.get("metrics") or {}
    flags = {
        "planning_go": str(result.get("preflight_planning_decision", "")).endswith("GO"),
        "dryrun_go": str(result.get("preflight_dryrun_decision", "")).endswith("GO"),
        "post_go": str(result.get("preflight_post_review_decision", "")).endswith("GO"),
        "no_preflight_exec": result.get("preflight_execution_allowed") is False,
        "no_option_b": result.get("option_b_execution_allowed") is False,
        "scope_2": m.get("preflight_candidate_count") == 2,
        "no_execution": m.get("execution_allowed_rate") == 0,
        "next_ce_planning": result.get("recommended_next_phase") == NEXT_CE,
        "smoke": smoke.get("smoke_passed") == 8,
    }
    for k, v in flags.items():
        if not v:
            failed.append(f"guard.fail={k}")

    decision = FINAL_GO if not failed else "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_PREFLIGHT_CLOSURE_BLOCKED"
    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_preflight_closure_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    review_result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "preflight_closure_only": True,
        "audit_flags": flags,
        "final_decision": decision,
        "closure_final_decision": result.get("final_decision"),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "preflight_closure_completed": result.get("preflight_closure_completed"),
        "recommended_next_phase": NEXT_CE if decision == FINAL_GO else None,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "candidate_only": True,
        "not_fact": True,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_preflight_closure_review_v1.json"
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
    print(json.dumps(r, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

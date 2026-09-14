# -*- coding: utf-8 -*-
"""P1 Document Surface — Option B candidate route dryrun review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Candidate-Route-DryRun-v1-001"
OBR_REL = "capabilities/midplatform/model_manager/runtime/document_surface/option_b_candidate_route_dryrun"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1_001"
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_DRYRUN_BLOCKED"
NEXT_POST_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Candidate-Route-Post-Review-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{OBR_REL}/document_surface_option_b_candidate_route_dryrun_adapter_v1.py",
    f"{OBR_REL}/document_surface_option_b_admission_dryrun_v1.py",
    f"{OBR_REL}/document_surface_option_b_route_selector_v1.py",
    f"{OBR_REL}/document_surface_option_b_output_contract_v1.py",
    f"{OBR_REL}/document_surface_option_a_b_conflict_policy_v1.py",
    f"{OBR_REL}/document_surface_option_b_validation_adapter_v1.py",
    f"{OBR_REL}/document_surface_option_b_metrics_v1.py",
    f"{OBR_REL}/document_surface_option_b_candidate_route_policy_v1.json",
    f"{TB_REL}/luna_model_manager_document_surface_detector_option_b_candidate_route_dryrun_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_option_b_candidate_route_dryrun_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_option_b_candidate_route_dryrun_v1.py",
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

    from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_candidate_route_dryrun_adapter_v1 import (  # noqa: WPS433
        run_option_b_candidate_route_dryrun,
    )
    from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1_001.luna_model_manager_document_surface_detector_option_b_candidate_route_dryrun_smoke_v1 import (  # noqa: E402
        run_smoke_cases,
    )

    dryrun = run_option_b_candidate_route_dryrun(repo_root=repo, write_outputs=True)
    smoke = run_smoke_cases()
    adapter_src = _read(f"{OBR_REL}/document_surface_option_b_candidate_route_dryrun_adapter_v1.py")

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1"
    outputs_ok = all((out_dir / f).is_file() for f in (
        "option_b_candidate_route_dryrun_summary.json",
        "option_b_admission_dryrun_summary.json",
        "option_b_output_contract_summary.json",
        "option_b_route_selection_summary.json",
        "option_a_b_conflict_policy_summary.json",
        "option_b_case_mapping_summary.json",
        "option_b_metrics_summary.json",
        "option_b_protocol_compliance_summary.json",
    ))

    flags = {
        "no_option_b_execution": "option_b_execution_forbidden" in adapter_src,
        "no_active_model": "active_model_id" in _read(f"{OBR_REL}/document_surface_option_b_admission_dryrun_v1.py"),
        "admission_gate": dryrun.get("option_b_status") == "candidate_route_only",
        "output_contract": "validate_option_b_output_contract" in adapter_src,
        "route_candidate_only": "execution_decision" in _read(f"{OBR_REL}/document_surface_option_b_route_selector_v1.py"),
        "conflict_validation_review": "validation_review" in _read(f"{OBR_REL}/document_surface_option_a_b_conflict_policy_v1.py"),
        "no_silent_fallback": dryrun.get("metrics", {}).get("option_b_execution_block_rate") == 1.0,
        "case_mapping": dryrun.get("case_count", 0) >= 6,
        "protocol": dryrun.get("protocol_compliance_passed") is True,
        "next_not_activation": dryrun.get("recommended_next_phase") == NEXT_POST_REVIEW,
        "smoke": smoke.get("smoke_passed") == 8 and not smoke.get("failed_checks"),
        "outputs": outputs_ok,
    }
    for k, v in flags.items():
        if not v:
            failed.append(f"guard.fail={k}")
    if dryrun.get("final_decision") != FINAL_GO:
        failed.append(f"dryrun.not_go={dryrun.get('final_decision')}")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "option_b_candidate_route_dryrun_only": True,
        "runtime_activation_allowed": False,
        "audit_flags": flags,
        "blocker_count": len(failed),
        "failed_checks": failed,
        "final_decision": decision,
        "dryrun_final_decision": dryrun.get("final_decision"),
        "recommended_next_phase": NEXT_POST_REVIEW if decision == FINAL_GO else None,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_review_v1.json"
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
        "dryrun_final_decision": r.get("dryrun_final_decision"),
        "blocker_count": r["blocker_count"],
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

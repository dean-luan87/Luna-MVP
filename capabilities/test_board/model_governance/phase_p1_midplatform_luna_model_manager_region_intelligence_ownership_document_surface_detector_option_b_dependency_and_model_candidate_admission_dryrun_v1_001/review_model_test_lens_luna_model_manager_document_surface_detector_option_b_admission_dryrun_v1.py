# -*- coding: utf-8 -*-
"""P1 Document Surface — Option B admission dryrun review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Dependency-And-Model-Candidate-Admission-DryRun-v1-001"
OBR_REL = "capabilities/midplatform/model_manager/runtime/document_surface/option_b_admission_dryrun"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_dryrun_v1_001"
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_DRYRUN_BLOCKED"
NEXT_POST_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Dependency-And-Model-Candidate-Admission-Post-Review-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{OBR_REL}/document_surface_option_b_admission_dryrun_plan_v1.md",
    f"{OBR_REL}/document_surface_option_b_admission_dryrun_policy_v1.json",
    f"{OBR_REL}/document_surface_option_b_candidate_fixture_registry_v1.py",
    f"{OBR_REL}/document_surface_option_b_dependency_admission_dryrun_v1.py",
    f"{OBR_REL}/document_surface_option_b_model_candidate_admission_dryrun_v1.py",
    f"{OBR_REL}/document_surface_option_b_license_weight_dryrun_v1.py",
    f"{OBR_REL}/document_surface_option_b_output_contract_dryrun_v1.py",
    f"{OBR_REL}/document_surface_option_b_wrapper_requirement_dryrun_v1.py",
    f"{OBR_REL}/document_surface_option_b_abort_rollback_dryrun_v1.py",
    f"{OBR_REL}/document_surface_option_b_admission_dryrun_metrics_v1.py",
    f"{OBR_REL}/document_surface_option_b_admission_dryrun_adapter_v1.py",
    f"{TB_REL}/luna_model_manager_document_surface_detector_option_b_admission_dryrun_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_option_b_admission_dryrun_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_option_b_admission_dryrun_v1.py",
)

OUTPUT_FILES = (
    "option_b_admission_dryrun_summary.json",
    "option_b_candidate_fixture_registry.json",
    "option_b_dependency_admission_results.json",
    "option_b_model_candidate_admission_results.json",
    "option_b_license_weight_results.json",
    "option_b_output_contract_results.json",
    "option_b_wrapper_requirement_results.json",
    "option_b_abort_rollback_results.json",
    "option_b_admission_dryrun_metrics.json",
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

    from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_dryrun.document_surface_option_b_admission_dryrun_adapter_v1 import (  # noqa: WPS433
        run_option_b_admission_dryrun,
    )
    from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_dryrun_v1_001.luna_model_manager_document_surface_detector_option_b_admission_dryrun_smoke_v1 import (  # noqa: E402
        run_smoke_cases,
    )

    dryrun = run_option_b_admission_dryrun(repo_root=repo, write_outputs=True)
    smoke = run_smoke_cases()
    adapter_src = _read(f"{OBR_REL}/document_surface_option_b_admission_dryrun_adapter_v1.py")
    results = dryrun.get("results") or []
    by_id = {r["model_candidate_id"]: r for r in results}

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_dryrun_v1"
    outputs_ok = all((out_dir / f).is_file() for f in OUTPUT_FILES)

    blocked = [r for r in results if str(r.get("admission_status_candidate", "")).startswith("blocked")]
    abort_ok = all(
        (r.get("abort_rollback") or {}).get("abort_reason")
        and (r.get("abort_rollback") or {}).get("rollback_action")
        for r in blocked
    )

    flags = {
        "no_option_b_execution": dryrun.get("option_b_execution_allowed") is False,
        "no_segmentation_execution": dryrun.get("segmentation_execution_forbidden") is True,
        "no_active_model_selection": dryrun.get("option_b_active_model_selected") is False,
        "no_model_download": dryrun.get("model_download_forbidden") is True,
        "no_dependency_install": dryrun.get("dependency_install_forbidden") is True,
        "fixtures_complete": dryrun.get("fixture_count") == 8,
        "a1_c1_preflight_only": all(
            by_id.get(cid, {}).get("admission_status_candidate") == "admitted_for_preflight_candidate"
            and by_id.get(cid, {}).get("execution_allowed") is False
            for cid in (
                "family_a_classical_helper_ok_candidate",
                "family_c_document_specific_surface_model_ok_for_preflight",
            )
        ),
        "blocks_correct": all(r.get("expectation_met") for r in results),
        "b3_wrapper": by_id.get("family_b_sam_like_caption_or_text_default", {}).get("admission_status_candidate") == "blocked_or_requires_wrapper_candidate",
        "abort_rollback": abort_ok,
        "metrics_complete": dryrun.get("metrics", {}).get("execution_block_rate") == 1.0,
        "protocol": dryrun.get("protocol_compliance_passed") is True,
        "next_not_execution": dryrun.get("recommended_next_phase") == NEXT_POST_REVIEW,
        "smoke": smoke.get("smoke_passed") == 8 and not smoke.get("failed_checks"),
        "outputs": outputs_ok,
        "no_runtime_activation": dryrun.get("runtime_activation_allowed") is False,
        "no_preflight_execution": dryrun.get("preflight_execution_forbidden") is True,
        "no_controlled_execution": dryrun.get("controlled_execution_forbidden") is True,
        "protocol_chain_extension": "existing_midplatform_protocol_chain_extension" in adapter_src,
    }
    for k, v in flags.items():
        if not v:
            failed.append(f"guard.fail={k}")
    if dryrun.get("final_decision") != FINAL_GO:
        failed.append(f"dryrun.not_go={dryrun.get('final_decision')}")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "admission_dryrun_only": True,
        "runtime_activation_allowed": False,
        "audit_flags": flags,
        "blocker_count": len(failed),
        "failed_checks": failed,
        "final_decision": decision,
        "dryrun_final_decision": dryrun.get("final_decision"),
        "recommended_next_phase": NEXT_POST_REVIEW if decision == FINAL_GO else None,
        "parallel_next_track": dryrun.get("parallel_next_track"),
        "metrics": dryrun.get("metrics"),
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "candidate_only": True,
        "not_fact": True,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_dryrun_review_v1.json"
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
    print(json.dumps({k: v for k, v in r.items() if k not in ("metrics",)}, indent=2, ensure_ascii=False))
    return 0 if r.get("final_decision") == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

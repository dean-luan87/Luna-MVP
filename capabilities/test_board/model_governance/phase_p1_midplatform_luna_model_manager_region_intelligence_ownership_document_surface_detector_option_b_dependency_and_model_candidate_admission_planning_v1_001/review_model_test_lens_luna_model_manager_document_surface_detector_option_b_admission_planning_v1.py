# -*- coding: utf-8 -*-
"""P1 Document Surface — Option B admission planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Dependency-And-Model-Candidate-Admission-Planning-v1-001"
AP_REL = "capabilities/midplatform/model_manager/runtime/document_surface/option_b_admission_planning"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_planning_v1_001"
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Dependency-And-Model-Candidate-Admission-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{AP_REL}/document_surface_option_b_admission_planning_adapter_v1.py",
    f"{AP_REL}/document_surface_option_b_model_candidate_types_v1.py",
    f"{AP_REL}/document_surface_option_b_candidate_registry_schema_v1.json",
    f"{AP_REL}/document_surface_option_b_dependency_admission_policy_v1.json",
    f"{AP_REL}/document_surface_option_b_model_candidate_admission_policy_v1.json",
    f"{AP_REL}/document_surface_option_b_license_and_weight_policy_v1.json",
    f"{AP_REL}/document_surface_option_b_output_contract_compatibility_v1.py",
    f"{AP_REL}/document_surface_option_b_preflight_requirements_v1.py",
    f"{AP_REL}/document_surface_option_b_abort_rollback_policy_v1.json",
    f"{AP_REL}/document_surface_option_b_admission_plan_v1.md",
    f"{TB_REL}/luna_model_manager_document_surface_detector_option_b_admission_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_option_b_admission_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_option_b_admission_planning_v1.py",
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

    from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_planning.document_surface_option_b_admission_planning_adapter_v1 import (  # noqa: WPS433
        run_option_b_admission_planning,
    )
    from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_planning_v1_001.luna_model_manager_document_surface_detector_option_b_admission_planning_smoke_v1 import (  # noqa: E402
        run_smoke_cases,
    )

    planning = run_option_b_admission_planning(repo_root=repo, write_outputs=True)
    smoke = run_smoke_cases()
    license_policy = json.loads(_read(f"{AP_REL}/document_surface_option_b_license_and_weight_policy_v1.json") or "{}")

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_planning_v1"
    outputs_ok = all((out_dir / f).is_file() for f in (
        "option_b_admission_planning_summary.json",
        "option_b_candidate_family_evaluation.json",
        "option_b_dependency_admission_policy_summary.json",
        "option_b_preflight_requirements_summary.json",
        "option_b_abort_rollback_policy_summary.json",
    ))

    flags = {
        "no_execution": planning.get("option_b_execution_forbidden") is True,
        "no_active_model": planning.get("option_b_active_model_selected") is False,
        "families_abcd": planning.get("families", {}).get("all_families_abcd_evaluated") is True,
        "registry_schema": planning.get("registry_review", {}).get("schema_complete") is True,
        "dependency_blocks": planning.get("dependency_policy", {}).get("install_allowed") is False,
        "license_blocks": len(license_policy.get("block_conditions") or []) >= 8,
        "output_contract": planning.get("output_contract", {}).get("caption_text_semantic_blocked_or_wrapper") is True,
        "preflight": planning.get("preflight", {}).get("all_checks_required") is True,
        "abort_rollback": len(planning.get("abort_rollback", {}).get("abort_conditions") or []) >= 12,
        "protocol": planning.get("protocol_compliance_passed") is True,
        "next_dryrun_not_execution": planning.get("recommended_next_phase") == NEXT_PHASE,
        "smoke": smoke.get("smoke_passed") == 8 and not smoke.get("failed_checks"),
        "outputs": outputs_ok,
    }
    for k, v in flags.items():
        if not v:
            failed.append(f"guard.fail={k}")
    if planning.get("final_decision") != FINAL_GO:
        failed.append(f"planning.not_go={planning.get('final_decision')}")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "admission_planning_only": True,
        "option_b_execution_allowed": False,
        "option_b_active_model_selected": False,
        "audit_flags": flags,
        "blocker_count": len(failed),
        "failed_checks": failed,
        "final_decision": decision,
        "planning_final_decision": planning.get("final_decision"),
        "recommended_next_phase": NEXT_PHASE if decision == FINAL_GO else None,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_planning_review_v1.json"
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
        "planning_final_decision": r.get("planning_final_decision"),
        "blocker_count": r["blocker_count"],
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

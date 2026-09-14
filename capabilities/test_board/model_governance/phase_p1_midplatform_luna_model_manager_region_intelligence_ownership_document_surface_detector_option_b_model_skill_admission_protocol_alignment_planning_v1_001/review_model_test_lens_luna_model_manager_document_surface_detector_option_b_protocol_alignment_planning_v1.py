# -*- coding: utf-8 -*-
"""P1 Document Surface — Option B protocol alignment planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Model-Skill-Admission-Protocol-Alignment-Planning-v1-001"
PLAN_REL = "capabilities/midplatform/model_manager/runtime/document_surface/option_b_protocol_alignment_planning"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_planning_v1_001"
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Model-Skill-Admission-Protocol-Alignment-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{PLAN_REL}/document_surface_option_b_model_skill_admission_protocol_alignment_plan_v1.md",
    f"{PLAN_REL}/document_surface_option_b_protocol_alignment_planning_adapter_v1.py",
    f"{PLAN_REL}/document_surface_option_b_model_skill_admission_contract_mapping_v1.py",
    f"{PLAN_REL}/document_surface_option_b_model_candidate_registry_alignment_v1.py",
    f"{PLAN_REL}/document_surface_option_b_dependency_admission_protocol_mapping_v1.py",
    f"{PLAN_REL}/document_surface_option_b_output_contract_protocol_mapping_v1.py",
    f"{PLAN_REL}/document_surface_option_b_permission_runtime_boundary_mapping_v1.py",
    f"{PLAN_REL}/document_surface_option_b_change_control_freeze_mapping_v1.py",
    f"{PLAN_REL}/document_surface_option_b_protocol_alignment_review_v1.py",
    f"{TB_REL}/luna_model_manager_document_surface_detector_option_b_protocol_alignment_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_option_b_protocol_alignment_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_option_b_protocol_alignment_planning_v1.py",
)

OUTPUT_FILES = (
    "option_b_protocol_alignment_planning_summary.json",
    "option_b_model_skill_admission_contract_mapping_v1.json",
    "option_b_model_candidate_registry_alignment_v1.json",
    "option_b_dependency_admission_protocol_mapping_v1.json",
    "option_b_output_contract_protocol_mapping_v1.json",
    "option_b_permission_runtime_boundary_mapping_v1.json",
    "option_b_change_control_freeze_mapping_v1.json",
    "option_b_protocol_alignment_review_v1.json",
    "option_b_model_skill_admission_protocol_alignment_plan_v1.md",
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

    from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_planning.document_surface_option_b_protocol_alignment_planning_adapter_v1 import (  # noqa: WPS433
        run_option_b_protocol_alignment_planning,
    )
    from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_planning_v1_001.luna_model_manager_document_surface_detector_option_b_protocol_alignment_planning_smoke_v1 import (  # noqa: E402
        run_smoke_cases,
    )

    planning = run_option_b_protocol_alignment_planning(repo_root=repo, write_outputs=True)
    smoke = run_smoke_cases()
    if planning.get("final_decision") != FINAL_GO:
        failed.append(f"planning.not_go={planning.get('final_decision')}")

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_planning_v1"
    if not all((out_dir / f).is_file() for f in OUTPUT_FILES):
        failed.append("outputs.incomplete")

    fs = planning.get("option_b_frozen_state") or {}
    flags = {
        "contract_mapped": planning.get("primary_contract") is not None,
        "chain_extension": planning.get("existing_midplatform_protocol_chain_extension") is True,
        "not_new_branch": planning.get("protocol_patch_not_new_branch") is True,
        "no_execution": planning.get("option_b_execution_allowed") is False,
        "no_active_model": planning.get("option_b_active_model_selected") is False,
        "model_candidate_route": fs.get("model_candidate_route") is True,
        "skill_candidate_route": fs.get("skill_candidate_route") is True,
        "preflight_required": fs.get("preflight_required") is True,
        "alignment_review": planning.get("alignment_review_passed") is True,
        "next_is_dryrun": planning.get("recommended_next_phase") == NEXT_PHASE,
        "smoke": smoke.get("smoke_passed") == 8 and not smoke.get("failed_checks"),
    }
    for k, v in flags.items():
        if not v:
            failed.append(f"guard.fail={k}")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "protocol_alignment_planning_only": True,
        "audit_flags": flags,
        "final_decision": decision,
        "planning_final_decision": planning.get("final_decision"),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "governance_conclusion": planning.get("governance_conclusion"),
        "adjusted_pipeline": planning.get("adjusted_pipeline"),
        "recommended_next_phase": NEXT_PHASE if decision == FINAL_GO else None,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "candidate_only": True,
        "not_fact": True,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_planning_review_v1.json"
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
    print(json.dumps(r, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

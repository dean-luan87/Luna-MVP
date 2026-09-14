# -*- coding: utf-8 -*-
"""P1 Document Surface — Option B protocol alignment dryrun review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Model-Skill-Admission-Protocol-Alignment-DryRun-v1-001"
DR_REL = "capabilities/midplatform/model_manager/runtime/document_surface/option_b_protocol_alignment_dryrun"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_dryrun_v1_001"
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_DRYRUN_BLOCKED"
NEXT_POST_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Model-Skill-Admission-Protocol-Alignment-Post-Review-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{DR_REL}/document_surface_option_b_protocol_alignment_dryrun_adapter_v1.py",
    f"{DR_REL}/document_surface_option_b_model_skill_admission_contract_dryrun_v1.py",
    f"{DR_REL}/document_surface_option_b_registry_alignment_dryrun_v1.py",
    f"{DR_REL}/document_surface_option_b_dependency_protocol_mapping_dryrun_v1.py",
    f"{DR_REL}/document_surface_option_b_output_contract_protocol_mapping_dryrun_v1.py",
    f"{DR_REL}/document_surface_option_b_runtime_boundary_protocol_mapping_dryrun_v1.py",
    f"{DR_REL}/document_surface_option_b_permission_admission_mapping_dryrun_v1.py",
    f"{DR_REL}/document_surface_option_b_change_control_mapping_dryrun_v1.py",
    f"{DR_REL}/document_surface_option_b_evidence_chain_mapping_dryrun_v1.py",
    f"{DR_REL}/document_surface_option_b_protocol_alignment_metrics_v1.py",
    f"{TB_REL}/luna_model_manager_document_surface_detector_option_b_protocol_alignment_dryrun_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_option_b_protocol_alignment_dryrun_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_option_b_protocol_alignment_dryrun_v1.py",
)

OUTPUT_FILES = (
    "option_b_protocol_alignment_dryrun_summary.json",
    "option_b_model_skill_contract_mapping_results.json",
    "option_b_registry_alignment_results.json",
    "option_b_dependency_protocol_mapping_results.json",
    "option_b_output_contract_protocol_mapping_results.json",
    "option_b_runtime_boundary_mapping_results.json",
    "option_b_permission_admission_mapping_results.json",
    "option_b_change_control_mapping_results.json",
    "option_b_evidence_chain_mapping_results.json",
    "option_b_protocol_alignment_metrics.json",
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

    from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_dryrun.document_surface_option_b_protocol_alignment_dryrun_adapter_v1 import (  # noqa: WPS433
        run_option_b_protocol_alignment_dryrun,
    )
    from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_dryrun_v1_001.luna_model_manager_document_surface_detector_option_b_protocol_alignment_dryrun_smoke_v1 import (  # noqa: E402
        run_smoke_cases,
    )

    dryrun = run_option_b_protocol_alignment_dryrun(repo_root=repo, write_outputs=True)
    smoke = run_smoke_cases()
    chain = _load_chain(repo)

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_dryrun_v1"
    if not all((out_dir / f).is_file() for f in OUTPUT_FILES):
        failed.append("outputs.incomplete")

    m = dryrun.get("metrics") or {}
    flags = {
        "no_preflight_planning": dryrun.get("preflight_planning_forbidden") is True,
        "no_option_b_execution": dryrun.get("option_b_execution_allowed") is False,
        "no_active_model": m.get("active_model_mapping_count") == 0,
        "no_active_skill": m.get("active_skill_mapping_count") == 0,
        "no_registry_update": m.get("active_registry_update_count") == 0,
        "contract_mapped_8": (dryrun.get("contract_mapping") or {}).get("all_mapped") is True,
        "preflight_2_blocked_6": m.get("preflight_candidate_mapping_count") == 2 and m.get("blocked_candidate_mapping_count") == 6,
        "protocol_chain": "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1" in chain,
        "not_new_branch": dryrun.get("protocol_patch_not_new_branch") is True,
        "next_post_review": dryrun.get("recommended_next_phase") == NEXT_POST_REVIEW,
        "smoke": smoke.get("smoke_passed") == 8 and not smoke.get("failed_checks"),
        "metrics_complete": m.get("protocol_ref_completeness_rate") == 1.0,
    }
    for k, v in flags.items():
        if not v:
            failed.append(f"guard.fail={k}")
    if dryrun.get("final_decision") != FINAL_GO:
        failed.append(f"dryrun.not_go={dryrun.get('final_decision')}")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "protocol_alignment_dryrun_only": True,
        "audit_flags": flags,
        "final_decision": decision,
        "dryrun_final_decision": dryrun.get("final_decision"),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "governance_conclusion": dryrun.get("governance_conclusion"),
        "recommended_next_phase": NEXT_POST_REVIEW if decision == FINAL_GO else None,
        "parallel_next_track": dryrun.get("parallel_next_track"),
        "metrics": m,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "candidate_only": True,
        "not_fact": True,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_dryrun_review_v1.json"
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


def _load_chain(repo: Path) -> List[str]:
    p = repo / "capabilities/midplatform/protocols/region_intelligence_protocol_chain_v1.json"
    if not p.is_file():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return [x.get("protocol_ref", "") for x in data.get("legacy_protocols_required") or []]


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({k: v for k, v in r.items() if k != "metrics"}, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

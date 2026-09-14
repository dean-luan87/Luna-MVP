# -*- coding: utf-8 -*-
"""P1 Document Surface — Option B preflight planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Preflight-Planning-v1-001"
PLAN_REL = "capabilities/midplatform/model_manager/runtime/document_surface/option_b_preflight_planning"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_preflight_planning_v1_001"
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_PREFLIGHT_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_PREFLIGHT_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Preflight-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{PLAN_REL}/document_surface_option_b_preflight_plan_v1.md",
    f"{PLAN_REL}/document_surface_option_b_preflight_planning_adapter_v1.py",
    f"{PLAN_REL}/document_surface_option_b_preflight_candidate_scope_v1.py",
    f"{PLAN_REL}/document_surface_option_b_dependency_availability_check_plan_v1.py",
    f"{PLAN_REL}/document_surface_option_b_model_weight_presence_check_plan_v1.py",
    f"{PLAN_REL}/document_surface_option_b_license_check_plan_v1.py",
    f"{PLAN_REL}/document_surface_option_b_input_boundary_check_plan_v1.py",
    f"{PLAN_REL}/document_surface_option_b_output_boundary_check_plan_v1.py",
    f"{PLAN_REL}/document_surface_option_b_raw_output_normalization_check_plan_v1.py",
    f"{PLAN_REL}/document_surface_option_b_candidate_schema_compliance_check_plan_v1.py",
    f"{PLAN_REL}/document_surface_option_b_no_text_fact_leak_check_plan_v1.py",
    f"{PLAN_REL}/document_surface_option_b_runtime_trace_check_plan_v1.py",
    f"{PLAN_REL}/document_surface_option_b_preflight_abort_rollback_policy_v1.json",
    f"{TB_REL}/luna_model_manager_document_surface_detector_option_b_preflight_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_option_b_preflight_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_option_b_preflight_planning_v1.py",
)

OUTPUT_FILES = (
    "option_b_preflight_planning_summary.json",
    "option_b_preflight_candidate_scope.json",
    "option_b_dependency_availability_check_plan.json",
    "option_b_model_weight_presence_check_plan.json",
    "option_b_license_check_plan.json",
    "option_b_input_boundary_check_plan.json",
    "option_b_output_boundary_check_plan.json",
    "option_b_raw_output_normalization_check_plan.json",
    "option_b_candidate_schema_compliance_check_plan.json",
    "option_b_no_text_fact_leak_check_plan.json",
    "option_b_runtime_trace_check_plan.json",
    "option_b_preflight_abort_rollback_policy.json",
    "option_b_preflight_metrics_plan.json",
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

    from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_preflight_planning_adapter_v1 import (  # noqa: WPS433
        run_option_b_preflight_planning,
    )
    from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_preflight_planning_v1_001.luna_model_manager_document_surface_detector_option_b_preflight_planning_smoke_v1 import (  # noqa: E402
        run_smoke_cases,
    )

    planning = run_option_b_preflight_planning(repo_root=repo, write_outputs=True)
    smoke = run_smoke_cases()
    if planning.get("final_decision") != FINAL_GO:
        failed.append(f"planning.not_go={planning.get('final_decision')}")

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_preflight_planning_v1"
    if not all((out_dir / f).is_file() for f in OUTPUT_FILES):
        failed.append("outputs.incomplete")

    scope = planning.get("scope") or {}
    flags = {
        "no_preflight_execution": planning.get("preflight_execution_allowed") is False,
        "no_option_b_execution": planning.get("option_b_execution_allowed") is False,
        "no_active_model": planning.get("active_model_selected") is False,
        "scope_a1_c1_only": scope.get("preflight_candidate_count") == 2,
        "checks_planned": len((planning.get("abort_policy") or {}).get("abort_conditions") or []) >= 16,
        "trace_complete": len((planning.get("trace_plan") or {}).get("required_trace_fields") or []) >= 16,
        "no_image_read": (planning.get("input_plan") or {}).get("image_read_allowed") is False,
        "next_preflight_dryrun": planning.get("recommended_next_phase") == NEXT_PHASE,
        "protocol": planning.get("protocol_compliance_passed") is True,
        "smoke": smoke.get("smoke_passed") == 8 and not smoke.get("failed_checks"),
    }
    for k, v in flags.items():
        if not v:
            failed.append(f"guard.fail={k}")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_preflight_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "preflight_planning_only": True,
        "audit_flags": flags,
        "final_decision": decision,
        "planning_final_decision": planning.get("final_decision"),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "preflight_planning_completed": planning.get("preflight_planning_completed"),
        "recommended_next_phase": NEXT_PHASE if decision == FINAL_GO else None,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "candidate_only": True,
        "not_fact": True,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_preflight_planning_review_v1.json"
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

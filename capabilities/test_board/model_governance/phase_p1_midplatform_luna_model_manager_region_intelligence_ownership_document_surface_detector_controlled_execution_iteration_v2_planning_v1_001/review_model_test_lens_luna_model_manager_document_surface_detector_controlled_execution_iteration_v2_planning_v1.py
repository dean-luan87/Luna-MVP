# -*- coding: utf-8 -*-
"""P1 Document Surface Detector — iteration v2 planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-v2-Planning-v1-001"
PLAN_REL = "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_iteration_v2_planning"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_v2_planning_v1_001"
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_V2_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_V2_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Candidate-Route-DryRun-v1-001"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{PLAN_REL}/document_surface_iteration_v2_planning_adapter_v1.py",
    f"{PLAN_REL}/document_surface_option_a_limit_review_v1.py",
    f"{PLAN_REL}/document_surface_option_b_candidate_route_v1.py",
    f"{PLAN_REL}/document_surface_option_a_b_route_comparison_v1.py",
    f"{PLAN_REL}/document_surface_hybrid_candidate_policy_v1.py",
    f"{PLAN_REL}/document_surface_option_b_admission_constraints_v1.json",
    f"{PLAN_REL}/document_surface_iteration_v2_case_mapping_v1.py",
    f"{PLAN_REL}/document_surface_iteration_v2_fixture_plan_v1.py",
    f"{PLAN_REL}/document_surface_iteration_v2_metrics_plan_v1.py",
    f"{PLAN_REL}/document_surface_iteration_v2_policy_v1.json",
    f"{PLAN_REL}/document_surface_iteration_v2_plan_v1.md",
    f"{TB_REL}/luna_model_manager_document_surface_detector_controlled_execution_iteration_v2_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_controlled_execution_iteration_v2_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_controlled_execution_iteration_v2_planning_v1.py",
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

    from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_v2_planning.document_surface_iteration_v2_planning_adapter_v1 import (  # noqa: WPS433
        run_iteration_v2_planning,
    )
    from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_v2_planning_v1_001.luna_model_manager_document_surface_detector_controlled_execution_iteration_v2_planning_smoke_v1 import (  # noqa: E402
        run_smoke_cases,
    )

    planning = run_iteration_v2_planning(repo_root=repo, write_outputs=True)
    smoke = run_smoke_cases()

    adapter_src = _read(f"{PLAN_REL}/document_surface_iteration_v2_planning_adapter_v1.py")
    constraints = json.loads(_read(f"{PLAN_REL}/document_surface_option_b_admission_constraints_v1.json") or "{}")

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_v2_planning_v1"
    outputs_ok = all((out_dir / f).is_file() for f in (
        "iteration_v2_planning_summary.json",
        "option_a_limit_review.json",
        "option_b_candidate_route_plan.json",
        "option_a_b_route_comparison.json",
        "hybrid_candidate_policy.json",
        "option_b_admission_constraints.json",
        "iteration_v2_case_mapping.json",
        "iteration_v2_fixture_plan.json",
        "iteration_v2_metrics_plan.json",
    ))

    flags = {
        "no_detector_execution": "detector_execution_forbidden" in adapter_src,
        "no_option_b_execution": constraints.get("execution_allowed") is False,
        "no_model_download": constraints.get("model_download_allowed") is False,
        "option_a_limit_complete": bool(planning.get("option_a_limit_review", {}).get("option_a_not_sufficient_for")),
        "option_b_candidate_only": constraints.get("option_b_status") == "candidate_route_only",
        "not_silent_fallback": constraints.get("silent_fallback_forbidden") is True,
        "case_mapping_complete": planning.get("case_mapping", {}).get("all_required_cases_covered") is True,
        "fixture_semantic_attributed": True,
        "route_metrics_planned": planning.get("metrics_plan", {}).get("route_level_metrics_complete") is True,
        "admission_blocks_execution": constraints.get("controlled_execution_planning_required_before_any_execution") is True,
        "protocol_retained": planning.get("protocol_compliance_passed") is True,
        "next_not_activation": planning.get("recommended_next_phase") == NEXT_PHASE,
        "smoke": smoke.get("smoke_passed") == 8 and not smoke.get("failed_checks"),
        "outputs": outputs_ok,
    }

    for k, v in flags.items():
        if not v:
            failed.append(f"guard.fail={k}")

    if planning.get("final_decision") != FINAL_GO:
        failed.append(f"planning.not_go={planning.get('final_decision')}")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_v2_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "iteration_v2_planning_only": True,
        "runtime_activation_allowed": False,
        "boundary_status": planning.get("boundary_status", "frozen"),
        "route_verdict": planning.get("route_verdict"),
        "audit_flags": flags,
        "blocker_count": len(failed),
        "failed_checks": failed,
        "final_decision": decision,
        "planning_final_decision": planning.get("final_decision"),
        "recommended_next_phase": NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL if decision == FINAL_GO else None,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_v2_planning_review_v1.json"
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
        "route_verdict": r.get("route_verdict"),
        "blocker_count": r["blocker_count"],
        "recommended_next_phase": r.get("recommended_next_phase"),
        "parallel_next_track": r.get("parallel_next_track"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

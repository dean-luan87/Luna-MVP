# -*- coding: utf-8 -*-
"""P1 Document Surface — iteration planning review v1."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO = Path(__file__).resolve().parents[4]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _repo() -> Path:
    for base in (Path.cwd(), _REPO):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO


from capabilities.test_board.test_board_protocol_v1 import TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1, write_test_board_records  # noqa: E402

IP_REL = "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_iteration_planning"
FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_PLANNING_GO"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-DryRun-v1-001"

REQUIRED: Tuple[str, ...] = (
    f"{IP_REL}/document_surface_iteration_planning_adapter_v1.py",
    f"{IP_REL}/document_surface_iteration_risk_mapping_v1.py",
    f"{IP_REL}/document_surface_candidate_quality_gate_v1.py",
    f"{IP_REL}/document_surface_overlap_separation_strategy_v1.py",
    f"{IP_REL}/document_surface_low_contrast_noise_strategy_v1.py",
    f"{IP_REL}/document_surface_attached_to_uncertainty_strategy_v1.py",
    f"{IP_REL}/document_surface_relation_hint_constraints_v1.py",
    f"{IP_REL}/document_surface_iteration_fixture_plan_v1.py",
    f"{IP_REL}/document_surface_iteration_metrics_plan_v1.py",
    f"{IP_REL}/document_surface_iteration_policy_v1.json",
)

GUARDS = (
    ("no_detector", "无 detector 重跑"),
    ("no_cv2", "无 cv2 执行"),
    ("no_image", "无图片读取"),
    ("bcd_mapped", "Case B/C/D 风险映射"),
    ("quality_gate", "Quality gate 不写 fact"),
    ("relation_evidence", "Relation evidence 约束"),
    ("fixture_plan", "Fixture 不要求真实图片"),
    ("metrics", "Metrics 非 accuracy-only"),
    ("no_fake", "无 fake relation"),
    ("protocol", "协议合规保留"),
    ("next_phase", "推荐 Iteration DryRun"),
    ("smoke", "smoke 8/8"),
)


def review(*, write_file: bool = True) -> Dict[str, Any]:
    repo = _repo()
    failed: List[str] = []
    for rel in REQUIRED:
        if not (repo / rel).is_file():
            failed.append(f"file.missing={rel}")

    from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_planning.document_surface_iteration_planning_adapter_v1 import (  # noqa: WPS433
        run_iteration_planning,
    )
    from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_planning_v1_001.luna_model_manager_document_surface_detector_controlled_execution_iteration_planning_smoke_v1 import (  # noqa: WPS433
        run_smoke_cases,
    )

    plan = run_iteration_planning(repo_root=repo, write_outputs=True)
    smoke = run_smoke_cases()
    qg = plan.get("quality_gate") or {}
    rel = plan.get("relation_constraints") or {}
    ov = plan.get("overlap_strategy") or {}

    flags = {
        "no_detector": plan.get("detector_rerun_forbidden") is True,
        "no_cv2": plan.get("cv2_execution_forbidden") is True,
        "no_image": plan.get("real_image_read_forbidden") is True,
        "bcd_mapped": plan.get("case_bcd_risks_mapped") is True,
        "quality_gate": qg.get("writes_fact") is False,
        "relation_evidence": rel.get("fake_relation_rate_target") == 0.0,
        "fixture_plan": (plan.get("fixture_plan") or {}).get("no_image_read_in_planning") is True,
        "metrics": (plan.get("metrics_plan") or {}).get("accuracy_not_primary_admission_criterion") is True,
        "no_fake": ov.get("does_not_fake_relation") is True and "no_forced_two_surface_output" in (ov.get("forbidden") or []),
        "protocol": plan.get("protocol_compliance_check") == "required",
        "next_phase": plan.get("recommended_next_phase") == NEXT_PHASE,
        "smoke": smoke.get("smoke_passed") == 8,
    }
    for k, ok in flags.items():
        if not ok:
            failed.append(f"guard.fail={k}")

    decision = FINAL_GO if not failed and plan.get("final_decision") == FINAL_GO else "BLOCKED"
    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)
    result = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-Planning-v1-001",
        "audit_flags": flags,
        "negative_guards": [{"key": k, "desc": d, "passed": flags[k]} for k, d in GUARDS],
        "blocker_count": len(failed),
        "failed_checks": failed,
        "final_decision": decision,
        "recommended_next_phase": NEXT_PHASE if decision == FINAL_GO else None,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }
    rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_planning_review_v1.json"
    if write_file:
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if decision == FINAL_GO:
        try:
            write_test_board_records(result, test_mode="dry_run", repo_root=repo, module="model_governance", source_review_file=str(rp))
        except (OSError, TypeError):
            pass
    return result


def main() -> int:
    r = review()
    print(json.dumps({"final_decision": r["final_decision"], "blocker_count": r["blocker_count"], "recommended_next_phase": r.get("recommended_next_phase")}, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

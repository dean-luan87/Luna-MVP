# -*- coding: utf-8
"""Perception Tool Layer — freeze smoke v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.model_test_lens.perception_tool_layer.perception_tool_layer_freeze_types_v1 import (
    DOCS_REL,
    FINAL_BLOCKED,
    FINAL_GO,
    FROZEN_CHAIN,
    ISSUE_REGISTRY_REL,
    RECOMMENDED_NEXT_PHASE,
    UPSTREAM_GO,
    VERIFIED_MODELS,
)

_REPO = Path(__file__).resolve().parents[3]


def _read(rel: str) -> str:
    for base in (_REPO, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _upstream_review(decision: str) -> bool:
    known_paths = {
        "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_EXECUTION_GO": (
            "_tmp_eval_out/p1_midplatform_scene_task_model_activation_execution_v1_smoke_v0/"
            "p1_midplatform_scene_task_model_activation_execution_review_v1.json"
        ),
        "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_PLANNING_GO": (
            "_tmp_eval_out/p1_midplatform_scene_task_model_activation_planning_v1_smoke_v0/"
            "p1_midplatform_scene_task_model_activation_planning_review_v1.json"
        ),
        "P1_MIDPLATFORM_TEXT_FIRST_TARGET_PROPOSAL_VALIDATION_PLANNING_GO": (
            "_tmp_eval_out/p1_midplatform_text_first_target_proposal_validation_planning_v1_smoke_v0/"
            "p1_midplatform_text_first_target_proposal_validation_planning_review_v1.json"
        ),
        "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_GO": (
            "_tmp_eval_out/p1_midplatform_dual_route_perception_validation_execution_v1_smoke_v0/"
            "p1_midplatform_dual_route_perception_validation_execution_review_v1.json"
        ),
        "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_EXECUTION_GO": (
            "_tmp_eval_out/p1_midplatform_scene_aware_segmentation_prompt_policy_execution_v1_smoke_v0/"
            "p1_midplatform_scene_aware_segmentation_prompt_policy_execution_review_v1.json"
        ),
        "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO": (
            "_tmp_eval_out/p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_smoke_v0/"
            "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_review.json"
        ),
    }
    rel = known_paths.get(decision)
    if rel:
        data = _load_json(rel)
        return data.get("final_decision") == decision
    for out_dir in _REPO.glob("_tmp_eval_out/p1_*"):
        for c in out_dir.glob("*review*.json"):
            try:
                data = json.loads(c.read_text(encoding="utf-8"))
                if data.get("final_decision") == decision:
                    return True
            except (OSError, json.JSONDecodeError):
                continue
    return False


def smoke_case_baseline_chain() -> Dict[str, Any]:
    report = _read(DOCS_REL)
    passed = all(step.replace("_", " ").title().replace(" ", "") in report.replace(" ", "") or step in report.lower()
                  for step in ("observation_attention", "task_candidate", "runner_admission", "controlled_execution",
                               "result_envelope", "midplatform_processing", "model_collaboration_candidate"))
    passed = passed and "Observation Attention" in report
    return {"case_id": "case_baseline_chain_documented", "passed": passed}


def smoke_case_five_problems() -> Dict[str, Any]:
    report = _read(DOCS_REL)
    problems = [
        "Problem 1",
        "Problem 2",
        "Problem 3",
        "Problem 4",
        "Problem 5",
        "缺少中台认知控制模型",
        "Scene Profile Ownership",
        "Model Activation Intelligence",
        "主图表达仍偏模型视角",
    ]
    passed = all(p in report for p in problems)
    return {"case_id": "case_five_problems_documented", "passed": passed}


def smoke_case_issue_registry() -> Dict[str, Any]:
    reg = _load_json(ISSUE_REGISTRY_REL)
    issues = reg.get("issues", [])
    required_ids = {
        "ISSUE_SHOP_SIGN_001",
        "ISSUE_SCENE_PROFILE_OWNERSHIP_001",
        "ISSUE_COGNITIVE_CONTROL_001",
        "ISSUE_MODEL_BOUNDARY_SAM_001",
        "ISSUE_MAIN_CANVAS_MODEL_VIEW_001",
    }
    found = {i.get("issue_id") for i in issues}
    passed = (
        reg.get("architecture_status") == "frozen"
        and len(issues) >= 10
        and required_ids.issubset(found)
        and all(
            all(k in i for k in (
                "issue_id", "scene", "observed_problem", "affected_layer",
                "current_behavior", "expected_behavior", "future_controller_signal",
            ))
            for i in issues
        )
    )
    return {"case_id": "case_issue_registry_complete", "passed": passed, "issue_count": len(issues)}


def smoke_case_freeze_status() -> Dict[str, Any]:
    report = _read(DOCS_REL)
    passed = (
        "architecture_status: frozen" in report
        and "optimization_status: paused" in report
        and "available_in_test_only" in report
    )
    return {"case_id": "case_freeze_status_documented", "passed": passed}


def smoke_case_upstream_go() -> Dict[str, Any]:
    missing = [g for g in UPSTREAM_GO if not _upstream_review(g)]
    passed = len(missing) == 0
    return {
        "case_id": "case_upstream_go_baseline",
        "passed": passed,
        "missing_upstream": missing,
    }


def smoke_case_verified_models() -> Dict[str, Any]:
    report = _read(DOCS_REL)
    checks = {
        "mobile_sam": "MobileSAM" in report,
        "ocr_route_candidate": "OCR route" in report or "ocr_route" in report.lower(),
        "dual_route_stub": "Dual Route" in report,
        "scene_task_model_activation_stub": "Model Activation" in report or "Scene-Task" in report,
    }
    passed = all(checks.values())
    return {"case_id": "case_verified_models_documented", "passed": passed, "checks": checks}


def smoke_case_shop_sign_evidence() -> Dict[str, Any]:
    report = _read(DOCS_REL)
    job_candidates = [
        _REPO / "capabilities/midplatform/model_test_lens/local_runner_bridge/jobs/job_564f1aa93983.json",
        Path("/Users/luanlei/Desktop/Luna-Core/capabilities/midplatform/model_test_lens/local_runner_bridge/jobs/job_564f1aa93983.json"),
    ]
    job_exists = any(p.is_file() for p in job_candidates)
    passed = "job_564f1aa93983" in report and "ISSUE_SHOP_SIGN_001" in report and job_exists
    return {"case_id": "case_shop_sign_evidence_preserved", "passed": passed, "job_exists": job_exists}


SMOKE_RUNNERS: Tuple[Any, ...] = (
    smoke_case_baseline_chain,
    smoke_case_five_problems,
    smoke_case_issue_registry,
    smoke_case_freeze_status,
    smoke_case_upstream_go,
    smoke_case_verified_models,
    smoke_case_shop_sign_evidence,
)


def run_smoke_cases() -> Dict[str, Any]:
    cases = [fn() for fn in SMOKE_RUNNERS]
    failed: List[str] = []
    for c in cases:
        if not c.get("passed"):
            failed.append(f"smoke.fail={c.get('case_id')}")

    decision = FINAL_GO.replace("_GO", "_SMOKE_GO") if not failed else FINAL_BLOCKED.replace(
        "_BLOCKED", "_SMOKE_BLOCKED"
    )
    if not failed:
        decision = "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_SMOKE_GO"
    else:
        decision = "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_SMOKE_BLOCKED"

    return {
        "phase_ref": "Phase-P1-Midplatform-Perception-Tool-Layer-Freeze-And-Handoff-v1-001",
        "frozen_chain": list(FROZEN_CHAIN),
        "architecture_status": "frozen",
        "optimization_status": "paused",
        "smoke_cases": cases,
        "smoke_case_count": len(cases),
        "smoke_passed": len(cases) - len([f for f in failed if f.startswith("smoke.fail")]),
        "failed_checks": failed,
        "final_decision": decision,
        "recommended_next_phase": RECOMMENDED_NEXT_PHASE,
        "freeze_only": True,
    }

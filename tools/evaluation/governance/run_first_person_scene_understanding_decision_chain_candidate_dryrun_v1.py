#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run First Person Scene Understanding Decision Chain Candidate DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.first_person_scene_understanding_decision_chain_candidate_dryrun_v1 import (
    run_first_person_scene_understanding_decision_chain_candidate_dryrun_v1,
)

DEFAULT_II_CHAIN_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_information_integration_chain_dryrun"
)
DEFAULT_DC_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_decision_center_module_dryrun_and_review"
)
DEFAULT_II_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_information_integration_layer_dryrun_and_review"
)
DEFAULT_DS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_drive_signal_contract_dryrun_and_review"
)
DEFAULT_CB_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
)
DEFAULT_SAFETY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_safety_gate_dryrun_and_review"
)
DEFAULT_HEALTH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_enforcement_supervisor_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_decision_chain_candidate_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "first_person_scene_understanding_decision_chain_dryrun_policy",
        "first_person_scene_understanding_decision_chain_dryrun_policy_v1.json",
    ),
    (
        "first_person_capability_stack_governance",
        "first_person_capability_stack_governance_v1.json",
    ),
    ("information_integration_input_review", "information_integration_input_review_v1.json"),
    ("decision_center_binding_review", "decision_center_binding_review_v1.json"),
    ("sample_decision_request_candidate", "sample_decision_request_candidate_v1.json"),
    ("sample_decision_candidate", "sample_decision_candidate_v1.json"),
    (
        "scene_understanding_decision_priority_review",
        "scene_understanding_decision_priority_review_v1.json",
    ),
    ("target_recognition_decision_review", "target_recognition_decision_review_v1.json"),
    ("text_recognition_decision_review", "text_recognition_decision_review_v1.json"),
    ("target_tracking_decision_review", "target_tracking_decision_review_v1.json"),
    ("task_intent_decision_review", "task_intent_decision_review_v1.json"),
    (
        "spatiotemporal_continuity_decision_review",
        "spatiotemporal_continuity_decision_review_v1.json",
    ),
    ("world_continuity_decision_review", "world_continuity_decision_review_v1.json"),
    ("survival_risk_decision_review", "survival_risk_decision_review_v1.json"),
    (
        "navigation_application_context_decision_review",
        "navigation_application_context_decision_review_v1.json",
    ),
    ("decision_action_taxonomy_review", "decision_action_taxonomy_review_v1.json"),
    ("decision_to_task_response_handoff_plan", "decision_to_task_response_handoff_plan_v1.json"),
    ("decision_traceability_review", "decision_traceability_review_v1.json"),
    ("decision_boundary_audit", "decision_boundary_audit_v1.json"),
    ("decision_blocked_path_result", "decision_blocked_path_result_v1.json"),
    ("decision_closure_decision", "decision_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--integration-chain-dryrun-root", default=DEFAULT_II_CHAIN_DR)
    p.add_argument("--decision-center-dryrun-root", default=DEFAULT_DC_DR)
    p.add_argument("--information-integration-dryrun-root", default=DEFAULT_II_DR)
    p.add_argument("--drive-signal-dryrun-root", default=DEFAULT_DS_DR)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB_DR)
    p.add_argument("--safety-gate-dryrun-root", default=DEFAULT_SAFETY_DR)
    p.add_argument("--health-enforcement-dryrun-root", default=DEFAULT_HEALTH_DR)
    args = p.parse_args()

    result = run_first_person_scene_understanding_decision_chain_candidate_dryrun_v1(
        first_person_scene_understanding_information_integration_chain_dryrun_root=args.integration_chain_dryrun_root,
        midplatform_decision_center_module_dryrun_and_review_root=args.decision_center_dryrun_root,
        midplatform_information_integration_layer_dryrun_and_review_root=args.information_integration_dryrun_root,
        seed_core_drive_signal_contract_dryrun_and_review_root=args.drive_signal_dryrun_root,
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=args.constitution_bus_dryrun_root,
        midplatform_safety_gate_dryrun_and_review_root=args.safety_gate_dryrun_root,
        health_enforcement_supervisor_dryrun_and_review_root=args.health_enforcement_dryrun_root,
        output_root=args.output_root,
    )

    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())

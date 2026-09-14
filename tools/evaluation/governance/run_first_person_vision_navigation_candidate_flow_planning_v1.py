#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run First Person Vision Navigation Candidate Flow Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.first_person_vision_navigation_candidate_flow_planning_v1 import (
    run_first_person_vision_navigation_candidate_flow_planning_v1,
)

DEFAULT_MAINLINE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_ocr_navigation_task_mainline_resume"
)
DEFAULT_CB_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
)
DEFAULT_II_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_information_integration_layer_dryrun_and_review"
)
DEFAULT_DS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_drive_signal_contract_dryrun_and_review"
)
DEFAULT_PROVIDER_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_dryrun_and_review"
)
DEFAULT_CR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_controlled_runtime_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_vision_navigation_candidate_flow_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "first_person_vision_navigation_candidate_flow_policy",
        "first_person_vision_navigation_candidate_flow_policy_v1.json",
    ),
    ("mainline_resume_input_review", "mainline_resume_input_review_v1.json"),
    ("perception_zone_candidate_flow_definition", "perception_zone_candidate_flow_definition_v1.json"),
    ("visual_observation_candidate_contract", "visual_observation_candidate_contract_v1.json"),
    ("visual_evidence_candidate_contract", "visual_evidence_candidate_contract_v1.json"),
    ("scene_context_candidate_contract", "scene_context_candidate_contract_v1.json"),
    ("obstacle_candidate_contract", "obstacle_candidate_contract_v1.json"),
    ("risk_context_candidate_contract", "risk_context_candidate_contract_v1.json"),
    ("ocr_result_candidate_contract", "ocr_result_candidate_contract_v1.json"),
    ("text_region_candidate_contract", "text_region_candidate_contract_v1.json"),
    ("signage_context_candidate_contract", "signage_context_candidate_contract_v1.json"),
    ("map_location_context_candidate_contract", "map_location_context_candidate_contract_v1.json"),
    ("route_context_candidate_contract", "route_context_candidate_contract_v1.json"),
    ("navigation_task_candidate_contract", "navigation_task_candidate_contract_v1.json"),
    ("task_route_progress_candidate_contract", "task_route_progress_candidate_contract_v1.json"),
    ("required_observation_candidate_contract", "required_observation_candidate_contract_v1.json"),
    ("visual_ocr_map_candidate_binding_policy", "visual_ocr_map_candidate_binding_policy_v1.json"),
    ("drive_signal_to_observation_priority_policy", "drive_signal_to_observation_priority_policy_v1.json"),
    (
        "candidate_to_information_integration_handoff_plan",
        "candidate_to_information_integration_handoff_plan_v1.json",
    ),
    ("candidate_evidence_traceability_policy", "candidate_evidence_traceability_policy_v1.json"),
    ("candidate_flow_boundary_matrix", "candidate_flow_boundary_matrix_v1.json"),
    ("candidate_flow_dryrun_plan", "candidate_flow_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "first_person_vision_navigation_candidate_flow_planning_decision",
        "first_person_vision_navigation_candidate_flow_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--mainline-resume-root", default=DEFAULT_MAINLINE)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB_DR)
    p.add_argument("--information-integration-dryrun-root", default=DEFAULT_II_DR)
    p.add_argument("--drive-signal-dryrun-root", default=DEFAULT_DS_DR)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER_DR)
    p.add_argument("--controlled-runtime-dryrun-root", default=DEFAULT_CR_DR)
    args = p.parse_args()

    result = run_first_person_vision_navigation_candidate_flow_planning_v1(
        vision_ocr_navigation_task_mainline_resume_root=args.mainline_resume_root,
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=args.constitution_bus_dryrun_root,
        midplatform_information_integration_layer_dryrun_and_review_root=args.information_integration_dryrun_root,
        seed_core_drive_signal_contract_dryrun_and_review_root=args.drive_signal_dryrun_root,
        provider_abstraction_standard_alignment_dryrun_and_review_root=args.provider_abstraction_dryrun_root,
        midplatform_controlled_runtime_dryrun_and_review_root=args.controlled_runtime_dryrun_root,
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
                "planning_pass": sm.get("planning_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())

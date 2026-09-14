#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Speech Gate Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_speech_gate_planning_v1 import (
    run_midplatform_speech_gate_planning_v1,
)

DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_speech_display_gate_roadmap_decision"
)
DEFAULT_SAFETY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_dryrun_and_review"
)
DEFAULT_SAFETY_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_planning"
)
DEFAULT_UO_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_user_output_constitution_dryrun_and_review"
)
DEFAULT_OUTPUT_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_output_plane_integration_dryrun_and_review"
)
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("speech_gate_planning_policy", "speech_gate_planning_policy_v1.json"),
    ("speech_display_roadmap_input_review", "speech_display_roadmap_input_review_v1.json"),
    ("speech_gate_module_definition", "speech_gate_module_definition_v1.json"),
    (
        "speech_gate_enforcement_result_intake_contract",
        "speech_gate_enforcement_result_intake_contract_v1.json",
    ),
    (
        "speech_gate_user_output_candidate_intake_contract",
        "speech_gate_user_output_candidate_intake_contract_v1.json",
    ),
    ("speech_gate_result_candidate_contract", "speech_gate_result_candidate_contract_v1.json"),
    ("speech_gate_action_taxonomy", "speech_gate_action_taxonomy_v1.json"),
    ("speech_channel_admission_rule_plan", "speech_channel_admission_rule_plan_v1.json"),
    ("speech_content_constraint_rule_plan", "speech_content_constraint_rule_plan_v1.json"),
    ("speech_uncertainty_disclosure_rule_plan", "speech_uncertainty_disclosure_rule_plan_v1.json"),
    ("speech_tone_personalization_boundary_plan", "speech_tone_personalization_boundary_plan_v1.json"),
    (
        "speech_interruption_and_timing_boundary_plan",
        "speech_interruption_and_timing_boundary_plan_v1.json",
    ),
    ("speech_safety_refusal_hold_degrade_plan", "speech_safety_refusal_hold_degrade_plan_v1.json"),
    ("speech_gate_downstream_handoff_plan", "speech_gate_downstream_handoff_plan_v1.json"),
    (
        "speech_gate_no_raw_constitution_binding_policy",
        "speech_gate_no_raw_constitution_binding_policy_v1.json",
    ),
    ("speech_gate_execution_layer_boundary_plan", "speech_gate_execution_layer_boundary_plan_v1.json"),
    ("speech_gate_traceability_plan", "speech_gate_traceability_plan_v1.json"),
    ("speech_gate_boundary_matrix", "speech_gate_boundary_matrix_v1.json"),
    ("speech_gate_dryrun_plan", "speech_gate_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("speech_gate_planning_decision", "speech_gate_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--roadmap-decision-root", default=DEFAULT_ROADMAP)
    p.add_argument("--safety-gate-dryrun-root", default=DEFAULT_SAFETY_DR)
    p.add_argument("--safety-gate-planning-root", default=DEFAULT_SAFETY_PLAN)
    p.add_argument("--user-output-constitution-dryrun-root", default=DEFAULT_UO_DR)
    p.add_argument("--output-plane-dryrun-root", default=DEFAULT_OUTPUT_DR)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    args = p.parse_args()

    result = run_midplatform_speech_gate_planning_v1(
        midplatform_speech_display_gate_roadmap_decision_root=args.roadmap_decision_root,
        midplatform_safety_gate_dryrun_and_review_root=args.safety_gate_dryrun_root,
        midplatform_safety_gate_planning_root=args.safety_gate_planning_root,
        midplatform_user_output_constitution_dryrun_and_review_root=args.user_output_constitution_dryrun_root,
        midplatform_output_plane_integration_dryrun_and_review_root=args.output_plane_dryrun_root,
        midplatform_module_definition_template_planning_root=args.template_planning_root,
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
                "speech_gate_enforcement_only": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())

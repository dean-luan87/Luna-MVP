#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Health Enforcement Supervisor Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.health_enforcement_supervisor_planning_v1 import (
    run_health_enforcement_supervisor_planning_v1,
)

DEFAULT_DISPLAY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_display_gate_dryrun_and_review"
)
DEFAULT_HEALTH_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_management_layer_integration_post_dryrun_review"
)
DEFAULT_HEALTH_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/health_management_layer_integration_dryrun"
)
DEFAULT_SAFETY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_dryrun_and_review"
)
DEFAULT_SPEECH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_dryrun_and_review"
)
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_FMIS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_frontend_model_influence_simulation_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/health_enforcement_supervisor_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("health_enforcement_supervisor_planning_policy", "health_enforcement_supervisor_planning_policy_v1.json"),
    ("display_gate_dryrun_input_review", "display_gate_dryrun_input_review_v1.json"),
    ("health_management_input_review", "health_management_input_review_v1.json"),
    (
        "health_enforcement_supervisor_module_definition",
        "health_enforcement_supervisor_module_definition_v1.json",
    ),
    (
        "health_enforcement_supervisor_health_signal_intake_contract",
        "health_enforcement_supervisor_health_signal_intake_contract_v1.json",
    ),
    (
        "health_enforcement_supervisor_gate_result_intake_contract",
        "health_enforcement_supervisor_gate_result_intake_contract_v1.json",
    ),
    (
        "health_enforcement_supervision_result_candidate_contract",
        "health_enforcement_supervision_result_candidate_contract_v1.json",
    ),
    (
        "health_enforcement_supervision_action_taxonomy",
        "health_enforcement_supervision_action_taxonomy_v1.json",
    ),
    ("gate_compliance_monitoring_rule_plan", "gate_compliance_monitoring_rule_plan_v1.json"),
    ("health_signal_binding_rule_plan", "health_signal_binding_rule_plan_v1.json"),
    ("boundary_violation_detection_rule_plan", "boundary_violation_detection_rule_plan_v1.json"),
    ("bypass_prevention_rule_plan", "bypass_prevention_rule_plan_v1.json"),
    ("enforcement_override_forbidden_rule_plan", "enforcement_override_forbidden_rule_plan_v1.json"),
    ("runtime_recommendation_rule_plan", "runtime_recommendation_rule_plan_v1.json"),
    ("health_enforcement_degrade_hold_plan", "health_enforcement_degrade_hold_plan_v1.json"),
    (
        "health_enforcement_supervisor_downstream_handoff_plan",
        "health_enforcement_supervisor_downstream_handoff_plan_v1.json",
    ),
    (
        "health_enforcement_supervisor_no_raw_constitution_binding_policy",
        "health_enforcement_supervisor_no_raw_constitution_binding_policy_v1.json",
    ),
    (
        "health_enforcement_supervisor_traceability_plan",
        "health_enforcement_supervisor_traceability_plan_v1.json",
    ),
    (
        "health_enforcement_supervisor_boundary_matrix",
        "health_enforcement_supervisor_boundary_matrix_v1.json",
    ),
    ("health_enforcement_supervisor_dryrun_plan", "health_enforcement_supervisor_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "health_enforcement_supervisor_planning_decision",
        "health_enforcement_supervisor_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--display-gate-dryrun-root", default=DEFAULT_DISPLAY_DR)
    p.add_argument("--health-post-dryrun-review-root", default=DEFAULT_HEALTH_POST)
    p.add_argument("--health-dryrun-root", default=DEFAULT_HEALTH_DRYRUN)
    p.add_argument("--safety-gate-dryrun-root", default=DEFAULT_SAFETY_DR)
    p.add_argument("--speech-gate-dryrun-root", default=DEFAULT_SPEECH_DR)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    p.add_argument("--fmis-dryrun-root", default=DEFAULT_FMIS_DR)
    args = p.parse_args()

    result = run_health_enforcement_supervisor_planning_v1(
        midplatform_display_gate_dryrun_and_review_root=args.display_gate_dryrun_root,
        health_management_layer_integration_post_dryrun_review_root=args.health_post_dryrun_review_root,
        health_management_layer_integration_dryrun_root=args.health_dryrun_root,
        midplatform_safety_gate_dryrun_and_review_root=args.safety_gate_dryrun_root,
        midplatform_speech_gate_dryrun_and_review_root=args.speech_gate_dryrun_root,
        midplatform_module_definition_template_planning_root=args.template_planning_root,
        midplatform_frontend_model_influence_simulation_dryrun_and_review_root=args.fmis_dryrun_root,
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

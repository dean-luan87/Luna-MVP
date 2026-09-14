#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Display Gate DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_display_gate_dryrun_and_review_v1 import (
    run_midplatform_display_gate_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_display_gate_planning"
)
DEFAULT_SAFETY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_dryrun_and_review"
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
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_display_gate_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("display_gate_dryrun_review_policy", "display_gate_dryrun_review_policy_v1.json"),
    ("display_gate_planning_input_review", "display_gate_planning_input_review_v1.json"),
    ("display_gate_model_candidate", "display_gate_model_candidate_v1.json"),
    ("sample_enforcement_result_intake", "sample_enforcement_result_intake_v1.json"),
    ("sample_user_output_candidate_intake", "sample_user_output_candidate_intake_v1.json"),
    ("sample_display_gate_result_candidate", "sample_display_gate_result_candidate_v1.json"),
    ("display_enforcement_layer_role_review", "display_enforcement_layer_role_review_v1.json"),
    ("display_no_raw_constitution_binding_review", "display_no_raw_constitution_binding_review_v1.json"),
    ("display_action_taxonomy_dryrun_review", "display_action_taxonomy_dryrun_review_v1.json"),
    ("display_channel_admission_dryrun_review", "display_channel_admission_dryrun_review_v1.json"),
    ("display_content_constraint_dryrun_review", "display_content_constraint_dryrun_review_v1.json"),
    ("display_uncertainty_disclosure_dryrun_review", "display_uncertainty_disclosure_dryrun_review_v1.json"),
    ("display_privacy_masking_dryrun_review", "display_privacy_masking_dryrun_review_v1.json"),
    ("display_layout_boundary_review", "display_layout_boundary_review_v1.json"),
    ("display_notification_boundary_review", "display_notification_boundary_review_v1.json"),
    ("display_refusal_hold_degrade_dryrun_review", "display_refusal_hold_degrade_dryrun_review_v1.json"),
    ("display_downstream_handoff_review", "display_downstream_handoff_review_v1.json"),
    ("display_execution_layer_boundary_review", "display_execution_layer_boundary_review_v1.json"),
    ("display_gate_traceability_review", "display_gate_traceability_review_v1.json"),
    ("display_gate_boundary_audit", "display_gate_boundary_audit_v1.json"),
    ("display_gate_blocked_path_result", "display_gate_blocked_path_result_v1.json"),
    ("display_gate_closure_decision", "display_gate_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--planning-root", default=DEFAULT_PLANNING)
    p.add_argument("--safety-gate-dryrun-root", default=DEFAULT_SAFETY_DR)
    p.add_argument("--output-plane-dryrun-root", default=DEFAULT_OUTPUT_DR)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    args = p.parse_args()

    result = run_midplatform_display_gate_dryrun_and_review_v1(
        midplatform_display_gate_planning_root=args.planning_root,
        midplatform_safety_gate_dryrun_and_review_root=args.safety_gate_dryrun_root,
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

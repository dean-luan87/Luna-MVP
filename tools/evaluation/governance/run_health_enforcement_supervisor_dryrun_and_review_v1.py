#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Health Enforcement Supervisor DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.health_enforcement_supervisor_dryrun_and_review_v1 import (
    run_health_enforcement_supervisor_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/health_enforcement_supervisor_planning"
)
DEFAULT_DISPLAY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_display_gate_dryrun_and_review"
)
DEFAULT_SPEECH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_dryrun_and_review"
)
DEFAULT_SAFETY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_dryrun_and_review"
)
DEFAULT_VALIDATION_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_PROVIDER_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_dryrun_and_review"
)
DEFAULT_E2E_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_end_to_end_output_chain_simulation_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/health_enforcement_supervisor_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "health_enforcement_supervisor_dryrun_review_policy",
        "health_enforcement_supervisor_dryrun_review_policy_v1.json",
    ),
    (
        "health_enforcement_supervisor_planning_input_review",
        "health_enforcement_supervisor_planning_input_review_v1.json",
    ),
    (
        "health_enforcement_supervisor_model_candidate",
        "health_enforcement_supervisor_model_candidate_v1.json",
    ),
    ("sample_health_signal_candidate", "sample_health_signal_candidate_v1.json"),
    ("sample_gate_result_candidate_set", "sample_gate_result_candidate_set_v1.json"),
    (
        "sample_health_enforcement_supervision_result_candidate",
        "sample_health_enforcement_supervision_result_candidate_v1.json",
    ),
    ("supervision_scope_review", "supervision_scope_review_v1.json"),
    ("gate_result_intake_review", "gate_result_intake_review_v1.json"),
    (
        "enforcement_compliance_observation_review",
        "enforcement_compliance_observation_review_v1.json",
    ),
    (
        "enforcement_health_signal_mapping_review",
        "enforcement_health_signal_mapping_review_v1.json",
    ),
    ("enforcement_issue_trace_review", "enforcement_issue_trace_review_v1.json"),
    ("enforcement_violation_report_review", "enforcement_violation_report_review_v1.json"),
    ("gate_conflict_drift_timeout_review", "gate_conflict_drift_timeout_review_v1.json"),
    ("supervisor_non_interference_review", "supervisor_non_interference_review_v1.json"),
    (
        "decision_center_whitebox_handoff_review",
        "decision_center_whitebox_handoff_review_v1.json",
    ),
    (
        "controlled_runtime_readiness_signal_review",
        "controlled_runtime_readiness_signal_review_v1.json",
    ),
    (
        "health_enforcement_supervisor_boundary_audit",
        "health_enforcement_supervisor_boundary_audit_v1.json",
    ),
    (
        "health_enforcement_supervisor_blocked_path_result",
        "health_enforcement_supervisor_blocked_path_result_v1.json",
    ),
    (
        "health_enforcement_supervisor_closure_decision",
        "health_enforcement_supervisor_closure_decision_v1.json",
    ),
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
    p.add_argument("--display-gate-dryrun-root", default=DEFAULT_DISPLAY_DR)
    p.add_argument("--speech-gate-dryrun-root", default=DEFAULT_SPEECH_DR)
    p.add_argument("--safety-gate-dryrun-root", default=DEFAULT_SAFETY_DR)
    p.add_argument("--validation-dryrun-root", default=DEFAULT_VALIDATION_DR)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER_DR)
    p.add_argument("--e2e-simulation-dryrun-root", default=DEFAULT_E2E_DR)
    args = p.parse_args()

    result = run_health_enforcement_supervisor_dryrun_and_review_v1(
        health_enforcement_supervisor_planning_root=args.planning_root,
        midplatform_display_gate_dryrun_and_review_root=args.display_gate_dryrun_root,
        midplatform_speech_gate_dryrun_and_review_root=args.speech_gate_dryrun_root,
        midplatform_safety_gate_dryrun_and_review_root=args.safety_gate_dryrun_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_dryrun_root,
        provider_abstraction_standard_alignment_dryrun_and_review_root=args.provider_abstraction_dryrun_root,
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root=args.e2e_simulation_dryrun_root,
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

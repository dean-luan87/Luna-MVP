#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Controlled Runtime DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    run_midplatform_controlled_runtime_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_controlled_runtime_planning"
)
DEFAULT_HEALTH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_enforcement_supervisor_dryrun_and_review"
)
DEFAULT_DISPLAY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_display_gate_dryrun_and_review"
)
DEFAULT_PROVIDER_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_dryrun_and_review"
)
DEFAULT_FMIS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_frontend_model_influence_simulation_dryrun_and_review"
)
DEFAULT_E2E_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_end_to_end_output_chain_simulation_dryrun_and_review"
)
DEFAULT_TTS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_dryrun_and_review"
)
DEFAULT_VALIDATION_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_controlled_runtime_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("controlled_runtime_dryrun_review_policy", "controlled_runtime_dryrun_review_policy_v1.json"),
    (
        "controlled_runtime_planning_input_review",
        "controlled_runtime_planning_input_review_v1.json",
    ),
    ("controlled_runtime_framework_candidate", "controlled_runtime_framework_candidate_v1.json"),
    ("runtime_candidate_registry_sample", "runtime_candidate_registry_sample_v1.json"),
    ("controlled_runtime_admission_review", "controlled_runtime_admission_review_v1.json"),
    ("controlled_runtime_authorization_review", "controlled_runtime_authorization_review_v1.json"),
    (
        "controlled_runtime_execution_window_review",
        "controlled_runtime_execution_window_review_v1.json",
    ),
    (
        "controlled_runtime_provider_readiness_review",
        "controlled_runtime_provider_readiness_review_v1.json",
    ),
    (
        "controlled_runtime_gate_precondition_review",
        "controlled_runtime_gate_precondition_review_v1.json",
    ),
    (
        "controlled_runtime_health_supervision_review",
        "controlled_runtime_health_supervision_review_v1.json",
    ),
    ("controlled_runtime_evidence_capture_review", "controlled_runtime_evidence_capture_review_v1.json"),
    ("controlled_runtime_rollback_review", "controlled_runtime_rollback_review_v1.json"),
    ("controlled_runtime_post_execution_review", "controlled_runtime_post_execution_review_v1.json"),
    ("controlled_runtime_failure_route_review", "controlled_runtime_failure_route_review_v1.json"),
    ("controlled_runtime_domain_matrix_review", "controlled_runtime_domain_matrix_review_v1.json"),
    ("controlled_runtime_boundary_audit", "controlled_runtime_boundary_audit_v1.json"),
    ("controlled_runtime_blocked_path_result", "controlled_runtime_blocked_path_result_v1.json"),
    ("controlled_runtime_closure_decision", "controlled_runtime_closure_decision_v1.json"),
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
    p.add_argument("--health-supervisor-dryrun-root", default=DEFAULT_HEALTH_DR)
    p.add_argument("--display-gate-dryrun-root", default=DEFAULT_DISPLAY_DR)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER_DR)
    p.add_argument("--fmis-dryrun-root", default=DEFAULT_FMIS_DR)
    p.add_argument("--e2e-simulation-dryrun-root", default=DEFAULT_E2E_DR)
    p.add_argument("--tts-runtime-dryrun-root", default=DEFAULT_TTS_DR)
    p.add_argument("--validation-dryrun-root", default=DEFAULT_VALIDATION_DR)
    args = p.parse_args()

    result = run_midplatform_controlled_runtime_dryrun_and_review_v1(
        midplatform_controlled_runtime_planning_root=args.planning_root,
        health_enforcement_supervisor_dryrun_and_review_root=args.health_supervisor_dryrun_root,
        midplatform_display_gate_dryrun_and_review_root=args.display_gate_dryrun_root,
        provider_abstraction_standard_alignment_dryrun_and_review_root=args.provider_abstraction_dryrun_root,
        midplatform_frontend_model_influence_simulation_dryrun_and_review_root=args.fmis_dryrun_root,
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root=args.e2e_simulation_dryrun_root,
        midplatform_tts_runtime_dryrun_and_review_root=args.tts_runtime_dryrun_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_dryrun_root,
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

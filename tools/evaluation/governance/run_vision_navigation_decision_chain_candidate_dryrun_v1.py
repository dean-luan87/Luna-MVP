#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision Navigation Decision Chain Candidate DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_navigation_decision_chain_candidate_dryrun_v1 import (
    run_vision_navigation_decision_chain_candidate_dryrun_v1,
)

DEFAULT_II_CHAIN_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_navigation_information_integration_chain_dryrun"
)
DEFAULT_DC_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_decision_center_module_dryrun_and_review"
)
DEFAULT_CB_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
)
DEFAULT_DS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_drive_signal_contract_dryrun_and_review"
)
DEFAULT_PROVIDER_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_navigation_decision_chain_candidate_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "vision_navigation_decision_chain_candidate_dryrun_policy",
        "vision_navigation_decision_chain_candidate_dryrun_policy_v1.json",
    ),
    ("integration_chain_input_review", "integration_chain_input_review_v1.json"),
    ("decision_chain_model_candidate", "decision_chain_model_candidate_v1.json"),
    ("sample_decision_request_candidate", "sample_decision_request_candidate_v1.json"),
    ("sample_decision_candidate", "sample_decision_candidate_v1.json"),
    (
        "readiness_conflict_gap_consumption_review",
        "readiness_conflict_gap_consumption_review_v1.json",
    ),
    (
        "constitution_health_drive_binding_review",
        "constitution_health_drive_binding_review_v1.json",
    ),
    (
        "decision_rationale_traceability_review",
        "decision_rationale_traceability_review_v1.json",
    ),
    ("decision_boundary_review", "decision_boundary_review_v1.json"),
    (
        "task_response_handoff_readiness_review",
        "task_response_handoff_readiness_review_v1.json",
    ),
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
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB_DR)
    p.add_argument("--drive-signal-dryrun-root", default=DEFAULT_DS_DR)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER_DR)
    args = p.parse_args()

    result = run_vision_navigation_decision_chain_candidate_dryrun_v1(
        vision_navigation_information_integration_chain_dryrun_root=args.integration_chain_dryrun_root,
        midplatform_decision_center_module_dryrun_and_review_root=args.decision_center_dryrun_root,
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=args.constitution_bus_dryrun_root,
        seed_core_drive_signal_contract_dryrun_and_review_root=args.drive_signal_dryrun_root,
        provider_abstraction_standard_alignment_dryrun_and_review_root=args.provider_abstraction_dryrun_root,
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

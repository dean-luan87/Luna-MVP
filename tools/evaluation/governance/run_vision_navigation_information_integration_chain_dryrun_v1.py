#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision Navigation Information Integration Chain DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_navigation_information_integration_chain_dryrun_v1 import (
    run_vision_navigation_information_integration_chain_dryrun_v1,
)

DEFAULT_CF_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_vision_navigation_candidate_flow_dryrun_and_review"
)
DEFAULT_CF_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_vision_navigation_candidate_flow_planning"
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
DEFAULT_PROVIDER_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_navigation_information_integration_chain_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "vision_navigation_information_integration_chain_dryrun_policy",
        "vision_navigation_information_integration_chain_dryrun_policy_v1.json",
    ),
    ("candidate_flow_input_review", "candidate_flow_input_review_v1.json"),
    ("sample_candidate_intake_set", "sample_candidate_intake_set_v1.json"),
    (
        "information_integration_chain_model_candidate",
        "information_integration_chain_model_candidate_v1.json",
    ),
    ("sample_integrated_context_candidate", "sample_integrated_context_candidate_v1.json"),
    ("sample_context_conflict_candidate", "sample_context_conflict_candidate_v1.json"),
    ("sample_context_gap_candidate", "sample_context_gap_candidate_v1.json"),
    ("sample_context_freshness_status", "sample_context_freshness_status_v1.json"),
    ("sample_context_priority_map", "sample_context_priority_map_v1.json"),
    ("sample_decision_readiness_candidate", "sample_decision_readiness_candidate_v1.json"),
    (
        "visual_ocr_map_route_integration_review",
        "visual_ocr_map_route_integration_review_v1.json",
    ),
    (
        "drive_signal_priority_integration_review",
        "drive_signal_priority_integration_review_v1.json",
    ),
    ("risk_context_integration_review", "risk_context_integration_review_v1.json"),
    (
        "evidence_traceability_integration_review",
        "evidence_traceability_integration_review_v1.json",
    ),
    (
        "conflict_gap_freshness_integration_review",
        "conflict_gap_freshness_integration_review_v1.json",
    ),
    (
        "decision_center_handoff_readiness_review",
        "decision_center_handoff_readiness_review_v1.json",
    ),
    ("chain_boundary_audit", "chain_boundary_audit_v1.json"),
    ("chain_blocked_path_result", "chain_blocked_path_result_v1.json"),
    ("chain_closure_decision", "chain_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--candidate-flow-dryrun-root", default=DEFAULT_CF_DR)
    p.add_argument("--candidate-flow-planning-root", default=DEFAULT_CF_PLAN)
    p.add_argument("--information-integration-dryrun-root", default=DEFAULT_II_DR)
    p.add_argument("--drive-signal-dryrun-root", default=DEFAULT_DS_DR)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB_DR)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER_DR)
    args = p.parse_args()

    result = run_vision_navigation_information_integration_chain_dryrun_v1(
        first_person_vision_navigation_candidate_flow_dryrun_and_review_root=args.candidate_flow_dryrun_root,
        first_person_vision_navigation_candidate_flow_planning_root=args.candidate_flow_planning_root,
        midplatform_information_integration_layer_dryrun_and_review_root=args.information_integration_dryrun_root,
        seed_core_drive_signal_contract_dryrun_and_review_root=args.drive_signal_dryrun_root,
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=args.constitution_bus_dryrun_root,
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

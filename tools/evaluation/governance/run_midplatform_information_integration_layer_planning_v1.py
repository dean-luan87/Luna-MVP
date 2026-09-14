#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Information Integration Layer Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_information_integration_layer_planning_v1 import (
    run_midplatform_information_integration_layer_planning_v1,
)

DEFAULT_DS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_drive_signal_contract_dryrun_and_review"
)
DEFAULT_SC_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_pluggable_layer_architecture_dryrun_and_review"
)
DEFAULT_CZ_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_cognitive_zoning_architecture_dryrun_and_review"
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
DEFAULT_CEF_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_candidate_evidence_flow_integration_dryrun_and_review"
)
DEFAULT_DC_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_decision_center_module_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_information_integration_layer_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("information_integration_layer_planning_policy", "information_integration_layer_planning_policy_v1.json"),
    ("upstream_drive_signal_input_review", "upstream_drive_signal_input_review_v1.json"),
    ("information_integration_layer_definition", "information_integration_layer_definition_v1.json"),
    ("integration_input_source_taxonomy", "integration_input_source_taxonomy_v1.json"),
    ("integrated_context_candidate_contract", "integrated_context_candidate_contract_v1.json"),
    ("context_conflict_candidate_contract", "context_conflict_candidate_contract_v1.json"),
    ("context_gap_candidate_contract", "context_gap_candidate_contract_v1.json"),
    ("context_freshness_status_contract", "context_freshness_status_contract_v1.json"),
    ("context_priority_map_contract", "context_priority_map_contract_v1.json"),
    ("decision_readiness_candidate_contract", "decision_readiness_candidate_contract_v1.json"),
    ("drive_signal_integration_policy", "drive_signal_integration_policy_v1.json"),
    ("perception_context_integration_policy", "perception_context_integration_policy_v1.json"),
    ("memory_worldmodel_context_integration_policy", "memory_worldmodel_context_integration_policy_v1.json"),
    ("task_route_map_context_integration_policy", "task_route_map_context_integration_policy_v1.json"),
    ("health_validation_whitebox_integration_policy", "health_validation_whitebox_integration_policy_v1.json"),
    ("provider_status_integration_policy", "provider_status_integration_policy_v1.json"),
    ("conflict_gap_freshness_scoring_policy", "conflict_gap_freshness_scoring_policy_v1.json"),
    (
        "information_integration_to_decision_center_handoff_plan",
        "information_integration_to_decision_center_handoff_plan_v1.json",
    ),
    (
        "information_integration_no_universal_brain_boundary",
        "information_integration_no_universal_brain_boundary_v1.json",
    ),
    ("information_integration_traceability_policy", "information_integration_traceability_policy_v1.json"),
    ("information_integration_boundary_matrix", "information_integration_boundary_matrix_v1.json"),
    ("information_integration_dryrun_plan", "information_integration_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "information_integration_layer_planning_decision",
        "information_integration_layer_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--drive-signal-dryrun-root", default=DEFAULT_DS_DR)
    p.add_argument("--seed-core-pluggable-dryrun-root", default=DEFAULT_SC_DR)
    p.add_argument("--cognitive-zoning-dryrun-root", default=DEFAULT_CZ_DR)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER_DR)
    p.add_argument("--fmis-dryrun-root", default=DEFAULT_FMIS_DR)
    p.add_argument("--e2e-simulation-dryrun-root", default=DEFAULT_E2E_DR)
    p.add_argument("--candidate-evidence-flow-dryrun-root", default=DEFAULT_CEF_DR)
    p.add_argument("--decision-center-dryrun-root", default=DEFAULT_DC_DR)
    args = p.parse_args()

    result = run_midplatform_information_integration_layer_planning_v1(
        seed_core_drive_signal_contract_dryrun_and_review_root=args.drive_signal_dryrun_root,
        seed_core_pluggable_layer_architecture_dryrun_and_review_root=args.seed_core_pluggable_dryrun_root,
        midplatform_cognitive_zoning_architecture_dryrun_and_review_root=args.cognitive_zoning_dryrun_root,
        provider_abstraction_standard_alignment_dryrun_and_review_root=args.provider_abstraction_dryrun_root,
        midplatform_frontend_model_influence_simulation_dryrun_and_review_root=args.fmis_dryrun_root,
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root=args.e2e_simulation_dryrun_root,
        midplatform_candidate_evidence_flow_integration_dryrun_and_review_root=args.candidate_evidence_flow_dryrun_root,
        midplatform_decision_center_module_dryrun_and_review_root=args.decision_center_dryrun_root,
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

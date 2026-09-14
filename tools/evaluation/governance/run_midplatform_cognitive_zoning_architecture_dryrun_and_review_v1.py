#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Cognitive Zoning Architecture DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_cognitive_zoning_architecture_dryrun_and_review_v1 import (
    run_midplatform_cognitive_zoning_architecture_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_cognitive_zoning_architecture_planning"
)
DEFAULT_VNEXT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_vnext_architecture_realignment_planning"
)
DEFAULT_CR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_controlled_runtime_dryrun_and_review"
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
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_cognitive_zoning_architecture_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("cognitive_zoning_dryrun_review_policy", "cognitive_zoning_dryrun_review_policy_v1.json"),
    ("cognitive_zoning_planning_input_review", "cognitive_zoning_planning_input_review_v1.json"),
    ("cognitive_zoning_model_candidate", "cognitive_zoning_model_candidate_v1.json"),
    ("zone_inventory_dryrun_review", "zone_inventory_dryrun_review_v1.json"),
    ("zone_responsibility_matrix_review", "zone_responsibility_matrix_review_v1.json"),
    ("zone_boundary_policy_review", "zone_boundary_policy_review_v1.json"),
    ("zone_signal_contract_review", "zone_signal_contract_review_v1.json"),
    ("no_universal_brain_policy_review", "no_universal_brain_policy_review_v1.json"),
    (
        "monolithic_to_modular_life_architecture_review",
        "monolithic_to_modular_life_architecture_review_v1.json",
    ),
    ("capability_bus_positioning_review", "capability_bus_positioning_review_v1.json"),
    ("zone_to_seed_core_dependency_review", "zone_to_seed_core_dependency_review_v1.json"),
    (
        "zone_to_governance_standard_dependency_review",
        "zone_to_governance_standard_dependency_review_v1.json",
    ),
    (
        "zone_to_pluggable_capability_dependency_review",
        "zone_to_pluggable_capability_dependency_review_v1.json",
    ),
    ("zone_communication_handoff_review", "zone_communication_handoff_review_v1.json"),
    ("future_module_split_principle_review", "future_module_split_principle_review_v1.json"),
    ("cognitive_zoning_boundary_audit", "cognitive_zoning_boundary_audit_v1.json"),
    ("cognitive_zoning_blocked_path_result", "cognitive_zoning_blocked_path_result_v1.json"),
    ("cognitive_zoning_closure_decision", "cognitive_zoning_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--cognitive-zoning-planning-root", default=DEFAULT_PLANNING)
    p.add_argument("--vnext-realignment-root", default=DEFAULT_VNEXT)
    p.add_argument("--controlled-runtime-dryrun-root", default=DEFAULT_CR_DR)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER_DR)
    p.add_argument("--fmis-dryrun-root", default=DEFAULT_FMIS_DR)
    p.add_argument("--e2e-simulation-dryrun-root", default=DEFAULT_E2E_DR)
    args = p.parse_args()

    result = run_midplatform_cognitive_zoning_architecture_dryrun_and_review_v1(
        midplatform_cognitive_zoning_architecture_planning_root=args.cognitive_zoning_planning_root,
        midplatform_vnext_architecture_realignment_planning_root=args.vnext_realignment_root,
        midplatform_controlled_runtime_dryrun_and_review_root=args.controlled_runtime_dryrun_root,
        provider_abstraction_standard_alignment_dryrun_and_review_root=args.provider_abstraction_dryrun_root,
        midplatform_frontend_model_influence_simulation_dryrun_and_review_root=args.fmis_dryrun_root,
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

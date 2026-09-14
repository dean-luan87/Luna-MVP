#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Layered Capability Stack Standard Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.layered_capability_stack_standard_planning_v1 import (
    run_layered_capability_stack_standard_planning_v1,
)

DEFAULT_CB_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
)
DEFAULT_FP_DECISION_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_decision_chain_candidate_dryrun"
)
DEFAULT_VNEXT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_vnext_architecture_realignment_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/layered_capability_stack_standard_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("layered_capability_stack_standard_policy", "layered_capability_stack_standard_policy_v1.json"),
    ("constitution_bus_input_review", "constitution_bus_input_review_v1.json"),
    (
        "reusable_governance_standard_registration",
        "reusable_governance_standard_registration_v1.json",
    ),
    ("capability_stack_definition_contract", "capability_stack_definition_contract_v1.json"),
    ("universal_capability_stack_rules", "universal_capability_stack_rules_v1.json"),
    ("voice_capability_stack_reference", "voice_capability_stack_reference_v1.json"),
    ("ocr_capability_stack_reference", "ocr_capability_stack_reference_v1.json"),
    ("map_navigation_capability_stack_reference", "map_navigation_capability_stack_reference_v1.json"),
    ("memory_capability_stack_reference", "memory_capability_stack_reference_v1.json"),
    ("emotion_capability_stack_reference", "emotion_capability_stack_reference_v1.json"),
    (
        "first_person_capability_stack_reference_binding",
        "first_person_capability_stack_reference_binding_v1.json",
    ),
    ("module_onboarding_gate_policy", "module_onboarding_gate_policy_v1.json"),
    ("layered_governance_mapping_addendum", "layered_governance_mapping_addendum_v1.json"),
    (
        "constitution_bus_standard_binding_addendum",
        "constitution_bus_standard_binding_addendum_v1.json",
    ),
    ("cross_domain_stack_consistency_review", "cross_domain_stack_consistency_review_v1.json"),
    ("planning_boundary_audit", "planning_boundary_audit_v1.json"),
    ("planning_closure_decision", "planning_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB_DR)
    p.add_argument("--first-person-decision-chain-dryrun-root", default=DEFAULT_FP_DECISION_DR)
    p.add_argument("--vnext-planning-root", default=DEFAULT_VNEXT)
    args = p.parse_args()

    result = run_layered_capability_stack_standard_planning_v1(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=args.constitution_bus_dryrun_root,
        first_person_scene_understanding_decision_chain_candidate_dryrun_root=args.first_person_decision_chain_dryrun_root,
        midplatform_vnext_architecture_realignment_planning_root=args.vnext_planning_root,
        output_root=args.output_root,
    )

    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    sm = result["summary"]
    print(json.dumps({"planning_pass": sm.get("planning_pass"), "final_decision": sm.get("final_decision")}))
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())

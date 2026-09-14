#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Constitution-Capability-Bus Governance Baseline Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.luna_constitution_capability_bus_governance_baseline_planning_v1 import (
    run_luna_constitution_capability_bus_governance_baseline_planning_v1,
)

DEFAULT_II_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_information_integration_layer_dryrun_and_review"
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
DEFAULT_VNEXT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_vnext_architecture_realignment_planning"
)
DEFAULT_PROVIDER_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_dryrun_and_review"
)
DEFAULT_CR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_controlled_runtime_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "constitution_capability_bus_governance_baseline_policy",
        "constitution_capability_bus_governance_baseline_policy_v1.json",
    ),
    (
        "upstream_information_integration_input_review",
        "upstream_information_integration_input_review_v1.json",
    ),
    (
        "luna_constitution_capability_bus_governance_module",
        "luna_constitution_capability_bus_governance_module_v1.json",
    ),
    ("constitution_bus_version_manifest", "constitution_bus_version_manifest_v1.json"),
    ("constitution_bus_module_boundary", "constitution_bus_module_boundary_v1.json"),
    ("constitution_bus_responsibility_matrix", "constitution_bus_responsibility_matrix_v1.json"),
    ("constitution_to_bus_propagation_model", "constitution_to_bus_propagation_model_v1.json"),
    (
        "bus_to_module_contract_enforcement_model",
        "bus_to_module_contract_enforcement_model_v1.json",
    ),
    (
        "module_registration_governance_contract",
        "module_registration_governance_contract_v1.json",
    ),
    ("capability_bus_governance_contract", "capability_bus_governance_contract_v1.json"),
    ("governance_standard_binding_matrix", "governance_standard_binding_matrix_v1.json"),
    (
        "constitution_bus_version_compatibility_policy",
        "constitution_bus_version_compatibility_policy_v1.json",
    ),
    (
        "constitution_bus_change_propagation_policy",
        "constitution_bus_change_propagation_policy_v1.json",
    ),
    (
        "constitution_bus_non_runtime_boundary_matrix",
        "constitution_bus_non_runtime_boundary_matrix_v1.json",
    ),
    (
        "constitution_bus_future_runtime_deferment_register",
        "constitution_bus_future_runtime_deferment_register_v1.json",
    ),
    (
        "constitution_bus_external_health_oversight_policy",
        "constitution_bus_external_health_oversight_policy_v1.json",
    ),
    (
        "constitution_bus_baseline_closure_decision",
        "constitution_bus_baseline_closure_decision_v1.json",
    ),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--information-integration-dryrun-root", default=DEFAULT_II_DR)
    p.add_argument("--drive-signal-dryrun-root", default=DEFAULT_DS_DR)
    p.add_argument("--seed-core-pluggable-dryrun-root", default=DEFAULT_SC_DR)
    p.add_argument("--cognitive-zoning-dryrun-root", default=DEFAULT_CZ_DR)
    p.add_argument("--vnext-realignment-root", default=DEFAULT_VNEXT)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER_DR)
    p.add_argument("--controlled-runtime-dryrun-root", default=DEFAULT_CR_DR)
    args = p.parse_args()

    result = run_luna_constitution_capability_bus_governance_baseline_planning_v1(
        midplatform_information_integration_layer_dryrun_and_review_root=args.information_integration_dryrun_root,
        seed_core_drive_signal_contract_dryrun_and_review_root=args.drive_signal_dryrun_root,
        seed_core_pluggable_layer_architecture_dryrun_and_review_root=args.seed_core_pluggable_dryrun_root,
        midplatform_cognitive_zoning_architecture_dryrun_and_review_root=args.cognitive_zoning_dryrun_root,
        midplatform_vnext_architecture_realignment_planning_root=args.vnext_realignment_root,
        provider_abstraction_standard_alignment_dryrun_and_review_root=args.provider_abstraction_dryrun_root,
        midplatform_controlled_runtime_dryrun_and_review_root=args.controlled_runtime_dryrun_root,
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

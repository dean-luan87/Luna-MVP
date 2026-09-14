#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Seed Core / Pluggable Layer Architecture Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.seed_core_pluggable_layer_architecture_planning_v1 import (
    run_seed_core_pluggable_layer_architecture_planning_v1,
)

DEFAULT_CZ_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_cognitive_zoning_architecture_dryrun_and_review"
)
DEFAULT_CZ_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_cognitive_zoning_architecture_planning"
)
DEFAULT_VNEXT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_vnext_architecture_realignment_planning"
)
DEFAULT_PROVIDER_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_dryrun_and_review"
)
DEFAULT_CR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_controlled_runtime_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/seed_core_pluggable_layer_architecture_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "seed_core_pluggable_layer_architecture_planning_policy",
        "seed_core_pluggable_layer_architecture_planning_policy_v1.json",
    ),
    ("cognitive_zoning_input_review", "cognitive_zoning_input_review_v1.json"),
    (
        "seed_core_pluggable_layer_architecture_model",
        "seed_core_pluggable_layer_architecture_model_v1.json",
    ),
    ("fixed_seed_core_definition", "fixed_seed_core_definition_v1.json"),
    ("seed_core_component_matrix", "seed_core_component_matrix_v1.json"),
    ("survival_drive_architecture_placeholder", "survival_drive_architecture_placeholder_v1.json"),
    ("personal_continuity_module_positioning", "personal_continuity_module_positioning_v1.json"),
    ("pluggable_capability_layer_definition", "pluggable_capability_layer_definition_v1.json"),
    ("capability_module_contract", "capability_module_contract_v1.json"),
    (
        "luna_capability_bus_architecture_placeholder",
        "luna_capability_bus_architecture_placeholder_v1.json",
    ),
    ("capability_bus_responsibility_matrix", "capability_bus_responsibility_matrix_v1.json"),
    ("product_form_topology_matrix", "product_form_topology_matrix_v1.json"),
    ("invariant_vs_pluggable_boundary_review", "invariant_vs_pluggable_boundary_review_v1.json"),
    (
        "seed_core_to_cognitive_zone_influence_matrix",
        "seed_core_to_cognitive_zone_influence_matrix_v1.json",
    ),
    (
        "personal_continuity_identity_boundary_policy",
        "personal_continuity_identity_boundary_policy_v1.json",
    ),
    ("module_registration_and_discovery_plan", "module_registration_and_discovery_plan_v1.json"),
    ("module_health_permission_runtime_plan", "module_health_permission_runtime_plan_v1.json"),
    ("migration_backup_restore_risk_register", "migration_backup_restore_risk_register_v1.json"),
    ("seed_core_pluggable_layer_dryrun_plan", "seed_core_pluggable_layer_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "seed_core_pluggable_layer_architecture_planning_decision",
        "seed_core_pluggable_layer_architecture_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--cognitive-zoning-dryrun-root", default=DEFAULT_CZ_DR)
    p.add_argument("--cognitive-zoning-planning-root", default=DEFAULT_CZ_PLAN)
    p.add_argument("--vnext-realignment-root", default=DEFAULT_VNEXT)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER_DR)
    p.add_argument("--controlled-runtime-dryrun-root", default=DEFAULT_CR_DR)
    args = p.parse_args()

    result = run_seed_core_pluggable_layer_architecture_planning_v1(
        midplatform_cognitive_zoning_architecture_dryrun_and_review_root=args.cognitive_zoning_dryrun_root,
        midplatform_cognitive_zoning_architecture_planning_root=args.cognitive_zoning_planning_root,
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

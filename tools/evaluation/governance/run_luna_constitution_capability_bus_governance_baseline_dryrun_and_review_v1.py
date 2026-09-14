#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Constitution-Capability-Bus Governance Baseline DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    run_luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "constitution_bus_governance_baseline_dryrun_review_policy",
        "constitution_bus_governance_baseline_dryrun_review_policy_v1.json",
    ),
    ("constitution_bus_planning_input_review", "constitution_bus_planning_input_review_v1.json"),
    ("constitution_bus_module_dryrun_review", "constitution_bus_module_dryrun_review_v1.json"),
    ("constitution_bus_version_manifest_review", "constitution_bus_version_manifest_review_v1.json"),
    ("constitution_bus_module_boundary_review", "constitution_bus_module_boundary_review_v1.json"),
    (
        "constitution_bus_responsibility_matrix_review",
        "constitution_bus_responsibility_matrix_review_v1.json",
    ),
    ("constitution_to_bus_propagation_review", "constitution_to_bus_propagation_review_v1.json"),
    (
        "bus_to_module_contract_enforcement_review",
        "bus_to_module_contract_enforcement_review_v1.json",
    ),
    ("module_registration_governance_review", "module_registration_governance_review_v1.json"),
    ("capability_bus_governance_contract_review", "capability_bus_governance_contract_review_v1.json"),
    ("governance_standard_binding_review", "governance_standard_binding_review_v1.json"),
    (
        "constitution_bus_version_compatibility_review",
        "constitution_bus_version_compatibility_review_v1.json",
    ),
    (
        "constitution_bus_change_propagation_review",
        "constitution_bus_change_propagation_review_v1.json",
    ),
    (
        "constitution_bus_future_runtime_deferment_review",
        "constitution_bus_future_runtime_deferment_review_v1.json",
    ),
    (
        "constitution_bus_external_health_oversight_review",
        "constitution_bus_external_health_oversight_review_v1.json",
    ),
    ("constitution_bus_boundary_audit", "constitution_bus_boundary_audit_v1.json"),
    ("constitution_bus_blocked_path_result", "constitution_bus_blocked_path_result_v1.json"),
    (
        "constitution_bus_governance_baseline_closure_decision",
        "constitution_bus_governance_baseline_closure_decision_v1.json",
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
    args = p.parse_args()

    result = run_luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1(
        luna_constitution_capability_bus_governance_baseline_planning_root=args.planning_root,
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

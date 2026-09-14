#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Micro-OS Core Component Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_micro_os_core_component_planning_v1 import (
    run_midplatform_micro_os_core_component_planning_v1,
)

DEFAULT_PLANNING = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_planning"
DEFAULT_DRYRUN = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_dryrun_and_review"
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_core_component_planning"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("midplatform_core_component_scope", "midplatform_core_component_scope_v1.json"),
    (
        "midplatform_core_component_contract_collection",
        "midplatform_core_component_contract_collection_v1.json",
    ),
    (
        "midplatform_core_component_upstream_downstream_matrix",
        "midplatform_core_component_upstream_downstream_matrix_v1.json",
    ),
    (
        "midplatform_core_component_information_contract",
        "midplatform_core_component_information_contract_v1.json",
    ),
    (
        "midplatform_core_component_management_logic",
        "midplatform_core_component_management_logic_v1.json",
    ),
    (
        "midplatform_core_component_model_rule_algorithm_map",
        "midplatform_core_component_model_rule_algorithm_map_v1.json",
    ),
    (
        "midplatform_core_component_failure_route_matrix",
        "midplatform_core_component_failure_route_matrix_v1.json",
    ),
    (
        "midplatform_core_component_health_metric_mapping",
        "midplatform_core_component_health_metric_mapping_v1.json",
    ),
    ("midplatform_core_component_boundary_matrix", "midplatform_core_component_boundary_matrix_v1.json"),
    (
        "midplatform_core_component_planning_readiness_decision",
        "midplatform_core_component_planning_readiness_decision_v1.json",
    ),
    (
        "midplatform_core_component_non_claims_register",
        "midplatform_core_component_non_claims_register_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--planning-root", default=str(DEFAULT_PLANNING))
    p.add_argument("--dryrun-root", default=str(DEFAULT_DRYRUN))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_micro_os_core_component_planning_v1(
        midplatform_micro_os_architecture_planning_root=args.planning_root,
        midplatform_micro_os_architecture_dryrun_and_review_root=args.dryrun_root,
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

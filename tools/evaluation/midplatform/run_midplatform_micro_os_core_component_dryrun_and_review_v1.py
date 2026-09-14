#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Micro-OS Core Component DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_micro_os_core_component_dryrun_and_review_v1 import (
    run_midplatform_micro_os_core_component_dryrun_and_review_v1,
)

DEFAULT_COMPONENT = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_core_component_planning"
DEFAULT_ARCH_DR = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_dryrun_and_review"
DEFAULT_ARCH_PLAN = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_planning"
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_core_component_dryrun_and_review"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("core_component_contract_consumability_review", "core_component_contract_consumability_review_v1.json"),
    ("component_upstream_downstream_dryrun_review", "component_upstream_downstream_dryrun_review_v1.json"),
    ("information_contract_transfer_dryrun", "information_contract_transfer_dryrun_v1.json"),
    ("management_logic_review", "management_logic_review_v1.json"),
    ("model_rule_algorithm_placement_review", "model_rule_algorithm_placement_review_v1.json"),
    ("component_failure_route_dryrun_review", "component_failure_route_dryrun_review_v1.json"),
    ("health_metric_mapping_review", "health_metric_mapping_review_v1.json"),
    ("boundary_matrix_review", "boundary_matrix_review_v1.json"),
    ("sample_end_to_end_component_flow_dryrun", "sample_end_to_end_component_flow_dryrun_v1.json"),
    ("dryrun_issue_register", "dryrun_issue_register_v1.json"),
    ("core_component_dryrun_readiness_decision", "core_component_dryrun_readiness_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--component-planning-root", default=str(DEFAULT_COMPONENT))
    p.add_argument("--architecture-dryrun-root", default=str(DEFAULT_ARCH_DR))
    p.add_argument("--architecture-planning-root", default=str(DEFAULT_ARCH_PLAN))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_micro_os_core_component_dryrun_and_review_v1(
        midplatform_micro_os_core_component_planning_root=args.component_planning_root,
        midplatform_micro_os_architecture_dryrun_and_review_root=args.architecture_dryrun_root,
        midplatform_micro_os_architecture_planning_root=args.architecture_planning_root,
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
                "dryrun_pass": sm.get("dryrun_pass"),
                "blocker_count": sm.get("blocker_count"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())

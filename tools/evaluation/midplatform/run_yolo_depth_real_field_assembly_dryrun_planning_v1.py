#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run YOLO + Depth Real Field Assembly DryRun Planning v1."""

from __future__ import annotations

import dataclasses
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_assembly_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_ASSEMBLY_ROOT,
)
from capabilities.midplatform.yolo_depth_real_field_assembly_dryrun_planning_v1 import (
    DEFAULT_OUTPUT,
    run_yolo_depth_real_field_assembly_dryrun_planning_v1,
)

OUTPUT_FILES = (
    ("yolo_depth_real_field_assembly_dryrun_planning_report", "yolo_depth_real_field_assembly_dryrun_planning_report_v1.json"),
    ("real_frame_input_package_contract", "real_frame_input_package_contract_v1.json"),
    ("yolo_real_output_package_contract", "yolo_real_output_package_contract_v1.json"),
    ("depth_real_output_package_contract", "depth_real_output_package_contract_v1.json"),
    ("real_field_assembly_dryrun_result_candidate_contract", "real_field_assembly_dryrun_result_candidate_contract_v1.json"),
    ("real_field_assembly_success_criteria", "real_field_assembly_success_criteria_v1.json"),
    ("yolo_depth_real_dryrun_case_registry", "yolo_depth_real_dryrun_case_registry_v1.json"),
    ("real_model_execution_authorization_matrix", "real_model_execution_authorization_matrix_v1.json"),
    ("dryrun_failure_point_policy", "dryrun_failure_point_policy_v1.json"),
    ("dryrun_traceability_policy", "dryrun_traceability_policy_v1.json"),
    ("next_controlled_dryrun_plan", "next_controlled_dryrun_plan_v1.json"),
    ("non_execution_boundary_review", "non_execution_boundary_review_v1.json"),
    ("prohibited_scope", "prohibited_scope_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("summary", "summary.json"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--assembly-root", default=DEFAULT_ASSEMBLY_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_yolo_depth_real_field_assembly_dryrun_planning_v1(
        assembly_root=args.assembly_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "yolo_depth_real_field_assembly_dryrun_planning_report_v1.md").write_text(
        result["yolo_depth_real_field_assembly_dryrun_planning_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "yolo_depth_real_field_assembly_dryrun_planning_pass": s.get("yolo_depth_real_field_assembly_dryrun_planning_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "dryrun_case_count": s.get("dryrun_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

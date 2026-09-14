#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run SLAM Spatial Mapping Model Smoke IO Inspection v1."""

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

from capabilities.midplatform.model_adapter_priority_sequence_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
)
from capabilities.midplatform.slam_spatial_mapping_model_smoke_io_inspection_v1 import (
    DEFAULT_OUTPUT,
    run_slam_spatial_mapping_model_smoke_io_inspection_v1,
)

OUTPUT_FILES = (
    ("slam_spatial_mapping_model_smoke_io_inspection_report", "slam_spatial_mapping_model_smoke_io_inspection_report_v1.json"),
    ("model_smoke_run_candidate_registry", "model_smoke_run_candidate_registry_v1.json"),
    ("model_io_inspection_candidate_registry", "model_io_inspection_candidate_registry_v1.json"),
    ("model_candidate_mapping_feasibility_registry", "model_candidate_mapping_feasibility_registry_v1.json"),
    ("slam_spatial_mapping_available_model_review", "slam_spatial_mapping_available_model_review_v1.json"),
    ("slam_spatial_mapping_input_format_review", "slam_spatial_mapping_input_format_review_v1.json"),
    ("slam_spatial_mapping_output_format_review", "slam_spatial_mapping_output_format_review_v1.json"),
    ("slam_spatial_mapping_failure_point_review", "slam_spatial_mapping_failure_point_review_v1.json"),
    ("slam_spatial_mapping_candidate_mapping_review", "slam_spatial_mapping_candidate_mapping_review_v1.json"),
    ("model_execution_authorization_review", "model_execution_authorization_review_v1.json"),
    ("new_protocol_reason_required_report", "new_protocol_reason_required_report_v1.json"),
    ("owner_constraint_compliance_review", "owner_constraint_compliance_review_v1.json"),
    ("smoke_io_case_results", "smoke_io_case_results_v1.json"),
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
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_slam_spatial_mapping_model_smoke_io_inspection_v1(
        planning_root=args.planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "slam_spatial_mapping_model_smoke_io_inspection_report_v1.md").write_text(
        result["slam_spatial_mapping_model_smoke_io_inspection_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "model_smoke_io_inspection_pass": s.get("model_smoke_io_inspection_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "smoke_io_case_count": s.get("smoke_io_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

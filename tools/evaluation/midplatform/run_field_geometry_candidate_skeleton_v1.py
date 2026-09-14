#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field Geometry Candidate Skeleton v1."""

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

from capabilities.midplatform.depth_object_fusion_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FUSION_ROOT,
)
from capabilities.midplatform.field_geometry_candidate_skeleton_v1 import (
    DEFAULT_OUTPUT,
    run_field_geometry_candidate_skeleton_v1,
)

OUTPUT_FILES = (
    ("field_geometry_candidate_skeleton_report", "field_geometry_candidate_skeleton_report_v1.json"),
    ("object_spatial_state_candidate_registry", "object_spatial_state_candidate_registry_v1.json"),
    ("field_geometry_candidate_registry", "field_geometry_candidate_registry_v1.json"),
    ("pseudo_3d_projection_policy", "pseudo_3d_projection_policy_v1.json"),
    ("field_zone_assignment_policy", "field_zone_assignment_policy_v1.json"),
    ("geometry_confidence_policy", "geometry_confidence_policy_v1.json"),
    ("field_geometry_generation_result_registry", "field_geometry_generation_result_registry_v1.json"),
    ("field_geometry_mock_case_results", "field_geometry_mock_case_results_v1.json"),
    ("readiness_for_field_assembly_review", "readiness_for_field_assembly_review_v1.json"),
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
    parser.add_argument("--fusion-root", default=DEFAULT_FUSION_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_geometry_candidate_skeleton_v1(
        fusion_root=args.fusion_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "field_geometry_candidate_skeleton_report_v1.md").write_text(
        result["field_geometry_candidate_skeleton_report_md"] + "\n", encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_geometry_candidate_skeleton_pass": s.get("field_geometry_candidate_skeleton_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "mock_case_count": s.get("mock_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

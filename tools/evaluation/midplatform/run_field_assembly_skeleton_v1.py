#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field Assembly Skeleton v1."""

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
    DEFAULT_OUTPUT,
    run_field_assembly_skeleton_v1,
)
from capabilities.midplatform.field_geometry_candidate_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_GEOMETRY_ROOT,
)

OUTPUT_FILES = (
    ("field_assembly_skeleton_report", "field_assembly_skeleton_report_v1.json"),
    ("enhanced_field_entity_candidate_registry", "enhanced_field_entity_candidate_registry_v1.json"),
    ("enhanced_field_scene_candidate_registry", "enhanced_field_scene_candidate_registry_v1.json"),
    ("field_assembly_result_candidate_registry", "field_assembly_result_candidate_registry_v1.json"),
    ("field_zone_summary_registry", "field_zone_summary_registry_v1.json"),
    ("field_scene_quality_summary_registry", "field_scene_quality_summary_registry_v1.json"),
    ("field_depth_quality_summary_registry", "field_depth_quality_summary_registry_v1.json"),
    ("field_geometry_quality_summary_registry", "field_geometry_quality_summary_registry_v1.json"),
    ("field_assembly_mock_case_results", "field_assembly_mock_case_results_v1.json"),
    ("readiness_for_field_first_core_review", "readiness_for_field_first_core_review_v1.json"),
    ("readiness_for_real_model_success_path_review", "readiness_for_real_model_success_path_review_v1.json"),
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
    parser.add_argument("--geometry-root", default=DEFAULT_GEOMETRY_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_assembly_skeleton_v1(
        geometry_root=args.geometry_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "field_assembly_skeleton_report_v1.md").write_text(
        result["field_assembly_skeleton_report_md"] + "\n", encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_assembly_skeleton_pass": s.get("field_assembly_skeleton_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "mock_case_count": s.get("mock_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

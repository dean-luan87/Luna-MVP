#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run YOLO + Depth Controlled Real Model DryRun v1."""

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

from capabilities.midplatform.yolo_depth_controlled_real_model_dryrun_v1 import (
    DEFAULT_OUTPUT,
    run_yolo_depth_controlled_real_model_dryrun_v1,
)
from capabilities.midplatform.yolo_depth_real_field_assembly_dryrun_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
)

OUTPUT_FILES = (
    ("yolo_depth_controlled_real_model_dryrun_report", "yolo_depth_controlled_real_model_dryrun_report_v1.json"),
    ("real_frame_input_package_registry", "real_frame_input_package_registry_v1.json"),
    ("yolo_real_output_package_registry", "yolo_real_output_package_registry_v1.json"),
    ("depth_real_output_package_registry", "depth_real_output_package_registry_v1.json"),
    ("object_observation_candidate_from_real_yolo_registry", "object_observation_candidate_from_real_yolo_registry_v1.json"),
    ("depth_observation_candidate_from_real_depth_registry", "depth_observation_candidate_from_real_depth_registry_v1.json"),
    ("real_field_assembly_dryrun_result_candidate_registry", "real_field_assembly_dryrun_result_candidate_registry_v1.json"),
    ("real_dryrun_case_results", "real_dryrun_case_results_v1.json"),
    ("real_dryrun_failure_points", "real_dryrun_failure_points_v1.json"),
    ("real_dryrun_traceability_review", "real_dryrun_traceability_review_v1.json"),
    ("execution_authorization_review", "execution_authorization_review_v1.json"),
    ("readiness_for_success_path_hardening_review", "readiness_for_success_path_hardening_review_v1.json"),
    ("non_execution_boundary_review", "non_execution_boundary_review_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("prohibited_scope", "prohibited_scope_v1.json"),
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
    result = run_yolo_depth_controlled_real_model_dryrun_v1(
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
    (out / "yolo_depth_controlled_real_model_dryrun_report_v1.md").write_text(
        result["yolo_depth_controlled_real_model_dryrun_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "yolo_depth_controlled_real_model_dryrun_pass": s.get("yolo_depth_controlled_real_model_dryrun_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "controlled_dryrun_case_count": s.get("controlled_dryrun_case_count"),
        "enhanced_field_scene_count": s.get("enhanced_field_scene_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

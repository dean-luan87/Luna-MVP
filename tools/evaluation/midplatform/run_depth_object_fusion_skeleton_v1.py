#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Depth-Object Fusion Skeleton v1."""

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
    DEFAULT_OUTPUT,
    run_depth_object_fusion_skeleton_v1,
)
from capabilities.midplatform.multi_model_alignment_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_ALIGNMENT_ROOT,
)

OUTPUT_FILES = (
    ("depth_object_fusion_skeleton_report", "depth_object_fusion_skeleton_report_v1.json"),
    ("depth_object_fusion_input_contract", "depth_object_fusion_input_contract_v1.json"),
    ("bbox_depth_sampling_policy", "bbox_depth_sampling_policy_v1.json"),
    ("object_depth_hint_candidate_registry", "object_depth_hint_candidate_registry_v1.json"),
    ("depth_object_fusion_result_candidate_registry", "depth_object_fusion_result_candidate_registry_v1.json"),
    ("depth_bucket_field_zone_hint_policy", "depth_bucket_field_zone_hint_policy_v1.json"),
    ("depth_object_fusion_mock_case_results", "depth_object_fusion_mock_case_results_v1.json"),
    ("depth_object_fusion_fallback_policy", "depth_object_fusion_fallback_policy_v1.json"),
    ("readiness_for_field_geometry_review", "readiness_for_field_geometry_review_v1.json"),
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
    parser.add_argument("--alignment-root", default=DEFAULT_ALIGNMENT_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_depth_object_fusion_skeleton_v1(
        alignment_root=args.alignment_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "depth_object_fusion_skeleton_report_v1.md").write_text(
        result["depth_object_fusion_skeleton_report_md"] + "\n", encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "depth_object_fusion_skeleton_pass": s.get("depth_object_fusion_skeleton_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "mock_case_count": s.get("mock_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

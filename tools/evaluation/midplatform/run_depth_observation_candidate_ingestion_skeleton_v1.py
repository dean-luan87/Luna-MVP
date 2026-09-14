#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Depth Observation Candidate Ingestion Skeleton v1."""

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

from capabilities.midplatform.depth_observation_candidate_ingestion_skeleton_v1 import (
    DEFAULT_OUTPUT,
    run_depth_observation_candidate_ingestion_skeleton_v1,
)
from capabilities.midplatform.field_construction_depth_geometry_model_integration_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
)

OUTPUT_FILES = (
    ("depth_observation_candidate_ingestion_skeleton_report", "depth_observation_candidate_ingestion_skeleton_report_v1.json"),
    ("depth_model_output_mock_contract", "depth_model_output_mock_contract_v1.json"),
    ("depth_observation_candidate_contract", "depth_observation_candidate_contract_v1.json"),
    ("object_depth_hint_candidate_contract", "object_depth_hint_candidate_contract_v1.json"),
    ("depth_sampling_policy", "depth_sampling_policy_v1.json"),
    ("depth_reliability_policy", "depth_reliability_policy_v1.json"),
    ("yolo_depth_alignment_policy", "yolo_depth_alignment_policy_v1.json"),
    ("depth_missing_fallback_execution_policy", "depth_missing_fallback_execution_policy_v1.json"),
    ("depth_ingestion_mock_case_results", "depth_ingestion_mock_case_results_v1.json"),
    ("field_geometry_readiness_review", "field_geometry_readiness_review_v1.json"),
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
    result = run_depth_observation_candidate_ingestion_skeleton_v1(
        planning_root=args.planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "depth_observation_candidate_ingestion_skeleton_report_v1.md").write_text(
        result["depth_observation_candidate_ingestion_skeleton_report_md"] + "\n", encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "depth_observation_candidate_ingestion_skeleton_pass": s.get("depth_observation_candidate_ingestion_skeleton_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "mock_case_count": s.get("mock_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

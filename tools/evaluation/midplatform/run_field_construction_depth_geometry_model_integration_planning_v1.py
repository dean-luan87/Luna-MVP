#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field Construction Depth / Geometry Model Integration Planning v1."""

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

from capabilities.midplatform.field_construction_depth_geometry_model_integration_planning_v1 import (
    DEFAULT_OUTPUT,
    run_field_construction_depth_geometry_model_integration_planning_v1,
)
from capabilities.midplatform.real_observation_candidate_ingestion_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_INGESTION_ROOT,
)

OUTPUT_FILES = (
    ("field_construction_depth_geometry_model_integration_planning_report", "field_construction_depth_geometry_model_integration_planning_report_v1.json"),
    ("depth_model_adapter_plan", "depth_model_adapter_plan_v1.json"),
    ("depth_observation_candidate_contract", "depth_observation_candidate_contract_v1.json"),
    ("object_depth_hint_candidate_contract", "object_depth_hint_candidate_contract_v1.json"),
    ("field_geometry_candidate_contract", "field_geometry_candidate_contract_v1.json"),
    ("yolo_depth_fusion_mapping", "yolo_depth_fusion_mapping_v1.json"),
    ("spatial_relation_candidate_contract", "spatial_relation_candidate_contract_v1.json"),
    ("field_construction_model_priority_plan", "field_construction_model_priority_plan_v1.json"),
    ("field_geometry_adapter_plan", "field_geometry_adapter_plan_v1.json"),
    ("depth_unreliable_fallback_execution_policy", "depth_unreliable_fallback_execution_policy_v1.json"),
    ("streaming_3d_slam_candidate_review", "streaming_3d_slam_candidate_review_v1.json"),
    ("scene_graph_spatial_relation_review", "scene_graph_spatial_relation_review_v1.json"),
    ("field_scene_candidate_enhancement_plan", "field_scene_candidate_enhancement_plan_v1.json"),
    ("depth_model_download_authorization_status", "depth_model_download_authorization_status_v1.json"),
    ("field_construction_planning_case_registry", "field_construction_planning_case_registry_v1.json"),
    ("field_construction_planning_rules", "field_construction_planning_rules_v1.json"),
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
    parser.add_argument("--ingestion-root", default=DEFAULT_INGESTION_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_construction_depth_geometry_model_integration_planning_v1(
        ingestion_root=args.ingestion_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "field_construction_depth_geometry_model_integration_planning_report_v1.md").write_text(
        result["field_construction_depth_geometry_model_integration_planning_report_md"] + "\n", encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_construction_depth_geometry_model_integration_planning_pass": s.get("field_construction_depth_geometry_model_integration_planning_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "mock_case_count": s.get("mock_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

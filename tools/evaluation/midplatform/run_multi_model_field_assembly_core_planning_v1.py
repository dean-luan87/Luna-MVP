#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Multi-Model Field Assembly Core Planning v1."""

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
    DEFAULT_OUTPUT as DEFAULT_DEPTH_INGESTION_ROOT,
)
from capabilities.midplatform.multi_model_field_assembly_core_planning_v1 import (
    DEFAULT_OUTPUT,
    run_multi_model_field_assembly_core_planning_v1,
)

OUTPUT_FILES = (
    ("multi_model_field_assembly_core_planning_report", "multi_model_field_assembly_core_planning_report_v1.json"),
    ("multi_model_role_registry", "multi_model_role_registry_v1.json"),
    ("multi_model_interaction_policy", "multi_model_interaction_policy_v1.json"),
    ("multi_model_alignment_policy", "multi_model_alignment_policy_v1.json"),
    ("object_depth_linking_policy", "object_depth_linking_policy_v1.json"),
    ("confidence_fusion_policy", "confidence_fusion_policy_v1.json"),
    ("conflict_handling_policy", "conflict_handling_policy_v1.json"),
    ("missing_model_fallback_policy", "missing_model_fallback_policy_v1.json"),
    ("field_geometry_candidate_contract", "field_geometry_candidate_contract_v1.json"),
    ("multi_model_aligned_observation_candidate_contract", "multi_model_aligned_observation_candidate_contract_v1.json"),
    ("field_assembly_result_candidate_contract", "field_assembly_result_candidate_contract_v1.json"),
    ("field_assembly_plan", "field_assembly_plan_v1.json"),
    ("multi_model_field_assembly_mock_case_registry", "multi_model_field_assembly_mock_case_registry_v1.json"),
    ("next_implementation_sequence", "next_implementation_sequence_v1.json"),
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
    parser.add_argument("--depth-ingestion-root", default=DEFAULT_DEPTH_INGESTION_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_multi_model_field_assembly_core_planning_v1(
        depth_ingestion_root=args.depth_ingestion_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "multi_model_field_assembly_core_planning_report_v1.md").write_text(
        result["multi_model_field_assembly_core_planning_report_md"] + "\n", encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "multi_model_field_assembly_core_planning_pass": s.get("multi_model_field_assembly_core_planning_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "mock_case_count": s.get("mock_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

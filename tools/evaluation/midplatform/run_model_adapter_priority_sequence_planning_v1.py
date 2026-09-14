#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Model Adapter Priority Sequence Planning v1."""

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
    DEFAULT_OUTPUT,
    run_model_adapter_priority_sequence_planning_v1,
)
from capabilities.midplatform.model_workflow_protocol_reuse_and_cleanup_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_CLEANUP_ROOT,
)

OUTPUT_FILES = (
    ("model_adapter_priority_sequence_planning_report", "model_adapter_priority_sequence_planning_report_v1.json"),
    ("model_adapter_priority_registry", "model_adapter_priority_registry_v1.json"),
    ("model_adapter_reuse_path_registry", "model_adapter_reuse_path_registry_v1.json"),
    ("world_model_construction_model_mapping", "world_model_construction_model_mapping_v1.json"),
    ("task_collaboration_model_mapping", "task_collaboration_model_mapping_v1.json"),
    ("scenario_2_to_3_model_group_registry", "scenario_2_to_3_model_group_registry_v1.json"),
    ("model_adapter_protocol_reuse_decision", "model_adapter_protocol_reuse_decision_v1.json"),
    ("model_adapter_new_protocol_reason_required_report", "model_adapter_new_protocol_reason_required_report_v1.json"),
    ("next_model_adapter_skeleton_recommendation", "next_model_adapter_skeleton_recommendation_v1.json"),
    ("deferred_model_adapter_registry", "deferred_model_adapter_registry_v1.json"),
    ("owner_constraint_compliance_review", "owner_constraint_compliance_review_v1.json"),
    ("planning_case_results", "planning_case_results_v1.json"),
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
    parser.add_argument("--cleanup-root", default=DEFAULT_CLEANUP_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_model_adapter_priority_sequence_planning_v1(
        cleanup_root=args.cleanup_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "model_adapter_priority_sequence_planning_report_v1.md").write_text(
        result["model_adapter_priority_sequence_planning_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "model_adapter_priority_sequence_planning_pass": s.get("model_adapter_priority_sequence_planning_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "next_adapter": "slam_spatial_mapping",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

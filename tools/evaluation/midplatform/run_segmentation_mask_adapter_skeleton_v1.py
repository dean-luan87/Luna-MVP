#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Segmentation / Mask Adapter Skeleton v1."""

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

from capabilities.midplatform.segmentation_mask_adapter_skeleton_v1 import (
    DEFAULT_OUTPUT,
    run_segmentation_mask_adapter_skeleton_v1,
)
from capabilities.midplatform.segmentation_mask_model_smoke_io_inspection_v1 import (
    DEFAULT_OUTPUT as DEFAULT_SMOKE_IO_ROOT,
)

OUTPUT_FILES = (
    ("segmentation_mask_adapter_skeleton_report", "segmentation_mask_adapter_skeleton_report_v1.json"),
    ("segmentation_mask_adapter_input_registry", "segmentation_mask_adapter_input_registry_v1.json"),
    ("segmentation_mask_raw_output_candidate_registry", "segmentation_mask_raw_output_candidate_registry_v1.json"),
    ("mask_observation_candidate_registry", "mask_observation_candidate_registry_v1.json"),
    ("object_boundary_candidate_registry", "object_boundary_candidate_registry_v1.json"),
    ("freespace_candidate_registry", "freespace_candidate_registry_v1.json"),
    ("region_observation_candidate_registry", "region_observation_candidate_registry_v1.json"),
    ("mask_quality_candidate_registry", "mask_quality_candidate_registry_v1.json"),
    ("segmentation_mask_adapter_result_candidate_registry", "segmentation_mask_adapter_result_candidate_registry_v1.json"),
    ("segmentation_mask_task_collaboration_readiness_review", "segmentation_mask_task_collaboration_readiness_review_v1.json"),
    ("segmentation_mask_later_world_model_readiness_review", "segmentation_mask_later_world_model_readiness_review_v1.json"),
    ("protocol_reuse_decision", "protocol_reuse_decision_v1.json"),
    ("new_protocol_reason_required_report", "new_protocol_reason_required_report_v1.json"),
    ("no_action_boundary_review", "no_action_boundary_review_v1.json"),
    ("no_world_model_assembly_boundary_review", "no_world_model_assembly_boundary_review_v1.json"),
    ("owner_constraint_compliance_review", "owner_constraint_compliance_review_v1.json"),
    ("skeleton_case_results", "skeleton_case_results_v1.json"),
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
    parser.add_argument("--smoke-io-root", default=DEFAULT_SMOKE_IO_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_segmentation_mask_adapter_skeleton_v1(
        smoke_io_root=args.smoke_io_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "segmentation_mask_adapter_skeleton_report_v1.md").write_text(
        result["segmentation_mask_adapter_skeleton_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "segmentation_mask_adapter_skeleton_pass": s.get("segmentation_mask_adapter_skeleton_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "skeleton_case_count": s.get("skeleton_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

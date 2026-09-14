#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Task Manager / Owner Approval canonical GO checkpoint rebuild v1."""

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

from capabilities.midplatform.task_manager_owner_approval_canonical_go_checkpoint_rebuild_items_v1 import (
    DEFAULT_OUTPUT,
    PASS_FLAG,
)
from capabilities.midplatform.task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1 import (
    run_task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1,
)

OUTPUT_FILES = (
    ("task_manager_owner_approval_canonical_go_checkpoint_rebuild_report", "task_manager_owner_approval_canonical_go_checkpoint_rebuild_report_v1.json"),
    ("canonical_checkpoint_registry", "canonical_checkpoint_registry_v1.json"),
    ("downstream_readable_checkpoint_index", "downstream_readable_checkpoint_index_v1.json"),
    ("final_decision_mapping_registry", "final_decision_mapping_registry_v1.json"),
    ("upstream_downstream_reference_map", "upstream_downstream_reference_map_v1.json"),
    ("first_failed_stage_review", "first_failed_stage_review_v1.json"),
    ("failed_stage_registry", "failed_stage_registry_v1.json"),
    ("downstream_blockage_projection", "downstream_blockage_projection_v1.json"),
    ("canonical_checkpoint_gap_classification", "canonical_checkpoint_gap_classification_v1.json"),
    ("checkpoint_rebuild_repair_plan", "checkpoint_rebuild_repair_plan_v1.json"),
    ("checkpoint_rebuild_execution_mode_review", "checkpoint_rebuild_execution_mode_review_v1.json"),
    ("no_original_stage_pollution_review", "no_original_stage_pollution_review_v1.json"),
    ("no_protocol_change_review", "no_protocol_change_review_v1.json"),
    ("no_world_model_boundary_review", "no_world_model_boundary_review_v1.json"),
    ("no_model_route_touched_review", "no_model_route_touched_review_v1.json"),
    ("owner_constraint_compliance_review", "owner_constraint_compliance_review_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("summary", "summary.json"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    if isinstance(obj, Path):
        return str(obj)
    return str(obj)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--mode",
        default="topdown-rerun",
        choices=("scan-only", "topdown-rerun"),
        help="scan-only: read existing artifacts; topdown-rerun: run original runner/verifier top-down",
    )
    args = parser.parse_args()
    result = run_task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1(
        output_root=args.output_root,
        mode=args.mode,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "task_manager_owner_approval_canonical_go_checkpoint_rebuild_report_v1.md").write_text(
        result["task_manager_owner_approval_canonical_go_checkpoint_rebuild_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        PASS_FLAG: s.get(PASS_FLAG),
        "execution_mode": s.get("execution_mode"),
        "first_failed_stage_key": s.get("first_failed_stage_key"),
        "go_stage_count": s.get("go_stage_count"),
        "hold_stage_count": s.get("hold_stage_count"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

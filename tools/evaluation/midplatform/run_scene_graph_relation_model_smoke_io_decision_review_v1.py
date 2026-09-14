#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Scene Graph / Relation Model Smoke IO Decision Review v1."""

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

from capabilities.midplatform.scene_graph_relation_model_smoke_io_decision_review_v1 import (
    DEFAULT_OUTPUT,
    run_scene_graph_relation_model_smoke_io_decision_review_v1,
)
from capabilities.midplatform.segmentation_mask_task_collaboration_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_TASK_PLANNING_ROOT,
)

OUTPUT_FILES = (
    ("scene_graph_relation_model_smoke_io_decision_review_report", "scene_graph_relation_model_smoke_io_decision_review_report_v1.json"),
    ("scene_graph_relation_input_source_review", "scene_graph_relation_input_source_review_v1.json"),
    ("scene_graph_relation_candidate_dependency_review", "scene_graph_relation_candidate_dependency_review_v1.json"),
    ("scene_graph_relation_deferred_status_review", "scene_graph_relation_deferred_status_review_v1.json"),
    ("scene_graph_relation_smoke_io_eligibility_review", "scene_graph_relation_smoke_io_eligibility_review_v1.json"),
    ("scene_graph_relation_next_phase_decision", "scene_graph_relation_next_phase_decision_v1.json"),
    ("scene_graph_relation_protocol_reuse_decision", "scene_graph_relation_protocol_reuse_decision_v1.json"),
    ("new_protocol_reason_required_report", "new_protocol_reason_required_report_v1.json"),
    ("no_relation_candidate_generation_review", "no_relation_candidate_generation_review_v1.json"),
    ("no_world_model_assembly_boundary_review", "no_world_model_assembly_boundary_review_v1.json"),
    ("owner_constraint_compliance_review", "owner_constraint_compliance_review_v1.json"),
    ("non_execution_boundary_review", "non_execution_boundary_review_v1.json"),
    ("prohibited_scope", "prohibited_scope_v1.json"),
    ("decision_case_registry", "decision_case_registry_v1.json"),
    ("scene_graph_relation_candidate_registry_review", "scene_graph_relation_candidate_registry_review_v1.json"),
    ("scene_graph_relation_prerequisite_chain_review", "scene_graph_relation_prerequisite_chain_review_v1.json"),
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
    parser.add_argument("--task-planning-root", default=DEFAULT_TASK_PLANNING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_scene_graph_relation_model_smoke_io_decision_review_v1(
        task_planning_root=args.task_planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "scene_graph_relation_model_smoke_io_decision_review_report_v1.md").write_text(
        result["scene_graph_relation_model_smoke_io_decision_review_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "scene_graph_relation_model_smoke_io_decision_review_pass": s.get("scene_graph_relation_model_smoke_io_decision_review_pass"),
        "smoke_io_allowed": s.get("smoke_io_allowed"),
        "scene_graph_still_deferred": s.get("scene_graph_still_deferred"),
        "selected_option": s.get("selected_option"),
        "overall_input_sufficiency": s.get("overall_input_sufficiency"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "decision_case_count": s.get("decision_case_count"),
        "prerequisite_go_count": s.get("prerequisite_go_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

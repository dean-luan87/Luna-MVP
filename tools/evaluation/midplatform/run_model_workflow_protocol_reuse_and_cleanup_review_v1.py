#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Model Workflow Protocol Reuse And Cleanup Review v1."""

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

from capabilities.midplatform.model_workflow_protocol_reuse_and_cleanup_review_v1 import (
    DEFAULT_OUTPUT,
    run_model_workflow_protocol_reuse_and_cleanup_review_v1,
)
from capabilities.midplatform.real_model_field_construction_execution_path_hardening_v1 import (
    DEFAULT_OUTPUT as DEFAULT_EXEC_PATH_ROOT,
)
from capabilities.midplatform.task_manager_broader_midplatform_closure_roadmap_v1 import (
    DEFAULT_OUTPUT as DEFAULT_BROADER_ROADMAP_ROOT,
)

OUTPUT_FILES = (
    ("model_workflow_protocol_reuse_and_cleanup_review_report", "model_workflow_protocol_reuse_and_cleanup_review_report_v1.json"),
    ("active_mainline_file_registry", "active_mainline_file_registry_v1.json"),
    ("deprecated_file_registry", "deprecated_file_registry_v1.json"),
    ("cleanup_required_file_registry", "cleanup_required_file_registry_v1.json"),
    ("protocol_reuse_review", "protocol_reuse_review_v1.json"),
    ("protocol_overreach_review", "protocol_overreach_review_v1.json"),
    ("field_simulation_deactivation_review", "field_simulation_deactivation_review_v1.json"),
    ("task_reasoning_defer_review", "task_reasoning_defer_review_v1.json"),
    ("world_model_candidate_scope_review", "world_model_candidate_scope_review_v1.json"),
    ("model_task_collaboration_scope_review", "model_task_collaboration_scope_review_v1.json"),
    ("next_allowed_phase_recommendation", "next_allowed_phase_recommendation_v1.json"),
    ("review_case_results", "cleanup_review_case_results_v1.json"),
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
    parser.add_argument("--broader-roadmap-root", default=DEFAULT_BROADER_ROADMAP_ROOT)
    parser.add_argument("--exec-path-root", default=DEFAULT_EXEC_PATH_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_model_workflow_protocol_reuse_and_cleanup_review_v1(
        broader_roadmap_root=args.broader_roadmap_root,
        exec_path_root=args.exec_path_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "model_workflow_protocol_reuse_and_cleanup_review_report_v1.md").write_text(
        result["model_workflow_protocol_reuse_and_cleanup_review_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "cleanup_review_pass": s.get("cleanup_review_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "active_count": s.get("active_mainline_registry_complete"),
        "field_simulation_deactivated": s.get("field_simulation_deactivated_from_mainline"),
    }, ensure_ascii=False))
    return 0 if s.get("cleanup_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())

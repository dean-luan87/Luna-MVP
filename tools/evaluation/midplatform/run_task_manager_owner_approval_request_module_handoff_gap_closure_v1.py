#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run module handoff gap closure v1."""

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

from capabilities.midplatform.task_manager_owner_approval_request_module_handoff_gap_closure_items_v1 import DEFAULT_OUTPUT
from capabilities.midplatform.task_manager_owner_approval_request_module_handoff_gap_closure_v1 import (
    run_task_manager_owner_approval_request_module_handoff_gap_closure_v1,
)

OUTPUT_FILES = (
    ("task_manager_owner_approval_request_module_handoff_gap_closure_report", "task_manager_owner_approval_request_module_handoff_gap_closure_report_v1.json"),
    ("module_handoff_gap_review", "module_handoff_gap_review_v1.json"),
    ("downstream_roadmap_expected_artifact_review", "downstream_roadmap_expected_artifact_review_v1.json"),
    ("owner_approval_request_handoff_artifact_visibility_review", "owner_approval_request_handoff_artifact_visibility_review_v1.json"),
    ("handoff_output_field_alignment_review", "handoff_output_field_alignment_review_v1.json"),
    ("task_manager_owner_approval_request_module_handoff_rerun_review", "task_manager_owner_approval_request_module_handoff_rerun_review_v1.json"),
    ("task_manager_broader_midplatform_closure_roadmap_readiness_review", "task_manager_broader_midplatform_closure_roadmap_readiness_review_v1.json"),
    ("no_protocol_change_review", "no_protocol_change_review_v1.json"),
    ("owner_constraint_compliance_review", "owner_constraint_compliance_review_v1.json"),
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
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_owner_approval_request_module_handoff_gap_closure_v1(output_root=args.output_root)
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "task_manager_owner_approval_request_module_handoff_gap_closure_report_v1.md").write_text(
        result["task_manager_owner_approval_request_module_handoff_gap_closure_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "task_manager_owner_approval_request_module_handoff_gap_closure_pass": s.get("task_manager_owner_approval_request_module_handoff_gap_closure_pass"),
        "owner_approval_request_module_handoff_go": s.get("owner_approval_request_module_handoff_go"),
        "broader_midplatform_closure_roadmap_go": s.get("broader_midplatform_closure_roadmap_go"),
        "first_unresolved_handoff_gap_identified": s.get("first_unresolved_handoff_gap_identified"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR / Text Task Collaboration Planning v1."""

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

from capabilities.midplatform.ocr_text_adapter_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_SKELETON_ROOT,
)
from capabilities.midplatform.ocr_text_task_collaboration_planning_v1 import (
    DEFAULT_OUTPUT,
    run_ocr_text_task_collaboration_planning_v1,
)

OUTPUT_FILES = (
    ("ocr_text_task_collaboration_planning_report", "ocr_text_task_collaboration_planning_report_v1.json"),
    ("ocr_text_task_collaboration_model_group_registry", "ocr_text_task_collaboration_model_group_registry_v1.json"),
    ("ocr_text_task_input_mapping_review", "ocr_text_task_input_mapping_review_v1.json"),
    ("ocr_text_task_output_evidence_mapping_review", "ocr_text_task_output_evidence_mapping_review_v1.json"),
    ("ocr_text_task_invocation_control_review", "ocr_text_task_invocation_control_review_v1.json"),
    ("ocr_text_task_failure_degradation_policy", "ocr_text_task_failure_degradation_policy_v1.json"),
    ("ocr_text_task_collaboration_case_registry", "ocr_text_task_collaboration_case_registry_v1.json"),
    ("ocr_text_task_collaboration_protocol_reuse_decision", "ocr_text_task_collaboration_protocol_reuse_decision_v1.json"),
    ("new_protocol_reason_required_report", "new_protocol_reason_required_report_v1.json"),
    ("no_action_boundary_review", "no_action_boundary_review_v1.json"),
    ("no_world_model_assembly_boundary_review", "no_world_model_assembly_boundary_review_v1.json"),
    ("owner_constraint_compliance_review", "owner_constraint_compliance_review_v1.json"),
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
    parser.add_argument("--skeleton-root", default=DEFAULT_SKELETON_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_ocr_text_task_collaboration_planning_v1(
        skeleton_root=args.skeleton_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "ocr_text_task_collaboration_planning_report_v1.md").write_text(
        result["ocr_text_task_collaboration_planning_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "ocr_text_task_collaboration_planning_pass": s.get("ocr_text_task_collaboration_planning_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "planning_case_count": s.get("planning_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

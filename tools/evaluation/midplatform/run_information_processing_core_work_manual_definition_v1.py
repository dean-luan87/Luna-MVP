#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Information Processing Core Work Manual Definition v1."""

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

from capabilities.midplatform.information_processing_core_work_manual_definition_v1 import (
    DEFAULT_OUTPUT,
    DEFAULT_WORK_MANUAL_MAPPING_ROOT,
    run_information_processing_core_work_manual_definition_v1,
)

OUTPUT_FILES = (
    ("organization_context", "organization_context_v1.json"),
    ("core_work_definition", "core_work_definition_v1.json"),
    ("role_job_definition", "role_job_definition_v1.json"),
    ("work_detail", "work_detail_v1.json"),
    ("internal_workflow", "internal_workflow_v1.json"),
    ("external_workflow", "external_workflow_v1.json"),
    ("judge_referee_rules", "judge_referee_rules_v1.json"),
    ("governance_protocol_boundary_service_rules", "governance_protocol_boundary_service_rules_v1.json"),
    ("workload_control", "workload_control_v1.json"),
    ("qualification_standard", "qualification_standard_v1.json"),
    ("future_expansion", "future_expansion_v1.json"),
    ("implementation_readiness_review", "implementation_readiness_review_v1.json"),
    ("next_route_decision", "next_route_decision_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("summary", "summary.json"),
)

MD_FILES = (
    ("organization_context_md", "organization_context_v1.md"),
    ("role_job_definition_md", "role_job_definition_v1.md"),
    ("work_detail_md", "work_detail_v1.md"),
    ("internal_workflow_md", "internal_workflow_v1.md"),
    ("external_workflow_md", "external_workflow_v1.md"),
    ("information_processing_core_work_manual_report_md", "information_processing_core_work_manual_report_v1.md"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--work-manual-mapping-root", default=DEFAULT_WORK_MANUAL_MAPPING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_information_processing_core_work_manual_definition_v1(
        work_manual_mapping_root=args.work_manual_mapping_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    for key, fname in MD_FILES:
        content = result.get(key, "")
        if content:
            (out / fname).write_text(content + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "information_processing_core_work_manual_definition_pass": s.get("information_processing_core_work_manual_definition_pass"),
        "selected_next_route": s.get("selected_next_route"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run IPC Self-Work Core Capability DryRun v1."""

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

from capabilities.midplatform.information_processing_core_self_work_core_capability_dryrun_v1 import (
    DEFAULT_IPC_IMPL_ROOT,
    DEFAULT_OUTPUT,
    run_information_processing_core_self_work_core_capability_dryrun_v1,
)

OUTPUT_FILES = (
    ("ipc_self_work_core_capability_dryrun_report", "ipc_self_work_core_capability_dryrun_report_v1.json"),
    ("three_part_work_model_positioning", "three_part_work_model_positioning_v1.json"),
    ("ipc_self_work_scope", "ipc_self_work_scope_v1.json"),
    ("ipc_internal_processing_logic_dryrun_cases", "ipc_internal_processing_logic_dryrun_cases_v1.json"),
    ("ipc_internal_processing_logic_dryrun_results", "ipc_internal_processing_logic_dryrun_results_v1.json"),
    ("ipc_conclusion_model", "ipc_conclusion_model_v1.json"),
    ("ipc_transparency_traceability_model", "ipc_transparency_traceability_model_v1.json"),
    ("ipc_self_check_internal_referee", "ipc_self_check_internal_referee_v1.json"),
    ("ipc_workload_control_self_validation", "ipc_workload_control_self_validation_v1.json"),
    ("downstream_need_extraction", "downstream_need_extraction_v1.json"),
    ("upstream_assumption_register", "upstream_assumption_register_v1.json"),
    ("core_qualification_result", "core_qualification_result_v1.json"),
    ("next_route_decision", "next_route_decision_v1.json"),
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
    parser.add_argument("--ipc-implementation-root", default=DEFAULT_IPC_IMPL_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_information_processing_core_self_work_core_capability_dryrun_v1(
        ipc_implementation_root=args.ipc_implementation_root, output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "ipc_self_work_core_capability_dryrun_report_v1.md").write_text(result["ipc_self_work_core_capability_dryrun_report_md"] + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({"output_root": str(out), "ipc_core_self_work_dryrun_ok": s.get("ipc_core_self_work_dryrun_ok"),
                      "all_self_work_cases_passed": s.get("all_self_work_cases_passed"),
                      "final_decision": s.get("final_decision"), "recommended_next_phase": s.get("recommended_next_phase")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

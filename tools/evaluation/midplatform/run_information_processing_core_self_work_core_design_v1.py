#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run IPC Self-Work Core Design v1."""

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

from capabilities.midplatform.information_processing_core_self_work_core_design_v1 import (
    DEFAULT_IPC_IMPL_ROOT,
    DEFAULT_OUTPUT,
    run_information_processing_core_self_work_core_design_v1,
)

OUTPUT_FILES = (
    ("ipc_self_work_core_design_report", "ipc_self_work_core_design_report_v1.json"),
    ("three_part_work_model_positioning", "three_part_work_model_positioning_v1.json"),
    ("ipc_self_work_scope", "ipc_self_work_scope_v1.json"),
    ("ipc_internal_processing_flow", "ipc_internal_processing_flow_v1.json"),
    ("ipc_conclusion_model", "ipc_conclusion_model_v1.json"),
    ("ipc_transparency_traceability_model", "ipc_transparency_traceability_model_v1.json"),
    ("ipc_self_check_referee_model", "ipc_self_check_referee_model_v1.json"),
    ("ipc_workload_control_model", "ipc_workload_control_model_v1.json"),
    ("downstream_need_observation_model", "downstream_need_observation_model_v1.json"),
    ("upstream_minimum_assumption_register", "upstream_minimum_assumption_register_v1.json"),
    ("current_non_goals", "current_non_goals_v1.json"),
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
    result = run_information_processing_core_self_work_core_design_v1(
        ipc_implementation_root=args.ipc_implementation_root, output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "ipc_self_work_core_design_report_v1.md").write_text(result["ipc_self_work_core_design_report_md"] + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({"output_root": str(out), "information_processing_core_self_work_core_design_pass": s.get("information_processing_core_self_work_core_design_pass"),
                      "final_decision": s.get("final_decision"), "recommended_next_phase": s.get("recommended_next_phase")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Protocol Canonical Standard Shared Code DryRun v1."""

from __future__ import annotations

import dataclasses
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.protocol_canonical_standard_planning_v1 import DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT
from capabilities.midplatform.protocol_canonical_standard_shared_code_dryrun_v1 import (
    DEFAULT_OUTPUT,
    run_protocol_canonical_standard_shared_code_dryrun_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("protocol_shared_code_dryrun_report", "protocol_shared_code_dryrun_report_v1.json"),
    ("protocol_shared_code_import_validation", "protocol_shared_code_import_validation_v1.json"),
    ("protocol_id_builder_validation", "protocol_id_builder_validation_v1.json"),
    ("protocol_error_code_builder_validation", "protocol_error_code_builder_validation_v1.json"),
    ("protocol_header_validation", "protocol_header_validation_v1.json"),
    ("protocol_execution_result_validation", "protocol_execution_result_validation_v1.json"),
    ("protocol_error_object_validation", "protocol_error_object_validation_v1.json"),
    ("protocol_registry_validation", "protocol_registry_validation_v1.json"),
    ("protocol_checker_flow_validation", "protocol_checker_flow_validation_v1.json"),
    (
        "protocol_whitebox_binding_candidate_validation",
        "protocol_whitebox_binding_candidate_validation_v1.json",
    ),
    ("protocol_health_monitor_contract_validation", "protocol_health_monitor_contract_validation_v1.json"),
    (
        "existing_protocol_classification_reuse_validation",
        "existing_protocol_classification_reuse_validation_v1.json",
    ),
    ("protocol_governance_debt_preservation", "protocol_governance_debt_preservation_v1.json"),
    ("protocol_shared_code_non_runtime_constraints", "protocol_shared_code_non_runtime_constraints_v1.json"),
    ("protocol_shared_code_post_review_readiness", "protocol_shared_code_post_review_readiness_v1.json"),
    ("summary", "summary.json"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_protocol_canonical_standard_shared_code_dryrun_v1(
        planning_root=args.planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "protocol_shared_code_dryrun_report_v1.md").write_text(
        result["protocol_shared_code_dryrun_report_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "dryrun_pass": summary.get("dryrun_pass"),
                "blocker_count": summary.get("blocker_count"),
                "shared_code_imports_ok": summary.get("shared_code_imports_ok"),
                "protocol_checker_flow_validation_ok": summary.get("protocol_checker_flow_validation_ok"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase_primary": summary.get("recommended_next_phase_primary"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("dryrun_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())

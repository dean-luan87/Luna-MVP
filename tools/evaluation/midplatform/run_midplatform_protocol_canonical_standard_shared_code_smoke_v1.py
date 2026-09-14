#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Protocol Canonical Standard Shared Code Smoke v1."""

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
from capabilities.midplatform.protocol_canonical_standard_shared_code_smoke_v1 import (
    DEFAULT_OUTPUT,
    run_protocol_canonical_standard_shared_code_smoke_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("protocol_shared_code_smoke_report", "protocol_shared_code_smoke_report_v1.json"),
    ("protocol_shared_code_smoke_validation", "protocol_shared_code_smoke_validation_v1.json"),
    ("protocol_standard_reference_rule", "protocol_standard_reference_rule_v1.json"),
    (
        "protocol_constraint_vs_module_logic_separation_rule",
        "protocol_constraint_vs_module_logic_separation_rule_v1.json",
    ),
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
    result = run_protocol_canonical_standard_shared_code_smoke_v1(
        planning_root=args.planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "protocol_shared_code_smoke_report_v1.md").write_text(
        result["protocol_shared_code_smoke_report_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "smoke_pass": summary.get("smoke_pass"),
                "blocker_count": summary.get("blocker_count"),
                "shared_code_imports_ok": summary.get("shared_code_imports_ok"),
                "ready_for_task_manager_owner_approval_dryrun": summary.get(
                    "ready_for_task_manager_owner_approval_dryrun"
                ),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("smoke_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())

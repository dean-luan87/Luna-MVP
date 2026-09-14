#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-SystemHealthCenter-Governance-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities").is_dir():
            sibling = parent.parent / "Luna-Workspace-Min"
            if (sibling / "_eval_out").is_dir():
                return sibling
            if (parent / "_eval_out").is_dir():
                return parent
            return parent
    return here.parents[4]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.system_health.system_health_center_governance_v0 import run_system_health_center_governance_v0

    (
        summary,
        module_schema,
        failure_enum,
        recovery_enum,
        operating_enum,
        mask_schema,
        aggregation,
        recovery_policy,
        sim_link,
        examples,
        boundary,
        snapshot_schema,
        plan_schema,
        whitebox,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_system_health_center_governance_v0()

    summary["output_root"] = str(out)
    summary["errors"] = list(errs)
    summary["phase_verdict_hint"] = "GO" if not errs else "NO_GO"

    _write_json(out / "system_health_center_governance_summary.json", summary)
    _write_json(out / "system_health_module_health_report_schema.json", module_schema)
    _write_json(out / "system_health_failure_class_enum.json", failure_enum)
    _write_json(out / "system_health_recovery_action_enum.json", recovery_enum)
    _write_json(out / "system_health_operating_mode_enum.json", operating_enum)
    _write_json(out / "system_health_capability_mask_schema.json", mask_schema)
    _write_json(out / "system_health_aggregation_policy.json", aggregation)
    _write_json(out / "system_health_recovery_decision_policy.json", recovery_policy)
    _write_json(out / "system_health_simulation_lab_link_report.json", sim_link)
    _write_json(out / "system_health_example_module_reports.json", examples)
    _write_json(out / "system_health_governance_boundary_report.json", boundary)
    _write_json(out / "system_health_snapshot_schema.json", snapshot_schema)
    _write_json(out / "system_health_recovery_action_plan_schema.json", plan_schema)
    _write_json(out / "system_health_whitebox_audit_link_policy.json", whitebox)
    _write_json(out / "system_health_governance_non_claims_report.json", non_claims)
    _write_json(out / "system_health_governance_open_followups.json", followups)
    _write_json(out / "system_health_governance_audit_report.json", audit)
    (out / "system_health_governance_notes.md").write_text(
        "\n".join(
            [
                "# System Health Center Governance",
                "",
                f"- phase: {summary.get('phase')}",
                f"- governance_scope: {summary.get('governance_scope')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Contract only; no runtime, no recovery execution, no routing changes.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "governance_scope": summary.get("governance_scope"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

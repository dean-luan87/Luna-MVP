#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Hardware-Profile-Capability-Registry-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("hardware_profile_capability_registry_v1_summary.json", "summary"),
    ("hardware_profile_registry_input_intake_matrix_v1.json", "intake"),
    ("hardware_profile_schema_v1.json", "profile_schema"),
    ("camera_capability_registry_schema_v1.json", "camera_schema"),
    ("device_registry_schema_v1.json", "device_schema"),
    ("sensor_registry_schema_v1.json", "sensor_schema"),
    ("hardware_capability_status_enum_v1.json", "status_enum"),
    ("hardware_minimal_unknown_profile_v1.json", "unknown_profile"),
    ("hardware_camera_runtime_adapter_placeholder_v1.json", "adapter_placeholder"),
    ("hardware_profile_freshness_stale_policy_v1.json", "freshness_policy"),
    ("hardware_profile_registry_system_health_link_v1.json", "health_link"),
    ("hardware_profile_registry_guardedtrial_precondition_link_v1.json", "guardedtrial_link"),
    ("hardware_profile_registry_long_term_candidate_link_v1.json", "long_term"),
    ("hardware_profile_registry_decision_trace_v1.json", "trace"),
    ("hardware_profile_registry_final_decision_v1.json", "final"),
    ("hardware_profile_registry_boundary_report_v1.json", "boundary"),
    ("hardware_profile_registry_metrics_candidate_report_v1.json", "metrics"),
    ("hardware_profile_registry_benchmark_link_report_v1.json", "benchmark_link"),
    ("hardware_profile_registry_system_health_report_v1.json", "health_report"),
    ("hardware_profile_registry_no_write_boundary_report_v1.json", "no_write"),
    ("hardware_profile_registry_simulation_context_report_v1.json", "sim_report"),
    ("hardware_profile_registry_non_claims_report_v1.json", "non_claims"),
    ("hardware_profile_registry_open_followups_v1.json", "followups"),
    ("hardware_profile_registry_audit_report_v1.json", "audit"),
]


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            return parent
    return here.parents[3]


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
    ap.add_argument("--hardware-runtime-root", required=True)
    ap.add_argument("--hardware-contract-root", required=True)
    ap.add_argument("--rrd-runtime-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.hardware_profile_capability_registry_v1 import (
        run_hardware_profile_capability_registry_v1,
    )

    result = run_hardware_profile_capability_registry_v1(
        hardware_runtime_root=str(_require_abs(args.hardware_runtime_root, "hw_rt")),
        hardware_contract_root=str(_require_abs(args.hardware_contract_root, "hw_contract")),
        rrd_runtime_root=str(_require_abs(args.rrd_runtime_root, "rrd")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(WS_ROOT),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "hardware_profile_registry_notes.md").write_text(
        "# Hardware Profile Capability Registry v1\n\n"
        "Schema + minimal unknown profile + adapter placeholder; no probe/camera/fact.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"output_root": str(out), "phase_verdict_hint": result["summary"].get("phase_verdict_hint")},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

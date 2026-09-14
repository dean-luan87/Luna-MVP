#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-WorldModel-Lookup-for-Reading-Framework-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("worldmodel_lookup_for_reading_framework_v1_summary.json", "summary"),
    ("worldmodel_lookup_reading_framework_input_intake_matrix_v1.json", "intake"),
    ("worldmodel_lookup_reading_request_schema_v1.json", "request_schema"),
    ("worldmodel_lookup_reading_response_candidate_schema_v1.json", "response_schema"),
    ("worldmodel_lookup_reading_source_priority_policy_v1.json", "source_priority"),
    ("worldmodel_lookup_reading_unresolved_slot_link_policy_v1.json", "unresolved_link"),
    ("worldmodel_lookup_reading_memory_reference_link_policy_v1.json", "memory_link"),
    ("worldmodel_lookup_reading_confirmed_text_hint_link_policy_v1.json", "confirmed_text_link"),
    ("worldmodel_lookup_reading_isrc_handoff_policy_v1.json", "isrc_handoff"),
    ("worldmodel_lookup_reading_rrd_handoff_policy_v1.json", "rrd_handoff"),
    ("worldmodel_lookup_reading_fallback_policy_v1.json", "fallback"),
    ("worldmodel_lookup_reading_candidate_classification_policy_v1.json", "classification"),
    ("worldmodel_lookup_reading_no_write_boundary_policy_v1.json", "no_write_policy"),
    ("worldmodel_lookup_reading_future_dryrun_entrypoint_v1.json", "future_dryrun"),
    ("worldmodel_lookup_reading_long_term_candidate_link_v1.json", "long_term"),
    ("worldmodel_lookup_reading_framework_decision_trace_v1.json", "trace"),
    ("worldmodel_lookup_reading_framework_final_decision_v1.json", "final"),
    ("worldmodel_lookup_reading_framework_boundary_report_v1.json", "boundary"),
    ("worldmodel_lookup_reading_framework_metrics_candidate_report_v1.json", "metrics"),
    ("worldmodel_lookup_reading_framework_benchmark_link_report_v1.json", "benchmark_link"),
    ("worldmodel_lookup_reading_framework_system_health_report_v1.json", "health_report"),
    ("worldmodel_lookup_reading_framework_no_write_boundary_report_v1.json", "no_write"),
    ("worldmodel_lookup_reading_framework_simulation_context_report_v1.json", "sim_report"),
    ("worldmodel_lookup_reading_framework_non_claims_report_v1.json", "non_claims"),
    ("worldmodel_lookup_reading_framework_open_followups_v1.json", "followups"),
    ("worldmodel_lookup_reading_framework_audit_report_v1.json", "audit"),
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
    ap.add_argument("--ocr-mainline-closure-root", required=True)
    ap.add_argument("--software-closure-root", required=True)
    ap.add_argument("--tsc-reevaluation-root", required=True)
    ap.add_argument("--isrc-runtime-root", required=True)
    ap.add_argument("--rrd-runtime-root", required=True)
    ap.add_argument("--worldmodel-unresolved-slot-root", required=True)
    ap.add_argument("--memory-governance-contract-root", required=True)
    ap.add_argument("--memory-handoff-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.worldmodel_lookup_for_reading_framework_v1 import (
        run_worldmodel_lookup_for_reading_framework_v1,
    )

    result = run_worldmodel_lookup_for_reading_framework_v1(
        ocr_mainline_closure_root=str(_require_abs(args.ocr_mainline_closure_root, "ocr_closure")),
        software_closure_root=str(_require_abs(args.software_closure_root, "sw_closure")),
        tsc_reevaluation_root=str(_require_abs(args.tsc_reevaluation_root, "tsc")),
        isrc_runtime_root=str(_require_abs(args.isrc_runtime_root, "isrc")),
        rrd_runtime_root=str(_require_abs(args.rrd_runtime_root, "rrd")),
        worldmodel_unresolved_slot_root=str(_require_abs(args.worldmodel_unresolved_slot_root, "unresolved")),
        memory_governance_contract_root=str(_require_abs(args.memory_governance_contract_root, "mem_gov")),
        memory_handoff_root=str(_require_abs(args.memory_handoff_root, "mem_handoff")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "worldmodel_lookup_reading_framework_notes.md").write_text(
        "# WorldModel Lookup for Reading Framework v1\n\n"
        f"Final: `{result['final']['final_decision']}`\n"
        f"Next: `{result['final']['recommended_next_phase']}`\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_root": str(out),
                "final_decision": result["final"]["final_decision"],
                "recommended_next_phase": result["final"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

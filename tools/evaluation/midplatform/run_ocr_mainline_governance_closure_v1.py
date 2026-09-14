#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Mainline-Governance-Closure-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("ocr_mainline_governance_closure_v1_summary.json", "summary"),
    ("ocr_mainline_governance_closure_input_intake_matrix_v1.json", "intake"),
    ("ocr_mainline_governance_closure_status_matrix_v1.json", "status_matrix"),
    ("ocr_mainline_governance_regression_caveat_acceptance_v1.json", "caveat_acceptance"),
    ("ocr_mainline_runtime_ocr_closed_report_v1.json", "runtime_closed"),
    ("ocr_mainline_future_reopen_condition_matrix_v1.json", "reopen_matrix"),
    ("ocr_mainline_forbidden_continuation_matrix_v1.json", "forbidden_matrix"),
    ("ocr_mainline_memory_worldmodel_boundary_status_v1.json", "mem_wm_boundary"),
    ("ocr_mainline_next_software_mainline_handoff_v1.json", "next_handoff"),
    ("ocr_mainline_governance_closure_decision_trace_v1.json", "trace"),
    ("ocr_mainline_governance_closure_final_decision_v1.json", "final"),
    ("ocr_mainline_governance_closure_boundary_report_v1.json", "boundary"),
    ("ocr_mainline_governance_closure_metrics_candidate_report_v1.json", "metrics"),
    ("ocr_mainline_governance_closure_benchmark_link_report_v1.json", "benchmark_link"),
    ("ocr_mainline_governance_closure_system_health_report_v1.json", "health_report"),
    ("ocr_mainline_governance_closure_no_write_boundary_report_v1.json", "no_write"),
    ("ocr_mainline_governance_closure_simulation_context_report_v1.json", "sim_report"),
    ("ocr_mainline_governance_closure_non_claims_report_v1.json", "non_claims"),
    ("ocr_mainline_governance_closure_open_followups_v1.json", "followups"),
    ("ocr_mainline_governance_closure_audit_report_v1.json", "audit"),
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
    ap.add_argument("--software-closure-root", required=True)
    ap.add_argument("--regression-route-compliance-root", required=True)
    ap.add_argument("--staticreading-ocrrequest-root", required=True)
    ap.add_argument("--memory-handoff-root", required=True)
    ap.add_argument("--hardware-adapter-stub-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.ocr_mainline_governance_closure_v1 import (
        run_ocr_mainline_governance_closure_v1,
    )

    result = run_ocr_mainline_governance_closure_v1(
        software_closure_root=str(_require_abs(args.software_closure_root, "software_closure")),
        regression_route_compliance_root=str(
            _require_abs(args.regression_route_compliance_root, "regression")
        ),
        staticreading_ocrrequest_root=str(_require_abs(args.staticreading_ocrrequest_root, "ocr_gate")),
        memory_handoff_root=str(_require_abs(args.memory_handoff_root, "mem_handoff")),
        hardware_adapter_stub_root=str(_require_abs(args.hardware_adapter_stub_root, "hw_stub")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_root=str(_require_abs(args.stc_root, "stc")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "ocr_mainline_governance_closure_notes.md").write_text(
        "# OCR Mainline Governance Closure v1\n\n"
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

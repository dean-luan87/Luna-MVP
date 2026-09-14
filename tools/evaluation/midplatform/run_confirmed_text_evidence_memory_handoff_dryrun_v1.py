#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Confirmed-Text-Evidence-Memory-Handoff-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("confirmed_text_evidence_memory_handoff_dryrun_v1_summary.json", "summary"),
    ("confirmed_text_memory_handoff_input_intake_matrix_v1.json", "intake"),
    ("confirmed_text_memory_handoff_dryrun_text_evidence_sample_set_v1.json", "sample_set"),
    ("confirmed_text_evidence_candidate_collection_v1.json", "evidence_collection"),
    ("confirmed_text_memory_append_request_candidate_collection_v1.json", "append_collection"),
    ("confirmed_text_memory_permission_policy_runtime_check_v1.json", "permission_check"),
    ("confirmed_text_memory_privacy_sensitivity_runtime_check_v1.json", "privacy_check"),
    ("confirmed_text_memory_correction_supersession_conflict_runtime_check_v1.json", "csc_check"),
    ("confirmed_text_memory_expired_stale_routing_runtime_check_v1.json", "stale_check"),
    ("confirmed_text_memory_governance_handoff_candidate_collection_v1.json", "handoff_collection"),
    ("confirmed_text_worldmodel_scenedelta_link_runtime_check_v1.json", "worldmodel_check"),
    ("confirmed_text_user_emotional_context_runtime_link_v1.json", "user_emotional_link"),
    ("confirmed_text_memory_read_call_reference_runtime_check_v1.json", "read_call_check"),
    ("confirmed_text_memory_handoff_decision_trace_v1.json", "trace"),
    ("confirmed_text_memory_handoff_final_decision_v1.json", "final"),
    ("confirmed_text_memory_handoff_boundary_report_v1.json", "boundary"),
    ("confirmed_text_memory_handoff_metrics_candidate_report_v1.json", "metrics"),
    ("confirmed_text_memory_handoff_benchmark_link_report_v1.json", "benchmark_link"),
    ("confirmed_text_memory_handoff_system_health_report_v1.json", "health_report"),
    ("confirmed_text_memory_handoff_no_write_boundary_report_v1.json", "no_write"),
    ("confirmed_text_memory_handoff_simulation_context_report_v1.json", "sim_report"),
    ("confirmed_text_memory_handoff_non_claims_report_v1.json", "non_claims"),
    ("confirmed_text_memory_handoff_open_followups_v1.json", "followups"),
    ("confirmed_text_memory_handoff_audit_report_v1.json", "audit"),
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
    ap.add_argument("--memory-governance-contract-root", required=True)
    ap.add_argument("--rrd-runtime-root", required=True)
    ap.add_argument("--isrc-runtime-root", required=True)
    ap.add_argument("--tsc-reevaluation-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--worldmodel-unresolved-slot-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.confirmed_text_evidence_memory_handoff_dryrun_v1 import (
        run_confirmed_text_evidence_memory_handoff_dryrun_v1,
    )

    result = run_confirmed_text_evidence_memory_handoff_dryrun_v1(
        memory_governance_contract_root=str(_require_abs(args.memory_governance_contract_root, "contract")),
        rrd_runtime_root=str(_require_abs(args.rrd_runtime_root, "rrd")),
        isrc_runtime_root=str(_require_abs(args.isrc_runtime_root, "isrc")),
        tsc_reevaluation_root=str(_require_abs(args.tsc_reevaluation_root, "tsc")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr")),
        worldmodel_unresolved_slot_root=str(_require_abs(args.worldmodel_unresolved_slot_root, "wm")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(WS_ROOT),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "confirmed_text_memory_handoff_notes.md").write_text(
        "# Confirmed Text Evidence Memory Handoff DryRun v1\n\n"
        "Dry-run append/handoff candidates only; no Memory System invoke.\n\n"
        f"Final: `{result['final']['final_decision']}`\n",
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

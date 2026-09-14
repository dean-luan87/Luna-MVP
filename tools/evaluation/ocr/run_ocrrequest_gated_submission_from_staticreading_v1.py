#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCRRequest-Gated-Submission-from-StaticReading-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("ocrrequest_gated_submission_from_staticreading_v1_summary.json", "summary"),
    ("ocrrequest_staticreading_input_intake_matrix_v1.json", "intake"),
    ("ocrrequest_staticreading_static_capture_readiness_intake_v1.json", "capture_readiness"),
    ("ocrrequest_staticreading_readable_region_input_gate_matrix_v1.json", "region_gate_matrix"),
    ("ocrrequest_staticreading_future_payload_schema_v1.json", "future_schema"),
    ("ocrrequest_staticreading_blocked_candidate_collection_v1.json", "blocked_collection"),
    ("ocrrequest_staticreading_gate_policy_matrix_v1.json", "gate_policy_matrix"),
    ("ocrrequest_staticreading_memory_governance_link_v1.json", "memory_governance_link"),
    ("ocrrequest_staticreading_evidence_pack_v5_future_plan_v1.json", "ep_v5_plan"),
    ("ocrrequest_staticreading_semantic_sv_future_plan_v1.json", "semantic_sv_plan"),
    ("ocrrequest_staticreading_provider_bypass_audit_v1.json", "bypass_audit"),
    ("ocrrequest_staticreading_long_term_candidate_link_v1.json", "long_term"),
    ("ocrrequest_staticreading_decision_trace_v1.json", "trace"),
    ("ocrrequest_staticreading_final_decision_v1.json", "final"),
    ("ocrrequest_staticreading_boundary_report_v1.json", "boundary"),
    ("ocrrequest_staticreading_metrics_candidate_report_v1.json", "metrics"),
    ("ocrrequest_staticreading_benchmark_link_report_v1.json", "benchmark_link"),
    ("ocrrequest_staticreading_system_health_report_v1.json", "health_report"),
    ("ocrrequest_staticreading_no_write_boundary_report_v1.json", "no_write"),
    ("ocrrequest_staticreading_simulation_context_report_v1.json", "sim_report"),
    ("ocrrequest_staticreading_non_claims_report_v1.json", "non_claims"),
    ("ocrrequest_staticreading_open_followups_v1.json", "followups"),
    ("ocrrequest_staticreading_audit_report_v1.json", "audit"),
]


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "ocr_runtime").is_dir():
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
    ap.add_argument("--memory-handoff-root", required=True)
    ap.add_argument("--memory-governance-contract-root", required=True)
    ap.add_argument("--hardware-adapter-stub-root", required=True)
    ap.add_argument("--hardware-adapter-contract-root", required=True)
    ap.add_argument("--hardware-runtime-root", required=True)
    ap.add_argument("--rrd-runtime-root", required=True)
    ap.add_argument("--isrc-runtime-root", required=True)
    ap.add_argument("--tsc-reevaluation-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-sampling-guidance-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.ocr_runtime.ocrrequest_gated_submission_from_staticreading_v1 import (
        run_ocrrequest_gated_submission_from_staticreading_v1,
    )

    result = run_ocrrequest_gated_submission_from_staticreading_v1(
        memory_handoff_root=str(_require_abs(args.memory_handoff_root, "mem_handoff")),
        memory_governance_contract_root=str(_require_abs(args.memory_governance_contract_root, "mem_contract")),
        hardware_adapter_stub_root=str(_require_abs(args.hardware_adapter_stub_root, "hw_stub")),
        hardware_adapter_contract_root=str(_require_abs(args.hardware_adapter_contract_root, "hw_contract")),
        hardware_runtime_root=str(_require_abs(args.hardware_runtime_root, "hw_rt")),
        rrd_runtime_root=str(_require_abs(args.rrd_runtime_root, "rrd")),
        isrc_runtime_root=str(_require_abs(args.isrc_runtime_root, "isrc")),
        tsc_reevaluation_root=str(_require_abs(args.tsc_reevaluation_root, "tsc")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr")),
        stc_sampling_guidance_root=str(_require_abs(args.stc_sampling_guidance_root, "stc")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "ocrrequest_staticreading_notes.md").write_text(
        "# OCRRequest Gated Submission from StaticReading v1\n\n"
        f"Final: `{result['final']['final_decision']}` — no OCR until captured frame.\n",
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-OCR-Evidence-Ingest-Integration-Check-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("vision_ocr_evidence_ingest_integration_check_v1_summary.json", "summary"),
    ("vision_ocr_evidence_ingest_input_intake_matrix_v1.json", "intake"),
    ("vision_ocr_observation_request_intake_matrix_v1.json", "obs_intake"),
    ("vision_evidence_ingest_schema_v1.json", "vision_schema"),
    ("ocr_evidence_ingest_schema_v1.json", "ocr_schema"),
    ("vision_ocr_evidence_lifecycle_policy_v1.json", "lifecycle_policy"),
    ("vision_ocr_baseline_task_evidence_separation_matrix_v1.json", "separation_matrix"),
    ("vision_ocr_ingest_ocr_joint_gate_check_v1.json", "ocr_joint_gate"),
    ("vision_evidence_candidate_collection_v1.json", "vision_collection"),
    ("ocr_evidence_candidate_collection_v1.json", "ocr_collection"),
    ("vision_ocr_action_support_evidence_candidate_collection_v1.json", "action_support_collection"),
    ("vision_ocr_verification_support_evidence_candidate_collection_v1.json", "verification_collection"),
    ("vision_ocr_evidence_to_task_feedback_contract_v1.json", "feedback_contract"),
    ("vision_ocr_evidence_freshness_expiry_policy_v1.json", "freshness_policy"),
    ("vision_ocr_provider_runtime_bypass_audit_v1.json", "bypass_audit"),
    ("vision_ocr_evidence_ingest_decision_trace_v1.json", "trace"),
    ("vision_ocr_evidence_ingest_final_decision_v1.json", "final"),
    ("vision_ocr_evidence_ingest_boundary_report_v1.json", "boundary"),
    ("vision_ocr_evidence_ingest_metrics_candidate_report_v1.json", "metrics"),
    ("vision_ocr_evidence_ingest_benchmark_link_report_v1.json", "benchmark_link"),
    ("vision_ocr_evidence_ingest_system_health_report_v1.json", "health_report"),
    ("vision_ocr_evidence_ingest_no_write_boundary_report_v1.json", "no_write"),
    ("vision_ocr_evidence_ingest_simulation_context_report_v1.json", "sim_report"),
    ("vision_ocr_evidence_ingest_non_claims_report_v1.json", "non_claims"),
    ("vision_ocr_evidence_ingest_open_followups_v1.json", "followups"),
    ("vision_ocr_evidence_ingest_audit_report_v1.json", "audit"),
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
    ap.add_argument("--task-observation-request-root", required=True)
    ap.add_argument("--basic-loop-audit-root", required=True)
    ap.add_argument("--task-manager-runtime-root", required=True)
    ap.add_argument("--vision-capture-governance-root", required=True)
    ap.add_argument("--vision-capture-runtime-root", required=True)
    ap.add_argument("--ocr-mainline-closure-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--ocrrequest-staticreading-gate-root", required=True)
    ap.add_argument("--realvideo-frame-root", required=True)
    ap.add_argument("--poster-consumer-root", required=True)
    ap.add_argument("--regression-root", required=True)
    ap.add_argument("--stc-root", required=True)
    ap.add_argument("--hardware-stub-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.vision_ocr_evidence_ingest_integration_check_v1 import (
        run_vision_ocr_evidence_ingest_integration_check_v1,
    )

    result = run_vision_ocr_evidence_ingest_integration_check_v1(
        task_observation_request_root=str(_require_abs(args.task_observation_request_root, "obs_req")),
        basic_loop_audit_root=str(_require_abs(args.basic_loop_audit_root, "audit")),
        task_manager_runtime_root=str(_require_abs(args.task_manager_runtime_root, "tm_rt")),
        vision_capture_governance_root=str(_require_abs(args.vision_capture_governance_root, "vision_gov")),
        vision_capture_runtime_root=str(_require_abs(args.vision_capture_runtime_root, "vision_rt")),
        ocr_mainline_closure_root=str(_require_abs(args.ocr_mainline_closure_root, "ocr_closure")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        ocrrequest_staticreading_gate_root=str(_require_abs(args.ocrrequest_staticreading_gate_root, "ocr_req_gate")),
        realvideo_frame_root=str(_require_abs(args.realvideo_frame_root, "realvideo")),
        poster_consumer_root=str(_require_abs(args.poster_consumer_root, "poster")),
        regression_root=str(_require_abs(args.regression_root, "regression")),
        stc_root=str(_require_abs(args.stc_root, "stc")),
        hardware_stub_root=str(_require_abs(args.hardware_stub_root, "hardware")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "vision_ocr_evidence_ingest_notes.md").write_text(
        "# Vision-OCR Evidence Ingest Integration Check v1\n\n"
        f"Final: `{result['final']['final_decision']}`\n"
        f"Next: `{result['final']['recommended_next_phase']}`\n"
        f"Vision evidence: {result['final']['vision_evidence_candidate_count']}\n"
        f"OCR evidence: {result['final']['ocr_evidence_candidate_count']}\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_root": str(out),
                "final_decision": result["final"]["final_decision"],
                "vision_count": result["final"]["vision_evidence_candidate_count"],
                "ocr_count": result["final"]["ocr_evidence_candidate_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

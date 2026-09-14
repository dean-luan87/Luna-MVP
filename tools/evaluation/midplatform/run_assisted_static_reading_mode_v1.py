#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Assisted-Static-Reading-Mode-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("assisted_static_reading_mode_v1_summary.json", "summary"),
    ("assisted_static_reading_input_intake_matrix_v1.json", "intake"),
    ("assisted_static_reading_mode_entry_policy_v1.json", "entry_policy"),
    ("assisted_static_reading_state_machine_v1.json", "state_machine"),
    ("assisted_static_reading_readiness_gate_v1.json", "readiness"),
    ("assisted_static_capture_quality_requirement_v1.json", "quality"),
    ("assisted_static_reading_user_guidance_sequence_v1.json", "guidance_seq"),
    ("assisted_static_reading_system_self_adjustment_policy_v1.json", "self_adj"),
    ("assisted_static_reading_ocrrequest_future_gate_v1.json", "ocr_gate"),
    ("assisted_static_reading_result_pipeline_plan_v1.json", "pipeline"),
    ("assisted_static_reading_exit_fallback_escalation_policy_v1.json", "exit_pol"),
    ("assisted_static_reading_expired_candidate_policy_v1.json", "expired"),
    ("assisted_static_reading_current_case_decision_v1.json", "current"),
    ("assisted_static_reading_ocr_activation_link_report_v1.json", "ocr_link"),
    ("assisted_static_reading_voice_guidance_link_report_v1.json", "voice_link"),
    ("assisted_static_reading_vision_capture_link_report_v1.json", "vc_link"),
    ("assisted_static_reading_boundary_report_v1.json", "boundary"),
    ("assisted_static_reading_metrics_candidate_report_v1.json", "metrics"),
    ("assisted_static_reading_benchmark_link_report_v1.json", "benchmark_link"),
    ("assisted_static_reading_system_health_link_report_v1.json", "health_link"),
    ("assisted_static_reading_no_write_boundary_report_v1.json", "no_write"),
    ("assisted_static_reading_simulation_context_report_v1.json", "sim_report"),
    ("assisted_static_reading_non_claims_report_v1.json", "non_claims"),
    ("assisted_static_reading_open_followups_v1.json", "followups"),
    ("assisted_static_reading_audit_report_v1.json", "audit"),
]


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if (parent / "_eval_out").is_dir():
                return parent
            sibling = parent.parent / "Luna-Workspace-Min"
            if (sibling / "_eval_out").is_dir():
                return sibling
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
    ap.add_argument("--voice-output-plane-adapter-root", required=True)
    ap.add_argument("--voice-guidance-runtime-root", required=True)
    ap.add_argument("--user-guidance-runtime-root", required=True)
    ap.add_argument("--vision-capture-runtime-root", required=True)
    ap.add_argument("--vision-capture-governance-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-sampling-guidance-root", required=True)
    ap.add_argument("--user-guidance-policy-root", required=True)
    ap.add_argument("--ocr-v2-root", required=True)
    ap.add_argument("--multiframe-crop-v2-root", required=True)
    ap.add_argument("--crop-quality-root", required=True)
    ap.add_argument("--evidence-pack-v4-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.assisted_static_reading_mode_v1 import run_assisted_static_reading_mode_v1

    result = run_assisted_static_reading_mode_v1(
        voice_output_plane_adapter_root=str(_require_abs(args.voice_output_plane_adapter_root, "vop")),
        voice_guidance_runtime_root=str(_require_abs(args.voice_guidance_runtime_root, "vg")),
        user_guidance_runtime_root=str(_require_abs(args.user_guidance_runtime_root, "ug")),
        vision_capture_runtime_root=str(_require_abs(args.vision_capture_runtime_root, "vc")),
        vision_capture_governance_root=str(_require_abs(args.vision_capture_governance_root, "vc_gov")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_sampling_guidance_root=str(_require_abs(args.stc_sampling_guidance_root, "stc")),
        user_guidance_policy_root=str(_require_abs(args.user_guidance_policy_root, "ug_pol")),
        ocr_v2_root=str(_require_abs(args.ocr_v2_root, "ocr_v2")),
        multiframe_crop_v2_root=str(_require_abs(args.multiframe_crop_v2_root, "crop_v2")),
        crop_quality_root=str(_require_abs(args.crop_quality_root, "cq")),
        evidence_pack_v4_root=str(_require_abs(args.evidence_pack_v4_root, "ep4")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "assisted_static_reading_notes.md").write_text(
        "# Assisted Static Reading Mode v1\n\nPolicy-only: mode, FSM, readiness, OCRRequest future gate. No capture/OCR/TTS.\n",
        encoding="utf-8",
    )
    print(json.dumps({"output_root": str(out), "phase_verdict_hint": result["summary"].get("phase_verdict_hint")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

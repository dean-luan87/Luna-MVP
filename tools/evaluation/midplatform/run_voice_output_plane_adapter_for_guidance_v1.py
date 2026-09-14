#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Voice-Output-Plane-Adapter-for-Guidance-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("voice_output_plane_adapter_for_guidance_v1_summary.json", "summary"),
    ("voice_output_plane_adapter_input_intake_matrix_v1.json", "intake"),
    ("voice_output_plane_adapter_mapping_contract_v1.json", "mapping"),
    ("voice_output_plane_adapter_payload_candidate_v1.json", "adapter_payload"),
    ("voice_output_plane_speech_request_payload_candidate_v1.json", "speech_payload"),
    ("voice_output_plane_speech_gate_admission_dryrun_v1.json", "admission"),
    ("voice_output_plane_submit_dryrun_v1.json", "vop_submit"),
    ("voice_output_plane_guidance_safety_interruptibility_matrix_v1.json", "safety_matrix"),
    ("voice_output_plane_stm_repeat_reference_preservation_report_v1.json", "stm_repeat"),
    ("voice_output_plane_adapter_final_dryrun_decision_v1.json", "final"),
    ("voice_output_plane_adapter_boundary_report_v1.json", "boundary"),
    ("voice_output_plane_adapter_metrics_candidate_report_v1.json", "metrics"),
    ("voice_output_plane_adapter_benchmark_link_report_v1.json", "benchmark_link"),
    ("voice_output_plane_adapter_system_health_link_report_v1.json", "health_link"),
    ("voice_output_plane_adapter_no_write_boundary_report_v1.json", "no_write"),
    ("voice_output_plane_adapter_simulation_context_report_v1.json", "sim_report"),
    ("voice_output_plane_adapter_non_claims_report_v1.json", "non_claims"),
    ("voice_output_plane_adapter_open_followups_v1.json", "followups"),
    ("voice_output_plane_adapter_audit_report_v1.json", "audit"),
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
    ap.add_argument("--voice-guidance-runtime-root", required=True)
    ap.add_argument("--voice-guidance-template-root", required=True)
    ap.add_argument("--user-guidance-runtime-root", required=True)
    ap.add_argument("--vision-capture-runtime-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    roots = {
        "voice_guidance_runtime_root": _require_abs(args.voice_guidance_runtime_root, "vg_runtime"),
        "voice_guidance_template_root": _require_abs(args.voice_guidance_template_root, "vg_template"),
        "user_guidance_runtime_root": _require_abs(args.user_guidance_runtime_root, "ug_rt"),
        "vision_capture_runtime_root": _require_abs(args.vision_capture_runtime_root, "vc_rt"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.voice_output_plane_adapter_for_guidance_v1 import (
        run_voice_output_plane_adapter_for_guidance_v1,
    )

    result = run_voice_output_plane_adapter_for_guidance_v1(
        voice_guidance_runtime_root=str(roots["voice_guidance_runtime_root"]),
        voice_guidance_template_root=str(roots["voice_guidance_template_root"]),
        user_guidance_runtime_root=str(roots["user_guidance_runtime_root"]),
        vision_capture_runtime_root=str(roots["vision_capture_runtime_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
        workspace_root=str(WS_ROOT),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    notes = """# Voice Output Plane Adapter for Guidance v1 — Notes

Adapter dry-run only: mapping → payload candidates → Speech Gate admission → VOP submit deferred.

No VOP invoke, no SpeechRequest submit, no TTS, no STM write.
"""
    (out / "voice_output_plane_adapter_notes.md").write_text(notes, encoding="utf-8")

    print(
        json.dumps(
            {"output_root": str(out), "phase_verdict_hint": result["summary"].get("phase_verdict_hint")},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

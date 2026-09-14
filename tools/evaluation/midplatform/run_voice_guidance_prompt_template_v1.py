#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Voice-Guidance-Prompt-Template-v1-001 runner (midplatform path; future: tools/evaluation/voice/)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("voice_guidance_prompt_template_v1_summary.json", "summary"),
    ("voice_guidance_trigger_governance_integration_report_v1.json", "integration"),
    ("voice_guidance_speech_priority_policy_v1.json", "priority"),
    ("voice_guidance_prompt_template_matrix_v1.json", "templates"),
    ("voice_guidance_prompt_safety_constraint_matrix_v1.json", "safety"),
    ("voice_guidance_short_term_memory_mount_contract_v1.json", "stm"),
    ("voice_guidance_repeat_on_user_inquiry_policy_v1.json", "repeat_policy"),
    ("voice_guidance_cooldown_repetition_policy_v1.json", "cooldown"),
    ("voice_guidance_prompt_candidate_selection_policy_v1.json", "selection"),
    ("voice_guidance_voice_output_plane_adapter_placeholder_v1.json", "adapter"),
    ("voice_guidance_prompt_runtime_state_placeholder_v1.json", "state_placeholder"),
    ("voice_guidance_current_case_prompt_dryrun_v1.json", "current_case"),
    ("voice_guidance_prompt_template_boundary_report_v1.json", "boundary"),
    ("voice_guidance_prompt_template_metrics_candidate_report_v1.json", "metrics"),
    ("voice_guidance_prompt_template_benchmark_link_report_v1.json", "benchmark_link"),
    ("voice_guidance_prompt_template_system_health_link_report_v1.json", "health_link"),
    ("voice_guidance_prompt_template_no_write_boundary_report_v1.json", "no_write"),
    ("voice_guidance_prompt_template_simulation_context_report_v1.json", "sim_report"),
    ("voice_guidance_prompt_template_non_claims_report_v1.json", "non_claims"),
    ("voice_guidance_prompt_template_open_followups_v1.json", "followups"),
    ("voice_guidance_prompt_template_audit_report_v1.json", "audit"),
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
    ap.add_argument("--user-guidance-runtime-root", required=True)
    ap.add_argument("--vision-capture-runtime-root", required=True)
    ap.add_argument("--user-guidance-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-sampling-guidance-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    roots = {
        "user_guidance_runtime_root": _require_abs(args.user_guidance_runtime_root, "ug_rt"),
        "vision_capture_runtime_root": _require_abs(args.vision_capture_runtime_root, "vc_rt"),
        "user_guidance_root": _require_abs(args.user_guidance_root, "ug"),
        "ocr_activation_root": _require_abs(args.ocr_activation_root, "ocr_act"),
        "stc_sampling_guidance_root": _require_abs(args.stc_sampling_guidance_root, "stc"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.voice_guidance_prompt_template_v1 import (
        run_voice_guidance_prompt_template_v1,
    )

    result = run_voice_guidance_prompt_template_v1(
        user_guidance_runtime_root=str(roots["user_guidance_runtime_root"]),
        vision_capture_runtime_root=str(roots["vision_capture_runtime_root"]),
        user_guidance_root=str(roots["user_guidance_root"]),
        ocr_activation_root=str(roots["ocr_activation_root"]),
        stc_sampling_guidance_root=str(roots["stc_sampling_guidance_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
        workspace_root=str(WS_ROOT),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    notes = """# Voice Guidance Prompt Template v1 — Notes

- Template-only phase; no TTS / VOP / SpeechRequest.
- OCR guidance = P3; safety P0 always above.
- Capability: `capabilities/midplatform/` (future `capabilities/voice/`).
- Runner: `tools/evaluation/midplatform/` (future `tools/evaluation/voice/`).
"""
    (out / "voice_guidance_prompt_template_notes.md").write_text(notes, encoding="utf-8")

    print(json.dumps({"output_root": str(out), "phase_verdict_hint": result["summary"].get("phase_verdict_hint")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

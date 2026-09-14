#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-User-Clarification-Prompt-Template-for-Reading-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("user_clarification_prompt_template_for_reading_v1_summary.json", "summary"),
    ("user_clarification_prompt_template_input_intake_matrix_v1.json", "intake"),
    ("user_clarification_prompt_template_matrix_v1.json", "matrix"),
    ("user_clarification_expected_response_schema_v1.json", "response_schema"),
    ("user_clarification_response_to_context_fill_policy_v1.json", "fill_policy"),
    ("user_clarification_prompt_priority_safety_policy_v1.json", "priority_safety"),
    ("user_clarification_prompt_cooldown_repeat_policy_v1.json", "cooldown"),
    ("user_clarification_handoff_to_task_scene_runtime_policy_v1.json", "handoff"),
    ("user_clarification_current_case_template_dryrun_v1.json", "current"),
    ("user_clarification_long_term_candidate_link_v1.json", "long_term"),
    ("user_clarification_prompt_template_boundary_report_v1.json", "boundary"),
    ("user_clarification_prompt_template_metrics_candidate_report_v1.json", "metrics"),
    ("user_clarification_prompt_template_benchmark_link_report_v1.json", "benchmark_link"),
    ("user_clarification_prompt_template_system_health_link_report_v1.json", "health_link"),
    ("user_clarification_prompt_template_no_write_boundary_report_v1.json", "no_write"),
    ("user_clarification_prompt_template_simulation_context_report_v1.json", "sim_report"),
    ("user_clarification_prompt_template_non_claims_report_v1.json", "non_claims"),
    ("user_clarification_prompt_template_open_followups_v1.json", "followups"),
    ("user_clarification_prompt_template_audit_report_v1.json", "audit"),
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
    ap.add_argument("--task-scene-runtime-root", required=True)
    ap.add_argument("--task-scene-policy-root", required=True)
    ap.add_argument("--voice-guidance-template-root", required=True)
    ap.add_argument("--voice-guidance-runtime-root", required=True)
    ap.add_argument("--voice-output-plane-adapter-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.user_clarification_prompt_template_for_reading_v1 import (
        run_user_clarification_prompt_template_for_reading_v1,
    )

    result = run_user_clarification_prompt_template_for_reading_v1(
        task_scene_runtime_root=str(_require_abs(args.task_scene_runtime_root, "tsc_rt")),
        task_scene_policy_root=str(_require_abs(args.task_scene_policy_root, "tsc")),
        voice_guidance_template_root=str(_require_abs(args.voice_guidance_template_root, "vg_tpl")),
        voice_guidance_runtime_root=str(_require_abs(args.voice_guidance_runtime_root, "vg_rt")),
        voice_output_plane_adapter_root=str(_require_abs(args.voice_output_plane_adapter_root, "vop")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(WS_ROOT),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "user_clarification_prompt_template_notes.md").write_text(
        "# User Clarification Prompt Template for Reading v1\n\n"
        "Templates only — P0/P1 above clarification; no TTS/VOP/STM in this phase.\n",
        encoding="utf-8",
    )
    print(json.dumps({"output_root": str(out), "phase_verdict_hint": result["summary"].get("phase_verdict_hint")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

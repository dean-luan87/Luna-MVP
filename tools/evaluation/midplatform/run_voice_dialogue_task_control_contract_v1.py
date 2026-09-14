#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Voice-Dialogue-Task-Control-Contract-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("voice_dialogue_task_control_contract_v1_summary.json", "summary"),
    ("voice_dialogue_task_control_input_intake_matrix_v1.json", "intake"),
    ("voice_dialogue_intent_candidate_schema_v1.json", "intent_schema"),
    ("voice_dialogue_task_control_command_candidate_schema_v1.json", "command_schema"),
    ("voice_dialogue_to_task_handoff_policy_v1.json", "handoff_policy"),
    ("voice_dialogue_short_term_context_policy_v1.json", "short_term_context"),
    ("voice_dialogue_repeat_pause_resume_cancel_policy_v1.json", "repeat_pause_resume_cancel"),
    ("voice_dialogue_query_status_policy_v1.json", "query_status"),
    ("voice_dialogue_task_clarification_policy_v1.json", "task_clarification"),
    ("voice_dialogue_safety_priority_suppression_policy_v1.json", "safety_priority"),
    ("voice_dialogue_speech_gate_vop_output_policy_v1.json", "speech_gate_vop"),
    ("voice_dialogue_minimal_template_matrix_v1.json", "template_matrix"),
    ("voice_dialogue_state_machine_contract_v1.json", "state_machine"),
    ("voice_dialogue_task_control_future_runtime_dryrun_entrypoint_v1.json", "future_dryrun"),
    ("voice_dialogue_midplatform_task_manager_boundary_v1.json", "midplatform_boundary"),
    ("voice_dialogue_navigation_guidance_link_policy_v1.json", "nav_link"),
    ("voice_dialogue_task_control_decision_trace_v1.json", "trace"),
    ("voice_dialogue_task_control_final_decision_v1.json", "final"),
    ("voice_dialogue_task_control_boundary_report_v1.json", "boundary"),
    ("voice_dialogue_task_control_metrics_candidate_report_v1.json", "metrics"),
    ("voice_dialogue_task_control_benchmark_link_report_v1.json", "benchmark_link"),
    ("voice_dialogue_task_control_system_health_report_v1.json", "health_report"),
    ("voice_dialogue_task_control_no_write_boundary_report_v1.json", "no_write"),
    ("voice_dialogue_task_control_simulation_context_report_v1.json", "sim_report"),
    ("voice_dialogue_task_control_non_claims_report_v1.json", "non_claims"),
    ("voice_dialogue_task_control_open_followups_v1.json", "followups"),
    ("voice_dialogue_task_control_audit_report_v1.json", "audit"),
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
    ap.add_argument("--basic-loop-plan-root", required=True)
    ap.add_argument("--voice-guidance-runtime-root", required=True)
    ap.add_argument("--vop-adapter-root", required=True)
    ap.add_argument("--user-clarification-runtime-root", required=True)
    ap.add_argument("--user-clarification-parsing-root", required=True)
    ap.add_argument("--task-scene-runtime-root", required=True)
    ap.add_argument("--task-scene-reevaluation-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.voice_dialogue_task_control_contract_v1 import (
        run_voice_dialogue_task_control_contract_v1,
    )

    result = run_voice_dialogue_task_control_contract_v1(
        basic_loop_plan_root=str(_require_abs(args.basic_loop_plan_root, "loop_plan")),
        voice_guidance_runtime_root=str(_require_abs(args.voice_guidance_runtime_root, "voice_guidance")),
        vop_adapter_root=str(_require_abs(args.vop_adapter_root, "vop")),
        user_clarification_runtime_root=str(_require_abs(args.user_clarification_runtime_root, "user_clarify")),
        user_clarification_parsing_root=str(_require_abs(args.user_clarification_parsing_root, "user_parse")),
        task_scene_runtime_root=str(_require_abs(args.task_scene_runtime_root, "task_scene")),
        task_scene_reevaluation_root=str(_require_abs(args.task_scene_reevaluation_root, "task_reeval")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_root=str(_require_abs(args.stc_root, "stc")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "voice_dialogue_task_control_notes.md").write_text(
        "# Voice Dialogue Task Control Contract v1\n\n"
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

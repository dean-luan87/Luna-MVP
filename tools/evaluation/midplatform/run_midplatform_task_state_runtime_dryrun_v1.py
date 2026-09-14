#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-MidPlatform-Task-State-Runtime-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("midplatform_task_state_runtime_dryrun_v1_summary.json", "summary"),
    ("midplatform_task_state_runtime_input_intake_matrix_v1.json", "intake"),
    ("midplatform_task_state_handoff_intake_matrix_v1.json", "handoff_intake"),
    ("midplatform_task_state_candidate_schema_v1.json", "state_schema"),
    ("midplatform_task_state_transition_guard_matrix_v1.json", "guard_matrix"),
    ("midplatform_task_state_candidate_collection_v1.json", "state_collection"),
    ("midplatform_task_lifecycle_candidate_collection_v1.json", "lifecycle_collection"),
    ("midplatform_task_guidance_need_candidate_collection_v1.json", "guidance_collection"),
    ("midplatform_task_observation_requirement_candidate_collection_v1.json", "observation_collection"),
    ("midplatform_task_speech_response_candidate_collection_v1.json", "speech_collection"),
    ("midplatform_task_confirmation_context_candidate_collection_v1.json", "confirmation_collection"),
    ("midplatform_task_state_safety_gate_dryrun_v1.json", "safety_dryrun"),
    ("midplatform_task_blocking_reason_matrix_v1.json", "blocking_matrix"),
    ("midplatform_task_state_boundary_check_v1.json", "boundary_check"),
    ("midplatform_task_state_navigation_guidance_link_check_v1.json", "nav_link_check"),
    ("midplatform_task_state_dialogue_feedback_link_check_v1.json", "dialogue_feedback_check"),
    ("midplatform_task_state_runtime_decision_trace_v1.json", "trace"),
    ("midplatform_task_state_runtime_final_decision_v1.json", "final"),
    ("midplatform_task_state_runtime_boundary_report_v1.json", "boundary"),
    ("midplatform_task_state_runtime_metrics_candidate_report_v1.json", "metrics"),
    ("midplatform_task_state_runtime_benchmark_link_report_v1.json", "benchmark_link"),
    ("midplatform_task_state_runtime_system_health_report_v1.json", "health_report"),
    ("midplatform_task_state_runtime_no_write_boundary_report_v1.json", "no_write"),
    ("midplatform_task_state_runtime_simulation_context_report_v1.json", "sim_report"),
    ("midplatform_task_state_runtime_non_claims_report_v1.json", "non_claims"),
    ("midplatform_task_state_runtime_open_followups_v1.json", "followups"),
    ("midplatform_task_state_runtime_audit_report_v1.json", "audit"),
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
    ap.add_argument("--voice-dialogue-runtime-root", required=True)
    ap.add_argument("--voice-dialogue-contract-root", required=True)
    ap.add_argument("--basic-loop-plan-root", required=True)
    ap.add_argument("--task-scene-runtime-root", required=True)
    ap.add_argument("--task-scene-reevaluation-root", required=True)
    ap.add_argument("--user-clarification-runtime-root", required=True)
    ap.add_argument("--user-clarification-parsing-root", required=True)
    ap.add_argument("--voice-guidance-runtime-root", required=True)
    ap.add_argument("--vop-adapter-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.midplatform_task_state_runtime_dryrun_v1 import (
        run_midplatform_task_state_runtime_dryrun_v1,
    )

    result = run_midplatform_task_state_runtime_dryrun_v1(
        voice_dialogue_runtime_root=str(_require_abs(args.voice_dialogue_runtime_root, "voice_rt")),
        voice_dialogue_contract_root=str(_require_abs(args.voice_dialogue_contract_root, "contract")),
        basic_loop_plan_root=str(_require_abs(args.basic_loop_plan_root, "loop_plan")),
        task_scene_runtime_root=str(_require_abs(args.task_scene_runtime_root, "task_scene")),
        task_scene_reevaluation_root=str(_require_abs(args.task_scene_reevaluation_root, "task_reeval")),
        user_clarification_runtime_root=str(_require_abs(args.user_clarification_runtime_root, "user_clarify")),
        user_clarification_parsing_root=str(_require_abs(args.user_clarification_parsing_root, "user_parse")),
        voice_guidance_runtime_root=str(_require_abs(args.voice_guidance_runtime_root, "voice_guidance")),
        vop_adapter_root=str(_require_abs(args.vop_adapter_root, "vop")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_root=str(_require_abs(args.stc_root, "stc")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "midplatform_task_state_runtime_notes.md").write_text(
        "# MidPlatform Task State Runtime DryRun v1\n\n"
        f"Final: `{result['final']['final_decision']}`\n"
        f"Next: `{result['final']['recommended_next_phase']}`\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_root": str(out),
                "final_decision": result["final"]["final_decision"],
                "handoff_count": result["final"]["handoff_candidate_count_observed"],
                "task_state_candidate_count": result["final"]["task_state_candidate_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

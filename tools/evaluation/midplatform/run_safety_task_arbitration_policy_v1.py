#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Safety-Task-Arbitration-Policy-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("safety_task_arbitration_policy_v1_summary.json", "summary"),
    ("safety_task_arbitration_input_intake_matrix_v1.json", "intake"),
    ("safety_task_arbitration_source_matrix_v1.json", "source_matrix"),
    ("safety_task_arbitration_schema_v1.json", "schema"),
    ("safety_task_priority_policy_v1.json", "priority_policy"),
    ("safety_task_suppression_policy_v1.json", "suppression_policy"),
    ("safety_task_delay_policy_v1.json", "delay_policy"),
    ("safety_task_interrupt_policy_v1.json", "interrupt_policy"),
    ("safety_task_speech_arbitration_handoff_policy_v1.json", "speech_handoff"),
    ("safety_task_commit_arbitration_policy_v1.json", "commit_policy"),
    ("safety_task_ocr_guidance_arbitration_policy_v1.json", "ocr_policy"),
    ("safety_task_human_assistance_arbitration_policy_v1.json", "human_policy"),
    ("safety_task_arbitration_candidate_collection_v1.json", "arb_collection"),
    ("safety_task_safety_active_scenario_matrix_v1.json", "scenario_matrix"),
    ("safety_task_arbitration_feedback_contract_v1.json", "feedback"),
    ("safety_task_arbitration_decision_trace_v1.json", "trace"),
    ("safety_task_arbitration_final_decision_v1.json", "final"),
    ("safety_task_arbitration_boundary_report_v1.json", "boundary"),
    ("safety_task_arbitration_metrics_candidate_report_v1.json", "metrics"),
    ("safety_task_arbitration_benchmark_link_report_v1.json", "benchmark_link"),
    ("safety_task_arbitration_system_health_report_v1.json", "health_report"),
    ("safety_task_arbitration_no_write_boundary_report_v1.json", "no_write"),
    ("safety_task_arbitration_simulation_context_report_v1.json", "sim_report"),
    ("safety_task_arbitration_non_claims_report_v1.json", "non_claims"),
    ("safety_task_arbitration_open_followups_v1.json", "followups"),
    ("safety_task_arbitration_audit_report_v1.json", "audit"),
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
    ap.add_argument("--basic-navigation-loop-root", required=True)
    ap.add_argument("--navigation-guidance-speech-adapter-root", required=True)
    ap.add_argument("--task-manager-runtime-root", required=True)
    ap.add_argument("--midplatform-task-state-root", required=True)
    ap.add_argument("--voice-dialogue-runtime-root", required=True)
    ap.add_argument("--vop-adapter-root", required=True)
    ap.add_argument("--voice-guidance-runtime-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.safety_task_arbitration_policy_v1 import run_safety_task_arbitration_policy_v1

    result = run_safety_task_arbitration_policy_v1(
        basic_navigation_loop_root=str(_require_abs(args.basic_navigation_loop_root, "nav_loop")),
        navigation_guidance_speech_adapter_root=str(
            _require_abs(args.navigation_guidance_speech_adapter_root, "speech_adapter")
        ),
        task_manager_runtime_root=str(_require_abs(args.task_manager_runtime_root, "tm_rt")),
        midplatform_task_state_root=str(_require_abs(args.midplatform_task_state_root, "mp_ts")),
        voice_dialogue_runtime_root=str(_require_abs(args.voice_dialogue_runtime_root, "voice_dialogue")),
        vop_adapter_root=str(_require_abs(args.vop_adapter_root, "vop")),
        voice_guidance_runtime_root=str(_require_abs(args.voice_guidance_runtime_root, "voice_guidance")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_root=str(_require_abs(args.stc_root, "stc")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "safety_task_arbitration_notes.md").write_text(
        "# Safety Task Arbitration Policy v1\n\n"
        f"Final: `{result['final']['final_decision']}`\n"
        f"Next: `{result['final']['recommended_next_phase']}`\n"
        f"Arbitration candidates: {result['final']['arbitration_candidate_count']}\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_root": str(out),
                "final_decision": result["final"]["final_decision"],
                "arbitration_count": result["final"]["arbitration_candidate_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

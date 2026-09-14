#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Task-Manager-Runtime-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("task_manager_runtime_dryrun_v1_summary.json", "summary"),
    ("task_manager_runtime_input_intake_matrix_v1.json", "intake"),
    ("task_manager_runtime_candidate_intake_matrix_v1.json", "candidate_intake"),
    ("task_manager_runtime_task_object_candidate_collection_v1.json", "task_objects"),
    ("task_manager_runtime_lifecycle_event_candidate_collection_v1.json", "lifecycle_events"),
    ("task_manager_runtime_commit_decision_candidate_collection_v1.json", "commit_decisions"),
    ("task_manager_runtime_state_machine_application_matrix_v1.json", "fsm_matrix"),
    ("task_manager_runtime_transition_guard_application_matrix_v1.json", "guard_matrix"),
    ("task_manager_runtime_confirmation_gate_application_matrix_v1.json", "confirm_matrix"),
    ("task_manager_runtime_safety_gate_application_matrix_v1.json", "safety_matrix"),
    ("task_manager_runtime_idempotency_duplicate_dryrun_v1.json", "idempotency_dryrun"),
    ("task_manager_runtime_context_enrichment_candidate_collection_v1.json", "enrichment_collection"),
    ("task_manager_runtime_verification_context_candidate_collection_v1.json", "verification_collection"),
    ("task_manager_runtime_execution_support_context_candidate_collection_v1.json", "execution_collection"),
    ("task_manager_runtime_downstream_candidate_collection_v1.json", "downstream_collection"),
    ("task_manager_runtime_task_spatial_relation_candidate_v1.json", "spatial_relations"),
    ("task_manager_runtime_information_gap_analysis_v1.json", "information_gaps"),
    ("task_manager_runtime_task_aware_observation_plan_v1.json", "observation_plans"),
    ("task_manager_runtime_ocr_activation_need_candidate_v1.json", "ocr_needs"),
    ("task_manager_runtime_human_assistance_need_candidate_v1.json", "human_needs"),
    ("task_manager_runtime_action_schedule_candidate_v1.json", "action_schedules"),
    ("task_manager_runtime_action_scheduling_policy_v1.json", "scheduling_policy"),
    ("task_manager_runtime_rollback_abort_dryrun_v1.json", "rollback_abort"),
    ("task_manager_runtime_audit_trace_collection_v1.json", "audit_collection"),
    ("task_manager_runtime_boundary_check_v1.json", "boundary_check"),
    ("task_manager_runtime_decision_trace_v1.json", "trace"),
    ("task_manager_runtime_final_decision_v1.json", "final"),
    ("task_manager_runtime_boundary_report_v1.json", "boundary"),
    ("task_manager_runtime_metrics_candidate_report_v1.json", "metrics"),
    ("task_manager_runtime_benchmark_link_report_v1.json", "benchmark_link"),
    ("task_manager_runtime_system_health_report_v1.json", "health_report"),
    ("task_manager_runtime_no_write_boundary_report_v1.json", "no_write"),
    ("task_manager_runtime_simulation_context_report_v1.json", "sim_report"),
    ("task_manager_runtime_non_claims_report_v1.json", "non_claims"),
    ("task_manager_runtime_open_followups_v1.json", "followups"),
    ("task_manager_runtime_audit_report_v1.json", "audit"),
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
    ap.add_argument("--task-manager-contract-root", required=True)
    ap.add_argument("--midplatform-task-state-root", required=True)
    ap.add_argument("--voice-dialogue-runtime-root", required=True)
    ap.add_argument("--basic-loop-plan-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.task_manager_runtime_dryrun_v1 import (
        run_task_manager_runtime_dryrun_v1,
    )

    result = run_task_manager_runtime_dryrun_v1(
        task_manager_contract_root=str(_require_abs(args.task_manager_contract_root, "contract")),
        midplatform_task_state_root=str(_require_abs(args.midplatform_task_state_root, "mp_state")),
        voice_dialogue_runtime_root=str(_require_abs(args.voice_dialogue_runtime_root, "voice_rt")),
        basic_loop_plan_root=str(_require_abs(args.basic_loop_plan_root, "loop_plan")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_root=str(_require_abs(args.stc_root, "stc")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "task_manager_runtime_notes.md").write_text(
        "# Task Manager Runtime DryRun v1\n\n"
        f"Final: `{result['final']['final_decision']}`\n"
        f"Next: `{result['final']['recommended_next_phase']}`\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_root": str(out),
                "final_decision": result["final"]["final_decision"],
                "task_state_count": result["summary"]["task_state_candidate_count_observed"],
                "enrichment_count": result["metrics"]["enrichment_candidate_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

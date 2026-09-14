#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Task-Manager-Contract-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("task_manager_contract_v1_summary.json", "summary"),
    ("task_manager_contract_input_intake_matrix_v1.json", "intake"),
    ("task_manager_task_object_schema_v1.json", "task_schema"),
    ("task_manager_lifecycle_event_schema_v1.json", "lifecycle_schema"),
    ("task_manager_commit_decision_schema_v1.json", "commit_schema"),
    ("task_manager_state_machine_contract_v1.json", "state_machine"),
    ("task_manager_transition_guard_policy_v1.json", "transition_guard"),
    ("task_manager_confirmation_gate_policy_v1.json", "confirmation_gate"),
    ("task_manager_safety_gate_policy_v1.json", "safety_gate"),
    ("task_manager_idempotency_duplicate_policy_v1.json", "idempotency"),
    ("task_manager_rollback_abort_policy_v1.json", "rollback_abort"),
    ("task_manager_external_boundary_policy_v1.json", "external_boundary"),
    ("task_manager_runtime_disabled_policy_v1.json", "runtime_disabled"),
    ("task_manager_future_runtime_dryrun_entrypoint_v1.json", "future_dryrun"),
    ("task_manager_audit_trace_policy_v1.json", "audit_trace"),
    ("task_manager_midplatform_integration_contract_v1.json", "midplatform_integration"),
    ("task_manager_task_context_enrichment_schema_v1.json", "context_enrichment_schema"),
    ("task_manager_context_enrichment_source_policy_v1.json", "enrichment_source_policy"),
    ("task_manager_task_verification_context_policy_v1.json", "verification_context_policy"),
    ("task_manager_execution_support_context_policy_v1.json", "execution_support_policy"),
    ("task_manager_contract_decision_trace_v1.json", "trace"),
    ("task_manager_contract_final_decision_v1.json", "final"),
    ("task_manager_contract_boundary_report_v1.json", "boundary"),
    ("task_manager_contract_metrics_candidate_report_v1.json", "metrics"),
    ("task_manager_contract_benchmark_link_report_v1.json", "benchmark_link"),
    ("task_manager_contract_system_health_report_v1.json", "health_report"),
    ("task_manager_contract_no_write_boundary_report_v1.json", "no_write"),
    ("task_manager_contract_simulation_context_report_v1.json", "sim_report"),
    ("task_manager_contract_non_claims_report_v1.json", "non_claims"),
    ("task_manager_contract_open_followups_v1.json", "followups"),
    ("task_manager_contract_audit_report_v1.json", "audit"),
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
    ap.add_argument("--midplatform-task-state-root", required=True)
    ap.add_argument("--voice-dialogue-runtime-root", required=True)
    ap.add_argument("--basic-loop-plan-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--voice-dialogue-contract-root", default=None)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.task_manager_contract_v1 import run_task_manager_contract_v1

    result = run_task_manager_contract_v1(
        midplatform_task_state_root=str(_require_abs(args.midplatform_task_state_root, "mp_state")),
        voice_dialogue_runtime_root=str(_require_abs(args.voice_dialogue_runtime_root, "voice_rt")),
        basic_loop_plan_root=str(_require_abs(args.basic_loop_plan_root, "loop_plan")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_root=str(_require_abs(args.stc_root, "stc")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        voice_dialogue_contract_root=args.voice_dialogue_contract_root,
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "task_manager_contract_notes.md").write_text(
        "# Task Manager Contract v1\n\n"
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

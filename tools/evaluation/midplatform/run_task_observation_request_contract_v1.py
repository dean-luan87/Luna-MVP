#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Task-Observation-Request-Contract-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("task_observation_request_contract_v1_summary.json", "summary"),
    ("task_observation_request_input_intake_matrix_v1.json", "intake"),
    ("task_observation_request_schema_v1.json", "schema"),
    ("task_observation_request_source_policy_v1.json", "source_policy"),
    ("task_observation_baseline_safety_request_policy_v1.json", "baseline_policy"),
    ("task_observation_task_driven_request_policy_v1.json", "task_driven_policy"),
    ("task_observation_target_module_routing_policy_v1.json", "routing_policy"),
    ("task_observation_request_gate_policy_v1.json", "gate_policy"),
    ("task_observation_priority_timing_freshness_policy_v1.json", "ptf_policy"),
    ("task_observation_request_candidate_collection_v1.json", "candidates"),
    ("task_observation_ocr_request_subpolicy_v1.json", "ocr_subpolicy"),
    ("task_observation_user_guidance_request_subpolicy_v1.json", "guidance_subpolicy"),
    ("task_observation_human_assistance_request_subpolicy_v1.json", "human_subpolicy"),
    ("task_observation_vision_ocr_ingest_handoff_contract_v1.json", "handoff"),
    ("task_observation_request_lifecycle_policy_v1.json", "lifecycle_policy"),
    ("task_observation_safety_task_request_separation_matrix_v1.json", "separation_matrix"),
    ("task_observation_request_contract_decision_trace_v1.json", "trace"),
    ("task_observation_request_contract_final_decision_v1.json", "final"),
    ("task_observation_request_boundary_report_v1.json", "boundary"),
    ("task_observation_request_metrics_candidate_report_v1.json", "metrics"),
    ("task_observation_request_benchmark_link_report_v1.json", "benchmark_link"),
    ("task_observation_request_system_health_report_v1.json", "health_report"),
    ("task_observation_request_no_write_boundary_report_v1.json", "no_write"),
    ("task_observation_request_simulation_context_report_v1.json", "sim_report"),
    ("task_observation_request_non_claims_report_v1.json", "non_claims"),
    ("task_observation_request_open_followups_v1.json", "followups"),
    ("task_observation_request_audit_report_v1.json", "audit"),
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
    ap.add_argument("--basic-loop-audit-root", required=True)
    ap.add_argument("--task-manager-runtime-root", required=True)
    ap.add_argument("--task-manager-contract-root", required=True)
    ap.add_argument("--midplatform-task-state-root", required=True)
    ap.add_argument("--vision-capture-governance-root", required=True)
    ap.add_argument("--vision-capture-runtime-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-root", required=True)
    ap.add_argument("--voice-guidance-runtime-root", required=True)
    ap.add_argument("--vop-adapter-root", required=True)
    ap.add_argument("--hardware-stub-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.task_observation_request_contract_v1 import (
        run_task_observation_request_contract_v1,
    )

    result = run_task_observation_request_contract_v1(
        basic_loop_audit_root=str(_require_abs(args.basic_loop_audit_root, "audit")),
        task_manager_runtime_root=str(_require_abs(args.task_manager_runtime_root, "tm_rt")),
        task_manager_contract_root=str(_require_abs(args.task_manager_contract_root, "tm_contract")),
        midplatform_task_state_root=str(_require_abs(args.midplatform_task_state_root, "mp_state")),
        vision_capture_governance_root=str(_require_abs(args.vision_capture_governance_root, "vision_gov")),
        vision_capture_runtime_root=str(_require_abs(args.vision_capture_runtime_root, "vision_rt")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_root=str(_require_abs(args.stc_root, "stc")),
        voice_guidance_runtime_root=str(_require_abs(args.voice_guidance_runtime_root, "voice_guidance")),
        vop_adapter_root=str(_require_abs(args.vop_adapter_root, "vop")),
        hardware_stub_root=str(_require_abs(args.hardware_stub_root, "hardware")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "task_observation_request_notes.md").write_text(
        "# Task Observation Request Contract v1\n\n"
        f"Final: `{result['final']['final_decision']}`\n"
        f"Next: `{result['final']['recommended_next_phase']}`\n"
        f"Candidates: {result['final']['observation_request_candidate_count']}\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_root": str(out),
                "final_decision": result["final"]["final_decision"],
                "observation_request_candidate_count": result["final"]["observation_request_candidate_count"],
                "baseline_count": result["final"]["baseline_request_candidate_count"],
                "task_driven_count": result["final"]["task_driven_request_candidate_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

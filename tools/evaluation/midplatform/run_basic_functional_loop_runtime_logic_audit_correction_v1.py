#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Basic-Functional-Loop-Runtime-Logic-Audit-and-Correction-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("basic_functional_loop_runtime_logic_audit_correction_v1_summary.json", "summary"),
    ("basic_loop_runtime_logic_input_intake_matrix_v1.json", "intake"),
    ("basic_loop_runtime_mainline_sequence_matrix_v1.json", "mainline"),
    ("basic_loop_baseline_safety_loop_policy_v1.json", "baseline_policy"),
    ("basic_loop_task_driven_loop_policy_v1.json", "task_driven_policy"),
    ("basic_loop_authority_boundary_matrix_v1.json", "authority"),
    ("basic_loop_candidate_to_commit_transition_matrix_v1.json", "candidate_transition"),
    ("basic_loop_observation_request_gap_analysis_v1.json", "observation_gap"),
    ("basic_loop_task_observation_request_contract_stub_v1.json", "observation_stub"),
    ("basic_loop_vision_evidence_lifecycle_matrix_v1.json", "evidence_lifecycle"),
    ("basic_loop_ocr_joint_gate_matrix_v1.json", "ocr_joint"),
    ("basic_loop_speech_output_path_matrix_v1.json", "speech_path"),
    ("basic_loop_safety_task_arbitration_matrix_v1.json", "arbitration"),
    ("basic_loop_navigation_guidance_action_boundary_v1.json", "nav_boundary"),
    ("basic_loop_information_lifecycle_gap_registry_v1.json", "info_lifecycle"),
    ("basic_loop_memory_system_boundary_deferred_report_v1.json", "memory_deferred"),
    ("basic_loop_missing_contract_registry_v1.json", "missing_contracts"),
    ("basic_loop_corrected_phase_roadmap_v1.json", "roadmap"),
    ("basic_loop_runtime_logic_audit_decision_trace_v1.json", "trace"),
    ("basic_loop_runtime_logic_audit_final_decision_v1.json", "final"),
    ("basic_loop_runtime_logic_audit_boundary_report_v1.json", "boundary"),
    ("basic_loop_runtime_logic_audit_metrics_candidate_report_v1.json", "metrics"),
    ("basic_loop_runtime_logic_audit_benchmark_link_report_v1.json", "benchmark_link"),
    ("basic_loop_runtime_logic_audit_system_health_report_v1.json", "health_report"),
    ("basic_loop_runtime_logic_audit_no_write_boundary_report_v1.json", "no_write"),
    ("basic_loop_runtime_logic_audit_simulation_context_report_v1.json", "sim_report"),
    ("basic_loop_runtime_logic_audit_non_claims_report_v1.json", "non_claims"),
    ("basic_loop_runtime_logic_audit_open_followups_v1.json", "followups"),
    ("basic_loop_runtime_logic_audit_audit_report_v1.json", "audit"),
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
    ap.add_argument("--voice-dialogue-contract-root", required=True)
    ap.add_argument("--voice-dialogue-runtime-root", required=True)
    ap.add_argument("--midplatform-task-state-root", required=True)
    ap.add_argument("--task-manager-contract-root", required=True)
    ap.add_argument("--task-manager-runtime-root", required=True)
    ap.add_argument("--ocr-mainline-closure-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-root", required=True)
    ap.add_argument("--vision-capture-governance-root", required=True)
    ap.add_argument("--vision-capture-runtime-root", required=True)
    ap.add_argument("--voice-guidance-runtime-root", required=True)
    ap.add_argument("--vop-adapter-root", required=True)
    ap.add_argument("--hardware-stub-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.basic_functional_loop_runtime_logic_audit_correction_v1 import (
        run_basic_functional_loop_runtime_logic_audit_correction_v1,
    )

    result = run_basic_functional_loop_runtime_logic_audit_correction_v1(
        basic_loop_plan_root=str(_require_abs(args.basic_loop_plan_root, "plan")),
        voice_dialogue_contract_root=str(_require_abs(args.voice_dialogue_contract_root, "voice_contract")),
        voice_dialogue_runtime_root=str(_require_abs(args.voice_dialogue_runtime_root, "voice_rt")),
        midplatform_task_state_root=str(_require_abs(args.midplatform_task_state_root, "mp_state")),
        task_manager_contract_root=str(_require_abs(args.task_manager_contract_root, "tm_contract")),
        task_manager_runtime_root=str(_require_abs(args.task_manager_runtime_root, "tm_rt")),
        ocr_mainline_closure_root=str(_require_abs(args.ocr_mainline_closure_root, "ocr_closure")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_root=str(_require_abs(args.stc_root, "stc")),
        vision_capture_governance_root=str(_require_abs(args.vision_capture_governance_root, "vision_gov")),
        vision_capture_runtime_root=str(_require_abs(args.vision_capture_runtime_root, "vision_rt")),
        voice_guidance_runtime_root=str(_require_abs(args.voice_guidance_runtime_root, "voice_guidance")),
        vop_adapter_root=str(_require_abs(args.vop_adapter_root, "vop")),
        hardware_stub_root=str(_require_abs(args.hardware_stub_root, "hardware")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "basic_loop_runtime_logic_audit_notes.md").write_text(
        "# Basic Functional Loop Runtime Logic Audit and Correction v1\n\n"
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

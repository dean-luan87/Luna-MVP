#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Basic-Navigation-Guidance-Loop-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("basic_navigation_guidance_loop_dryrun_v1_summary.json", "summary"),
    ("basic_navigation_guidance_loop_input_intake_matrix_v1.json", "intake"),
    ("basic_navigation_baseline_safety_loop_dryrun_matrix_v1.json", "baseline_matrix"),
    ("basic_navigation_task_driven_loop_dryrun_matrix_v1.json", "task_matrix"),
    ("basic_navigation_guidance_decision_candidate_collection_v1.json", "guidance_decisions"),
    ("basic_navigation_speech_chain_readiness_matrix_v1.json", "speech_readiness"),
    ("basic_navigation_safety_priority_preservation_matrix_v1.json", "safety_priority"),
    ("basic_navigation_guidance_action_boundary_check_v1.json", "nav_boundary"),
    ("basic_navigation_ocr_use_boundary_check_v1.json", "ocr_boundary"),
    ("basic_navigation_evidence_freshness_uncertainty_check_v1.json", "freshness_uncertainty"),
    ("basic_navigation_guidance_loop_end_to_end_candidate_trace_v1.json", "e2e_trace"),
    ("basic_navigation_guidance_loop_decision_trace_v1.json", "trace"),
    ("basic_navigation_guidance_loop_final_decision_v1.json", "final"),
    ("basic_navigation_guidance_loop_boundary_report_v1.json", "boundary"),
    ("basic_navigation_guidance_loop_metrics_candidate_report_v1.json", "metrics"),
    ("basic_navigation_guidance_loop_benchmark_link_report_v1.json", "benchmark_link"),
    ("basic_navigation_guidance_loop_system_health_report_v1.json", "health_report"),
    ("basic_navigation_guidance_loop_no_write_boundary_report_v1.json", "no_write"),
    ("basic_navigation_guidance_loop_simulation_context_report_v1.json", "sim_report"),
    ("basic_navigation_guidance_loop_non_claims_report_v1.json", "non_claims"),
    ("basic_navigation_guidance_loop_open_followups_v1.json", "followups"),
    ("basic_navigation_guidance_loop_audit_report_v1.json", "audit"),
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
    ap.add_argument("--task-observation-request-root", required=True)
    ap.add_argument("--vision-ocr-ingest-root", required=True)
    ap.add_argument("--navigation-guidance-speech-adapter-root", required=True)
    ap.add_argument("--task-manager-runtime-root", required=True)
    ap.add_argument("--voice-dialogue-runtime-root", required=True)
    ap.add_argument("--vop-adapter-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.basic_navigation_guidance_loop_dryrun_v1 import (
        run_basic_navigation_guidance_loop_dryrun_v1,
    )

    result = run_basic_navigation_guidance_loop_dryrun_v1(
        basic_loop_audit_root=str(_require_abs(args.basic_loop_audit_root, "audit")),
        task_observation_request_root=str(_require_abs(args.task_observation_request_root, "obs_req")),
        vision_ocr_ingest_root=str(_require_abs(args.vision_ocr_ingest_root, "vision_ocr")),
        navigation_guidance_speech_adapter_root=str(
            _require_abs(args.navigation_guidance_speech_adapter_root, "speech_adapter")
        ),
        task_manager_runtime_root=str(_require_abs(args.task_manager_runtime_root, "tm_rt")),
        voice_dialogue_runtime_root=str(_require_abs(args.voice_dialogue_runtime_root, "voice_dialogue")),
        vop_adapter_root=str(_require_abs(args.vop_adapter_root, "vop")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_root=str(_require_abs(args.stc_root, "stc")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "basic_navigation_guidance_loop_notes.md").write_text(
        "# Basic Navigation Guidance Loop DryRun v1\n\n"
        f"Final: `{result['final']['final_decision']}`\n"
        f"Next: `{result['final']['recommended_next_phase']}`\n"
        f"Baseline loops: {result['final']['baseline_loop_candidate_count']}\n"
        f"Task-driven loops: {result['final']['task_driven_loop_candidate_count']}\n"
        f"E2E traces: {result['e2e_trace']['trace_count']}\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_root": str(out),
                "final_decision": result["final"]["final_decision"],
                "baseline_count": result["final"]["baseline_loop_candidate_count"],
                "task_count": result["final"]["task_driven_loop_candidate_count"],
                "trace_count": result["e2e_trace"]["trace_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Navigation-Guidance-to-Speech-Candidate-Adapter-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("navigation_guidance_to_speech_candidate_adapter_v1_summary.json", "summary"),
    ("navigation_guidance_speech_adapter_input_intake_matrix_v1.json", "intake"),
    ("navigation_guidance_source_intake_matrix_v1.json", "guidance_source"),
    ("navigation_guidance_to_speech_mapping_policy_v1.json", "mapping_policy"),
    ("navigation_guidance_speech_priority_policy_v1.json", "priority_policy"),
    ("navigation_guidance_safety_suppression_policy_v1.json", "suppression_policy"),
    ("navigation_guidance_uncertainty_language_policy_v1.json", "uncertainty_policy"),
    ("navigation_guidance_speech_request_candidate_schema_v1.json", "speech_schema"),
    ("navigation_guidance_speech_candidate_collection_v1.json", "speech_collection"),
    ("navigation_guidance_vop_handoff_candidate_v1.json", "vop_handoff"),
    ("navigation_guidance_speech_gate_admission_dryrun_candidate_v1.json", "gate_admission"),
    ("navigation_guidance_speech_adapter_navigation_action_boundary_v1.json", "nav_boundary"),
    ("navigation_guidance_evidence_freshness_speech_check_v1.json", "freshness_check"),
    ("navigation_guidance_to_speech_adapter_decision_trace_v1.json", "trace"),
    ("navigation_guidance_to_speech_adapter_final_decision_v1.json", "final"),
    ("navigation_guidance_to_speech_adapter_boundary_report_v1.json", "boundary"),
    ("navigation_guidance_to_speech_adapter_metrics_candidate_report_v1.json", "metrics"),
    ("navigation_guidance_to_speech_adapter_benchmark_link_report_v1.json", "benchmark_link"),
    ("navigation_guidance_to_speech_adapter_system_health_report_v1.json", "health_report"),
    ("navigation_guidance_to_speech_adapter_no_write_boundary_report_v1.json", "no_write"),
    ("navigation_guidance_to_speech_adapter_simulation_context_report_v1.json", "sim_report"),
    ("navigation_guidance_to_speech_adapter_non_claims_report_v1.json", "non_claims"),
    ("navigation_guidance_to_speech_adapter_open_followups_v1.json", "followups"),
    ("navigation_guidance_to_speech_adapter_audit_report_v1.json", "audit"),
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
    ap.add_argument("--vision-ocr-ingest-root", required=True)
    ap.add_argument("--task-observation-request-root", required=True)
    ap.add_argument("--task-manager-runtime-root", required=True)
    ap.add_argument("--basic-loop-audit-root", required=True)
    ap.add_argument("--voice-dialogue-runtime-root", required=True)
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

    from capabilities.midplatform.navigation_guidance_to_speech_candidate_adapter_v1 import (
        run_navigation_guidance_to_speech_candidate_adapter_v1,
    )

    result = run_navigation_guidance_to_speech_candidate_adapter_v1(
        vision_ocr_ingest_root=str(_require_abs(args.vision_ocr_ingest_root, "vision_ocr")),
        task_observation_request_root=str(_require_abs(args.task_observation_request_root, "obs_req")),
        task_manager_runtime_root=str(_require_abs(args.task_manager_runtime_root, "tm_rt")),
        basic_loop_audit_root=str(_require_abs(args.basic_loop_audit_root, "audit")),
        voice_dialogue_runtime_root=str(_require_abs(args.voice_dialogue_runtime_root, "voice_dialogue")),
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

    (out / "navigation_guidance_to_speech_adapter_notes.md").write_text(
        "# Navigation Guidance to Speech Candidate Adapter v1\n\n"
        f"Final: `{result['final']['final_decision']}`\n"
        f"Next: `{result['final']['recommended_next_phase']}`\n"
        f"Speech candidates: {result['final']['speech_candidate_count']}\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_root": str(out),
                "final_decision": result["final"]["final_decision"],
                "speech_count": result["final"]["speech_candidate_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

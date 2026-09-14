#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-001 — Controlled trial execution plan & order definition (definition-only).

Does NOT execute trials, call providers, TTS, playback, or modify runtime defaults.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PHASE = "Phase-Mainline-GuardedTrial-001"
PLAN_ID = "mainline_controlled_trial_plan_v0"


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def build_artifacts() -> Dict[str, Any]:
    order_matrix: List[Dict[str, Any]] = [
        {
            "stage_index": 1,
            "stage_name": "Stage_1_YOLO_guarded_trial",
            "capability": "yolo",
            "trial_key": "yolo_guarded_trial_v1",
            "env_entry_flag": "LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1",
            "rationale": "Perception layer; low user impact; no voice/output chain.",
            "starts_after": [],
            "next_blocked_until_go": True,
        },
        {
            "stage_index": 2,
            "stage_name": "Stage_2_OCR_guarded_trial",
            "capability": "ocr",
            "trial_key": "ocr_guarded_trial_v1",
            "env_entry_flag": "LUNA_ENABLE_OCR_GUARDED_TRIAL_V1",
            "rationale": "Text layer; no semantic downstream; no user output.",
            "starts_after": ["Stage_1_YOLO_guarded_trial=GO"],
            "next_blocked_until_go": True,
        },
        {
            "stage_index": 3,
            "stage_name": "Stage_3_Qwen_Voice_governed_entry_trial",
            "capability": "qwen_voice",
            "trial_key": "qwen_voice_governed_entry_trial_v1",
            "env_entry_flag": "LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1",
            "rationale": "Output chain; highest user-impact risk; last.",
            "starts_after": ["Stage_1_YOLO_guarded_trial=GO", "Stage_2_OCR_guarded_trial=GO"],
            "next_blocked_until_go": True,
        },
    ]

    scope_matrix: List[Dict[str, Any]] = [
        {
            "capability": "yolo",
            "trial_name": "yolo_guarded_trial_v1",
            "objective": "Validate real frame / detector / RequestTrace injection vs shadow baseline.",
            "allowed": [
                "read_real_frame",
                "invoke_yolo_detector",
                "emit_detection_result",
                "write_trace_replay_whitebox",
                "emit_request_trace_stage",
                "compare_with_shadow_baseline",
            ],
            "forbidden": [
                "trigger_ocr_from_yolo",
                "enter_midplatform",
                "enter_scene_task_fusion_output",
                "navigation_action",
                "playback",
                "world_model_write",
                "hive_upload",
            ],
            "suggested_windows": {
                "dry_run_precheck_frames": 10,
                "controlled_local_trial_frames": 50,
                "extended_local_trial_frames": 200,
                "extended_requires_prior_go": "controlled_local_trial_frames=GO",
            },
        },
        {
            "capability": "ocr",
            "trial_name": "ocr_guarded_trial_v1",
            "objective": "Validate OCR source policy / provider / fallback / raw_text / RequestTrace.",
            "start_condition": "Stage_1 YOLO guarded trial = GO",
            "allowed": [
                "read_frame_or_crop",
                "invoke_ocr_source_policy",
                "invoke_provider_under_explicit_flag",
                "fallback_or_not_available",
                "write_raw_text_candidate",
                "write_trace_replay_whitebox",
                "emit_request_trace_stage",
            ],
            "forbidden": [
                "semantic_interpretation_enabled=true",
                "midplatform_downstream_auto_consume",
                "scene_task_fusion_output",
                "navigation_action",
                "playback",
                "world_model_write",
                "hive_upload",
            ],
            "suggested_windows": {
                "provider_disabled_precheck_samples": 10,
                "provider_controlled_trial_samples": 30,
                "extended_ocr_trial_samples": 100,
                "extended_requires_prior_go": "provider_controlled_trial=GO",
            },
        },
        {
            "capability": "qwen_voice",
            "trial_name": "qwen_voice_governed_entry_trial_v1",
            "objective": "Validate voice governance → governed entry → provider selection / diff audit / RequestTrace.",
            "start_condition": "Stage_1 YOLO=GO AND Stage_2 OCR=GO",
            "sub_stages": {
                "3A_governed_entry_dry_run": {
                    "description": "selection / diff_audit; no default real playback",
                    "requires": {"provider_invoked": False, "playback": False},
                },
                "3B_controlled_provider_invocation": {
                    "description": "Only after 3A GO; provider allowed when explicitly flagged",
                    "requires": {"playback_invoked": False},
                },
                "3C_controlled_playback": {
                    "description": "Only after 3B GO; short window; separate human approval",
                    "phase_001_status": "NOT_APPROVED_future_only",
                    "requires_human_confirmation": True,
                },
            },
            "allowed": [
                "read_voice_governance_decision",
                "run_GovernedVoiceProviderEntry",
                "provider_selection_dry_run",
                "optional_provider_invocation_only_in_approved_sub_stage_3B",
                "diff_audit",
                "emit_request_trace_stage",
                "fallback_decision",
            ],
            "forbidden": [
                "default_real_qwen",
                "default_real_tts",
                "default_playback",
                "bypass_governance",
                "remove_piper_fallback",
                "change_default_provider_policy",
                "output_to_user_audible_chain_without_approval",
            ],
        },
    ]

    acceptance_matrix: List[Dict[str, Any]] = [
        {
            "stage": "Stage_1_YOLO",
            "metrics": [
                {"name": "detector_invocation_success_rate", "threshold": ">= 0.95"},
                {"name": "schema_valid_rate", "threshold": "== 1.0"},
                {"name": "request_trace_emission_rate", "threshold": "== 1.0"},
                {"name": "downstream_invocation_count", "threshold": "== 0"},
                {"name": "navigation_action", "threshold": "null"},
                {"name": "real_tts_invoked", "threshold": "false"},
                {"name": "world_write_invoked", "threshold": "false"},
                {"name": "abort_switch_works", "threshold": "true"},
                {"name": "latency_p95", "threshold": "recorded_only_no_production_sla"},
            ],
        },
        {
            "stage": "Stage_2_OCR",
            "metrics": [
                {"name": "source_policy_selected_rate", "threshold": "== 1.0"},
                {"name": "provider_or_fallback_or_not_available_valid", "threshold": "100% legal outcomes"},
                {"name": "raw_text_schema_valid_rate", "threshold": "== 1.0"},
                {"name": "semantic_interpretation_enabled", "threshold": "false"},
                {"name": "downstream_invocation_count", "threshold": "== 0"},
                {"name": "real_tts_invoked", "threshold": "false"},
                {"name": "navigation_action", "threshold": "null"},
                {"name": "request_trace_emission_rate", "threshold": "== 1.0"},
                {"name": "governance_leakage", "threshold": "== 0"},
            ],
        },
        {
            "stage": "Stage_3_Qwen_Voice_3A",
            "metrics": [
                {"name": "governance_decision_exists", "threshold": "true"},
                {"name": "guard_speech_gate_result_exists", "threshold": "true"},
                {"name": "source_text_provider_input_spoken_diff_audit_present", "threshold": "true"},
                {"name": "blocked_request_selected_provider", "threshold": "none"},
                {"name": "offline_only_never_selects_qwen", "threshold": "true"},
                {"name": "qwen_only_in_online_prefer_qwen_allowed_mode", "threshold": "true"},
                {"name": "provider_invoked", "threshold": "false"},
                {"name": "playback_invoked", "threshold": "false"},
                {"name": "real_tts_invoked", "threshold": "false"},
                {"name": "request_trace_emission_rate", "threshold": "== 1.0"},
            ],
        },
        {
            "stage": "Stage_3_Qwen_Voice_3B",
            "metrics": [
                {"name": "provider_invocation_explicitly_flagged", "threshold": "true"},
                {"name": "provider_health_recorded", "threshold": "true"},
                {"name": "latency_recorded", "threshold": "true"},
                {"name": "timeout_handled", "threshold": "true"},
                {"name": "fallback_works", "threshold": "true"},
                {"name": "playback_invoked", "threshold": "false"},
                {"name": "source_text_diff_audit_preserved", "threshold": "true"},
                {"name": "provider_output_ref_recorded", "threshold": "true"},
            ],
        },
    ]

    abort_rollback_matrix: List[Dict[str, Any]] = [
        {
            "stage": "Stage_1_YOLO",
            "abort_conditions": [
                "detector_exception_streak >= 2",
                "schema_invalid_any",
                "downstream_invocation > 0",
                "navigation_action non-null",
                "real_tts_invoked=true",
                "world_write_invoked=true",
                "request_trace_missing",
                "global_kill_switch_triggered",
            ],
            "rollback_actions": [
                "disable LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1",
                "set LUNA_DISABLE_ALL_GUARDED_TRIALS=true if needed",
                "return_to_shadow_or_offline",
                "retain_logs",
                "generate post_trial_report",
            ],
        },
        {
            "stage": "Stage_2_OCR",
            "abort_conditions": [
                "source_policy_missing",
                "provider_exception_not_caught_by_fallback",
                "semantic_output_detected",
                "downstream_invocation > 0",
                "navigation_action non-null",
                "real_tts_invoked=true",
                "world_write_invoked=true",
                "request_trace_missing",
                "global_kill_switch_triggered",
            ],
            "rollback_actions": [
                "disable LUNA_ENABLE_OCR_GUARDED_TRIAL_V1",
                "force OCR mode shadow_only / not_available",
                "retain raw outputs",
                "generate post_trial_report",
            ],
        },
        {
            "stage": "Stage_3_Qwen_Voice",
            "abort_3A": [
                "governance_decision_missing",
                "speech_gate_missing",
                "diff_audit_missing",
                "blocked_request_selects_provider",
                "offline_only_selects_qwen",
                "provider_invoked=true",
                "playback_invoked=true",
                "request_trace_missing",
            ],
            "abort_3B": [
                "provider_invoked_without_flag",
                "playback_invoked",
                "timeout_not_handled",
                "fallback_failed",
                "diff_audit_missing",
                "provider_output_not_traceable",
            ],
            "rollback_actions": [
                "disable LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1",
                "disable provider invocation flags",
                "force offline_only / selected_provider=none",
                "retain logs",
                "generate post_trial_report",
            ],
        },
    ]

    precheck_matrix: List[Dict[str, Any]] = [
        {"check_id": "PT01", "rule": "LUNA_DISABLE_ALL_GUARDED_TRIALS must be false for trial (unless emergency)"},
        {"check_id": "PT02", "rule": "Only one trial entry flag may be true among YOLO/OCR/Qwen Voice"},
        {"check_id": "PT03", "rule": "All unrelated trial flags false"},
        {"check_id": "PT04", "rule": "RequestTrace output path writable"},
        {"check_id": "PT05", "rule": "trace/replay/whitebox output paths writable"},
        {"check_id": "PT06", "rule": "Rollback command documented"},
        {"check_id": "PT07", "rule": "Abort conditions active / monitored"},
        {"check_id": "PT08", "rule": "Operator confirms trial window"},
        {"check_id": "PT09", "rule": "Previous stage GO exists when required by order policy"},
        {"check_id": "PT10", "rule": "Global kill switch reachable (one-key disable all)"},
    ]

    post_report_schema: Dict[str, Any] = {
        "$schema": "luna.mainline_controlled_trial.post_report.v0",
        "required_fields": [
            "trial_id",
            "capability",
            "window_start",
            "window_end",
            "sample_count",
            "env_snapshot",
            "pass_fail_summary",
            "abort_events",
            "rollback_events",
            "trw_completeness",
            "hard_audit_summary",
            "side_effect_summary",
        ],
        "recommendation_enum": ["GO_next_window", "CONDITIONAL_GO_repeat", "NO_GO_rollback_and_fix"],
        "notes": "Generated per trial; Phase-001 defines schema only.",
    }

    summary: Dict[str, Any] = {
        "phase": PHASE,
        "plan_id": PLAN_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(Path(REPO_ROOT).resolve()),
        "prior_closure_reference": {
            "phase": "Phase-Mainline-RuntimeReadiness-006",
            "runtime_readiness_status": "closed_v0",
            "scope": "guarded_trial_readiness_layer",
            "real_runtime_activation_allowed": False,
            "real_qwen_invocation_allowed": False,
            "real_tts_invocation_allowed": False,
            "real_playback_allowed": False,
            "default_trial_enabled": False,
            "global_kill_switch_required": True,
            "whitebox_scope": "minimal_observability_only",
        },
        "execution_policy": {
            "sequential_only": True,
            "order": ["yolo", "ocr", "qwen_voice"],
            "no_parallel_trials": True,
            "single_active_capability_trial": True,
            "prior_stage_go_required_for_next": True,
            "any_stage_no_go_halts_later_stages": True,
            "global_kill_switch_must_disable_all": True,
        },
        "definition_only": {
            "real_trial_executed": False,
            "real_runtime_executed": False,
            "real_qwen_called": False,
            "real_tts_executed": False,
            "real_playback_executed": False,
            "playback_approved_in_this_phase": False,
            "qwen_voice_3C": "future_only_not_approved_in_phase_001",
        },
        "verdict": {
            "controlled_trial_plan_definition": "GO",
            "sample_count_and_latency_tuning": "CONDITIONAL_GO",
            "real_trial_execution": "NO_GO",
        },
    }

    return {
        "summary": summary,
        "order_matrix": order_matrix,
        "scope_matrix": scope_matrix,
        "acceptance_matrix": acceptance_matrix,
        "abort_rollback_matrix": abort_rollback_matrix,
        "precheck_matrix": precheck_matrix,
        "post_report_schema": post_report_schema,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = Path(REPO_ROOT)
    out = Path(args.output_root) if args.output_root else repo / "logs" / f"mainline_controlled_trial_plan_001_{_utc_tag()}"

    art = build_artifacts()
    _write_json(out / "mainline_controlled_trial_plan_summary.json", art["summary"])
    _write_json(out / "mainline_controlled_trial_order_matrix.json", art["order_matrix"])
    _write_json(out / "mainline_controlled_trial_scope_matrix.json", art["scope_matrix"])
    _write_json(out / "mainline_controlled_trial_acceptance_matrix.json", art["acceptance_matrix"])
    _write_json(out / "mainline_controlled_trial_abort_rollback_matrix.json", art["abort_rollback_matrix"])
    _write_json(out / "mainline_controlled_trial_precheck_matrix.json", art["precheck_matrix"])
    _write_json(out / "mainline_controlled_trial_post_report_schema.json", art["post_report_schema"])

    notes = [
        f"# {PHASE} — controlled trial plan (definition only)",
        "",
        f"- output_root: `{out}`",
        "- No trial executed; no provider/Qwen/TTS/playback in this tool.",
        "",
    ]
    (out / "review_notes.md").write_text("\n".join(notes), encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out), "verdict": art["summary"].get("verdict")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

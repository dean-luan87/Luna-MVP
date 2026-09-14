#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-RuntimeReadiness-002 — Guarded trial scope / env / acceptance / rollback definition.

Definition-only. Does NOT wire runtime, call providers, or change defaults.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

PHASE = "Phase-Mainline-RuntimeReadiness-002"
DEFINITION_ID = "mainline_guarded_trial_definition_v0"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _trial_matrix() -> List[Dict[str, Any]]:
    return [
        {
            "trial_name": "yolo_guarded_trial_v1",
            "capability": "yolo",
            "default_enabled": False,
            "entry_flag": "LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1",
            "allowed_actions": [
                "read_real_frame",
                "invoke_yolo_detector",
                "emit_detection_result",
                "write_trace_replay_whitebox",
                "emit_request_trace_stage",
                "compare_with_shadow_output",
            ],
            "forbidden_actions": [
                "enter_scene_task_fusion_output",
                "navigation_action",
                "trigger_playback_or_tts",
                "write_world_model",
                "upload_hive",
                "auto_affect_task_chain",
                "downstream_semantic_consumer_invocation",
            ],
            "acceptance_checks": [
                "detector_invocation_success_rate >= configured_threshold",
                "frame_id_timestamp_request_id_trace_id_injected",
                "detection_result_schema_valid",
                "downstream_invocation_count == 0",
                "request_trace_stage_emitted",
                "abort_path_verified_on_injected_fault",
            ],
            "abort_conditions": [
                "detector_exception",
                "missing_frame_id",
                "detection_schema_invalid",
                "latency_ms > trial_latency_budget_ms",
                "confidence_collapse_per_policy",
                "downstream_invocation_detected",
            ],
            "rollback_actions": [
                "set LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1=false",
                "return_to_offline_or_shadow_only_mode",
                "retain_trial_logs_under_trial_id",
            ],
            "required_trw_fields": [
                "request_id",
                "trace_id",
                "session_id",
                "runtime_run_id",
                "source_run_id",
                "execution_plane",
                "trial_id",
                "trial_mode",
                "capability",
                "hard_audit",
                "trace_ref",
                "replay_ref",
                "whitebox_ref",
            ],
            "max_allowed_readiness_level_after_pass": "R3_guarded_wiring_ready",
        },
        {
            "trial_name": "ocr_guarded_trial_v1",
            "capability": "ocr",
            "default_enabled": False,
            "entry_flag": "LUNA_ENABLE_OCR_GUARDED_TRIAL_V1",
            "allowed_actions": [
                "read_frame_or_crop",
                "invoke_ocr_source_policy",
                "invoke_provider_only_if_flags_allow",
                "fallback_or_not_available_path",
                "write_raw_text_candidate",
                "write_trace_replay_whitebox",
                "emit_request_trace_stage",
            ],
            "forbidden_actions": [
                "semantic_interpretation_enabled_true",
                "downstream_invocation",
                "navigation_action",
                "tts_or_playback",
                "write_world_model",
                "scene_task_fusion_output",
                "upload_hive",
            ],
            "acceptance_checks": [
                "source_policy_selected_and_logged",
                "provider_selected_or_fallback_or_not_available_valid",
                "raw_text_schema_valid",
                "semantic_interpretation_enabled_false",
                "downstream_invocation_count == 0",
                "governance_leakage_count == 0",
                "request_trace_stage_emitted",
            ],
            "abort_conditions": [
                "source_policy_missing",
                "provider_exception",
                "raw_text_schema_invalid",
                "semantic_output_detected",
                "downstream_invocation_detected",
                "real_tts_invoked_true",
            ],
            "rollback_actions": [
                "set LUNA_ENABLE_OCR_GUARDED_TRIAL_V1=false",
                "force_not_available_or_shadow_only",
                "retain_raw_outputs_under_trial_id",
            ],
            "required_trw_fields": [
                "request_id",
                "trace_id",
                "session_id",
                "runtime_run_id",
                "source_run_id",
                "execution_plane",
                "trial_id",
                "trial_mode",
                "capability",
                "hard_audit",
                "trace_ref",
                "replay_ref",
                "whitebox_ref",
            ],
            "max_allowed_readiness_level_after_pass": "R3_guarded_wiring_ready",
        },
        {
            "trial_name": "qwen_voice_governed_entry_trial_v1",
            "capability": "qwen_voice",
            "default_enabled": False,
            "entry_flag": "LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1",
            "allowed_actions": [
                "read_voice_output_governance_decision",
                "run_governed_voice_provider_entry",
                "provider_selection_dry_run",
                "optional_guarded_provider_invocation_only_under_explicit_flags",
                "write_diff_audit",
                "emit_request_trace_stage",
                "record_fallback_decision",
            ],
            "forbidden_actions": [
                "default_real_qwen_without_flags",
                "default_real_tts_without_flags",
                "default_real_playback_without_flags",
                "bypass_governance",
                "direct_run_tts_unified_entry_without_gates",
                "remove_piper_fallback",
                "change_default_provider_policy",
                "navigation_action",
                "write_world_model",
                "downstream_scene_task_or_fusion_invocation",
            ],
            "acceptance_checks": [
                "voice_output_governance_decision_exists",
                "guard_speechgate_passed_where_contract_requires",
                "governed_voice_provider_entry_decision_emitted",
                "source_text_spoken_text_diff_audit_present",
                "qwen_only_when_online_prefer_qwen_or_explicit_allowed_mode",
                "offline_only_never_selects_qwen",
                "blocked_request_selected_provider_none",
                "request_trace_stage_emitted",
                "hard_audit_valid_real_flags_expected_false_by_default",
            ],
            "abort_conditions": [
                "governance_decision_missing",
                "speechgate_missing_where_required",
                "diff_audit_missing_when_required_by_mode",
                "blocked_request_non_none_provider",
                "offline_only_selects_qwen",
                "provider_invoked_without_allow_flag",
                "playback_invoked_without_allow_flag",
                "unexpected_real_tts_invoked",
                "env_inconsistency_global_disable_vs_capability_enable",
            ],
            "rollback_actions": [
                "set LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1=false",
                "force_provider_mode_offline_only",
                "force_selected_provider_none_on_uncertainty",
                "retain_trial_logs_under_trial_id",
            ],
            "required_trw_fields": [
                "request_id",
                "trace_id",
                "session_id",
                "runtime_run_id",
                "source_run_id",
                "execution_plane",
                "trial_id",
                "trial_mode",
                "capability",
                "hard_audit",
                "trace_ref",
                "replay_ref",
                "whitebox_ref",
            ],
            "max_allowed_readiness_level_after_pass": "R3_guarded_wiring_ready",
        },
    ]


def _env_flag_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = [
        {
            "flag_name": "LUNA_DISABLE_ALL_GUARDED_TRIALS",
            "scope": "global",
            "capability": "all",
            "purpose": "global_kill_switch：为 true 时禁止一切 guarded trial（优先级最高）",
            "default_value": False,
            "semantic_when_true": "所有 YOLO/OCR/Qwen Voice trial 不得运行，即使分项 flag 为 true",
            "priority_rank": 0,
            "owner": "runtime",
        },
        {
            "flag_name": "LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1",
            "scope": "trial_entry",
            "capability": "yolo",
            "purpose": "YOLO guarded trial 总入口",
            "default_value": False,
            "semantic_when_true": "允许进入 trial 管线（仍受 global disable 约束）",
            "priority_rank": 10,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_YOLO_TRIAL_MODE",
            "scope": "mode",
            "capability": "yolo",
            "purpose": "shadow_only | guarded_local",
            "default_value": "shadow_only",
            "semantic_when_true": "枚举取值，非布尔",
            "priority_rank": 11,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_YOLO_TRIAL_MAX_FRAMES",
            "scope": "budget",
            "capability": "yolo",
            "purpose": "单次 trial 最大帧数上限",
            "default_value": 0,
            "semantic_when_true": "0 表示使用默认内置上限（接线 PR 冻结具体数值）",
            "priority_rank": 12,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_YOLO_TRIAL_ABORT_ON_DETECTOR_ERROR",
            "scope": "safety",
            "capability": "yolo",
            "purpose": "detector 异常即 abort trial tick",
            "default_value": True,
            "semantic_when_true": "trial 安全默认偏保守",
            "priority_rank": 13,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_YOLO_TRIAL_WRITE_REQUEST_TRACE",
            "scope": "observability",
            "capability": "yolo",
            "purpose": "trial 期间写 RequestTrace stage",
            "default_value": True,
            "semantic_when_true": "关闭则仅适合离线调试（不推荐 trial 验收）",
            "priority_rank": 14,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_ENABLE_OCR_GUARDED_TRIAL_V1",
            "scope": "trial_entry",
            "capability": "ocr",
            "purpose": "OCR guarded trial 总入口",
            "default_value": False,
            "semantic_when_true": "允许进入 OCR trial（受 global disable 约束）",
            "priority_rank": 10,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_OCR_TRIAL_MODE",
            "scope": "mode",
            "capability": "ocr",
            "purpose": "shadow_only | guarded_provider",
            "default_value": "shadow_only",
            "semantic_when_true": "枚举取值",
            "priority_rank": 11,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_OCR_TRIAL_PROVIDER_POLICY",
            "scope": "policy_ref",
            "capability": "ocr",
            "purpose": "trial 下使用的 source policy 标识（示例：ocr_default_offline_raw_text_source_policy_v0）",
            "default_value": "ocr_default_offline_raw_text_source_policy_v0",
            "semantic_when_true": "冻结为离线 raw text policy，不接语义",
            "priority_rank": 12,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION",
            "scope": "provider",
            "capability": "ocr",
            "purpose": "是否允许真实 OCR provider 调用",
            "default_value": False,
            "semantic_when_true": "仍禁止语义链路与下游",
            "priority_rank": 13,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_OCR_TRIAL_ABORT_ON_GOVERNANCE_LEAKAGE",
            "scope": "safety",
            "capability": "ocr",
            "purpose": "检测到治理泄漏则 abort",
            "default_value": True,
            "semantic_when_true": "默认启用",
            "priority_rank": 14,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_OCR_TRIAL_WRITE_REQUEST_TRACE",
            "scope": "observability",
            "capability": "ocr",
            "purpose": "trial 写 RequestTrace",
            "default_value": True,
            "semantic_when_true": "关闭则不适合 trial 验收",
            "priority_rank": 15,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1",
            "scope": "trial_entry",
            "capability": "qwen_voice",
            "purpose": "Qwen Voice governed entry trial 总入口",
            "default_value": False,
            "semantic_when_true": "允许进入 voice trial（受 global disable 约束）",
            "priority_rank": 10,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_QWEN_VOICE_TRIAL_MODE",
            "scope": "mode",
            "capability": "qwen_voice",
            "purpose": "shadow_only | governed_entry | provider_dry_run | controlled_provider",
            "default_value": "shadow_only",
            "semantic_when_true": "升级 controlled_provider 需完整 TRW，无 trace/session 则禁止升级",
            "priority_rank": 11,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_ENABLE_GOVERNED_QWEN_ENTRY_V1",
            "scope": "gate",
            "capability": "qwen_voice",
            "purpose": "显式开启 governed entry 真路径筹备（默认关闭）",
            "default_value": False,
            "semantic_when_true": "不改变仓库默认 provider yaml；仅 trial 闸",
            "priority_rank": 12,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_ENABLE_QWEN_PRIMARY_VOICE_MODE_V1",
            "scope": "gate",
            "capability": "qwen_voice",
            "purpose": "显式 trial online_prefer_qwen（与默认策略解耦）",
            "default_value": False,
            "semantic_when_true": "仅 trial 短窗",
            "priority_rank": 13,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_QWEN_VOICE_TRIAL_ALLOW_PROVIDER_INVOCATION",
            "scope": "provider",
            "capability": "qwen_voice",
            "purpose": "允许真实 provider 调用（仍禁止默认播放）",
            "default_value": False,
            "semantic_when_true": "须配合 mode 与 global disable",
            "priority_rank": 14,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_QWEN_VOICE_TRIAL_ALLOW_PLAYBACK",
            "scope": "playback",
            "capability": "qwen_voice",
            "purpose": "允许真实扬声器播放（默认禁止）",
            "default_value": False,
            "semantic_when_true": "独立于 provider invocation",
            "priority_rank": 15,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_QWEN_VOICE_TRIAL_ABORT_ON_DIFF_AUDIT_MISSING",
            "scope": "safety",
            "capability": "qwen_voice",
            "purpose": "diff_audit 缺失则 abort",
            "default_value": True,
            "semantic_when_true": "trial 默认严格",
            "priority_rank": 16,
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_QWEN_VOICE_TRIAL_WRITE_REQUEST_TRACE",
            "scope": "observability",
            "capability": "qwen_voice",
            "purpose": "trial 写 RequestTrace",
            "default_value": True,
            "semantic_when_true": "关闭则不得宣称 trial 通过",
            "priority_rank": 17,
            "owner": "sandbox",
        },
    ]
    return rows


def _abort_rollback_matrix() -> Dict[str, Any]:
    return {
        "priority_order": [
            "LUNA_DISABLE_ALL_GUARDED_TRIALS",
            "capability_entry_flag",
            "provider_or_mode_flags",
        ],
        "trials": [
            {
                "trial_name": "yolo_guarded_trial_v1",
                "abort_playbook_ref": "trial_matrix[].abort_conditions",
                "rollback_playbook_ref": "trial_matrix[].rollback_actions",
                "post_rollback_state": "offline_shadow_only_no_downstream",
            },
            {
                "trial_name": "ocr_guarded_trial_v1",
                "abort_playbook_ref": "trial_matrix[].abort_conditions",
                "rollback_playbook_ref": "trial_matrix[].rollback_actions",
                "post_rollback_state": "not_available_or_shadow_only",
            },
            {
                "trial_name": "qwen_voice_governed_entry_trial_v1",
                "abort_playbook_ref": "trial_matrix[].abort_conditions",
                "rollback_playbook_ref": "trial_matrix[].rollback_actions",
                "post_rollback_state": "offline_only_selected_provider_none_logs_retained",
            },
        ],
        "global_disable_behavior": {
            "when_LUNA_DISABLE_ALL_GUARDED_TRIALS_true": [
                "instant_short_circuit_all_trials",
                "log_short_circuit_reason",
                "no_partial_provider_side_effects",
            ]
        },
    }


def _trw_requirement_matrix() -> Dict[str, Any]:
    return {
        "missing_trace_or_session_policy": {
            "must_not_fabricate_ids": True,
            "must_record_missing_fields": True,
            "trial_must_not_upgrade_to_controlled_provider": True,
        },
        "required_fields_all_trials": [
            "request_id",
            "trace_id",
            "session_id",
            "runtime_run_id",
            "source_run_id",
            "execution_plane",
            "trial_id",
            "trial_mode",
            "capability",
            "hard_audit",
            "trace_ref",
            "replay_ref",
            "whitebox_ref",
        ],
        "execution_plane_enum": ["runtime", "shadow", "sandbox"],
        "notes": "execution_plane 标明 trial 运行在何种平面；trial_id 由 orchestrator 分配；trial_mode 与 env 对齐。",
    }


def _acceptance_matrix() -> List[Dict[str, Any]]:
    """Flatten acceptance-oriented view (same facts as trial_matrix, checks explicit)."""
    out: List[Dict[str, Any]] = []
    for row in _trial_matrix():
        out.append(
            {
                "trial_name": row["trial_name"],
                "capability": row["capability"],
                "acceptance_checks": row["acceptance_checks"],
                "abort_conditions": row["abort_conditions"],
                "rollback_actions": row["rollback_actions"],
                "max_allowed_readiness_level_after_pass": row["max_allowed_readiness_level_after_pass"],
            }
        )
    return out


def run_definition(*, out_root: Path) -> Dict[str, Any]:
    trial_matrix = _trial_matrix()
    summary: Dict[str, Any] = {
        "phase": PHASE,
        "definition_id": DEFINITION_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "output_root": str(out_root),
        "constraints": {
            "definition_only": True,
            "no_runtime_wiring": True,
            "no_real_provider_calls": True,
            "no_real_qwen": True,
            "no_real_playback": True,
            "no_real_tts_execution": True,
            "no_mainline_code_change_in_this_phase": True,
            "no_default_provider_policy_change": True,
            "no_env_semantics_change": True,
            "trials_mutually_independent": True,
            "all_trial_entry_flags_default_false": True,
        },
        "global_kill_switch": {
            "flag_name": "LUNA_DISABLE_ALL_GUARDED_TRIALS",
            "default_value": False,
            "semantic_when_true": "禁止全部 guarded trial，优先级高于分项 flag",
        },
        "trial_track_count": 3,
        "trial_names": [t["trial_name"] for t in trial_matrix],
        "readiness": {
            "starting_level_all_capabilities": "R2_shadow_ready",
            "target_level_after_acceptance": "R3_guarded_wiring_ready",
            "never_claim_in_this_phase": ["R4_controlled_trial_ready", "R5_production_ready"],
        },
        "verdict": {
            "phase_definition_documentation": "GO",
            "guarded_wiring_implementation_next_phase": "CONDITIONAL_GO",
            "real_runtime_activation": "NO_GO",
            "rationale": "Trial scopes, flags, acceptance, rollback, TRW frozen as data artifacts; implementation wiring is out of scope.",
        },
    }

    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "mainline_guarded_trial_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_guarded_trial_matrix.json").write_text(
        json.dumps(trial_matrix, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_guarded_trial_env_flag_matrix.json").write_text(
        json.dumps(_env_flag_matrix(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_guarded_trial_acceptance_matrix.json").write_text(
        json.dumps(_acceptance_matrix(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_guarded_trial_abort_rollback_matrix.json").write_text(
        json.dumps(_abort_rollback_matrix(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_guarded_trial_trw_requirement_matrix.json").write_text(
        json.dumps(_trw_requirement_matrix(), ensure_ascii=False, indent=2), encoding="utf-8"
    )

    notes = [
        f"# {PHASE} — definition artifacts",
        "",
        "Generated JSON only; no runtime connection.",
        "",
        "## Files",
        "",
        "- `mainline_guarded_trial_summary.json`",
        "- `mainline_guarded_trial_matrix.json`",
        "- `mainline_guarded_trial_env_flag_matrix.json`",
        "- `mainline_guarded_trial_acceptance_matrix.json`",
        "- `mainline_guarded_trial_abort_rollback_matrix.json`",
        "- `mainline_guarded_trial_trw_requirement_matrix.json`",
        "",
        "## Priority",
        "",
        "`LUNA_DISABLE_ALL_GUARDED_TRIALS` > capability entry flag > provider/mode flags.",
        "",
    ]
    (out_root / "review_notes.md").write_text("\n".join(notes), encoding="utf-8")

    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit guarded trial definition matrices (Phase-002).")
    ap.add_argument("--output-root", default="", help="Directory to write JSON artifacts")
    args = ap.parse_args()

    repo = _repo_root()
    out = Path(args.output_root) if args.output_root else repo / "logs" / f"mainline_guarded_trial_definition_002_{_utc_tag()}"
    summary = run_definition(out_root=out)
    print(
        json.dumps(
            {"ok": True, "output_root": str(out), "verdict": summary.get("verdict")},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

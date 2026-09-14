# -*- coding: utf-8 -*-
"""System Health Center governance contract (no runtime, no recovery execution).

Phase-SystemHealthCenter-Governance-001
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

PHASE_ID = "SystemHealthCenter-Governance-001"

SUMMARY_SCHEMA = "system_health_center_governance_summary_v0"
MODULE_REPORT_SCHEMA = "system_health_module_health_report_schema_v0"
FAILURE_CLASS_SCHEMA = "system_health_failure_class_enum_v0"
RECOVERY_ACTION_SCHEMA = "system_health_recovery_action_enum_v0"
OPERATING_MODE_SCHEMA = "system_health_operating_mode_enum_v0"
CAPABILITY_MASK_SCHEMA = "system_health_capability_mask_schema_v0"
AGGREGATION_SCHEMA = "system_health_aggregation_policy_v0"
RECOVERY_POLICY_SCHEMA = "system_health_recovery_decision_policy_v0"
SIM_LINK_SCHEMA = "system_health_simulation_lab_link_report_v0"
EXAMPLES_SCHEMA = "system_health_example_module_reports_v0"
BOUNDARY_SCHEMA = "system_health_governance_boundary_report_v0"
SNAPSHOT_SCHEMA = "system_health_snapshot_schema_v0"
PLAN_SCHEMA = "system_health_recovery_action_plan_schema_v0"
WHITEBOX_SCHEMA = "system_health_whitebox_audit_link_policy_v0"
NON_CLAIMS_SCHEMA = "system_health_governance_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "system_health_governance_open_followups_v0"
AUDIT_SCHEMA = "system_health_governance_audit_v0"

MODULE_TYPES = (
    "ocr_runtime",
    "vision_runtime",
    "voice_input",
    "voice_output",
    "stcm",
    "cross_modal",
    "task_chain",
    "scene_delta_executor",
    "model_provider",
    "storage",
    "network",
    "simulation_lab",
)

HEALTH_STATUSES = ("HEALTHY", "WARNING", "DEGRADED", "FAILED", "QUARANTINED", "UNKNOWN")

FAILURE_CLASSES: Tuple[Dict[str, Any], ...] = (
    {"failure_class": "SIGSEGV", "description": "Segmentation fault / exit 139", "example_source_module": "ocr_runtime", "severity_default": "critical", "retry_allowed": True, "quarantine_candidate": True, "requires_simulation_profile": "crash_recovery", "requires_audit": True},
    {"failure_class": "OOM", "description": "Out of memory / memory pressure", "example_source_module": "ocr_runtime", "severity_default": "critical", "retry_allowed": False, "quarantine_candidate": True, "requires_simulation_profile": "low_memory_4gb", "requires_audit": True},
    {"failure_class": "TIMEOUT", "description": "Operation timed out", "example_source_module": "ocr_runtime", "severity_default": "high", "retry_allowed": True, "quarantine_candidate": False, "requires_simulation_profile": None, "requires_audit": True},
    {"failure_class": "DEADLINE_MISS", "description": "STCM deadline exceeded; stale context", "example_source_module": "stcm", "severity_default": "high", "retry_allowed": False, "quarantine_candidate": False, "requires_simulation_profile": "stcm_deadline_stress", "requires_audit": True},
    {"failure_class": "STALE_INPUT", "description": "Input older than freshness window", "example_source_module": "stcm", "severity_default": "medium", "retry_allowed": False, "quarantine_candidate": False, "requires_simulation_profile": "stcm_deadline_stress", "requires_audit": True},
    {"failure_class": "FRAME_DELAY", "description": "Vision frame pipeline latency excessive", "example_source_module": "vision_runtime", "severity_default": "medium", "retry_allowed": True, "quarantine_candidate": False, "requires_simulation_profile": "vision_frame_delay", "requires_audit": True},
    {"failure_class": "PROVIDER_ERROR", "description": "Provider returned error without crash", "example_source_module": "model_provider", "severity_default": "high", "retry_allowed": True, "quarantine_candidate": True, "requires_simulation_profile": None, "requires_audit": True},
    {"failure_class": "MODEL_LOAD_FAILURE", "description": "Model or manifest failed to load", "example_source_module": "model_provider", "severity_default": "critical", "retry_allowed": True, "quarantine_candidate": True, "requires_simulation_profile": None, "requires_audit": True},
    {"failure_class": "EMPTY_RESULT", "description": "Empty output where content expected", "example_source_module": "ocr_runtime", "severity_default": "low", "retry_allowed": True, "quarantine_candidate": False, "requires_simulation_profile": None, "requires_audit": True},
    {"failure_class": "PARTIAL_FAILURE", "description": "Subset of batch/samples failed", "example_source_module": "ocr_runtime", "severity_default": "medium", "retry_allowed": True, "quarantine_candidate": False, "requires_simulation_profile": "crash_recovery", "requires_audit": True},
    {"failure_class": "NETWORK_UNAVAILABLE", "description": "Network fully unavailable", "example_source_module": "network", "severity_default": "high", "retry_allowed": True, "quarantine_candidate": False, "requires_simulation_profile": "offline", "requires_audit": True},
    {"failure_class": "NETWORK_UNSTABLE", "description": "Intermittent network failures", "example_source_module": "network", "severity_default": "medium", "retry_allowed": True, "quarantine_candidate": False, "requires_simulation_profile": "network_unstable", "requires_audit": True},
    {"failure_class": "VOICE_NOTICE_EXPIRED", "description": "Voice notice TTL exceeded", "example_source_module": "voice_output", "severity_default": "medium", "retry_allowed": False, "quarantine_candidate": False, "requires_simulation_profile": "voice_notice_expiry", "requires_audit": True},
    {"failure_class": "AUDIO_OUTPUT_BLOCKED", "description": "Audio output path blocked", "example_source_module": "voice_output", "severity_default": "high", "retry_allowed": False, "quarantine_candidate": False, "requires_simulation_profile": None, "requires_audit": True},
    {"failure_class": "SENSOR_UNAVAILABLE", "description": "Sensor input unavailable", "example_source_module": "vision_runtime", "severity_default": "high", "retry_allowed": True, "quarantine_candidate": False, "requires_simulation_profile": None, "requires_audit": True},
    {"failure_class": "STORAGE_WRITE_FAILURE", "description": "Storage write failed", "example_source_module": "storage", "severity_default": "critical", "retry_allowed": True, "quarantine_candidate": False, "requires_simulation_profile": None, "requires_audit": True},
    {"failure_class": "DATABASE_FAILURE", "description": "Database operation failed", "example_source_module": "storage", "severity_default": "critical", "retry_allowed": True, "quarantine_candidate": False, "requires_simulation_profile": None, "requires_audit": True},
    {"failure_class": "UNKNOWN_FAILURE", "description": "Unclassified failure", "example_source_module": "task_chain", "severity_default": "medium", "retry_allowed": False, "quarantine_candidate": False, "requires_simulation_profile": None, "requires_audit": True},
)

RECOVERY_ACTIONS: Tuple[Dict[str, Any], ...] = (
    {"action_id": "NO_ACTION", "allowed_for_failure_classes": [], "action_committed_default": False, "routing_change_required": False, "requires_gate_check": False, "requires_audit": True, "safe_for_auto_dryrun": True},
    {"action_id": "RETRY", "allowed_for_failure_classes": ["TIMEOUT", "PROVIDER_ERROR", "NETWORK_UNSTABLE"], "action_committed_default": False, "routing_change_required": False, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": True},
    {"action_id": "RETRY_SINGLE_SAMPLE", "allowed_for_failure_classes": ["SIGSEGV", "PARTIAL_FAILURE"], "action_committed_default": False, "routing_change_required": False, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": True},
    {"action_id": "REDUCE_BATCH_SIZE", "allowed_for_failure_classes": ["SIGSEGV", "OOM", "PARTIAL_FAILURE"], "action_committed_default": False, "routing_change_required": False, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": True},
    {"action_id": "FALLBACK_PROVIDER", "allowed_for_failure_classes": ["SIGSEGV", "PROVIDER_ERROR", "MODEL_LOAD_FAILURE"], "action_committed_default": False, "routing_change_required": True, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": False},
    {"action_id": "DISABLE_HEAVY_PROVIDER", "allowed_for_failure_classes": ["SIGSEGV", "OOM"], "action_committed_default": False, "routing_change_required": True, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": False},
    {"action_id": "QUARANTINE_PROVIDER", "allowed_for_failure_classes": ["SIGSEGV", "OOM", "PROVIDER_ERROR"], "action_committed_default": False, "routing_change_required": True, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": False},
    {"action_id": "DROP_EXPIRED_TASK", "allowed_for_failure_classes": ["VOICE_NOTICE_EXPIRED", "DEADLINE_MISS"], "action_committed_default": False, "routing_change_required": False, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": True},
    {"action_id": "REBUILD_CONTEXT", "allowed_for_failure_classes": ["DEADLINE_MISS", "STALE_INPUT"], "action_committed_default": False, "routing_change_required": False, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": True},
    {"action_id": "RESUME_FROM_CACHE", "allowed_for_failure_classes": ["NETWORK_UNAVAILABLE", "PROVIDER_ERROR"], "action_committed_default": False, "routing_change_required": False, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": True},
    {"action_id": "SWITCH_TO_LIGHTWEIGHT_MODE", "allowed_for_failure_classes": ["FRAME_DELAY", "OOM"], "action_committed_default": False, "routing_change_required": True, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": False},
    {"action_id": "LOWER_FRAME_RATE", "allowed_for_failure_classes": ["FRAME_DELAY"], "action_committed_default": False, "routing_change_required": False, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": True},
    {"action_id": "HOLD_TASK", "allowed_for_failure_classes": ["PARTIAL_FAILURE", "UNKNOWN_FAILURE"], "action_committed_default": False, "routing_change_required": False, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": True},
    {"action_id": "SAFE_FREEZE", "allowed_for_failure_classes": ["SIGSEGV", "OOM", "SENSOR_UNAVAILABLE"], "action_committed_default": False, "routing_change_required": True, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": False},
    {"action_id": "MANUAL_REVIEW_REQUIRED", "allowed_for_failure_classes": ["UNKNOWN_FAILURE", "PARTIAL_FAILURE"], "action_committed_default": False, "routing_change_required": False, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": True},
    {"action_id": "MARK_SAMPLE_UNSTABLE", "allowed_for_failure_classes": ["SIGSEGV", "PARTIAL_FAILURE"], "action_committed_default": False, "routing_change_required": False, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": True},
    {"action_id": "RESTART_MODULE", "allowed_for_failure_classes": ["MODEL_LOAD_FAILURE"], "action_committed_default": False, "routing_change_required": True, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": False},
    {"action_id": "RESTART_WORKER", "allowed_for_failure_classes": ["SIGSEGV", "OOM"], "action_committed_default": False, "routing_change_required": True, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": False},
    {"action_id": "ESCALATE_TO_RISK_CENTER", "allowed_for_failure_classes": ["UNKNOWN_FAILURE", "STORAGE_WRITE_FAILURE"], "action_committed_default": False, "routing_change_required": False, "requires_gate_check": True, "requires_audit": True, "safe_for_auto_dryrun": True},
)

OPERATING_MODES: Tuple[Dict[str, Any], ...] = (
    {"mode": "NORMAL", "description": "Full capability within gate policy", "allowed_capabilities": ["ocr_light", "ocr_heavy_gated", "vision_realtime", "voice_io"], "forbidden_capabilities": [], "speech_policy": "normal", "taskchain_policy": "full_schedule", "scene_delta_write_allowed": False, "world_model_write_allowed": False},
    {"mode": "DEGRADED", "description": "Reduced providers and rates", "allowed_capabilities": ["ocr_light", "vision_sampled", "voice_input"], "forbidden_capabilities": ["ocr_heavy_default"], "speech_policy": "cautious_only", "taskchain_policy": "defer_non_critical", "scene_delta_write_allowed": False, "world_model_write_allowed": False},
    {"mode": "MINIMUM_OPERATIONAL", "description": "Safety-critical paths only", "allowed_capabilities": ["vision_sampled", "voice_input"], "forbidden_capabilities": ["ocr_heavy", "navigation"], "speech_policy": "minimal", "taskchain_policy": "safety_only", "scene_delta_write_allowed": False, "world_model_write_allowed": False},
    {"mode": "SAFE_FREEZE", "description": "Halt new work; hold state", "allowed_capabilities": [], "forbidden_capabilities": ["ocr_submission", "navigation", "scene_delta_write"], "speech_policy": "silent", "taskchain_policy": "freeze", "scene_delta_write_allowed": False, "world_model_write_allowed": False},
    {"mode": "RECOVERY_PENDING", "description": "Awaiting recovery plan approval", "allowed_capabilities": ["diagnostics"], "forbidden_capabilities": ["ocr_heavy", "navigation"], "speech_policy": "status_only", "taskchain_policy": "hold", "scene_delta_write_allowed": False, "world_model_write_allowed": False},
    {"mode": "RECOVERY_TESTING", "description": "Dry-run recovery under simulation", "allowed_capabilities": ["simulation_lab", "readonly_metrics"], "forbidden_capabilities": ["production_write"], "speech_policy": "dry_run", "taskchain_policy": "test_only", "scene_delta_write_allowed": False, "world_model_write_allowed": False},
)


def build_summary() -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "governance_scope": "contract_only",
        "runtime_execution": False,
        "module_restart_invoked": False,
        "recovery_action_committed": False,
        "routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "system_health_center_role": "runtime_health_governance_layer",
        "module_local_decision_allowed": False,
        "centralized_recovery_decision_required": True,
    }


def build_module_health_report_schema() -> Dict[str, Any]:
    return {
        "schema_version": MODULE_REPORT_SCHEMA,
        "required_fields": [
            "report_id",
            "module_id",
            "module_type",
            "provider_id",
            "timestamp",
            "heartbeat_status",
            "health_status",
            "last_success_at",
            "last_failure_at",
            "last_error",
            "latency_ms",
            "timeout_count",
            "crash_count",
            "retry_count",
            "resource_snapshot",
            "recommended_local_action",
            "confidence",
            "evidence_refs",
            "fact_status",
        ],
        "module_type_enum": list(MODULE_TYPES),
        "health_status_enum": list(HEALTH_STATUSES),
        "last_error_fields": [
            "error_code",
            "exit_code",
            "signal",
            "exception_type",
            "message",
            "failed_sample_ref",
            "provider_ref",
        ],
        "fact_status_default": "not_fact",
        "module_local_decision_note": "recommended_local_action is advisory only; Health Center decides system mode.",
    }


def build_failure_class_enum() -> Dict[str, Any]:
    return {"schema_version": FAILURE_CLASS_SCHEMA, "failure_class_count": len(FAILURE_CLASSES), "failure_classes": list(FAILURE_CLASSES)}


def build_recovery_action_enum() -> Dict[str, Any]:
    return {"schema_version": RECOVERY_ACTION_SCHEMA, "action_count": len(RECOVERY_ACTIONS), "actions": list(RECOVERY_ACTIONS)}


def build_operating_mode_enum() -> Dict[str, Any]:
    return {"schema_version": OPERATING_MODE_SCHEMA, "mode_count": len(OPERATING_MODES), "modes": list(OPERATING_MODES)}


def build_capability_mask_schema() -> Dict[str, Any]:
    return {
        "schema_version": CAPABILITY_MASK_SCHEMA,
        "description": "Health Center output consumed by TaskChain / ModelController / STCM / Voice / OCR schedulers.",
        "required_top_level_fields": ["capability_mask_id", "operating_mode", "fact_status", "write_allowed"],
        "example": {
            "capability_mask_id": "mask_example_degraded_v0",
            "operating_mode": "DEGRADED",
            "fact_status": "not_fact",
            "write_allowed": False,
            "ocr": {
                "heavy_provider_allowed": False,
                "lightweight_provider_allowed": True,
                "submission_allowed": True,
                "write_allowed": False,
            },
            "vision": {
                "realtime_allowed": True,
                "heavy_detection_allowed": False,
                "frame_sampling_allowed": True,
            },
            "voice": {"input_allowed": True, "output_allowed": True, "drop_expired_notice": True},
            "scene_delta": {"candidate_allowed": True, "write_allowed": False},
            "world_model": {"write_allowed": False},
            "navigation": {"decision_allowed": False},
        },
        "defaults": {
            "scene_delta_write_allowed": False,
            "world_model_write_allowed": False,
            "navigation_decision_allowed": False,
        },
        "note": "Mask is arbitration result, not module self-declaration.",
    }


def build_aggregation_policy() -> Dict[str, Any]:
    return {
        "schema_version": AGGREGATION_SCHEMA,
        "rules": [
            "single_module_FAILED_does_not_always_imply_SAFE_FREEZE",
            "ocr_heavy_FAILED_may_downgrade_to_lightweight_provider",
            "vision_realtime_FAILED_may_enter_MINIMUM_OPERATIONAL_or_SAFE_FREEZE",
            "voice_output_expired_must_not_replay_stale_notice",
            "stcm_DEADLINE_MISS_must_drop_or_rebuild_stale_context",
            "scene_delta_executor_failure_must_not_break_no_write_boundary",
            "multiple_DEGRADED_modules_may_upgrade_system_operating_mode",
            "QUARANTINED_provider_must_not_be_scheduled",
        ],
        "health_center_vs_gate": {
            "health_center": "decides_if_capability_usable",
            "gate": "decides_if_output_write_navigation_allowed",
        },
    }


def build_recovery_decision_policy() -> Dict[str, Any]:
    return {
        "schema_version": RECOVERY_POLICY_SCHEMA,
        "policies": {
            "paddleocr_sigsegv": {
                "failure_class": "SIGSEGV",
                "module_id": "paddleocr_heavy",
                "first_action": "RETRY_SINGLE_SAMPLE",
                "second_action": "REDUCE_BATCH_SIZE",
                "fallback": "FALLBACK_PROVIDER",
                "repeated_failure": "QUARANTINE_PROVIDER",
            },
            "voice_notice_expired": {
                "failure_class": "VOICE_NOTICE_EXPIRED",
                "low_priority": "DROP_EXPIRED_TASK",
                "high_priority": "REBUILD_CONTEXT",
            },
            "vision_frame_delay": {
                "failure_class": "FRAME_DELAY",
                "actions": ["LOWER_FRAME_RATE", "SWITCH_TO_LIGHTWEIGHT_MODE"],
                "if_safety_affected": "SAFE_FREEZE",
            },
        },
        "general_rules": [
            "retry_when_transient_and_gate_allows",
            "fallback_when_provider_specific_failure",
            "quarantine_after_repeated_sigsegv_or_oom",
            "safe_freeze_when_safety_sensor_or_navigation_at_risk",
            "manual_review_when_unknown_or_high_impact",
            "resume_from_cache_when_network_restored",
            "drop_expired_task_for_stale_voice_or_stcm",
            "lower_frame_rate_for_vision_backpressure",
            "disable_heavy_provider_under_memory_pressure",
        ],
    }


def build_simulation_lab_link_report() -> Dict[str, Any]:
    profiles = [
        ("crash_recovery", ["SIGSEGV", "PARTIAL_FAILURE"], "provider crash / batch recovery"),
        ("low_memory_4gb", ["OOM"], "memory pressure"),
        ("low_memory_2gb", ["OOM"], "severe memory pressure"),
        ("stcm_deadline_stress", ["DEADLINE_MISS", "STALE_INPUT"], "deadline / stale input"),
        ("voice_notice_expiry", ["VOICE_NOTICE_EXPIRED"], "expired voice notice"),
        ("vision_frame_delay", ["FRAME_DELAY"], "frame pipeline delay"),
        ("network_unstable", ["NETWORK_UNSTABLE"], "intermittent network"),
        ("offline", ["NETWORK_UNAVAILABLE"], "offline"),
        ("long_run_1h", ["TIMEOUT", "PARTIAL_FAILURE"], "stability / drift"),
        ("long_run_4h", ["TIMEOUT", "PARTIAL_FAILURE"], "long-run leak / drift"),
    ]
    rows = [
        {
            "simulation_profile_id": pid,
            "failure_classes": fcs,
            "purpose": purpose,
            "simulation_lab_role": "inject_stress_and_fault",
            "health_center_role": "classify_and_decide_recovery",
            "benchmark_collector_role": "record_metrics",
            "whitebox_role": "observe_and_replay_later",
        }
        for pid, fcs, purpose in profiles
    ]
    return {
        "schema_version": SIM_LINK_SCHEMA,
        "row_count": len(rows),
        "profiles": rows,
        "interpretation": {
            "simulation_lab": "manufactures_faults_and_pressure",
            "system_health_center": "detects_classifies_decides_isolation_degradation",
            "benchmark_collector": "records_outcomes",
            "whitebox": "future_observation_and_replay",
        },
    }


def _example_report(
    report_id: str,
    module_id: str,
    module_type: str,
    health_status: str,
    last_error: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "report_id": report_id,
        "module_id": module_id,
        "module_type": module_type,
        "provider_id": module_id,
        "timestamp": "2026-05-19T00:00:00Z",
        "heartbeat_status": "stale" if health_status != "HEALTHY" else "ok",
        "health_status": health_status,
        "last_success_at": "2026-05-19T00:00:00Z",
        "last_failure_at": "2026-05-19T00:00:01Z",
        "last_error": last_error,
        "latency_ms": 1200,
        "timeout_count": 1 if "TIMEOUT" in str(last_error) else 0,
        "crash_count": 1 if last_error.get("exit_code") == 139 else 0,
        "retry_count": 0,
        "resource_snapshot": {"rss_mb": 512},
        "recommended_local_action": "retry_suggested",
        "confidence": 0.7,
        "evidence_refs": ["stub://evidence/" + report_id],
        "fact_status": "not_fact",
    }


def build_example_module_reports() -> Dict[str, Any]:
    examples = [
        {
            "example_id": "ex_paddleocr_sigsegv",
            "module_health_report": _example_report(
                "rpt_paddleocr_001",
                "paddleocr_heavy",
                "ocr_runtime",
                "FAILED",
                {"error_code": "SIGSEGV", "exit_code": 139, "signal": "SIGSEGV", "message": "child exit 139", "failed_sample_ref": "sample_042"},
            ),
            "expected_failure_class": "SIGSEGV",
            "expected_recovery_action": "RETRY_SINGLE_SAMPLE",
            "expected_operating_mode": "DEGRADED",
            "expected_capability_mask_delta": {"ocr.heavy_provider_allowed": False},
        },
        {
            "example_id": "ex_rapidocr_timeout",
            "module_health_report": _example_report(
                "rpt_rapidocr_001",
                "rapidocr_light",
                "ocr_runtime",
                "DEGRADED",
                {"error_code": "TIMEOUT", "message": "request timed out"},
            ),
            "expected_failure_class": "TIMEOUT",
            "expected_recovery_action": "RETRY",
            "expected_operating_mode": "DEGRADED",
            "expected_capability_mask_delta": {},
        },
        {
            "example_id": "ex_vision_frame_delay",
            "module_health_report": _example_report(
                "rpt_vision_001",
                "vision_realtime",
                "vision_runtime",
                "DEGRADED",
                {"error_code": "FRAME_DELAY", "message": "frame latency > threshold"},
            ),
            "expected_failure_class": "FRAME_DELAY",
            "expected_recovery_action": "LOWER_FRAME_RATE",
            "expected_operating_mode": "MINIMUM_OPERATIONAL",
            "expected_capability_mask_delta": {"vision.heavy_detection_allowed": False},
        },
        {
            "example_id": "ex_voice_notice_expired",
            "module_health_report": _example_report(
                "rpt_voice_001",
                "voice_output",
                "voice_output",
                "WARNING",
                {"error_code": "VOICE_NOTICE_EXPIRED", "message": "notice TTL exceeded"},
            ),
            "expected_failure_class": "VOICE_NOTICE_EXPIRED",
            "expected_recovery_action": "DROP_EXPIRED_TASK",
            "expected_operating_mode": "DEGRADED",
            "expected_capability_mask_delta": {"voice.drop_expired_notice": True},
        },
        {
            "example_id": "ex_stcm_deadline_miss",
            "module_health_report": _example_report(
                "rpt_stcm_001",
                "stcm",
                "stcm",
                "DEGRADED",
                {"error_code": "DEADLINE_MISS", "message": "context stale"},
            ),
            "expected_failure_class": "DEADLINE_MISS",
            "expected_recovery_action": "REBUILD_CONTEXT",
            "expected_operating_mode": "DEGRADED",
            "expected_capability_mask_delta": {},
        },
        {
            "example_id": "ex_low_memory_warning",
            "module_health_report": _example_report(
                "rpt_ocr_mem_001",
                "paddleocr_heavy",
                "ocr_runtime",
                "WARNING",
                {"error_code": "OOM", "message": "rss approaching limit"},
            ),
            "expected_failure_class": "OOM",
            "expected_recovery_action": "DISABLE_HEAVY_PROVIDER",
            "expected_operating_mode": "DEGRADED",
            "expected_capability_mask_delta": {"ocr.heavy_provider_allowed": False},
        },
    ]
    return {"schema_version": EXAMPLES_SCHEMA, "example_count": len(examples), "examples": examples}


def build_governance_boundary_report() -> Dict[str, Any]:
    return {
        "schema_version": BOUNDARY_SCHEMA,
        "health_center_does_not_run_ocr": True,
        "health_center_does_not_run_vision": True,
        "health_center_does_not_run_voice": True,
        "health_center_does_not_modify_routing_directly": True,
        "health_center_does_not_write_facts": True,
        "health_center_does_not_write_scene_delta": True,
        "health_center_does_not_write_world_model": True,
        "health_center_does_not_navigate": True,
        "health_center_does_not_replace_gate": True,
        "health_center_does_not_replace_risk_center": True,
        "health_center_does_not_replace_taskchain": True,
        "health_center_does_not_replace_stcm": True,
        "outputs_only": [
            "health_snapshot",
            "recovery_action_plan",
            "capability_mask",
        ],
    }


def build_snapshot_schema() -> Dict[str, Any]:
    return {
        "schema_version": SNAPSHOT_SCHEMA,
        "required_fields": [
            "snapshot_id",
            "timestamp",
            "operating_mode",
            "global_health_status",
            "module_status_matrix_ref",
            "failure_classification_ref",
            "recovery_action_plan_ref",
            "capability_mask_ref",
            "simulation_profile_id",
            "audit_ref",
            "whitebox_trace_ref",
            "fact_status",
            "write_allowed",
        ],
        "fact_status_default": "not_fact",
        "write_allowed_default": False,
    }


def build_recovery_action_plan_schema() -> Dict[str, Any]:
    return {
        "schema_version": PLAN_SCHEMA,
        "required_fields": [
            "plan_id",
            "trigger_failure_class",
            "affected_modules",
            "recommended_actions",
            "action_commit_status",
            "action_requires_gate",
            "action_requires_manual_review",
            "capability_mask_delta",
            "expected_recovery_check",
            "rollback_plan",
            "audit_refs",
        ],
        "action_commit_status_default": "planned_only",
        "action_commit_status_allowed": ["planned_only", "committed"],
        "governance_note": "This phase allows planned_only only; committed forbidden.",
    }


def build_whitebox_audit_link_policy() -> Dict[str, Any]:
    return {
        "schema_version": WHITEBOX_SCHEMA,
        "rules": [
            "every_failure_classification_must_write_audit",
            "every_recovery_plan_must_be_traceable",
            "every_capability_mask_change_must_be_replayable",
            "whitebox_displays_module_health_mode_recovery_plan_mask",
            "ui_not_implemented_in_this_phase",
        ],
        "audit_refs_required": True,
        "replay_fields": ["operating_mode", "capability_mask_id", "recovery_action_plan_ref"],
    }


def build_non_claims_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "not_runtime_health_center": True,
        "no_real_crash_recovery": True,
        "no_module_restart": True,
        "no_real_module_detection": True,
        "no_provider_routing_change": True,
        "no_production_stability_claim": True,
        "no_long_run_pass_claim": True,
        "no_crash_recovery_verified_claim": True,
        "not_integrated_to_mainline": True,
    }


def build_open_followups() -> Dict[str, Any]:
    items = [
        "SystemHealthCenter-DryRun-001",
        "ModuleHealthReport adapters for OCR / Vision / Voice",
        "PaddleOCR SIGSEGV fixture",
        "Vision frame delay fixture",
        "Voice expiry fixture",
        "STCM deadline miss fixture",
        "capability_mask consumer in TaskChain",
        "health snapshot whitebox viewer",
        "recovery action dry-run",
        "quarantine provider policy",
        "benchmark collector health metrics",
        "runtime integration gate",
    ]
    return {"schema_version": FOLLOWUPS_SCHEMA, "items": items, "item_count": len(items)}


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "system_health_governance_executed": True,
        "governance_only": True,
        "runtime_execution": False,
        "module_restart_invoked": False,
        "recovery_action_committed": False,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "voice_runtime_invoked": False,
        "stcm_runtime_invoked": False,
        "taskchain_modified": False,
        "routing_changed": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
    }


def run_system_health_center_governance_v0() -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    summary = build_summary()
    module_schema = build_module_health_report_schema()
    failure_enum = build_failure_class_enum()
    recovery_enum = build_recovery_action_enum()
    operating_enum = build_operating_mode_enum()
    mask_schema = build_capability_mask_schema()
    aggregation = build_aggregation_policy()
    recovery_policy = build_recovery_decision_policy()
    sim_link = build_simulation_lab_link_report()
    examples = build_example_module_reports()
    boundary = build_governance_boundary_report()
    snapshot_schema = build_snapshot_schema()
    plan_schema = build_recovery_action_plan_schema()
    whitebox = build_whitebox_audit_link_policy()
    non_claims = build_non_claims_report()
    followups = build_open_followups()
    audit = build_audit()

    required_fc = {"SIGSEGV", "OOM", "TIMEOUT", "DEADLINE_MISS", "VOICE_NOTICE_EXPIRED", "FRAME_DELAY"}
    fc_set = {x["failure_class"] for x in failure_enum["failure_classes"]}
    if not required_fc.issubset(fc_set):
        errs.append("failure_class_enum_incomplete")

    required_actions = {"RETRY", "REDUCE_BATCH_SIZE", "FALLBACK_PROVIDER", "QUARANTINE_PROVIDER", "SAFE_FREEZE"}
    act_set = {x["action_id"] for x in recovery_enum["actions"]}
    if not required_actions.issubset(act_set):
        errs.append("recovery_action_enum_incomplete")

    required_modes = {"NORMAL", "DEGRADED", "MINIMUM_OPERATIONAL", "SAFE_FREEZE", "RECOVERY_PENDING"}
    mode_set = {x["mode"] for x in operating_enum["modes"]}
    if not required_modes.issubset(mode_set):
        errs.append("operating_mode_enum_incomplete")

    if examples.get("example_count", 0) < 6:
        errs.append("example_count_lt_6")

    if "paddleocr_sigsegv" not in recovery_policy.get("policies", {}):
        errs.append("missing_paddleocr_sigsegv_policy")

    crash_row = next((p for p in sim_link["profiles"] if p["simulation_profile_id"] == "crash_recovery"), None)
    if not crash_row or "SIGSEGV" not in crash_row.get("failure_classes", []):
        errs.append("crash_recovery_sigsegv_mapping_missing")

    return (
        summary,
        module_schema,
        failure_enum,
        recovery_enum,
        operating_enum,
        mask_schema,
        aggregation,
        recovery_policy,
        sim_link,
        examples,
        boundary,
        snapshot_schema,
        plan_schema,
        whitebox,
        non_claims,
        followups,
        audit,
        errs,
    )

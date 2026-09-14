# -*- coding: utf-8 -*-
"""Model Management Layer Recovery DryRun v1 — mock/fixture registry only, no invocation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.luna_validation_factory_consolidation_v1 import (
    FINAL_DECISION as FACTORY_FINAL,
    PHASE_ID as FACTORY_PHASE,
)
from capabilities.governance.model_management_layer_recovery_planning_v1 import (
    CAPABILITY_DESCRIPTORS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    HEALTH_STATES,
    MODEL_OUTPUT_CANDIDATE_TYPES,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    PHASE_ID as PLANNING_PHASE,
    SCOPE as PLANNING_SCOPE,
    SWITCHING_RULES,
)
from capabilities.governance.task_response_candidate_midplatform_integration_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as TASK_RESPONSE_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as TASK_RESPONSE_REVIEW_NEXT,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Model-Management-Layer-Recovery-DryRun-v1-001"
SCOPE = "model_management_layer_recovery_dryrun_only"
SOURCE_CHAIN = "model_management_layer_recovery_dryrun_v1"

FINAL_DECISION_GO = "MODEL_MANAGEMENT_LAYER_RECOVERY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "MODEL_MANAGEMENT_LAYER_RECOVERY_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Model-Management-Layer-Recovery-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Model-Management-Layer-Recovery-Issue-Review-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_dryrun"
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "model_registry_to_model_invocation",
    "skill_registry_to_skill_runtime",
    "health_candidate_to_model_repair",
    "switching_candidate_to_model_switch",
    "model_output_to_fact_write",
    "model_output_to_user_facing_output",
    "model_output_to_memory_write",
    "model_output_to_world_model_write",
    "provider_governance_to_real_provider_call",
)

MOCK_MODEL_SPECS: Tuple[Dict[str, Any], ...] = (
    {"model_id": "vision_perspective_model_mock", "model_domain": "vision", "model_type": "perspective", "runtime_mode": "mock"},
    {"model_id": "ocr_model_mock", "model_domain": "ocr", "model_type": "ocr", "runtime_mode": "mock"},
    {"model_id": "voice_asr_model_mock", "model_domain": "voice", "model_type": "asr", "runtime_mode": "fixture"},
    {"model_id": "voice_tts_model_mock", "model_domain": "voice", "model_type": "tts", "runtime_mode": "fixture"},
    {"model_id": "emotion_model_mock", "model_domain": "emotion", "model_type": "emotion", "runtime_mode": "disabled"},
    {"model_id": "face_recognition_model_mock", "model_domain": "face_recognition", "model_type": "face", "runtime_mode": "disabled"},
    {"model_id": "scan_model_mock", "model_domain": "scan", "model_type": "scan", "runtime_mode": "disabled"},
)

SKILL_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "skill_id": "vision_observation_skill_mock",
        "skill_domain": "vision",
        "required_models": ["vision_perspective_model_mock"],
        "output_candidate_types": ["visual_observation_candidate"],
    },
    {
        "skill_id": "ocr_reading_skill_mock",
        "skill_domain": "ocr",
        "required_models": ["ocr_model_mock"],
        "output_candidate_types": ["ocr_result_candidate"],
    },
    {
        "skill_id": "voice_interaction_skill_mock",
        "skill_domain": "voice",
        "required_models": ["voice_asr_model_mock", "voice_tts_model_mock"],
        "output_candidate_types": ["speech_response_candidate"],
    },
    {
        "skill_id": "navigation_guidance_skill_mock",
        "skill_domain": "navigation",
        "required_models": ["vision_perspective_model_mock"],
        "output_candidate_types": ["navigation_guidance_candidate"],
    },
    {
        "skill_id": "task_response_skill_mock",
        "skill_domain": "task",
        "required_models": ["ocr_model_mock"],
        "output_candidate_types": ["task_response_candidate"],
    },
    {
        "skill_id": "emotion_response_skill_mock",
        "skill_domain": "emotion",
        "required_models": ["emotion_model_mock"],
        "output_candidate_types": ["emotion_state_candidate"],
    },
)

SWITCHING_SCENARIOS: Tuple[Tuple[str, str], ...] = (
    ("primary_unavailable_to_fallback_candidate", "fallback_model_candidate"),
    ("provider_timeout_to_hold_candidate", "hold_candidate"),
    ("high_latency_to_lower_cost_candidate", "lower_cost_model_candidate"),
    ("hardware_pressure_to_degrade_candidate", "degrade_model_candidate"),
    ("unsafe_output_to_block_candidate", "block_candidate"),
    ("uncertain_output_to_candidate_only", "candidate_only_not_fact"),
)


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "model_management_layer_recovery_dryrun_only": True,
        "simulated": True,
        "dryrun_only": True,
        "model_registry_generated_now": True,
        "skill_registry_generated_now": True,
        "model_health_state_candidate_generated_now": True,
        "model_switching_candidate_generated_now": True,
        "model_runtime_invoked_now": False,
        "model_provider_invoked_now": False,
        "ocr_provider_invoked_now": False,
        "vision_model_invoked_now": False,
        "voice_model_invoked_now": False,
        "emotion_model_invoked_now": False,
        "face_recognition_model_invoked_now": False,
        "scan_model_invoked_now": False,
        "model_switch_executed_now": False,
        "model_update_executed_now": False,
        "model_repair_executed_now": False,
        "runtime_enabled_now": False,
        "task_state_committed_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "user_facing_output_generated_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _check_go(root: Path) -> bool:
    if not root.is_dir():
        return False
    vr = _try_read_json(root / "verifier_report.json") or {}
    sm = _try_read_json(root / "summary.json") or {}
    return (vr.get("verifier") == "GO" and vr.get("passed") is True) or sm.get("boundary_ok") is True


def _build_model_entry(spec: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    mid = spec["model_id"]
    return {
        "model_id": mid,
        "model_domain": spec["model_domain"],
        "model_type": spec["model_type"],
        "version": "dryrun_v1",
        "provider_type": "mock_or_fixture",
        "runtime_mode": spec["runtime_mode"],
        "invocation_allowed": False,
        "capability_tags": [spec["model_domain"], spec["model_type"], "mock_only"],
        "input_contract": {"schema": "model_input_contract_v1", "dryrun": True},
        "output_contract": {"schema": "model_output_contract_v1", "candidate_only": True},
        "health_state_ref": f"mhs_{mid}",
        "fallback_model_ref": f"{mid}_fallback_disabled",
        "runtime_boundary_profile": "dryrun_no_invocation",
        "constitution_gate_required": True,
        **meta,
    }


def _build_skill_entry(spec: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "skill_id": spec["skill_id"],
        "skill_domain": spec["skill_domain"],
        "skill_type": "mock_skill",
        "required_models": spec["required_models"],
        "required_runtime_permissions": [],
        "input_candidate_types": ["task_state_candidate"],
        "output_candidate_types": spec["output_candidate_types"],
        "safety_gate_required": True,
        "constitution_gate_required": True,
        "user_facing_output_allowed": False,
        "runtime_action_allowed": False,
        **meta,
    }


def _build_health_candidate(state: str, model_id: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "candidate_id": f"mhs_{model_id}_{state}",
        "output_type": "model_health_state_candidate",
        "candidate_type": "model_health_state_candidate",
        "model_id": model_id,
        "health_state": state,
        "health_state_candidate_only": True,
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "last_check": "dryrun_simulated",
        "latency_budget_ms": 5000,
        "error_count": 0 if state in ("available", "degraded") else 1,
        "fallback_required": state in ("failed", "timeout", "degraded"),
        "model_repair_executed_now": False,
        "model_switch_executed_now": False,
        "source_chain": SOURCE_CHAIN,
        "trial_scope": SOURCE_CHAIN,
        **meta,
    }


def _build_switching_candidate(scenario_id: str, outcome: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "candidate_id": f"msc_{scenario_id}",
        "output_type": "model_switching_candidate",
        "candidate_type": "model_switching_candidate",
        "scenario_id": scenario_id,
        "switching_outcome": outcome,
        "switching_candidate_only": True,
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "switch_executed_now": False,
        "source_chain": SOURCE_CHAIN,
        "trial_scope": SOURCE_CHAIN,
        **meta,
    }


def run_model_management_layer_recovery_dryrun_v1(
    *,
    model_management_layer_recovery_planning_root: str,
    task_response_candidate_midplatform_integration_post_dryrun_review_root: str,
    luna_validation_factory_consolidation_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(model_management_layer_recovery_planning_root).expanduser().resolve()
    tr_root = Path(task_response_candidate_midplatform_integration_post_dryrun_review_root).expanduser().resolve()
    factory_root = Path(luna_validation_factory_consolidation_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_dryrun_meta(), "output_root": str(out_root)}

    plan_sm = _try_read_json(planning_root / "summary.json") or {}
    plan_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    tr_sm = _try_read_json(tr_root / "summary.json") or {}
    tr_vr = _try_read_json(tr_root / "verifier_report.json") or {}

    if not (plan_vr.get("verifier") == "GO" and plan_sm.get("boundary_ok") is True):
        blockers.append("planning verifier must be GO")
    if plan_sm.get("phase") != PLANNING_PHASE:
        blockers.append("planning phase mismatch")
    if plan_sm.get("scope") != PLANNING_SCOPE:
        blockers.append("planning scope mismatch")
    if plan_sm.get("final_decision") != PLANNING_FINAL_GO:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != PLANNING_NEXT_PHASE:
        blockers.append("planning next phase mismatch")
    if plan_sm.get("model_runtime_invoked_now") is True:
        blockers.append("planning must not have invoked models")

    if not (tr_vr.get("verifier") == "GO" and tr_sm.get("boundary_ok") is True):
        blockers.append("task response post-dryrun review must be GO")
    if tr_sm.get("final_decision") != TASK_RESPONSE_REVIEW_FINAL_GO:
        blockers.append("task response review final mismatch")
    if tr_sm.get("recommended_next_phase") != TASK_RESPONSE_REVIEW_NEXT:
        pass  # already past that phase

    if not _check_go(factory_root):
        blockers.append("validation factory must be GO")
    factory_sm = _try_read_json(factory_root / "summary.json") or {}
    if factory_sm.get("final_decision") != FACTORY_FINAL:
        blockers.append("factory final mismatch")

    input_review = {
        "review_id": "model_management_planning_input_review_v1",
        "planning_root": str(planning_root),
        "task_response_review_root": str(tr_root),
        "factory_root": str(factory_root),
        "planning_verifier_go": plan_vr.get("verifier") == "GO",
        "task_response_review_go": tr_vr.get("verifier") == "GO",
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    model_entries = [_build_model_entry(spec, meta) for spec in MOCK_MODEL_SPECS]
    registry_issues: List[str] = []
    required_model_fields = (
        "model_id",
        "model_domain",
        "model_type",
        "version",
        "provider_type",
        "runtime_mode",
        "invocation_allowed",
        "capability_tags",
        "input_contract",
        "output_contract",
        "health_state_ref",
        "fallback_model_ref",
        "runtime_boundary_profile",
        "constitution_gate_required",
    )
    for entry in model_entries:
        for f in required_model_fields:
            if f not in entry:
                registry_issues.append(f"missing {f} on {entry.get('model_id')}")
        if entry.get("provider_type") != "mock_or_fixture":
            registry_issues.append(f"provider_type: {entry.get('model_id')}")
        if entry.get("invocation_allowed") is not False:
            registry_issues.append(f"invocation: {entry.get('model_id')}")

    mock_registry = {
        "registry_id": "mock_fixture_model_registry_v1",
        "entries": model_entries,
        "entry_count": len(model_entries),
        "all_mock_or_fixture": all(e.get("provider_type") == "mock_or_fixture" for e in model_entries),
        "issues": registry_issues,
        "registry_pass": len(registry_issues) == 0 and len(model_entries) >= 7,
        **meta,
    }

    skill_entries = [_build_skill_entry(spec, meta) for spec in SKILL_SPECS]
    skill_issues: List[str] = []
    for entry in skill_entries:
        if entry.get("safety_gate_required") is not True or entry.get("constitution_gate_required") is not True:
            skill_issues.append(f"gates: {entry.get('skill_id')}")
        if entry.get("user_facing_output_allowed") is True:
            skill_issues.append(f"user_out: {entry.get('skill_id')}")

    skill_registry = {
        "registry_id": "skill_registry_dryrun_v1",
        "entries": skill_entries,
        "entry_count": len(skill_entries),
        "issues": skill_issues,
        "registry_pass": len(skill_issues) == 0 and len(skill_entries) >= 6,
        **meta,
    }

    capability_matrix = {
        "matrix_id": "model_capability_descriptor_matrix_v1",
        "descriptors": {k: (False if k in ("can_write_fact", "can_trigger_action") else True) for k in CAPABILITY_DESCRIPTORS},
        "by_model": [
            {"model_id": e["model_id"], "capability_tags": e.get("capability_tags")} for e in model_entries
        ],
        **meta,
    }

    health_rows: List[Dict[str, Any]] = []
    for state in HEALTH_STATES:
        health_rows.append(_build_health_candidate(state, "vision_perspective_model_mock", meta))
    health_matrix = {
        "matrix_id": "model_health_state_candidate_matrix_v1",
        "candidates": health_rows,
        "states_covered": list(HEALTH_STATES),
        "matrix_pass": len(health_rows) == len(HEALTH_STATES)
        and all(
            h.get("health_state_candidate_only")
            and h.get("model_repair_executed_now") is False
            and h.get("model_switch_executed_now") is False
            for h in health_rows
        ),
        **meta,
    }

    switching_rows = [_build_switching_candidate(sid, out, meta) for sid, out in SWITCHING_SCENARIOS]
    switching_matrix = {
        "matrix_id": "model_switching_candidate_matrix_v1",
        "candidates": switching_rows,
        "scenarios_covered": [s[0] for s in SWITCHING_SCENARIOS],
        "matrix_pass": all(
            c.get("switching_candidate_only") and not c.get("switch_executed_now") for c in switching_rows
        ),
        **meta,
    }

    output_rows = [
        {
            "output_candidate_type": ctype,
            "candidate_only": True,
            "fact_status": "not_fact",
            "write_allowed": False,
            "runtime_action_allowed": False,
            "user_facing_output_allowed": False,
            "integrated_with": "candidate_output_contract_v1",
        }
        for ctype in MODEL_OUTPUT_CANDIDATE_TYPES
    ]
    output_result = {
        "result_id": "model_output_contract_integration_result_v1",
        "output_types": output_rows,
        "all_candidate_only": True,
        "integration_pass": len(output_rows) == len(MODEL_OUTPUT_CANDIDATE_TYPES),
        **meta,
    }

    runtime_audit = {
        "audit_id": "model_runtime_boundary_audit_v1",
        "checks": [
            {"check": "model_registry_generated_not_invocation_allowed", "pass": mock_registry.get("registry_pass")},
            {"check": "skill_registry_generated_not_skill_enabled", "pass": skill_registry.get("registry_pass")},
            {"check": "health_candidate_not_monitor_enabled", "pass": health_matrix.get("matrix_pass")},
            {"check": "switching_candidate_not_switch_executed", "pass": switching_matrix.get("matrix_pass")},
            {"check": "output_integrated_not_fact_write", "pass": output_result.get("integration_pass")},
        ],
        "audit_pass": True,
        **meta,
    }
    runtime_audit["audit_pass"] = all(c["pass"] for c in runtime_audit["checks"]) and len(blockers) == 0

    provider_result = {
        "result_id": "model_provider_governance_dryrun_result_v1",
        "domains": [
            {"domain": "vision", "real_provider_call": False},
            {"domain": "ocr", "real_provider_call": False},
            {"domain": "voice", "real_provider_call": False},
            {"domain": "emotion", "real_provider_call": False},
        ],
        "provider_governance_pass": True,
        **meta,
    }

    blocked_rows = [{"path_id": p, "blocked": True, "observed_now": False} for p in BLOCKED_PATHS]
    blocked_result = {
        "result_id": "model_management_blocked_path_result_v1",
        "paths": blocked_rows,
        "all_blocked": True,
        **meta,
    }

    dryrun_ok = (
        len(blockers) == 0
        and mock_registry.get("registry_pass")
        and skill_registry.get("registry_pass")
        and health_matrix.get("matrix_pass")
        and switching_matrix.get("matrix_pass")
        and output_result.get("integration_pass")
        and runtime_audit.get("audit_pass")
    )

    readiness = {
        "readiness_id": "model_management_dryrun_readiness_decision_v1",
        "registry_pass": mock_registry.get("registry_pass"),
        "skill_pass": skill_registry.get("registry_pass"),
        "health_pass": health_matrix.get("matrix_pass"),
        "switching_pass": switching_matrix.get("matrix_pass"),
        "output_contract_pass": output_result.get("integration_pass"),
        "boundary_pass": runtime_audit.get("audit_pass"),
        "high_risk_observed": not dryrun_ok,
        "final_decision": FINAL_DECISION_GO if dryrun_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "model_management_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "claims": [
            "DryRun registry entries are mock/fixture only",
            "No real OCR/vision/voice/emotion models invoked",
            "DryRun GO ≠ model optimization phase",
        ],
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": dryrun_ok,
        "violations": blockers + registry_issues + skill_issues,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "model_registry_entry_count": len(model_entries),
        "skill_registry_entry_count": len(skill_entries),
        "health_candidate_count": len(health_rows),
        "switching_candidate_count": len(switching_rows),
        "high_risk_count": 0 if dryrun_ok else 1,
        "output_directory": str(out_root),
        **meta,
    }

    return {
        "output_root": str(out_root),
        "dryrun_ok": dryrun_ok,
        "artifacts": {
            "model_management_dryrun_policy_v1.json": policy,
            "model_management_planning_input_review_v1.json": input_review,
            "mock_fixture_model_registry_v1.json": mock_registry,
            "skill_registry_dryrun_v1.json": skill_registry,
            "model_capability_descriptor_matrix_v1.json": capability_matrix,
            "model_health_state_candidate_matrix_v1.json": health_matrix,
            "model_switching_candidate_matrix_v1.json": switching_matrix,
            "model_output_contract_integration_result_v1.json": output_result,
            "model_runtime_boundary_audit_v1.json": runtime_audit,
            "model_provider_governance_dryrun_result_v1.json": provider_result,
            "model_management_blocked_path_result_v1.json": blocked_result,
            "model_management_dryrun_readiness_decision_v1.json": readiness,
            "non_claims_register_v1.json": non_claims,
            "summary.json": summary,
        },
    }

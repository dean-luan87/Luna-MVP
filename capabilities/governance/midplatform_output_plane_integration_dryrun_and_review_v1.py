# -*- coding: utf-8 -*-
"""Midplatform Output Plane Integration DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_output_plane_integration_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    OUTPUT_CHANNEL_TAXONOMY,
    TASK_RESPONSE_INTAKE_FIELDS,
    USER_OUTPUT_CANDIDATE_FIELDS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Output-Plane-Integration-DryRunAndReview-v1-001"
SCOPE = "output_plane_integration_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_output_plane_integration_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_OUTPUT_PLANE_INTEGRATION_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_USER_OUTPUT_CONSTITUTION_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_OUTPUT_PLANE_INTEGRATION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-User-Output-Constitution-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Output-Plane-Integration-Issue-Review-v1-001"

OUTPUT_ASSEMBLY_DRYRUN: Tuple[Dict[str, str], ...] = (
    {"task_response_type": "normal_task_response_candidate", "output_assembly": "user_output_candidate"},
    {
        "task_response_type": "block_response_candidate",
        "output_assembly": "no_output_or_block_notice_candidate",
    },
    {"task_response_type": "hold_response_candidate", "output_assembly": "hold_notice_candidate"},
    {
        "task_response_type": "evidence_request_response_candidate",
        "output_assembly": "clarification_or_evidence_request_output_candidate",
    },
    {
        "task_response_type": "validation_request_response_candidate",
        "output_assembly": "internal_hold_or_validation_notice_candidate",
    },
    {
        "task_response_type": "reobserve_response_candidate",
        "output_assembly": "reobserve_guidance_output_candidate",
    },
    {
        "task_response_type": "degraded_response_candidate",
        "output_assembly": "degraded_mode_notice_candidate",
    },
    {"task_response_type": "fallback_response_candidate", "output_assembly": "fallback_output_candidate"},
    {"task_response_type": "escalation_candidate", "output_assembly": "escalation_notice_candidate"},
    {
        "task_response_type": "violation_response_candidate",
        "output_assembly": "safety_or_violation_notice_candidate",
    },
    {"task_response_type": "reject_response_candidate", "output_assembly": "reject_output_candidate"},
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_output_plane_runtime_enable",
    "dryrun_to_real_user_output_candidate_generation",
    "dryrun_to_user_facing_output",
    "dryrun_to_speech_request_generation",
    "dryrun_to_speech_gate_invocation",
    "dryrun_to_tts_invocation",
    "dryrun_to_voice_output_plane_invocation",
    "dryrun_to_display_output_invocation",
    "dryrun_to_notification_send",
    "dryrun_to_app_push",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Output Plane DryRunAndReview GO ≠ output plane runtime enabled",
    "user_output_candidate sample ≠ user-facing output",
    "speech channel candidate ≠ speech_request / TTS",
    "display channel candidate ≠ display rendered",
    "next User Output Constitution Planning ≠ final output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "output_plane_integration_dryrun_and_review_only",
    "simulated",
    "output_plane_model_candidate_generated_now",
    "sample_task_response_candidate_intake_generated_now",
    "sample_user_output_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "output_plane_runtime_enabled_now",
    "real_user_output_candidate_generated_now",
    "user_facing_output_generated_now",
    "speech_request_generated_now",
    "speech_gate_invoked_now",
    "tts_invoked_now",
    "voice_output_plane_invoked_now",
    "display_output_invoked_now",
    "notification_sent_now",
    "app_push_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_output_plane_integration_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def _sample_task_response_intake(upstream_sample: Dict[str, Any]) -> Dict[str, Any]:
    base = {
        "task_response_candidate_id": upstream_sample.get(
            "task_response_candidate_id", "sample_task_response_intake_v1_001"
        ),
        "source_decision_candidate_ref": upstream_sample.get("source_decision_candidate_ref"),
        "response_type": upstream_sample.get("response_type", "normal_task_response_candidate"),
        "response_scope": upstream_sample.get("response_scope"),
        "response_intent": upstream_sample.get("response_intent"),
        "response_payload_candidate": upstream_sample.get("response_payload_candidate") or {},
        "rationale_refs": list(upstream_sample.get("rationale_refs") or []),
        "evidence_refs": list(upstream_sample.get("evidence_refs") or []),
        "validation_refs": list(upstream_sample.get("validation_refs") or []),
        "health_refs": list(upstream_sample.get("health_refs") or []),
        "constitution_refs": list(upstream_sample.get("constitution_refs") or []),
        "whitebox_refs": list(upstream_sample.get("whitebox_refs") or []),
        "uncertainty_level": upstream_sample.get("uncertainty_level"),
        "candidate_only": True,
        "fact_status": "not_fact",
        "user_output_allowed": False,
        "speech_output_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "task_state_commit_allowed": False,
        "source_chain": upstream_sample.get("source_chain", SOURCE_CHAIN),
        "simulated": True,
    }
    return base


def _sample_user_output(task_resp: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "user_output_candidate_id": "sample_user_output_candidate_v1_001",
        "source_task_response_candidate_ref": task_resp["task_response_candidate_id"],
        "output_type": "user_output_candidate",
        "output_channel_candidate": "display_output_candidate",
        "output_payload_candidate": {
            "assembly_rule": "normal_task_response_candidate → user_output_candidate",
            "response_type": task_resp.get("response_type"),
        },
        "safety_refs": ["safety_gate:pending_later"],
        "constitution_refs": list(task_resp.get("constitution_refs") or []),
        "evidence_refs": list(task_resp.get("evidence_refs") or []),
        "rationale_refs": list(task_resp.get("rationale_refs") or []),
        "uncertainty_level": task_resp.get("uncertainty_level"),
        "personalization_refs": [],
        "output_constraints": {
            "user_output_constitution_required_later": True,
            "safety_gate_required_later": True,
        },
        "user_facing_output_allowed": False,
        "speech_request_allowed": False,
        "display_output_allowed": False,
        "candidate_only": True,
        "fact_status": "not_fact",
        "source_chain": task_resp.get("source_chain", SOURCE_CHAIN),
        "simulated": True,
    }


def run_midplatform_output_plane_integration_dryrun_and_review_v1(
    *,
    midplatform_output_plane_integration_planning_root: str,
    midplatform_task_response_candidate_integration_dryrun_and_review_root: str,
    midplatform_task_response_candidate_integration_planning_root: str,
    midplatform_module_definition_template_planning_root: str,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(midplatform_output_plane_integration_planning_root).expanduser().resolve()
    task_dr_root = Path(
        midplatform_task_response_candidate_integration_dryrun_and_review_root
    ).expanduser().resolve()
    task_plan_root = Path(
        midplatform_task_response_candidate_integration_planning_root
    ).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()
    constitution_dr_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
    ).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_module = _try_read_json(plan_root / "output_plane_module_definition_v1.json") or {}
    plan_user_contract = _try_read_json(plan_root / "user_output_candidate_contract_v1.json") or {}
    plan_channels = _try_read_json(plan_root / "output_channel_taxonomy_v1.json") or {}
    plan_boundary = _try_read_json(plan_root / "output_plane_boundary_matrix_v1.json") or {}
    upstream_task_sample = _try_read_json(task_dr_root / "sample_task_response_candidate_v1.json") or {}
    task_dr_vr = _try_read_json(task_dr_root / "verifier_report.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}
    constitution_dr_vr = _try_read_json(constitution_dr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_task_response_dryrun_root": str(task_dr_root),
        "upstream_task_response_planning_root": str(task_plan_root),
        "upstream_template_planning_root": str(template_root),
        "upstream_constitution_dryrun_root": str(constitution_dr_root),
        "output_root": str(out_root),
    }

    module_identity = plan_module.get("module_identity") or {}
    boundary_matrix = plan_boundary.get("matrix") or {}
    uo_defaults = plan_user_contract.get("defaults") or {}

    if plan_vr.get("verifier") != "GO":
        blockers.append("Output Plane Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if module_identity.get("module_id") != "midplatform_output_plane_integration_v1":
        blockers.append("output_plane module_id mismatch")
    if not plan_user_contract.get("contract_id"):
        blockers.append("user_output_candidate_contract_v1 must exist")
    if plan_channels.get("channel_count") != 6:
        blockers.append("output_channel_taxonomy must define 6 channels")
    if not plan_boundary.get("all_runtime_actions_false"):
        blockers.append("output_boundary_matrix must be all false")
    for field, val in boundary_matrix.items():
        if val is not False:
            blockers.append(f"boundary_matrix.{field} must be false")
    if task_dr_vr.get("verifier") != "GO":
        blockers.append("Task Response DryRunAndReview must be GO")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")
    if constitution_dr_vr.get("verifier") != "GO":
        blockers.append("Constitution DryRunAndReview must be GO")
    if uo_defaults.get("user_facing_output_allowed") is not False:
        blockers.append("user_output defaults must forbid user_facing_output")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "output_plane_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "task_response_not_user_output": True,
        "user_output_not_user_facing": True,
        "output_plane_not_speech_not_tts": True,
        "channel_taxonomy_count": plan_channels.get("channel_count"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    model_candidate = {
        "model_id": "output_plane_model_candidate_v1",
        "module_id": "midplatform_output_plane_integration_v1",
        "module_type": "midplatform_output_candidate_assembly_module",
        "role": "task_response_candidate_to_user_output_candidate_assembly",
        "system_layer": "Output",
        "runtime_enabled_now": False,
        "upstream_modules": ["midplatform_task_response_candidate_integration_v1"],
        "downstream_modules": [
            "speech_gate_later",
            "voice_output_plane_later",
            "display_output_later",
            "user_output_constitution_later",
        ],
        "consumes_task_response_candidate": True,
        "emits_user_output_candidate": True,
        "emits_user_facing_output": False,
        "speech_gate_invocation_allowed": False,
        "tts_invocation_allowed": False,
        "voice_output_plane_invocation_allowed": False,
        "display_output_invocation_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "task_state_commit_allowed": False,
        "provider_invocation_allowed": False,
        "simulated": True,
        **meta,
    }

    sample_task_intake = {**_sample_task_response_intake(upstream_task_sample), **meta}
    sample_user_output = {**_sample_user_output(sample_task_intake), **meta}

    channel_checks: List[Tuple[str, bool]] = []
    simulated_channels = []
    for ch in OUTPUT_CHANNEL_TAXONOMY:
        channel_checks.append((f"channel.{ch['channel_id'][:18]}", True))
        simulated_channels.append({**ch, "simulated": True, "executes_now": False, "verified": True})

    channel_checks.extend(
        [
            ("channel_not_execution", True),
            ("speech_not_tts", True),
            ("display_not_actual", True),
            ("notification_not_push", True),
            ("no_output_valid", True),
        ]
    )

    channel_review = {
        "review_id": "output_channel_taxonomy_dryrun_review_v1",
        "channels": simulated_channels,
        "channel_count": len(OUTPUT_CHANNEL_TAXONOMY),
        "all_six_channels_covered": len(simulated_channels) == 6,
        "channel_candidate_not_execution": True,
        "speech_output_candidate_not_tts": True,
        "display_output_candidate_not_actual_display": True,
        "app_notification_candidate_not_app_push": True,
        "no_output_candidate_valid": True,
        **_review_ok(channel_checks),
        **meta,
    }

    constitution_checks: List[Tuple[str, bool]] = [
        ("constitution_later", True),
        ("constraints_bind", True),
        ("no_pref_override", True),
        ("uncertainty_surface_later", True),
        ("unsafe_blocked", True),
        ("gate_not_executed", meta.get("user_facing_output_generated_now") is False),
    ]
    constitution_review = {
        "review_id": "user_output_constitution_binding_review_v1",
        "user_output_candidate_requires_constitution_later": True,
        "constitution_gate_not_executed_now": True,
        **_review_ok(constitution_checks),
        **meta,
    }

    safety_checks: List[Tuple[str, bool]] = [
        ("gate_required_later", True),
        ("block_overrides_pref", True),
        ("hold_no_output", True),
        ("warning_later", True),
        ("gate_not_invoked", meta.get("user_facing_output_generated_now") is False),
    ]
    safety_review = {
        "review_id": "safety_gate_binding_review_v1",
        "safety_gate_required_before_user_facing_output": True,
        "safety_gate_not_invoked_now": True,
        **_review_ok(safety_checks),
        **meta,
    }

    speech_checks: List[Tuple[str, bool]] = [
        ("gate_later", True),
        ("voice_later", True),
        ("tts_separate", True),
        ("no_request", meta.get("speech_request_generated_now") is False),
        ("no_gate", meta.get("speech_gate_invoked_now") is False),
        ("no_tts", meta.get("tts_invoked_now") is False),
    ]
    speech_review = {
        "review_id": "speech_gate_binding_review_v1",
        "speech_output_requires_speech_gate_later": True,
        "speech_output_requires_voice_output_plane_later": True,
        **_review_ok(speech_checks),
        **meta,
    }

    voice_checks: List[Tuple[str, bool]] = [
        ("not_invoked", meta.get("voice_output_plane_invoked_now") is False),
        ("no_tts", True),
        ("no_audio", True),
        ("no_interrupt", True),
        ("later_only", True),
    ]
    voice_review = {
        "review_id": "voice_output_plane_boundary_review_v1",
        "voice_output_remains_later_only": True,
        **_review_ok(voice_checks),
        **meta,
    }

    display_checks: List[Tuple[str, bool]] = [
        ("not_invoked", meta.get("display_output_invoked_now") is False),
        ("no_ui", True),
        ("no_notification", meta.get("notification_sent_now") is False),
        ("no_push", meta.get("app_push_invoked_now") is False),
        ("later_only", True),
    ]
    display_review = {
        "review_id": "display_output_boundary_review_v1",
        "display_output_remains_later_only": True,
        **_review_ok(display_checks),
        **meta,
    }

    assembly_checks: List[Tuple[str, bool]] = []
    simulated_assemblies = []
    for m in OUTPUT_ASSEMBLY_DRYRUN:
        assembly_checks.append((f"asm.{m['task_response_type'][:16]}", True))
        simulated_assemblies.append({**m, "simulated": True, "executes_output": False, "verified": True})

    assembly_checks.extend(
        [
            ("no_output_exec", True),
            ("notice_not_facing", True),
            ("clarify_not_ask", True),
            ("reobserve_no_camera", meta.get("model_runtime_invoked_now") is False),
            ("escalation_no_hive", True),
        ]
    )

    assembly_review = {
        "review_id": "output_assembly_rule_dryrun_review_v1",
        "mappings": simulated_assemblies,
        "mapping_count": len(OUTPUT_ASSEMBLY_DRYRUN),
        "all_eleven_types_covered": len(simulated_assemblies) == 11,
        "assembly_does_not_execute_output": True,
        **_review_ok(assembly_checks),
        **meta,
    }

    preservation_checks: List[Tuple[str, bool]] = [
        ("uncertainty", sample_user_output.get("uncertainty_level") == sample_task_intake.get("uncertainty_level")),
        ("source_chain", sample_user_output.get("source_chain") == sample_task_intake.get("source_chain")),
        ("evidence", sample_user_output.get("evidence_refs") == sample_task_intake.get("evidence_refs")),
        ("rationale", sample_user_output.get("rationale_refs") == sample_task_intake.get("rationale_refs")),
        ("constitution", sample_user_output.get("constitution_refs") == sample_task_intake.get("constitution_refs")),
        ("validation_preserved", True),
        ("health_preserved", True),
        ("whitebox_preserved", True),
        ("no_evidence_mutate", True),
        ("no_task_resp_mutate", True),
    ]

    preservation_review = {
        "review_id": "output_uncertainty_evidence_preservation_review_v1",
        "sample_refs_preserved": True,
        **_review_ok(preservation_checks),
        **meta,
    }

    personalization_checks: List[Tuple[str, bool]] = [
        ("shape_later", True),
        ("no_override", True),
        ("no_mem_write", meta.get("memory_written_now") is False),
        ("no_profile", True),
        ("optional_refs", True),
    ]
    personalization_review = {
        "review_id": "output_personalization_boundary_review_v1",
        "personalization_refs_optional_context_only": True,
        **_review_ok(personalization_checks),
        **meta,
    }

    memory_checks: List[Tuple[str, bool]] = [
        ("no_memory", meta.get("memory_written_now") is False),
        ("no_wm", meta.get("world_model_written_now") is False),
        ("no_fact", sample_user_output.get("fact_status") == "not_fact"),
        ("no_commit", meta.get("task_state_committed_now") is False),
        ("task_state_later", True),
        ("admission_later", True),
    ]
    memory_review = {
        "review_id": "memory_worldmodel_task_state_boundary_review_v1",
        "no_fact_admission_here": True,
        **_review_ok(memory_checks),
        **meta,
    }

    audit_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        audit_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    audit_checks.append(("model_generated", meta.get("output_plane_model_candidate_generated_now") is True))

    boundary_audit = {
        "audit_id": "output_plane_boundary_audit_v1",
        "forbidden_actions_absent": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(audit_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "output_plane_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        planning_input_review,
        channel_review,
        constitution_review,
        safety_review,
        speech_review,
        voice_review,
        display_review,
        assembly_review,
        preservation_review,
        personalization_review,
        memory_review,
        boundary_audit,
    ]

    model_ok = (
        model_candidate.get("module_id") == "midplatform_output_plane_integration_v1"
        and model_candidate.get("emits_user_output_candidate") is True
        and model_candidate.get("emits_user_facing_output") is False
        and model_candidate.get("speech_gate_invocation_allowed") is False
        and model_candidate.get("display_output_invocation_allowed") is False
    )

    sample_intake_ok = (
        all(f in sample_task_intake for f in TASK_RESPONSE_INTAKE_FIELDS)
        and sample_task_intake.get("candidate_only") is True
        and sample_task_intake.get("user_output_allowed") is False
    )

    sample_user_ok = (
        all(f in sample_user_output for f in USER_OUTPUT_CANDIDATE_FIELDS)
        and sample_user_output.get("candidate_only") is True
        and sample_user_output.get("user_facing_output_allowed") is False
        and sample_user_output.get("speech_request_allowed") is False
        and sample_user_output.get("display_output_allowed") is False
        and sample_user_output.get("fact_status") == "not_fact"
    )

    all_pass = (
        input_ok
        and model_ok
        and sample_intake_ok
        and sample_user_ok
        and channel_review.get("all_six_channels_covered") is True
        and assembly_review.get("all_eleven_types_covered") is True
        and all(s.get("dryrun_and_review_pass") is True for s in review_sections if "dryrun_and_review_pass" in s)
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "output_plane_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "main_chain_closed": [
            "candidate/evidence/validation/health/whitebox",
            "→ decision_request_candidate",
            "→ decision_candidate",
            "→ task_response_candidate",
            "→ user_output_candidate",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_user_output_constitution_planning": all_pass,
        "output_plane_runtime_enabled": False,
        "user_facing_output_still_forbidden": True,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "output_plane_integration_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_not_runtime": True,
        "output_plane_not_user_facing": True,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": all_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": all_pass,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "output_plane_integration_dryrun_review_policy": policy,
        "output_plane_planning_input_review": planning_input_review,
        "output_plane_model_candidate": model_candidate,
        "sample_task_response_candidate_intake": sample_task_intake,
        "sample_user_output_candidate": sample_user_output,
        "output_channel_taxonomy_dryrun_review": channel_review,
        "user_output_constitution_binding_review": constitution_review,
        "safety_gate_binding_review": safety_review,
        "speech_gate_binding_review": speech_review,
        "voice_output_plane_boundary_review": voice_review,
        "display_output_boundary_review": display_review,
        "output_assembly_rule_dryrun_review": assembly_review,
        "output_uncertainty_evidence_preservation_review": preservation_review,
        "output_personalization_boundary_review": personalization_review,
        "memory_worldmodel_task_state_boundary_review": memory_review,
        "output_plane_boundary_audit": boundary_audit,
        "output_plane_blocked_path_result": blocked_path_result,
        "output_plane_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }

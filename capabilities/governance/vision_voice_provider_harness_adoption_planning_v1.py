# -*- coding: utf-8 -*-
"""Vision / Voice Provider Harness Adoption Planning v1 — domain_config only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.controlled_provider_readiness_harness_v1 import (
    ANTI_RECURSION,
    HARNESS_ID,
    HARNESS_PHASES,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_next_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as ROADMAP_NEXT_PHASE,
    SELECTED_ROUTE,
)

PHASE_ID = "Phase-Vision-Voice-Provider-Harness-Adoption-Planning-v1-001"
SCOPE = "vision_voice_provider_harness_adoption_planning_only"
SOURCE_CHAIN = "vision_voice_provider_harness_adoption_planning_v1"

UPSTREAM_ROADMAP_FINAL = ROADMAP_FINAL_GO
UPSTREAM_ROADMAP_NEXT = ROADMAP_NEXT_PHASE

FINAL_DECISION_GO = "VISION_VOICE_PROVIDER_HARNESS_ADOPTION_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_HOLD = "VISION_VOICE_PROVIDER_HARNESS_ADOPTION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Vision-Voice-Provider-Harness-Adoption-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-Voice-Provider-Harness-Adoption-Issue-Review-v1-001"

HARNESS_SUB_CONTRACTS: Tuple[str, ...] = (
    "provider_candidate_contract_v1",
    "dependency_readiness_contract_v1",
    "environment_readiness_contract_v1",
    "provider_comparison_matrix_contract_v1",
    "real_dependency_check_contract_v1",
    "provider_evidence_package_contract_v1",
    "provider_failure_route_contract_v1",
    "provider_rollback_contract_v1",
    "provider_boundary_guard_contract_v1",
    "provider_authorization_readiness_contract_v1",
)

VISION_CANDIDATES: Tuple[Dict[str, Any], ...] = (
    {
        "provider_candidate_id": "vision_provider_mock_fixture",
        "provider_family": "vision_mock_or_fixture",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
    },
    {
        "provider_candidate_id": "vision_provider_local_model_later",
        "provider_family": "local_vision_model_later",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
    },
    {
        "provider_candidate_id": "vision_provider_vlm_later",
        "provider_family": "vlm_provider_later",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
    },
    {
        "provider_candidate_id": "vision_provider_external_later",
        "provider_family": "external_vision_provider_later",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
    },
)

VOICE_CANDIDATES: Tuple[Dict[str, Any], ...] = (
    {
        "provider_candidate_id": "voice_provider_mock_fixture",
        "provider_family": "voice_mock_or_fixture",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
    },
    {
        "provider_candidate_id": "voice_provider_local_asr_later",
        "provider_family": "local_asr_provider_later",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
    },
    {
        "provider_candidate_id": "voice_provider_local_tts_later",
        "provider_family": "local_tts_provider_later",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
    },
    {
        "provider_candidate_id": "voice_provider_external_asr_later",
        "provider_family": "external_asr_provider_later",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
    },
    {
        "provider_candidate_id": "voice_provider_external_tts_later",
        "provider_family": "external_tts_provider_later",
        "provider_status": "planned_candidate",
        "invocation_allowed": False,
    },
)

VISION_FAILURE_ROUTES: Tuple[Dict[str, str], ...] = (
    {"trigger": "vision_provider_import_failed", "route": "dependency_issue_candidate"},
    {"trigger": "vision_model_file_missing", "route": "model_cache_issue_candidate"},
    {"trigger": "vision_model_timeout", "route": "hold_candidate"},
    {"trigger": "low_visual_confidence", "route": "reobserve_or_retry_candidate"},
    {"trigger": "unsafe_visual_output", "route": "block_candidate"},
    {"trigger": "runtime_boundary_violation", "route": "block_candidate"},
)

VOICE_FAILURE_ROUTES: Tuple[Dict[str, str], ...] = (
    {"trigger": "asr_provider_import_failed", "route": "dependency_issue_candidate"},
    {"trigger": "tts_provider_import_failed", "route": "dependency_issue_candidate"},
    {"trigger": "asr_timeout", "route": "clarification_or_hold_candidate"},
    {"trigger": "tts_disabled", "route": "no_voice_output_candidate"},
    {"trigger": "unsafe_speech_response", "route": "block_candidate"},
    {"trigger": "runtime_boundary_violation", "route": "block_candidate"},
)

ADOPTION_BLOCKED_PATHS: Tuple[str, ...] = (
    "vision_candidate_to_live_camera",
    "vision_candidate_to_image_read",
    "vision_provider_candidate_to_model_invocation",
    "visual_observation_candidate_to_fact",
    "visual_observation_candidate_to_world_model_write",
    "voice_provider_candidate_to_asr_runtime",
    "voice_provider_candidate_to_tts_runtime",
    "transcript_candidate_to_task_commit",
    "speech_response_candidate_to_tts",
    "speech_response_candidate_to_user_output",
    "candidate_to_memory_write",
    "candidate_to_world_model_write",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Planning GO ≠ Vision/Voice provider runtime enabled",
    "domain_config plan ≠ live camera or ASR/TTS invoked",
    "harness mapping planned ≠ harness globally enforced",
    "DryRun next ≠ real vision model or voice output",
    "Vision second consumer planned ≠ OCR fields required in Voice contract",
    "adoption planning ≠ provider trial",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "vision_harness_adoption_started_now",
    "voice_harness_adoption_started_now",
    "provider_runtime_enabled_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "real_vision_model_invoked_now",
    "live_camera_enabled_now",
    "image_read_executed_now",
    "asr_runtime_invoked_now",
    "tts_runtime_invoked_now",
    "voice_output_generated_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/vision_voice_provider_harness_adoption_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "vision_voice_provider_harness_adoption_planning_only": True,
        "harness_id": HARNESS_ID,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _harness_mapping(domain: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "mapping_id": f"{domain}_harness_contract_mapping_v1",
        "provider_domain": domain,
        "harness_id": HARNESS_ID,
        "mapped_sub_contracts": list(HARNESS_SUB_CONTRACTS),
        "mapped_sub_contract_count": len(HARNESS_SUB_CONTRACTS),
        "harness_phases_covered": list(HARNESS_PHASES),
        "mapping_pass": True,
        "ocr_specific_fields_not_required": True,
        **meta,
    }


def run_vision_voice_provider_harness_adoption_planning_v1(
    *,
    ocr_provider_next_roadmap_decision_root: str,
    controlled_provider_readiness_harness_root: Optional[str] = None,
    vision_ocr_voice_controlled_optimization_post_dryrun_review_root: Optional[str] = None,
    model_registry_canonicalization_post_dryrun_review_root: Optional[str] = None,
    health_management_layer_integration_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    roadmap_root = Path(ocr_provider_next_roadmap_decision_root).expanduser().resolve()
    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    next_route = _try_read_json(roadmap_root / "next_phase_readiness_decision_v1.json") or {}

    harness_root = Path(
        controlled_provider_readiness_harness_root
        or roadmap_root.parent / "controlled_provider_readiness_harness"
    ).expanduser().resolve()
    harness_sm = _try_read_json(harness_root / "summary.json") or {}
    harness_vr = _try_read_json(harness_root / "verifier_report.json") or {}
    validation = _try_read_json(
        harness_root / "controlled_provider_readiness_harness_validation_result_v1.json"
    ) or {}
    harness_contract = _try_read_json(
        harness_root / "controlled_provider_readiness_harness_contract_v1.json"
    ) or {}
    future_plan = _try_read_json(harness_root / "future_consumer_adoption_plan_v1.json") or {}

    vov_post_root = Path(
        vision_ocr_voice_controlled_optimization_post_dryrun_review_root
        or roadmap_root.parent / "vision_ocr_voice_controlled_optimization_post_dryrun_review"
    ).expanduser().resolve()
    canonical_root = Path(
        model_registry_canonicalization_post_dryrun_review_root
        or roadmap_root.parent / "model_registry_canonicalization_post_dryrun_review"
    ).expanduser().resolve()
    health_post_root = Path(
        health_management_layer_integration_post_dryrun_review_root
        or roadmap_root.parent / "health_management_layer_integration_post_dryrun_review"
    ).expanduser().resolve()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_roadmap_root": str(roadmap_root),
        "upstream_harness_root": str(harness_root),
        "output_root": str(out_root),
    }

    roadmap_go = roadmap_vr.get("verifier") == "GO" and roadmap_vr.get("passed") is True
    if not roadmap_go:
        blockers.append("roadmap decision verifier must be GO")
    if roadmap_sm.get("final_decision") != UPSTREAM_ROADMAP_FINAL:
        blockers.append("roadmap final_decision mismatch")
    if roadmap_sm.get("recommended_next_phase") != UPSTREAM_ROADMAP_NEXT:
        blockers.append("roadmap recommended_next_phase mismatch")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be Route B")

    harness_go = harness_vr.get("verifier") == "GO" and harness_vr.get("passed") is True
    if not harness_go:
        blockers.append("harness verifier must be GO")
    if harness_sm.get("harness_id") != HARNESS_ID:
        blockers.append("harness_id mismatch")
    if validation.get("ocr_first_consumer_validated") is not True:
        blockers.append("OCR first consumer must be validated")
    if harness_sm.get("harness_runtime_enforced_globally_now") is True:
        blockers.append("harness_runtime_enforced_globally_now must be false")

    domains = {c.get("domain") for c in future_plan.get("consumers") or []}
    if "vision" not in domains or "voice" not in domains:
        blockers.append("future consumers must include vision and voice")

    anti_rules = harness_contract.get("anti_recursion_rules") or []
    if len(anti_rules) < len(ANTI_RECURSION):
        blockers.append("anti_recursion must be active in harness")

    vov_sm = _try_read_json(vov_post_root / "summary.json") or {}
    canonical_sm = _try_read_json(canonical_root / "summary.json") or {}
    health_sm = _try_read_json(health_post_root / "summary.json") or {}

    if vov_sm.get("controlled_optimization_dryrun_closed") is not True:
        blockers.append("vision_ocr_voice controlled optimization should be closed")
    if canonical_sm.get("b_lite_canonical_v0_baseline_closed") is not True:
        blockers.append("model_registry_canonical_v0 must be closed")
    if health_sm.get("health_management_integration_dryrun_closed") is not True:
        blockers.append("health management must be closed")

    roadmap_input = {
        "review_id": "ocr_provider_next_roadmap_input_review_v1",
        "upstream_roadmap_root": str(roadmap_root),
        "upstream_verifier_go": roadmap_go,
        "upstream_final_decision": roadmap_sm.get("final_decision"),
        "selected_route": roadmap_sm.get("selected_route"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    harness_input = {
        "review_id": "controlled_provider_readiness_harness_input_review_v1",
        "upstream_harness_root": str(harness_root),
        "harness_verifier_go": harness_go,
        "harness_id": HARNESS_ID,
        "ocr_first_consumer_validated": validation.get("ocr_first_consumer_validated"),
        "anti_recursion_active": len(anti_rules) >= len(ANTI_RECURSION),
        "review_pass": len(blockers) == 0,
        **meta,
    }

    vision_domain = {
        "plan_id": "vision_provider_domain_config_plan_v1",
        "provider_domain": "vision",
        "provider_candidate_families": [
            "vision_mock_or_fixture",
            "local_vision_model_later",
            "vlm_provider_later",
            "external_vision_provider_later",
        ],
        "output_contract": "visual_observation_candidate",
        "evidence_pack": "visual_evidence_pack_candidate_later",
        "defaults": {
            "provider_status": "planned_candidate",
            "invocation_allowed": False,
            "live_camera_allowed": False,
            "image_read_allowed": False,
            "controlled_trial_required": True,
            "dependency_check_required": True,
            "environment_check_required": True,
            "health_binding_required": True,
            "constitution_gate_required": True,
        },
        "forbidden_now": [
            "live_camera",
            "arbitrary_image_read",
            "real_vision_model_invocation",
            "visual_fact_write",
            "world_model_write",
            "user_output",
        ],
        "failure_routes": list(VISION_FAILURE_ROUTES),
        **meta,
    }

    voice_domain = {
        "plan_id": "voice_provider_domain_config_plan_v1",
        "provider_domain": "voice",
        "provider_candidate_families": [
            "voice_mock_or_fixture",
            "local_asr_provider_later",
            "local_tts_provider_later",
            "external_asr_provider_later",
            "external_tts_provider_later",
        ],
        "output_contracts": ["transcript_candidate", "speech_response_candidate"],
        "evidence_pack": "voice_evidence_pack_candidate_later",
        "defaults": {
            "provider_status": "planned_candidate",
            "invocation_allowed": False,
            "asr_runtime_allowed": False,
            "tts_runtime_allowed": False,
            "voice_output_allowed": False,
            "controlled_trial_required": True,
            "dependency_check_required": True,
            "environment_check_required": True,
            "health_binding_required": True,
            "constitution_gate_required": True,
        },
        "forbidden_now": [
            "asr_runtime",
            "tts_runtime",
            "real_voice_output",
            "user_facing_output",
            "direct_emotional_expression_output",
            "transcript_to_task_commit",
        ],
        "failure_routes": list(VOICE_FAILURE_ROUTES),
        **meta,
    }

    vision_inventory = {
        "plan_id": "vision_provider_candidate_inventory_plan_v1",
        "candidates": list(VISION_CANDIDATES),
        "candidate_count": len(VISION_CANDIDATES),
        **meta,
    }

    voice_inventory = {
        "plan_id": "voice_provider_candidate_inventory_plan_v1",
        "candidates": list(VOICE_CANDIDATES),
        "candidate_count": len(VOICE_CANDIDATES),
        **meta,
    }

    vision_mapping = _harness_mapping("vision", meta)
    voice_mapping = _harness_mapping("voice", meta)

    boundary_matrix = {
        "matrix_id": "vision_voice_adoption_boundary_matrix_v1",
        "paths": [{"path_id": p, "blocked": True} for p in ADOPTION_BLOCKED_PATHS],
        "path_count": len(ADOPTION_BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    no_runtime_audit = {
        "plan_id": "vision_voice_no_runtime_audit_plan_v1",
        "vision_forbidden": vision_domain["forbidden_now"],
        "voice_forbidden": voice_domain["forbidden_now"],
        "real_vision_model_invoked_now": False,
        "asr_runtime_invoked_now": False,
        "tts_runtime_invoked_now": False,
        "provider_imported_now": False,
        "audit_pass": True,
        **meta,
    }

    generalization = {
        "review_id": "future_harness_consumer_generalization_review_v1",
        "ocr_first_consumer_validated": validation.get("ocr_first_consumer_validated"),
        "vision_second_consumer_mappable": True,
        "voice_third_consumer_mappable": True,
        "map_library_hive_memory_future_only": True,
        "no_automatic_consumer_runtime_enablement": True,
        "no_ocr_specific_fields_leak_into_vision_voice_required_contract": True,
        "domain_config_required": True,
        "future_only_domains": ["map", "library", "hive", "memory"],
        "review_pass": len(blockers) == 0,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "vision_voice_harness_adoption_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_goals": [
            "consume Vision domain_config via Controlled Provider Readiness Harness",
            "consume Voice domain_config via Controlled Provider Readiness Harness",
            "generate vision_provider_readiness_candidate",
            "generate voice_provider_readiness_candidate",
            "verify no-runtime / no-import / no-provider-invocation",
            "no real Vision / ASR / TTS",
        ],
        **meta,
    }

    planning_ok = len(blockers) == 0 and roadmap_input.get("review_pass") is True
    boundary_ok = planning_ok

    policy = {
        "policy_id": "vision_voice_harness_adoption_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    decision = {
        "decision_id": "vision_voice_harness_adoption_planning_decision_v1",
        "planning_pass": planning_ok,
        "ready_for_dryrun": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
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
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": decision["final_decision"],
        "recommended_next_phase": decision["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "vision_voice_harness_adoption_planning_policy": policy,
        "ocr_provider_next_roadmap_input_review": roadmap_input,
        "controlled_provider_readiness_harness_input_review": harness_input,
        "vision_provider_domain_config_plan": vision_domain,
        "voice_provider_domain_config_plan": voice_domain,
        "vision_provider_candidate_inventory_plan": vision_inventory,
        "voice_provider_candidate_inventory_plan": voice_inventory,
        "vision_harness_contract_mapping": vision_mapping,
        "voice_harness_contract_mapping": voice_mapping,
        "vision_voice_adoption_boundary_matrix": boundary_matrix,
        "vision_voice_no_runtime_audit_plan": no_runtime_audit,
        "future_harness_consumer_generalization_review": generalization,
        "vision_voice_harness_adoption_dryrun_plan": dryrun_plan,
        "vision_voice_harness_adoption_planning_decision": decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }

# -*- coding: utf-8 -*-
"""Model Registry Canonicalization Planning v1 — canonical table plan only, no registry generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.luna_validation_factory_consolidation_v1 import (
    FINAL_DECISION as FACTORY_FINAL,
    PHASE_ID as FACTORY_PHASE,
)
from capabilities.governance.model_management_layer_recovery_dryrun_v1 import (
    MODEL_OUTPUT_CANDIDATE_TYPES,
    SKILL_SPECS,
)
from capabilities.governance.model_management_layer_recovery_planning_v1 import (
    CAPABILITY_DESCRIPTORS,
    HEALTH_STATES,
)
from capabilities.governance.model_management_layer_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL_GO,
    FUTURE_VERSIONS,
    NEXT_PHASE_GO as ROADMAP_NEXT_PHASE,
    REGISTRY_VERSION,
    ROUTE_B_LITE,
    SCHEMA_VERSION,
    SELECTED_ROUTE,
    UPDATE_TRIGGERS,
    VERSION_SCOPE,
    VERSION_STATUS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Model-Registry-Canonicalization-Planning-v1-001"
SCOPE = "model_registry_canonicalization_planning_only"
SOURCE_CHAIN = "model_registry_canonicalization_planning_v1"

UPSTREAM_ROADMAP_FINAL = ROADMAP_FINAL_GO
UPSTREAM_ROADMAP_NEXT = ROADMAP_NEXT_PHASE

FINAL_DECISION_GO = "MODEL_REGISTRY_CANONICALIZATION_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_HOLD = "MODEL_REGISTRY_CANONICALIZATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Model-Registry-Canonicalization-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Model-Management-Layer-Recovery-Issue-Review-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_registry_canonicalization_planning"
)

SCHEMA_V0_PLANNING_FIELDS: Tuple[str, ...] = (
    "registry_version",
    "schema_version",
    "model_id",
    "model_domain",
    "model_type",
    "version",
    "provider_type",
    "runtime_mode",
    "capability_tags",
    "input_contract",
    "output_contract",
    "candidate_output_type",
    "health_state_ref",
    "fallback_model_ref",
    "invocation_allowed",
    "runtime_boundary_profile",
    "constitution_gate_required",
    "safety_gate_required",
    "source_chain_required",
    "write_allowed",
    "runtime_action_allowed",
    "user_facing_output_allowed",
    "notes",
)

MODEL_DOMAIN_TAXONOMY: Tuple[str, ...] = (
    "vision",
    "ocr",
    "voice_asr",
    "voice_tts",
    "emotion",
    "face_recognition",
    "scan",
)

PROVIDER_TYPE_TAXONOMY: Tuple[str, ...] = (
    "mock_or_fixture",
    "local_provider_later",
    "cloud_provider_later",
    "external_provider_later",
    "disabled",
)

RUNTIME_MODE_TAXONOMY: Tuple[str, ...] = (
    "mock",
    "fixture",
    "disabled",
    "controlled_provider_later",
    "limited_runtime_later",
    "real_runtime_later",
)

CAPABILITY_TAG_TAXONOMY: Tuple[str, ...] = (
    "can_see",
    "can_read_text",
    "can_transcribe",
    "can_speak",
    "can_detect_emotion",
    "can_recognize_face",
    "can_scan",
    "can_generate_candidate",
    "can_write_fact",
    "can_trigger_action",
)

CANONICAL_ENTRY_DEFAULTS: Dict[str, Any] = {
    "registry_version": REGISTRY_VERSION,
    "schema_version": SCHEMA_VERSION,
    "provider_type": "mock_or_fixture",
    "invocation_allowed": False,
    "write_allowed": False,
    "runtime_action_allowed": False,
    "user_facing_output_allowed": False,
    "constitution_gate_required": True,
    "safety_gate_required": True,
    "candidate_only_output": True,
    "fact_status_default": "not_fact",
    "source_chain_required": True,
}

CANONICAL_ENTRY_PLANS: Tuple[Dict[str, Any], ...] = (
    {
        "model_id": "vision_perspective_model_mock",
        "model_domain": "vision",
        "model_type": "perspective",
        "runtime_mode": "mock",
        "capability_tags": ["can_see", "can_generate_candidate"],
        "candidate_output_type": "visual_observation_candidate",
        "health_state_ref": "mhs_vision_perspective_model_mock",
        "fallback_model_ref": "vision_perspective_model_mock_fallback_disabled",
    },
    {
        "model_id": "ocr_model_mock",
        "model_domain": "ocr",
        "model_type": "ocr",
        "runtime_mode": "mock",
        "capability_tags": ["can_read_text", "can_generate_candidate"],
        "candidate_output_type": "ocr_result_candidate",
        "health_state_ref": "mhs_ocr_model_mock",
        "fallback_model_ref": "ocr_model_mock_fallback_disabled",
    },
    {
        "model_id": "voice_asr_model_mock",
        "model_domain": "voice_asr",
        "model_type": "asr",
        "runtime_mode": "fixture",
        "capability_tags": ["can_transcribe", "can_generate_candidate"],
        "candidate_output_type": "speech_response_candidate",
        "health_state_ref": "mhs_voice_asr_model_mock",
        "fallback_model_ref": "voice_asr_model_mock_fallback_disabled",
    },
    {
        "model_id": "voice_tts_model_mock",
        "model_domain": "voice_tts",
        "model_type": "tts",
        "runtime_mode": "fixture",
        "capability_tags": ["can_speak", "can_generate_candidate"],
        "candidate_output_type": "speech_response_candidate",
        "health_state_ref": "mhs_voice_tts_model_mock",
        "fallback_model_ref": "voice_tts_model_mock_fallback_disabled",
    },
    {
        "model_id": "emotion_model_mock",
        "model_domain": "emotion",
        "model_type": "emotion",
        "runtime_mode": "disabled",
        "capability_tags": ["can_detect_emotion", "can_generate_candidate"],
        "candidate_output_type": "emotion_state_candidate",
        "health_state_ref": "mhs_emotion_model_mock",
        "fallback_model_ref": "emotion_model_mock_fallback_disabled",
    },
    {
        "model_id": "face_recognition_model_mock",
        "model_domain": "face_recognition",
        "model_type": "face",
        "runtime_mode": "disabled",
        "capability_tags": ["can_recognize_face", "can_generate_candidate"],
        "candidate_output_type": "face_identity_candidate",
        "health_state_ref": "mhs_face_recognition_model_mock",
        "fallback_model_ref": "face_recognition_model_mock_fallback_disabled",
    },
    {
        "model_id": "scan_model_mock",
        "model_domain": "scan",
        "model_type": "scan",
        "runtime_mode": "disabled",
        "capability_tags": ["can_scan", "can_generate_candidate"],
        "candidate_output_type": "scan_result_candidate",
        "health_state_ref": "mhs_scan_model_mock",
        "fallback_model_ref": "scan_model_mock_fallback_disabled",
    },
)

NORMALIZATION_RULES: Tuple[Dict[str, str], ...] = (
    {"rule_id": "model_id_snake_case", "detail": "model_id must remain stable snake_case from dryrun baseline"},
    {"rule_id": "voice_domain_split", "detail": "voice ASR/TTS normalized to voice_asr / voice_tts in canonical v0"},
    {"rule_id": "provider_mock_fixture_only", "detail": "v0 provider_type locked to mock_or_fixture"},
    {"rule_id": "invocation_false_default", "detail": "invocation_allowed=false for all v0 entries"},
    {"rule_id": "health_ref_required", "detail": "health_state_ref must reference health candidate matrix id"},
    {"rule_id": "fallback_candidate_only", "detail": "fallback_model_ref may point to disabled fallback placeholder only"},
    {"rule_id": "output_candidate_binding", "detail": "candidate_output_type must bind CandidateOutputContract"},
    {"rule_id": "capability_tags_from_descriptor", "detail": "capability_tags derived from capability descriptor taxonomy"},
    {"rule_id": "no_production_registry", "detail": "planning does not emit production registry artifact"},
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "canonical_registry_generated_now",
    "production_registry_generated_now",
    "model_registry_published_now",
    "schema_upgrade_executed_now",
    "model_runtime_invoked_now",
    "model_provider_invoked_now",
    "ocr_provider_invoked_now",
    "vision_model_invoked_now",
    "voice_model_invoked_now",
    "emotion_model_invoked_now",
    "face_recognition_model_invoked_now",
    "scan_model_invoked_now",
    "model_switch_executed_now",
    "model_update_executed_now",
    "model_repair_executed_now",
    "skill_runtime_enabled_now",
    "runtime_enabled_now",
    "tts_invoked_now",
    "llm_invoked_now",
    "user_facing_output_generated_now",
    "world_model_written_now",
    "memory_written_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Canonicalization Planning GO ≠ canonical registry generated",
    "Table plan ≠ production registry published",
    "Schema v0 plan ≠ schema_version upgraded",
    "Skill relationship plan ≠ skill runtime enabled",
    "DryRun plan next ≠ model invocation allowed",
    "model_registry_canonical_v0 plan ≠ final model registry",
    "Planning GO ≠ real provider enabled",
)

PLANNING_FORBIDDEN: Tuple[str, ...] = (
    "production registry generation",
    "model invocation",
    "provider modification",
    "model switch execution",
    "schema_version upgrade",
    "real provider introduction",
    "skill runtime enablement",
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "model_registry_canonicalization_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _build_canonical_entry_plan(spec: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **CANONICAL_ENTRY_DEFAULTS,
        **spec,
        "version": "canonical_v0_plan",
        "runtime_boundary_profile": "planning_no_invocation",
        "input_contract": {"schema": "model_input_contract_v1", "planning": True},
        "output_contract": {"schema": "model_output_contract_v1", "candidate_only": True},
        "notes": "canonical v0 table plan entry — not production registry",
    }


def run_model_registry_canonicalization_planning_v1(
    *,
    model_management_layer_roadmap_decision_root: str,
    model_management_layer_recovery_post_dryrun_review_root: Optional[str] = None,
    model_management_layer_recovery_dryrun_root: Optional[str] = None,
    model_management_layer_recovery_planning_root: Optional[str] = None,
    luna_validation_factory_consolidation_root: Optional[str] = None,
    planning_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    roadmap_root = Path(model_management_layer_roadmap_decision_root).expanduser().resolve()
    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    versioning = _try_read_json(roadmap_root / "model_registry_versioning_policy_v1.json") or {}

    post_root = Path(
        model_management_layer_recovery_post_dryrun_review_root
        or roadmap_sm.get("upstream_post_dryrun_review_root")
        or roadmap_root.parent / "model_management_layer_recovery_post_dryrun_review"
    ).expanduser().resolve()
    dryrun_root = Path(
        model_management_layer_recovery_dryrun_root
        or roadmap_sm.get("upstream_dryrun_root")
        or roadmap_root.parent / "model_management_layer_recovery_dryrun"
    ).expanduser().resolve()
    recovery_planning_root = Path(
        model_management_layer_recovery_planning_root
        or roadmap_sm.get("upstream_planning_root")
        or roadmap_root.parent / "model_management_layer_recovery_planning"
    ).expanduser().resolve()
    factory_root = Path(
        luna_validation_factory_consolidation_root
        or roadmap_root.parent / "luna_validation_factory_consolidation"
    ).expanduser().resolve()

    out_root = (
        Path(planning_output_root).expanduser().resolve()
        if planning_output_root
        else roadmap_root.parent / "model_registry_canonicalization_planning"
    )

    meta = {
        **_planning_meta(),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_post_dryrun_review_root": str(post_root),
        "upstream_dryrun_root": str(dryrun_root),
        "upstream_recovery_planning_root": str(recovery_planning_root),
        "upstream_validation_factory_root": str(factory_root),
        "output_root": str(out_root),
    }

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    recovery_planning_sm = _try_read_json(recovery_planning_root / "summary.json") or {}
    factory_sm = _try_read_json(factory_root / "summary.json") or {}
    registry = _try_read_json(dryrun_root / "mock_fixture_model_registry_v1.json") or {}

    roadmap_go = roadmap_vr.get("verifier") == "GO" and roadmap_vr.get("passed") is True
    if not roadmap_go:
        blockers.append("roadmap decision verifier must be GO")
    if roadmap_sm.get("final_decision") != UPSTREAM_ROADMAP_FINAL:
        blockers.append("roadmap final_decision mismatch")
    if roadmap_sm.get("recommended_next_phase") != UPSTREAM_ROADMAP_NEXT:
        blockers.append("roadmap recommended_next_phase mismatch")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be B-lite v0")
    if roadmap_sm.get("selected_registry_baseline_version") != REGISTRY_VERSION:
        blockers.append("registry baseline version mismatch")
    if roadmap_sm.get("selected_schema_version") != SCHEMA_VERSION:
        blockers.append("schema version mismatch")
    if roadmap_sm.get("version_status") != VERSION_STATUS:
        blockers.append("version_status must be baseline")
    if roadmap_sm.get("version_scope") != VERSION_SCOPE:
        blockers.append("version_scope mismatch")
    if roadmap_sm.get("real_provider_included") is not False:
        blockers.append("real_provider_included must be false")
    if roadmap_sm.get("production_runtime_included") is not False:
        blockers.append("production_runtime_included must be false")

    counts = {
        "mock_fixture_model_registry": dryrun_sm.get("model_registry_entry_count", len(registry.get("entries") or [])),
        "skill_registry_dryrun": dryrun_sm.get("skill_registry_entry_count", 0),
        "model_health_state_candidate": dryrun_sm.get("health_candidate_count", 0),
        "model_switching_candidate": dryrun_sm.get("switching_candidate_count", 0),
        "output_contract": len(
            (_try_read_json(dryrun_root / "model_output_contract_integration_result_v1.json") or {}).get("output_types")
            or []
        ),
    }
    for key, exp in (
        ("mock_fixture_model_registry", 7),
        ("skill_registry_dryrun", 6),
        ("model_health_state_candidate", 6),
        ("model_switching_candidate", 6),
        ("output_contract", 7),
    ):
        if counts[key] != exp:
            blockers.append(f"{key} count must be {exp}")

    for field in ("model_runtime_invoked_now", "model_provider_invoked_now", "model_switch_executed_now"):
        if dryrun_sm.get(field) is True or roadmap_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    if dryrun_vr.get("verifier") != "GO":
        blockers.append("dryrun verifier should be GO")
    if recovery_planning_sm.get("boundary_ok") is not True:
        blockers.append("recovery planning boundary_ok required")
    if not factory_sm.get("final_decision"):
        blockers.append("validation factory summary required")

    roadmap_input = {
        "review_id": "roadmap_decision_input_review_v1",
        "upstream_root": str(roadmap_root),
        "upstream_verifier_go": roadmap_go,
        "upstream_final_decision": roadmap_sm.get("final_decision"),
        "selected_route": roadmap_sm.get("selected_route"),
        "counts": counts,
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    version_input = {
        "review_id": "model_registry_version_input_review_v1",
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "version_status": VERSION_STATUS,
        "version_scope": VERSION_SCOPE,
        "real_provider_included": False,
        "production_runtime_included": False,
        "future_update_expected": versioning.get("future_update_expected", True),
        "update_triggers_inherited": list(UPDATE_TRIGGERS),
        "future_versions_inherited": list(FUTURE_VERSIONS),
        "review_pass": len(blockers) == 0,
        **meta,
    }

    schema_plan = {
        "plan_id": "model_registry_schema_v0_planning_v1",
        "schema_version": SCHEMA_VERSION,
        "registry_version": REGISTRY_VERSION,
        "fields": list(SCHEMA_V0_PLANNING_FIELDS),
        "field_count": len(SCHEMA_V0_PLANNING_FIELDS),
        "schema_upgrade_executed_now": False,
        "notes": "schema v0 planning only — no schema upgrade in this phase",
        **meta,
    }

    table_entries = [_build_canonical_entry_plan(spec) for spec in CANONICAL_ENTRY_PLANS]
    table_plan = {
        "plan_id": "model_registry_canonical_v0_table_plan_v1",
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "entry_count": len(table_entries),
        "planned_entries": table_entries,
        "all_invocation_false": all(e.get("invocation_allowed") is False for e in table_entries),
        "canonical_registry_generated_now": False,
        **meta,
    }

    normalization = {
        "rules_id": "model_registry_entry_normalization_rules_v1",
        "rules": list(NORMALIZATION_RULES),
        **meta,
    }

    domain_taxonomy = {
        "taxonomy_id": "model_domain_taxonomy_v0",
        "domains": list(MODEL_DOMAIN_TAXONOMY),
        "domain_to_model_ids": {
            e["model_domain"]: e["model_id"] for e in CANONICAL_ENTRY_PLANS
        },
        **meta,
    }

    provider_taxonomy = {
        "taxonomy_id": "provider_type_taxonomy_v0",
        "provider_types": list(PROVIDER_TYPE_TAXONOMY),
        "v0_active": ["mock_or_fixture"],
        "v0_later_only": [p for p in PROVIDER_TYPE_TAXONOMY if p != "mock_or_fixture"],
        **meta,
    }

    runtime_taxonomy = {
        "taxonomy_id": "runtime_mode_taxonomy_v0",
        "runtime_modes": list(RUNTIME_MODE_TAXONOMY),
        "v0_active": ["mock", "fixture", "disabled"],
        "v0_later_only": ["controlled_provider_later", "limited_runtime_later", "real_runtime_later"],
        **meta,
    }

    capability_taxonomy = {
        "taxonomy_id": "capability_tag_taxonomy_v0",
        "capability_tags": list(CAPABILITY_TAG_TAXONOMY),
        "can_write_fact_default": False,
        "can_trigger_action_default": False,
        "descriptor_alignment": list(CAPABILITY_DESCRIPTORS),
        **meta,
    }

    io_binding = {
        "binding_id": "model_input_output_contract_binding_v1",
        "bindings": [
            {
                "model_id": e["model_id"],
                "input_contract": {"schema": "model_input_contract_v1"},
                "output_contract": {"schema": "model_output_contract_v1", "candidate_only": True},
                "candidate_output_type": e["candidate_output_type"],
            }
            for e in CANONICAL_ENTRY_PLANS
        ],
        **meta,
    }

    health_binding = {
        "binding_id": "model_health_and_fallback_binding_v1",
        "health_states_reference": list(HEALTH_STATES),
        "bindings": [
            {
                "model_id": e["model_id"],
                "health_state_ref": e["health_state_ref"],
                "fallback_model_ref": e["fallback_model_ref"],
                "fallback_candidate_only": True,
            }
            for e in CANONICAL_ENTRY_PLANS
        ],
        **meta,
    }

    skill_relationships = [
        {
            "skill_id": s["skill_id"],
            "required_models": s["required_models"],
            "output_candidate_types": s["output_candidate_types"],
            "skill_runtime_enabled": False,
        }
        for s in SKILL_SPECS
    ]
    skill_plan = {
        "plan_id": "skill_registry_relationship_plan_v1",
        "skill_entry_count": len(skill_relationships),
        "relationships": skill_relationships,
        "skill_registry_expansion_deferred": True,
        "skill_runtime_enabled": False,
        "full_expansion_after": "map / library / hive / external tool integration prep",
        **meta,
    }

    output_binding = {
        "plan_id": "candidate_output_contract_binding_plan_v1",
        "output_types": list(MODEL_OUTPUT_CANDIDATE_TYPES),
        "bindings": [
            {
                "output_candidate_type": ot,
                "candidate_only": True,
                "fact_status": "not_fact",
                "write_allowed": False,
                "runtime_action_allowed": False,
                "user_facing_output_allowed": False,
            }
            for ot in MODEL_OUTPUT_CANDIDATE_TYPES
        ],
        **meta,
    }

    version_policy = {
        "policy_id": "version_upgrade_and_deprecation_policy_v1",
        "current_registry_version": REGISTRY_VERSION,
        "current_schema_version": SCHEMA_VERSION,
        "future_versions": list(FUTURE_VERSIONS),
        "update_triggers": list(UPDATE_TRIGGERS),
        "schema_upgrade_executed_now": False,
        "deprecation_policy": "prior version retained read-only when version bump occurs",
        **meta,
    }

    dryrun_plan = {
        "plan_id": "canonical_registry_generation_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_goals": [
            "generate model_registry_canonical_v0_candidate",
            "verify 7 canonical entries",
            "verify schema_version=model_registry_schema_v0",
            "verify all invocation_allowed=false",
            "verify candidate output contract binding",
            "verify version note and future update triggers",
            "no model invocation",
        ],
        "dryrun_forbidden": list(PLANNING_FORBIDDEN),
        "production_registry_generated_now": False,
        **meta,
    }

    planning_ok = len(blockers) == 0

    planning_decision = {
        "decision_id": "model_registry_canonicalization_planning_decision_v1",
        "planning_complete": planning_ok,
        "selected_route": SELECTED_ROUTE,
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "final_decision": FINAL_DECISION_GO if planning_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "model_registry_canonicalization_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "selected_route": SELECTED_ROUTE,
        "principles": [
            "planning_only_no_registry_generation",
            "canonical_v0_baseline_mock_fixture_only",
            "no_model_no_provider_no_runtime",
        ],
        "forbidden_in_planning": list(PLANNING_FORBIDDEN),
        **meta,
    }

    non_claims = {
        "register_id": "model_registry_canonicalization_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": planning_ok,
        "violations": blockers,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        "selected_route": SELECTED_ROUTE,
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "canonical_entry_count_planned": len(table_entries),
        "skill_relationship_count_planned": len(skill_relationships),
        "high_risk_count": 0 if planning_ok else 1,
        "counts": counts,
        **meta,
    }

    return {
        "model_registry_canonicalization_planning_policy": policy,
        "roadmap_decision_input_review": roadmap_input,
        "model_registry_version_input_review": version_input,
        "model_registry_schema_v0_planning": schema_plan,
        "model_registry_canonical_v0_table_plan": table_plan,
        "model_registry_entry_normalization_rules": normalization,
        "model_domain_taxonomy_v0": domain_taxonomy,
        "provider_type_taxonomy_v0": provider_taxonomy,
        "runtime_mode_taxonomy_v0": runtime_taxonomy,
        "capability_tag_taxonomy_v0": capability_taxonomy,
        "model_input_output_contract_binding": io_binding,
        "model_health_and_fallback_binding": health_binding,
        "skill_registry_relationship_plan": skill_plan,
        "candidate_output_contract_binding_plan": output_binding,
        "version_upgrade_and_deprecation_policy": version_policy,
        "canonical_registry_generation_dryrun_plan": dryrun_plan,
        "model_registry_canonicalization_non_claims_register": non_claims,
        "model_registry_canonicalization_planning_decision": planning_decision,
        "summary": summary,
    }

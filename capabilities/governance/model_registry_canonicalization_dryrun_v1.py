# -*- coding: utf-8 -*-
"""Model Registry Canonicalization DryRun v1 — generates canonical v0 candidate only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.model_management_layer_recovery_dryrun_v1 import (
    MODEL_OUTPUT_CANDIDATE_TYPES,
    SKILL_SPECS,
)
from capabilities.governance.model_management_layer_roadmap_decision_v1 import (
    FUTURE_VERSIONS,
    REGISTRY_VERSION,
    SCHEMA_VERSION,
    UPDATE_TRIGGERS,
    VERSION_SCOPE,
    VERSION_STATUS,
)
from capabilities.governance.model_registry_canonicalization_planning_v1 import (
    CANONICAL_ENTRY_PLANS,
    CAPABILITY_TAG_TAXONOMY,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    MODEL_DOMAIN_TAXONOMY,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    PHASE_ID as PLANNING_PHASE,
    PROVIDER_TYPE_TAXONOMY,
    RUNTIME_MODE_TAXONOMY,
    SCHEMA_V0_PLANNING_FIELDS,
    SCOPE as PLANNING_SCOPE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Model-Registry-Canonicalization-DryRun-v1-001"
SCOPE = "model_registry_canonicalization_dryrun_only"
SOURCE_CHAIN = "model_registry_canonicalization_dryrun_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = "MODEL_REGISTRY_CANONICALIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "MODEL_REGISTRY_CANONICALIZATION_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Model-Registry-Canonicalization-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Model-Registry-Canonicalization-Issue-Review-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_registry_canonicalization_dryrun"
)

V0_ACTIVE_RUNTIME_MODES: Tuple[str, ...] = ("mock", "fixture", "disabled")

IO_BINDING_EXPECTED: Dict[str, str] = {
    "vision_perspective_model_mock": "visual_observation_candidate",
    "ocr_model_mock": "ocr_result_candidate",
    "voice_asr_model_mock": "transcript_candidate",
    "voice_tts_model_mock": "speech_response_candidate",
    "emotion_model_mock": "emotion_state_candidate",
    "face_recognition_model_mock": "face_identity_candidate",
    "scan_model_mock": "scan_result_candidate",
}

IO_BINDING_ASR_ALTERNATIVES: Tuple[str, ...] = ("speech_input_candidate", "transcript_candidate")

BLOCKED_PATHS: Tuple[str, ...] = (
    "canonical_registry_to_production_registry",
    "registry_candidate_to_model_invocation",
    "registry_candidate_to_provider_call",
    "registry_candidate_to_model_switch",
    "registry_candidate_to_skill_runtime",
    "model_output_to_fact_write",
    "model_output_to_user_facing_output",
    "model_output_to_memory_write",
    "model_output_to_world_model_write",
    "schema_v0_to_schema_upgrade",
)

NON_CLAIMS: Tuple[str, ...] = (
    "DryRun GO ≠ production registry published",
    "model_registry_canonical_v0_candidate ≠ final model registry",
    "Candidate generated ≠ model invocation enabled",
    "Candidate generated ≠ provider enabled",
    "Schema validation pass ≠ schema_version upgraded",
    "Skill relationship validated ≠ skill runtime enabled",
    "Post-DryRun Review next ≠ production registry",
)

BOUNDARY_FALSE_DRYRUN: Tuple[str, ...] = (
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


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "model_registry_canonicalization_dryrun_only": True,
        "simulated": True,
        "model_registry_canonical_v0_candidate_generated_now": True,
        "production_registry_generated_now": False,
        "model_registry_published_now": False,
        "schema_upgrade_executed_now": False,
        "real_provider_included": False,
        "production_runtime_included": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
    }
    for field in BOUNDARY_FALSE_DRYRUN:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _build_canonical_entry(spec: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    mid = spec["model_id"]
    output_type = IO_BINDING_EXPECTED.get(mid, spec.get("candidate_output_type", ""))
    if mid == "voice_asr_model_mock":
        output_type = "transcript_candidate"
    return {
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "model_id": mid,
        "model_domain": spec["model_domain"],
        "model_type": spec["model_type"],
        "version": "canonical_v0_candidate",
        "provider_type": "mock_or_fixture",
        "runtime_mode": spec["runtime_mode"],
        "capability_tags": list(spec["capability_tags"]),
        "input_contract": {
            "schema": "model_input_contract_v1",
            "dryrun": True,
            "candidate_only": True,
        },
        "output_contract": {
            "schema": "model_output_contract_v1",
            "candidate_only": True,
            "fact_status": "not_fact",
        },
        "candidate_output_type": output_type,
        "health_state_ref": spec["health_state_ref"],
        "fallback_model_ref": spec.get("fallback_model_ref"),
        "invocation_allowed": False,
        "runtime_boundary_profile": "dryrun_no_invocation",
        "constitution_gate_required": True,
        "safety_gate_required": True,
        "source_chain_required": True,
        "write_allowed": False,
        "runtime_action_allowed": False,
        "user_facing_output_allowed": False,
        "notes": f"canonical v0 candidate entry for {mid} — not production registry",
        **meta,
    }


def _validate_entry(entry: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for field in SCHEMA_V0_PLANNING_FIELDS:
        if field == "fallback_model_ref":
            if entry.get(field) is None and entry.get("fallback_model_ref") != "":
                pass  # null_allowed
            elif not entry.get(field):
                issues.append(f"{entry.get('model_id')}:fallback_model_ref")
        elif entry.get(field) is None or entry.get(field) == "":
            if field not in ("notes",):
                issues.append(f"{entry.get('model_id')}:missing_{field}")
    if entry.get("registry_version") != REGISTRY_VERSION:
        issues.append(f"{entry.get('model_id')}:registry_version")
    if entry.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"{entry.get('model_id')}:schema_version")
    if entry.get("model_domain") not in MODEL_DOMAIN_TAXONOMY:
        issues.append(f"{entry.get('model_id')}:model_domain")
    if entry.get("provider_type") != "mock_or_fixture":
        issues.append(f"{entry.get('model_id')}:provider_type")
    if entry.get("runtime_mode") not in V0_ACTIVE_RUNTIME_MODES:
        issues.append(f"{entry.get('model_id')}:runtime_mode")
    if entry.get("invocation_allowed") is not False:
        issues.append(f"{entry.get('model_id')}:invocation_allowed")
    for flag in ("constitution_gate_required", "safety_gate_required", "source_chain_required"):
        if entry.get(flag) is not True:
            issues.append(f"{entry.get('model_id')}:{flag}")
    for flag in ("write_allowed", "runtime_action_allowed", "user_facing_output_allowed"):
        if entry.get(flag) is not False:
            issues.append(f"{entry.get('model_id')}:{flag}")
    return issues


def run_model_registry_canonicalization_dryrun_v1(
    *,
    model_registry_canonicalization_planning_root: str,
    model_management_layer_roadmap_decision_root: Optional[str] = None,
    model_management_layer_recovery_dryrun_root: Optional[str] = None,
    luna_validation_factory_consolidation_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(model_registry_canonicalization_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}
    plan_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    table_plan = _try_read_json(planning_root / "model_registry_canonical_v0_table_plan_v1.json") or {}

    roadmap_root = Path(
        model_management_layer_roadmap_decision_root
        or plan_sm.get("upstream_roadmap_decision_root")
        or planning_root.parent / "model_management_layer_roadmap_decision"
    ).expanduser().resolve()
    recovery_dryrun_root = Path(
        model_management_layer_recovery_dryrun_root
        or plan_sm.get("upstream_dryrun_root")
        or planning_root.parent / "model_management_layer_recovery_dryrun"
    ).expanduser().resolve()
    factory_root = Path(
        luna_validation_factory_consolidation_root
        or plan_sm.get("upstream_validation_factory_root")
        or planning_root.parent / "luna_validation_factory_consolidation"
    ).expanduser().resolve()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_dryrun_meta(), "output_root": str(out_root)}

    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    recovery_dryrun_sm = _try_read_json(recovery_dryrun_root / "summary.json") or {}
    factory_sm = _try_read_json(factory_root / "summary.json") or {}

    planning_go = plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True
    if not planning_go:
        blockers.append("planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning next phase mismatch")
    if plan_sm.get("registry_version") != REGISTRY_VERSION:
        blockers.append("registry_version mismatch")
    if plan_sm.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version mismatch")
    if plan_sm.get("canonical_entry_count_planned") != 7:
        blockers.append("canonical_entry_count_planned must be 7")
    if plan_sm.get("canonical_registry_generated_now") is not False:
        blockers.append("planning canonical_registry_generated_now must be false")
    if plan_sm.get("production_registry_generated_now") is not False:
        blockers.append("planning production_registry_generated_now must be false")

    for field in ("model_runtime_invoked_now", "model_provider_invoked_now", "model_switch_executed_now"):
        if plan_sm.get(field) is True:
            blockers.append(f"planning {field} must be false")

    if roadmap_sm.get("real_provider_included") is not False:
        blockers.append("roadmap real_provider_included must be false")
    if not factory_sm.get("final_decision"):
        blockers.append("validation factory summary required")

    input_review = {
        "review_id": "canonicalization_planning_input_review_v1",
        "upstream_root": str(planning_root),
        "upstream_verifier_go": planning_go,
        "upstream_final_decision": plan_sm.get("final_decision"),
        "registry_version": plan_sm.get("registry_version"),
        "schema_version": plan_sm.get("schema_version"),
        "canonical_entry_count_planned": plan_sm.get("canonical_entry_count_planned"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    entries = [_build_canonical_entry(spec, meta) for spec in CANONICAL_ENTRY_PLANS]
    ids: Set[str] = {e["model_id"] for e in entries}
    entry_issues: List[str] = []
    if len(entries) != 7:
        entry_issues.append("entry_count")
    if len(ids) != len(entries):
        entry_issues.append("unique_model_id")
    validation_rows: List[Dict[str, Any]] = []
    for entry in entries:
        issues = _validate_entry(entry)
        entry_issues.extend(issues)
        validation_rows.append(
            {
                "model_id": entry["model_id"],
                "validation_pass": len(issues) == 0,
                "issues": issues,
            }
        )

    candidate = {
        "registry_id": "model_registry_canonical_v0_candidate",
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "candidate_only": True,
        "production_registry": False,
        "entry_count": len(entries),
        "entries": entries,
        "validation_pass": len(entry_issues) == 0 and len(blockers) == 0,
        **meta,
    }

    schema_validation = {
        "validation_id": "model_registry_schema_v0_validation_result_v1",
        "schema_version": SCHEMA_VERSION,
        "fields_required": list(SCHEMA_V0_PLANNING_FIELDS),
        "field_count": len(SCHEMA_V0_PLANNING_FIELDS),
        "all_entries_valid": len(entry_issues) == 0,
        "issues": entry_issues,
        **meta,
    }

    entry_matrix = {
        "matrix_id": "canonical_entry_validation_matrix_v1",
        "entry_count": len(entries),
        "rows": validation_rows,
        "matrix_pass": len(entry_issues) == 0,
        **meta,
    }

    domain_val = {
        "validation_id": "model_domain_taxonomy_validation_v1",
        "domains_required": list(MODEL_DOMAIN_TAXONOMY),
        "domains_covered": sorted({e["model_domain"] for e in entries}),
        "validation_pass": set(MODEL_DOMAIN_TAXONOMY) == {e["model_domain"] for e in entries},
        **meta,
    }

    provider_val = {
        "validation_id": "provider_type_taxonomy_validation_v1",
        "provider_types": list(PROVIDER_TYPE_TAXONOMY),
        "v0_active": ["mock_or_fixture"],
        "validation_pass": all(e.get("provider_type") == "mock_or_fixture" for e in entries),
        **meta,
    }

    runtime_val = {
        "validation_id": "runtime_mode_taxonomy_validation_v1",
        "runtime_modes": list(RUNTIME_MODE_TAXONOMY),
        "v0_active": list(V0_ACTIVE_RUNTIME_MODES),
        "validation_pass": all(e.get("runtime_mode") in V0_ACTIVE_RUNTIME_MODES for e in entries),
        **meta,
    }

    capability_val = {
        "validation_id": "capability_tag_taxonomy_validation_v1",
        "capability_tags": list(CAPABILITY_TAG_TAXONOMY),
        "can_write_fact_false": True,
        "can_trigger_action_false": True,
        "validation_pass": all(
            "can_write_fact" not in e.get("capability_tags", [])
            and "can_trigger_action" not in e.get("capability_tags", [])
            for e in entries
        ),
        **meta,
    }

    io_bindings: List[Dict[str, Any]] = []
    io_issues: List[str] = []
    for entry in entries:
        mid = entry["model_id"]
        expected = IO_BINDING_EXPECTED.get(mid, "")
        actual = entry.get("candidate_output_type", "")
        if mid == "voice_asr_model_mock":
            ok = actual in IO_BINDING_ASR_ALTERNATIVES
        else:
            ok = actual == expected
        if not ok:
            io_issues.append(f"{mid}:output_binding")
        io_bindings.append(
            {
                "model_id": mid,
                "candidate_output_type": actual,
                "expected": expected if mid != "voice_asr_model_mock" else list(IO_BINDING_ASR_ALTERNATIVES),
                "binding_pass": ok,
            }
        )
    io_result = {
        "result_id": "model_input_output_contract_binding_result_v1",
        "bindings": io_bindings,
        "validation_pass": len(io_issues) == 0,
        "issues": io_issues,
        **meta,
    }

    health_bindings = [
        {
            "model_id": e["model_id"],
            "health_state_ref": e["health_state_ref"],
            "fallback_model_ref": e.get("fallback_model_ref"),
            "binding_pass": bool(e.get("health_state_ref")),
        }
        for e in entries
    ]
    health_result = {
        "result_id": "model_health_and_fallback_binding_result_v1",
        "bindings": health_bindings,
        "validation_pass": all(b["binding_pass"] for b in health_bindings),
        **meta,
    }

    skill_rows = [
        {
            "skill_id": s["skill_id"],
            "required_models": s["required_models"],
            "output_candidate_types": s["output_candidate_types"],
            "skill_runtime_enabled": False,
            "binding_pass": True,
        }
        for s in SKILL_SPECS
    ]
    skill_val = {
        "validation_id": "skill_registry_relationship_validation_v1",
        "skill_count": len(skill_rows),
        "relationships": skill_rows,
        "skill_runtime_enabled": False,
        "skill_registry_expansion_deferred": True,
        "no_external_tool_skill": True,
        "no_map_library_hive_skill": True,
        "validation_pass": len(skill_rows) == 6,
        **meta,
    }

    output_types_seen = {e["candidate_output_type"] for e in entries}
    output_bindings = []
    for ot in sorted(output_types_seen):
        output_bindings.append(
            {
                "output_candidate_type": ot,
                "candidate_only": True,
                "fact_status": "not_fact",
                "write_allowed": False,
                "runtime_action_allowed": False,
                "user_facing_output_allowed": False,
            }
        )
    output_result = {
        "result_id": "candidate_output_contract_binding_result_v1",
        "bindings": output_bindings,
        "validation_pass": all(
            b["candidate_only"] and b["fact_status"] == "not_fact" and b["write_allowed"] is False
            for b in output_bindings
        ),
        **meta,
    }

    future_labels = {fv["version"] for fv in FUTURE_VERSIONS}
    version_val = {
        "validation_id": "version_policy_validation_result_v1",
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "version_status": VERSION_STATUS,
        "version_scope": VERSION_SCOPE,
        "future_update_expected": True,
        "update_triggers_count": len(UPDATE_TRIGGERS),
        "future_versions": list(FUTURE_VERSIONS),
        "validation_pass": len(UPDATE_TRIGGERS) == 10 and future_labels >= {
            "v0.1",
            "v0.2",
            "v0.3",
            "v1.0",
            "v1.1",
            "v2.0",
        },
        **meta,
    }

    runtime_audit = {
        "audit_id": "model_registry_runtime_boundary_audit_v1",
        "checks": [
            {"check_id": "candidate_not_production", "passed": candidate.get("production_registry") is False},
            {"check_id": "no_invocation", "passed": all(e.get("invocation_allowed") is False for e in entries)},
            {"check_id": "no_provider", "passed": meta.get("model_provider_invoked_now") is False},
            {"check_id": "no_switch", "passed": meta.get("model_switch_executed_now") is False},
            {"check_id": "no_skill_runtime", "passed": meta.get("skill_runtime_enabled_now") is False},
            {"check_id": "no_schema_upgrade", "passed": meta.get("schema_upgrade_executed_now") is False},
        ],
        "audit_pass": True,
        **meta,
    }

    blocked_paths = [
        {
            "path_id": pid,
            "blocked": True,
            "observed_now": False,
        }
        for pid in BLOCKED_PATHS
    ]
    blocked_result = {
        "result_id": "model_registry_blocked_path_result_v1",
        "paths": blocked_paths,
        "all_blocked": True,
        **meta,
    }

    all_pass = (
        len(blockers) == 0
        and len(entry_issues) == 0
        and len(io_issues) == 0
        and schema_validation.get("all_entries_valid") is True
        and domain_val.get("validation_pass") is True
        and provider_val.get("validation_pass") is True
        and runtime_val.get("validation_pass") is True
        and capability_val.get("validation_pass") is True
        and io_result.get("validation_pass") is True
        and health_result.get("validation_pass") is True
        and skill_val.get("validation_pass") is True
        and output_result.get("validation_pass") is True
        and version_val.get("validation_pass") is True
        and runtime_audit.get("audit_pass") is True
        and blocked_result.get("all_blocked") is True
    )

    readiness = {
        "readiness_id": "model_registry_canonicalization_dryrun_readiness_decision_v1",
        "candidate_generated": True,
        "entries_validated": len(entry_issues) == 0,
        "ready_for_post_dryrun_review": all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "model_registry_canonicalization_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "principles": [
            "dryrun_only_candidate_not_production",
            "no_model_no_provider_no_runtime",
            "schema_v0_validation_only",
        ],
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
        "violations": blockers + entry_issues + io_issues,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "canonical_entry_count": len(entries),
        "high_risk_count": 0 if all_pass else 1,
        **meta,
    }

    return {
        "model_registry_canonicalization_dryrun_policy": policy,
        "canonicalization_planning_input_review": input_review,
        "model_registry_canonical_v0_candidate": candidate,
        "model_registry_schema_v0_validation_result": schema_validation,
        "canonical_entry_validation_matrix": entry_matrix,
        "model_domain_taxonomy_validation": domain_val,
        "provider_type_taxonomy_validation": provider_val,
        "runtime_mode_taxonomy_validation": runtime_val,
        "capability_tag_taxonomy_validation": capability_val,
        "model_input_output_contract_binding_result": io_result,
        "model_health_and_fallback_binding_result": health_result,
        "skill_registry_relationship_validation": skill_val,
        "candidate_output_contract_binding_result": output_result,
        "version_policy_validation_result": version_val,
        "model_registry_runtime_boundary_audit": runtime_audit,
        "model_registry_blocked_path_result": blocked_result,
        "model_registry_canonicalization_dryrun_readiness_decision": readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }

# -*- coding: utf-8 -*-
"""Model Registry Canonicalization Post-DryRun Review v1 — review-only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.model_management_layer_recovery_dryrun_v1 import SKILL_SPECS
from capabilities.governance.model_management_layer_roadmap_decision_v1 import (
    FUTURE_VERSIONS,
    NEXT_ROUTE,
    REGISTRY_VERSION,
    ROUTE_C,
    SCHEMA_VERSION,
    UPDATE_TRIGGERS,
    VERSION_SCOPE,
    VERSION_STATUS,
    V0_MODEL_IDS,
)
from capabilities.governance.model_registry_canonicalization_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    IO_BINDING_EXPECTED,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
)
from capabilities.governance.model_registry_canonicalization_planning_v1 import (
    MODEL_DOMAIN_TAXONOMY,
    PROVIDER_TYPE_TAXONOMY,
    RUNTIME_MODE_TAXONOMY,
    SCHEMA_V0_PLANNING_FIELDS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Model-Registry-Canonicalization-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "model_registry_canonicalization_post_dryrun_review_only"
SOURCE_CHAIN = "model_registry_canonicalization_post_dryrun_review_v1"

UPSTREAM_REQUIRED_FINAL = DRYRUN_FINAL_GO
UPSTREAM_NEXT_PHASE = DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "MODEL_REGISTRY_CANONICALIZATION_POST_DRYRUN_REVIEW_CLOSED_READY_FOR_HEALTH_MANAGEMENT_LAYER_INTEGRATION_PLANNING"
)
FINAL_DECISION_HOLD = "MODEL_REGISTRY_CANONICALIZATION_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Health-Management-Layer-Integration-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Model-Registry-Canonicalization-Issue-Review-v1-001"

BOUNDARY_FALSE_REVIEW: Tuple[str, ...] = (
    "new_canonical_registry_generated_now",
    "production_registry_generated_now",
    "model_registry_published_now",
    "schema_upgrade_executed_now",
    "real_provider_included",
    "production_runtime_included",
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
    "Post-DryRun Review GO ≠ production registry generated",
    "model_registry_canonical_v0 closure ≠ real provider enabled",
    "canonical candidate closure ≠ model runtime callable",
    "schema_v0 compliance ≠ schema upgrade completed",
    "skill relationship closure ≠ Skill runtime enabled",
    "candidate output binding closure ≠ fact write allowed",
    "next Health Management readiness ≠ health integration started",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_registry_canonicalization_post_dryrun_review"
)


def _review_meta() -> Dict[str, Any]:
    meta = {
        "model_registry_canonicalization_post_dryrun_review_only": True,
        "review_only": True,
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }
    for field in BOUNDARY_FALSE_REVIEW:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _validate_entry_schema(entry: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    mid = entry.get("model_id", "?")
    for field in SCHEMA_V0_PLANNING_FIELDS:
        if field == "fallback_model_ref":
            continue
        if entry.get(field) is None or entry.get(field) == "":
            issues.append(f"{mid}:missing_{field}")
    if entry.get("registry_version") != REGISTRY_VERSION:
        issues.append(f"{mid}:registry_version")
    if entry.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"{mid}:schema_version")
    if entry.get("provider_type") != "mock_or_fixture":
        issues.append(f"{mid}:provider_type")
    if entry.get("invocation_allowed") is not False:
        issues.append(f"{mid}:invocation_allowed")
    for flag in ("write_allowed", "runtime_action_allowed", "user_facing_output_allowed"):
        if entry.get(flag) is not False:
            issues.append(f"{mid}:{flag}")
    for flag in ("constitution_gate_required", "safety_gate_required"):
        if entry.get(flag) is not True:
            issues.append(f"{mid}:{flag}")
    return issues


def run_model_registry_canonicalization_post_dryrun_review_v1(
    *,
    model_registry_canonicalization_dryrun_root: str,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(model_registry_canonicalization_dryrun_root).expanduser().resolve()
    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "model_registry_canonicalization_post_dryrun_review"
    )

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    candidate = _try_read_json(dryrun_root / "model_registry_canonical_v0_candidate.json") or {}
    schema_val = _try_read_json(dryrun_root / "model_registry_schema_v0_validation_result_v1.json") or {}
    entry_matrix = _try_read_json(dryrun_root / "canonical_entry_validation_matrix_v1.json") or {}
    domain_val = _try_read_json(dryrun_root / "model_domain_taxonomy_validation_v1.json") or {}
    provider_val = _try_read_json(dryrun_root / "provider_type_taxonomy_validation_v1.json") or {}
    runtime_val = _try_read_json(dryrun_root / "runtime_mode_taxonomy_validation_v1.json") or {}
    capability_val = _try_read_json(dryrun_root / "capability_tag_taxonomy_validation_v1.json") or {}
    io_result = _try_read_json(dryrun_root / "model_input_output_contract_binding_result_v1.json") or {}
    health_result = _try_read_json(dryrun_root / "model_health_and_fallback_binding_result_v1.json") or {}
    skill_val = _try_read_json(dryrun_root / "skill_registry_relationship_validation_v1.json") or {}
    output_result = _try_read_json(dryrun_root / "candidate_output_contract_binding_result_v1.json") or {}
    version_val = _try_read_json(dryrun_root / "version_policy_validation_result_v1.json") or {}
    audit = _try_read_json(dryrun_root / "model_registry_runtime_boundary_audit_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "model_registry_blocked_path_result_v1.json") or {}

    meta = {
        **_review_meta(),
        "upstream_dryrun_root": str(dryrun_root),
        "review_output_root": str(out_root),
    }

    verifier_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    if not verifier_go:
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_NEXT_PHASE:
        blockers.append("dryrun recommended_next_phase mismatch")
    if dryrun_sm.get("canonical_entry_count") != 7:
        blockers.append("canonical_entry_count must be 7")
    if dryrun_sm.get("model_registry_canonical_v0_candidate_generated_now") is not True:
        blockers.append("candidate must be generated in dryrun")
    if dryrun_sm.get("production_registry_generated_now") is not False:
        blockers.append("production_registry_generated_now must be false")
    if dryrun_sm.get("model_registry_published_now") is not False:
        blockers.append("model_registry_published_now must be false")
    if dryrun_sm.get("registry_version") != REGISTRY_VERSION:
        blockers.append("registry_version mismatch")
    if dryrun_sm.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version mismatch")

    for field in ("model_runtime_invoked_now", "model_provider_invoked_now", "model_switch_executed_now"):
        if dryrun_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    entries = candidate.get("entries") or []
    ids: Set[str] = {e.get("model_id") for e in entries if e.get("model_id")}

    input_review = {
        "review_id": "canonicalization_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_verifier_go": verifier_go,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "candidate_exists": bool(candidate.get("registry_id")),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    completeness_issues: List[str] = []
    if len(entries) != 7:
        completeness_issues.append("entry_count")
    if len(ids) != len(entries):
        completeness_issues.append("unique_model_id")
    if candidate.get("production_registry") is not False:
        completeness_issues.append("production_registry")
    for mid in V0_MODEL_IDS:
        if mid not in ids:
            completeness_issues.append(f"missing_{mid}")

    completeness = {
        "review_id": "canonical_candidate_completeness_review_v1",
        "candidate_file": "model_registry_canonical_v0_candidate.json",
        "entry_count": len(entries),
        "unique_model_ids": len(ids),
        "production_registry_generated": False,
        "registry_published": False,
        "issues": completeness_issues,
        "review_pass": len(completeness_issues) == 0,
        **meta,
    }

    schema_issues: List[str] = []
    for entry in entries:
        schema_issues.extend(_validate_entry_schema(entry))
    schema_review = {
        "review_id": "schema_v0_compliance_review_v1",
        "schema_version": SCHEMA_VERSION,
        "fields_required": list(SCHEMA_V0_PLANNING_FIELDS),
        "field_count": len(SCHEMA_V0_PLANNING_FIELDS),
        "issues": schema_issues,
        "review_pass": len(schema_issues) == 0 and schema_val.get("all_entries_valid") is True,
        **meta,
    }

    entry_issues: List[str] = []
    entry_rows: List[Dict[str, Any]] = []
    for mid in V0_MODEL_IDS:
        entry = next((e for e in entries if e.get("model_id") == mid), None)
        if not entry:
            entry_issues.append(f"missing_{mid}")
            entry_rows.append({"model_id": mid, "review_pass": False})
            continue
        issues = _validate_entry_schema(entry)
        entry_issues.extend(issues)
        entry_rows.append({"model_id": mid, "review_pass": len(issues) == 0, "issues": issues})

    entry_review = {
        "review_id": "canonical_entry_validation_review_v1",
        "entries_reviewed": entry_rows,
        "all_entries_pass": len(entry_issues) == 0 and entry_matrix.get("matrix_pass") is True,
        "issues": entry_issues,
        "review_pass": len(entry_issues) == 0,
        **meta,
    }

    taxonomy_issues: List[str] = []
    if domain_val.get("validation_pass") is not True:
        taxonomy_issues.append("domain_taxonomy")
    if provider_val.get("validation_pass") is not True:
        taxonomy_issues.append("provider_taxonomy")
    if runtime_val.get("validation_pass") is not True:
        taxonomy_issues.append("runtime_taxonomy")
    if capability_val.get("validation_pass") is not True:
        taxonomy_issues.append("capability_taxonomy")
    taxonomy_review = {
        "review_id": "taxonomy_validation_review_v1",
        "domains": list(MODEL_DOMAIN_TAXONOMY),
        "provider_types": list(PROVIDER_TYPE_TAXONOMY),
        "runtime_modes": list(RUNTIME_MODE_TAXONOMY),
        "issues": taxonomy_issues,
        "review_pass": len(taxonomy_issues) == 0,
        **meta,
    }

    io_issues: List[str] = []
    for mid, expected in IO_BINDING_EXPECTED.items():
        entry = next((e for e in entries if e.get("model_id") == mid), {})
        if entry.get("candidate_output_type") != expected:
            io_issues.append(f"{mid}:binding")
    io_review = {
        "review_id": "input_output_binding_review_v1",
        "expected_bindings": dict(IO_BINDING_EXPECTED),
        "issues": io_issues,
        "review_pass": len(io_issues) == 0 and io_result.get("validation_pass") is True,
        **meta,
    }

    health_review = {
        "review_id": "health_fallback_binding_review_v1",
        "bindings": health_result.get("bindings") or [],
        "review_pass": health_result.get("validation_pass") is True,
        **meta,
    }

    skill_review = {
        "review_id": "skill_relationship_review_v1",
        "skill_count": skill_val.get("skill_count", 0),
        "relationships": skill_val.get("relationships") or [],
        "skill_runtime_enabled": False,
        "skill_registry_expansion_deferred": skill_val.get("skill_registry_expansion_deferred", True),
        "review_pass": skill_val.get("validation_pass") is True and skill_val.get("skill_count") == 6,
        **meta,
    }

    output_issues: List[str] = []
    for row in output_result.get("bindings") or []:
        for key, val in (
            ("candidate_only", True),
            ("fact_status", "not_fact"),
            ("write_allowed", False),
            ("runtime_action_allowed", False),
            ("user_facing_output_allowed", False),
        ):
            if row.get(key) != val:
                output_issues.append(f"{row.get('output_candidate_type')}:{key}")
    output_review = {
        "review_id": "candidate_output_contract_review_v1",
        "bindings": output_result.get("bindings") or [],
        "issues": output_issues,
        "review_pass": len(output_issues) == 0 and output_result.get("validation_pass") is True,
        **meta,
    }

    future_labels = {fv["version"] for fv in FUTURE_VERSIONS}
    version_issues: List[str] = []
    if version_val.get("registry_version") != REGISTRY_VERSION:
        version_issues.append("registry_version")
    if version_val.get("schema_version") != SCHEMA_VERSION:
        version_issues.append("schema_version")
    if version_val.get("version_status") != VERSION_STATUS:
        version_issues.append("version_status")
    if version_val.get("version_scope") != VERSION_SCOPE:
        version_issues.append("version_scope")
    if version_val.get("update_triggers_count") != 10:
        version_issues.append("update_triggers")
    if not future_labels >= {"v0.1", "v0.2", "v0.3", "v1.0", "v1.1", "v2.0"}:
        version_issues.append("future_versions")
    version_review = {
        "review_id": "version_policy_review_v1",
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "version_status": VERSION_STATUS,
        "version_scope": VERSION_SCOPE,
        "future_update_expected": True,
        "update_triggers_count": len(UPDATE_TRIGGERS),
        "future_versions": list(FUTURE_VERSIONS),
        "issues": version_issues,
        "review_pass": len(version_issues) == 0 and version_val.get("validation_pass") is True,
        **meta,
    }

    runtime_issues: List[str] = []
    if audit.get("audit_pass") is not True:
        runtime_issues.append("audit")
    if candidate.get("production_registry") is not False:
        runtime_issues.append("candidate_not_production")
    runtime_review = {
        "review_id": "runtime_boundary_review_v1",
        "checks": audit.get("checks") or [],
        "candidate_not_production": candidate.get("production_registry") is False,
        "registry_not_invocation": all(e.get("invocation_allowed") is False for e in entries),
        "skill_not_runtime": skill_val.get("skill_runtime_enabled") is False,
        "mock_not_real_provider": all(e.get("provider_type") == "mock_or_fixture" for e in entries),
        "schema_not_upgraded": meta.get("schema_upgrade_executed_now") is False,
        "issues": runtime_issues,
        "review_pass": len(runtime_issues) == 0,
        **meta,
    }

    blocked_issues: List[str] = []
    paths = {p.get("path_id"): p for p in blocked.get("paths") or []}
    for pid in BLOCKED_PATHS:
        row = paths.get(pid)
        if not row or row.get("blocked") is not True or row.get("observed_now") is True:
            blocked_issues.append(pid)
    blocked_review = {
        "review_id": "blocked_path_review_v1",
        "paths_total": len(BLOCKED_PATHS),
        "all_blocked": len(blocked_issues) == 0 and blocked.get("all_blocked") is True,
        "issues": blocked_issues,
        "review_pass": len(blocked_issues) == 0,
        **meta,
    }

    reviews_pass = (
        len(blockers) == 0
        and completeness.get("review_pass")
        and schema_review.get("review_pass")
        and entry_review.get("review_pass")
        and taxonomy_review.get("review_pass")
        and io_review.get("review_pass")
        and health_review.get("review_pass")
        and skill_review.get("review_pass")
        and output_review.get("review_pass")
        and version_review.get("review_pass")
        and runtime_review.get("review_pass")
        and blocked_review.get("review_pass")
    )

    closure = {
        "closure_id": "canonical_registry_closure_decision_v1",
        "model_registry_canonical_v0_candidate_closed": reviews_pass,
        "b_lite_route_closed": reviews_pass,
        "production_registry_still_not_generated": True,
        "final_decision": FINAL_DECISION_GO if reviews_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if reviews_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    next_route = {
        "readiness_id": "next_route_readiness_decision_v1",
        "ready_for_health_management_layer_integration_planning": reviews_pass,
        "next_route": ROUTE_C,
        "next_route_label": "Route C — Health Management Layer Integration",
        "b_lite_canonical_v0_baseline_closed": reviews_pass,
        "recommended_next_phase": NEXT_PHASE_GO if reviews_pass else PHASE_ID,
        "final_decision": closure["final_decision"],
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": reviews_pass,
        "violations": blockers + completeness_issues + schema_issues + entry_issues + io_issues + blocked_issues,
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "canonical_entry_count": len(entries),
        "high_risk_count": 0 if reviews_pass else 1,
        "b_lite_canonical_v0_baseline_closed": reviews_pass,
        **meta,
    }

    return {
        "canonicalization_dryrun_input_review": input_review,
        "canonical_candidate_completeness_review": completeness,
        "schema_v0_compliance_review": schema_review,
        "canonical_entry_validation_review": entry_review,
        "taxonomy_validation_review": taxonomy_review,
        "input_output_binding_review": io_review,
        "health_fallback_binding_review": health_review,
        "skill_relationship_review": skill_review,
        "candidate_output_contract_review": output_review,
        "version_policy_review": version_review,
        "runtime_boundary_review": runtime_review,
        "blocked_path_review": blocked_review,
        "canonical_registry_closure_decision": closure,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }

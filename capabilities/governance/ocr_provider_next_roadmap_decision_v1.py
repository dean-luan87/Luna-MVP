# -*- coding: utf-8 -*-
"""OCR Provider Next Roadmap Decision v1 — Route B Vision/Voice harness adoption selected."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.controlled_provider_readiness_harness_v1 import (
    ANTI_RECURSION,
    FINAL_DECISION_GO as HARNESS_FINAL_GO,
    FUTURE_CONSUMERS,
    HARNESS_ID,
    NEXT_PHASE_GO as HARNESS_NEXT_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-OCR-Provider-Next-Roadmap-Decision-v1-001"
SCOPE = "ocr_provider_next_roadmap_decision_only"
SOURCE_CHAIN = "ocr_provider_next_roadmap_decision_v1"

UPSTREAM_HARNESS_FINAL = HARNESS_FINAL_GO
UPSTREAM_HARNESS_NEXT = HARNESS_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_PROVIDER_NEXT_ROADMAP_DECISION_READY_FOR_VISION_VOICE_PROVIDER_HARNESS_ADOPTION_PLANNING"
)
FINAL_DECISION_HOLD = "OCR_PROVIDER_NEXT_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Vision-Voice-Provider-Harness-Adoption-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Next-Roadmap-Issue-Review-v1-001"

ROUTE_A = "Route A — Continue OCR Provider Authorization Planning"
ROUTE_B = "Route B — Vision / Voice Harness Adoption Planning"
ROUTE_C = "Route C — OCR Real Dependency Check Authorization"
ROUTE_D = "Route D — Pause Provider Work and Return to Midplatform / Visual Context Governance"

SELECTED_ROUTE = ROUTE_B
DEFERRED_ROUTE_A = ROUTE_A
BLOCKED_ROUTE_C = ROUTE_C
DEFERRED_ROUTE_D = ROUTE_D

REQUIRED_FUTURE_DOMAINS: Set[str] = {"vision", "voice", "map", "library", "hive", "memory"}

BOUNDARY_FALSE: Tuple[str, ...] = (
    "ocr_authorization_started_now",
    "ocr_real_dependency_check_authorization_started_now",
    "vision_harness_adoption_started_now",
    "voice_harness_adoption_started_now",
    "provider_runtime_enabled_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "controlled_trial_started_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ OCR provider authorization enabled",
    "Route B selected ≠ Vision/Voice provider runtime enabled",
    "Route B selected ≠ domain_config executed for Vision/Voice",
    "deferred Route A ≠ OCR authorization abandoned forever",
    "blocked Route C ≠ real dependency check abandoned forever",
    "harness adoption planning next ≠ provider import/install",
    "OCR chain mature ≠ duplicate selection→real-dep long chain required",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_next_roadmap_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_next_roadmap_decision_only": True,
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


def run_ocr_provider_next_roadmap_decision_v1(
    *,
    controlled_provider_readiness_harness_root: str,
    ocr_provider_real_dependency_check_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_selection_dependency_environment_post_dryrun_review_root: Optional[str] = None,
    ocr_controlled_provider_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    harness_root = Path(controlled_provider_readiness_harness_root).expanduser().resolve()
    harness_sm = _try_read_json(harness_root / "summary.json") or {}
    harness_vr = _try_read_json(harness_root / "verifier_report.json") or {}
    validation = _try_read_json(
        harness_root / "controlled_provider_readiness_harness_validation_result_v1.json"
    ) or {}
    harness_contract = _try_read_json(
        harness_root / "controlled_provider_readiness_harness_contract_v1.json"
    ) or {}
    future_plan = _try_read_json(harness_root / "future_consumer_adoption_plan_v1.json") or {}
    ocr_mapping = _try_read_json(harness_root / "ocr_first_consumer_mapping_v1.json") or {}

    real_post_root = Path(
        ocr_provider_real_dependency_check_post_dryrun_review_root
        or harness_root.parent / "ocr_provider_real_dependency_check_post_dryrun_review"
    ).expanduser().resolve()
    sel_post_root = Path(
        ocr_provider_selection_dependency_environment_post_dryrun_review_root
        or harness_root.parent / "ocr_provider_selection_dependency_environment_post_dryrun_review"
    ).expanduser().resolve()
    ocr_post_root = Path(
        ocr_controlled_provider_post_dryrun_review_root
        or harness_root.parent / "ocr_controlled_provider_post_dryrun_review"
    ).expanduser().resolve()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_boundary_meta(),
        "upstream_harness_root": str(harness_root),
        "upstream_real_dep_post_root": str(real_post_root),
        "upstream_selection_post_root": str(sel_post_root),
        "upstream_ocr_controlled_post_root": str(ocr_post_root),
        "output_root": str(out_root),
        "harness_id": HARNESS_ID,
    }

    harness_go = harness_vr.get("verifier") == "GO" and harness_vr.get("passed") is True
    if not harness_go:
        blockers.append("harness verifier must be GO")
    if harness_sm.get("final_decision") != UPSTREAM_HARNESS_FINAL:
        blockers.append("harness final_decision mismatch")
    if harness_sm.get("recommended_next_phase") != UPSTREAM_HARNESS_NEXT:
        blockers.append("harness recommended_next_phase mismatch")
    if harness_sm.get("harness_id") != HARNESS_ID:
        blockers.append("harness_id mismatch")
    if validation.get("ocr_first_consumer_validated") is not True:
        blockers.append("OCR first consumer must be validated")
    if validation.get("harness_global_enforcement_now") is True:
        blockers.append("harness must not be globally enforced now")
    if harness_sm.get("harness_runtime_enforced_globally_now") is True:
        blockers.append("harness_runtime_enforced_globally_now must be false")

    registered_domains = {c.get("domain") for c in future_plan.get("consumers") or []}
    if not REQUIRED_FUTURE_DOMAINS.issubset(registered_domains):
        blockers.append("future consumers Vision/Voice/Map/Library/Hive/Memory must be registered")
    if "vision" not in registered_domains or "voice" not in registered_domains:
        blockers.append("vision and voice must be in future consumer plan")

    anti_rules = harness_contract.get("anti_recursion_rules") or []
    if len(anti_rules) < len(ANTI_RECURSION):
        blockers.append("anti_recursion rules must be present in harness contract")

    if ocr_mapping.get("first_consumer_status") != "validated":
        blockers.append("ocr first_consumer_status must be validated")

    sel_post_sm = _try_read_json(sel_post_root / "summary.json") or {}
    ocr_post_sm = _try_read_json(ocr_post_root / "summary.json") or {}
    real_post_sm = _try_read_json(real_post_root / "summary.json") or {}

    if sel_post_sm.get("ocr_provider_selection_dependency_environment_dryrun_closed") is not True:
        blockers.append("OCR selection dryrun should be closed")
    if ocr_post_sm.get("ocr_controlled_provider_dryrun_closed") is not True:
        blockers.append("OCR controlled provider dryrun should be closed")
    if real_post_sm.get("ocr_provider_real_dependency_check_dryrun_closed") is not True:
        blockers.append("OCR real dependency dryrun should be closed")

    for field in (
        "provider_imported_now",
        "provider_invoked_now",
        "dependency_install_executed_now",
        "model_download_executed_now",
    ):
        if harness_sm.get(field) is True:
            blockers.append(f"harness {field} must be false")

    input_review = {
        "review_id": "controlled_provider_readiness_harness_input_review_v1",
        "upstream_harness_root": str(harness_root),
        "upstream_verifier_go": harness_go,
        "upstream_final_decision": harness_sm.get("final_decision"),
        "harness_id": harness_sm.get("harness_id"),
        "ocr_first_consumer_validated": validation.get("ocr_first_consumer_validated"),
        "future_consumer_domains": sorted(registered_domains),
        "anti_recursion_active": len(anti_rules) >= len(ANTI_RECURSION),
        "ocr_chain_duplicate_long_chain_not_required": True,
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_continue_ocr_authorization_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "deferred",
        "defer_reasons": [
            "OCR chain is mature but harness was just extracted — second consumer not yet validated",
            "immediate authorization continues single-domain push and reduces harness generalization value",
            "may resume after Vision/Voice adoption planning",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_vision_voice_harness_adoption_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "selected",
        "selection_reasons": [
            "harness validated with OCR as first consumer",
            "Vision and Voice are remaining foundation chains in three-chain optimization",
            "domain_config + adoption planning only — no real provider runtime",
            "validates harness is not OCR-specific pseudo-generic module",
            "prevents Vision/Voice from copying OCR selection→real-dep long chain",
        ],
        "planning_scope": ["vision_domain_config", "voice_domain_config", "harness_adoption_planning"],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_ocr_real_dependency_authorization_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "blocked_until_explicit_authorization",
        "block_reasons": [
            "real dependency check requires explicit authorization, execution window, sandbox, rollback, evidence pack",
            "do not open real checks now",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_pause_provider_return_midplatform_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "deferred",
        "defer_reasons": [
            "Visual Context Governance remains important",
            "provider readiness harness just closed — generalization validation should complete first",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "ocr_provider_next_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "deferred"},
            {"route": ROUTE_B, "status": "selected"},
            {"route": ROUTE_C, "status": "blocked_until_explicit_authorization"},
            {"route": ROUTE_D, "status": "deferred"},
        ],
        "selected_route": SELECTED_ROUTE,
        "deferred_route_a": DEFERRED_ROUTE_A,
        "blocked_route_c": BLOCKED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        **meta,
    }

    preconditions = {
        "preconditions_id": "selected_route_preconditions_v1",
        "selected_route": SELECTED_ROUTE,
        "preconditions": [
            "controlled_provider_readiness_harness_v1 GO",
            "OCR first consumer validated",
            "harness_runtime_enforced_globally_now=false",
            "no import/install/download/invoke in harness extraction",
            "anti_recursion active",
        ],
        "forbidden_now": [
            "OCR provider authorization",
            "OCR real dependency check execution",
            "Vision/Voice provider runtime",
            "provider import/install/download",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_items": [
            {"route": ROUTE_A, "status": "deferred", "resume_after": "vision_voice_harness_adoption_planning"},
            {"route": ROUTE_C, "status": "blocked_until_explicit_authorization", "resume_after": "authorization_planning"},
            {"route": ROUTE_D, "status": "deferred", "note": "midplatform/visual context after harness generalization"},
        ],
        **meta,
    }

    decision_ok = len(blockers) == 0
    boundary_ok = decision_ok

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_vision_voice_provider_harness_adoption_planning": boundary_ok,
        "selected_route": SELECTED_ROUTE,
        "do_not_start_ocr_authorization_now": True,
        "do_not_start_real_dependency_check_now": True,
        "do_not_enable_vision_voice_provider_now": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_provider_next_roadmap_decision_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
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
        "final_decision": next_readiness["final_decision"],
        "recommended_next_phase": next_readiness["recommended_next_phase"],
        "selected_route": SELECTED_ROUTE,
        "deferred_route_a": DEFERRED_ROUTE_A,
        "blocked_route_c": BLOCKED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "ocr_provider_next_roadmap_decision_policy": policy,
        "controlled_provider_readiness_harness_input_review": input_review,
        "route_a_continue_ocr_authorization_assessment": route_a,
        "route_b_vision_voice_harness_adoption_assessment": route_b,
        "route_c_ocr_real_dependency_authorization_assessment": route_c,
        "route_d_pause_provider_return_midplatform_assessment": route_d,
        "ocr_provider_next_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }

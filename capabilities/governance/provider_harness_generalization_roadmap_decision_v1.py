# -*- coding: utf-8 -*-
"""Provider Harness Generalization Roadmap Decision v1 — Route B Validation Factory registration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.controlled_provider_readiness_harness_v1 import (
    ANTI_RECURSION,
    FINAL_DECISION_GO as HARNESS_FINAL_GO,
    FUTURE_CONSUMERS,
    HARNESS_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_next_roadmap_decision_v1 import SELECTED_ROUTE as PRIOR_ROADMAP_SELECTED
from capabilities.governance.vision_voice_provider_harness_adoption_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
)

PHASE_ID = "Phase-Provider-Harness-Generalization-Roadmap-Decision-v1-001"
SCOPE = "provider_harness_generalization_roadmap_decision_only"
SOURCE_CHAIN = "provider_harness_generalization_roadmap_decision_v1"

UPSTREAM_POST_REVIEW_FINAL = POST_REVIEW_FINAL_GO
UPSTREAM_POST_REVIEW_NEXT = POST_REVIEW_NEXT_PHASE

FINAL_DECISION_GO = (
    "PROVIDER_HARNESS_GENERALIZATION_ROADMAP_DECISION_READY_FOR_VALIDATION_FACTORY_REGISTRATION_PLANNING"
)
FINAL_DECISION_HOLD = "PROVIDER_HARNESS_GENERALIZATION_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = (
    "Phase-Controlled-Provider-Readiness-Harness-Validation-Factory-Registration-Planning-v1-001"
)
NEXT_PHASE_HOLD = "Phase-Provider-Harness-Generalization-Roadmap-Issue-Review-v1-001"

ROUTE_A = "Route A — Return to OCR Provider Authorization"
ROUTE_B = "Route B — Register Controlled Provider Readiness Harness into Luna Validation Factory"
ROUTE_C = "Route C — Adopt Map / Library / Hive / Memory as Future Consumers"
ROUTE_D = "Route D — Pause Provider Work and Return to Visual Context Governance"

SELECTED_ROUTE = ROUTE_B
DEFERRED_ROUTE_A = "Return to OCR Provider Authorization"
DEFERRED_ROUTE_C = "Map / Library / Hive / Memory Future Consumer Adoption"
DEFERRED_ROUTE_D = "Visual Context Governance"

FUTURE_ONLY_DOMAINS: Set[str] = {"map", "library", "hive", "memory"}
VALIDATED_CONSUMER_DOMAINS: Set[str] = {"ocr", "vision", "voice"}

VALIDATION_FACTORY_BASE_MODULES: Tuple[str, ...] = (
    "batch_preflight_harness",
    "single_chain_trial_validation_harness",
    "controlled_trial_authorization_harness",
    "candidate_output_contract",
    "no_runtime_boundary_audit",
    "controlled_trial_post_execution_review_harness",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "harness_runtime_enforced_globally_now",
    "ocr_authorization_started_now",
    "validation_factory_registration_started_now",
    "map_library_hive_memory_adoption_started_now",
    "visual_context_governance_started_now",
    "provider_runtime_enabled_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "real_dependency_check_executed_now",
    "controlled_trial_started_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ Validation Factory runtime enforced",
    "Route B selected ≠ provider readiness harness globally enforced",
    "Route B selected ≠ OCR authorization started",
    "deferred Route A ≠ OCR authorization abandoned",
    "deferred Route C ≠ Map/Library/Hive/Memory adopted now",
    "deferred Route D ≠ Visual Context Governance abandoned",
    "Factory registration planning next ≠ provider import/install/invoke",
    "three consumer validated ≠ all future consumers adopted",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/provider_harness_generalization_roadmap_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "provider_harness_generalization_roadmap_decision_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "harness_id": HARNESS_ID,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_provider_harness_generalization_roadmap_decision_v1(
    *,
    vision_voice_provider_harness_adoption_post_dryrun_review_root: str,
    vision_voice_provider_harness_adoption_dryrun_root: Optional[str] = None,
    controlled_provider_readiness_harness_root: Optional[str] = None,
    luna_validation_factory_consolidation_root: Optional[str] = None,
    ocr_provider_next_roadmap_decision_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    post_root = Path(vision_voice_provider_harness_adoption_post_dryrun_review_root).expanduser().resolve()
    post_sm = _try_read_json(post_root / "summary.json") or {}
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}
    closure = _try_read_json(post_root / "vision_voice_harness_adoption_closure_decision_v1.json") or {}
    gen_review = _try_read_json(post_root / "harness_generalization_review_v1.json") or {}

    dryrun_root = Path(
        vision_voice_provider_harness_adoption_dryrun_root
        or post_root.parent / "vision_voice_provider_harness_adoption_dryrun"
    ).expanduser().resolve()
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    dryrun_gen = _try_read_json(dryrun_root / "harness_generalization_dryrun_result_v1.json") or {}

    harness_root = Path(
        controlled_provider_readiness_harness_root
        or post_root.parent / "controlled_provider_readiness_harness"
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

    factory_root = Path(
        luna_validation_factory_consolidation_root
        or post_root.parent / "luna_validation_factory_consolidation"
    ).expanduser().resolve()
    factory_sm = _try_read_json(factory_root / "summary.json") or {}
    factory_vr = _try_read_json(factory_root / "verifier_report.json") or {}
    factory_registry = _try_read_json(factory_root / "validation_factory_module_registry_v1.json") or {}

    prior_roadmap_root = Path(
        ocr_provider_next_roadmap_decision_root
        or post_root.parent / "ocr_provider_next_roadmap_decision"
    ).expanduser().resolve()
    prior_roadmap_sm = _try_read_json(prior_roadmap_root / "summary.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_boundary_meta(),
        "upstream_post_review_root": str(post_root),
        "upstream_dryrun_root": str(dryrun_root),
        "upstream_harness_root": str(harness_root),
        "upstream_validation_factory_root": str(factory_root),
        "upstream_prior_roadmap_root": str(prior_roadmap_root),
        "output_root": str(out_root),
    }

    post_go = post_vr.get("verifier") == "GO" and post_vr.get("passed") is True
    if not post_go:
        blockers.append("post-dryrun review verifier must be GO")
    if post_sm.get("final_decision") != UPSTREAM_POST_REVIEW_FINAL:
        blockers.append("post-review final_decision mismatch")
    if post_sm.get("recommended_next_phase") != UPSTREAM_POST_REVIEW_NEXT:
        blockers.append("post-review recommended_next_phase mismatch")
    if post_sm.get("harness_generalization_established") is not True:
        blockers.append("harness_generalization_established must be true")
    if closure.get("ocr_vision_voice_three_consumer_harness_validated") is not True:
        blockers.append("three consumer harness must be validated")

    dryrun_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    if not dryrun_go:
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("boundary_ok") is not True:
        blockers.append("dryrun boundary_ok must be true")
    if dryrun_gen.get("vision_second_consumer_dryrun_pass") is not True:
        blockers.append("vision second consumer dryrun pass required")
    if dryrun_gen.get("voice_third_consumer_dryrun_pass") is not True:
        blockers.append("voice third consumer dryrun pass required")

    if gen_review.get("review_pass") is not True:
        blockers.append("harness generalization review must pass")
    if gen_review.get("vision_second_consumer_dryrun_pass") is not True:
        blockers.append("vision second consumer post-review pass required")
    if gen_review.get("voice_third_consumer_dryrun_pass") is not True:
        blockers.append("voice third consumer post-review pass required")

    harness_go = harness_vr.get("verifier") == "GO" and harness_vr.get("passed") is True
    if not harness_go:
        blockers.append("controlled_provider_readiness_harness verifier must be GO")
    if harness_sm.get("harness_id") != HARNESS_ID:
        blockers.append("harness_id must be controlled_provider_readiness_harness_v1")
    if validation.get("ocr_first_consumer_validated") is not True:
        blockers.append("OCR first consumer must be validated")
    if harness_sm.get("harness_runtime_enforced_globally_now") is True:
        blockers.append("harness_runtime_enforced_globally_now must be false")
    if validation.get("harness_global_enforcement_now") is True:
        blockers.append("harness must not be globally enforced")

    anti_rules = harness_contract.get("anti_recursion_rules") or []
    if len(anti_rules) < len(ANTI_RECURSION):
        blockers.append("anti_recursion must be preserved in harness contract")

    for field in (
        "provider_imported_now",
        "provider_invoked_now",
        "dependency_install_executed_now",
        "model_download_executed_now",
    ):
        if harness_sm.get(field) is True or dryrun_sm.get(field) is True or post_sm.get(field) is True:
            blockers.append(f"{field} must be false across chain")

    factory_go = factory_vr.get("verifier") == "GO" and factory_vr.get("passed") is True
    if not factory_go:
        blockers.append("luna_validation_factory_consolidation verifier should be GO")
    if factory_sm.get("validation_factory_runtime_enforced_now") is True:
        blockers.append("validation factory must not be runtime enforced now")

    registry_modules = {m.get("module_id") for m in factory_registry.get("modules") or []}
    for mid in VALIDATION_FACTORY_BASE_MODULES:
        if mid not in registry_modules:
            blockers.append(f"validation factory missing module {mid}")

    consumer_status = {c.get("domain"): c.get("status") for c in future_plan.get("consumers") or []}
    for domain in FUTURE_ONLY_DOMAINS:
        if consumer_status.get(domain) not in ("planned", "future_only"):
            blockers.append(f"{domain} must remain future/planned only")
    if future_plan.get("future_consumer_runtime_enabled_now") is True:
        blockers.append("future consumer runtime must not be enabled")

    if prior_roadmap_sm.get("selected_route") != PRIOR_ROADMAP_SELECTED:
        blockers.append("prior OCR roadmap should have selected Vision/Voice harness adoption")

    input_review = {
        "review_id": "vision_voice_post_review_input_review_v1",
        "upstream_post_review_root": str(post_root),
        "upstream_dryrun_root": str(dryrun_root),
        "upstream_harness_root": str(harness_root),
        "upstream_validation_factory_root": str(factory_root),
        "post_review_verifier_go": post_go,
        "post_review_final_decision": post_sm.get("final_decision"),
        "dryrun_verifier_go": dryrun_go,
        "harness_verifier_go": harness_go,
        "factory_consolidation_verifier_go": factory_go,
        "ocr_first_consumer_validated": validation.get("ocr_first_consumer_validated"),
        "three_consumer_harness_validated": closure.get("ocr_vision_voice_three_consumer_harness_validated"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    harness_generalization_review = {
        "review_id": "controlled_provider_readiness_harness_generalization_review_v1",
        "harness_id": HARNESS_ID,
        "ocr_first_consumer_validated": validation.get("ocr_first_consumer_validated"),
        "vision_second_consumer_dryrun_pass": dryrun_gen.get("vision_second_consumer_dryrun_pass"),
        "vision_second_consumer_post_review_pass": gen_review.get("review_pass"),
        "voice_third_consumer_dryrun_pass": dryrun_gen.get("voice_third_consumer_dryrun_pass"),
        "voice_third_consumer_post_review_pass": gen_review.get("review_pass"),
        "map_library_hive_memory_future_only": dryrun_gen.get("map_library_hive_memory_future_only"),
        "no_ocr_specific_fields_leak": dryrun_gen.get("no_ocr_specific_fields_leak"),
        "anti_recursion_preserved": len(anti_rules) >= len(ANTI_RECURSION),
        "generalization_review_pass": len(blockers) == 0,
        "validated_consumer_domains": sorted(VALIDATED_CONSUMER_DOMAINS),
        "future_only_domains": sorted(FUTURE_ONLY_DOMAINS),
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_return_ocr_authorization_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "deferred_next",
        "defer_reasons": [
            "OCR authorization is a reasonable next step after harness generalization",
            "Harness just completed OCR / Vision / Voice three-consumer validation",
            "Register harness into Validation Factory first to avoid OCR single-line divergence",
            "Resume OCR authorization after factory registration planning + dryrun",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_validation_factory_registration_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "selected",
        "selection_reasons": [
            "OCR / Vision / Voice three consumers validated via harness",
            "Harness is a reusable provider readiness factory, not OCR-specific",
            "Luna Validation Factory already consolidates BatchPreflight / SingleChainTrial / "
            "ControlledTrialAuthorization / CandidateOutput / NoRuntimeBoundary / PostExecutionReview",
            "Provider Readiness should become a factory-level capability",
            "After registration, OCR / Vision / Voice and future domains can share domain_config entry",
        ],
        "validation_factory_base_module_count": len(VALIDATION_FACTORY_BASE_MODULES),
        "proposed_factory_module_id": "controlled_provider_readiness_harness",
        "planning_scope": [
            "validation_factory_module_registry_update_plan",
            "provider_readiness_factory_entrypoint_plan",
            "domain_config_consumer_registration_plan",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_future_consumer_adoption_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "deferred",
        "defer_reasons": [
            "Register future consumers only — no Map / Library / Hive / Memory adoption now",
            "Those domains depend on business contracts not yet in provider readiness adoption",
        ],
        "future_consumers": [c for c in FUTURE_CONSUMERS if c.get("domain") in FUTURE_ONLY_DOMAINS],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_visual_context_governance_return_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "deferred",
        "defer_reasons": [
            "Visual Context Governance remains important",
            "Provider harness generalization is near closure — complete factory registration first",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "provider_harness_generalization_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "deferred_next"},
            {"route": ROUTE_B, "status": "selected"},
            {"route": ROUTE_C, "status": "deferred"},
            {"route": ROUTE_D, "status": "deferred"},
        ],
        "selected_route": SELECTED_ROUTE,
        "deferred_route_a": DEFERRED_ROUTE_A,
        "deferred_route_c": DEFERRED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        **meta,
    }

    preconditions = {
        "preconditions_id": "selected_route_preconditions_v1",
        "selected_route": SELECTED_ROUTE,
        "preconditions": [
            "vision_voice_harness_adoption_post_dryrun_review GO",
            "OCR / Vision / Voice three-consumer harness validated",
            "controlled_provider_readiness_harness_v1 exists and GO",
            "harness_runtime_enforced_globally_now=false",
            "luna_validation_factory_consolidation GO with base modules present",
            "anti_recursion preserved",
            "no provider import/install/download/invoke in adoption chain",
        ],
        "forbidden_now": [
            "OCR provider authorization execution",
            "Validation Factory runtime enforcement",
            "Map / Library / Hive / Memory consumer adoption",
            "Visual Context Governance branch switch",
            "provider import/install/download/invoke",
            "real dependency check execution",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_items": [
            {
                "route": DEFERRED_ROUTE_A,
                "status": "deferred_next",
                "resume_after": "validation_factory_registration_planning_and_dryrun",
            },
            {
                "route": DEFERRED_ROUTE_C,
                "status": "deferred",
                "note": "future consumer registration only — no adoption execution",
            },
            {
                "route": DEFERRED_ROUTE_D,
                "status": "deferred",
                "resume_after": "validation_factory_registration_closure",
            },
        ],
        **meta,
    }

    decision_ok = len(blockers) == 0
    boundary_ok = decision_ok

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_validation_factory_registration_planning": boundary_ok,
        "selected_route": SELECTED_ROUTE,
        "do_not_start_ocr_authorization_now": True,
        "do_not_start_validation_factory_registration_execution_now": True,
        "do_not_adopt_map_library_hive_memory_now": True,
        "do_not_start_visual_context_governance_now": True,
        "resume_ocr_authorization_after_factory_registration": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "provider_harness_generalization_roadmap_policy_v1",
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
        "deferred_route_c": DEFERRED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "provider_harness_generalization_roadmap_policy": policy,
        "vision_voice_post_review_input_review": input_review,
        "controlled_provider_readiness_harness_generalization_review": harness_generalization_review,
        "route_a_return_ocr_authorization_assessment": route_a,
        "route_b_validation_factory_registration_assessment": route_b,
        "route_c_future_consumer_adoption_assessment": route_c,
        "route_d_visual_context_governance_return_assessment": route_d,
        "provider_harness_generalization_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }

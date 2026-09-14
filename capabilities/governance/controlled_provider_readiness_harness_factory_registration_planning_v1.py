# -*- coding: utf-8 -*-
"""Controlled Provider Readiness Harness Validation Factory Registration Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.controlled_provider_readiness_harness_v1 import (
    ANTI_RECURSION,
    FUTURE_CONSUMERS,
    HARNESS_ID,
    HARNESS_MODULE,
    HARNESS_PHASES,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_harness_generalization_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as ROADMAP_NEXT_PHASE,
    SELECTED_ROUTE,
)

PHASE_ID = "Phase-Controlled-Provider-Readiness-Harness-Validation-Factory-Registration-Planning-v1-001"
SCOPE = "controlled_provider_readiness_harness_factory_registration_planning_only"
SOURCE_CHAIN = "controlled_provider_readiness_harness_factory_registration_planning_v1"

UPSTREAM_ROADMAP_FINAL = ROADMAP_FINAL_GO
UPSTREAM_ROADMAP_NEXT = ROADMAP_NEXT_PHASE

FINAL_DECISION_GO = "CONTROLLED_PROVIDER_READINESS_HARNESS_FACTORY_REGISTRATION_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_HOLD = (
    "CONTROLLED_PROVIDER_READINESS_HARNESS_FACTORY_REGISTRATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = (
    "Phase-Controlled-Provider-Readiness-Harness-Validation-Factory-Registration-DryRun-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Controlled-Provider-Readiness-Harness-Validation-Factory-Registration-Issue-Review-v1-001"
)

FACTORY_ID = "luna_validation_factory_v1"
EXISTING_FACTORY_MODULE_COUNT = 6

EXISTING_FACTORY_MODULES: Tuple[Dict[str, str], ...] = (
    {"module_id": "batch_preflight_harness", "display_name": "BatchPreflightHarness"},
    {"module_id": "single_chain_trial_validation_harness", "display_name": "SingleChainTrialValidationHarness"},
    {"module_id": "controlled_trial_authorization_harness", "display_name": "ControlledTrialAuthorizationHarness"},
    {"module_id": "candidate_output_contract", "display_name": "CandidateOutputContract"},
    {"module_id": "no_runtime_boundary_audit", "display_name": "NoRuntimeBoundaryAudit"},
    {
        "module_id": "controlled_trial_post_execution_review_harness",
        "display_name": "ControlledTrialPostExecutionReviewHarness",
    },
)

NEW_FACTORY_MODULE_ID = "controlled_provider_readiness_harness_v1"
NEW_FACTORY_MODULE_DISPLAY = "ControlledProviderReadinessHarness"
NEW_FACTORY_MODULE_TYPE = "provider_readiness_validation_harness"
NEW_FACTORY_MODULE_STATUS = "validated_contract_candidate"

VALIDATED_CONSUMERS: Tuple[str, ...] = ("ocr", "vision", "voice")
FUTURE_CONSUMER_DOMAINS: Tuple[str, ...] = ("map", "library", "hive", "memory")

FACTORY_INTERFACE_INPUTS: Tuple[str, ...] = (
    "provider_domain",
    "provider_candidates",
    "output_contract",
    "evidence_pack_contract",
    "dependency_requirements",
    "environment_requirements",
    "failure_routes",
    "boundary_rules",
    "authorization_requirements",
)

FACTORY_INTERFACE_OUTPUTS: Tuple[str, ...] = (
    "provider_readiness_candidate",
    "dependency_readiness_candidate",
    "environment_readiness_candidate",
    "provider_comparison_candidate",
    "real_dependency_check_plan_candidate",
    "evidence_package_candidate",
    "authorization_readiness_candidate",
)

BOUNDARY_BLOCKED_PATHS: Tuple[str, ...] = (
    "factory_registration_to_runtime_enforcement",
    "provider_readiness_to_provider_invocation",
    "dependency_readiness_to_dependency_install",
    "environment_readiness_to_runtime_enabled",
    "real_dependency_plan_to_real_check_execution",
    "evidence_package_candidate_to_fact_commit",
    "future_consumer_register_to_consumer_adoption",
    "domain_config_to_runtime_provider",
)

PLANNING_ANTI_RECURSION: Tuple[str, ...] = ANTI_RECURSION + (
    "Real runtime / real provider / user output / fact write / hardware control require separate authorization phase",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "validation_factory_registry_updated_now",
    "validation_factory_runtime_enforced_now",
    "controlled_provider_harness_runtime_enforced_now",
    "provider_runtime_enabled_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "real_dependency_check_executed_now",
    "controlled_trial_started_now",
    "map_library_hive_memory_adoption_started_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Planning GO ≠ Validation Factory registry updated",
    "Planning GO ≠ ControlledProviderReadinessHarness runtime enforced",
    "registry entry plan ≠ provider import/install/download",
    "factory contract extension plan ≠ provider invocation",
    "DryRun next ≠ Map/Library/Hive/Memory consumer adoption",
    "three consumer validated ≠ all domains adopted",
    "factory registration planning ≠ OCR authorization started",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "controlled_provider_readiness_harness_factory_registration_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "harness_id": HARNESS_ID,
        "factory_id": FACTORY_ID,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    meta["harness_runtime_enforced_globally_now"] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_controlled_provider_readiness_harness_factory_registration_planning_v1(
    *,
    provider_harness_generalization_roadmap_decision_root: str,
    controlled_provider_readiness_harness_root: str,
    luna_validation_factory_consolidation_root: str,
    vision_voice_provider_harness_adoption_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    roadmap_root = Path(provider_harness_generalization_roadmap_decision_root).expanduser().resolve()
    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}

    harness_root = Path(controlled_provider_readiness_harness_root).expanduser().resolve()
    harness_sm = _try_read_json(harness_root / "summary.json") or {}
    harness_vr = _try_read_json(harness_root / "verifier_report.json") or {}
    validation = _try_read_json(
        harness_root / "controlled_provider_readiness_harness_validation_result_v1.json"
    ) or {}
    harness_contract = _try_read_json(
        harness_root / "controlled_provider_readiness_harness_contract_v1.json"
    ) or {}

    factory_root = Path(luna_validation_factory_consolidation_root).expanduser().resolve()
    factory_sm = _try_read_json(factory_root / "summary.json") or {}
    factory_vr = _try_read_json(factory_root / "verifier_report.json") or {}
    factory_registry = _try_read_json(factory_root / "validation_factory_module_registry_v1.json") or {}

    post_root = Path(
        vision_voice_provider_harness_adoption_post_dryrun_review_root
        or roadmap_root.parent / "vision_voice_provider_harness_adoption_post_dryrun_review"
    ).expanduser().resolve()
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}
    closure = _try_read_json(post_root / "vision_voice_harness_adoption_closure_decision_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_roadmap_root": str(roadmap_root),
        "upstream_harness_root": str(harness_root),
        "upstream_validation_factory_root": str(factory_root),
        "upstream_post_review_root": str(post_root),
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
        blockers.append("controlled_provider_readiness_harness verifier must be GO")
    if harness_sm.get("harness_id") != HARNESS_ID:
        blockers.append("harness_id mismatch")
    if validation.get("ocr_first_consumer_validated") is not True:
        blockers.append("OCR first consumer must be validated")
    if harness_sm.get("harness_runtime_enforced_globally_now") is True:
        blockers.append("harness_runtime_enforced_globally_now must be false")

    post_go = post_vr.get("verifier") == "GO" and post_vr.get("passed") is True
    if not post_go:
        blockers.append("vision/voice post-dryrun review must be GO")
    if closure.get("ocr_vision_voice_three_consumer_harness_validated") is not True:
        blockers.append("OCR / Vision / Voice three consumer must be validated")

    factory_go = factory_vr.get("verifier") == "GO" and factory_vr.get("passed") is True
    if not factory_go:
        blockers.append("luna_validation_factory_consolidation verifier must be GO")
    registry_modules = factory_registry.get("modules") or []
    if len(registry_modules) != EXISTING_FACTORY_MODULE_COUNT:
        blockers.append(f"existing factory modules count must be {EXISTING_FACTORY_MODULE_COUNT}")
    if factory_sm.get("validation_factory_runtime_enforced_now") is True:
        blockers.append("validation_factory_runtime_enforced_now must be false")

    existing_ids = {m.get("module_id") for m in registry_modules}
    for mod in EXISTING_FACTORY_MODULES:
        if mod["module_id"] not in existing_ids:
            blockers.append(f"missing existing factory module {mod['module_id']}")
    if NEW_FACTORY_MODULE_ID in existing_ids:
        blockers.append("provider harness must not already be in registry")

    anti_rules = harness_contract.get("anti_recursion_rules") or []
    if len(anti_rules) < len(ANTI_RECURSION):
        blockers.append("anti_recursion must be preserved")

    for field in (
        "provider_imported_now",
        "provider_invoked_now",
        "dependency_install_executed_now",
        "model_download_executed_now",
    ):
        if harness_sm.get(field) is True or roadmap_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    if roadmap_sm.get("map_library_hive_memory_adoption_started_now") is True:
        blockers.append("map/library/hive/memory adoption must not start")

    input_review = {
        "review_id": "provider_harness_generalization_roadmap_input_review_v1",
        "upstream_roadmap_root": str(roadmap_root),
        "upstream_verifier_go": roadmap_go,
        "upstream_final_decision": roadmap_sm.get("final_decision"),
        "selected_route": roadmap_sm.get("selected_route"),
        "three_consumer_validated": closure.get("ocr_vision_voice_three_consumer_harness_validated"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    registry_review = {
        "review_id": "validation_factory_existing_registry_review_v1",
        "factory_id": factory_registry.get("factory_id") or FACTORY_ID,
        "existing_module_count": len(registry_modules),
        "existing_modules": list(EXISTING_FACTORY_MODULES),
        "provider_harness_not_yet_registered": NEW_FACTORY_MODULE_ID not in existing_ids,
        "review_pass": len(blockers) == 0 and len(registry_modules) == EXISTING_FACTORY_MODULE_COUNT,
        **meta,
    }

    registry_entry_plan = {
        "plan_id": "controlled_provider_harness_registry_entry_plan_v1",
        "proposed_module": {
            "module_id": NEW_FACTORY_MODULE_ID,
            "display_name": NEW_FACTORY_MODULE_DISPLAY,
            "module_type": NEW_FACTORY_MODULE_TYPE,
            "status": NEW_FACTORY_MODULE_STATUS,
            "harness_id": HARNESS_ID,
            "module_path": HARNESS_MODULE,
            "first_consumer": "ocr",
            "additional_validated_consumers": ["vision", "voice"],
            "future_consumers": list(FUTURE_CONSUMER_DOMAINS),
            "runtime_enforced": False,
            "global_enforcement": False,
            "domain_config_required": True,
            "provider_invocation_allowed": False,
            "dependency_install_allowed": False,
            "model_download_allowed": False,
            "evidence_package_required": True,
            "boundary_guard_required": True,
            "harness_phases": list(HARNESS_PHASES),
        },
        "registry_update_mode": "append_seventh_module",
        "registry_updated_now": False,
        **meta,
    }

    contract_extension = {
        "plan_id": "validation_factory_contract_extension_plan_v1",
        "existing_modules": [m["display_name"] for m in EXISTING_FACTORY_MODULES],
        "existing_module_count": EXISTING_FACTORY_MODULE_COUNT,
        "proposed_seventh_module": NEW_FACTORY_MODULE_DISPLAY,
        "proposed_module_id": NEW_FACTORY_MODULE_ID,
        "extension_type": "provider_readiness_factory_capability",
        "contract_updated_now": False,
        **meta,
    }

    interface_plan = {
        "plan_id": "provider_harness_factory_interface_plan_v1",
        "standard_inputs": list(FACTORY_INTERFACE_INPUTS),
        "standard_outputs": list(FACTORY_INTERFACE_OUTPUTS),
        "entrypoint": "run_provider_readiness_plan_and_dryrun(domain_config)",
        "consumer_entry": "domain_config → ControlledProviderReadinessHarness → readiness candidates",
        **meta,
    }

    consumer_mapping = {
        "plan_id": "provider_harness_consumer_mapping_plan_v1",
        "consumers": [
            {"domain": "ocr", "consumer_order": "first", "status": "validated"},
            {"domain": "vision", "consumer_order": "second", "status": "validated"},
            {"domain": "voice", "consumer_order": "third", "status": "validated"},
            {"domain": "map", "consumer_order": None, "status": "future_only"},
            {"domain": "library", "consumer_order": None, "status": "future_only"},
            {"domain": "hive", "consumer_order": None, "status": "future_only"},
            {"domain": "memory", "consumer_order": None, "status": "future_only"},
        ],
        "future_consumer_adoption_started_now": False,
        **meta,
    }

    boundary_policy = {
        "plan_id": "provider_harness_boundary_policy_plan_v1",
        "default_blocked_paths": [
            {"path_id": p, "blocked": True, "default": True} for p in BOUNDARY_BLOCKED_PATHS
        ],
        "path_count": len(BOUNDARY_BLOCKED_PATHS),
        "all_blocked_by_default": True,
        **meta,
    }

    anti_recursion_plan = {
        "plan_id": "provider_harness_anti_recursion_rule_plan_v1",
        "rules": list(PLANNING_ANTI_RECURSION),
        "rule_count": len(PLANNING_ANTI_RECURSION),
        "no_per_domain_long_chain_duplication": True,
        "domain_config_plus_harness_required": True,
        "separate_authorization_for_runtime_exceptions": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "validation_factory_registration_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate validation_factory_registry_candidate",
            "register ControlledProviderReadinessHarness as seventh module candidate",
            "verify factory contract extension",
            "verify OCR/Vision/Voice consumer mapping",
            "verify boundary and anti-recursion",
            "no runtime enforcement",
        ],
        "dryrun_forbidden": [
            "provider import/install/download/invoke",
            "validation factory runtime enforcement",
            "Map/Library/Hive/Memory consumer adoption",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_consumer_register_v1",
        "deferred_consumers": [
            {"domain": c.get("domain"), "status": "future_only", "adopted_now": False}
            for c in FUTURE_CONSUMERS
            if c.get("domain") in FUTURE_CONSUMER_DOMAINS
        ],
        "map_library_hive_memory_adoption_deferred": True,
        **meta,
    }

    planning_ok = len(blockers) == 0
    boundary_ok = planning_ok

    planning_decision = {
        "decision_id": "factory_registration_planning_decision_v1",
        "planning_pass": boundary_ok,
        "ready_for_dryrun": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "controlled_provider_harness_factory_registration_planning_policy_v1",
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
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        "selected_route": SELECTED_ROUTE,
        "existing_factory_module_count": EXISTING_FACTORY_MODULE_COUNT,
        "proposed_seventh_module": NEW_FACTORY_MODULE_DISPLAY,
        "three_consumer_validated": closure.get("ocr_vision_voice_three_consumer_harness_validated"),
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "controlled_provider_harness_factory_registration_planning_policy": policy,
        "provider_harness_generalization_roadmap_input_review": input_review,
        "validation_factory_existing_registry_review": registry_review,
        "controlled_provider_harness_registry_entry_plan": registry_entry_plan,
        "validation_factory_contract_extension_plan": contract_extension,
        "provider_harness_factory_interface_plan": interface_plan,
        "provider_harness_consumer_mapping_plan": consumer_mapping,
        "provider_harness_boundary_policy_plan": boundary_policy,
        "provider_harness_anti_recursion_rule_plan": anti_recursion_plan,
        "validation_factory_registration_dryrun_plan": dryrun_plan,
        "deferred_consumer_register": deferred_register,
        "factory_registration_planning_decision": planning_decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }

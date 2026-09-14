# -*- coding: utf-8 -*-
"""Controlled Provider Readiness Harness Validation Factory Registration DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.controlled_provider_readiness_harness_factory_registration_planning_v1 import (
    BOUNDARY_BLOCKED_PATHS,
    EXISTING_FACTORY_MODULE_COUNT,
    EXISTING_FACTORY_MODULES,
    FACTORY_ID,
    FACTORY_INTERFACE_INPUTS,
    FACTORY_INTERFACE_OUTPUTS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    FUTURE_CONSUMER_DOMAINS,
    HARNESS_ID,
    NEW_FACTORY_MODULE_DISPLAY,
    NEW_FACTORY_MODULE_ID,
    NEW_FACTORY_MODULE_STATUS,
    NEW_FACTORY_MODULE_TYPE,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    PLANNING_ANTI_RECURSION,
    VALIDATED_CONSUMERS,
)
from capabilities.governance.controlled_provider_readiness_harness_v1 import HARNESS_MODULE, HARNESS_PHASES
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_harness_generalization_roadmap_decision_v1 import SELECTED_ROUTE

PHASE_ID = "Phase-Controlled-Provider-Readiness-Harness-Validation-Factory-Registration-DryRun-v1-001"
SCOPE = "controlled_provider_readiness_harness_factory_registration_dryrun_only"
SOURCE_CHAIN = "controlled_provider_readiness_harness_factory_registration_dryrun_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "CONTROLLED_PROVIDER_READINESS_HARNESS_FACTORY_REGISTRATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
FINAL_DECISION_HOLD = (
    "CONTROLLED_PROVIDER_READINESS_HARNESS_FACTORY_REGISTRATION_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = (
    "Phase-Controlled-Provider-Readiness-Harness-Validation-Factory-Registration-Post-DryRun-Review-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Controlled-Provider-Readiness-Harness-Validation-Factory-Registration-Issue-Review-v1-001"
)

DISPLAY_NAME_BY_MODULE_ID: Dict[str, str] = {m["module_id"]: m["display_name"] for m in EXISTING_FACTORY_MODULES}

NON_CLAIMS: Tuple[str, ...] = (
    "DryRun GO ≠ Validation Factory registry updated",
    "registry candidate ≠ factory runtime enforced",
    "seventh module candidate ≠ provider import/install/download",
    "Post-DryRun Review next ≠ OCR authorization started",
    "consumer mapping dryrun pass ≠ Map/Library/Hive/Memory adopted",
    "contract extension dryrun ≠ real provider invocation",
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

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_dryrun"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "controlled_provider_readiness_harness_factory_registration_dryrun_only": True,
        "simulated": True,
        "validation_factory_registry_candidate_generated_now": True,
        "harness_id": HARNESS_ID,
        "factory_id": FACTORY_ID,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    meta["validation_factory_registry_updated_now"] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _seventh_module_candidate() -> Dict[str, Any]:
    return {
        "module_id": NEW_FACTORY_MODULE_ID,
        "display_name": NEW_FACTORY_MODULE_DISPLAY,
        "module_type": NEW_FACTORY_MODULE_TYPE,
        "status": NEW_FACTORY_MODULE_STATUS,
        "harness_id": HARNESS_ID,
        "module_path": HARNESS_MODULE,
        "registry_role": "provider_readiness_validation",
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
        "candidate_only": True,
        "registry_updated_now": False,
        "entrypoint": "run_provider_readiness_plan_and_dryrun(domain_config)",
    }


def run_controlled_provider_readiness_harness_factory_registration_dryrun_v1(
    *,
    controlled_provider_readiness_harness_factory_registration_planning_root: str,
    provider_harness_generalization_roadmap_decision_root: Optional[str] = None,
    controlled_provider_readiness_harness_root: Optional[str] = None,
    luna_validation_factory_consolidation_root: Optional[str] = None,
    vision_voice_provider_harness_adoption_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(
        controlled_provider_readiness_harness_factory_registration_planning_root
    ).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}
    plan_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    entry_plan = _try_read_json(planning_root / "controlled_provider_harness_registry_entry_plan_v1.json") or {}
    interface_plan = _try_read_json(planning_root / "provider_harness_factory_interface_plan_v1.json") or {}
    consumer_plan = _try_read_json(planning_root / "provider_harness_consumer_mapping_plan_v1.json") or {}
    boundary_plan = _try_read_json(planning_root / "provider_harness_boundary_policy_plan_v1.json") or {}
    anti_plan = _try_read_json(planning_root / "provider_harness_anti_recursion_rule_plan_v1.json") or {}
    deferred_plan = _try_read_json(planning_root / "deferred_consumer_register_v1.json") or {}

    roadmap_root = Path(
        provider_harness_generalization_roadmap_decision_root
        or planning_root.parent / "provider_harness_generalization_roadmap_decision"
    ).expanduser().resolve()
    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}

    harness_root = Path(
        controlled_provider_readiness_harness_root
        or planning_root.parent / "controlled_provider_readiness_harness"
    ).expanduser().resolve()
    harness_vr = _try_read_json(harness_root / "verifier_report.json") or {}
    validation = _try_read_json(
        harness_root / "controlled_provider_readiness_harness_validation_result_v1.json"
    ) or {}

    factory_root = Path(
        luna_validation_factory_consolidation_root
        or planning_root.parent / "luna_validation_factory_consolidation"
    ).expanduser().resolve()
    factory_registry = _try_read_json(factory_root / "validation_factory_module_registry_v1.json") or {}

    post_root = Path(
        vision_voice_provider_harness_adoption_post_dryrun_review_root
        or planning_root.parent / "vision_voice_provider_harness_adoption_post_dryrun_review"
    ).expanduser().resolve()
    closure = _try_read_json(post_root / "vision_voice_harness_adoption_closure_decision_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(planning_root),
        "upstream_roadmap_root": str(roadmap_root),
        "upstream_harness_root": str(harness_root),
        "upstream_validation_factory_root": str(factory_root),
        "upstream_post_review_root": str(post_root),
        "output_root": str(out_root),
    }

    planning_go = plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True
    if not planning_go:
        blockers.append("planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_sm.get("boundary_ok") is not True:
        blockers.append("planning boundary_ok must be true")

    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("roadmap must have selected Route B")
    if harness_vr.get("verifier") != "GO":
        blockers.append("harness verifier must be GO")
    if validation.get("ocr_first_consumer_validated") is not True:
        blockers.append("OCR first consumer must be validated")
    if closure.get("ocr_vision_voice_three_consumer_harness_validated") is not True:
        blockers.append("three consumer harness must be validated")

    existing_modules_raw = factory_registry.get("modules") or []
    if len(existing_modules_raw) != EXISTING_FACTORY_MODULE_COUNT:
        blockers.append(f"existing factory modules count must be {EXISTING_FACTORY_MODULE_COUNT}")

    proposed = entry_plan.get("proposed_module") or {}
    if proposed.get("module_id") != NEW_FACTORY_MODULE_ID:
        blockers.append("planned module_id mismatch")

    for field in BOUNDARY_FALSE:
        if plan_sm.get(field) is True:
            blockers.append(f"planning {field} must be false")

    input_review = {
        "review_id": "factory_registration_planning_input_review_v1",
        "upstream_planning_root": str(planning_root),
        "upstream_verifier_go": planning_go,
        "upstream_final_decision": plan_sm.get("final_decision"),
        "planned_module_id": proposed.get("module_id"),
        "three_consumer_validated": closure.get("ocr_vision_voice_three_consumer_harness_validated"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    existing_modules_candidate: List[Dict[str, Any]] = []
    for mod in existing_modules_raw:
        mid = mod.get("module_id", "")
        enriched = {
            **mod,
            "display_name": DISPLAY_NAME_BY_MODULE_ID.get(mid, mid),
            "registry_status": "existing_closed",
            "candidate_only": False,
        }
        existing_modules_candidate.append(enriched)

    seventh = _seventh_module_candidate()
    registry_candidate = {
        "registry_id": "validation_factory_registry_candidate_v1",
        "factory_id": factory_registry.get("factory_id") or FACTORY_ID,
        "modules": existing_modules_candidate + [seventh],
        "module_count": EXISTING_FACTORY_MODULE_COUNT + 1,
        "existing_module_count": EXISTING_FACTORY_MODULE_COUNT,
        "proposed_seventh_module_id": NEW_FACTORY_MODULE_ID,
        "proposed_seventh_module_display": NEW_FACTORY_MODULE_DISPLAY,
        "candidate_only": True,
        "registry_updated_now": False,
        "source_registry": str(factory_root / "validation_factory_module_registry_v1.json"),
        **meta,
    }

    entry_candidate = {
        "candidate_id": "controlled_provider_harness_registry_entry_candidate_v1",
        **seventh,
        **meta,
    }

    contract_extension = {
        "result_id": "validation_factory_contract_extension_dryrun_result_v1",
        "existing_module_count": EXISTING_FACTORY_MODULE_COUNT,
        "proposed_seventh_module": NEW_FACTORY_MODULE_DISPLAY,
        "standard_input_contract_present": True,
        "standard_output_contract_present": True,
        "boundary_policy_present": bool(boundary_plan.get("default_blocked_paths")),
        "anti_recursion_rule_present": bool(anti_plan.get("rules")),
        "consumer_mapping_present": bool(consumer_plan.get("consumers")),
        "deferred_consumer_register_present": bool(deferred_plan.get("deferred_consumers")),
        "extension_dryrun_pass": len(blockers) == 0,
        **meta,
    }

    interface_dryrun = {
        "result_id": "provider_harness_factory_interface_dryrun_result_v1",
        "standard_inputs": list(FACTORY_INTERFACE_INPUTS),
        "standard_outputs": list(FACTORY_INTERFACE_OUTPUTS),
        "input_count": len(FACTORY_INTERFACE_INPUTS),
        "output_count": len(FACTORY_INTERFACE_OUTPUTS),
        "inputs_match_plan": interface_plan.get("standard_inputs") == list(FACTORY_INTERFACE_INPUTS),
        "outputs_match_plan": interface_plan.get("standard_outputs") == list(FACTORY_INTERFACE_OUTPUTS),
        "interface_dryrun_pass": len(blockers) == 0,
        **meta,
    }

    consumer_mapping = {
        "result_id": "provider_harness_consumer_mapping_dryrun_result_v1",
        "consumers": [
            {"domain": "ocr", "consumer_order": "first", "status": "validated", "adopted_now": False},
            {"domain": "vision", "consumer_order": "second", "status": "validated", "adopted_now": False},
            {"domain": "voice", "consumer_order": "third", "status": "validated", "adopted_now": False},
            *[
                {"domain": d, "consumer_order": None, "status": "future_only", "adopted_now": False}
                for d in FUTURE_CONSUMER_DOMAINS
            ],
        ],
        "future_consumers_not_adopted_now": True,
        "consumer_mapping_dryrun_pass": len(blockers) == 0,
        **meta,
    }

    boundary_result = {
        "result_id": "provider_harness_boundary_policy_dryrun_result_v1",
        "paths": [{"path_id": p, "blocked": True, "executed_now": False} for p in BOUNDARY_BLOCKED_PATHS],
        "path_count": len(BOUNDARY_BLOCKED_PATHS),
        "all_blocked": True,
        "boundary_dryrun_pass": len(blockers) == 0,
        **meta,
    }

    anti_recursion = {
        "result_id": "provider_harness_anti_recursion_dryrun_result_v1",
        "rules": list(PLANNING_ANTI_RECURSION),
        "rule_count": len(PLANNING_ANTI_RECURSION),
        "no_per_domain_long_chain_duplication": True,
        "domain_config_plus_harness_required": True,
        "separate_authorization_for_runtime_exceptions": True,
        "anti_recursion_dryrun_pass": len(blockers) == 0,
        **meta,
    }

    deferred_result = {
        "result_id": "deferred_consumer_register_dryrun_result_v1",
        "deferred_consumers": deferred_plan.get("deferred_consumers") or [
            {"domain": d, "status": "future_only", "adopted_now": False} for d in FUTURE_CONSUMER_DOMAINS
        ],
        "map_library_hive_memory_adoption_deferred": True,
        "adopted_now": False,
        **meta,
    }

    no_runtime_audit = {
        "audit_id": "validation_factory_registration_no_runtime_audit_v1",
        "validation_factory_registry_updated_now": False,
        "validation_factory_runtime_enforced_now": False,
        "controlled_provider_harness_runtime_enforced_now": False,
        "provider_imported_now": False,
        "provider_invoked_now": False,
        "real_dependency_check_executed_now": False,
        "audit_pass": True,
        **meta,
    }

    blocked_result = {
        "result_id": "validation_factory_registration_blocked_path_result_v1",
        "paths": boundary_result["paths"],
        "path_count": boundary_result["path_count"],
        "all_blocked": True,
        **meta,
    }

    checks_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and registry_candidate.get("module_count") == 7
        and contract_extension.get("extension_dryrun_pass")
        and interface_dryrun.get("interface_dryrun_pass")
        and consumer_mapping.get("consumer_mapping_dryrun_pass")
        and boundary_result.get("boundary_dryrun_pass")
        and anti_recursion.get("anti_recursion_dryrun_pass")
        and no_runtime_audit.get("audit_pass")
    )

    readiness = {
        "decision_id": "validation_factory_registration_readiness_decision_v1",
        "registry_candidate_pass": checks_pass,
        "contract_extension_pass": checks_pass,
        "interface_pass": checks_pass,
        "consumer_mapping_pass": checks_pass,
        "boundary_pass": checks_pass,
        "anti_recursion_pass": checks_pass,
        "all_pass": checks_pass,
        "high_risk_count": 0 if checks_pass else 1,
        "final_decision": FINAL_DECISION_GO if checks_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if checks_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "controlled_provider_harness_factory_registration_dryrun_policy_v1",
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
        "boundary_ok": checks_pass,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "module_count": registry_candidate.get("module_count"),
        "proposed_seventh_module": NEW_FACTORY_MODULE_DISPLAY,
        "three_consumer_validated": closure.get("ocr_vision_voice_three_consumer_harness_validated"),
        **meta,
    }

    return {
        "controlled_provider_harness_factory_registration_dryrun_policy": policy,
        "factory_registration_planning_input_review": input_review,
        "validation_factory_registry_candidate": registry_candidate,
        "controlled_provider_harness_registry_entry_candidate": entry_candidate,
        "validation_factory_contract_extension_dryrun_result": contract_extension,
        "provider_harness_factory_interface_dryrun_result": interface_dryrun,
        "provider_harness_consumer_mapping_dryrun_result": consumer_mapping,
        "provider_harness_boundary_policy_dryrun_result": boundary_result,
        "provider_harness_anti_recursion_dryrun_result": anti_recursion,
        "deferred_consumer_register_dryrun_result": deferred_result,
        "validation_factory_registration_no_runtime_audit": no_runtime_audit,
        "validation_factory_registration_blocked_path_result": blocked_result,
        "validation_factory_registration_readiness_decision": readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }

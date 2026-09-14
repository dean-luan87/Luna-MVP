# -*- coding: utf-8 -*-
"""Controlled Provider Readiness Harness Validation Factory Registration Post-DryRun Review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.controlled_provider_readiness_harness_factory_registration_dryrun_v1 import (
    BOUNDARY_FALSE as DRYRUN_BOUNDARY_FALSE,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PHASE_ID as DRYRUN_PHASE,
    SCOPE as DRYRUN_SCOPE,
)
from capabilities.governance.controlled_provider_readiness_harness_factory_registration_planning_v1 import (
    BOUNDARY_BLOCKED_PATHS,
    EXISTING_FACTORY_MODULE_COUNT,
    EXISTING_FACTORY_MODULES,
    FACTORY_INTERFACE_INPUTS,
    FACTORY_INTERFACE_OUTPUTS,
    FUTURE_CONSUMER_DOMAINS,
    HARNESS_ID,
    NEW_FACTORY_MODULE_ID,
    NEW_FACTORY_MODULE_STATUS,
    NEW_FACTORY_MODULE_TYPE,
    PLANNING_ANTI_RECURSION,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = (
    "Phase-Controlled-Provider-Readiness-Harness-Validation-Factory-Registration-Post-DryRun-Review-v1-001"
)
REVIEW_SCOPE = "controlled_provider_readiness_harness_factory_registration_post_dryrun_review_only"
SOURCE_CHAIN = "controlled_provider_readiness_harness_factory_registration_post_dryrun_review_v1"

UPSTREAM_DRYRUN_FINAL = DRYRUN_FINAL_GO
UPSTREAM_DRYRUN_NEXT = DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "CONTROLLED_PROVIDER_READINESS_HARNESS_FACTORY_REGISTRATION_POST_DRYRUN_REVIEW_CLOSED_READY_FOR_OCR_PROVIDER_AUTHORIZATION_RETURN"
)
FINAL_DECISION_HOLD = (
    "CONTROLLED_PROVIDER_READINESS_HARNESS_FACTORY_REGISTRATION_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Provider-Authorization-Return-Roadmap-Decision-v1-001"
NEXT_PHASE_HOLD = (
    "Phase-Controlled-Provider-Readiness-Harness-Validation-Factory-Registration-Issue-Review-v1-001"
)

ENTRY_BOOL_CHECKS: Tuple[Tuple[str, bool], ...] = (
    ("runtime_enforced", False),
    ("global_enforcement", False),
    ("domain_config_required", True),
    ("provider_invocation_allowed", False),
    ("dependency_install_allowed", False),
    ("model_download_allowed", False),
    ("evidence_package_required", True),
    ("boundary_guard_required", True),
)

BOUNDARY_FALSE_REVIEW: Tuple[str, ...] = (
    "new_validation_factory_registry_candidate_generated_now",
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
    "Post-DryRun Review GO ≠ Validation Factory runtime enabled",
    "Registry candidate closure ≠ registry updated",
    "ControlledProviderReadinessHarness registration ≠ provider invocation allowed",
    "Factory module candidate ≠ global enforcement",
    "Future consumer register ≠ Map/Library/Hive/Memory adoption",
    "OCR return readiness ≠ OCR provider authorization granted",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)


def _review_meta() -> Dict[str, Any]:
    meta = {
        "controlled_provider_readiness_harness_factory_registration_post_dryrun_review_only": True,
        "review_only": True,
        "harness_id": HARNESS_ID,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }
    for field in BOUNDARY_FALSE_REVIEW:
        meta[field] = False
    meta["new_validation_factory_registry_candidate_generated_now"] = False
    meta["validation_factory_registry_updated_now"] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_controlled_provider_readiness_harness_factory_registration_post_dryrun_review_v1(
    *,
    controlled_provider_readiness_harness_factory_registration_dryrun_root: str,
    controlled_provider_readiness_harness_factory_registration_planning_root: Optional[str] = None,
    provider_harness_generalization_roadmap_decision_root: Optional[str] = None,
    controlled_provider_readiness_harness_root: Optional[str] = None,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(
        controlled_provider_readiness_harness_factory_registration_dryrun_root
    ).expanduser().resolve()
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}

    planning_root = Path(
        controlled_provider_readiness_harness_factory_registration_planning_root
        or dryrun_root.parent / "controlled_provider_readiness_harness_factory_registration_planning"
    ).expanduser().resolve()

    harness_root = Path(
        controlled_provider_readiness_harness_root
        or dryrun_root.parent / "controlled_provider_readiness_harness"
    ).expanduser().resolve()
    validation = _try_read_json(
        harness_root / "controlled_provider_readiness_harness_validation_result_v1.json"
    ) or {}

    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    )
    meta = {**_review_meta(), "upstream_dryrun_root": str(dryrun_root), "review_output_root": str(out_root)}

    dryrun_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    if not dryrun_go:
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_DRYRUN_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_DRYRUN_NEXT:
        blockers.append("dryrun recommended_next_phase mismatch")
    if dryrun_sm.get("boundary_ok") is not True:
        blockers.append("dryrun boundary_ok must be true")
    if dryrun_sm.get("simulated") is not True:
        blockers.append("dryrun simulated must be true")
    if dryrun_sm.get("validation_factory_registry_candidate_generated_now") is not True:
        blockers.append("registry candidate must have been generated in dryrun")

    for field in DRYRUN_BOUNDARY_FALSE:
        if dryrun_sm.get(field) is True:
            blockers.append(f"dryrun {field} must be false")

    if validation.get("ocr_first_consumer_validated") is not True:
        blockers.append("OCR first consumer must be validated")

    registry = _try_read_json(dryrun_root / "validation_factory_registry_candidate_v1.json") or {}
    entry = _try_read_json(dryrun_root / "controlled_provider_harness_registry_entry_candidate_v1.json") or {}
    contract = _try_read_json(
        dryrun_root / "validation_factory_contract_extension_dryrun_result_v1.json"
    ) or {}
    interface = _try_read_json(dryrun_root / "provider_harness_factory_interface_dryrun_result_v1.json") or {}
    consumer = _try_read_json(dryrun_root / "provider_harness_consumer_mapping_dryrun_result_v1.json") or {}
    boundary = _try_read_json(dryrun_root / "provider_harness_boundary_policy_dryrun_result_v1.json") or {}
    anti = _try_read_json(dryrun_root / "provider_harness_anti_recursion_dryrun_result_v1.json") or {}
    deferred = _try_read_json(dryrun_root / "deferred_consumer_register_dryrun_result_v1.json") or {}
    no_runtime = _try_read_json(dryrun_root / "validation_factory_registration_no_runtime_audit_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "validation_factory_registration_blocked_path_result_v1.json") or {}

    input_review = {
        "review_id": "factory_registration_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_phase": DRYRUN_PHASE,
        "upstream_scope": DRYRUN_SCOPE,
        "upstream_verifier_go": dryrun_go,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "upstream_simulated": dryrun_sm.get("simulated"),
        "module_count": registry.get("module_count"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    registry_issues: List[Dict[str, Any]] = []
    if registry.get("registry_id") != "validation_factory_registry_candidate_v1":
        registry_issues.append({"issue_id": "registry_id", "detail": "candidate registry id required"})
    if registry.get("module_count") != EXISTING_FACTORY_MODULE_COUNT + 1:
        registry_issues.append({"issue_id": "module_count", "detail": "expected 7 modules"})
    if registry.get("existing_module_count") != EXISTING_FACTORY_MODULE_COUNT:
        registry_issues.append({"issue_id": "existing_count", "detail": "expected 6 existing"})
    if registry.get("registry_updated_now") is not False:
        registry_issues.append({"issue_id": "not_updated", "detail": "registry must not be updated"})
    if registry.get("candidate_only") is not True:
        registry_issues.append({"issue_id": "candidate_only", "detail": "must be candidate only"})

    modules = registry.get("modules") or []
    module_ids = {m.get("module_id") for m in modules}
    for mod in EXISTING_FACTORY_MODULES:
        if mod["module_id"] not in module_ids:
            registry_issues.append({"issue_id": mod["module_id"], "detail": "existing module missing"})
    if NEW_FACTORY_MODULE_ID not in module_ids:
        registry_issues.append({"issue_id": "seventh", "detail": "seventh module missing"})

    registry_review = {
        "review_id": "validation_factory_registry_candidate_review_v1",
        "module_count": registry.get("module_count"),
        "existing_module_count": registry.get("existing_module_count"),
        "registry_updated_now": registry.get("registry_updated_now"),
        "seventh_module_present": NEW_FACTORY_MODULE_ID in module_ids,
        "issues": registry_issues,
        "review_pass": len(registry_issues) == 0,
        **meta,
    }

    entry_issues: List[Dict[str, Any]] = []
    checks = (
        ("module_id", NEW_FACTORY_MODULE_ID),
        ("module_type", NEW_FACTORY_MODULE_TYPE),
        ("status", NEW_FACTORY_MODULE_STATUS),
        ("first_consumer", "ocr"),
    )
    for key, expected in checks:
        if entry.get(key) != expected:
            entry_issues.append({"issue_id": key, "detail": f"expected {expected}"})
    if set(entry.get("additional_validated_consumers") or []) != {"vision", "voice"}:
        entry_issues.append({"issue_id": "additional_consumers", "detail": "vision, voice"})
    if set(entry.get("future_consumers") or []) != set(FUTURE_CONSUMER_DOMAINS):
        entry_issues.append({"issue_id": "future_consumers", "detail": str(FUTURE_CONSUMER_DOMAINS)})
    for key, expected in ENTRY_BOOL_CHECKS:
        if entry.get(key) is not expected:
            entry_issues.append({"issue_id": key, "detail": f"expected {expected}"})

    entry_review = {
        "review_id": "controlled_provider_harness_registry_entry_review_v1",
        "module_id": entry.get("module_id"),
        "status": entry.get("status"),
        "issues": entry_issues,
        "review_pass": len(entry_issues) == 0,
        **meta,
    }

    contract_issues: List[Dict[str, Any]] = []
    contract_checks = (
        ("standard_input_contract_present", True),
        ("standard_output_contract_present", True),
        ("boundary_policy_present", True),
        ("anti_recursion_rule_present", True),
        ("consumer_mapping_present", True),
        ("deferred_consumer_register_present", True),
        ("extension_dryrun_pass", True),
    )
    for key, expected in contract_checks:
        if contract.get(key) is not expected:
            contract_issues.append({"issue_id": key, "detail": f"expected {expected}"})

    contract_review = {
        "review_id": "validation_factory_contract_extension_review_v1",
        "issues": contract_issues,
        "review_pass": len(contract_issues) == 0,
        **meta,
    }

    interface_issues: List[Dict[str, Any]] = []
    inputs = interface.get("standard_inputs") or []
    outputs = interface.get("standard_outputs") or []
    if inputs != list(FACTORY_INTERFACE_INPUTS):
        interface_issues.append({"issue_id": "inputs", "detail": "9 standard inputs required"})
    if outputs != list(FACTORY_INTERFACE_OUTPUTS):
        interface_issues.append({"issue_id": "outputs", "detail": "7 standard outputs required"})
    if interface.get("interface_dryrun_pass") is not True:
        interface_issues.append({"issue_id": "dryrun_pass", "detail": "must pass"})

    interface_review = {
        "review_id": "provider_harness_factory_interface_review_v1",
        "standard_inputs": inputs,
        "standard_outputs": outputs,
        "input_count": len(inputs),
        "output_count": len(outputs),
        "issues": interface_issues,
        "review_pass": len(interface_issues) == 0,
        **meta,
    }

    consumer_issues: List[Dict[str, Any]] = []
    cmap = {c.get("domain"): c for c in consumer.get("consumers") or []}
    if cmap.get("ocr", {}).get("status") != "validated":
        consumer_issues.append({"issue_id": "ocr", "detail": "validated first consumer"})
    if cmap.get("vision", {}).get("status") != "validated":
        consumer_issues.append({"issue_id": "vision", "detail": "validated second consumer"})
    if cmap.get("voice", {}).get("status") != "validated":
        consumer_issues.append({"issue_id": "voice", "detail": "validated third consumer"})
    for domain in FUTURE_CONSUMER_DOMAINS:
        if cmap.get(domain, {}).get("status") != "future_only":
            consumer_issues.append({"issue_id": domain, "detail": "future_only"})
    if consumer.get("future_consumers_not_adopted_now") is not True:
        consumer_issues.append({"issue_id": "not_adopted", "detail": "future consumers not adopted"})

    consumer_review = {
        "review_id": "provider_harness_consumer_mapping_review_v1",
        "issues": consumer_issues,
        "review_pass": len(consumer_issues) == 0,
        **meta,
    }

    boundary_issues: List[Dict[str, Any]] = []
    paths = {p.get("path_id"): p for p in boundary.get("paths") or blocked.get("paths") or []}
    if boundary.get("all_blocked") is not True:
        boundary_issues.append({"issue_id": "all_blocked", "detail": "must be true"})
    if len(paths) != len(BOUNDARY_BLOCKED_PATHS):
        boundary_issues.append({"issue_id": "count", "detail": f"expected {len(BOUNDARY_BLOCKED_PATHS)}"})
    for pid in BOUNDARY_BLOCKED_PATHS:
        row = paths.get(pid)
        if not row or row.get("blocked") is not True:
            boundary_issues.append({"issue_id": pid, "detail": "must be blocked"})

    boundary_review = {
        "review_id": "provider_harness_boundary_policy_review_v1",
        "path_count": len(BOUNDARY_BLOCKED_PATHS),
        "all_blocked": boundary.get("all_blocked"),
        "issues": boundary_issues,
        "review_pass": len(boundary_issues) == 0,
        **meta,
    }

    blocked_review = {
        "review_id": "validation_factory_registration_blocked_path_review_v1",
        "paths_total": len(BOUNDARY_BLOCKED_PATHS),
        "all_blocked": blocked.get("all_blocked"),
        "issues": boundary_issues,
        "review_pass": len(boundary_issues) == 0,
        **meta,
    }

    anti_issues: List[Dict[str, Any]] = []
    if anti.get("no_per_domain_long_chain_duplication") is not True:
        anti_issues.append({"issue_id": "no_long_chain", "detail": "required"})
    if anti.get("domain_config_plus_harness_required") is not True:
        anti_issues.append({"issue_id": "domain_config", "detail": "required"})
    if anti.get("separate_authorization_for_runtime_exceptions") is not True:
        anti_issues.append({"issue_id": "runtime_auth", "detail": "required"})
    if anti.get("anti_recursion_dryrun_pass") is not True:
        anti_issues.append({"issue_id": "dryrun_pass", "detail": "required"})
    if len(anti.get("rules") or []) < len(PLANNING_ANTI_RECURSION):
        anti_issues.append({"issue_id": "rules", "detail": "anti-recursion rules missing"})

    anti_review = {
        "review_id": "provider_harness_anti_recursion_review_v1",
        "rule_count": len(anti.get("rules") or []),
        "issues": anti_issues,
        "review_pass": len(anti_issues) == 0,
        **meta,
    }

    deferred_issues: List[Dict[str, Any]] = []
    if deferred.get("map_library_hive_memory_adoption_deferred") is not True:
        deferred_issues.append({"issue_id": "deferred", "detail": "must be deferred"})
    if deferred.get("adopted_now") is not False:
        deferred_issues.append({"issue_id": "adopted_now", "detail": "must be false"})

    deferred_review = {
        "review_id": "deferred_consumer_register_review_v1",
        "issues": deferred_issues,
        "review_pass": len(deferred_issues) == 0,
        **meta,
    }

    no_runtime_issues: List[Dict[str, Any]] = []
    if no_runtime.get("audit_pass") is not True:
        no_runtime_issues.append({"issue_id": "audit_pass", "detail": "must pass"})
    for flag in (
        "validation_factory_registry_updated_now",
        "validation_factory_runtime_enforced_now",
        "controlled_provider_harness_runtime_enforced_now",
        "provider_imported_now",
        "provider_invoked_now",
    ):
        if no_runtime.get(flag) is not False:
            no_runtime_issues.append({"issue_id": flag, "detail": "must be false"})

    no_runtime_review = {
        "review_id": "validation_factory_registration_no_runtime_review_v1",
        "audit_pass": no_runtime.get("audit_pass"),
        "issues": no_runtime_issues,
        "review_pass": len(no_runtime_issues) == 0,
        **meta,
    }

    reviews_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and registry_review.get("review_pass")
        and entry_review.get("review_pass")
        and contract_review.get("review_pass")
        and interface_review.get("review_pass")
        and consumer_review.get("review_pass")
        and boundary_review.get("review_pass")
        and blocked_review.get("review_pass")
        and anti_review.get("review_pass")
        and deferred_review.get("review_pass")
        and no_runtime_review.get("review_pass")
    )
    boundary_ok = reviews_pass

    closure = {
        "closure_id": "factory_registration_closure_decision_v1",
        "factory_registration_dryrun_closed": boundary_ok,
        "validation_factory_registry_candidate_trusted": boundary_ok,
        "controlled_provider_readiness_harness_seventh_module_candidate_trusted": boundary_ok,
        "ready_for_ocr_provider_authorization_return": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    next_route = {
        "readiness_id": "next_route_readiness_decision_v1",
        "ready_for_ocr_provider_authorization_return_roadmap_decision": boundary_ok,
        "do_not_update_validation_factory_registry_now": True,
        "do_not_enable_validation_factory_runtime_now": True,
        "do_not_enable_provider_runtime_now": True,
        "do_not_adopt_map_library_hive_memory_now": True,
        "resume_ocr_authorization_after_return_roadmap_decision": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": closure["final_decision"],
        "rationale": (
            "After factory registration dryrun closure, short OCR authorization return "
            "roadmap decision — harness registered as factory candidate only"
        ),
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    all_issue_ids = (
        blockers
        + [i["issue_id"] for i in registry_issues]
        + [i["issue_id"] for i in entry_issues]
        + [i["issue_id"] for i in contract_issues]
        + [i["issue_id"] for i in interface_issues]
        + [i["issue_id"] for i in consumer_issues]
        + [i["issue_id"] for i in boundary_issues]
        + [i["issue_id"] for i in anti_issues]
        + [i["issue_id"] for i in deferred_issues]
        + [i["issue_id"] for i in no_runtime_issues]
    )

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": all_issue_ids,
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        "factory_registration_dryrun_closed": boundary_ok,
        "validation_factory_registry_candidate_trusted": boundary_ok,
        "module_count": registry.get("module_count"),
        **meta,
    }

    return {
        "factory_registration_dryrun_input_review": input_review,
        "validation_factory_registry_candidate_review": registry_review,
        "controlled_provider_harness_registry_entry_review": entry_review,
        "validation_factory_contract_extension_review": contract_review,
        "provider_harness_factory_interface_review": interface_review,
        "provider_harness_consumer_mapping_review": consumer_review,
        "provider_harness_boundary_policy_review": boundary_review,
        "provider_harness_anti_recursion_review": anti_review,
        "deferred_consumer_register_review": deferred_review,
        "validation_factory_registration_no_runtime_review": no_runtime_review,
        "validation_factory_registration_blocked_path_review": blocked_review,
        "factory_registration_closure_decision": closure,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }

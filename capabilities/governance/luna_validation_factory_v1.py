# -*- coding: utf-8 -*-
"""Luna Validation Factory v1 — registry and consolidated contracts for reusable validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.candidate_output_contract_v1 import (
    CONTRACT_ID as CANDIDATE_CONTRACT_ID,
    build_contract_document as build_candidate_contract,
)
from capabilities.governance.controlled_trial_authorization_harness_v1 import (
    ANTI_RECURSION_RULES as AUTH_ANTI_RECURSION,
    AUTHORIZATION_CONFIG_REQUIRED_FIELDS,
    FUTURE_TRIAL_ADOPTIONS,
    HARNESS_ID as AUTH_HARNESS_ID,
    HARNESS_MODULE as AUTH_HARNESS_MODULE,
    build_extraction_planning_artifacts,
    build_vision_sample_frame_authorization_config,
)
from capabilities.governance.controlled_trial_post_execution_review_harness_v1 import (
    build_contract_document as build_post_review_contract,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.no_runtime_boundary_audit_v1 import build_contract_document as build_no_runtime_contract
from capabilities.governance.single_chain_trial_validation_harness_v1 import (
    ANTI_RECURSION_RULES as SINGLE_CHAIN_ANTI_RECURSION,
    FUTURE_CHAIN_ADOPTIONS,
    HARNESS_ID as SINGLE_CHAIN_HARNESS_ID,
)

FACTORY_ID = "luna_validation_factory_v1"
FACTORY_VERSION = "v1"

BATCH_PREFLIGHT_HARNESS_ID = "main_project_structure_migration_batch_preflight_harness_v1"
BATCH_PREFLIGHT_MODULE = "capabilities.governance.main_project_structure_migration_batch_preflight_harness_extraction_planning_v1"

FACTORY_ANTI_RECURSION: Tuple[str, ...] = (
    "Do not regenerate Planning → DryRun → Review long chains per feature chain",
    "Single-chain validation must use SingleChainTrialValidationHarness first",
    "Controlled trial authorization must use ControlledTrialAuthorizationHarness first",
    "Candidate outputs must reference CandidateOutputContract",
    "No-runtime checks must reference NoRuntimeBoundaryAudit profiles",
    "Post-execution review must use ControlledTrialPostExecutionReviewHarness after execution",
    "Extra phases only for live camera, real OCR, navigation action, task commit, WM/Memory write, user output, external provider, safety high-risk",
)

FACTORY_NON_CLAIMS: Tuple[str, ...] = (
    "Validation Factory GO ≠ runtime enabled",
    "Factory contract generated ≠ factory globally enforced",
    "AuthorizationHarness defined ≠ request sent",
    "CandidateOutputContract defined ≠ fact write allowed",
    "NoRuntimeAudit defined ≠ runtime action allowed",
    "PostExecutionReviewHarness defined ≠ execution reviewed",
    "Future adoption matrix ≠ future chains implemented",
    "Anti-recursion rules ≠ historical phase artifacts deleted",
)

STANDARD_FEATURE_FLOW: Tuple[str, ...] = (
    "chain_config",
    "SingleChainTrialValidationHarness",
    "authorization_config",
    "ControlledTrialAuthorizationHarness",
    "controlled_trial_execution",
    "ControlledTrialPostExecutionReviewHarness",
    "closure",
)

MODULE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "module_id": "batch_preflight_harness",
        "harness_id": BATCH_PREFLIGHT_HARNESS_ID,
        "module_path": BATCH_PREFLIGHT_MODULE,
        "registry_role": "engineering_migration_validation",
        "already_closed": True,
        "reusable": True,
        "entrypoint": "batch_config → preflight → execution → post_migration_review",
    },
    {
        "module_id": "single_chain_trial_validation_harness",
        "harness_id": SINGLE_CHAIN_HARNESS_ID,
        "module_path": "capabilities.governance.single_chain_trial_validation_harness_v1",
        "registry_role": "single_chain_candidate_validation",
        "already_closed": True,
        "reusable": True,
        "first_consumer": "vision_sample_frame",
        "entrypoint": "run_single_chain_trial_plan_and_dryrun(chain_config)",
    },
    {
        "module_id": "controlled_trial_authorization_harness",
        "harness_id": AUTH_HARNESS_ID,
        "module_path": AUTH_HARNESS_MODULE,
        "registry_role": "controlled_trial_authorization_lifecycle",
        "already_closed": True,
        "reusable": True,
        "entrypoint": "run_authorization_validate(authorization_config)",
    },
    {
        "module_id": "candidate_output_contract",
        "contract_id": CANDIDATE_CONTRACT_ID,
        "module_path": "capabilities.governance.candidate_output_contract_v1",
        "registry_role": "candidate_output_constraints",
        "reusable": True,
        "entrypoint": "validate_candidate_output(candidate, expected_type)",
    },
    {
        "module_id": "no_runtime_boundary_audit",
        "audit_id": "no_runtime_boundary_audit_v1",
        "module_path": "capabilities.governance.no_runtime_boundary_audit_v1",
        "registry_role": "no_runtime_boundary_profiles",
        "reusable": True,
        "entrypoint": "audit_boundary(snapshot, profile)",
    },
    {
        "module_id": "controlled_trial_post_execution_review_harness",
        "harness_id": "controlled_trial_post_execution_review_harness_v1",
        "module_path": "capabilities.governance.controlled_trial_post_execution_review_harness_v1",
        "registry_role": "post_execution_review",
        "contract_defined": True,
        "runtime_consumption_tested_now": False,
        "entrypoint": "review_execution_result_contract_level(execution_result)",
    },
)

FUTURE_ADOPTION_MATRIX: Tuple[Dict[str, str], ...] = (
    {"chain": "vision_sample_frame_controlled_trial", "modules": "single_chain+authorization+post_review", "status": "first_integrated_consumer"},
    {"chain": "ocr_mock_controlled_trial", "modules": "single_chain+authorization+post_review", "status": "second_integrated_consumer"},
    {"chain": "ocr_real_provider_trial", "modules": "single_chain+authorization+extra_review", "status": "planned_later"},
    {
        "chain": "navigation_guidance_candidate_trial",
        "modules": "single_chain+authorization+post_review",
        "status": "third_integrated_consumer",
    },
    {"chain": "task_response_candidate_trial", "modules": "single_chain+authorization", "status": "planned"},
    {"chain": "voice_output_candidate_trial", "modules": "single_chain+authorization", "status": "planned_later"},
    {"chain": "memory_readonly_lookup_trial", "modules": "single_chain+authorization", "status": "planned_later"},
    {"chain": "world_model_readonly_candidate_trial", "modules": "single_chain+authorization", "status": "planned_later"},
)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _check_go(root: Path) -> Tuple[bool, Dict[str, Any]]:
    sm = _try_read_json(root / "summary.json") or {}
    vr = _try_read_json(root / "verifier_report.json") or {}
    ok = (vr.get("verifier") == "GO" and vr.get("passed") is True) or sm.get("boundary_ok") is True
    return ok, {"summary": sm, "verifier": vr}


def validate_consolidation_upstream(reference_roots: Dict[str, str]) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    ctx: Dict[str, Any] = {"roots": reference_roots}

    checks = [
        ("migration_final_closure", "migration final closure"),
        ("b0_harness_adoption_closure", "b0 harness adoption closure"),
        ("single_chain_harness_closure", "single chain harness closure"),
        ("vision_plan_and_dryrun", "vision plan_and_dryrun"),
        ("vision_controlled_trial_dryrun", "vision controlled trial dryrun"),
        ("vision_auth_planning", "vision auth planning"),
        ("vision_auth_dryrun", "vision auth dryrun"),
        ("vision_request_planning", "vision request planning"),
    ]

    for key, label in checks:
        root = Path(reference_roots.get(key, "")).expanduser()
        if not root.is_dir():
            blockers.append(f"{label}: root missing")
            continue
        ok, data = _check_go(root)
        ctx[key] = data
        if not ok:
            blockers.append(f"{label}: verifier must be GO")

    release_flags = (
        "trial_execution_authorized_now",
        "controlled_trial_started_now",
        "execution_window_opened_now",
        "request_sent_now",
        "grant_issued_now",
    )
    for key in ("vision_auth_planning", "vision_request_planning", "vision_controlled_trial_dryrun"):
        sm = ctx.get(key, {}).get("summary") or {}
        for flag in release_flags:
            if sm.get(flag) is True:
                blockers.append(f"{key}: {flag} must be false")

    return blockers, ctx


def build_factory_consolidation_artifacts(
    *,
    meta: Dict[str, Any],
    reference_roots: Dict[str, str],
    boundary_ok: bool,
) -> Dict[str, Any]:
    auth_example = build_vision_sample_frame_authorization_config(
        source_validation_phase="Phase-Luna-Validation-Factory-Consolidation-v1-001",
    )
    auth_contract = build_extraction_planning_artifacts(
        meta=meta,
        reference_roots=reference_roots,
        boundary_ok=True,
    )

    return {
        "policy": {
            "policy_id": "luna_validation_factory_consolidation_policy_v1",
            "factory_id": FACTORY_ID,
            "factory_version": FACTORY_VERSION,
            "scope": "luna_validation_factory_consolidation_only",
            "module_count": len(MODULE_REGISTRY),
            "reference_roots": reference_roots,
            **meta,
        },
        "registry": {
            "registry_id": "validation_factory_module_registry_v1",
            "factory_id": FACTORY_ID,
            "modules": list(MODULE_REGISTRY),
            **meta,
        },
        "batch_review": {
            "review_id": "batch_preflight_harness_registry_review_v1",
            "harness_id": BATCH_PREFLIGHT_HARNESS_ID,
            "already_closed": True,
            "reusable": True,
            "registry_role": "engineering_migration_validation",
            "upstream_root": reference_roots.get("b0_harness_adoption_closure"),
            "review_pass": boundary_ok,
            **meta,
        },
        "single_chain_review": {
            "review_id": "single_chain_trial_validation_harness_registry_review_v1",
            "harness_id": SINGLE_CHAIN_HARNESS_ID,
            "already_closed": True,
            "first_consumer": "vision_sample_frame",
            "reusable": True,
            "upstream_root": reference_roots.get("single_chain_harness_closure"),
            "review_pass": boundary_ok,
            **meta,
        },
        "auth_harness_contract": {
            **auth_contract["lifecycle_contract"],
            "contract_id": "controlled_trial_authorization_harness_contract_v1",
            "harness_id": AUTH_HARNESS_ID,
            "required_config_fields": list(AUTHORIZATION_CONFIG_REQUIRED_FIELDS),
            "entrypoints": [
                "build_authorization_config",
                "validate_authorization_scope",
                "validate_allowlist_blocklist",
                "validate_pre_execution_gates",
                "validate_execution_window",
                "validate_request_lifecycle",
                "validate_grant_lifecycle",
                "produce_execution_readiness",
                "run_authorization_validate",
            ],
            "example_config": auth_example,
            **meta,
        },
        "candidate_contract": build_candidate_contract(meta=meta),
        "no_runtime_contract": build_no_runtime_contract(meta=meta),
        "post_review_contract": build_post_review_contract(meta=meta),
        "usage_guide": {
            "guide_id": "validation_factory_usage_guide_v1",
            "factory_id": FACTORY_ID,
            "standard_feature_flow": list(STANDARD_FEATURE_FLOW),
            "batch_flow": "batch_config → BatchPreflightHarness → execution → post_migration_review",
            "single_chain_flow": "chain_config → SingleChainTrialValidationHarness → readiness",
            "authorization_flow": "authorization_config → ControlledTrialAuthorizationHarness.validate → execution_readiness",
            "post_execution_flow": "execution_result → ControlledTrialPostExecutionReviewHarness → closure",
            "extra_phase_triggers": [
                "live_camera",
                "real_ocr_provider",
                "real_navigation_action",
                "task_commit",
                "worldmodel_memory_write",
                "user_facing_output",
                "external_provider",
                "safety_high_risk",
            ],
            **meta,
        },
        "anti_recursion": {
            "rules_id": "validation_factory_anti_recursion_rules_v1",
            "rules": list(FACTORY_ANTI_RECURSION),
            "single_chain_rules": list(SINGLE_CHAIN_ANTI_RECURSION),
            "authorization_rules": list(AUTH_ANTI_RECURSION),
            **meta,
        },
        "adoption_matrix": {
            "matrix_id": "validation_factory_future_adoption_matrix_v1",
            "trials": list(FUTURE_ADOPTION_MATRIX),
            "single_chain_chains": list(FUTURE_CHAIN_ADOPTIONS),
            "authorization_trials": list(FUTURE_TRIAL_ADOPTIONS),
            **meta,
        },
        "vision_integrated_review": {
            "review_id": "vision_sample_frame_integrated_consumer_review_v1",
            "single_chain_first_consumer": True,
            "authorization_legacy_phases_consumed": True,
            "harness_migration_target": "authorization_config → ControlledTrialAuthorizationHarness",
            "plan_and_dryrun_root": reference_roots.get("vision_plan_and_dryrun"),
            "controlled_trial_dryrun_root": reference_roots.get("vision_controlled_trial_dryrun"),
            "review_pass": boundary_ok,
            **meta,
        },
        "non_claims": {
            "register_id": "validation_factory_non_claims_register_v1",
            "non_claims": list(FACTORY_NON_CLAIMS),
            **meta,
        },
        "decision": {
            "decision_id": "validation_factory_consolidation_decision_v1",
            "final_decision": (
                "LUNA_VALIDATION_FACTORY_CONSOLIDATION_READY_FOR_VISION_SAMPLE_FRAME_AUTHORIZATION_VIA_HARNESS"
                if boundary_ok
                else "LUNA_VALIDATION_FACTORY_CONSOLIDATION_REQUIRES_FIXES"
            ),
            "recommended_next_phase": (
                "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Authorization-Via-Harness-v1-001"
                if boundary_ok
                else "Phase-Luna-Validation-Factory-Issue-Review-v1-001"
            ),
            "boundary_ok": boundary_ok,
            "validation_factory_contract_generated_now": True,
            **meta,
        },
    }

# -*- coding: utf-8 -*-
"""Controlled Trial Authorization Harness Validation Closure v1."""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.controlled_trial_authorization_harness_v1 import (
    ANTI_RECURSION_RULES,
    AUTHORIZATION_CONFIG_REQUIRED_FIELDS,
    HARNESS_ID,
    build_vision_sample_frame_authorization_config,
    validate_authorization_config,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Controlled-Trial-Authorization-Harness-Validation-Closure-v1-001"
CLOSURE_SCOPE = "controlled_trial_authorization_harness_validation_closure_only"
SOURCE_CHAIN = "controlled_trial_authorization_harness_validation_closure_v1"

UPSTREAM_EXTRACTION_PHASE = "Phase-Controlled-Trial-Authorization-Harness-Extraction-Planning-v1-001"
UPSTREAM_EXTRACTION_FINAL = (
    "CONTROLLED_TRIAL_AUTHORIZATION_HARNESS_EXTRACTION_PLANNING_READY_FOR_VALIDATION_CLOSURE"
)

UPSTREAM_VISION_REQUEST_DRYRUN_PHASE = (
    "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Request-DryRunAndReview-v1-001"
)
UPSTREAM_VISION_REQUEST_DRYRUN_FINAL = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_EXECUTION_AUTHORIZATION_REQUEST_DRYRUN_AND_REVIEW_READY_FOR_REQUEST_ARTIFACT_GENERATION_PLANNING"
)

FINAL_DECISION = (
    "CONTROLLED_TRIAL_AUTHORIZATION_HARNESS_VALIDATION_CLOSED_READY_FOR_VISION_SAMPLE_FRAME_AUTHORIZATION_LIFECYCLE"
)
NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Authorization-Lifecycle-v1-001"

HARNESS_MODULE_PATH = "capabilities/governance/controlled_trial_authorization_harness_v1.py"
REQUIRED_SYMBOLS: Tuple[str, ...] = (
    "build_vision_sample_frame_authorization_config",
    "validate_authorization_config",
    "validate_vision_authorization_reference_roots",
    "build_extraction_planning_artifacts",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "controlled_trial_authorization_harness_validation_closure_only": True,
        "closure_only": True,
        "harness_contract_validated_now": True,
        "harness_module_present_now": True,
        "harness_first_consumer_validated_now": True,
        "authorization_harness_enforced_globally_now": False,
        "request_artifact_generated_now": False,
        "request_sent_now": False,
        "grant_issued_now": False,
        "execution_window_opened_now": False,
        "controlled_trial_started_now": False,
        "trial_execution_authorized_now": False,
        "runtime_enabled_now": False,
        "live_camera_enabled_now": False,
        "vision_model_invoked_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def _try_read_json(path: Path) -> Any:
    try:
        import json

        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_harness_module(repo_root: Path) -> Tuple[bool, Dict[str, Any], List[str]]:
    issues: List[str] = []
    module_path = repo_root / HARNESS_MODULE_PATH
    file_exists = module_path.is_file()
    symbol_status: Dict[str, bool] = {}

    if file_exists:
        try:
            mod = importlib.import_module(
                "capabilities.governance.controlled_trial_authorization_harness_v1"
            )
            for sym in REQUIRED_SYMBOLS:
                symbol_status[sym] = callable(getattr(mod, sym, None))
            if getattr(mod, "HARNESS_ID", None) != HARNESS_ID:
                issues.append("HARNESS_ID mismatch")
            if not all(symbol_status.values()):
                issues.append("required symbols missing")
        except Exception as exc:  # noqa: BLE001
            issues.append(f"import_failed:{exc}")
    else:
        issues.append("harness_module_file_missing")

    passed = file_exists and not issues and all(symbol_status.values())
    return passed, {
        "review_id": "harness_module_presence_review_v1",
        "module_path": str(module_path),
        "file_exists": file_exists,
        "symbols": symbol_status,
        "issues": issues,
        "review_pass": passed,
    }, issues


def run_controlled_trial_authorization_harness_validation_closure_v1(
    *,
    controlled_trial_authorization_harness_extraction_planning_root: str,
    vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_dryrun_and_review_root: str,
    repo_root: Optional[str] = None,
    closure_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    extraction_root = Path(
        controlled_trial_authorization_harness_extraction_planning_root
    ).expanduser().resolve()
    vision_req_dryrun_root = Path(
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_dryrun_and_review_root
    ).expanduser().resolve()

    luna_core = Path(repo_root).expanduser().resolve() if repo_root else extraction_root.parent.parent.parent / "Luna-Core"
    if not (luna_core / "capabilities").is_dir():
        luna_core = Path(__file__).resolve().parents[2]

    out_root = (
        Path(closure_output_root).expanduser().resolve()
        if closure_output_root
        else extraction_root.parent / "controlled_trial_authorization_harness_validation_closure"
    )

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(extraction_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_extraction_planning_root": str(extraction_root),
        "upstream_vision_request_dryrun_and_review_root": str(vision_req_dryrun_root),
        "closure_output_root": str(out_root),
        "harness_module_ref": HARNESS_MODULE_PATH,
    }

    ext_sm = _try_read_json(extraction_root / "summary.json") or {}
    ext_vr = _try_read_json(extraction_root / "verifier_report.json") or {}
    contract = _try_read_json(extraction_root / "reusable_authorization_lifecycle_contract_v1.json") or {}
    anti_rules = _try_read_json(extraction_root / "anti_recursion_rules_for_authorization_trials_v1.json") or {}
    schema = _try_read_json(extraction_root / "authorization_config_schema_planning_v1.json") or {}

    ext_trusted = ext_vr.get("verifier") == "GO" and ext_vr.get("passed") is True
    if not ext_trusted and ext_sm.get("boundary_ok") is not True:
        blockers.append("extraction planning verifier must be GO")
    if ext_sm.get("final_decision") != UPSTREAM_EXTRACTION_FINAL:
        blockers.append("extraction final_decision mismatch")

    contract_fields_ok = all(
        f in (schema.get("required_fields") or []) for f in AUTHORIZATION_CONFIG_REQUIRED_FIELDS
    )
    if contract.get("harness_id") != HARNESS_ID:
        blockers.append("contract harness_id mismatch")
    if not contract_fields_ok:
        blockers.append("authorization config schema missing required fields")

    example = schema.get("example") or build_vision_sample_frame_authorization_config(
        source_validation_phase=UPSTREAM_VISION_REQUEST_DRYRUN_PHASE,
    )
    cfg_ok, cfg_issues = validate_authorization_config(example)
    if not cfg_ok:
        blockers.extend(cfg_issues)

    module_ok, module_review, module_issues = _review_harness_module(luna_core)
    blockers.extend(module_issues)

    vis_sm = _try_read_json(vision_req_dryrun_root / "summary.json") or {}
    vis_vr = _try_read_json(vision_req_dryrun_root / "verifier_report.json") or {}
    identity = _try_read_json(vision_req_dryrun_root / "request_identity_consumption_result_v1.json") or {}
    scope = _try_read_json(vision_req_dryrun_root / "request_scope_binding_consumption_result_v1.json") or {}
    lifecycle = _try_read_json(vision_req_dryrun_root / "request_lifecycle_consumption_result_v1.json") or {}

    vis_trusted = vis_vr.get("verifier") == "GO" and vis_vr.get("passed") is True
    vis_summary_ok = (
        vis_sm.get("boundary_ok") is True
        and vis_sm.get("phase") == UPSTREAM_VISION_REQUEST_DRYRUN_PHASE
        and vis_sm.get("final_decision") == UPSTREAM_VISION_REQUEST_DRYRUN_FINAL
    )
    if not vis_trusted and not vis_summary_ok:
        blockers.append("vision request dryrun+review verifier must be GO")
    if vis_sm.get("authorization_request_artifact_generated_now") is True:
        blockers.append("vision request artifact must not be generated yet")
    if vis_sm.get("execution_authorization_granted_now") is True:
        blockers.append("vision grant must not be issued yet")

    harness_reuse_ok = (
        identity.get("consumption_pass") is True
        and scope.get("consumption_pass") is True
        and lifecycle.get("current_state") == "planning_defined"
    )
    if not harness_reuse_ok:
        blockers.append("vision request dryrun consumption incomplete")

    policy = {
        "policy_id": "controlled_trial_authorization_harness_validation_closure_policy_v1",
        "scope": CLOSURE_SCOPE,
        "merges_phases": ["Harness-Extraction-Validation", "First-Consumer-Readiness"],
        **meta,
    }

    input_review = {
        "review_id": "extraction_planning_input_review_v1",
        "extraction_root": str(extraction_root),
        "extraction_verifier": ext_vr.get("verifier"),
        "review_pass": ext_trusted or ext_sm.get("boundary_ok") is True,
        **meta,
    }

    contract_review = {
        "review_id": "harness_contract_consumption_review_v1",
        "harness_id": contract.get("harness_id"),
        "required_fields_present": contract_fields_ok,
        "example_config_valid": cfg_ok,
        "review_pass": contract_fields_ok and cfg_ok,
        **meta,
    }

    module_review_payload = {**module_review, **meta}

    vision_review = {
        "review_id": "vision_first_authorization_consumer_review_v1",
        "trial_id": "vision_sample_frame_controlled",
        "request_dryrun_root": str(vision_req_dryrun_root),
        "identity_consumption_pass": identity.get("consumption_pass"),
        "scope_consumption_pass": scope.get("consumption_pass"),
        "lifecycle_state": lifecycle.get("current_state"),
        "harness_config_example_chain_id": example.get("chain_id"),
        "review_pass": vis_summary_ok and harness_reuse_ok,
        **meta,
    }

    schema_closure = {
        "closure_id": "authorization_config_schema_closure_v1",
        "schema_id": schema.get("schema_id"),
        "example_chain_id": example.get("chain_id"),
        "frozen": True,
        **meta,
    }

    anti_closure = {
        "closure_id": "anti_recursion_rule_closure_v1",
        "rules": anti_rules.get("rules") or list(ANTI_RECURSION_RULES),
        "no_full_auth_planning_chain": True,
        "harness_first_required": True,
        **meta,
    }

    usage_guide = {
        "guide_id": "future_authorization_usage_guide_v1",
        "standard_flow": [
            "authorization_config",
            "ControlledTrialAuthorizationHarness.validate",
            "request_lifecycle_result",
            "grant_lifecycle_result",
            "controlled_trial_execution",
            "post_execution_review",
        ],
        "per_trial_outputs_only": [
            "authorization_config",
            "authorization_validation_result",
            "request_lifecycle_result",
            "grant_lifecycle_result",
            "execution_result",
            "post_execution_review_result",
        ],
        "superseded_phases": [
            "Authorization Planning",
            "Authorization DryRunAndReview",
            "Request Planning",
            "Request DryRunAndReview",
        ],
        **meta,
    }

    boundary_ok = (
        len(blockers) == 0
        and module_ok
        and contract_review.get("review_pass")
        and vision_review.get("review_pass")
    )

    closure_decision = {
        "decision_id": "controlled_trial_authorization_harness_validation_closure_decision_v1",
        "final_decision": FINAL_DECISION if boundary_ok else "CONTROLLED_TRIAL_AUTHORIZATION_HARNESS_VALIDATION_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "boundary_ok": boundary_ok,
        "harness_validation_closed": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "controlled_trial_authorization_harness_validation_closure_policy": policy,
        "extraction_planning_input_review": input_review,
        "harness_contract_consumption_review": contract_review,
        "harness_module_presence_review": module_review_payload,
        "vision_first_authorization_consumer_review": vision_review,
        "authorization_config_schema_closure": schema_closure,
        "anti_recursion_rule_closure": anti_closure,
        "future_authorization_usage_guide": usage_guide,
        "controlled_trial_authorization_harness_validation_closure_decision": closure_decision,
        "summary": summary,
    }

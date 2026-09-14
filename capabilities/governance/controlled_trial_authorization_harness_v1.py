# -*- coding: utf-8 -*-
"""Controlled Trial Authorization Harness v1.

Reusable authorization lifecycle validation for controlled trials:
planning → dryrun/review → request → grant → execution → post-execution review.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_v1 import (
    PLANNED_EXECUTION_OUTPUT_DIR,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_v1 import (
    ABORT_CONDITIONS,
    AUTHORIZATION_ALLOWED,
    AUTHORIZATION_FORBIDDEN,
    EXECUTION_ALLOWLIST,
    EXECUTION_BLOCKLIST,
    POST_EXECUTION_REVIEW_PHASE,
    PRE_EXECUTION_GATES,
    TRIAL_SCOPE,
)

HARNESS_ID = "controlled_trial_authorization_harness_v1"
HARNESS_MODULE = "capabilities.governance.controlled_trial_authorization_harness_v1"

AUTHORIZATION_CONFIG_REQUIRED_FIELDS: Tuple[str, ...] = (
    "chain_id",
    "trial_id",
    "trial_domain",
    "target_execution_phase",
    "source_validation_phase",
    "trial_scope",
    "input_allowlist",
    "input_blocklist",
    "execution_allowlist",
    "execution_blocklist",
    "pre_execution_gates",
    "abort_conditions",
    "output_contract",
    "execution_window",
    "logging_policy",
    "post_execution_review_required",
    "request_lifecycle",
    "grant_lifecycle",
    "non_claims",
)

AUTH_LIFECYCLE_STATES: Tuple[str, ...] = (
    "planning_defined",
    "authorization_dryrun_reviewed",
    "request_artifact_generation_planning",
    "request_artifact_generated",
    "request_send_planning",
    "request_sent",
    "grant_planning",
    "grant_issued",
    "execution_window_opened",
    "controlled_trial_execution",
    "post_execution_review",
    "closed",
)

GRANT_LIFECYCLE_STATES: Tuple[str, ...] = (
    "grant_not_requested",
    "grant_planning",
    "grant_pending",
    "grant_issued",
    "grant_revoked",
    "grant_expired",
)

HARNESS_NON_CLAIMS: Tuple[str, ...] = (
    "authorization planning GO ≠ execution authorized",
    "authorization dryrun GO ≠ request generated",
    "request planning GO ≠ request artifact generated",
    "request artifact generated ≠ request sent",
    "request sent ≠ grant issued",
    "grant issued ≠ trial execution started",
    "trial execution completed ≠ fact write",
    "trial output logging ≠ WorldModel / Memory write",
)

ANTI_RECURSION_RULES: Tuple[str, ...] = (
    "Do not regenerate full Authorization Planning → DryRunAndReview → Request Planning → Request DryRunAndReview per trial",
    "Subsequent controlled trials must use ControlledTrialAuthorizationHarness first",
    "Per trial only: authorization_config + authorization_validation_result + request_lifecycle_result + grant_lifecycle_result + execution_result + post_execution_review_result",
    "Extra authorization review only when opening real runtime, fact layer, task commit, user output, or external provider",
)

FUTURE_TRIAL_ADOPTIONS: Tuple[Dict[str, str], ...] = (
    {"trial_id": "vision_sample_frame_controlled", "chain_id": "vision_sample_frame", "domain": "vision", "status": "first_consumer"},
    {"trial_id": "ocr_mock_controlled", "chain_id": "ocr_mock_result_single_chain", "domain": "ocr", "status": "second_consumer"},
    {"trial_id": "ocr_provider_controlled", "chain_id": "ocr_provider", "domain": "ocr", "status": "planned_later"},
    {
        "trial_id": "navigation_guidance_controlled",
        "chain_id": "navigation_guidance_candidate_single_chain",
        "domain": "navigation",
        "status": "third_consumer",
    },
    {"trial_id": "task_candidate", "chain_id": "task_response", "domain": "task", "status": "planned"},
    {"trial_id": "voice_output_candidate", "chain_id": "voice_output", "domain": "voice", "status": "planned_later"},
)

OCR_AUTHORIZATION_ALLOWED: Tuple[str, ...] = (
    "mock_ocr_response",
    "fixture_ocr_response",
    "previous_ocr_request_candidate",
    "visual_observation_candidate_reference",
)

OCR_AUTHORIZATION_FORBIDDEN: Tuple[str, ...] = (
    "real_ocr_provider",
    "paddleocr",
    "rapidocr",
    "live_image_read",
    "arbitrary_image_read",
    "ocr_evidence_generation",
    "fact_write",
    "worldmodel_write",
    "memory_write",
    "navigation",
    "task_commit",
    "tts",
    "llm",
    "user_facing_output",
)

OCR_EXECUTION_ALLOWLIST: Tuple[str, ...] = (
    "mock_ocr_fixture_input",
    "candidate_generation",
    "controlled_logging",
)

OCR_EXECUTION_BLOCKLIST: Tuple[str, ...] = (
    "real_ocr_provider",
    "paddleocr",
    "rapidocr",
    "ocr_evidence",
    "fact_write",
    "runtime_action",
    "worldmodel_write",
    "memory_write",
)

OCR_TRIAL_SCOPE = "ocr_mock_result_single_chain"
OCR_PLANNED_EXECUTION_OUTPUT_DIR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_mock_result_single_chain_trial_via_validation_factory/_controlled_execution"
)

NAV_AUTHORIZATION_ALLOWED: Tuple[str, ...] = (
    "synthetic_route_context",
    "readonly_map_hint",
    "visual_observation_candidate_reference",
    "task_context_fixture",
    "prior_navigation_guidance_candidate",
)

NAV_AUTHORIZATION_FORBIDDEN: Tuple[str, ...] = (
    "live_navigation_runtime",
    "navigation_action",
    "map_write",
    "gps_strong_anchor_commit",
    "route_commit",
    "user_facing_output",
    "task_commit",
    "worldmodel_write",
    "memory_write",
    "tts",
    "llm",
    "real_ocr_provider",
    "live_camera",
)

NAV_EXECUTION_ALLOWLIST: Tuple[str, ...] = (
    "synthetic_route_fixture_input",
    "readonly_map_hint_input",
    "candidate_generation",
    "controlled_logging",
)

NAV_EXECUTION_BLOCKLIST: Tuple[str, ...] = (
    "live_navigation_runtime",
    "navigation_action",
    "map_write",
    "gps_strong_anchor_commit",
    "route_commit",
    "user_facing_output",
    "task_commit",
    "fact_write",
    "runtime_action",
    "worldmodel_write",
    "memory_write",
)

NAV_TRIAL_SCOPE = "navigation_guidance_candidate_single_chain"
NAV_PLANNED_EXECUTION_OUTPUT_DIR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "navigation_guidance_candidate_single_chain_trial_via_validation_factory/_controlled_execution"
)

DEFAULT_OUTPUT_CONTRACT: Dict[str, Any] = {
    "output_type": "visual_observation_candidate",
    "candidate_only": True,
    "fact_status": "not_fact",
    "write_allowed": False,
    "runtime_action_allowed": False,
    "source_chain_present": True,
    "frame_ref_present": True,
    "timestamp_present": True,
}

DEFAULT_EXECUTION_WINDOW: Dict[str, Any] = {
    "execution_window_type": "controlled_fixture_only",
    "max_trial_scope": "single_chain",
    "max_output_count": 3,
    "no_live_input": True,
    "no_external_provider": True,
    "no_user_facing_output": True,
}

DEFAULT_LOGGING_POLICY: Dict[str, Any] = {
    "workspace_fallback_only": True,
    "forbidden_targets": [
        "repo__eval_out",
        "WorldModel",
        "Memory",
        "SceneDelta",
        "protected",
        "HR",
        "DnAE",
    ],
}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def build_vision_sample_frame_authorization_config(
    *,
    source_validation_phase: str,
    output_directory: Optional[str] = None,
) -> Dict[str, Any]:
    out_dir = output_directory or PLANNED_EXECUTION_OUTPUT_DIR
    return {
        "chain_id": "vision_sample_frame",
        "trial_id": "vision_sample_frame_controlled",
        "trial_domain": "vision",
        "target_execution_phase": "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-v1-001",
        "source_validation_phase": source_validation_phase,
        "trial_scope": "controlled_fixture_only",
        "chain_trial_scope": TRIAL_SCOPE,
        "input_allowlist": list(AUTHORIZATION_ALLOWED),
        "input_blocklist": list(AUTHORIZATION_FORBIDDEN),
        "execution_allowlist": list(EXECUTION_ALLOWLIST),
        "execution_blocklist": list(EXECUTION_BLOCKLIST),
        "pre_execution_gates": list(PRE_EXECUTION_GATES),
        "abort_conditions": list(ABORT_CONDITIONS),
        "output_contract": {**DEFAULT_OUTPUT_CONTRACT, "trial_scope": TRIAL_SCOPE},
        "execution_window": {
            **DEFAULT_EXECUTION_WINDOW,
            "output_directory": out_dir,
            "post_execution_review_required": True,
        },
        "logging_policy": {**DEFAULT_LOGGING_POLICY, "allowed_write_root": out_dir},
        "post_execution_review_required": True,
        "post_execution_review_phase": POST_EXECUTION_REVIEW_PHASE,
        "request_lifecycle": list(AUTH_LIFECYCLE_STATES),
        "grant_lifecycle": list(GRANT_LIFECYCLE_STATES),
        "non_claims": list(HARNESS_NON_CLAIMS),
    }


def build_ocr_mock_authorization_config(
    *,
    source_validation_phase: str,
    output_directory: Optional[str] = None,
) -> Dict[str, Any]:
    out_dir = output_directory or OCR_PLANNED_EXECUTION_OUTPUT_DIR
    ocr_output_contract = {
        "output_type": "ocr_result_candidate",
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_action_allowed": False,
        "source_chain_present": True,
        "provenance_present": True,
        "provider_type": "mock_or_fixture_only",
        "trial_scope": OCR_TRIAL_SCOPE,
    }
    return {
        "chain_id": "ocr_mock_result_single_chain",
        "trial_id": "ocr_mock_controlled",
        "trial_domain": "ocr",
        "target_execution_phase": "Phase-OCR-Mock-Result-Single-Chain-Trial-Via-Validation-Factory-v1-001",
        "source_validation_phase": source_validation_phase,
        "trial_scope": "controlled_fixture_only",
        "chain_trial_scope": OCR_TRIAL_SCOPE,
        "input_allowlist": list(OCR_AUTHORIZATION_ALLOWED),
        "input_blocklist": list(OCR_AUTHORIZATION_FORBIDDEN),
        "execution_allowlist": list(OCR_EXECUTION_ALLOWLIST),
        "execution_blocklist": list(OCR_EXECUTION_BLOCKLIST),
        "pre_execution_gates": list(PRE_EXECUTION_GATES) + ["no_real_ocr_provider_gate", "no_ocr_evidence_gate"],
        "abort_conditions": list(ABORT_CONDITIONS) + [
            "real_ocr_provider_requested",
            "paddleocr_requested",
            "rapidocr_requested",
            "ocr_evidence_generation_requested",
            "ocr_fact_write_requested",
        ],
        "output_contract": ocr_output_contract,
        "execution_window": {
            **DEFAULT_EXECUTION_WINDOW,
            "output_directory": out_dir,
            "post_execution_review_required": True,
        },
        "logging_policy": {**DEFAULT_LOGGING_POLICY, "allowed_write_root": out_dir},
        "post_execution_review_required": True,
        "post_execution_review_phase": "Phase-OCR-Mock-Result-Single-Chain-Trial-Via-Validation-Factory-v1-001",
        "request_lifecycle": list(AUTH_LIFECYCLE_STATES),
        "grant_lifecycle": list(GRANT_LIFECYCLE_STATES),
        "non_claims": list(HARNESS_NON_CLAIMS),
    }


def build_navigation_guidance_authorization_config(
    *,
    source_validation_phase: str,
    output_directory: Optional[str] = None,
) -> Dict[str, Any]:
    out_dir = output_directory or NAV_PLANNED_EXECUTION_OUTPUT_DIR
    nav_output_contract = {
        "output_type": "navigation_guidance_candidate",
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_action_allowed": False,
        "user_facing_output_allowed": False,
        "navigation_action_allowed": False,
        "source_chain_present": True,
        "provenance_present": True,
        "map_context_type": "readonly_or_synthetic_only",
        "trial_scope": NAV_TRIAL_SCOPE,
    }
    return {
        "chain_id": "navigation_guidance_candidate_single_chain",
        "trial_id": "navigation_guidance_controlled",
        "trial_domain": "navigation",
        "target_execution_phase": (
            "Phase-Navigation-Guidance-Candidate-Single-Chain-Trial-Via-Validation-Factory-v1-001"
        ),
        "source_validation_phase": source_validation_phase,
        "trial_scope": "controlled_fixture_only",
        "chain_trial_scope": NAV_TRIAL_SCOPE,
        "input_allowlist": list(NAV_AUTHORIZATION_ALLOWED),
        "input_blocklist": list(NAV_AUTHORIZATION_FORBIDDEN),
        "execution_allowlist": list(NAV_EXECUTION_ALLOWLIST),
        "execution_blocklist": list(NAV_EXECUTION_BLOCKLIST),
        "pre_execution_gates": list(PRE_EXECUTION_GATES)
        + ["no_navigation_action_gate", "no_map_write_gate", "no_gps_commit_gate"],
        "abort_conditions": list(ABORT_CONDITIONS)
        + [
            "navigation_action_requested",
            "map_write_requested",
            "gps_strong_anchor_commit_requested",
            "route_commit_requested",
            "user_facing_output_requested",
            "task_commit_requested",
        ],
        "output_contract": nav_output_contract,
        "execution_window": {
            **DEFAULT_EXECUTION_WINDOW,
            "output_directory": out_dir,
            "post_execution_review_required": True,
        },
        "logging_policy": {**DEFAULT_LOGGING_POLICY, "allowed_write_root": out_dir},
        "post_execution_review_required": True,
        "post_execution_review_phase": (
            "Phase-Navigation-Guidance-Candidate-Single-Chain-Trial-Via-Validation-Factory-v1-001"
        ),
        "request_lifecycle": list(AUTH_LIFECYCLE_STATES),
        "grant_lifecycle": list(GRANT_LIFECYCLE_STATES),
        "non_claims": list(HARNESS_NON_CLAIMS),
    }


def validate_vision_authorization_reference_roots(
    *,
    authorization_planning_root: Path,
    authorization_dryrun_and_review_root: Path,
    request_planning_root: Path,
) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    ctx: Dict[str, Any] = {}

    roots = {
        "authorization_planning": authorization_planning_root,
        "authorization_dryrun_and_review": authorization_dryrun_and_review_root,
        "request_planning": request_planning_root,
    }

    release_flags = (
        "authorization_request_artifact_generated_now",
        "authorization_request_sent_now",
        "execution_authorization_granted_now",
        "trial_execution_authorized_now",
        "controlled_trial_started_now",
        "execution_window_opened_now",
    )

    for name, root in roots.items():
        sm = _try_read_json(root / "summary.json") or {}
        vr = _try_read_json(root / "verifier_report.json") or {}
        ctx[f"{name}_sm"] = sm
        ctx[f"{name}_vr"] = vr

        if not (vr.get("verifier") == "GO" and vr.get("passed") is True):
            if sm.get("boundary_ok") is not True:
                blockers.append(f"{name}: verifier must be GO")
        for flag in release_flags:
            if sm.get(flag) is True:
                blockers.append(f"{name}: {flag} must be false")

    plan_sm = ctx["authorization_planning_sm"]
    if plan_sm.get("controlled_trial_execution_authorization_planning_only") is not True:
        blockers.append("authorization planning must be planning_only")
    dry_sm = ctx["authorization_dryrun_and_review_sm"]
    if dry_sm.get("execution_authorization_dryrun_and_review_only") is not True:
        blockers.append("authorization dryrun+review must be dryrun_and_review_only")
    req_sm = ctx["request_planning_sm"]
    if req_sm.get("execution_authorization_request_planning_only") is not True:
        blockers.append("request planning must be request_planning_only")
    if req_sm.get("lifecycle_current_state") != "planning_defined":
        blockers.append("request planning lifecycle must be planning_defined")

    return blockers, ctx


def build_extraction_planning_artifacts(
    *,
    meta: Dict[str, Any],
    reference_roots: Dict[str, str],
    boundary_ok: bool,
) -> Dict[str, Any]:
    example_config = build_vision_sample_frame_authorization_config(
        source_validation_phase="Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-Authorization-Request-DryRunAndReview-v1-001",
    )

    lifecycle_contract = {
        "contract_id": "reusable_authorization_lifecycle_contract_v1",
        "harness_id": HARNESS_ID,
        "authorization_lifecycle": list(AUTH_LIFECYCLE_STATES),
        "grant_lifecycle": list(GRANT_LIFECYCLE_STATES),
        "entrypoint_validate": "ControlledTrialAuthorizationHarness.validate(authorization_config, boundary_meta)",
        "entrypoint_lifecycle": "ControlledTrialAuthorizationHarness.run_authorization_lifecycle(authorization_config)",
        "required_per_trial_outputs": [
            "authorization_config",
            "authorization_validation_result",
            "request_lifecycle_result",
            "grant_lifecycle_result",
            "execution_result",
            "post_execution_review_result",
        ],
        **meta,
    }

    return {
        "extraction_policy": {
            "policy_id": "controlled_trial_authorization_harness_extraction_policy_v1",
            "scope": "controlled_trial_authorization_harness_extraction_planning_only",
            "harness_module": HARNESS_MODULE,
            "harness_id": HARNESS_ID,
            "reference_roots": reference_roots,
            **meta,
        },
        "lifecycle_contract": lifecycle_contract,
        "config_schema": {
            "schema_id": "authorization_config_schema_planning_v1",
            "required_fields": list(AUTHORIZATION_CONFIG_REQUIRED_FIELDS),
            "example": example_config,
            **meta,
        },
        "scope_contract": {
            "contract_id": "authorization_scope_contract_planning_v1",
            "input_allowlist_pattern": list(AUTHORIZATION_ALLOWED),
            "input_blocklist_pattern": list(AUTHORIZATION_FORBIDDEN),
            "vision_reference": list(AUTHORIZATION_ALLOWED),
            **meta,
        },
        "allowlist_blocklist_contract": {
            "contract_id": "allowlist_blocklist_contract_planning_v1",
            "execution_allowlist_pattern": list(EXECUTION_ALLOWLIST),
            "execution_blocklist_pattern": list(EXECUTION_BLOCKLIST),
            **meta,
        },
        "gate_contract": {
            "contract_id": "pre_execution_gate_contract_planning_v1",
            "gates": list(PRE_EXECUTION_GATES),
            "gates_total": len(PRE_EXECUTION_GATES),
            **meta,
        },
        "window_contract": {
            "contract_id": "execution_window_contract_planning_v1",
            "defaults": dict(DEFAULT_EXECUTION_WINDOW),
            "planned_output_directory": PLANNED_EXECUTION_OUTPUT_DIR,
            **meta,
        },
        "abort_contract": {
            "contract_id": "abort_condition_contract_planning_v1",
            "conditions": list(ABORT_CONDITIONS),
            "conditions_total": len(ABORT_CONDITIONS),
            **meta,
        },
        "output_contract": {
            "contract_id": "output_contract_binding_planning_v1",
            "defaults": dict(DEFAULT_OUTPUT_CONTRACT),
            **meta,
        },
        "request_lifecycle_contract": {
            "contract_id": "request_lifecycle_contract_planning_v1",
            "states": list(AUTH_LIFECYCLE_STATES),
            "initial_state": "planning_defined",
            **meta,
        },
        "grant_lifecycle_contract": {
            "contract_id": "grant_lifecycle_contract_planning_v1",
            "states": list(GRANT_LIFECYCLE_STATES),
            "initial_state": "grant_not_requested",
            **meta,
        },
        "post_review_contract": {
            "contract_id": "post_execution_review_contract_planning_v1",
            "required_phase": POST_EXECUTION_REVIEW_PHASE,
            "mandatory": True,
            "cannot_bypass": True,
            **meta,
        },
        "adoption_matrix": {
            "matrix_id": "future_trial_authorization_adoption_matrix_v1",
            "trials": list(FUTURE_TRIAL_ADOPTIONS),
            "first_consumer": "vision_sample_frame_controlled",
            **meta,
        },
        "anti_recursion": {
            "rules_id": "anti_recursion_rules_for_authorization_trials_v1",
            "rules": list(ANTI_RECURSION_RULES),
            "superseded_phase_pattern": "Authorization Planning → DryRunAndReview → Request Planning → Request DryRunAndReview",
            **meta,
        },
        "readiness": {
            "decision_id": "controlled_trial_authorization_harness_readiness_decision_v1",
            "final_decision": (
                "CONTROLLED_TRIAL_AUTHORIZATION_HARNESS_EXTRACTION_PLANNING_READY_FOR_VALIDATION_CLOSURE"
                if boundary_ok
                else "CONTROLLED_TRIAL_AUTHORIZATION_HARNESS_EXTRACTION_PLANNING_REQUIRES_FIXES"
            ),
            "recommended_next_phase": (
                "Phase-Controlled-Trial-Authorization-Harness-Validation-Closure-v1-001"
                if boundary_ok
                else "Phase-Controlled-Trial-Authorization-Harness-Issue-Review-v1-001"
            ),
            "harness_planned_not_generated": True,
            "harness_contract_planned": True,
            "boundary_ok": boundary_ok,
            **meta,
        },
    }


def validate_authorization_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate authorization_config shape (harness consumer contract)."""
    issues: List[str] = []
    for field in AUTHORIZATION_CONFIG_REQUIRED_FIELDS:
        if field not in config:
            issues.append(f"missing field: {field}")
    if config.get("post_execution_review_required") is not True:
        issues.append("post_execution_review_required must be true")
    gates = config.get("pre_execution_gates") or []
    if len(gates) < len(PRE_EXECUTION_GATES):
        issues.append("pre_execution_gates incomplete")
    return len(issues) == 0, issues


def _simulate_gate_validation(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    gates = config.get("pre_execution_gates") or list(PRE_EXECUTION_GATES)
    return [
        {
            "gate_id": g,
            "validation_pass": True,
            "simulated": True,
        }
        for g in gates
    ]


def run_authorization_validate(
    authorization_config: Dict[str, Any],
    *,
    boundary_meta: Optional[Dict[str, Any]] = None,
    upstream_blockers: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Single-shot harness validation: config → validation → lifecycle readiness (no grant/execution)."""
    meta = dict(boundary_meta or {})
    blockers = list(upstream_blockers or [])

    cfg_ok, cfg_issues = validate_authorization_config(authorization_config)
    blockers.extend(cfg_issues)

    window = authorization_config.get("execution_window") or {}
    out_dir = str(window.get("output_directory") or PLANNED_EXECUTION_OUTPUT_DIR)
    window_ok = all(
        [
            window.get("execution_window_type") == "controlled_fixture_only",
            window.get("max_trial_scope") == "single_chain",
            window.get("max_output_count") == 3,
            window.get("no_live_input") is True,
            "Luna-Workspace-Min" in out_dir or "Luna-Workspace-Min" in str(
                (authorization_config.get("logging_policy") or {}).get("allowed_write_root", "")
            ),
        ]
    )
    if not window_ok:
        blockers.append("execution_window contract invalid")

    domain = authorization_config.get("trial_domain", "vision")
    if domain == "navigation":
        required_allowed = NAV_AUTHORIZATION_ALLOWED
        required_blocked = (
            "live_navigation_runtime",
            "navigation_action",
            "map_write",
            "gps_strong_anchor_commit",
            "user_facing_output",
        )
    elif domain == "ocr":
        required_allowed = OCR_AUTHORIZATION_ALLOWED
        required_blocked = ("real_ocr_provider", "paddleocr", "rapidocr", "fact_write")
    else:
        required_allowed = AUTHORIZATION_ALLOWED
        required_blocked = ("live_camera", "fact_write", "vision_model_inference")

    allowed = set(authorization_config.get("input_allowlist") or [])
    for item in required_allowed:
        if item not in allowed:
            blockers.append(f"input_allowlist missing: {item}")

    blocked = set(authorization_config.get("input_blocklist") or [])
    for item in required_blocked:
        if item not in blocked:
            blockers.append(f"input_blocklist missing: {item}")

    output = authorization_config.get("output_contract") or {}
    output_ok = all(
        [
            output.get("candidate_only") is True,
            output.get("fact_status") == "not_fact",
            output.get("write_allowed") is False,
        ]
    )
    if not output_ok:
        blockers.append("output_contract invalid")

    validation_pass = len(blockers) == 0 and cfg_ok

    gate_rows = _simulate_gate_validation(authorization_config)

    request_lifecycle = {
        "result_id": "request_lifecycle_result",
        "harness_id": HARNESS_ID,
        "simulated": True,
        "prior_states_absorbed": [
            "Authorization Planning",
            "Authorization DryRunAndReview",
            "Request Planning",
            "Request DryRunAndReview",
        ],
        "current_state": "authorization_dryrun_reviewed" if validation_pass else "planning_defined",
        "target_states": list(AUTH_LIFECYCLE_STATES),
        "lifecycle_pass": validation_pass,
        "authorization_request_artifact_generated_now": False,
        "authorization_request_sent_now": False,
        **meta,
    }

    grant_lifecycle = {
        "result_id": "grant_lifecycle_result",
        "harness_id": HARNESS_ID,
        "simulated": True,
        "current_state": "grant_planning" if validation_pass else "grant_not_requested",
        "target_states": list(GRANT_LIFECYCLE_STATES),
        "grant_readiness_pass": validation_pass,
        "execution_authorization_granted_now": False,
        "grant_issued_now": False,
        **meta,
    }

    validation_result = {
        "result_id": "authorization_validation_result",
        "harness_id": HARNESS_ID,
        "validation_pass": validation_pass,
        "config_valid": cfg_ok,
        "gates": gate_rows,
        "gates_passed": sum(1 for g in gate_rows if g.get("validation_pass")),
        "gates_total": len(gate_rows),
        "scope_narrow": True,
        "blockers": blockers,
        **meta,
    }

    execution_readiness = {
        "decision_id": "controlled_trial_execution_readiness_decision",
        "ready_for_controlled_trial_execution": validation_pass,
        "ready_for_post_execution_review_after_execution": validation_pass,
        "trial_execution_authorized_now": False,
        "controlled_trial_started_now": False,
        "execution_window_opened_now": False,
        "target_execution_phase": authorization_config.get("target_execution_phase"),
        "post_execution_review_phase": authorization_config.get("post_execution_review_phase")
        or POST_EXECUTION_REVIEW_PHASE,
        **meta,
    }

    return {
        "authorization_validation_result": validation_result,
        "request_lifecycle_result": request_lifecycle,
        "grant_lifecycle_result": grant_lifecycle,
        "execution_readiness": execution_readiness,
        "validation_pass": validation_pass,
        "blockers": blockers,
    }


def build_authorization_config(**kwargs: Any) -> Dict[str, Any]:
    """Factory entry: build authorization_config (domain-specific builder)."""
    if kwargs.get("trial_domain") == "navigation" or kwargs.get("chain_id") == "navigation_guidance_candidate_single_chain":
        return build_navigation_guidance_authorization_config(**kwargs)
    if kwargs.get("trial_domain") == "ocr" or kwargs.get("chain_id") == "ocr_mock_result_single_chain":
        return build_ocr_mock_authorization_config(**kwargs)
    return build_vision_sample_frame_authorization_config(**kwargs)


def validate_authorization_scope(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    allowed = set(config.get("input_allowlist") or [])
    for item in AUTHORIZATION_ALLOWED:
        if item not in allowed:
            issues.append(f"missing allowed: {item}")
    forbidden = set(config.get("input_blocklist") or [])
    for item in AUTHORIZATION_FORBIDDEN[:6]:
        if item not in forbidden:
            issues.append(f"missing forbidden: {item}")
    return len(issues) == 0, issues


def validate_allowlist_blocklist(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for op in EXECUTION_ALLOWLIST:
        if op not in (config.get("execution_allowlist") or []):
            issues.append(f"execution_allowlist missing: {op}")
    for op in ("live_camera", "model_inference", "runtime_action"):
        if op not in (config.get("execution_blocklist") or []):
            issues.append(f"execution_blocklist missing: {op}")
    return len(issues) == 0, issues


def validate_pre_execution_gates(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    gates = config.get("pre_execution_gates") or []
    missing = [g for g in PRE_EXECUTION_GATES if g not in gates]
    return len(missing) == 0, [f"missing gate: {g}" for g in missing]


def validate_execution_window(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    window = config.get("execution_window") or {}
    issues: List[str] = []
    if window.get("execution_window_type") != "controlled_fixture_only":
        issues.append("execution_window_type invalid")
    if window.get("max_trial_scope") != "single_chain":
        issues.append("max_trial_scope invalid")
    return len(issues) == 0, issues


def validate_request_lifecycle(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    states = config.get("request_lifecycle") or []
    if not states:
        issues = ["request_lifecycle empty"]
    else:
        issues = [s for s in AUTH_LIFECYCLE_STATES if s not in states]
    return len(issues) == 0, [f"missing lifecycle state: {s}" for s in issues]


def validate_grant_lifecycle(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    states = config.get("grant_lifecycle") or []
    if not states:
        return False, ["grant_lifecycle empty"]
    missing = [s for s in GRANT_LIFECYCLE_STATES if s not in states]
    return len(missing) == 0, [f"missing grant state: {s}" for s in missing]


def produce_execution_readiness(
    authorization_config: Dict[str, Any],
    *,
    boundary_meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Factory entry: full validate → execution_readiness."""
    return run_authorization_validate(authorization_config, boundary_meta=boundary_meta)["execution_readiness"]

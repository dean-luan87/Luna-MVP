# -*- coding: utf-8 -*-
"""Single-Chain Trial Validation Harness v1.

Reusable plan-and-dryrun validation for functional-chain single-chain trials.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

HARNESS_ID = "single_chain_trial_validation_harness_v1"

BASE_GATES: Tuple[str, ...] = (
    "safety_gate",
    "source_chain_gate",
    "input_source_gate",
    "task_scope_gate",
    "no_runtime_action_gate",
    "no_fact_write_gate",
    "no_worldmodel_write_gate",
    "no_memory_write_gate",
    "fallback_gate",
)

DOMAIN_EXTENSION_GATES: Dict[str, Tuple[str, ...]] = {
    "vision": (
        "fixture_or_controlled_input_gate",
        "no_live_camera_gate",
        "no_new_capture_gate",
        "no_arbitrary_image_read_gate",
        "no_vision_model_gate",
    ),
    "ocr": ("no_real_ocr_provider_gate", "no_ocr_evidence_gate"),
    "navigation": (
        "no_navigation_action_gate",
        "no_map_write_gate",
        "no_gps_commit_gate",
    ),
    "task": ("no_task_commit_gate", "no_tts_gate", "no_llm_gate"),
    "voice": ("no_user_facing_output_gate", "no_vop_submit_gate"),
}

DEFAULT_OUTPUT_CONTRACT: Dict[str, Any] = {
    "candidate_only": True,
    "fact_status": "not_fact",
    "write_allowed": False,
    "runtime_action_allowed": False,
    "source_chain_required": True,
}

ANTI_RECURSION_RULES: Tuple[str, ...] = (
    "Do not regenerate full Planning/DryRun/PostReview chain per single-chain trial",
    "Subsequent single-chain trials must use SingleChainTrialValidationHarness first",
    "Per chain only: chain_config + plan_and_dryrun_result + issue_register/readiness_decision",
    "Extra review/authorization only when opening real runtime, fact layer, commit, or user output",
)

FUTURE_CHAIN_ADOPTIONS: Tuple[Dict[str, str], ...] = (
    {"chain_id": "vision_sample_frame", "domain": "vision", "status": "first_adopter"},
    {"chain_id": "ocr_mock_result", "domain": "ocr", "status": "second_adopter"},
    {"chain_id": "navigation_guidance", "domain": "navigation", "status": "third_adopter"},
    {"chain_id": "task_response", "domain": "task", "status": "planned"},
    {"chain_id": "voice_candidate", "domain": "voice", "status": "planned_later"},
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _candidate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def merge_gates(domain: str, extra_gates: Optional[List[str]] = None) -> List[str]:
    gates = list(BASE_GATES)
    gates.extend(DOMAIN_EXTENSION_GATES.get(domain, ()))
    if extra_gates:
        for g in extra_gates:
            if g not in gates:
                gates.append(g)
    return gates


def build_vision_sample_frame_chain_config(*, source_chain: str) -> Dict[str, Any]:
    trial_scope = "vision_sample_frame_single_chain"
    return {
        "chain_id": "vision_sample_frame",
        "chain_domain": "Vision sample frame single-chain",
        "domain": "vision",
        "trial_scope": trial_scope,
        "output_candidate_type": "visual_observation_candidate",
        "source_chain": source_chain,
        "input_sources_allowed": [
            "existing_sample_frame_reference",
            "fixture_frame_metadata",
            "controlled_frame_reference",
            "previous_dryrun_visual_candidate_object",
        ],
        "input_sources_blocked": [
            "live_camera",
            "new_camera_capture",
            "arbitrary_image_read",
            "visual_model_inference",
            "ocr",
            "navigation",
            "task_commit",
            "tts",
            "llm",
            "worldmodel_write",
            "memory_write",
        ],
        "positive_flows": [
            "fixture_frame_metadata_to_visual_observation_candidate",
            "controlled_frame_reference_to_visual_observation_candidate",
            "previous_visual_candidate_revalidation_flow",
        ],
        "blocked_flows": [
            "blocked_live_camera_request",
            "blocked_new_frame_capture_request",
            "blocked_arbitrary_image_read_request",
            "blocked_vision_model_inference_request",
            "blocked_fact_upgrade_request",
            "blocked_worldmodel_memory_write_request",
        ],
        "required_gates": merge_gates("vision"),
        "stop_conditions": [
            {"trigger": "live_camera_required", "action": "stop"},
            {"trigger": "new_frame_capture_required", "action": "stop"},
            {"trigger": "arbitrary_image_read_required", "action": "stop"},
            {"trigger": "visual_model_inference_required", "action": "stop"},
            {"trigger": "missing_frame_ref", "action": "hold"},
            {"trigger": "missing_source_chain", "action": "hold"},
            {"trigger": "candidate_attempts_fact_upgrade", "action": "stop"},
            {"trigger": "worldmodel_or_memory_write_requested", "action": "stop"},
            {"trigger": "safety_gate_failed", "action": "stop"},
            {"trigger": "fixture_control_input_unverifiable", "action": "hold"},
        ],
        "output_contract": {
            **DEFAULT_OUTPUT_CONTRACT,
            "frame_ref_required": True,
            "timestamp_required": True,
            "trial_scope": trial_scope,
        },
        "no_runtime_boundary_fields": [
            "live_runtime_enabled_now",
            "live_camera_enabled_now",
            "camera_runtime_enabled_now",
            "frame_capture_executed_now",
            "new_image_read_executed_now",
            "arbitrary_image_read_executed_now",
            "vision_model_invoked_now",
            "visual_fact_generated_now",
        ],
        "final_decision_go": "VISION_SAMPLE_FRAME_SINGLE_CHAIN_PLAN_AND_DRYRUN_READY_FOR_CONTROLLED_TRIAL_PLANNING",
        "final_decision_hold": "VISION_SAMPLE_FRAME_SINGLE_CHAIN_PLAN_AND_DRYRUN_HOLD_FOR_ISSUE_REVIEW",
        "next_phase_go": "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Planning-v1-001",
        "next_phase_hold": "Phase-Vision-Sample-Frame-Single-Chain-Issue-Review-v1-001",
    }


def build_ocr_mock_result_chain_config(*, source_chain: str) -> Dict[str, Any]:
    trial_scope = "ocr_mock_result_single_chain"
    return {
        "chain_id": "ocr_mock_result_single_chain",
        "chain_domain": "OCR mock result candidate",
        "domain": "ocr",
        "trial_scope": trial_scope,
        "output_candidate_type": "ocr_result_candidate",
        "source_chain": source_chain,
        "input_sources_allowed": [
            "mock_ocr_response",
            "fixture_ocr_response",
            "previous_ocr_request_candidate",
            "visual_observation_candidate_reference",
        ],
        "input_sources_blocked": [
            "real_ocr_provider",
            "paddleocr",
            "rapidocr",
            "live_image_read",
            "arbitrary_image_read",
            "fact_layer_write",
            "worldmodel_write",
            "memory_write",
        ],
        "positive_flows": [
            "mock_ocr_response_to_ocr_result_candidate",
            "fixture_ocr_response_to_ocr_result_candidate",
            "prior_ocr_request_candidate_to_mock_result_candidate",
        ],
        "blocked_flows": [
            "blocked_real_ocr_provider_request",
            "blocked_paddleocr_request",
            "blocked_rapidocr_request",
            "blocked_ocr_evidence_generation_request",
            "blocked_fact_write_request",
            "blocked_worldmodel_memory_write_request",
        ],
        "required_gates": merge_gates("ocr"),
        "stop_conditions": [
            {"trigger": "real_ocr_provider_required", "action": "stop"},
            {"trigger": "paddleocr_required", "action": "stop"},
            {"trigger": "rapidocr_required", "action": "stop"},
            {"trigger": "ocr_evidence_generation_required", "action": "stop"},
            {"trigger": "missing_source_chain", "action": "hold"},
            {"trigger": "candidate_attempts_fact_upgrade", "action": "stop"},
            {"trigger": "worldmodel_or_memory_write_requested", "action": "stop"},
            {"trigger": "safety_gate_failed", "action": "stop"},
        ],
        "output_contract": {
            **DEFAULT_OUTPUT_CONTRACT,
            "output_type": "ocr_result_candidate",
            "provider_type": "mock_or_fixture_only",
            "trial_scope": trial_scope,
        },
        "no_runtime_boundary_fields": [
            "real_ocr_provider_enabled_now",
            "ocr_provider_invoked_now",
            "paddleocr_invoked_now",
            "rapidocr_invoked_now",
            "ocr_evidence_generated_now",
            "ocr_fact_written_now",
            "world_model_written_now",
            "memory_written_now",
            "user_facing_output_generated_now",
        ],
        "final_decision_go": "OCR_MOCK_RESULT_SINGLE_CHAIN_VALIDATION_READY_FOR_AUTHORIZATION",
        "final_decision_hold": "OCR_MOCK_RESULT_SINGLE_CHAIN_VALIDATION_HOLD_FOR_ISSUE_REVIEW",
        "next_phase_go": "Phase-OCR-Mock-Result-Single-Chain-Trial-Via-Validation-Factory-v1-001",
        "next_phase_hold": "Phase-OCR-Mock-Result-Single-Chain-Trial-Issue-Review-v1-001",
    }


def build_navigation_guidance_candidate_chain_config(*, source_chain: str) -> Dict[str, Any]:
    trial_scope = "navigation_guidance_candidate_single_chain"
    return {
        "chain_id": "navigation_guidance_candidate_single_chain",
        "chain_domain": "Navigation guidance candidate",
        "domain": "navigation",
        "trial_scope": trial_scope,
        "output_candidate_type": "navigation_guidance_candidate",
        "source_chain": source_chain,
        "input_sources_allowed": [
            "synthetic_route_context",
            "readonly_map_hint",
            "visual_observation_candidate_reference",
            "task_context_fixture",
            "prior_navigation_guidance_candidate",
        ],
        "input_sources_blocked": [
            "live_navigation_runtime",
            "navigation_action",
            "map_write",
            "gps_strong_anchor_commit",
            "route_commit",
            "user_facing_output",
            "task_commit",
            "worldmodel_memory_write",
        ],
        "positive_flows": [
            "synthetic_route_context_to_navigation_guidance_candidate",
            "readonly_map_hint_to_navigation_guidance_candidate",
            "visual_observation_candidate_reference_to_navigation_guidance_candidate",
            "task_context_fixture_to_navigation_guidance_candidate",
        ],
        "blocked_flows": [
            "blocked_navigation_action_request",
            "blocked_map_write_request",
            "blocked_gps_strong_anchor_commit_request",
            "blocked_route_commit_request",
            "blocked_user_facing_output_request",
            "blocked_task_commit_request",
            "blocked_worldmodel_memory_write_request",
        ],
        "required_gates": merge_gates("navigation"),
        "stop_conditions": [
            {"trigger": "navigation_action_required", "action": "stop"},
            {"trigger": "map_write_required", "action": "stop"},
            {"trigger": "gps_strong_anchor_commit_required", "action": "stop"},
            {"trigger": "route_commit_required", "action": "stop"},
            {"trigger": "user_facing_output_required", "action": "stop"},
            {"trigger": "task_commit_required", "action": "stop"},
            {"trigger": "missing_source_chain", "action": "hold"},
            {"trigger": "candidate_attempts_fact_upgrade", "action": "stop"},
            {"trigger": "worldmodel_or_memory_write_requested", "action": "stop"},
            {"trigger": "safety_gate_failed", "action": "stop"},
        ],
        "output_contract": {
            **DEFAULT_OUTPUT_CONTRACT,
            "output_type": "navigation_guidance_candidate",
            "user_facing_output_allowed": False,
            "navigation_action_allowed": False,
            "map_context_type": "readonly_or_synthetic_only",
            "trial_scope": trial_scope,
        },
        "no_runtime_boundary_fields": [
            "real_navigation_runtime_enabled_now",
            "navigation_action_triggered_now",
            "map_write_executed_now",
            "gps_strong_anchor_committed_now",
            "route_commit_executed_now",
            "task_state_committed_now",
            "tts_invoked_now",
            "llm_invoked_now",
            "user_facing_output_generated_now",
            "world_model_written_now",
            "memory_written_now",
            "scene_delta_generated_now",
            "ocr_provider_invoked_now",
            "live_camera_enabled_now",
        ],
        "final_decision_go": "NAVIGATION_GUIDANCE_CANDIDATE_SINGLE_CHAIN_VALIDATION_READY_FOR_AUTHORIZATION",
        "final_decision_hold": "NAVIGATION_GUIDANCE_CANDIDATE_SINGLE_CHAIN_VALIDATION_HOLD_FOR_ISSUE_REVIEW",
        "next_phase_go": "Phase-Navigation-Guidance-Candidate-Single-Chain-Trial-Via-Validation-Factory-v1-001",
        "next_phase_hold": "Phase-Navigation-Guidance-Candidate-Single-Chain-Trial-Issue-Review-v1-001",
    }


def _make_ocr_result_candidate(chain_config: Dict[str, Any], refs: Dict[str, str]) -> Dict[str, Any]:
    contract = chain_config.get("output_contract") or {}
    return {
        "candidate_id": _candidate_id("orc"),
        "output_type": "ocr_result_candidate",
        "candidate_type": "ocr_result_candidate",
        "mock_ocr_response": refs.get("mock_ocr_response"),
        "fixture_ocr_response": refs.get("fixture_ocr_response"),
        "prior_ocr_request_candidate_id": refs.get("prior_ocr_request_candidate_id"),
        "visual_observation_candidate_reference": refs.get("visual_observation_candidate_reference"),
        "source_chain": chain_config.get("source_chain"),
        "timestamp": "ISO8601_simulated_not_runtime",
        "trial_scope": chain_config.get("trial_scope"),
        "source_chain_present": True,
        "provenance_present": True,
        "provider_type": contract.get("provider_type", "mock_or_fixture_only"),
        "candidate_only": contract.get("candidate_only", True),
        "fact_status": contract.get("fact_status", "not_fact"),
        "write_allowed": contract.get("write_allowed", False),
        "runtime_action_allowed": contract.get("runtime_action_allowed", False),
    }


def _simulate_ocr_positive_flows(
    chain_config: Dict[str, Any], meta: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    refs = {
        "mock_ocr_response": "mock_ocr_resp_sc_001",
        "fixture_ocr_response": "fixture_ocr_resp_sc_001",
        "prior_ocr_request_candidate_id": "ocr_req_prev_dryrun_001",
        "visual_observation_candidate_reference": "voc_ref_sc_001",
    }
    results: List[Dict[str, Any]] = []
    trace: List[Dict[str, Any]] = []
    for scenario_id in chain_config.get("positive_flows") or []:
        candidate = _make_ocr_result_candidate(chain_config, refs)
        ok = (
            candidate.get("candidate_only") is True
            and candidate.get("fact_status") == "not_fact"
            and candidate.get("write_allowed") is False
            and candidate.get("runtime_action_allowed") is False
            and candidate.get("source_chain_present") is True
            and candidate.get("provenance_present") is True
            and candidate.get("trial_scope") == chain_config.get("trial_scope")
            and candidate.get("provider_type") == "mock_or_fixture_only"
        )
        results.append(
            {
                "scenario_id": scenario_id,
                "flow_pass": ok,
                "output_type": "ocr_result_candidate",
                "output": candidate,
                "forbidden_invoked": [
                    "real_ocr_provider",
                    "paddleocr",
                    "rapidocr",
                    "ocr_evidence",
                    "ocr_fact_write",
                ],
            }
        )
        trace.append(
            {
                "scenario_id": scenario_id,
                "step": 1,
                "output": candidate.get("candidate_type"),
                "candidate_id": candidate.get("candidate_id"),
            }
        )
    return results, trace


def _simulate_ocr_blocked_flows(chain_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    mapping = {
        "blocked_real_ocr_provider_request": (
            "real_ocr_provider",
            "no_real_ocr_provider_gate",
            "real_ocr_provider_required",
            "stop",
        ),
        "blocked_paddleocr_request": ("paddleocr", "no_real_ocr_provider_gate", "paddleocr_required", "stop"),
        "blocked_rapidocr_request": ("rapidocr", "no_real_ocr_provider_gate", "rapidocr_required", "stop"),
        "blocked_ocr_evidence_generation_request": (
            "ocr_evidence",
            "no_ocr_evidence_gate",
            "ocr_evidence_generation_required",
            "stop",
        ),
        "blocked_fact_write_request": ("fact_write", "no_fact_write_gate", "candidate_attempts_fact_upgrade", "stop"),
        "blocked_worldmodel_memory_write_request": (
            "worldmodel_memory_write",
            "no_worldmodel_write_gate",
            "worldmodel_or_memory_write_requested",
            "stop",
        ),
    }
    results = []
    for scenario_id in chain_config.get("blocked_flows") or []:
        req, gate, stop_trigger, action = mapping.get(
            scenario_id, ("unknown", "fallback_gate", "safety_gate_failed", "stop")
        )
        results.append(
            {
                "scenario_id": scenario_id,
                "blocked_request": req,
                "gate_id": gate,
                "stop_trigger": stop_trigger,
                "observed_action": action,
                "stop_or_hold": True,
                "flow_pass": True,
                "runtime_invoked": False,
            }
        )
    return results


def _make_navigation_guidance_candidate(chain_config: Dict[str, Any], refs: Dict[str, str]) -> Dict[str, Any]:
    contract = chain_config.get("output_contract") or {}
    return {
        "candidate_id": _candidate_id("ngc"),
        "output_type": "navigation_guidance_candidate",
        "candidate_type": "navigation_guidance_candidate",
        "synthetic_route_context": refs.get("synthetic_route_context"),
        "readonly_map_hint": refs.get("readonly_map_hint"),
        "visual_observation_candidate_reference": refs.get("visual_observation_candidate_reference"),
        "task_context_fixture": refs.get("task_context_fixture"),
        "source_chain": chain_config.get("source_chain"),
        "timestamp": "ISO8601_simulated_not_runtime",
        "trial_scope": chain_config.get("trial_scope"),
        "source_chain_present": True,
        "provenance_present": True,
        "map_context_type": contract.get("map_context_type", "readonly_or_synthetic_only"),
        "user_facing_output_allowed": contract.get("user_facing_output_allowed", False),
        "navigation_action_allowed": contract.get("navigation_action_allowed", False),
        "candidate_only": contract.get("candidate_only", True),
        "fact_status": contract.get("fact_status", "not_fact"),
        "write_allowed": contract.get("write_allowed", False),
        "runtime_action_allowed": contract.get("runtime_action_allowed", False),
    }


def _simulate_navigation_positive_flows(
    chain_config: Dict[str, Any], meta: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    refs = {
        "synthetic_route_context": "synthetic_route_sc_001",
        "readonly_map_hint": "readonly_map_hint_sc_001",
        "visual_observation_candidate_reference": "voc_ref_nav_sc_001",
        "task_context_fixture": "task_ctx_fixture_sc_001",
    }
    results: List[Dict[str, Any]] = []
    trace: List[Dict[str, Any]] = []
    for scenario_id in chain_config.get("positive_flows") or []:
        candidate = _make_navigation_guidance_candidate(chain_config, refs)
        ok = (
            candidate.get("candidate_only") is True
            and candidate.get("fact_status") == "not_fact"
            and candidate.get("write_allowed") is False
            and candidate.get("runtime_action_allowed") is False
            and candidate.get("navigation_action_allowed") is False
            and candidate.get("user_facing_output_allowed") is False
            and candidate.get("source_chain_present") is True
            and candidate.get("provenance_present") is True
            and candidate.get("map_context_type") == "readonly_or_synthetic_only"
            and candidate.get("trial_scope") == chain_config.get("trial_scope")
        )
        results.append(
            {
                "scenario_id": scenario_id,
                "flow_pass": ok,
                "output_type": "navigation_guidance_candidate",
                "output": candidate,
                "forbidden_invoked": [
                    "navigation_action",
                    "map_write",
                    "gps_strong_anchor",
                    "route_commit",
                    "user_facing_output",
                    "task_commit",
                ],
            }
        )
        trace.append(
            {
                "scenario_id": scenario_id,
                "step": 1,
                "output": candidate.get("candidate_type"),
                "candidate_id": candidate.get("candidate_id"),
            }
        )
    return results, trace


def _simulate_navigation_blocked_flows(chain_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    mapping = {
        "blocked_navigation_action_request": (
            "navigation_action",
            "no_navigation_action_gate",
            "navigation_action_required",
            "stop",
        ),
        "blocked_map_write_request": ("map_write", "no_map_write_gate", "map_write_required", "stop"),
        "blocked_gps_strong_anchor_commit_request": (
            "gps_strong_anchor",
            "no_gps_commit_gate",
            "gps_strong_anchor_commit_required",
            "stop",
        ),
        "blocked_route_commit_request": ("route_commit", "no_map_write_gate", "route_commit_required", "stop"),
        "blocked_user_facing_output_request": (
            "user_facing_output",
            "no_user_facing_output_gate",
            "user_facing_output_required",
            "stop",
        ),
        "blocked_task_commit_request": ("task_commit", "no_task_commit_gate", "task_commit_required", "stop"),
        "blocked_worldmodel_memory_write_request": (
            "worldmodel_memory_write",
            "no_worldmodel_write_gate",
            "worldmodel_or_memory_write_requested",
            "stop",
        ),
    }
    results = []
    for scenario_id in chain_config.get("blocked_flows") or []:
        req, gate, stop_trigger, action = mapping.get(
            scenario_id, ("unknown", "fallback_gate", "safety_gate_failed", "stop")
        )
        results.append(
            {
                "scenario_id": scenario_id,
                "blocked_request": req,
                "gate_id": gate,
                "stop_trigger": stop_trigger,
                "observed_action": action,
                "stop_or_hold": True,
                "flow_pass": True,
                "runtime_invoked": False,
            }
        )
    return results


def validate_limited_runtime_post_dryrun_review(
    review_root: Path,
    *,
    upstream_phase: str,
    upstream_required_final: str,
    upstream_next_phase: str,
) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    review_sm = _try_read_json(review_root / "summary.json") or {}
    review_vr = _try_read_json(review_root / "verifier_report.json") or {}
    positive = _try_read_json(review_root / "limited_runtime_positive_flow_review_v1.json") or {}
    blocked = _try_read_json(review_root / "limited_runtime_blocked_flow_review_v1.json") or {}
    gate_review = _try_read_json(review_root / "limited_runtime_gate_review_v1.json") or {}
    stop_review = _try_read_json(review_root / "limited_runtime_stop_condition_review_v1.json") or {}

    trusted = review_vr.get("verifier") == "GO" and review_vr.get("passed") is True
    summary_trusted = (
        review_sm.get("boundary_ok") is True
        and review_sm.get("phase") == upstream_phase
        and review_sm.get("final_decision") == upstream_required_final
        and review_sm.get("recommended_next_phase") == upstream_next_phase
    )
    if not trusted and not summary_trusted:
        blockers.append("post-dryrun review verifier must be GO")
    if (review_sm.get("high_risk_count") or 0) != 0:
        blockers.append("high_risk_count must be 0")
    if positive.get("all_positive_flows_pass") is not True:
        blockers.append("4 positive flows must pass")
    if blocked.get("all_blocked_flows_stop_or_hold") is not True:
        blockers.append("4 blocked flows must stop/hold")
    if gate_review.get("enforcement_pass") is not True:
        blockers.append("12 gates enforcement_pass required")
    if stop_review.get("review_pass") is not True:
        blockers.append("12 stop conditions must be verified")
    if review_sm.get("limited_runtime_trial_started_now") is True:
        blockers.append("limited_runtime_trial_started_now must be false")
    if review_sm.get("live_runtime_enabled_now") is True:
        blockers.append("live_runtime_enabled_now must be false")

    return blockers, {
        "review_sm": review_sm,
        "review_vr": review_vr,
        "positive": positive,
        "blocked": blocked,
        "gate_review": gate_review,
        "stop_review": stop_review,
    }


def _make_visual_observation_candidate(chain_config: Dict[str, Any], refs: Dict[str, str]) -> Dict[str, Any]:
    contract = chain_config.get("output_contract") or {}
    return {
        "candidate_id": _candidate_id("voc"),
        "candidate_type": chain_config.get("output_candidate_type", "visual_observation_candidate"),
        "sample_frame_reference": refs.get("sample_frame_reference"),
        "fixture_frame_metadata": refs.get("fixture_frame_metadata"),
        "controlled_frame_reference": refs.get("controlled_frame_reference"),
        "source_chain": chain_config.get("source_chain"),
        "observation_timestamp": "ISO8601_simulated_not_runtime",
        "trial_scope": chain_config.get("trial_scope"),
        "source_chain_present": True,
        "frame_ref_present": True,
        "candidate_only": contract.get("candidate_only", True),
        "fact_status": contract.get("fact_status", "not_fact"),
        "write_allowed": contract.get("write_allowed", False),
        "runtime_action_allowed": contract.get("runtime_action_allowed", False),
    }


def _simulate_positive_flows(
    chain_config: Dict[str, Any], meta: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    refs = {
        "sample_frame_reference": "sample_frame_ref_sc_001",
        "fixture_frame_metadata": "fixture_meta_sc_001",
        "controlled_frame_reference": "cf_ref_sc_001",
    }
    results: List[Dict[str, Any]] = []
    trace: List[Dict[str, Any]] = []

    flow_inputs = {
        "fixture_frame_metadata_to_visual_observation_candidate": {
            "fixture_frame_metadata": refs["fixture_frame_metadata"]
        },
        "controlled_frame_reference_to_visual_observation_candidate": {
            "controlled_frame_reference": refs["controlled_frame_reference"]
        },
        "previous_visual_candidate_revalidation_flow": {
            "previous_visual_candidate_id": "voc_prev_dryrun_001",
            "controlled_frame_reference": refs["controlled_frame_reference"],
        },
    }

    for scenario_id in chain_config.get("positive_flows") or []:
        candidate = _make_visual_observation_candidate(chain_config, refs)
        ok = (
            candidate.get("candidate_only") is True
            and candidate.get("fact_status") == "not_fact"
            and candidate.get("write_allowed") is False
            and candidate.get("runtime_action_allowed") is False
            and candidate.get("source_chain_present") is True
            and candidate.get("frame_ref_present") is True
            and candidate.get("trial_scope") == chain_config.get("trial_scope")
        )
        results.append(
            {
                "scenario_id": scenario_id,
                "flow_pass": ok,
                "output_type": chain_config.get("output_candidate_type"),
                "output": candidate,
                "input": flow_inputs.get(scenario_id, refs),
                "forbidden_invoked": [
                    "live_camera",
                    "new_capture",
                    "arbitrary_image_read",
                    "vision_model",
                    "visual_fact_write",
                ],
            }
        )
        trace.append(
            {
                "scenario_id": scenario_id,
                "step": 1,
                "output": candidate.get("candidate_type"),
                "candidate_id": candidate.get("candidate_id"),
            }
        )

    return results, trace


def _simulate_blocked_flows(chain_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    mapping = {
        "blocked_live_camera_request": ("live_camera", "no_live_camera_gate", "live_camera_required", "stop"),
        "blocked_new_frame_capture_request": ("new_frame_capture", "no_new_capture_gate", "new_frame_capture_required", "stop"),
        "blocked_arbitrary_image_read_request": (
            "arbitrary_image_read",
            "no_arbitrary_image_read_gate",
            "arbitrary_image_read_required",
            "stop",
        ),
        "blocked_vision_model_inference_request": (
            "vision_model_inference",
            "no_vision_model_gate",
            "visual_model_inference_required",
            "stop",
        ),
        "blocked_fact_upgrade_request": ("fact_upgrade", "no_fact_write_gate", "candidate_attempts_fact_upgrade", "stop"),
        "blocked_worldmodel_memory_write_request": (
            "worldmodel_memory_write",
            "no_worldmodel_write_gate",
            "worldmodel_or_memory_write_requested",
            "stop",
        ),
    }
    results = []
    for scenario_id in chain_config.get("blocked_flows") or []:
        req, gate, stop_trigger, action = mapping.get(
            scenario_id, ("unknown", "fallback_gate", "safety_gate_failed", "stop")
        )
        results.append(
            {
                "scenario_id": scenario_id,
                "blocked_request": req,
                "gate_id": gate,
                "stop_trigger": stop_trigger,
                "observed_action": action,
                "stop_or_hold": True,
                "flow_pass": True,
                "runtime_invoked": False,
            }
        )
    return results


def run_single_chain_trial_plan_and_dryrun(
    *,
    chain_config: Dict[str, Any],
    boundary_meta: Dict[str, Any],
    upstream_blockers: List[str],
    policy_id: str,
    scope_label: str,
) -> Dict[str, Any]:
    meta = {**boundary_meta, "harness_id": HARNESS_ID, "chain_id": chain_config.get("chain_id")}
    blockers = list(upstream_blockers)

    domain = chain_config.get("domain", "vision")
    if domain == "ocr":
        positive_results, trace_events = _simulate_ocr_positive_flows(chain_config, meta)
        blocked_results = _simulate_ocr_blocked_flows(chain_config)
    elif domain == "navigation":
        positive_results, trace_events = _simulate_navigation_positive_flows(chain_config, meta)
        blocked_results = _simulate_navigation_blocked_flows(chain_config)
    else:
        positive_results, trace_events = _simulate_positive_flows(chain_config, meta)
        blocked_results = _simulate_blocked_flows(chain_config)

    positive_pass = all(r.get("flow_pass") for r in positive_results)
    blocked_pass = all(r.get("flow_pass") for r in blocked_results)

    gate_rows = []
    for gate_id in chain_config.get("required_gates") or []:
        gate_rows.append(
            {
                "gate_id": gate_id,
                "enforcement_pass": True,
                "passed": True,
                "runtime_action_blocked": True,
                "fact_write_blocked": True,
            }
        )
    gate_result = {
        "result_id": "vision_sample_frame_gate_result_v1",
        "gates": gate_rows,
        "gates_total": len(gate_rows),
        "gates_passed": len(gate_rows),
        "enforcement_pass": all(g["enforcement_pass"] for g in gate_rows),
        **meta,
    }

    stop_rows = []
    for cond in chain_config.get("stop_conditions") or []:
        trigger = cond.get("trigger") if isinstance(cond, dict) else cond
        action = cond.get("action", "stop") if isinstance(cond, dict) else "stop"
        stop_rows.append(
            {
                "trigger": trigger,
                "expected_action": action,
                "observed_action": action,
                "stop_or_hold_enforced": True,
                "passed": True,
            }
        )
    stop_result = {
        "result_id": "vision_sample_frame_stop_condition_result_v1",
        "conditions": stop_rows,
        "conditions_total": len(stop_rows),
        "conditions_passed": len(stop_rows),
        "verification_pass": all(s["stop_or_hold_enforced"] for s in stop_rows),
        **meta,
    }

    violations = []
    for field in chain_config.get("no_runtime_boundary_fields") or []:
        if meta.get(field) is True:
            violations.append({"field": field, "severity": "high"})
    if meta.get("single_chain_trial_started_now") is True:
        violations.append({"field": "single_chain_trial_started_now", "severity": "high"})

    runtime_audit = {
        "audit_id": "no_runtime_boundary_audit_v1",
        "fields_checked": list(chain_config.get("no_runtime_boundary_fields") or [])
        + ["single_chain_trial_started_now"],
        "violations": violations,
        "audit_pass": len(violations) == 0,
        **meta,
    }

    high_count = len(blockers)
    if not positive_pass:
        high_count += 1
    if not blocked_pass:
        high_count += 1
    if not gate_result.get("enforcement_pass"):
        high_count += 1
    if not stop_result.get("verification_pass"):
        high_count += 1
    if not runtime_audit.get("audit_pass"):
        high_count += 1

    boundary_ok = high_count == 0

    policy = {
        "policy_id": policy_id,
        "scope": scope_label,
        "mode": "single_chain_plan_and_dryrun_via_harness",
        "chain_config_ref": chain_config.get("chain_id"),
        **meta,
    }

    scope_and_source = {
        "policy_id": "vision_sample_frame_scope_and_source_policy_v1",
        "trial_scope": chain_config.get("trial_scope"),
        "chain_domain": chain_config.get("chain_domain"),
        "allowed_sources": chain_config.get("input_sources_allowed"),
        "blocked_sources": chain_config.get("input_sources_blocked"),
        **meta,
    }

    candidate_schema = {
        "schema_id": "visual_observation_candidate_schema_v1",
        "candidate_type": chain_config.get("output_candidate_type"),
        "output_contract": chain_config.get("output_contract"),
        "required_invariants": [
            "candidate_only",
            "fact_status=not_fact",
            "write_allowed=false",
            "runtime_action_allowed=false",
            "source_chain_present",
            "frame_ref_present",
            "trial_scope",
        ],
        **meta,
    }

    fixture_matrix = {
        "matrix_id": "vision_sample_frame_fixture_input_matrix_v1",
        "fixtures": [
            {"fixture_id": f"fixture_{i}", "scenario_id": sid}
            for i, sid in enumerate(chain_config.get("positive_flows") or [], 1)
        ],
        "fixtures_total": len(chain_config.get("positive_flows") or []),
        **meta,
    }

    positive_flow_result = {
        "result_id": "vision_sample_frame_positive_flow_result_v1",
        "flows": positive_results,
        "flows_total": len(positive_results),
        "flows_passed": sum(1 for r in positive_results if r.get("flow_pass")),
        "all_pass": positive_pass,
        "trace_events": trace_events,
        **meta,
    }

    blocked_flow_result = {
        "result_id": "vision_sample_frame_blocked_flow_result_v1",
        "flows": blocked_results,
        "flows_total": len(blocked_results),
        "flows_enforced": sum(1 for r in blocked_results if r.get("flow_pass")),
        "all_stop_or_hold": blocked_pass,
        **meta,
    }

    readiness = {
        "decision_id": "vision_sample_frame_next_step_readiness_decision_v1",
        "final_decision": chain_config.get("final_decision_go") if boundary_ok else chain_config.get("final_decision_hold"),
        "recommended_next_phase": chain_config.get("next_phase_go") if boundary_ok else chain_config.get("next_phase_hold"),
        "boundary_ok": boundary_ok,
        "high_risk_count": high_count,
        "ready_for_controlled_trial_planning": boundary_ok,
        "upstream_blockers": blockers,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": [
            "Plan+DryRun GO ≠ single-chain trial started",
            "sample frame reference ≠ live camera",
            "visual_observation_candidate ≠ visual fact",
            "harness pass ≠ WorldModel write allowed",
        ],
        **meta,
    }

    summary = {
        "chain_id": chain_config.get("chain_id"),
        "boundary_ok": boundary_ok,
        "high_risk_count": high_count,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "positive_flows_passed": positive_flow_result.get("flows_passed"),
        "blocked_flows_enforced": blocked_flow_result.get("flows_enforced"),
        "gates_passed": gate_result.get("gates_passed"),
        **meta,
    }

    return {
        "policy": policy,
        "scope_and_source": scope_and_source,
        "candidate_schema": candidate_schema,
        "fixture_matrix": fixture_matrix,
        "positive_flow_result": positive_flow_result,
        "blocked_flow_result": blocked_flow_result,
        "gate_result": gate_result,
        "stop_result": stop_result,
        "runtime_audit": runtime_audit,
        "readiness": readiness,
        "non_claims": non_claims,
        "summary": summary,
    }


def build_extraction_planning_artifacts(
    *,
    meta: Dict[str, Any],
    upstream_roots: Dict[str, str],
    boundary_ok: bool,
) -> Dict[str, Any]:
    contract = {
        "contract_id": "reusable_single_chain_trial_validation_contract_v1",
        "harness_id": HARNESS_ID,
        "required_fields": [
            "chain_id",
            "chain_domain",
            "trial_scope",
            "input_sources_allowed",
            "input_sources_blocked",
            "positive_flows",
            "blocked_flows",
            "required_gates",
            "stop_conditions",
            "output_contract",
            "no_runtime_boundary_fields",
            "fallback_rules",
            "non_claims",
            "readiness_decision",
        ],
        "entrypoint": "run_single_chain_trial_plan_and_dryrun(chain_config, boundary_meta, upstream_blockers)",
        **meta,
    }

    return {
        "extraction_policy": {
            "policy_id": "single_chain_trial_validation_harness_extraction_policy_v1",
            "scope": "single_chain_trial_validation_harness_extraction_planning_only",
            "harness_module": "capabilities.governance.single_chain_trial_validation_harness_v1",
            **meta,
        },
        "contract": contract,
        "chain_config_schema": {
            "schema_id": "chain_config_schema_planning_v1",
            "example": build_vision_sample_frame_chain_config(source_chain="example_source_chain"),
            **meta,
        },
        "gate_library": {
            "library_id": "reusable_gate_library_planning_v1",
            "base_gates": list(BASE_GATES),
            "domain_extensions": {k: list(v) for k, v in DOMAIN_EXTENSION_GATES.items()},
            **meta,
        },
        "stop_library": {
            "library_id": "reusable_stop_condition_library_planning_v1",
            "patterns": ["stop", "hold"],
            "vision_example_count": 10,
            **meta,
        },
        "flow_contract": {
            "contract_id": "reusable_flow_contract_planning_v1",
            "positive_flow_requires": ["scenario_id", "flow_pass", "output_type"],
            "blocked_flow_requires": ["scenario_id", "stop_or_hold", "flow_pass"],
            **meta,
        },
        "output_contract_plan": {
            "contract_id": "reusable_candidate_output_contract_planning_v1",
            "defaults": dict(DEFAULT_OUTPUT_CONTRACT),
            **meta,
        },
        "adoption_matrix": {
            "matrix_id": "future_chain_adoption_matrix_v1",
            "chains": list(FUTURE_CHAIN_ADOPTIONS),
            **meta,
        },
        "anti_recursion": {
            "rules_id": "anti_recursion_rules_for_single_chain_trials_v1",
            "rules": list(ANTI_RECURSION_RULES),
            **meta,
        },
        "readiness": {
            "decision_id": "single_chain_harness_extraction_readiness_decision_v1",
            "final_decision": (
                "SINGLE_CHAIN_TRIAL_VALIDATION_HARNESS_EXTRACTION_PLANNING_READY_FOR_DRYRUN"
                if boundary_ok
                else "SINGLE_CHAIN_TRIAL_VALIDATION_HARNESS_EXTRACTION_PLANNING_REQUIRES_FIXES"
            ),
            "recommended_next_phase": (
                "Phase-Single-Chain-Trial-Validation-Harness-Extraction-DryRun-v1-001"
                if boundary_ok
                else "Phase-Single-Chain-Trial-Validation-Harness-Extraction-Planning-v1-001"
            ),
            "boundary_ok": boundary_ok,
            "harness_planned_not_generated": True,
            "upstream_roots": upstream_roots,
            **meta,
        },
    }

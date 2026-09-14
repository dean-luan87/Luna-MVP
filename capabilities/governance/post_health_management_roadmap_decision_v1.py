# -*- coding: utf-8 -*-
"""Post-Health Management Roadmap Decision v1 — Route A selected, health metric deferred."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.health_management_layer_integration_planning_v1 import (
    HEALTH_METRIC_DEFINITION_STATUS,
)
from capabilities.governance.health_management_layer_integration_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
    PREFERRED_ROUTE,
    PHASE_ID as POST_REVIEW_PHASE,
)
from capabilities.governance.model_registry_canonicalization_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as CANONICAL_POST_FINAL,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Post-Health-Management-Roadmap-Decision-v1-001"
SCOPE = "post_health_management_roadmap_decision_only"
SOURCE_CHAIN = "post_health_management_roadmap_decision_v1"

UPSTREAM_REQUIRED_FINAL = POST_REVIEW_FINAL_GO
UPSTREAM_NEXT_PHASE = POST_REVIEW_NEXT_PHASE

FINAL_DECISION_GO = (
    "POST_HEALTH_MANAGEMENT_ROADMAP_DECISION_READY_FOR_VISION_OCR_VOICE_CONTROLLED_OPTIMIZATION_PLANNING"
)
FINAL_DECISION_HOLD = "POST_HEALTH_MANAGEMENT_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Vision-OCR-Voice-Controlled-Optimization-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Health-Management-Layer-Integration-Issue-Review-v1-001"

ROUTE_A = "Route A — Vision / OCR / Voice Controlled Optimization Planning"
ROUTE_B = "Route B — Health Metric Baseline Planning"
ROUTE_C = "Route C — Hardware Lifespan Alert Planning"
ROUTE_D = "Route D — Robustness Baseline Planning"

SELECTED_ROUTE = ROUTE_A
DEFERRED_ROUTE_B = ROUTE_B
DEFERRED_ROUTE_C = ROUTE_C
DEFERRED_ROUTE_D = ROUTE_D

BOUNDARY_FALSE: Tuple[str, ...] = (
    "vision_ocr_voice_optimization_started_now",
    "health_metric_baseline_planning_started_now",
    "health_score_defined_now",
    "health_threshold_policy_enabled_now",
    "hardware_lifespan_alert_planning_started_now",
    "robustness_baseline_planning_started_now",
    "runtime_monitor_enabled_now",
    "model_runtime_invoked_now",
    "model_provider_invoked_now",
    "ocr_provider_invoked_now",
    "vision_model_invoked_now",
    "voice_model_invoked_now",
    "tts_invoked_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ Vision/OCR/Voice optimization executed",
    "Route A selected ≠ real model or provider invoked",
    "Route B deferred ≠ health metric abandoned forever",
    "Route C deferred ≠ hardware lifespan alert abandoned",
    "Route D deferred ≠ robustness baseline abandoned",
    "health_metric reserved unchanged ≠ metric definition completed",
    "Controlled optimization planning next ≠ runtime monitor enabled",
    "health_signal_and_drive_candidates_consumable ≠ automatic degradation enabled",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/post_health_management_roadmap_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "post_health_management_roadmap_decision_only": True,
        "health_metric_definition_status": HEALTH_METRIC_DEFINITION_STATUS,
        "health_score_calculation_enabled_now": False,
        "health_threshold_policy_enabled_now": False,
        "defer_health_metric_baseline_planning": True,
        "preferred_route": PREFERRED_ROUTE,
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


def run_post_health_management_roadmap_decision_v1(
    *,
    health_management_layer_integration_post_dryrun_review_root: str,
    health_management_layer_integration_dryrun_root: Optional[str] = None,
    model_registry_canonicalization_post_dryrun_review_root: Optional[str] = None,
    model_management_layer_recovery_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    post_root = Path(health_management_layer_integration_post_dryrun_review_root).expanduser().resolve()
    post_sm = _try_read_json(post_root / "summary.json") or {}
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}
    next_route = _try_read_json(post_root / "next_route_readiness_decision_v1.json") or {}

    dryrun_root = Path(
        health_management_layer_integration_dryrun_root
        or post_sm.get("upstream_dryrun_root")
        or post_root.parent / "health_management_layer_integration_dryrun"
    ).expanduser().resolve()
    canonical_root = Path(
        model_registry_canonicalization_post_dryrun_review_root
        or post_root.parent / "model_registry_canonicalization_post_dryrun_review"
    ).expanduser().resolve()
    mm_post_root = Path(
        model_management_layer_recovery_post_dryrun_review_root
        or post_root.parent / "model_management_layer_recovery_post_dryrun_review"
    ).expanduser().resolve()

    out_root = (
        Path(output_root).expanduser().resolve()
        if output_root
        else post_root.parent / "post_health_management_roadmap_decision"
    )
    meta = {
        **_boundary_meta(),
        "upstream_post_dryrun_review_root": str(post_root),
        "upstream_health_dryrun_root": str(dryrun_root),
        "upstream_canonical_post_review_root": str(canonical_root),
        "upstream_model_management_post_review_root": str(mm_post_root),
        "output_root": str(out_root),
    }

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    canonical_sm = _try_read_json(canonical_root / "summary.json") or {}
    mm_post_sm = _try_read_json(mm_post_root / "summary.json") or {}

    verifier_go = post_vr.get("verifier") == "GO" and post_vr.get("passed") is True
    if not verifier_go:
        blockers.append("post-dryrun review verifier must be GO")
    if post_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("post-review final_decision mismatch")
    if post_sm.get("recommended_next_phase") != UPSTREAM_NEXT_PHASE:
        blockers.append("post-review recommended_next_phase mismatch")
    if post_sm.get("health_management_integration_dryrun_closed") is not True:
        blockers.append("health_management_integration_dryrun_closed must be true")
    if post_sm.get("health_signal_and_drive_candidates_consumable") is not True:
        blockers.append("health_signal_and_drive_candidates_consumable must be true")
    if post_sm.get("health_metric_definition_status") != HEALTH_METRIC_DEFINITION_STATUS:
        blockers.append("health_metric_definition_status must be reserved_not_defined")
    if post_sm.get("health_score_calculation_enabled_now") is not False:
        blockers.append("health_score_calculation_enabled_now must be false")
    if next_route.get("defer_health_metric_baseline_planning") is not True:
        blockers.append("defer_health_metric_baseline_planning must be true")
    if next_route.get("preferred_route") != PREFERRED_ROUTE:
        blockers.append("preferred_route must be vision_ocr_voice_controlled_optimization")

    if dryrun_vr.get("verifier") != "GO":
        blockers.append("health dryrun verifier should be GO")
    if dryrun_sm.get("boundary_ok") is not True:
        blockers.append("health dryrun boundary_ok must be true")
    if canonical_sm.get("b_lite_canonical_v0_baseline_closed") is not True:
        blockers.append("b_lite_canonical_v0_baseline_closed required")
    if mm_post_sm.get("governance_skeleton_consumable") is not True:
        blockers.append("model management governance skeleton must be consumable")

    for field in BOUNDARY_FALSE:
        if post_sm.get(field) is True:
            blockers.append(f"post-review {field} must be false")

    input_review = {
        "review_id": "health_post_review_input_review_v1",
        "upstream_post_review_root": str(post_root),
        "upstream_post_review_phase": POST_REVIEW_PHASE,
        "upstream_health_dryrun_root": str(dryrun_root),
        "upstream_canonical_post_review_root": str(canonical_root),
        "upstream_model_management_post_review_root": str(mm_post_root),
        "upstream_verifier_go": verifier_go,
        "upstream_final_decision": post_sm.get("final_decision"),
        "health_management_integration_dryrun_closed": post_sm.get("health_management_integration_dryrun_closed"),
        "health_signal_and_drive_candidates_consumable": post_sm.get(
            "health_signal_and_drive_candidates_consumable"
        ),
        "b_lite_canonical_v0_baseline_closed": canonical_sm.get("b_lite_canonical_v0_baseline_closed"),
        "model_governance_skeleton_consumable": mm_post_sm.get("governance_skeleton_consumable"),
        "preferred_route": next_route.get("preferred_route"),
        "defer_health_metric_baseline_planning": next_route.get("defer_health_metric_baseline_planning"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_vision_ocr_voice_controlled_optimization_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "selected",
        "selection_reasons": [
            "midplatform eight-layer minimal backbone dryrun completed",
            "task_response_candidate midplatform first-round closure completed",
            "model_registry_canonical_v0 B-lite baseline closed",
            "health management has consumable health_signal + drive candidate skeleton",
            "health metric, hardware lifespan alert, robustness baseline lack real hardware/runtime data",
            "return to Vision / OCR / Voice controlled optimization planning now",
        ],
        "does_not_enable_real_model_or_provider": True,
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_health_metric_baseline_defer_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "deferred_until_hardware_ready",
        "defer_reasons": [
            "no real runtime monitor data",
            "no hardware operation samples",
            "no model/provider latency and error-rate baseline",
            "no hardware lifespan or failure samples",
            "do not define health score / threshold / weight now",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_hardware_lifespan_alert_defer_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "deferred_until_hardware_layer_ready",
        "defer_reasons": [
            "requires real hardware data",
            "requires battery/temperature/camera/compute/storage/network long-term samples",
            "requires hardware lifespan and aging observation data",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_robustness_baseline_defer_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "deferred_until_runtime_observation_ready",
        "defer_reasons": [
            "requires real runtime failure samples",
            "requires recovery success rate / degradation frequency / module fault samples",
            "only recovery_plan_candidate and fallback_candidate retained — no automatic policy now",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "post_health_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "selected"},
            {"route": ROUTE_B, "status": "deferred_until_hardware_ready"},
            {"route": ROUTE_C, "status": "deferred_until_hardware_layer_ready"},
            {"route": ROUTE_D, "status": "deferred_until_runtime_observation_ready"},
        ],
        "selected_route": SELECTED_ROUTE,
        "deferred_route_b": DEFERRED_ROUTE_B,
        "deferred_route_c": DEFERRED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        **meta,
    }

    preconditions = {
        "preconditions_id": "selected_route_preconditions_v1",
        "selected_route": SELECTED_ROUTE,
        "preconditions": [
            "model_registry_canonical_v0 baseline closed (B-lite)",
            "health_signal_and_drive_candidates_consumable",
            "health_metric_definition_status=reserved_not_defined",
            "controlled optimization planning only — no real model/provider",
            "no runtime monitor enabled",
            "no health score / threshold definition",
        ],
        "forbidden_now": [
            "real model invocation",
            "real provider invocation",
            "health metric baseline planning start",
            "hardware lifespan alert planning start",
            "robustness automatic policy definition",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_health_metric_hardware_robustness_register_v1",
        "deferred_items": [
            {
                "item_id": "health_metric_baseline",
                "route": ROUTE_B,
                "status": "deferred_until_hardware_ready",
                "health_score_defined_now": False,
            },
            {
                "item_id": "hardware_lifespan_alert",
                "route": ROUTE_C,
                "status": "deferred_until_hardware_layer_ready",
            },
            {
                "item_id": "robustness_baseline",
                "route": ROUTE_D,
                "status": "deferred_until_runtime_observation_ready",
            },
        ],
        "health_metric_definition_status": HEALTH_METRIC_DEFINITION_STATUS,
        **meta,
    }

    decision_ok = len(blockers) == 0
    boundary_ok = decision_ok

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_vision_ocr_voice_controlled_optimization_planning": boundary_ok,
        "selected_route": SELECTED_ROUTE,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "planning_only_no_runtime": True,
        **meta,
    }

    policy = {
        "policy_id": "post_health_roadmap_decision_policy_v1",
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
        "deferred_route_b": DEFERRED_ROUTE_B,
        "deferred_route_c": DEFERRED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "post_health_roadmap_decision_policy": policy,
        "health_post_review_input_review": input_review,
        "route_a_vision_ocr_voice_controlled_optimization_assessment": route_a,
        "route_b_health_metric_baseline_defer_assessment": route_b,
        "route_c_hardware_lifespan_alert_defer_assessment": route_c,
        "route_d_robustness_baseline_defer_assessment": route_d,
        "post_health_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_health_metric_hardware_robustness_register": deferred_register,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }

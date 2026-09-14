# -*- coding: utf-8 -*-
"""Luna Model Manager Foundation — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.luna_model_manager_processor_v1 import (
    build_model_admission_candidate,
    lookup_capability_providers,
    run_model_manager_planning,
)
from capabilities.midplatform.model_manager.luna_model_manager_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)
from capabilities.midplatform.model_manager.engines.model_routing_engine_v1 import (
    route_model_request,
)
from capabilities.midplatform.model_manager.engines.model_evaluation_engine_v1 import (
    evaluate_model_performance,
)


def _situation(scene: str, missing: List[str]) -> Dict[str, Any]:
    return {
        "scene_profile_candidate": {
            "scene_type": scene,
            "confidence": 0.35 if scene == "unknown_scene" else 0.85,
            "candidate_only": True,
            "not_fact": True,
        },
        "missing_information_candidates": [
            {"info_type": m, "candidate_only": True} for m in missing
        ],
        "candidate_only": True,
        "not_fact": True,
    }


def _ocr_plan() -> Dict[str, Any]:
    return {
        "plan_goal_candidate": {"goal_type": "identify_place"},
        "tool_plan_candidates": [{"capability_type": "ocr"}],
        "candidate_only": True,
    }


def _validation() -> Dict[str, Any]:
    return {"validation_status_candidate": "validated_candidate"}


def smoke_case_a_shopfront_ocr_routing() -> Dict[str, Any]:
    """Case A: shopfront → OCR score 0.95 > Qwen 0.4."""
    case_id = "case_a_shopfront_ocr_routing"
    result = run_model_manager_planning(
        situation_understanding_candidate=_situation("shopfront_sign", ["text_content", "place_identity"]),
        agent_plan_candidate=_ocr_plan(),
        decision_validation_candidate=_validation(),
    )
    routing = result.get("model_routing_result") or {}
    scores = {s["model_id"]: s["routing_score"] for s in routing.get("provider_scores", [])}
    passed = (
        routing.get("capability_need") == "text_recognition"
        and routing.get("selected_tool_id") == "ocr_v1"
        and scores.get("ocr_v1", 0) >= 0.9
        and scores.get("qwen_vl", 0) < scores.get("ocr_v1", 1)
        and routing.get("should_request_teacher") is False
        and result.get("no_auto_execution") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_b_unknown_scene_qwen_routing() -> Dict[str, Any]:
    """Case B: unknown_scene → Qwen 0.85."""
    case_id = "case_b_unknown_scene_qwen_routing"
    result = run_model_manager_planning(
        situation_understanding_candidate=_situation("unknown_scene", ["scene_identity", "environment_type"]),
        agent_plan_candidate=_ocr_plan(),
    )
    routing = result.get("model_routing_result") or {}
    scores = {s["model_id"]: s["routing_score"] for s in routing.get("provider_scores", [])}
    passed = (
        routing.get("capability_need") == "unknown_scene_reasoning"
        and routing.get("selected_model_id") == "qwen_vl"
        and scores.get("qwen_vl", 0) >= 0.8
        and routing.get("selected_tool_id") is None
        and routing.get("should_request_teacher") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_c_capability_first_lookup() -> Dict[str, Any]:
    """Case C: capability-first — need unknown_scene_reasoning → providers list."""
    case_id = "case_c_capability_first_lookup"
    lookup = lookup_capability_providers("unknown_scene_reasoning")
    provider_ids = [p.get("model_id") for p in lookup.get("providers", [])]
    passed = (
        lookup.get("found") is True
        and "qwen_vl" in provider_ids
        and "gemini_vision" in provider_ids
        and "human_review" in provider_ids
    )
    return {"case_id": case_id, "passed": passed, "lookup": lookup}


def smoke_case_d_model_admission_candidate() -> Dict[str, Any]:
    """Case D: Gemini admission candidate — no auto admission."""
    case_id = "case_d_model_admission_candidate"
    admission = build_model_admission_candidate(model_id="gemini_vision", model_type="teacher")
    passed = (
        admission.get("admission_status") == "candidate"
        and admission.get("no_auto_admission") is True
        and any(s.get("stage") == "benchmark" and s.get("status") == "pending" for s in admission.get("pipeline_stages", []))
    )
    return {"case_id": case_id, "passed": passed, "admission": admission}


def smoke_case_e_unified_evaluation_profile() -> Dict[str, Any]:
    """Case E: unified evaluation subsumes teacher performance metrics."""
    case_id = "case_e_unified_evaluation_profile"
    metrics = {
        "evidence_accept_rate": 0.33,
        "rejection_rate": 0.67,
        "hallucination_rate": 0.33,
        "useful_evidence_rate": 0.33,
        "latency_ms_avg": 0.05,
        "cost_estimate_total": 0.015,
        "teacher_value_score_avg": -0.09,
        "unsupported_claim_rate": 0.33,
    }
    eval_result = evaluate_model_performance(
        model_id="qwen_vl",
        scene_type="unknown_scene",
        performance_metrics=metrics,
    )
    profile = eval_result.get("model_evaluation_profile") or {}
    passed = (
        eval_result.get("evaluation_engine") == "model_evaluation_engine_v1"
        and profile.get("model_id") == "qwen_vl"
        and eval_result.get("does_not_affect_current_decision") is True
        and eval_result.get("no_auto_policy_update") is True
        and profile.get("routing_profile_candidate", {}).get("recommended_usage") == "high"
    )
    return {"case_id": case_id, "passed": passed, "evaluation": eval_result}


def run_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a_shopfront_ocr_routing,
        smoke_case_b_unknown_scene_qwen_routing,
        smoke_case_c_capability_first_lookup,
        smoke_case_d_model_admission_candidate,
        smoke_case_e_unified_evaluation_profile,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Foundation-Planning-v1-001",
        "planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "unified_manager": True,
        "teacher_system_subsumed": True,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }

# -*- coding: utf-8 -*-
"""Local Model Runtime DryRun Adapter — full transparent chain v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.engines.model_evaluation_engine_v1 import (
    evaluate_model_performance,
)
from capabilities.midplatform.model_manager.local_runtime.dryrun.local_model_resource_scheduler_v1 import (
    schedule_runtime_resources,
)
from capabilities.midplatform.model_manager.local_runtime.dryrun.local_model_runtime_health_dryrun_v1 import (
    build_runtime_unavailable_candidate,
    run_local_runtime_health_dryrun,
)
from capabilities.midplatform.model_manager.local_runtime.dryrun.local_model_runtime_selection_v1 import (
    select_runtime_provider,
)
from capabilities.midplatform.model_manager.local_runtime.local_model_lifecycle_adapter_v1 import (
    LOCAL_MODEL_ID,
    run_local_version_upgrade,
)
from capabilities.midplatform.model_manager.luna_model_manager_local_model_processor_v1 import (
    build_provider_fallback_candidate,
)
from capabilities.midplatform.model_manager.luna_model_manager_local_model_types_v1 import (
    EXTERNAL_MODEL_ID,
    LOCAL_MODEL_ID as INTERNVL_ID,
)
from capabilities.midplatform.model_manager.model_manager_dryrun.luna_model_manager_dryrun_adapter_v1 import (
    run_model_manager_dryrun,
)
from capabilities.midplatform.model_manager.providers.qwen_vl.dryrun.qwen_vl_evidence_normalizer_v1 import (
    detect_unsupported_claim,
    normalize_qwen_evidence_candidate,
)
from capabilities.midplatform.model_manager.providers.qwen_vl.qwen_vl_provider_adapter_v1 import (
    review_qwen_provider_evidence,
)
from capabilities.midplatform.model_manager.providers.qwen_vl.qwen_vl_response_parser_v1 import (
    parse_qwen_vl_provider_response,
)
from capabilities.midplatform.model_manager.runtime.local_model_runtime_adapter_v1 import (
    build_local_model_record,
    invoke_local_runtime,
)

DRYRUN_POLICY_REF = "local_model_runtime_dryrun_policy_v1"
FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LOCAL_MODEL_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LOCAL_MODEL_INTEGRATION_DRYRUN_BLOCKED"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[5]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[5]


def _load_fixture(fixture_id: str) -> Dict[str, Any]:
    path = (
        _repo_root()
        / "capabilities/midplatform/teacher_adapter/providers/qwen_vl/fixtures/raw_responses"
        / f"{fixture_id}.json"
    )
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _active_local_record() -> Dict[str, Any]:
    record = build_local_model_record(
        model_id=INTERNVL_ID,
        model_label="InternVL 2.5",
        capabilities=["scene_understanding", "visual_reasoning", "unknown_scene_reasoning"],
    )
    record["lifecycle_state"] = "active"
    record["admission_status"] = "admitted"
    return record


def _build_local_evidence(
    *,
    situation: Dict[str, Any],
    mock_scenario: str = "unknown_scene_hypothesis",
) -> Dict[str, Any]:
    """Local runtime output → same governance normalizer as API models."""
    raw = _load_fixture(mock_scenario)
    parsed = parse_qwen_vl_provider_response(
        {"raw_response": raw.get("raw_response", raw), "candidate_only": True},
        request_context={"model_id": INTERNVL_ID},
    )
    if parsed.get("parse_status") != "ok":
        return {"parsed": parsed, "normalized": None, "has_unsupported_claim": False}

    normalized = normalize_qwen_evidence_candidate(
        parsed_response=parsed,
        situation_candidate=situation,
        raw_envelope={"source": "local_runtime", "mock_scenario": mock_scenario},
    )
    normalized["execution_mode"] = "local_runtime"
    normalized["provider_id"] = INTERNVL_ID
    unsupported = detect_unsupported_claim(normalized) or parsed.get("has_unsupported_claim", False)
    return {
        "parsed": parsed,
        "normalized": normalized,
        "has_unsupported_claim": unsupported,
    }


def run_local_model_runtime_dryrun(
    job_envelope: Dict[str, Any],
    *,
    case_id: str = "dryrun",
    gpu_memory_available_gb: float = 12,
    internvl_status: str = "available",
    scoring_mode: str = "cost_priority",
    mock_scenario: str = "unknown_scene_hypothesis",
    force_internvl_unavailable: bool = False,
) -> Dict[str, Any]:
    """
    Full chain:
    L1→L2→L2.5→MM→Capability→Runtime Selection→Adapter→Evidence→Validation→Evaluation.
    """
    dryrun_id = _uid("lrd")
    capability_id = "unknown_scene_reasoning"

    mm_result = run_model_manager_dryrun(
        job_envelope,
        score_profile="unknown_scene_multi",
    )
    situation = mm_result.get("situation_understanding_candidate") or {}
    plan = mm_result.get("agent_plan_candidate") or {}
    validation = mm_result.get("decision_validation_candidate") or {}

    if force_internvl_unavailable:
        internvl_status = "insufficient"
        gpu_memory_available_gb = 2.0

    health = run_local_runtime_health_dryrun(gpu_memory_available_gb=gpu_memory_available_gb)
    profiles = schedule_runtime_resources(
        model_ids=["internvl2_5", "qwen_vl", "gemini_vision"],
        gpu_memory_available_gb=gpu_memory_available_gb,
        internvl_status=internvl_status,
    )

    selection = select_runtime_provider(
        capability_id=capability_id,
        resource_profiles=profiles,
        scoring_mode=scoring_mode,
    )

    selected = selection.get("selected_provider") or {}
    selected_id = selected.get("model_id")
    model_record = _active_local_record()

    runtime_unavailable = None
    fallback_provider = None
    provider_result = None
    evidence_bundle = None
    provider_review = None

    if force_internvl_unavailable:
        runtime_unavailable = build_runtime_unavailable_candidate(
            model_id=INTERNVL_ID,
            reason="gpu_memory_insufficient",
        )
        fallback_provider = build_provider_fallback_candidate(
            primary_model_id=INTERNVL_ID,
            fallback_model_id=EXTERNAL_MODEL_ID,
            reason="runtime_unavailable",
            capability_id=capability_id,
        )
        selected_id = None
    elif selected_id == INTERNVL_ID:
        profile = profiles.get(INTERNVL_ID, {})
        provider_result = invoke_local_runtime(
            model_record=model_record,
            resource_profile=profile,
        )
        evidence_bundle = _build_local_evidence(situation=situation, mock_scenario=mock_scenario)
        if evidence_bundle.get("has_unsupported_claim"):
            provider_result["has_unsupported_claim"] = True
            provider_result["evidence_candidate"] = None
        else:
            norm = evidence_bundle.get("normalized") or {}
            provider_result["evidence_candidate"] = norm
            provider_result["scene_hypothesis_candidate"] = norm.get("scene_hypothesis_candidate")
            provider_result["visual_reasoning_candidate"] = norm.get("visual_reasoning_candidate")

        provider_review = review_qwen_provider_evidence(
            provider_result=provider_result,
            routing_result=selected,
            plan=plan,
            situation=situation,
        )

    metrics = {
        "usage_count": 1,
        "selected_count": 1 if selected_id == INTERNVL_ID else 0,
        "noop_count": 0 if selected_id == INTERNVL_ID else 1,
        "useful_evidence_rate": 1.0 if (provider_review or {}).get("validation_status") == "accepted_as_evidence" else 0.0,
        "unsupported_claim_rate": 1.0 if evidence_bundle and evidence_bundle.get("has_unsupported_claim") else 0.0,
        "latency_ms_avg": 2000 if selected_id == INTERNVL_ID else 0,
        "cost_estimate_total": 0.0,
    }
    evaluation_record = evaluate_model_performance(
        model_id=selected_id or INTERNVL_ID,
        scene_type=(situation.get("scene_profile_candidate") or {}).get("scene_type", ""),
        performance_metrics=metrics,
        routing_result=selected,
    )

    return {
        "dryrun_id": dryrun_id,
        "case_id": case_id,
        "chain": [
            "situation_understanding_candidate",
            "agent_plan_candidate",
            "decision_validation_candidate",
            "capability_match",
            "runtime_selection",
            "local_runtime_adapter",
            "evidence_candidate",
            "validation",
            "evaluation_record",
        ],
        "model_manager_result": mm_result,
        "capability_id": capability_id,
        "runtime_health": health,
        "resource_profiles": profiles,
        "runtime_selection": selection,
        "provider_selected_id": selected_id,
        "selection_reason": selected.get("selection_reason"),
        "provider_result": provider_result,
        "evidence_bundle": evidence_bundle,
        "provider_validation_review": provider_review,
        "runtime_unavailable_candidate": runtime_unavailable,
        "fallback_provider_candidate": fallback_provider,
        "model_evaluation_record": evaluation_record,
        "runtime_not_tool_os": True,
        "runtime_not_task_decider": True,
        "upper_layer_transparent": True,
        "dryrun_only": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [DRYRUN_POLICY_REF],
    }


def run_local_vs_external_competition_dryrun(
    *,
    gpu_memory_available_gb: float = 12,
    internvl_status: str = "available",
) -> Dict[str, Any]:
    """Case C: multi-factor provider competition."""
    profiles = schedule_runtime_resources(
        model_ids=["internvl2_5", "qwen_vl", "gemini_vision"],
        gpu_memory_available_gb=gpu_memory_available_gb,
        internvl_status=internvl_status,
    )
    selection = select_runtime_provider(
        capability_id="unknown_scene_reasoning",
        resource_profiles=profiles,
        scoring_mode="balanced",
    )
    selected = selection.get("selected_provider") or {}
    scores = selection.get("provider_scores") or []
    return {
        "resource_profiles": profiles,
        "runtime_selection": selection,
        "multi_factor_scoring": all(
            s.get("capability_score") is not None
            and s.get("resource_score") is not None
            for s in scores
        ),
        "not_capability_only": len({s["routing_score"] for s in scores}) > 1,
        "provider_selection_candidate": True,
        "selected_provider_id": selected.get("model_id"),
        "candidate_only": True,
        "not_fact": True,
    }


def run_local_lifecycle_upgrade_dryrun() -> Dict[str, Any]:
    """Case E: runtime lifecycle upgrade — L1/L2 unchanged."""
    return run_local_version_upgrade(gpu_memory_available_gb=12)

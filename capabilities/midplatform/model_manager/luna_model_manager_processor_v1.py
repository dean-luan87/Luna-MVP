# -*- coding: utf-8 -*-
"""Luna Model Manager — foundation processor v1 (planning orchestrator)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.engines.model_evaluation_engine_v1 import (
    evaluate_model_performance,
)
from capabilities.midplatform.model_manager.engines.model_routing_engine_v1 import (
    resolve_capability_need,
    route_model_request,
    score_providers,
)
from capabilities.midplatform.model_manager.luna_model_manager_types_v1 import (
    LIFECYCLE_REF,
    POLICY_REF,
)

FROZEN_MODULES = (
    "teacher_adapter",
    "teacher_routing",
    "teacher_performance_evaluation",
    "qwen_vl_real_provider",
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[3]


def _load_json(rel: str) -> Dict[str, Any]:
    path = _repo_root() / rel
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def lookup_capability_providers(capability_id: str) -> Dict[str, Any]:
    """Capability-first lookup — who provides this capability?"""
    registry = _load_json("capabilities/midplatform/model_manager/registries/capability_registry_v1.json")
    entry = next((c for c in registry.get("capabilities") or [] if c.get("capability_id") == capability_id), None)
    if not entry:
        return {"capability_id": capability_id, "providers": [], "found": False}
    return {
        "capability_id": capability_id,
        "capability_label": entry.get("capability_label"),
        "providers": entry.get("providers", []),
        "found": True,
        "candidate_only": True,
        "not_fact": True,
    }


def build_model_admission_candidate(
    *,
    model_id: str,
    model_type: str = "teacher",
) -> Dict[str, Any]:
    """Model Admission pipeline candidate — no auto admission."""
    return {
        "admission_candidate_id": _uid("mac"),
        "model_id": model_id,
        "model_type": model_type,
        "pipeline_stages": [
            {"stage": "model_candidate", "status": "completed"},
            {"stage": "security_review", "status": "pending"},
            {"stage": "capability_review", "status": "pending"},
            {"stage": "benchmark", "status": "pending"},
            {"stage": "admission_decision", "status": "pending"},
        ],
        "admission_status": "candidate",
        "no_auto_admission": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF, LIFECYCLE_REF],
    }


def run_model_manager_planning(
    *,
    situation_understanding_candidate: Dict[str, Any],
    agent_plan_candidate: Dict[str, Any],
    decision_validation_candidate: Optional[Dict[str, Any]] = None,
    need_capability: Optional[str] = None,
    performance_metrics: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Model Manager foundation orchestrator (planning only).
    Unifies routing + evaluation + admission lookup.
    Does NOT execute models or tools.
    """
    manager_id = _uid("lmm")
    routing = route_model_request(
        situation_understanding_candidate=situation_understanding_candidate,
        agent_plan_candidate=agent_plan_candidate,
        decision_validation_candidate=decision_validation_candidate,
        need_capability=need_capability,
    )

    capability_id = routing.get("capability_need", "")
    capability_lookup = lookup_capability_providers(capability_id)

    evaluation = None
    selected_id = routing.get("selected_model_id") or routing.get("selected_tool_id")
    if selected_id and performance_metrics:
        scene = (situation_understanding_candidate.get("scene_profile_candidate") or {}).get("scene_type", "")
        evaluation = evaluate_model_performance(
            model_id=selected_id,
            scene_type=scene,
            performance_metrics=performance_metrics,
            routing_result=routing,
        )

    return {
        "manager_id": manager_id,
        "frozen_prerequisites": list(FROZEN_MODULES),
        "capability_need": capability_id,
        "capability_lookup": capability_lookup,
        "model_routing_result": routing,
        "model_evaluation_result": evaluation,
        "selected_provider_id": selected_id,
        "provider_scores": routing.get("provider_scores", []),
        "does_not_affect_current_decision": True,
        "no_auto_execution": True,
        "no_auto_admission": True,
        "planning_only": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF, LIFECYCLE_REF],
        "trace_refs": [{"stage": "model_manager", "ref": manager_id}],
    }

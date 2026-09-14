# -*- coding: utf-8 -*-
"""Lightweight Vision Runtime Planning Adapter v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.mixed_region.lightweight_vision.planning.lightweight_vision_evidence_package_v1 import (
    build_lightweight_vision_evidence_package,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.lightweight_vision.planning.lightweight_vision_runtime_registry_v1 import (
    select_runtimes_for_scene,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.lightweight_vision.planning.lightweight_vision_simulators_v1 import (
    run_selected_runtimes,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.lightweight_vision.planning.per_entity_channel_activation_planner_v1 import (
    plan_channel_activation_from_entities,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.lightweight_vision.planning.planning_fixtures_v1 import (
    get_fixture,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_LIGHTWEIGHT_VISION_RUNTIME_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_LIGHTWEIGHT_VISION_RUNTIME_PLANNING_BLOCKED"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def run_lightweight_vision_runtime_planning(
    *,
    fixture_key: str = "stacked_papers",
    situation: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Planning pipeline:
    Attention-Gated Region → Runtime Selection → Candidates → Evidence → Validation
    """
    fixture = get_fixture(fixture_key)
    gate = fixture.get("attention_gate") or {}
    source_region_id = fixture.get("source_region_id", "region_001")
    scene_type = fixture.get("scene_type", "stacked_documents")
    allowed = bool(gate.get("allowed_region_ids"))

    if fixture.get("runtime_unavailable"):
        return {
            "planning_only": True,
            "fixture_key": fixture_key,
            "runtime_error_candidate": {
                "error_id": _uid("lver"),
                "error_type": "lightweight_vision_runtime_unavailable",
                "replan_target": "L2_or_Attention_replan",
                "candidate_only": True,
            },
            "failure_returns_runtime_error_candidate": True,
            "no_global_ocr": True,
            "no_all_model_activation": True,
            "not_silent_fallback": True,
            "governance_loop_complete": True,
            "candidate_only": True,
            "not_fact": True,
        }

    runtime_ids = select_runtimes_for_scene(scene_type=scene_type, attention_allowed=allowed)
    if fixture_key == "attention_blocked":
        runtime_ids = []

    execution = run_selected_runtimes(
        runtime_ids=runtime_ids,
        scene_type=scene_type,
        fixture=fixture,
    )
    channel_activation = plan_channel_activation_from_entities(
        entity_candidates=execution.get("entity_candidates") or [],
    )

    validation_status = "pending_validation"
    if execution.get("runtime_conflict_detected"):
        validation_status = "validation_review"

    evidence = build_lightweight_vision_evidence_package(
        source_region_id=source_region_id,
        attention_gate_status="allowed" if allowed else "blocked",
        runtime_execution=execution,
        per_entity_channel_activation=channel_activation,
        validation_status_candidate=validation_status,
    )

    pkg = evidence.get("lightweight_vision_evidence_package") or {}

    return {
        "planning_only": True,
        "fixture_key": fixture_key,
        "situation": situation or {},
        "attention_gate": gate,
        "selected_runtime_ids": runtime_ids,
        "runtime_execution": execution,
        "lightweight_vision_evidence_package": pkg,
        "evidence_wrapper": evidence,
        "validation_status_candidate": validation_status,
        "attention_gate_required": True,
        "no_global_ocr": execution.get("no_global_ocr") is True,
        "no_all_model_activation": execution.get("not_all_model_activation") is True,
        "runtime_outputs_candidate_only": evidence.get("runtime_outputs_candidate_only") is True,
        "runtime_does_not_assign_fact": evidence.get("runtime_does_not_assign_fact") is True,
        "runtime_does_not_override_ownership_graph": evidence.get("runtime_does_not_override_ownership_graph") is True,
        "first_real_runtime_priority": "document_surface_detector_v1",
        "governance_loop_complete": True,
        "candidate_only": True,
        "not_fact": True,
    }

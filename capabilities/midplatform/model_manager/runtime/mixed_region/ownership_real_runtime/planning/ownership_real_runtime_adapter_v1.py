# -*- coding: utf-8 -*-
"""Ownership Real Runtime Integration Planning Adapter v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_real_runtime.planning.ownership_evidence_package_v1 import (
    build_ownership_evidence_package,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_real_runtime.planning.per_entity_channel_activation_v1 import (
    plan_per_entity_channel_activation,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_real_runtime.planning.planning_fixtures_v1 import (
    blocked_entity_ids,
    get_fixture,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_real_runtime.planning.slot_occlusion_reasoning_v1 import (
    run_slot_occlusion_reasoning,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_real_runtime.planning.slot_ownership_discovery_v1 import (
    run_slot_ownership_discovery,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_real_runtime.planning.slot_text_owner_assignment_v1 import (
    run_slot_text_owner_assignment,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_PLANNING_BLOCKED"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _validation_review(*, status: str, **extra: Any) -> Dict[str, Any]:
    return {
        "validation_id": _uid("val"),
        "validation_status": status,
        "not_fact_admission": True,
        "candidate_only": True,
        **extra,
    }


def run_ownership_real_runtime_planning(
    *,
    fixture_key: str = "stacked_papers",
    situation: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Planning pipeline:
    Attention-Gated Region → Discovery → Ownership → Occlusion → Text Owner
    → Channel Activation → Evidence → Validation
    """
    fixture = get_fixture(fixture_key)
    gate = fixture.get("attention_gate") or {}
    profile_key = fixture.get("profile_key", "stacked_documents")
    entity_id_map = fixture.get("entity_id_map") or {}
    blocked_ids = blocked_entity_ids(fixture)

    if fixture.get("runtime_unavailable"):
        return {
            "planning_only": True,
            "fixture_key": fixture_key,
            "situation": situation or {},
            "ownership_runtime_error_candidate": {
                "error_id": _uid("ore"),
                "error_type": "ownership_runtime_unavailable",
                "replan_target": "L2_or_Attention_replan",
                "candidate_only": True,
            },
            "validation_review": _validation_review(
                status="ownership_runtime_error_acknowledged",
                not_silent_fallback=True,
            ),
            "not_full_image_ocr_fallback": True,
            "not_all_models_fallback": True,
            "governance_loop_complete": True,
            "candidate_only": True,
            "not_fact": True,
        }

    discovery = run_slot_ownership_discovery(
        profile_key=profile_key,
        attention_gate=gate,
        entity_id_map=entity_id_map,
        blocked_entity_ids=blocked_ids,
        upstream_region_id=(gate.get("allowed_region_ids") or ["reg_gated"])[0],
    )
    occlusion = run_slot_occlusion_reasoning(
        discovery=discovery,
        profile_key=profile_key,
        entity_id_map=entity_id_map,
        blocked_entity_ids=blocked_ids,
    )
    text_assignment = run_slot_text_owner_assignment(
        discovery=discovery,
        occlusion=occlusion,
        profile_key=profile_key,
        entity_id_map=entity_id_map,
        blocked_entity_ids=blocked_ids,
    )
    channel_activation = plan_per_entity_channel_activation(
        entity_candidates=discovery.get("entity_candidates") or [],
        text_owner_assignments=text_assignment.get("text_owner_assignments") or [],
    )
    evidence = build_ownership_evidence_package(
        entity_candidates=discovery.get("entity_candidates") or [],
        relation_candidates=occlusion.get("relation_candidates") or [],
        text_owner_assignments=text_assignment.get("text_owner_assignments") or [],
        channel_activation=channel_activation,
        missing_information=fixture.get("missing_information"),
        blocked_regions=gate.get("blocked_regions") or [],
    )

    validation = _validation_review(status="accepted_as_ownership_evidence")

    return {
        "planning_only": True,
        "fixture_key": fixture_key,
        "situation": situation or {},
        "attention_gate": gate,
        "slot_ownership_discovery": discovery,
        "slot_occlusion_reasoning": occlusion,
        "slot_text_owner_assignment": text_assignment,
        "per_entity_channel_activation": channel_activation,
        "evidence_package": evidence,
        "validation_review": validation,
        "attention_gated_input": True,
        "carrier_before_ocr": discovery.get("carrier_before_ocr") is True,
        "text_owner_binding": text_assignment.get("each_text_has_owner") is True,
        "not_full_image_ocr": True,
        "blocked_entities_excluded": len(blocked_ids) > 0,
        "governance_loop_complete": True,
        "candidate_only": True,
        "not_fact": True,
    }

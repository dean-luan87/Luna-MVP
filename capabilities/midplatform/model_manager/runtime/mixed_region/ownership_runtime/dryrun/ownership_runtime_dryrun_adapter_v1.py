# -*- coding: utf-8 -*-
"""Ownership Runtime DryRun Adapter — governance loop v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_runtime.dryrun.dryrun_fixtures_v1 import (
    get_fixture,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_runtime.dryrun.occlusion_reasoning_simulator_v1 import (
    simulate_occlusion_reasoning,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_runtime.dryrun.ownership_discovery_simulator_v1 import (
    simulate_ownership_discovery,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_runtime.dryrun.ownership_evidence_package_builder_v1 import (
    build_ownership_evidence_package,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_runtime.dryrun.ownership_slot_binding_v1 import (
    bind_ownership_slots,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_runtime.dryrun.per_entity_channel_activation_adapter_v1 import (
    adapt_per_entity_channel_activation,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_runtime.dryrun.text_owner_assignment_simulator_v1 import (
    simulate_text_owner_assignment,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_DRYRUN_BLOCKED"


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


def run_ownership_runtime_dryrun(
    *,
    fixture_key: str = "stacked_papers",
    situation: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    DryRun governance loop:
    Attention-Gated Region → Slot Binding → Discovery → Occlusion → Text Owner
    → Evidence Package → Channel Activation → Validation
    """
    fixture = get_fixture(fixture_key)
    gate = fixture.get("attention_gate") or {}
    source_region_id = (gate.get("allowed_region_ids") or ["region_001"])[0]

    if fixture.get("runtime_unavailable"):
        return {
            "dryrun_only": True,
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
                runtime_error_no_silent_fallback=True,
            ),
            "no_global_ocr": True,
            "no_all_model_activation": True,
            "not_full_image_ocr_fallback": True,
            "runtime_error_no_silent_fallback": True,
            "governance_loop_complete": True,
            "candidate_only": True,
            "not_fact": True,
        }

    slot_binding = bind_ownership_slots(
        attention_gate=gate,
        source_region_id=source_region_id,
    )
    discovery = simulate_ownership_discovery(fixture=fixture, slot_binding=slot_binding)
    occlusion = simulate_occlusion_reasoning(fixture=fixture, discovery=discovery)
    text_assignment = simulate_text_owner_assignment(
        fixture=fixture,
        discovery=discovery,
        occlusion=occlusion,
    )
    channel_activation = adapt_per_entity_channel_activation(
        entity_candidates=discovery.get("entity_candidates") or [],
        text_owner_assignments=text_assignment.get("text_owner_assignments") or [],
    )
    evidence = build_ownership_evidence_package(
        source_region_id=source_region_id,
        attention_gate_status=slot_binding.get("attention_gate_status", "allowed"),
        entity_candidates=discovery.get("entity_candidates") or [],
        relation_candidates=occlusion.get("relation_candidates") or [],
        text_owner_assignments=text_assignment.get("text_owner_assignments") or [],
        per_entity_channel_activation_candidates=channel_activation.get(
            "per_entity_channel_activation_candidates"
        ) or [],
        missing_information_candidates=fixture.get("missing_information"),
        blocked_regions=gate.get("blocked_regions") or [],
    )

    pkg = evidence.get("ownership_evidence_package") or {}
    validation = _validation_review(
        status="accepted_as_ownership_runtime_evidence",
        attention_gate_required=True,
    )

    return {
        "dryrun_only": True,
        "fixture_key": fixture_key,
        "situation": situation or {},
        "ownership_slot_binding": slot_binding,
        "slot_ownership_discovery": discovery,
        "slot_occlusion_reasoning": occlusion,
        "slot_text_owner_assignment": text_assignment,
        "per_entity_channel_activation": channel_activation,
        "ownership_evidence_package": pkg,
        "evidence_wrapper": evidence,
        "validation_review": validation,
        "attention_gate_required": slot_binding.get("attention_gate_required") is True,
        "slots_in_order": slot_binding.get("slots_in_order") is True,
        "no_global_ocr": evidence.get("no_global_ocr") is True,
        "no_all_model_activation": channel_activation.get("no_all_model_activation") is True,
        "owner_required_for_text": text_assignment.get("owner_required_for_text") is True,
        "occlusion_not_absence": occlusion.get("occlusion_not_absence") is True,
        "candidate_only_not_fact": evidence.get("candidate_only_not_fact") is True,
        "governance_loop_complete": True,
        "candidate_only": True,
        "not_fact": True,
    }

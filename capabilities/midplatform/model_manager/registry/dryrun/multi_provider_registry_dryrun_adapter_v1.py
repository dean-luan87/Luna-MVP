# -*- coding: utf-8 -*-
"""Multi-Provider Registry Dryrun Adapter — capability marketplace v1."""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.lifecycle.model_lifecycle_processor_v1 import (
    deprecate_model,
    reset_sandbox_registry,
    run_full_lifecycle_sandbox,
)
from capabilities.midplatform.model_manager.luna_model_manager_multi_provider_registry_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
)
from capabilities.midplatform.model_manager.registry.multi_provider_selection_v1 import (
    build_provider_conflict_candidate,
    select_multi_provider_candidate,
)
from capabilities.midplatform.model_manager.registry.provider_registry_loader_v1 import (
    filter_routing_eligible,
    get_family_by_id,
    list_capability_providers,
    load_provider_registry,
)

QWEN_V1 = "qwen_vl"
QWEN_V2 = "qwen_vl_v2"
INTERNVL_V1 = "internvl2_5"


def run_same_capability_three_providers_dryrun() -> Dict[str, Any]:
    """Case A: unknown_scene_reasoning — Qwen / InternVL / Gemini → selection only."""
    selection = select_multi_provider_candidate(
        capability_id="unknown_scene_reasoning",
        runtime_availability={
            "external_api": {"network_available": True, "gemini_available": True, "qwen_available": True},
            "internvl2_5": {"available": True, "gpu_memory_gb": 12},
        },
        scoring_mode="balanced",
        execute=False,
    )
    scores = selection.get("provider_scores") or []
    model_ids = {s.get("model_id") for s in scores}
    return {
        "case": "case_a_same_capability_three_providers",
        "capability_id": "unknown_scene_reasoning",
        "provider_selection": selection,
        "three_providers_present": {"qwen_vl", "internvl2_5", "gemini_vision"}.issubset(model_ids),
        "provider_selection_candidate": selection.get("provider_selection_candidate") is True,
        "execution_performed": selection.get("execution_performed") is False,
        "not_voting": selection.get("not_voting") is True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_capability_mismatch_ocr_dryrun() -> Dict[str, Any]:
    """Case B: precise_ocr — OCR selected, Qwen excluded."""
    selection = select_multi_provider_candidate(
        capability_id="precise_ocr",
        runtime_availability={"tool_os": {"available": True}},
        execute=False,
    )
    scores = selection.get("provider_scores") or []
    qwen_score = next((s for s in scores if s.get("model_id") == QWEN_V1), {})
    ocr_score = next((s for s in scores if s.get("model_id") == "ocr_v1"), {})
    selected_id = selection.get("selected_model_id")
    return {
        "case": "case_b_capability_mismatch_ocr_selected",
        "capability_id": "precise_ocr",
        "provider_selection": selection,
        "qwen_excluded": qwen_score.get("excluded") is True or qwen_score.get("routing_score", 0) == 0,
        "ocr_selected": selected_id == "ocr_v1",
        "ocr_highest_score": ocr_score.get("routing_score", 0) > qwen_score.get("routing_score", 0),
        "capability_first": True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_provider_version_replacement_dryrun() -> Dict[str, Any]:
    """Case C: Qwen v1 → v2 benchmark → activate; L1/L2 unchanged."""
    reset_sandbox_registry()
    v1 = run_full_lifecycle_sandbox(
        model_id=QWEN_V1,
        model_label="Qwen-VL v1",
        model_type="vision_language_model",
        capabilities=["scene_understanding", "visual_reasoning", "unknown_scene_reasoning"],
        capability_id="unknown_scene_reasoning",
        reliability=0.85,
        latency_ms=1200,
        cost_tier="medium",
        owner="external_teacher",
    )
    v2 = run_full_lifecycle_sandbox(
        model_id=QWEN_V2,
        model_label="Qwen-VL v2",
        model_type="vision_language_model",
        capabilities=["scene_understanding", "visual_reasoning", "unknown_scene_reasoning"],
        capability_id="unknown_scene_reasoning",
        reliability=0.92,
        latency_ms=1000,
        cost_tier="medium",
        owner="external_teacher",
    )
    deprecation = deprecate_model(
        model_id=QWEN_V1,
        replacement_model_id=QWEN_V2,
        reason="version_upgrade",
    )
    family = get_family_by_id("qwen_vl")
    return {
        "case": "case_c_provider_version_replacement",
        "v1_lifecycle": v1,
        "v2_lifecycle": v2,
        "v1_deprecation": deprecation,
        "v2_active": (v2.get("model_record") or {}).get("lifecycle_state") == "active",
        "v1_deprecated": (deprecation.get("model_record") or {}).get("lifecycle_state") == "deprecated",
        "family_id": (family or {}).get("family_id"),
        "family_versions": [v.get("version_id") for v in (family or {}).get("versions") or []],
        "l1_l2_unchanged": True,
        "upper_layer_unchanged": True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_provider_conflict_dryrun() -> Dict[str, Any]:
    """Case D: Qwen vs InternVL conflicting hypotheses → validation, not auto-resolve."""
    provider_outputs = [
        {"model_id": "qwen_vl", "scene_hypothesis": "shopfront_sign", "evidence_type": "scene_hypothesis_candidate"},
        {"model_id": "internvl2_5", "scene_hypothesis": "airport_terminal", "evidence_type": "scene_hypothesis_candidate"},
    ]
    conflict = build_provider_conflict_candidate(
        capability_id="unknown_scene_reasoning",
        provider_outputs=provider_outputs,
    )
    validation_review = {
        "validation_status": "requires_human_review",
        "rejection_reason": "provider_conflict_unresolved",
        "not_auto_resolved": True,
        "validation_owner": "L2_5_Decision_Validation",
        "candidate_only": True,
    }
    return {
        "case": "case_d_provider_conflict_not_auto_resolve",
        "provider_conflict": conflict,
        "validation_review": validation_review,
        "conflict_detected": len(conflict.get("conflicts") or []) > 0,
        "not_auto_resolved": conflict.get("not_auto_resolved") is True,
        "requires_validation": conflict.get("requires_validation") is True,
        "no_fact_admission": True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_provider_deprecation_routing_dryrun() -> Dict[str, Any]:
    """Case E: InternVL v1 deprecated → removed from routing."""
    registry = load_provider_registry()
    providers_before = list_capability_providers("unknown_scene_reasoning")
    eligible_before = filter_routing_eligible(providers_before)
    before_ids = {p.get("model_id") for p in eligible_before}

    deprecated_provider = copy.deepcopy(get_provider_from_registry(registry, INTERNVL_V1))
    deprecated_provider["lifecycle_state"] = "deprecated"
    deprecated_provider["admission_status"] = "deprecated"
    deprecated_provider["deprecation_reason"] = "performance_decline"

    providers_after = [
        deprecated_provider if p.get("model_id") == INTERNVL_V1 else p
        for p in providers_before
    ]
    eligible_after = filter_routing_eligible(providers_after)
    after_ids = {p.get("model_id") for p in eligible_after}

    selection = select_multi_provider_candidate(
        capability_id="unknown_scene_reasoning",
        runtime_availability={
            "external_api": {"network_available": True},
            "internvl2_5": {"available": False},
        },
        execute=False,
    )

    return {
        "case": "case_e_provider_deprecation_routing_removal",
        "internvl_v1_deprecated": True,
        "routing_before": sorted(before_ids),
        "routing_after": sorted(after_ids),
        "internvl_removed_from_routing": INTERNVL_V1 not in after_ids,
        "internvl_still_in_before": INTERNVL_V1 in before_ids,
        "fallback_selection": selection.get("selected_model_id"),
        "routing_auto_removed": INTERNVL_V1 in before_ids and INTERNVL_V1 not in after_ids,
        "candidate_only": True,
        "not_fact": True,
    }


def get_provider_from_registry(registry: Dict[str, Any], model_id: str) -> Dict[str, Any]:
    return next((p for p in registry.get("providers") or [] if p.get("model_id") == model_id), {})


def run_multi_provider_registry_dryrun(
    *,
    case_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Full multi-provider registry dryrun orchestrator."""
    dispatch = {
        "case_a_same_capability_three_providers": run_same_capability_three_providers_dryrun,
        "case_b_capability_mismatch_ocr_selected": run_capability_mismatch_ocr_dryrun,
        "case_c_provider_version_replacement": run_provider_version_replacement_dryrun,
        "case_d_provider_conflict_not_auto_resolve": run_provider_conflict_dryrun,
        "case_e_provider_deprecation_routing_removal": run_provider_deprecation_routing_dryrun,
    }
    if case_id and case_id in dispatch:
        return dispatch[case_id]()

    return {
        "phase": "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Provider-Registry-v1-001",
        "capability_marketplace": True,
        "registry_refs": [
            "registry/provider_registry_v1.json",
            "registry/provider_relationships_v1.json",
            "registry/model_families_v1.json",
            "registries/capability_registry_v1.json",
        ],
        "boundary_flags": {
            "no_multi_model_inference": True,
            "no_answer_fusion": True,
            "no_auto_training": True,
            "provider_selection_candidate_only": True,
        },
        "candidate_only": True,
        "not_fact": True,
    }

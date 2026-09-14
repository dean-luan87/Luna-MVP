# -*- coding: utf-8 -*-
"""Region Intelligence Adapter — ownership + five-channel pipeline v1."""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.midplatform.model_manager.runtime.mixed_region.context_evidence_builder_v1 import (
    build_context_evidence,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.information_channel_activation_v1 import (
    activate_information_channels,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.mixed_region_analyzer_v1 import (
    analyze_mixed_region,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_understanding.occlusion_graph_v1 import (
    build_occlusion_graph,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_understanding.ownership_evidence_builder_v1 import (
    build_ownership_evidence,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_understanding.region_owner_analyzer_v1 import (
    analyze_region_owners,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_understanding.text_owner_assignment_v1 import (
    assign_text_owners,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.semantic_fusion_adapter_v1 import (
    fuse_mixed_evidence,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.spatial_evidence_builder_v1 import (
    build_spatial_evidence,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.text_evidence_builder_v1 import (
    build_text_evidence,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.visual_evidence_builder_v1 import (
    build_visual_evidence,
)
from capabilities.midplatform.model_manager.runtime.text_recognition.text_recognition_runtime_adapter_v1 import (
    run_text_recognition_slot,
)

TEXT_SLOTS = frozenset({"text", "price_number"})
OWNERSHIP_PROFILES = frozenset({
    "stacked_documents", "glass_reflection", "shelf_multi_entity", "device_screen",
})


def _text_slot_required(region_analysis: Dict[str, Any]) -> bool:
    if region_analysis.get("text_absent"):
        return False
    slots = region_analysis.get("information_slots") or []
    return any(s in TEXT_SLOTS for s in slots)


def _build_channel_result(
    *,
    situation: Dict[str, Any],
    plan: Dict[str, Any],
    region_evidence: Dict[str, Any],
    region_analysis: Dict[str, Any],
    ocr_fixture_key: str,
    visual_fixture_key: str,
    spatial_fixture_key: str,
    context_fixture_key: str,
    ocr_scenario: str,
) -> Dict[str, Any]:
    text_path_result: Dict[str, Any] = {}
    text_evidence: Dict[str, Any] = {
        "type": "text_candidate", "status": "slot_not_required", "candidate_only": True,
    }
    if _text_slot_required(region_analysis):
        text_path_result = run_text_recognition_slot(
            situation=situation,
            plan=plan,
            text_region_evidence=region_evidence,
            fixture_key=ocr_fixture_key,
            scenario=ocr_scenario,
        )
        text_evidence = build_text_evidence(
            ocr_evidence=text_path_result.get("evidence_package") or {},
            region_analysis=region_analysis,
        )
        if text_evidence.get("confidence", 0) < 0.5:
            text_evidence["low_confidence"] = True

    return {
        "text_evidence": text_evidence,
        "text_path_result": text_path_result,
        "visual_evidence": build_visual_evidence(fixture_key=visual_fixture_key, region_analysis=region_analysis),
        "spatial_evidence": build_spatial_evidence(fixture_key=spatial_fixture_key, region_analysis=region_analysis),
        "context_evidence": build_context_evidence(
            situation=situation, fixture_key=context_fixture_key, region_analysis=region_analysis,
        ),
    }


def run_region_intelligence(
    *,
    situation: Dict[str, Any],
    plan: Dict[str, Any],
    region_evidence: Dict[str, Any],
    region_profile: str = "shopfront_mixed",
    ownership_profile: Optional[str] = None,
    ocr_fixture_key: str = "shopfront_ashu",
    visual_fixture_key: str = "shopfront_occlusion",
    spatial_fixture_key: str = "shopfront_default",
    context_fixture_key: str = "commercial_shopfront",
    ocr_scenario: str = "shopfront",
) -> Dict[str, Any]:
    """
    Region Intelligence Layer:
    Region Discovery → Ownership (if needed) → Channel Activation → Evidence → Fusion
    """
    ownership_key = ownership_profile or (region_profile if region_profile in OWNERSHIP_PROFILES else None)

    if ownership_key:
        return _run_ownership_pipeline(
            situation=situation,
            plan=plan,
            region_evidence=region_evidence,
            ownership_profile=ownership_key,
            visual_fixture_key=visual_fixture_key,
            spatial_fixture_key=spatial_fixture_key,
            context_fixture_key=context_fixture_key,
        )

    region_analysis = analyze_mixed_region(region_evidence=region_evidence, profile_key=region_profile)
    channel_activations = activate_information_channels(
        region_analysis=region_analysis,
        region_id=region_analysis.get("region_id", "region_001"),
    )
    ch = _build_channel_result(
        situation=situation, plan=plan, region_evidence=region_evidence,
        region_analysis=region_analysis, ocr_fixture_key=ocr_fixture_key,
        visual_fixture_key=visual_fixture_key, spatial_fixture_key=spatial_fixture_key,
        context_fixture_key=context_fixture_key, ocr_scenario=ocr_scenario,
    )
    mixed_fusion = fuse_mixed_evidence(
        text_evidence=ch["text_evidence"],
        visual_evidence=ch["visual_evidence"],
        spatial_evidence=ch["spatial_evidence"],
        context_evidence=ch["context_evidence"],
        channel_activations=channel_activations,
        region_analysis=region_analysis,
        situation=situation,
    )
    return _assemble_result(
        region_analysis=region_analysis,
        channel_activations=channel_activations,
        ch=ch,
        mixed_fusion=mixed_fusion,
        ownership_evidence=None,
        ownership_layer=None,
    )


def _run_ownership_pipeline(
    *,
    situation: Dict[str, Any],
    plan: Dict[str, Any],
    region_evidence: Dict[str, Any],
    ownership_profile: str,
    visual_fixture_key: str,
    spatial_fixture_key: str,
    context_fixture_key: str,
) -> Dict[str, Any]:
    """Ownership-first: Region Discovery → Occlusion → per-owner OCR → Fusion."""
    upstream_id = region_evidence.get("evidence_id", "region_001")
    owner_analysis = analyze_region_owners(profile_key=ownership_profile, upstream_region_id=upstream_id)
    occlusion_graph = build_occlusion_graph(owner_analysis=owner_analysis, profile_key=ownership_profile)
    text_assignment = assign_text_owners(
        owner_analysis=owner_analysis,
        profile_key=ownership_profile,
        occlusion_graph=occlusion_graph,
    )
    ownership_evidence = build_ownership_evidence(
        owner_analysis=owner_analysis,
        occlusion_graph=occlusion_graph,
        text_assignment=text_assignment,
    )

    region_analysis = {
        "analysis_id": owner_analysis.get("analysis_id"),
        "region_id": upstream_id,
        "region_type_candidate": owner_analysis.get("region_type_candidate"),
        "information_slots": owner_analysis.get("information_slots", []),
        "ownership_first": True,
        "candidate_only": True,
    }
    channel_activations = activate_information_channels(
        region_analysis=region_analysis,
        region_id=upstream_id,
    )

    ch = {
        "text_evidence": {
            "type": "text_candidate",
            "status": "per_owner_assignment",
            "text_with_owners": text_assignment.get("text_with_owners"),
            "candidate_only": True,
        },
        "text_path_result": {},
        "visual_evidence": build_visual_evidence(
            fixture_key=visual_fixture_key,
            region_analysis={"information_slots": ["visual_symbol"]},
        ),
        "spatial_evidence": build_spatial_evidence(
            fixture_key=spatial_fixture_key,
            region_analysis={"information_slots": ["layout"]},
        ),
        "context_evidence": build_context_evidence(
            situation=situation,
            fixture_key=context_fixture_key,
            region_analysis={"information_slots": ["context"]},
        ),
    }

    mixed_fusion = fuse_mixed_evidence(
        text_evidence=ch["text_evidence"],
        visual_evidence=ch["visual_evidence"],
        spatial_evidence=ch["spatial_evidence"],
        context_evidence=ch["context_evidence"],
        ownership_evidence=ownership_evidence,
        channel_activations=channel_activations,
        region_analysis=region_analysis,
        situation=situation,
    )

    return _assemble_result(
        region_analysis=region_analysis,
        channel_activations=channel_activations,
        ch=ch,
        mixed_fusion=mixed_fusion,
        ownership_evidence=ownership_evidence,
        ownership_layer={
            "region_discovery": owner_analysis,
            "occlusion_graph": occlusion_graph,
            "text_owner_assignment": text_assignment,
        },
    )


def _assemble_result(
    *,
    region_analysis: Dict[str, Any],
    channel_activations: Dict[str, Any],
    ch: Dict[str, Any],
    mixed_fusion: Dict[str, Any],
    ownership_evidence: Optional[Dict[str, Any]],
    ownership_layer: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    return {
        "layer": "region_intelligence",
        "region_analysis": region_analysis,
        "channel_activation": channel_activations,
        "ownership_layer": ownership_layer,
        "channels": {
            "ownership_channel": {
                "capability": "understand_region_ownership",
                "enabled": ownership_evidence is not None,
                "evidence": ownership_evidence or {},
            },
            "text_channel": {
                "capability": "understand_region_text",
                "evidence": ch["text_evidence"],
                "runtime_result": ch.get("text_path_result"),
            },
            "visual_channel": {
                "capability": "understand_region_visual",
                "evidence": ch["visual_evidence"],
            },
            "spatial_channel": {
                "capability": "understand_region_layout",
                "evidence": ch["spatial_evidence"],
            },
            "context_channel": {
                "capability": "understand_region_context",
                "evidence": ch["context_evidence"],
            },
        },
        "fusion": mixed_fusion,
        "text_path": {
            "text_evidence": ch["text_evidence"],
            "runtime_result": ch.get("text_path_result"),
        },
        "visual_path": {"visual_evidence": ch["visual_evidence"]},
        "fusion_slot": {"mixed_evidence": mixed_fusion},
        "dual_path_not_competition": True,
        "five_channel_with_ownership": ownership_evidence is not None,
        "region_intelligence_layer": True,
        "not_ocr_extension": True,
        "candidate_only": True,
        "not_fact": True,
    }


run_mixed_region_understanding = run_region_intelligence

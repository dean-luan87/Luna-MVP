# -*- coding: utf-8 -*-
"""Region Intelligence Ownership DryRun Adapter — governance loop v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.mixed_region.dryrun.channel_selection_v1 import (
    select_information_channels,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.dryrun.entity_discovery_simulator_v1 import (
    simulate_entity_discovery,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.dryrun.information_ownership_graph_v1 import (
    build_information_ownership_graph,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.dryrun.missing_information_reasoner_v1 import (
    reason_missing_information,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.dryrun.region_intelligence_dryrun_metrics_v1 import (
    get_ownership_dryrun_metrics,
    record_entity_discovery,
    record_handoff,
    record_missing_reasoning,
    record_selective_activation,
    record_semantic_conflict,
    reset_ownership_dryrun_metrics,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.dryrun.semantic_conflict_detector_v1 import (
    detect_semantic_conflict,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DRYRUN_BLOCKED"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _validation_review(
    *,
    ownership_graph: Dict[str, Any],
    semantic_conflict: Optional[Dict[str, Any]],
    missing_info: list,
    discovery: Dict[str, Any],
) -> Dict[str, Any]:
    if discovery.get("runtime_unavailable"):
        status = "runtime_error_acknowledged"
    elif semantic_conflict:
        status = "validation_review"
    elif missing_info:
        status = "missing_information_acknowledged"
    else:
        status = "accepted_as_ownership_graph"
    return {
        "validation_id": _uid("val"),
        "validation_status": status,
        "not_fact_admission": True,
        "candidate_only": True,
    }


def run_region_intelligence_ownership_dryrun(
    *,
    fixture_key: str,
    situation: Optional[Dict[str, Any]] = None,
    plan: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Governance loop:
    Image → Entity Discovery → Ownership Graph → Channel Selection
    → Evidence Package → Validation

    NOT: image → all models → fusion
    """
    record_entity_discovery()
    discovery = simulate_entity_discovery(fixture_key=fixture_key)
    channel_selection = select_information_channels(discovery=discovery)
    record_selective_activation(not_all_models=channel_selection.get("not_all_models_started", False))

    ownership_graph = build_information_ownership_graph(
        discovery=discovery,
        channel_selection=channel_selection,
    )
    missing_info = reason_missing_information(discovery=discovery, ownership_graph=ownership_graph)
    if missing_info:
        record_missing_reasoning()

    semantic_conflict = detect_semantic_conflict(discovery=discovery, ownership_graph=ownership_graph)
    if semantic_conflict:
        record_semantic_conflict()

    validation = _validation_review(
        ownership_graph=ownership_graph,
        semantic_conflict=semantic_conflict,
        missing_info=missing_info,
        discovery=discovery,
    )

    handoff_ok = discovery.get("discovery_status") == "ok" and bool(ownership_graph.get("entity_candidates"))
    record_handoff(success=handoff_ok)

    return {
        "dryrun_only": True,
        "fixture_key": fixture_key,
        "situation": situation or {},
        "plan": plan or {},
        "entity_discovery": discovery,
        "channel_selection": channel_selection,
        "evidence_package": {
            "entity_candidates": ownership_graph.get("entity_candidates"),
            "relation_candidates": ownership_graph.get("relation_candidates"),
            "missing_information_candidates": missing_info,
            "semantic_conflict_candidate": semantic_conflict,
        },
        "ownership_graph": ownership_graph,
        "validation_review": validation,
        "ownership_first": channel_selection.get("ownership_before_ocr"),
        "not_global_model_activation": channel_selection.get("not_all_models_started"),
        "not_all_models_fusion": True,
        "governance_loop_complete": True,
        "dryrun_metrics": get_ownership_dryrun_metrics(),
        "candidate_only": True,
        "not_fact": True,
    }

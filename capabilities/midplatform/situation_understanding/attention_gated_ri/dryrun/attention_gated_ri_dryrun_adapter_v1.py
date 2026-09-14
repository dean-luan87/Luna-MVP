# -*- coding: utf-8 -*-
"""Attention-Gated Region Intelligence DryRun Adapter — governance loop v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.situation_understanding.attention_allocation.l0_observation_scan_v1 import (
    run_l0_observation_scan,
)
from capabilities.midplatform.situation_understanding.attention_gated_ri.dryrun.attention_gate_v1 import (
    apply_attention_gate,
)
from capabilities.midplatform.situation_understanding.attention_gated_ri.dryrun.attention_gated_ri_dryrun_metrics_v1 import (
    get_attention_gated_ri_dryrun_metrics,
    record_efficiency_computed,
    record_gate_applied,
    record_scene_graph_merged,
)
from capabilities.midplatform.situation_understanding.attention_gated_ri.dryrun.gated_region_intelligence_v1 import (
    run_gated_region_intelligence,
)
from capabilities.midplatform.situation_understanding.attention_gated_ri.dryrun.information_efficiency_score_v1 import (
    compute_information_efficiency,
)
from capabilities.midplatform.situation_understanding.attention_gated_ri.dryrun.observation_priority_graph_v1 import (
    build_observation_priority_graph,
)
from capabilities.midplatform.situation_understanding.attention_gated_ri.dryrun.scene_graph_merger_v1 import (
    merge_scene_graph,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_BLOCKED"

TRADITIONAL_BASELINE_REGIONS = 100


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _validation_review(
    *,
    gate: Dict[str, Any],
    gated_ri: Dict[str, Any],
    efficiency: Dict[str, Any],
) -> Dict[str, Any]:
    if gate.get("attention_gates_region_intelligence") and gated_ri.get("blocked_region_count", 0) > 0:
        status = "attention_gate_verified"
    elif gated_ri.get("activated_region_count", 0) > 0:
        status = "accepted_as_gated_evidence"
    else:
        status = "validation_review"
    return {
        "validation_id": _uid("val"),
        "validation_status": status,
        "not_fact_admission": True,
        "candidate_only": True,
        "attention_is_control_system": gate.get("attention_gates_region_intelligence") is True,
    }


def run_attention_gated_ri_dryrun(
    *,
    scan_fixture: str = "subway_platform",
    goal_type: str = "find_subway_exit",
    situation: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Governance loop:
    Image → L0 Scan → Situation → Attention Budget → Region Selection
    → Ownership / Channel Activation → Evidence → Validation

    NOT: Attention outputs priority but all RI still executes
    """
    l0_scan = run_l0_observation_scan(fixture_key=scan_fixture)
    gate = apply_attention_gate(l0_scan=l0_scan, goal_type=goal_type)

    blocked = gate.get("blocked_regions") or []
    caps_blocked = sum(len(b.get("blocked_capabilities") or []) for b in blocked)
    record_gate_applied(blocked_count=len(blocked), capabilities_blocked=caps_blocked)

    budget = gate.get("observation_budget") or {}
    priority_graph = build_observation_priority_graph(
        l0_scan=l0_scan,
        goal_type=goal_type,
        budget=budget,
    )
    gated_ri = run_gated_region_intelligence(gate=gate)
    scene_graph = merge_scene_graph(
        priority_graph=priority_graph,
        gated_ri=gated_ri,
        gate=gate,
    )
    record_scene_graph_merged()

    efficiency = compute_information_efficiency(
        gated_ri=gated_ri,
        traditional_region_count=TRADITIONAL_BASELINE_REGIONS,
    )
    record_efficiency_computed()

    validation = _validation_review(gate=gate, gated_ri=gated_ri, efficiency=efficiency)

    return {
        "dryrun_only": True,
        "scan_fixture": scan_fixture,
        "goal_type": goal_type,
        "situation": situation or {"goal_type": goal_type},
        "l0_observation_scan": l0_scan,
        "attention_gate": gate,
        "observation_priority_graph": priority_graph,
        "gated_region_intelligence": gated_ri,
        "scene_graph": scene_graph,
        "information_efficiency": efficiency,
        "evidence_package": {
            "entity_candidates": gated_ri.get("entity_candidates"),
            "blocked_regions": blocked,
            "scene_graph_entities": scene_graph.get("entities"),
            "efficiency_score": efficiency,
        },
        "validation_review": validation,
        "attention_gates_region_intelligence": gate.get("attention_gates_region_intelligence"),
        "not_all_regions_execute": gate.get("not_all_regions_execute"),
        "model_calls_reduced": gated_ri.get("blocked_region_count", 0) > 0,
        "governance_loop_complete": True,
        "dryrun_metrics": get_attention_gated_ri_dryrun_metrics(),
        "candidate_only": True,
        "not_fact": True,
    }

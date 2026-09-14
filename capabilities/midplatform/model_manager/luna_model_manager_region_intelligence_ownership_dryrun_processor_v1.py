# -*- coding: utf-8 -*-
"""Luna Region Intelligence Ownership — dryrun processor v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.mixed_region.dryrun.region_intelligence_dryrun_metrics_v1 import (
    reset_ownership_dryrun_metrics,
)
from capabilities.midplatform.model_manager.runtime.mixed_region.dryrun.region_intelligence_ownership_dryrun_adapter_v1 import (
    run_region_intelligence_ownership_dryrun,
)


def _entity(result: Dict[str, Any], entity_id: str) -> Dict[str, Any]:
    pkg = result.get("evidence_package") or {}
    return next(
        (e for e in pkg.get("entity_candidates") or [] if e.get("entity_id") == entity_id),
        {},
    )


def run_ownership_first_stacked_menus() -> Dict[str, Any]:
    """Case A: 两张菜单重叠 — entity discovery → OCR per entity, NOT global OCR."""
    reset_ownership_dryrun_metrics()
    result = run_region_intelligence_ownership_dryrun(fixture_key="stacked_menus")
    sel = result.get("channel_selection") or {}
    disc = result.get("entity_discovery") or {}
    return {
        **result,
        "scenario": "case_a_ownership_first_stacked_menus",
        "entity_discovery_first": disc.get("ownership_first") is True,
        "two_entities": disc.get("entity_count", 0) >= 2,
        "ocr_per_entity_only": sel.get("ocr_per_entity_only") is True,
        "not_global_ocr": sel.get("not_global_ocr") is True,
        "ownership_before_ocr": sel.get("ownership_before_ocr") is True,
        "menu_a_has_text": bool(_entity(result, "menu_A").get("information_channels", {}).get("text", {}).get("candidates")),
        "menu_b_has_text": bool(_entity(result, "menu_B").get("information_channels", {}).get("text", {}).get("candidates")),
    }


def run_missing_information_occlusion() -> Dict[str, Any]:
    """Case B: paper_B 标题缺失 — reason=occluded, not assume absent."""
    reset_ownership_dryrun_metrics()
    result = run_region_intelligence_ownership_dryrun(fixture_key="stacked_papers_occlusion")
    missing = (result.get("evidence_package") or {}).get("missing_information_candidates") or []
    paper_b = _entity(result, "paper_B")
    comp = paper_b.get("completeness") or {}
    return {
        **result,
        "scenario": "case_b_missing_information_occlusion",
        "has_missing_candidate": len(missing) > 0,
        "occluded_reason": any(m.get("reason") == "occluded" for m in missing),
        "not_assume_absent": any(m.get("not_assume_absent") for m in missing),
        "completeness_not_confidence": comp.get("not_confidence") is True,
        "paper_b_completeness": comp.get("information_completeness", 0) > 0,
        "paper_a_zhangsan": any(
            "张三" in (c.get("text") or "")
            for c in _entity(result, "paper_A").get("information_channels", {}).get("text", {}).get("candidates", [])
        ),
    }


def run_channel_conflict_same_region() -> Dict[str, Any]:
    """Case C: STARBUCKS + 汽车维修 — semantic_conflict_candidate."""
    reset_ownership_dryrun_metrics()
    result = run_region_intelligence_ownership_dryrun(fixture_key="same_region_conflict")
    conflict = (result.get("evidence_package") or {}).get("semantic_conflict_candidate") or {}
    return {
        **result,
        "scenario": "case_c_channel_conflict_same_region",
        "semantic_conflict": conflict.get("type") == "semantic_conflict_candidate",
        "not_merged_answer": conflict.get("not_visual_plus_text_answer") is True,
        "need_more_evidence": conflict.get("next_action") == "need_additional_evidence",
        "validation_review": (result.get("validation_review") or {}).get("validation_status") == "validation_review",
    }


def run_selective_channel_not_all_models() -> Dict[str, Any]:
    """Case D: 货架 — selective activation, not all models start."""
    reset_ownership_dryrun_metrics()
    result = run_region_intelligence_ownership_dryrun(fixture_key="selective_channels_shelf")
    sel = result.get("channel_selection") or {}
    noop = sel.get("noop_capabilities") or []
    return {
        **result,
        "scenario": "case_d_selective_channel_not_all_models",
        "not_all_models_started": sel.get("not_all_models_started") is True,
        "noop_capabilities_exist": len(noop) > 0,
        "not_global_activation": result.get("not_global_model_activation") is True,
        "two_entities_separated": (result.get("entity_discovery") or {}).get("entity_count", 0) >= 2,
    }


def run_ownership_graph_structure() -> Dict[str, Any]:
    """Case E: 输出结构 — entity_candidates + relation_candidates."""
    reset_ownership_dryrun_metrics()
    result = run_region_intelligence_ownership_dryrun(fixture_key="stacked_papers_occlusion")
    pkg = result.get("evidence_package") or {}
    graph = result.get("ownership_graph") or {}
    relations = pkg.get("relation_candidates") or []
    return {
        **result,
        "scenario": "case_e_ownership_graph_structure",
        "has_entity_candidates": len(pkg.get("entity_candidates") or []) >= 2,
        "has_relation_candidates": len(relations) > 0,
        "occlusion_relation": any(r.get("relation") == "occlusion" for r in relations),
        "entity_has_channels": all(
            "information_channels" in e for e in pkg.get("entity_candidates") or []
        ),
        "entity_has_completeness": all(
            "completeness" in e for e in pkg.get("entity_candidates") or []
        ),
        "not_flat_structure": graph.get("not_flat_text_visual_spatial") is True,
    }


def run_runtime_unavailable_replan() -> Dict[str, Any]:
    """Case F: runtime unavailable — no silent all-model fallback."""
    reset_ownership_dryrun_metrics()
    result = run_region_intelligence_ownership_dryrun(fixture_key="runtime_unavailable")
    disc = result.get("entity_discovery") or {}
    return {
        **result,
        "scenario": "case_f_runtime_unavailable_replan",
        "runtime_unavailable": disc.get("runtime_unavailable") is True,
        "no_entity_discovery": disc.get("entity_count", 0) == 0,
        "validation_error": (result.get("validation_review") or {}).get("validation_status") == "runtime_error_acknowledged",
        "not_global_fallback": disc.get("runtime_unavailable") is True,
    }

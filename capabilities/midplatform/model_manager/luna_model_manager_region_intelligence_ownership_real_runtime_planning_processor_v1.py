# -*- coding: utf-8 -*-
"""Luna Ownership Real Runtime Integration — planning processor v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_real_runtime.planning.ownership_real_runtime_adapter_v1 import (
    run_ownership_real_runtime_planning,
)


def _entity_ids(pkg: Dict[str, Any]) -> List[str]:
    return [e.get("entity_id") for e in pkg.get("entity_candidates") or []]


def _text_owners(pkg: Dict[str, Any]) -> List[str]:
    return [t.get("owner_entity_id") for t in pkg.get("text_owner_assignments") or []]


def run_stacked_papers_per_owner_ocr() -> Dict[str, Any]:
    """Case A: 叠放纸张 — paper_A/paper_B 分离，OCR per owner."""
    result = run_ownership_real_runtime_planning(fixture_key="stacked_papers")
    pkg = result.get("evidence_package") or {}
    return {
        **result,
        "scenario": "case_a_stacked_papers_per_owner_ocr",
        "two_entities": len(_entity_ids(pkg)) >= 2,
        "has_paper_a": "paper_A" in _entity_ids(pkg),
        "has_paper_b": "paper_B" in _entity_ids(pkg),
        "per_owner_text": "paper_A" in _text_owners(pkg) and "paper_B" in _text_owners(pkg),
        "not_flat_merge": result.get("text_owner_binding") is True,
    }


def run_shelf_distinct_owners() -> Dict[str, Any]:
    """Case B: 货架 — 商品/价签/广告分属不同 owner."""
    result = run_ownership_real_runtime_planning(fixture_key="shelf_price_tags")
    pkg = result.get("evidence_package") or {}
    owners = set(_entity_ids(pkg))
    text_owners = set(_text_owners(pkg))
    return {
        **result,
        "scenario": "case_b_shelf_distinct_owners",
        "three_entities": len(owners) >= 3,
        "product_owner": "product_a" in owners,
        "price_tag_owner": "price_tag" in owners,
        "ad_owner": "bg_ad" in owners,
        "distinct_text_owners": len(text_owners) >= 3,
        "not_single_ocr_task": len(text_owners) >= 2,
    }


def run_glass_reflection_separation() -> Dict[str, Any]:
    """Case C: 玻璃反光 — 真实店招与反光分离."""
    result = run_ownership_real_runtime_planning(fixture_key="glass_reflection")
    pkg = result.get("evidence_package") or {}
    relations = pkg.get("relation_candidates") or []
    assignments = pkg.get("text_owner_assignments") or []
    return {
        **result,
        "scenario": "case_c_glass_reflection_separation",
        "real_sign": "sign_real" in _entity_ids(pkg),
        "reflection_entity": "sign_reflection" in _entity_ids(pkg),
        "reflection_relation": any(r.get("relation_type") == "reflection_of" for r in relations),
        "reflection_marked": any(a.get("reflection_artifact") for a in assignments),
    }


def run_attention_blocked_no_ownership() -> Dict[str, Any]:
    """Case D: Attention blocked 广告 — 不进入 Ownership Runtime."""
    result = run_ownership_real_runtime_planning(fixture_key="attention_blocked_ad")
    pkg = result.get("evidence_package") or {}
    blocked = pkg.get("attention_blocked_regions") or []
    return {
        **result,
        "scenario": "case_d_attention_blocked_no_ownership",
        "has_blocked_region": len(blocked) > 0,
        "bg_ad_not_in_entities": "bg_ad" not in _entity_ids(pkg),
        "bg_ad_not_in_text": "bg_ad" not in _text_owners(pkg),
        "product_still_processed": "product_a" in _entity_ids(pkg),
        "attention_gated": result.get("attention_gated_input") is True,
    }


def run_occluded_title_not_absent() -> Dict[str, Any]:
    """Case E: 遮挡标题 — reason=occluded，非不存在."""
    result = run_ownership_real_runtime_planning(fixture_key="occluded_title")
    pkg = result.get("evidence_package") or {}
    missing = pkg.get("missing_information_candidates") or []
    return {
        **result,
        "scenario": "case_e_occluded_title_not_absent",
        "has_missing_candidate": len(missing) > 0,
        "occluded_reason": any(m.get("reason") == "occluded" for m in missing),
        "not_assume_absent": any(m.get("not_assume_absent") for m in missing),
        "paper_b_owner_exists": "paper_B" in _entity_ids(pkg),
    }


def run_runtime_unavailable_no_fallback() -> Dict[str, Any]:
    """Case F: Runtime 故障 — error candidate，禁止全图 OCR fallback."""
    result = run_ownership_real_runtime_planning(fixture_key="runtime_unavailable")
    err = result.get("ownership_runtime_error_candidate") or {}
    return {
        **result,
        "scenario": "case_f_runtime_unavailable_no_fallback",
        "runtime_error": err.get("error_type") == "ownership_runtime_unavailable",
        "replan_target": err.get("replan_target") == "L2_or_Attention_replan",
        "no_full_ocr_fallback": result.get("not_full_image_ocr_fallback") is True,
        "no_evidence_package": result.get("evidence_package") is None,
    }

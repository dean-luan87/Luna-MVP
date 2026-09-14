# -*- coding: utf-8 -*-
"""Luna Ownership Real Runtime Integration — dryrun processor v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_runtime.dryrun.ownership_runtime_dryrun_adapter_v1 import (
    run_ownership_runtime_dryrun,
)


def _pkg(result: Dict[str, Any]) -> Dict[str, Any]:
    return result.get("ownership_evidence_package") or {}


def _entity_ids(pkg: Dict[str, Any]) -> List[str]:
    return [e.get("entity_id") for e in pkg.get("entity_candidates") or []]


def _text_owners(pkg: Dict[str, Any]) -> List[str]:
    return [t.get("owner_entity_id") for t in pkg.get("text_owner_assignments") or []]


def run_stacked_papers() -> Dict[str, Any]:
    """Case A: paper_A / paper_B 分离，不平铺合并."""
    result = run_ownership_runtime_dryrun(fixture_key="stacked_papers")
    pkg = _pkg(result)
    assignments = pkg.get("text_owner_assignments") or []
    owners = set(_text_owners(pkg))
    return {
        **result,
        "scenario": "case_a_stacked_papers",
        "paper_a": "paper_A" in _entity_ids(pkg),
        "paper_b": "paper_B" in _entity_ids(pkg),
        "per_owner_assignments": "paper_A" in owners and "paper_B" in owners,
        "no_flat_merge": len(owners) >= 2,
        "owner_required": all(a.get("owner_entity_id") for a in assignments),
    }


def run_shelf_price_tags() -> Dict[str, Any]:
    """Case B: product / price_tag / bg_ad 三类 owner 分离."""
    result = run_ownership_runtime_dryrun(fixture_key="shelf_price_tags")
    pkg = _pkg(result)
    entities = set(_entity_ids(pkg))
    return {
        **result,
        "scenario": "case_b_shelf_price_tags",
        "product": "product_a" in entities,
        "price_tag": "price_tag" in entities,
        "bg_ad": "bg_ad" in entities,
        "three_owners": len(entities) >= 3,
        "distinct_text_owners": len(set(_text_owners(pkg))) >= 3,
    }


def run_glass_reflection() -> Dict[str, Any]:
    """Case C: real_sign vs reflected_text 分离，relation=reflection_of."""
    result = run_ownership_runtime_dryrun(fixture_key="glass_reflection")
    pkg = _pkg(result)
    relations = pkg.get("relation_candidates") or []
    assignments = pkg.get("text_owner_assignments") or []
    reflection_entry = next((a for a in assignments if a.get("reflection_artifact")), {})
    return {
        **result,
        "scenario": "case_c_glass_reflection",
        "real_sign": "sign_real" in _entity_ids(pkg),
        "reflection_entity": "sign_reflection" in _entity_ids(pkg),
        "reflection_relation": any(r.get("relation_type") == "reflection_of" for r in relations),
        "reflection_not_real_sign": reflection_entry.get("owner_entity_id") == "sign_reflection",
        "reflection_marked": reflection_entry.get("reflection_artifact") is True,
    }


def run_attention_blocked() -> Dict[str, Any]:
    """Case D: bg_ad 被 gate block，不进入 ownership slots."""
    result = run_ownership_runtime_dryrun(fixture_key="attention_blocked_ad")
    pkg = _pkg(result)
    blocked = pkg.get("attention_blocked_regions") or []
    return {
        **result,
        "scenario": "case_d_attention_blocked",
        "has_blocked": len(blocked) > 0,
        "bg_ad_not_entity": "bg_ad" not in _entity_ids(pkg),
        "bg_ad_not_text": "bg_ad" not in _text_owners(pkg),
        "product_processed": "product_a" in _entity_ids(pkg),
    }


def run_occluded_missing() -> Dict[str, Any]:
    """Case E: missing_reason=occluded，禁止推断没有标题."""
    result = run_ownership_runtime_dryrun(fixture_key="occluded_title")
    pkg = _pkg(result)
    missing = pkg.get("missing_information_candidates") or []
    return {
        **result,
        "scenario": "case_e_occluded_missing",
        "has_missing": len(missing) > 0,
        "occluded_reason": any(m.get("reason") == "occluded" for m in missing),
        "not_assume_absent": any(m.get("not_assume_absent") for m in missing),
        "paper_b_exists": "paper_B" in _entity_ids(pkg),
    }


def run_runtime_failure() -> Dict[str, Any]:
    """Case F: runtime_error_candidate，禁止全图 OCR fallback."""
    result = run_ownership_runtime_dryrun(fixture_key="runtime_unavailable")
    err = result.get("ownership_runtime_error_candidate") or {}
    return {
        **result,
        "scenario": "case_f_runtime_failure",
        "runtime_error": err.get("error_type") == "ownership_runtime_unavailable",
        "replan": err.get("replan_target") == "L2_or_Attention_replan",
        "no_fallback": result.get("runtime_error_no_silent_fallback") is True,
        "no_global_ocr": result.get("no_global_ocr") is True,
        "no_evidence": result.get("ownership_evidence_package") is None,
    }

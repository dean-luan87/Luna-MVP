# -*- coding: utf-8 -*-
"""Luna Lightweight Vision Runtime — planning processor v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.mixed_region.lightweight_vision.planning.lightweight_vision_planning_adapter_v1 import (
    run_lightweight_vision_runtime_planning,
)


def _pkg(result: Dict[str, Any]) -> Dict[str, Any]:
    return result.get("lightweight_vision_evidence_package") or {}


def _entity_ids(pkg: Dict[str, Any]) -> List[str]:
    return [e.get("entity_id") for e in pkg.get("entity_candidates") or []]


def _runtime_ids(pkg: Dict[str, Any]) -> List[str]:
    return [r.get("runtime_id") for r in pkg.get("runtime_candidates") or []]


def run_stacked_documents_occlusion() -> Dict[str, Any]:
    """Case A: document_surface paper_A/B + occlusion_relation."""
    result = run_lightweight_vision_runtime_planning(fixture_key="stacked_papers")
    pkg = _pkg(result)
    relations = pkg.get("relation_candidates") or []
    return {
        **result,
        "scenario": "case_a_stacked_documents_occlusion",
        "doc_runtime": "document_surface_detector_v1" in _runtime_ids(pkg),
        "paper_a": "paper_A" in _entity_ids(pkg),
        "paper_b": "paper_B" in _entity_ids(pkg),
        "occlusion": any(r.get("relation_type") == "occludes" for r in relations),
        "occlusion_runtime": "overlap_occlusion_detector_v1" in _runtime_ids(pkg),
    }


def run_shelf_price_tag_separation() -> Dict[str, Any]:
    """Case B: price_tag 与 product 分离，价签不绑定商品包装."""
    result = run_lightweight_vision_runtime_planning(fixture_key="shelf_price_tags")
    pkg = _pkg(result)
    entities = pkg.get("entity_candidates") or []
    price_tag = next((e for e in entities if e.get("entity_id") == "price_tag"), {})
    return {
        **result,
        "scenario": "case_b_shelf_price_tag_separation",
        "price_runtime": "price_tag_detector_v1" in _runtime_ids(pkg),
        "price_tag_entity": "price_tag" in _entity_ids(pkg),
        "product_entity": "product_a" in _entity_ids(pkg),
        "not_bound_to_package": price_tag.get("not_bound_to_product_package") is True,
    }


def run_screen_surface_split() -> Dict[str, Any]:
    """Case C: device_surface vs screen_content 分离."""
    result = run_lightweight_vision_runtime_planning(fixture_key="device_screen")
    pkg = _pkg(result)
    return {
        **result,
        "scenario": "case_c_screen_surface_split",
        "screen_runtime": "screen_surface_detector_v1" in _runtime_ids(pkg),
        "device": "phone_device" in _entity_ids(pkg),
        "screen": "phone_screen" in _entity_ids(pkg),
        "both_present": "phone_device" in _entity_ids(pkg) and "phone_screen" in _entity_ids(pkg),
    }


def run_reflection_not_real_sign() -> Dict[str, Any]:
    """Case D: reflection_detector 标记 reflected_text，非真实店招."""
    result = run_lightweight_vision_runtime_planning(fixture_key="glass_reflection")
    pkg = _pkg(result)
    entities = pkg.get("entity_candidates") or []
    reflection = next((e for e in entities if e.get("entity_id") == "sign_reflection"), {})
    return {
        **result,
        "scenario": "case_d_reflection_not_real_sign",
        "reflection_runtime": "reflection_detector_v1" in _runtime_ids(pkg),
        "real_sign": "sign_real" in _entity_ids(pkg),
        "reflection_entity": "sign_reflection" in _entity_ids(pkg),
        "not_real_sign": reflection.get("not_real_sign") is True,
        "reflected_text": reflection.get("reflected_text") is True,
    }


def run_attention_blocked_no_runtime() -> Dict[str, Any]:
    """Case E: Attention blocked 区域不调用 lightweight runtime."""
    result = run_lightweight_vision_runtime_planning(fixture_key="attention_blocked")
    return {
        **result,
        "scenario": "case_e_attention_blocked_no_runtime",
        "no_runtimes": len(result.get("selected_runtime_ids") or []) == 0,
        "empty_entities": len(_entity_ids(_pkg(result))) == 0,
        "attention_gate_required": result.get("attention_gate_required") is True,
    }


def run_runtime_unavailable_replan() -> Dict[str, Any]:
    """Case F: runtime_error_candidate → L2/Attention replan."""
    result = run_lightweight_vision_runtime_planning(fixture_key="runtime_unavailable")
    err = result.get("runtime_error_candidate") or {}
    return {
        **result,
        "scenario": "case_f_runtime_unavailable_replan",
        "runtime_error": err.get("error_type") == "lightweight_vision_runtime_unavailable",
        "replan": err.get("replan_target") == "L2_or_Attention_replan",
        "no_fallback": result.get("not_silent_fallback") is True,
        "no_evidence": result.get("lightweight_vision_evidence_package") is None,
    }


def run_layout_multi_block() -> Dict[str, Any]:
    """Case G: layout title/body/image/table，禁止直接文本合并."""
    result = run_lightweight_vision_runtime_planning(fixture_key="document_layout")
    pkg = _pkg(result)
    layouts = pkg.get("layout_region_candidates") or []
    block_types = {b.get("layout_type_candidate") for b in layouts}
    return {
        **result,
        "scenario": "case_g_layout_multi_block",
        "layout_runtime": "layout_detector_v1" in _runtime_ids(pkg),
        "has_title": "title" in block_types,
        "has_body": "body" in block_types,
        "has_table": "table" in block_types,
        "not_flat_merge": all(b.get("not_flat_text_merge") for b in layouts),
    }


def run_runtime_conflict_validation() -> Dict[str, Any]:
    """Case H: document vs layout 冲突 → validation_review."""
    result = run_lightweight_vision_runtime_planning(fixture_key="model_conflict")
    return {
        **result,
        "scenario": "case_h_runtime_conflict_validation",
        "conflict_detected": (result.get("runtime_execution") or {}).get("runtime_conflict_detected") is True,
        "validation_review": result.get("validation_status_candidate") == "validation_review",
        "not_auto_pick_high_conf": result.get("validation_status_candidate") != "accepted",
    }

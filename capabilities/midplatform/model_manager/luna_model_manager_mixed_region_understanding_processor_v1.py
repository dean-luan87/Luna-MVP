# -*- coding: utf-8 -*-
"""Luna Model Manager Mixed Region Understanding — planning processor v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.mixed_region.mixed_region_understanding_adapter_v1 import (
    run_region_intelligence,
)
from capabilities.midplatform.model_manager.runtime.text_recognition.text_recognition_runtime_metrics_v1 import (
    reset_ocr_runtime_metrics,
)


def _situation(scene_type: str) -> Dict[str, Any]:
    return {"scene_profile_candidate": {"scene_type": scene_type}, "candidate_only": True}


def _plan() -> Dict[str, Any]:
    return {
        "plan_goal_candidate": {"goal_type": "understand_region"},
        "collaboration_plan": {
            "slot_1": "text_detection",
            "slot_2": "region_intelligence",
            "slot_3": "evidence_fusion",
        },
        "candidate_only": True,
    }


def _region(region_id: str = "region_001") -> Dict[str, Any]:
    return {
        "evidence_id": "ev_region_upstream",
        "evidence_type": "region_candidate",
        "regions": [{"region_id": region_id, "bbox": [120, 80, 340, 160], "confidence": 0.91}],
        "region_ids": [region_id],
        "candidate_only": True,
    }


def run_shopfront_information_slots() -> Dict[str, Any]:
    """Case A: 店招 — information slots text + visual_symbol + style."""
    reset_ocr_runtime_metrics()
    result = run_region_intelligence(
        situation=_situation("shopfront_sign"),
        plan=_plan(),
        region_evidence=_region(),
        region_profile="shopfront_mixed",
        ocr_fixture_key="shopfront_ashu",
        visual_fixture_key="shopfront_occlusion",
    )
    analysis = result.get("region_analysis") or {}
    activation = result.get("channel_activation") or {}
    slots = set(analysis.get("information_slots") or [])
    return {
        **result,
        "scenario": "case_a_shopfront_information_slots",
        "mixed_business_sign": analysis.get("region_type_candidate") == "mixed_business_sign",
        "has_text_slot": "text" in slots,
        "has_visual_slot": "visual_symbol" in slots,
        "multi_slot_activation": len(activation.get("channel_activations") or []) >= 3,
        "not_single_ocr_task": analysis.get("not_recognizer") is True,
    }


def run_metro_multi_channel() -> Dict[str, Any]:
    """Case B: 地铁 — text + direction_symbol + layout_relation + spatial."""
    reset_ocr_runtime_metrics()
    result = run_region_intelligence(
        situation=_situation("subway_platform"),
        plan=_plan(),
        region_evidence=_region(),
        region_profile="metro_mixed",
        ocr_fixture_key="metro_jiahui_direction",
        visual_fixture_key="metro_direction",
        spatial_fixture_key="metro_direction",
        ocr_scenario="metro_direction",
    )
    analysis = result.get("region_analysis") or {}
    spatial = (result.get("channels") or {}).get("spatial_channel", {}).get("evidence") or {}
    return {
        **result,
        "scenario": "case_b_metro_multi_channel",
        "transit_sign": analysis.get("region_type_candidate") == "transit_direction_sign",
        "has_layout_slot": "layout_relation" in (analysis.get("information_slots") or []),
        "spatial_evidence": len(spatial.get("spatial_hints") or []) > 0,
        "direction_in_spatial": "arrow" in str(spatial.get("spatial_hints") or []).lower(),
    }


def run_occlusion_visual_supplement() -> Dict[str, Any]:
    """Case F: 遮挡 — Visual 补语义不补文字."""
    reset_ocr_runtime_metrics()
    result = run_region_intelligence(
        situation=_situation("shopfront_sign"),
        plan=_plan(),
        region_evidence=_region(),
        region_profile="shopfront_occlusion",
        ocr_fixture_key="damaged_text",
        visual_fixture_key="shopfront_occlusion",
    )
    fusion = result.get("fusion") or {}
    comp = fusion.get("evidence_completeness") or {}
    return {
        **result,
        "scenario": "case_f_occlusion_visual_supplement",
        "visual_supplements": fusion.get("visual_supplements_damaged_text") is True,
        "not_text_completion": fusion.get("not_text_completion") is True,
        "has_completeness": comp.get("is_coverage_not_probability") is True,
        "visual_higher_than_text": (comp.get("visual_completeness") or 0) > (comp.get("text_completeness") or 0),
    }


def run_text_visual_conflict() -> Dict[str, Any]:
    """Case G: STARBUCKS vs 汽车维修 — validation_review."""
    reset_ocr_runtime_metrics()
    result = run_region_intelligence(
        situation=_situation("advertisement"),
        plan=_plan(),
        region_evidence=_region(),
        region_profile="logo_mixed",
        ocr_fixture_key="starbucks_text",
        visual_fixture_key="starbucks_conflict",
    )
    fusion = result.get("fusion") or {}
    return {
        **result,
        "scenario": "case_g_text_visual_conflict",
        "conflict": fusion.get("conflict") is True,
        "validation_review": fusion.get("next_action") == "validation_review",
        "not_answer_merge": fusion.get("not_answer_merge") is True,
    }


def run_artistic_text_visual_gap() -> Dict[str, Any]:
    """Case H: 艺术字 — Visual 补充 OCR 缺口."""
    reset_ocr_runtime_metrics()
    result = run_region_intelligence(
        situation=_situation("shopfront_sign"),
        plan=_plan(),
        region_evidence=_region(),
        region_profile="artistic_text",
        ocr_fixture_key="artistic_hotpot_fail",
        visual_fixture_key="hotpot_artistic",
    )
    fusion = result.get("fusion") or {}
    return {
        **result,
        "scenario": "case_h_artistic_text_visual_gap",
        "visual_supplements_gap": fusion.get("visual_supplements_ocr_gap") is True,
        "not_vlm_replaces_ocr": fusion.get("not_vlm_replaces_ocr") is True,
    }


def run_logo_only_no_text_fact() -> Dict[str, Any]:
    """Case I: 仅 Logo — Visual exists, Text missing, 禁止文字事实."""
    reset_ocr_runtime_metrics()
    result = run_region_intelligence(
        situation=_situation("brand_signage"),
        plan=_plan(),
        region_evidence=_region(),
        region_profile="logo_only",
        ocr_fixture_key="artistic_hotpot_fail",
        visual_fixture_key="logo_only",
    )
    channels = result.get("channels") or {}
    fusion = result.get("fusion") or {}
    text_ev = channels.get("text_channel", {}).get("evidence") or {}
    visual_ev = channels.get("visual_channel", {}).get("evidence") or {}
    return {
        **result,
        "scenario": "case_i_logo_only_no_text_fact",
        "visual_exists": len(visual_ev.get("features") or []) > 0,
        "text_missing": fusion.get("text_missing") is True or text_ev.get("status") == "slot_not_required",
        "not_invented_text": fusion.get("not_invented_text") is True,
        "not_text_fact_from_visual": fusion.get("not_text_fact_from_visual") is True,
    }


def run_ocr_wrong_visual_support() -> Dict[str, Any]:
    """Case J: OCR Xx咖啡 错误 — Visual 支持 → request_more_evidence."""
    reset_ocr_runtime_metrics()
    result = run_region_intelligence(
        situation=_situation("coffee_shop"),
        plan=_plan(),
        region_evidence=_region(),
        region_profile="coffee_artistic_wrong",
        ocr_fixture_key="coffee_wrong_ocr",
        visual_fixture_key="coffee_storefront",
        context_fixture_key="commercial_shopfront",
    )
    text_ev = (result.get("channels") or {}).get("text_channel", {}).get("evidence") or {}
    fusion = result.get("fusion") or {}
    return {
        **result,
        "scenario": "case_j_ocr_wrong_visual_support",
        "ocr_low_confidence": (text_ev.get("confidence") or 0) < 0.5,
        "visual_support": len((result.get("channels") or {}).get("visual_channel", {}).get("evidence", {}).get("features") or []) > 0,
        "request_more_evidence": fusion.get("next_action") == "request_more_evidence",
    }


def run_multi_object_multi_slots() -> Dict[str, Any]:
    """Case K: 广告牌多对象 — multiple information slots."""
    reset_ocr_runtime_metrics()
    result = run_region_intelligence(
        situation=_situation("retail_advertisement"),
        plan=_plan(),
        region_evidence=_region(),
        region_profile="billboard_multi",
        ocr_fixture_key="shopfront_ashu",
        visual_fixture_key="billboard_multi",
        spatial_fixture_key="billboard_multi",
        context_fixture_key="retail_billboard",
    )
    analysis = result.get("region_analysis") or {}
    slots = analysis.get("information_slots") or []
    return {
        **result,
        "scenario": "case_k_multi_object_multi_slots",
        "multi_object": analysis.get("multi_object") is True,
        "slot_count_gte_4": len(slots) >= 4,
        "has_logo_slot": "logo" in slots,
        "has_price_slot": "price_number" in slots,
        "has_qr_slot": "qr_code" in slots,
        "not_one_ocr_task": len(slots) > 1,
    }


def run_stacked_documents_ownership() -> Dict[str, Any]:
    """Case L: 叠放纸张 — ownership before OCR, per-owner text, occlusion graph."""
    reset_ocr_runtime_metrics()
    result = run_region_intelligence(
        situation=_situation("desktop_documents"),
        plan=_plan(),
        region_evidence=_region(),
        ownership_profile="stacked_documents",
    )
    ownership = (result.get("channels") or {}).get("ownership_channel", {}).get("evidence") or {}
    fusion = result.get("fusion") or {}
    docs = ownership.get("per_owner_documents") or []
    paper_a = next((d for d in docs if d.get("owner_id") == "paper_001"), {})
    paper_b = next((d for d in docs if d.get("owner_id") == "paper_002"), {})
    return {
        **result,
        "scenario": "case_l_stacked_documents_ownership",
        "multi_objects": ownership.get("object_count", 0) >= 2,
        "occlusion_graph": len(ownership.get("occlusion_relation") or []) > 0,
        "each_text_has_owner": ownership.get("text_with_owners") and all(
            t.get("owner_candidate") for t in ownership.get("text_with_owners", [])
        ),
        "paper_a_zhangsan": any("张三" in (t.get("text") or "") for t in paper_a.get("text_candidates", [])),
        "paper_b_lisi": any("李四" in (t.get("text") or "") for t in paper_b.get("text_candidates", [])),
        "not_flat_merge": fusion.get("not_flat_text_merge") is True,
        "per_owner_ocr": all(d.get("ocr_per_crop") for d in docs),
    }


def run_glass_reflection_ownership() -> Dict[str, Any]:
    """Case M: 橱窗玻璃反光 — real sign vs reflection ownership."""
    reset_ocr_runtime_metrics()
    result = run_region_intelligence(
        situation=_situation("shopfront_glass"),
        plan=_plan(),
        region_evidence=_region(),
        ownership_profile="glass_reflection",
        visual_fixture_key="shopfront_occlusion",
    )
    ownership = (result.get("channels") or {}).get("ownership_channel", {}).get("evidence") or {}
    objects = ownership.get("object_candidates") or []
    texts = ownership.get("text_with_owners") or []
    return {
        **result,
        "scenario": "case_m_glass_reflection_ownership",
        "has_real_and_reflection": any(o.get("object_id") == "sign_real" for o in objects)
        and any(o.get("object_id") == "sign_reflection" for o in objects),
        "reflection_marked": any(t.get("reflection_artifact") for t in texts),
        "owners_separated": len(set(t.get("owner_candidate", {}).get("id") for t in texts)) >= 2,
        "not_merged_fact": result.get("not_fact") is True,
    }


def run_shelf_entity_separation() -> Dict[str, Any]:
    """Case N: 货架 — product / price tag / background ad separated."""
    reset_ocr_runtime_metrics()
    result = run_region_intelligence(
        situation=_situation("retail_shelf"),
        plan=_plan(),
        region_evidence=_region(),
        ownership_profile="shelf_multi_entity",
        visual_fixture_key="billboard_multi",
        spatial_fixture_key="billboard_multi",
        context_fixture_key="retail_billboard",
    )
    ownership = (result.get("channels") or {}).get("ownership_channel", {}).get("evidence") or {}
    docs = ownership.get("per_owner_documents") or []
    owner_ids = {d.get("owner_id") for d in docs}
    return {
        **result,
        "scenario": "case_n_shelf_entity_separation",
        "three_entities": ownership.get("object_count", 0) >= 3,
        "product_separated": "product_a" in owner_ids,
        "price_separated": "price_tag" in owner_ids,
        "ad_separated": "bg_ad" in owner_ids,
        "not_one_ocr_task": len(docs) >= 3,
    }

# -*- coding: utf-8 -*-
"""
MidPlatform forwarding rules v0 — design-only decision function.

Does not invoke MidPlatform or any network/runtime.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Set

ForwardingModeV0 = Literal["blocked", "evidence_only", "conditional_evidence", "eligible_text_only"]


def _has_required_top_level_refs(pack: Dict[str, Any]) -> bool:
    for k in (
        "source_image_ref",
        "source_provider_ref",
        "source_quality_gate_ref",
        "source_layout_ref",
        "source_eligibility_gate_ref",
    ):
        v = pack.get(k)
        if not isinstance(v, str) or not v.strip():
            return False
    return True


def _any_non_ocr_fact_violation(pack: Dict[str, Any], non_ocr_types: Set[str]) -> bool:
    for it in pack.get("eligible_text_evidence") or []:
        ct = str((it.get("source_refs") or {}).get("eval_content_type") or "")
        if ct in non_ocr_types and bool(it.get("should_enter_fact_text_layer")):
            return True
    return False


def _symbol_glyph_raw_text_violation(pack: Dict[str, Any]) -> bool:
    for key in ("symbol_evidence", "glyph_evidence"):
        for it in pack.get(key) or []:
            if bool(it.get("should_enter_raw_text")) or bool(it.get("should_enter_fact_text_layer")):
                return True
    return False


def decide_midplatform_forwarding_v0(
    *,
    pack: Dict[str, Any],
    validation_passed: bool,
    non_ocr_types: Set[str],
) -> Dict[str, Any]:
    """
    Returns forwarding decision + recommended midplatform_contract flags (design-only).
    """
    rationale: List[str] = []
    mode: ForwardingModeV0 = "blocked"

    if not validation_passed:
        rationale.append("validation_failed")
        return _decision(mode, rationale, pack)

    if not _has_required_top_level_refs(pack):
        rationale.append("missing_source_refs")
        return _decision("blocked", rationale, pack)

    if _any_non_ocr_fact_violation(pack, non_ocr_types):
        rationale.append("non_ocr_fact_layer_violation")
        return _decision("blocked", rationale, pack)

    if _symbol_glyph_raw_text_violation(pack):
        rationale.append("symbol_glyph_raw_or_fact_violation")
        return _decision("blocked", rationale, pack)

    ro = pack.get("reading_order") or {}
    uncertain = bool(ro.get("reading_order_uncertain"))
    global_avail = bool(ro.get("global_reading_order_available"))

    eligible = pack.get("eligible_text_evidence") or []
    conditional = pack.get("conditional_text_evidence") or []
    sym = pack.get("symbol_evidence") or []
    gly = pack.get("glyph_evidence") or []
    lay = pack.get("layout_evidence") or []
    rej = pack.get("rejected_or_uncertain_evidence") or []

    fact_candidates = pack.get("fact_text_layer_candidates") or []

    if uncertain and fact_candidates:
        rationale.append("reading_order_uncertain_with_fact_candidates")
        return _decision("blocked", rationale, pack)

    has_non_text = bool(sym or gly or lay or rej)
    has_eligible = bool(eligible)
    has_conditional = bool(conditional)

    if has_eligible and not uncertain and global_avail and fact_candidates:
        if not has_conditional and not has_non_text:
            mode = "eligible_text_only"
            rationale.append("eligible_clean_reading_order")
        elif not has_conditional:
            mode = "eligible_text_only"
            rationale.append("eligible_with_layout_symbol_but_fact_candidates_isolated")
        else:
            mode = "conditional_evidence"
            rationale.append("eligible_plus_conditional_default_to_conditional_path")
    elif has_eligible or has_conditional:
        mode = "conditional_evidence"
        rationale.append("eligible_or_conditional_without_full_fact_forwarding_guarantee")
    elif has_non_text and not has_eligible and not has_conditional:
        mode = "evidence_only"
        rationale.append("non_text_evidence_only")
    else:
        mode = "blocked"
        rationale.append("empty_evidence_pack")

    return _decision(mode, rationale, pack)


def _decision(mode: ForwardingModeV0, rationale: List[str], pack: Dict[str, Any]) -> Dict[str, Any]:
    eligible = bool(pack.get("eligible_text_evidence"))
    conditional = bool(pack.get("conditional_text_evidence"))
    if mode == "blocked":
        allowed_fwd = False
        allowed_fact = False
        review = True
    elif mode == "evidence_only":
        allowed_fwd = True
        allowed_fact = False
        review = True
    elif mode == "conditional_evidence":
        allowed_fwd = True
        allowed_fact = False
        review = True
    else:  # eligible_text_only
        allowed_fwd = True
        allowed_fact = True
        review = False

    return {
        "forwarding_mode": mode,
        "rationale": rationale,
        "midplatform_contract": {
            "allowed_to_forward_to_midplatform": allowed_fwd,
            "allowed_to_enter_fact_text_layer": allowed_fact,
            "requires_human_or_higher_layer_review": review,
            "forwarding_mode": mode,
        },
        "notes": "Design-only forwarding; not invoked by MidPlatform runtime.",
    }


def merge_forwarding_into_pack_midplatform_contract(pack: Dict[str, Any], decision: Dict[str, Any]) -> None:
    mc = pack.get("midplatform_contract")
    if not isinstance(mc, dict):
        mc = {}
    inner = decision.get("midplatform_contract") or {}
    mc.update(inner)
    pack["midplatform_contract"] = mc

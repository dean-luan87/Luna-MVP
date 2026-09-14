# -*- coding: utf-8 -*-
"""
OcrEvidencePackV0 — design contract schema + builder from Evaluation Tools routing pack.

No runtime, no MidPlatform calls.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from capabilities.ocr_bridge.ocr_evidence_types_v0 import default_source_refs_v0

OCR_EVIDENCE_PACK_VERSION = "ocr_evidence_pack_v0"


def build_ocr_evidence_pack_skeleton_v0(*, pack_id: str, source_refs: Dict[str, str]) -> Dict[str, Any]:
    """Empty structural template with conservative defaults."""
    return {
        "pack_id": pack_id,
        "pack_version": OCR_EVIDENCE_PACK_VERSION,
        "source_image_ref": source_refs.get("source_image_ref", ""),
        "source_provider_ref": source_refs.get("source_provider_ref", ""),
        "source_quality_gate_ref": source_refs.get("source_quality_gate_ref", ""),
        "source_layout_ref": source_refs.get("source_layout_ref", ""),
        "source_eligibility_gate_ref": source_refs.get("source_eligibility_gate_ref", ""),
        "eligible_text_evidence": [],
        "conditional_text_evidence": [],
        "symbol_evidence": [],
        "glyph_evidence": [],
        "layout_evidence": [],
        "rejected_or_uncertain_evidence": [],
        "fact_text_layer_candidates": [],
        "must_not_enter_fact_text_layer": [],
        "reading_order": {
            "global_reading_order_available": False,
            "global_reading_order_confidence": 0.0,
            "reading_order_uncertain": True,
            "reason": ["design_default_no_runtime_reading_order_signal"],
        },
        "uncertainty": {
            "has_uncertainty": True,
            "reasons": ["design_default_conservative"],
            "requires_preprocess": False,
            "requires_layout_branch": False,
            "requires_symbol_branch": False,
            "requires_glyph_branch": False,
            "requires_manual_review": True,
            "requires_provider_fallback": False,
        },
        "midplatform_contract": {
            "allowed_to_forward_to_midplatform": False,
            "allowed_to_enter_fact_text_layer": False,
            "requires_human_or_higher_layer_review": True,
            "forwarding_mode": "blocked",
        },
        "hard_audit": {
            "runtime_integration": False,
            "whitebox_integration": False,
            "mainline_side_effect": False,
            "mainline_routing_changed": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "navigation_action": None,
            "world_write_invoked": False,
            "hive_upload_invoked": False,
        },
    }


def _cer_to_confidence(cer: Optional[float]) -> float:
    if cer is None:
        return 0.0
    return max(0.0, min(1.0, 1.0 - float(cer)))


def _map_eligible(
    row: Dict[str, Any],
    *,
    pack_id: str,
    eligibility_gate_root: str,
    boundary_eval_root: str,
) -> Dict[str, Any]:
    cid = str(row.get("case_id") or "")
    sm = row.get("source_metrics") or {}
    refs = default_source_refs_v0(
        case_id=cid,
        content_type=str(row.get("content_type") or ""),
        evidence_route=str(row.get("evidence_route") or "eligible_text"),
        pack_id=pack_id,
        eligibility_gate_root=eligibility_gate_root,
        boundary_eval_root=boundary_eval_root,
    )
    cer = sm.get("cer")
    cer_f = float(cer) if cer is not None else None
    qg = str(sm.get("image_quality_gate") or "NO_GO")
    return {
        "evidence_id": f"eligible_{cid}",
        "evidence_type": "eligible_text",
        "text": str(row.get("ocr_raw_text") or ""),
        "bbox": [],
        "layout_group_id": f"lg_{cid}",
        "provider": "rapidocr_eval_boundary_v0",
        "confidence": _cer_to_confidence(cer_f),
        "cer_estimate": cer_f,
        "quality_gate": qg if qg in ("GO", "CONDITIONAL_GO", "NO_GO") else "NO_GO",
        "should_enter_fact_text_layer": bool(row.get("should_enter_fact_text_layer")),
        "source_candidate_ids": [cid],
        "source_refs": refs,
    }


def _map_conditional(row: Dict[str, Any], *, pack_id: str, eligibility_gate_root: str, boundary_eval_root: str) -> Dict[str, Any]:
    cid = str(row.get("case_id") or "")
    u = row.get("uncertainty") or {}
    reasons = u.get("reason") if isinstance(u.get("reason"), list) else []
    refs = default_source_refs_v0(
        case_id=cid,
        content_type=str(row.get("content_type") or ""),
        evidence_route="conditional_text",
        pack_id=pack_id,
        eligibility_gate_root=eligibility_gate_root,
        boundary_eval_root=boundary_eval_root,
    )
    return {
        "evidence_id": f"conditional_{cid}",
        "evidence_type": "conditional_text",
        "text": str(row.get("ocr_raw_text") or ""),
        "reason": [str(x) for x in reasons],
        "uncertainty_level": "high" if u.get("needs_manual_review") else "medium",
        "requires_preprocess": any("preprocess" in str(x) for x in reasons),
        "requires_layout_branch": bool(u.get("needs_layout")),
        "requires_provider_fallback": any("provider_fallback" in str(x) for x in reasons),
        "should_enter_fact_text_layer": False,
        "source_refs": refs,
    }


def _map_symbol(row: Dict[str, Any], *, pack_id: str, eligibility_gate_root: str, boundary_eval_root: str) -> Dict[str, Any]:
    cid = str(row.get("case_id") or "")
    refs = default_source_refs_v0(
        case_id=cid,
        content_type=str(row.get("content_type") or ""),
        evidence_route="symbol",
        pack_id=pack_id,
        eligibility_gate_root=eligibility_gate_root,
        boundary_eval_root=boundary_eval_root,
    )
    return {
        "evidence_id": f"symbol_{cid}",
        "evidence_type": "symbol",
        "symbol_type": "icon" if "icon" in str(row.get("content_type") or "") else "unknown",
        "bbox": [],
        "overlapping_ocr_candidate_ids": [cid],
        "should_enter_raw_text": False,
        "should_enter_fact_text_layer": False,
        "source_refs": refs,
    }


def _map_glyph(row: Dict[str, Any], *, pack_id: str, eligibility_gate_root: str, boundary_eval_root: str) -> Dict[str, Any]:
    cid = str(row.get("case_id") or "")
    ct = str(row.get("content_type") or "")
    gtype = "stylized_digit" if "digit" in ct else "artistic_text" if "artistic" in ct else "unknown"
    refs = default_source_refs_v0(
        case_id=cid,
        content_type=ct,
        evidence_route="glyph",
        pack_id=pack_id,
        eligibility_gate_root=eligibility_gate_root,
        boundary_eval_root=boundary_eval_root,
    )
    return {
        "evidence_id": f"glyph_{cid}",
        "evidence_type": "glyph",
        "glyph_type": gtype,
        "visual_hint": ct,
        "bbox": [],
        "ocr_confirmed": False,
        "requires_confirmation": True,
        "should_enter_raw_text": False,
        "should_enter_fact_text_layer": False,
        "source_refs": refs,
    }


def _map_layout(row: Dict[str, Any], *, pack_id: str, eligibility_gate_root: str, boundary_eval_root: str) -> Dict[str, Any]:
    cid = str(row.get("case_id") or "")
    ct = str(row.get("content_type") or "")
    refs = default_source_refs_v0(
        case_id=cid,
        content_type=ct,
        evidence_route="layout",
        pack_id=pack_id,
        eligibility_gate_root=eligibility_gate_root,
        boundary_eval_root=boundary_eval_root,
    )
    gtype = "poster_block" if "panel" in ct else "unknown"
    return {
        "evidence_id": f"layout_{cid}",
        "evidence_type": "layout",
        "layout_group_id": f"lg_{cid}",
        "group_type": gtype,
        "bbox": [],
        "text_evidence_ids": [],
        "symbol_evidence_ids": [],
        "glyph_evidence_ids": [],
        "reading_order_id": f"ro_{cid}",
        "group_raw_text_joined": str(row.get("ocr_raw_text") or ""),
        "group_confidence": 0.35,
        "should_enter_fact_text_layer": False,
        "source_refs": refs,
    }


def _map_rejected(row: Dict[str, Any], *, pack_id: str, eligibility_gate_root: str, boundary_eval_root: str) -> Dict[str, Any]:
    cid = str(row.get("case_id") or "")
    u = row.get("uncertainty") or {}
    refs = default_source_refs_v0(
        case_id=cid,
        content_type=str(row.get("content_type") or ""),
        evidence_route="rejected_or_uncertain",
        pack_id=pack_id,
        eligibility_gate_root=eligibility_gate_root,
        boundary_eval_root=boundary_eval_root,
    )
    rsn = u.get("reason") if isinstance(u.get("reason"), list) else []
    return {
        "evidence_id": f"rejected_{cid}",
        "evidence_type": "rejected_or_uncertain",
        "rejection_reason": ["eval_gate_reject_or_uncertain"],
        "uncertainty_reason": [str(x) for x in rsn],
        "original_text_or_candidate": str(row.get("ocr_raw_text") or ""),
        "should_enter_fact_text_layer": False,
        "source_refs": refs,
    }


def build_ocr_evidence_pack_from_eval_routing_pack_v0(
    *,
    routing_pack: Dict[str, Any],
    eligibility_gate_root: str,
    boundary_eval_root: str,
    pack_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Maps OCR-007 `ocr_evidence_routing_pack.json` rows into OcrEvidencePackV0 evidence lists.
    """
    rid = pack_id or f"ocr_pack_{uuid.uuid4().hex[:12]}"
    rpid = str(routing_pack.get("routing_pack_id") or "unknown_routing_pack")
    src_eval = str(routing_pack.get("source_eval_root") or boundary_eval_root)

    top_refs = {
        "source_image_ref": f"eval:bundle:{eligibility_gate_root}:images",
        "source_provider_ref": "eval:provider:rapidocr_boundary_v0",
        "source_quality_gate_ref": f"eval:quality_gate:{src_eval}",
        "source_layout_ref": f"eval:layout:{src_eval}",
        "source_eligibility_gate_ref": f"eval:eligibility_gate_sim:{eligibility_gate_root}:{rpid}",
    }
    pack = build_ocr_evidence_pack_skeleton_v0(pack_id=rid, source_refs=top_refs)

    for row in routing_pack.get("eligible_text_evidence") or []:
        pack["eligible_text_evidence"].append(_map_eligible(row, pack_id=rpid, eligibility_gate_root=eligibility_gate_root, boundary_eval_root=boundary_eval_root))
    for row in routing_pack.get("conditional_text_evidence") or []:
        pack["conditional_text_evidence"].append(_map_conditional(row, pack_id=rpid, eligibility_gate_root=eligibility_gate_root, boundary_eval_root=boundary_eval_root))
    for row in routing_pack.get("symbol_evidence") or []:
        pack["symbol_evidence"].append(_map_symbol(row, pack_id=rpid, eligibility_gate_root=eligibility_gate_root, boundary_eval_root=boundary_eval_root))
    for row in routing_pack.get("glyph_evidence") or []:
        pack["glyph_evidence"].append(_map_glyph(row, pack_id=rpid, eligibility_gate_root=eligibility_gate_root, boundary_eval_root=boundary_eval_root))
    for row in routing_pack.get("layout_evidence") or []:
        pack["layout_evidence"].append(_map_layout(row, pack_id=rpid, eligibility_gate_root=eligibility_gate_root, boundary_eval_root=boundary_eval_root))
    for row in routing_pack.get("rejected_or_uncertain_evidence") or []:
        pack["rejected_or_uncertain_evidence"].append(_map_rejected(row, pack_id=rpid, eligibility_gate_root=eligibility_gate_root, boundary_eval_root=boundary_eval_root))

    # Aggregate uncertainty from conditional + rejected hints
    reasons: List[str] = []
    if pack["conditional_text_evidence"]:
        reasons.append("has_conditional_text_evidence")
    if pack["rejected_or_uncertain_evidence"]:
        reasons.append("has_rejected_or_uncertain_evidence")
    pack["uncertainty"]["reasons"] = reasons or ["design_default_conservative"]
    def _cond_reasons(x: Dict[str, Any]) -> List[str]:
        u = x.get("uncertainty") or {}
        r = u.get("reason")
        return [str(s) for s in r] if isinstance(r, list) else []

    pack["uncertainty"]["requires_preprocess"] = any(
        any("preprocess" in str(r) for r in _cond_reasons(x)) for x in routing_pack.get("conditional_text_evidence") or []
    )
    pack["uncertainty"]["requires_layout_branch"] = any(bool((x.get("uncertainty") or {}).get("needs_layout")) for x in (routing_pack.get("conditional_text_evidence") or []))
    pack["uncertainty"]["requires_symbol_branch"] = bool(pack["symbol_evidence"])
    pack["uncertainty"]["requires_glyph_branch"] = bool(pack["glyph_evidence"])
    pack["uncertainty"]["requires_manual_review"] = bool(pack["rejected_or_uncertain_evidence"]) or bool(pack["conditional_text_evidence"])

    # Fact layer candidates: only when reading order is not uncertain (design v0: keep empty for eval import)
    ro_uncertain = bool((pack.get("reading_order") or {}).get("reading_order_uncertain"))
    if not ro_uncertain:
        for e in pack["eligible_text_evidence"]:
            if e.get("should_enter_fact_text_layer"):
                pack["fact_text_layer_candidates"].append(
                    {"evidence_id": e.get("evidence_id"), "text": e.get("text"), "quality_gate": e.get("quality_gate")}
                )

    must_not: List[str] = []
    for bucket in ("conditional_text_evidence", "symbol_evidence", "glyph_evidence", "layout_evidence", "rejected_or_uncertain_evidence"):
        for it in pack.get(bucket) or []:
            eid = it.get("evidence_id")
            if eid:
                must_not.append(str(eid))
    for e in pack["eligible_text_evidence"]:
        if not e.get("should_enter_fact_text_layer"):
            must_not.append(str(e.get("evidence_id")))
    pack["must_not_enter_fact_text_layer"] = must_not

    return pack


def load_non_ocr_types_from_boundary_map_v0(path: Any) -> Set[str]:
    p = Path(path)
    if not p.is_file():
        return set()
    data = json.loads(p.read_text(encoding="utf-8"))
    raw = data.get("non_ocr_content_types") or []
    return {str(x) for x in raw}

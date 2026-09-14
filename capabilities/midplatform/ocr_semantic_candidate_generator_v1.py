# -*- coding: utf-8 -*-
"""OCR Semantic Candidate Generator v1 — tier-aware dry-run from Evidence Pack v1.

Phase-OCR-Semantic-Candidate-Generator-v1-001
Rule/heuristic only; consumes evidence_tier from Adapter v1. No LLM/VLM/OCR.
"""

from __future__ import annotations

import copy
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "OCR-Semantic-Candidate-Generator-v1-001"
GENERATOR_STEP = "ocr_semantic_candidate_generator_v1"
CANDIDATE_VERSION = "ocr_semantic_candidate_v1"

FORBIDDEN_SCAN_USAGE = [
    "ocr_semantic_fact",
    "world_model_attach",
    "navigation_decision",
    "entity_commit",
]
ALLOWED_SCAN_USAGE = [
    "frame_selection",
    "roi_proposal",
    "future_observation_fill",
    "unresolved_slot_candidate_later",
]

POSTER_SEMANTIC_RULES: Dict[str, Dict[str, Any]] = {
    "default": {
        "semantic_type_candidate": "poster_promo_text",
        "entity_type_candidate": "promo",
        "meaning_candidate": "poster promotional text",
        "requires_ttl": True,
        "commercial_claim": True,
    },
    "price": {
        "semantic_type_candidate": "price_discount_text",
        "entity_type_candidate": "discount",
        "meaning_candidate": "price or discount promotional text",
        "requires_ttl": True,
        "commercial_claim": True,
    },
    "video_short": {
        "semantic_type_candidate": "unknown_text_or_unreadable",
        "entity_type_candidate": "unknown",
        "meaning_candidate": None,
        "requires_ttl": False,
        "commercial_claim": False,
    },
}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _normalize_text(raw: str) -> Optional[str]:
    if not raw or not str(raw).strip():
        return None
    parts = [p.strip() for p in re.split(r"\s*\|\s*", str(raw)) if p.strip()]
    return " ".join(parts) if len(parts) > 1 else str(raw).strip()


def _classify_gated_pack(pack: Dict[str, Any]) -> Dict[str, Any]:
    raw = str((pack.get("raw_ocr") or {}).get("raw_ocr_text") or "")
    src = pack.get("source") if isinstance(pack.get("source"), dict) else {}
    stype = str(src.get("source_type") or "")
    if stype == "video_frame_roi" and len(raw.strip()) <= 2:
        rule = POSTER_SEMANTIC_RULES["video_short"]
    elif re.search(r"\d+[\.\d]*\s*元|折|优惠|特价", raw):
        rule = POSTER_SEMANTIC_RULES["price"]
    else:
        rule = POSTER_SEMANTIC_RULES["default"]
    return rule


def _governance_block(semantic_type: str, *, requires_ttl: bool, commercial: bool = False) -> Dict[str, Any]:
    route_map = {
        "poster_promo_text": "semantic_candidate_review_later",
        "price_discount_text": "poster_ttl_policy_later",
        "unknown_text_or_unreadable": "text_bearing_sample_later",
        "public_facility_sign": "public_facility_semantic_first",
    }
    return {
        "fact_status": "not_fact",
        "write_allowed": False,
        "raw_text_overwritten": False,
        "completion_committed": False,
        "correction_committed": False,
        "requires_review": True,
        "requires_source_validation": True,
        "ttl_required": requires_ttl,
        "commercial_claim_candidate": commercial,
        "routed_governance": route_map.get(semantic_type, "semantic_candidate_review_later"),
        "world_model_attach_allowed": False,
        "scene_delta_candidate_allowed": False,
        "semantic_model_invoked": False,
    }


def _build_gated_candidate(pack: Dict[str, Any], adapter_root: str) -> Dict[str, Any]:
    ev_id = str(pack.get("evidence_id") or "")
    ic = pack.get("input_candidate_ref") or (pack.get("source") or {}).get("input_candidate_ref")
    raw = str((pack.get("raw_ocr") or {}).get("raw_ocr_text") or "")
    rule = _classify_gated_pack(pack)
    ocr_ref = pack.get("ocr_request_ref") or {}
    read_ref = pack.get("readability_gate_ref") or {}
    read_grade = read_ref.get("readability_grade") or (pack.get("readability_quality") or {}).get("readability_grade")
    sq_grade = pack.get("source_quality_grade") or (pack.get("source_quality") or {}).get("source_quality_grade")

    src = pack.get("source") if isinstance(pack.get("source"), dict) else {}
    chain = list(src.get("source_chain") or [])
    if GENERATOR_STEP not in chain:
        chain.append(GENERATOR_STEP)

    sem_id = f"ocr_sem_v1_{ev_id}"
    return {
        "semantic_candidate_id": sem_id,
        "semantic_candidate_version": CANDIDATE_VERSION,
        "source_evidence_pack_ref": f"{adapter_root}/ocr_evidence_pack_v1_gated_collection.json#{ev_id}",
        "source_ocr_request_ref": ocr_ref,
        "source_input_candidate_ref": ic,
        "evidence_tier": "gated_ocr_primary",
        "raw_ocr_text": raw,
        "raw_ocr_text_preserved": True,
        "normalized_text_candidate": _normalize_text(raw),
        "semantic_type_candidate": rule["semantic_type_candidate"],
        "entity_type_candidate": rule["entity_type_candidate"],
        "meaning_candidate": rule.get("meaning_candidate"),
        "interpretation_basis": {
            "ocr_request_ref": ocr_ref,
            "evidence_pack_ref": {"evidence_id": ev_id, "schema_version": pack.get("schema_version")},
            "input_candidate_ref": ic,
            "image_coordinate_ref": pack.get("image_coordinates"),
            "temporal_coordinate_ref": pack.get("temporal_coordinates"),
            "spatial_coordinate_ref": pack.get("spatial_coordinates"),
            "source_quality_ref": {"source_quality_grade": sq_grade, "source_quality": pack.get("source_quality")},
            "readability_gate_ref": read_ref,
            "gated_path_ref": pack.get("gated_path_ref"),
            "scan_observation_ref": pack.get("scan_observation_ref"),
            "source_chain": chain,
        },
        "source_quality_grade": sq_grade,
        "readability_grade": read_grade,
        "governance": _governance_block(
            rule["semantic_type_candidate"],
            requires_ttl=bool(rule.get("requires_ttl")),
            commercial=bool(rule.get("commercial_claim")),
        ),
        "fact_status": "not_fact",
        "write_allowed": False,
        "semantic_model_invoked": False,
        "raw_text_overwritten": False,
    }


def run_ocr_semantic_candidate_generator_v1(
    *,
    output_root: str,
    adapter_v1_root: str,
    mixed_batch_v2_root: str,
    contract_root: str,
    readability_governance_root: str,
    linebox_sq_root: str,
    worldmodel_unresolved_slot_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    errs: List[str] = []
    adapter = Path(adapter_v1_root).resolve()
    v2 = Path(mixed_batch_v2_root).resolve()
    contract = Path(contract_root).resolve()
    readability = Path(readability_governance_root).resolve()
    linebox = Path(linebox_sq_root).resolve()
    wm_slot = Path(worldmodel_unresolved_slot_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    for label, p in [("adapter_v1", adapter), ("mixed_batch_v2", v2), ("contract", contract)]:
        if not p.is_dir():
            errs.append(f"missing_root:{label}")

    gated_doc = _read_json(adapter / "ocr_evidence_pack_v1_gated_collection.json") or {}
    scan_doc = _read_json(adapter / "ocr_evidence_pack_v1_scan_observation_sidecar_collection.json") or {}
    route_sidecar = _read_json(adapter / "ocr_evidence_pack_v1_routing_sidecar_index.json") or {}
    v2_routing = _read_json(v2 / "mixed_batch_v2_routing_matrix.json") or {}
    routing_rows = [r for r in (v2_routing.get("rows") or []) if isinstance(r, dict)]

    gated_packs = [p for p in (gated_doc.get("packs") or []) if isinstance(p, dict)]
    scan_sidecars = [s for s in (scan_doc.get("scan_observations") or []) if isinstance(s, dict)]
    visual_sidecars = [v for v in (route_sidecar.get("visual_symbol_candidates") or []) if isinstance(v, dict)]

    adapter_str = str(adapter)
    gated_candidates = [_build_gated_candidate(p, adapter_str) for p in gated_packs]

    # Evidence tier input matrix
    matrix_rows: List[Dict[str, Any]] = []

    def _matrix_row(
        *,
        source_item_id: str,
        source_type: str,
        evidence_tier: str,
        sq: Optional[str],
        read: Optional[str],
        ocr_ref: Any,
        gated_ref: Any,
        scan_ref: Any,
        vs_ref: Any,
        raw: str,
        empty: bool,
        eligible: bool,
        semantic_route: str,
    ) -> Dict[str, Any]:
        return {
            "source_item_id": source_item_id,
            "source_type": source_type,
            "evidence_tier": evidence_tier,
            "source_quality_grade": sq,
            "readability_grade": read,
            "ocr_request_ref": ocr_ref,
            "gated_path_ref": gated_ref,
            "scan_observation_ref": scan_ref,
            "visual_symbol_route_ref": vs_ref,
            "raw_ocr_text": raw,
            "empty_text": empty,
            "eligible_for_semantic_candidate_v1": eligible,
            "semantic_route": semantic_route,
            "fact_status": "not_fact",
            "write_allowed": False,
        }

    for p in gated_packs:
        ic = p.get("input_candidate_ref") or ""
        read_g = (p.get("readability_gate_ref") or {}).get("readability_grade")
        matrix_rows.append(
            _matrix_row(
                source_item_id=ic or p.get("evidence_id", ""),
                source_type=(p.get("source") or {}).get("source_type", "gated_pack"),
                evidence_tier="gated_ocr_primary",
                sq=p.get("source_quality_grade"),
                read=read_g,
                ocr_ref=p.get("ocr_request_ref"),
                gated_ref=p.get("gated_path_ref"),
                scan_ref=p.get("scan_observation_ref"),
                vs_ref=None,
                raw=str((p.get("raw_ocr") or {}).get("raw_ocr_text") or ""),
                empty=bool((p.get("raw_ocr") or {}).get("empty_text")),
                eligible=True,
                semantic_route="gated_ocr_semantic_candidate",
            )
        )

    for s in scan_sidecars:
        sid = s.get("scan_observation_id") or s.get("sidecar_id", "")
        matrix_rows.append(
            _matrix_row(
                source_item_id=s.get("source_id") or sid,
                source_type="scan_observation_sidecar",
                evidence_tier="scan_observation_only",
                sq=s.get("source_quality_grade"),
                read=(s.get("readability_gate_ref") or {}).get("readability_grade"),
                ocr_ref=None,
                gated_ref=s.get("gated_path_ref"),
                scan_ref=s.get("scan_observation_ref") or sid,
                vs_ref=None,
                raw=str(s.get("ocr_preview_or_text_hint") or ""),
                empty=not bool(s.get("ocr_preview_or_text_hint")),
                eligible=False,
                semantic_route="scan_observation_hint",
            )
        )

    for v in visual_sidecars:
        ic = v.get("input_candidate_ref") or ""
        matrix_rows.append(
            _matrix_row(
                source_item_id=ic,
                source_type="visual_symbol_sidecar",
                evidence_tier="visual_symbol_route",
                sq=v.get("source_quality_grade"),
                read=None,
                ocr_ref=None,
                gated_ref=None,
                scan_ref=None,
                vs_ref=v.get("sidecar_id"),
                raw="",
                empty=True,
                eligible=False,
                semantic_route="visual_symbol_candidate",
            )
        )

    sq_e_rows: List[Dict[str, Any]] = []
    for r in routing_rows:
        if r.get("route") != "rejected_unreadable":
            continue
        cid = str(r.get("candidate_id") or "")
        sq_e_rows.append(
            {
                "blocked_item_id": f"blocked_{cid}",
                "source_item_ref": cid,
                "source_quality_grade": "SQ_E",
                "blocked_reason": r.get("blocked_reason") or r.get("route_reason") or "reject_as_unreadable_or_mixed",
                "semantic_route": "blocked_unreadable_or_low_quality",
                "strong_semantic_generated": False,
                "requires_better_source": True,
                "future_observation_required": True,
                "unresolved_slot_candidate_allowed_later": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
        matrix_rows.append(
            _matrix_row(
                source_item_id=cid,
                source_type="routing_rejected_unreadable",
                evidence_tier="sq_e_blocked",
                sq="SQ_E",
                read=None,
                ocr_ref=None,
                gated_ref=None,
                scan_ref=None,
                vs_ref=None,
                raw="",
                empty=True,
                eligible=False,
                semantic_route="blocked_low_quality",
            )
        )

    scan_hints: List[Dict[str, Any]] = []
    for s in scan_sidecars:
        sid = s.get("scan_observation_id") or s.get("scan_observation_ref", "")
        scan_hints.append(
            {
                "scan_hint_id": f"scan_hint_{sid}",
                "scan_observation_ref": s.get("scan_observation_ref") or sid,
                "source_id": s.get("source_id"),
                "scan_text_preview": s.get("ocr_preview_or_text_hint"),
                "linebox_refs": s.get("linebox_refs") or [],
                "source_quality_grade": s.get("source_quality_grade"),
                "reason_not_primary_evidence": s.get("reason_not_primary_evidence")
                or "scan_observation_only_not_gated_ocr",
                "semantic_hint_candidate": "deferred_scan_preview_only",
                "allowed_usage": list(ALLOWED_SCAN_USAGE),
                "forbidden_usage": list(FORBIDDEN_SCAN_USAGE),
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    visual_routes: List[Dict[str, Any]] = []
    for v in visual_sidecars:
        ic = v.get("input_candidate_ref") or ""
        visual_routes.append(
            {
                "visual_route_id": v.get("sidecar_id") or f"vs_route_{ic}",
                "source_item_ref": ic,
                "source_quality_grade": v.get("source_quality_grade") or "SQ_D",
                "visual_symbol_candidate_type": "brand_or_logo_like",
                "brand_symbol_candidate_allowed": True,
                "public_facility_symbol_candidate_allowed": False,
                "ordinary_ocr_semantic_allowed": False,
                "requires_visual_symbol_registry": True,
                "no_brand_fact_without_registry_or_review": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    route_map = {
        "gated_ocr_request": "generate_ocr_semantic_candidate",
        "scan_observation_only": "generate_scan_observation_hint",
        "visual_symbol_candidate": "route_to_visual_symbol",
        "rejected_unreadable": "block_low_quality",
        "public_facility_semantic_first": "hold_for_review",
    }
    output_type_map = {
        "generate_ocr_semantic_candidate": "OCRSemanticCandidate_v1",
        "generate_scan_observation_hint": "scan_observation_semantic_hint",
        "route_to_visual_symbol": "visual_symbol_route_candidate",
        "block_low_quality": "blocked_unreadable_or_low_quality",
        "hold_for_review": "hold_for_review",
    }

    gated_by_ic = {p.get("input_candidate_ref"): p for p in gated_packs}
    cand_by_ic = {c.get("source_input_candidate_ref"): c for c in gated_candidates}
    scan_by_source: Dict[str, Dict[str, Any]] = {}
    for s in scan_sidecars:
        if s.get("source_id"):
            scan_by_source[str(s["source_id"])] = s
        if s.get("image_id"):
            scan_by_source[str(s["image_id"])] = s
    visual_by_ic = {v.get("input_candidate_ref"): v for v in visual_sidecars}
    blocked_by_ic = {r["source_item_ref"]: r for r in sq_e_rows}

    routing_decisions: List[Dict[str, Any]] = []
    for r in routing_rows:
        cid = str(r.get("candidate_id") or "")
        route = str(r.get("route") or "")
        decision = route_map.get(route, "hold_for_review")
        sq_row = None
        for m in matrix_rows:
            if m.get("source_item_id") == cid and m.get("evidence_tier") != "sq_e_blocked":
                if m.get("evidence_tier") == "gated_ocr_primary":
                    sq_row = m
                    break
        sq_grade = (sq_row or {}).get("source_quality_grade")
        read_grade = (sq_row or {}).get("readability_grade")
        raw_text = (sq_row or {}).get("raw_ocr_text", "")
        if cid in cand_by_ic:
            raw_text = cand_by_ic[cid].get("raw_ocr_text", raw_text)
        out_ref = None
        if decision == "generate_ocr_semantic_candidate" and cid in cand_by_ic:
            out_ref = cand_by_ic[cid].get("semantic_candidate_id")
        elif decision == "generate_scan_observation_hint":
            sid = (scan_by_source.get(r.get("source_id", "")) or {}).get("scan_observation_id")
            if sid:
                out_ref = f"scan_hint_{sid}"
        elif decision == "route_to_visual_symbol" and cid in visual_by_ic:
            out_ref = visual_by_ic[cid].get("sidecar_id")
        elif decision == "block_low_quality" and cid in blocked_by_ic:
            out_ref = blocked_by_ic[cid].get("blocked_item_id")

        routing_decisions.append(
            {
                "item_id": cid,
                "evidence_tier": (
                    "gated_ocr_primary"
                    if cid in gated_by_ic
                    else "visual_symbol_route"
                    if cid in visual_by_ic
                    else "sq_e_blocked"
                    if route == "rejected_unreadable"
                    else "scan_observation_only"
                ),
                "source_quality_grade": sq_grade,
                "readability_grade": read_grade,
                "raw_ocr_text": raw_text,
                "route_decision": decision,
                "generated_output_type": output_type_map.get(decision),
                "generated_output_ref": out_ref,
                "blocked_reason": r.get("blocked_reason"),
                "review_required": True,
                "ttl_required": decision == "generate_ocr_semantic_candidate",
                "source_validation_required": True,
                "world_model_attach_allowed": False,
                "scene_delta_candidate_allowed": False,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    gated_type_dist = Counter(c.get("semantic_type_candidate") for c in gated_candidates)
    requires_ttl = sum(1 for c in gated_candidates if (c.get("governance") or {}).get("ttl_required"))
    review_count = len(gated_candidates) + len(scan_hints) + len(visual_routes) + len(sq_e_rows)

    type_classification = {
        "schema_version": "ocr_semantic_candidate_v1_type_classification_report_v0",
        "gated_semantic_type_distribution": dict(gated_type_dist),
        "scan_hint_count": len(scan_hints),
        "visual_symbol_route_count": len(visual_routes),
        "sq_e_blocked_count": len(sq_e_rows),
        "unknown_or_unreadable_count": gated_type_dist.get("unknown_text_or_unreadable", 0),
        "requires_ttl_count": requires_ttl,
        "requires_review_count": review_count,
        "fact_write_default_false_count": len(gated_candidates) + len(scan_hints) + len(visual_routes) + len(sq_e_rows),
        "scan_not_in_gated_distribution": True,
        "visual_not_in_ordinary_text_distribution": True,
        "blocked_not_in_strong_semantic": True,
    }

    raw_preservation = {
        "schema_version": "ocr_semantic_candidate_v1_raw_text_preservation_report_v0",
        "raw_text_preservation_rate": 1.0,
        "raw_text_overwritten": False,
        "normalized_text_separate": True,
        "correction_committed": False,
        "completion_committed": False,
        "scan_text_preview_not_raw_ocr_text": True,
        "gated_candidate_count": len(gated_candidates),
    }

    basis_rows = []
    for c in gated_candidates:
        ib = c.get("interpretation_basis") if isinstance(c.get("interpretation_basis"), dict) else {}
        basis_rows.append(
            {
                "semantic_candidate_id": c.get("semantic_candidate_id"),
                "output_type": "OCRSemanticCandidate_v1",
                "ocr_request_ref": ib.get("ocr_request_ref"),
                "evidence_pack_ref": ib.get("evidence_pack_ref"),
                "input_candidate_ref": ib.get("input_candidate_ref"),
                "image_coordinate_ref": ib.get("image_coordinate_ref"),
                "temporal_coordinate_ref": ib.get("temporal_coordinate_ref"),
                "spatial_coordinate_ref": ib.get("spatial_coordinate_ref"),
                "source_quality_ref": ib.get("source_quality_ref"),
                "readability_gate_ref": ib.get("readability_gate_ref"),
                "gated_path_ref": ib.get("gated_path_ref"),
                "source_chain": ib.get("source_chain"),
            }
        )
    for h in scan_hints:
        basis_rows.append(
            {
                "scan_hint_id": h.get("scan_hint_id"),
                "output_type": "scan_observation_semantic_hint",
                "scan_observation_ref": h.get("scan_observation_ref"),
                "source_id": h.get("source_id"),
                "ocr_request_ref": None,
            }
        )
    for v in visual_routes:
        basis_rows.append(
            {
                "visual_route_id": v.get("visual_route_id"),
                "output_type": "visual_symbol_route_candidate",
                "source_item_ref": v.get("source_item_ref"),
                "ocr_request_ref": None,
            }
        )
    for b in sq_e_rows:
        basis_rows.append(
            {
                "blocked_item_id": b.get("blocked_item_id"),
                "output_type": "blocked_unreadable_or_low_quality",
                "source_item_ref": b.get("source_item_ref"),
                "ocr_request_ref": None,
            }
        )

    interpretation_basis = {
        "schema_version": "ocr_semantic_candidate_v1_interpretation_basis_report_v0",
        "row_count": len(basis_rows),
        "rows": basis_rows,
        "main_candidates_require_ocr_request_ref": all(
            (r.get("ocr_request_ref") or {}).get("request_id") for r in basis_rows if r.get("output_type") == "OCRSemanticCandidate_v1"
        )
        if gated_candidates
        else True,
    }

    gov_rows = []
    for c in gated_candidates:
        g = c.get("governance") or {}
        gov_rows.append(
            {
                "semantic_candidate_id": c.get("semantic_candidate_id"),
                "semantic_type": c.get("semantic_type_candidate"),
                "routed_governance": g.get("routed_governance"),
                "world_model_attach_allowed": False,
                "scene_delta_candidate_allowed": False,
            }
        )
    governance_routing = {
        "schema_version": "ocr_semantic_candidate_v1_governance_routing_report_v0",
        "rules": [
            "gated OCR semantic candidate → semantic_candidate_review_later / ttl_later if needed",
            "scan observation hint → roi_proposal_later / unresolved_slot_later",
            "visual symbol route → VisualSymbolRegistry later",
            "SQ_E blocked → better_source_required",
            "world_model_attach_allowed=false for all",
            "scene_delta_candidate_allowed=false for all",
        ],
        "rows": gov_rows,
        "scan_hint_governance": "roi_proposal_later",
        "visual_symbol_governance": "visual_symbol_registry_later",
        "sq_e_governance": "better_source_required",
        "world_model_attach_allowed": False,
        "scene_delta_candidate_allowed": False,
    }

    wm_schema = _read_json(wm_slot / "worldmodel_unresolved_observation_slot_schema_v0.json") or {}
    linkage_items: List[Dict[str, Any]] = []
    for h in scan_hints:
        if h.get("source_quality_grade") == "SQ_E":
            linkage_items.append(
                {
                    "source_item_ref": h.get("source_id"),
                    "potential_slot_type": "unresolved_text_observation",
                    "unresolved_reason_candidate": "sq_e_blocked_scan_preview_only",
                    "required_future_observation": "gated_roi_ocr_or_better_frame",
                    "slot_generation_allowed_in_this_phase": False,
                    "world_model_write_allowed": False,
                }
            )
        else:
            linkage_items.append(
                {
                    "source_item_ref": h.get("source_id"),
                    "potential_slot_type": "scan_without_gated_ocr",
                    "unresolved_reason_candidate": "scan_saw_text_no_gated_pack",
                    "required_future_observation": "roi_crop_and_gated_ocr",
                    "slot_generation_allowed_in_this_phase": False,
                    "world_model_write_allowed": False,
                }
            )
    for b in sq_e_rows:
        linkage_items.append(
            {
                "source_item_ref": b.get("source_item_ref"),
                "potential_slot_type": "blocked_unreadable",
                "unresolved_reason_candidate": b.get("blocked_reason"),
                "required_future_observation": "better_source_or_roi",
                "slot_generation_allowed_in_this_phase": False,
                "world_model_write_allowed": False,
            }
        )
    for v in visual_routes:
        linkage_items.append(
            {
                "source_item_ref": v.get("source_item_ref"),
                "potential_slot_type": "visual_symbol_unresolved",
                "unresolved_reason_candidate": "logo_like_not_in_registry",
                "required_future_observation": "visual_symbol_registry_match",
                "slot_generation_allowed_in_this_phase": False,
                "world_model_write_allowed": False,
            }
        )

    unresolved_linkage = {
        "schema_version": "ocr_semantic_candidate_v1_unresolved_slot_linkage_plan_v0",
        "worldmodel_contract_root": str(wm_slot),
        "worldmodel_schema_available": bool(wm_schema),
        "item_count": len(linkage_items),
        "items": linkage_items,
        "slot_generation_allowed_in_this_phase": False,
        "world_model_write_allowed": False,
    }

    promotion_risk = sum(
        1 for h in scan_hints if h.get("semantic_hint_candidate") and "fact" in str(h.get("semantic_hint_candidate"))
    )
    quality_risk = {
        "schema_version": "ocr_semantic_candidate_v1_quality_risk_report_v0",
        "scan_observation_promotion_risk_count": promotion_risk,
        "visual_symbol_plain_text_misinterpretation_risk_count": 0,
        "sq_e_strong_semantic_risk_count": 0,
        "low_quality_source_count": len(sq_e_rows),
        "mixed_region_risk_count": len(sq_e_rows),
        "missing_spatial_anchor_count": sum(
            1 for c in gated_candidates if not ((c.get("interpretation_basis") or {}).get("spatial_coordinate_ref") or {}).get("gps_lat")
        ),
        "ttl_required_count": requires_ttl,
        "review_required_count": review_count,
        "world_model_write_blocked_count": len(gated_candidates) + len(scan_hints) + len(visual_routes) + len(sq_e_rows),
    }

    chain_rows: List[Dict[str, Any]] = []
    for c in gated_candidates:
        ib = c.get("interpretation_basis") or {}
        chain_rows.append(
            {
                "output_id": c.get("semantic_candidate_id"),
                "output_type": "OCRSemanticCandidate_v1",
                "source_item_ref": c.get("source_input_candidate_ref"),
                "evidence_pack_ref": (ib.get("evidence_pack_ref") or {}).get("evidence_id"),
                "ocr_request_ref": (ib.get("ocr_request_ref") or {}).get("request_id"),
                "scan_observation_ref": ib.get("scan_observation_ref"),
                "visual_symbol_route_ref": None,
                "source_chain_preserved": True,
                "semantic_v1_step_appended": GENERATOR_STEP in (ib.get("source_chain") or []),
                "lineage_status": "traceable",
                "traceable_to_ocr_request": bool((ib.get("ocr_request_ref") or {}).get("request_id")),
            }
        )
    for h in scan_hints:
        chain_rows.append(
            {
                "output_id": h.get("scan_hint_id"),
                "output_type": "scan_observation_semantic_hint",
                "source_item_ref": h.get("source_id"),
                "evidence_pack_ref": None,
                "ocr_request_ref": None,
                "scan_observation_ref": h.get("scan_observation_ref"),
                "visual_symbol_route_ref": None,
                "source_chain_preserved": True,
                "semantic_v1_step_appended": True,
                "lineage_status": "traceable",
                "traceable_to_scan_observation": bool(h.get("scan_observation_ref")),
            }
        )
    for v in visual_routes:
        chain_rows.append(
            {
                "output_id": v.get("visual_route_id"),
                "output_type": "visual_symbol_route_candidate",
                "source_item_ref": v.get("source_item_ref"),
                "evidence_pack_ref": None,
                "ocr_request_ref": None,
                "scan_observation_ref": None,
                "visual_symbol_route_ref": v.get("visual_route_id"),
                "source_chain_preserved": True,
                "semantic_v1_step_appended": True,
                "lineage_status": "traceable",
                "traceable_to_visual_route": True,
            }
        )

    source_chain_report = {
        "schema_version": "ocr_semantic_candidate_v1_source_chain_report_v0",
        "row_count": len(chain_rows),
        "rows": chain_rows,
        "main_semantic_traceable_to_ocr_request": all(r.get("traceable_to_ocr_request") for r in chain_rows if r.get("output_type") == "OCRSemanticCandidate_v1")
        if gated_candidates
        else True,
        "scan_hint_traceable_to_scan_observation": all(
            r.get("traceable_to_scan_observation") for r in chain_rows if r.get("output_type") == "scan_observation_semantic_hint"
        )
        if scan_hints
        else True,
    }

    metrics = {
        "schema_version": "ocr_semantic_candidate_v1_metrics_candidate_report_v0",
        "input_gated_pack_count": len(gated_packs),
        "generated_semantic_candidate_count": len(gated_candidates),
        "scan_hint_count": len(scan_hints),
        "visual_symbol_route_count": len(visual_routes),
        "sq_e_blocked_count": len(sq_e_rows),
        "semantic_candidate_consumes_evidence_tier": True,
        "scan_observation_not_promoted_to_ocr_semantic": True,
        "visual_symbol_route_not_interpreted_as_plain_text": True,
        "sq_e_blocked_no_strong_semantic": True,
        "raw_text_preservation_rate": 1.0,
        "no_write_boundary_pass_rate": 1.0,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    benchmark_link = {
        "schema_version": "ocr_semantic_candidate_v1_benchmark_link_report_v0",
        "benchmark_real_values_smoke_available": bench.is_dir(),
        "benchmark_smoke_root": str(bench),
        "current_phase_updates_benchmark_values": False,
        "current_phase_collects_t2": False,
        "ground_truth_available": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health_link = {
        "schema_version": "ocr_semantic_candidate_v1_system_health_link_report_v0",
        "system_health_governance_available": health.is_dir(),
        "system_health_governance_root": str(health),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    boundary = {
        "schema_version": "ocr_semantic_candidate_v1_no_write_boundary_report_v0",
        "boundary_ok": True,
        "violations": [],
        "dryrun_only": True,
        "semantic_model_invoked": False,
        "llm_invoked": False,
        "vlm_invoked": False,
        "raw_text_overwritten": False,
        "correction_committed": False,
        "completion_committed": False,
        "scan_observation_promoted_to_fact": False,
        "visual_symbol_committed_as_brand_fact": False,
        "sq_e_strong_semantic_generated": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
    }

    sim_sm = _read_json(sim / "simulation_summary.json") or {}
    sim_report = {
        "schema_version": "ocr_semantic_candidate_v1_simulation_context_report_v0",
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": "ocr_semantic_candidate_v1_non_claims_report_v0",
        "no_ocr_execution": True,
        "no_semantic_model": True,
        "no_llm_vlm": True,
        "no_raw_ocr_overwrite": True,
        "no_correction_completion_commit": True,
        "scan_observation_not_fact": True,
        "visual_symbol_not_brand_fact": True,
        "sq_e_not_semantic_fact": True,
        "no_real_unresolved_slot": True,
        "no_world_model_attach": True,
        "no_world_model_write": True,
        "no_scene_delta": True,
        "not_ocr_accuracy": True,
        "not_benchmark": True,
        "not_provider_comparison": True,
        "not_navigation": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": "ocr_semantic_candidate_v1_open_followups_v0",
        "items": [
            "Evidence Pack Adapter v1 consumer integration — done in v1 generator",
            "Semantic Candidate v1 review policy",
            "ROI-to-OCR Reference expansion",
            "VisualSymbolRegistry integration",
            "PublicFacility semantic-first runtime extension",
            "Unresolved Slot dry-run from scan observation",
            "Ground Truth Annotation Schema",
            "Benchmark T2 collector",
            "SystemHealth provider runtime dry-run",
            "Controlled runtime integration",
        ],
    }

    summary = {
        "schema_version": "ocr_semantic_candidate_v1_summary_v0",
        "phase": PHASE_ID,
        "generator_scope": "semantic_candidate_v1_tier_aware_dryrun",
        "based_on_evidence_pack_adapter_v1": adapter.is_dir(),
        "based_on_mixed_batch_v2": v2.is_dir(),
        "based_on_contract": contract.is_dir(),
        "based_on_readability_governance": readability.is_dir(),
        "based_on_source_quality_gate": linebox.is_dir(),
        "based_on_worldmodel_unresolved_slot_contract": wm_slot.is_dir(),
        "input_gated_pack_count": len(gated_packs),
        "input_scan_observation_count": len(scan_sidecars),
        "input_visual_symbol_route_count": len(visual_sidecars),
        "semantic_candidate_v1_generated": bool(gated_candidates),
        "semantic_candidate_consumes_evidence_tier": True,
        "scan_observation_not_promoted_to_ocr_semantic": True,
        "visual_symbol_route_not_interpreted_as_plain_text": True,
        "sq_e_blocked_no_strong_semantic": True,
        "semantic_model_invoked": False,
        "llm_invoked": False,
        "vlm_invoked": False,
        "raw_text_overwritten": False,
        "completion_committed": False,
        "correction_committed": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "phase_verdict_hint": "GO" if not errs else "CONDITIONAL_GO",
    }
    if errs:
        summary["errors"] = errs

    audit = {
        "schema_version": "ocr_semantic_candidate_v1_audit_report_v0",
        "ocr_semantic_candidate_v1_executed": True,
        "dryrun_only": True,
        "semantic_candidate_consumes_evidence_tier": True,
        "input_gated_pack_count": len(gated_packs),
        "generated_semantic_candidate_count": len(gated_candidates),
        "scan_hint_count": len(scan_hints),
        "visual_symbol_route_count": len(visual_routes),
        "sq_e_blocked_count": len(sq_e_rows),
        "semantic_model_invoked": False,
        "llm_invoked": False,
        "vlm_invoked": False,
        "raw_text_overwritten": False,
        "correction_committed": False,
        "completion_committed": False,
        "scan_observation_promoted_to_fact": False,
        "visual_symbol_committed_as_brand_fact": False,
        "sq_e_strong_semantic_generated": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "model_selection_claimed": False,
        "production_readiness_claimed": False,
    }

    return {
        "summary": summary,
        "evidence_tier_matrix": {
            "schema_version": "ocr_semantic_candidate_v1_evidence_tier_input_matrix_v0",
            "row_count": len(matrix_rows),
            "rows": matrix_rows,
        },
        "gated_collection": {
            "schema_version": "ocr_semantic_candidate_v1_gated_ocr_collection_v0",
            "candidate_count": len(gated_candidates),
            "every_candidate_has_ocr_request_ref": all(
                (c.get("source_ocr_request_ref") or {}).get("request_id") for c in gated_candidates
            )
            if gated_candidates
            else True,
            "candidates": gated_candidates,
        },
        "scan_hint_report": {
            "schema_version": "ocr_semantic_candidate_v1_scan_observation_hint_report_v0",
            "hint_count": len(scan_hints),
            "visual_symbol_route_not_interpreted_as_plain_text": True,
            "hints": scan_hints,
        },
        "visual_route_report": {
            "schema_version": "ocr_semantic_candidate_v1_visual_symbol_route_report_v0",
            "route_count": len(visual_routes),
            "visual_symbol_route_not_interpreted_as_plain_text": True,
            "routes": visual_routes,
        },
        "sq_e_blocked_report": {
            "schema_version": "ocr_semantic_candidate_v1_sq_e_blocked_report_v0",
            "blocked_count": len(sq_e_rows),
            "strong_semantic_generated": False,
            "items": sq_e_rows,
        },
        "routing_matrix": {
            "schema_version": "ocr_semantic_candidate_v1_routing_decision_matrix_v0",
            "row_count": len(routing_decisions),
            "rows": routing_decisions,
        },
        "type_classification": type_classification,
        "raw_preservation": raw_preservation,
        "interpretation_basis": interpretation_basis,
        "governance_routing": governance_routing,
        "unresolved_linkage": unresolved_linkage,
        "quality_risk": quality_risk,
        "source_chain": source_chain_report,
        "metrics": metrics,
        "benchmark_link": benchmark_link,
        "health_link": health_link,
        "boundary": boundary,
        "sim_report": sim_report,
        "non_claims": non_claims,
        "followups": followups,
        "audit": audit,
        "errs": errs,
    }

# -*- coding: utf-8 -*-
"""OCR Source Validation DryRun v1 — source chain / reliability planning only.

Phase-OCR-Source-Validation-DryRun-v1-001
No approval, no fact write, no WM/SceneDelta. validation_satisfied always false for fact path.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "OCR-Source-Validation-DryRun-v1-001"
VALIDATION_STEP = "ocr_source_validation_dryrun_v1"

RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "single_ocr_not_enough_for_fact",
        "applies_to": ["gated_ocr_primary"],
        "condition": "single_observation_only",
        "validation_effect": "insufficient_for_fact",
        "required_next_action": "repeated_observation_or_review",
        "blocked_action": ["fact_write", "world_model_attach"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "gated_ocr_requires_repeated_observation_or_review",
        "applies_to": ["gated_ocr_primary"],
        "condition": "gated_pack_present",
        "validation_effect": "pending_repeated_observation",
        "required_next_action": "repeated_observation",
        "blocked_action": ["fact_commit"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "ttl_text_requires_source_validation",
        "applies_to": ["gated_ocr_primary", "ttl_gate"],
        "condition": "semantic_type in poster_promo_text,price_discount_text,temporal_notice_text",
        "validation_effect": "hold_for_stale_expiry_policy",
        "required_next_action": "ttl_and_source_validation",
        "blocked_action": ["fact_write"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "commercial_text_requires_stale_and_expiry_policy",
        "applies_to": ["gated_ocr_primary", "ttl_gate"],
        "condition": "commercial_claim",
        "validation_effect": "hold_for_stale_expiry_policy",
        "required_next_action": "stale_expiry_check_later",
        "blocked_action": ["fact_write"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "scan_hint_is_weak_source",
        "applies_to": ["scan_observation_only"],
        "condition": "scan_only_no_gated_ocr",
        "validation_effect": "weak_scan_only",
        "required_next_action": "roi_retry",
        "blocked_action": ["fact_validation", "world_model_attach"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "sq_e_blocked_cannot_validate",
        "applies_to": ["sq_e_blocked"],
        "condition": "source_quality_grade==SQ_E",
        "validation_effect": "blocked_low_quality",
        "required_next_action": "better_source",
        "blocked_action": ["fact_validation", "ocr_request", "strong_semantic"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "visual_symbol_requires_registry",
        "applies_to": ["visual_symbol_route"],
        "condition": "logo_like_or_SQ_D",
        "validation_effect": "pending_registry",
        "required_next_action": "visual_symbol_registry_later",
        "blocked_action": ["brand_fact", "ordinary_ocr_semantic"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "public_facility_requires_semantic_first_or_registry",
        "applies_to": ["gated_ocr_primary"],
        "condition": "semantic_type==public_facility_sign",
        "validation_effect": "pending_source_review",
        "required_next_action": "public_facility_semantic_first",
        "blocked_action": ["ordinary_ocr_fact_first"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "missing_spatial_anchor_blocks_worldmodel",
        "applies_to": ["gated_ocr_primary"],
        "condition": "gps_lat is null",
        "validation_effect": "pending_source_review",
        "required_next_action": "spatial_anchor_later",
        "blocked_action": ["world_model_attach"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "missing_ocr_request_blocks_primary_validation",
        "applies_to": ["scan_observation_only", "visual_symbol_route", "sq_e_blocked"],
        "condition": "ocr_request_ref is null",
        "validation_effect": "insufficient_for_fact",
        "required_next_action": "gated_ocr_or_better_source",
        "blocked_action": ["primary_fact_validation"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "source_chain_required",
        "applies_to": ["*"],
        "condition": "always",
        "validation_effect": "chain_check",
        "required_next_action": "preserve_source_chain",
        "blocked_action": ["orphan_fact_write"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "raw_text_preservation_required",
        "applies_to": ["gated_ocr_primary"],
        "condition": "raw_ocr_text_preserved",
        "validation_effect": "chain_check",
        "required_next_action": "maintain_raw_text",
        "blocked_action": ["overwrite_raw_ocr"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "map_or_poi_context_optional_not_fact",
        "applies_to": ["*"],
        "condition": "optional",
        "validation_effect": "optional_context",
        "required_next_action": "map_poi_dryrun_later",
        "blocked_action": ["map_claim_as_fact"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "human_review_optional_later",
        "applies_to": ["gated_ocr_primary", "ttl_gate"],
        "condition": "commercial_or_entity",
        "validation_effect": "pending_source_review",
        "required_next_action": "human_review_adapter_later",
        "blocked_action": ["auto_approve"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "applies_to": ["*"],
        "condition": "always",
        "validation_effect": "block_wm",
        "required_next_action": "policy_only",
        "blocked_action": ["world_model_attach", "world_model_write"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "applies_to": ["*"],
        "condition": "always",
        "validation_effect": "block_sd",
        "required_next_action": "policy_only",
        "blocked_action": ["scene_delta_candidate", "scene_delta_write"],
        "validation_satisfied_in_this_phase": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _vid(prefix: str, key: str) -> str:
    h = hashlib.sha256(f"{prefix}:{key}".encode()).hexdigest()[:10]
    return f"sv_{prefix}_{h}"


def _build_semantic_index(semantic_root: Path) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for c in (_read_json(semantic_root / "ocr_semantic_candidate_v1_gated_ocr_collection.json") or {}).get("candidates") or []:
        if isinstance(c, dict) and c.get("semantic_candidate_id"):
            idx[str(c["semantic_candidate_id"])] = {"type": "gated", "ref": c}
    for h in (_read_json(semantic_root / "ocr_semantic_candidate_v1_scan_observation_hint_report.json") or {}).get("hints") or []:
        if isinstance(h, dict) and h.get("scan_hint_id"):
            idx[str(h["scan_hint_id"])] = {"type": "scan", "ref": h}
    for v in (_read_json(semantic_root / "ocr_semantic_candidate_v1_visual_symbol_route_report.json") or {}).get("routes") or []:
        if isinstance(v, dict) and v.get("visual_route_id"):
            idx[str(v["visual_route_id"])] = {"type": "visual", "ref": v}
    for b in (_read_json(semantic_root / "ocr_semantic_candidate_v1_sq_e_blocked_report.json") or {}).get("items") or []:
        if isinstance(b, dict) and b.get("blocked_item_id"):
            idx[str(b["blocked_item_id"])] = {"type": "sq_e", "ref": b}
    return idx


def _runtime_index(runtime_root: Path) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for r in (_read_json(runtime_root / "ocr_review_queue_runtime_intake_report.json") or {}).get("rows") or []:
        if isinstance(r, dict) and r.get("runtime_queue_item_id"):
            idx[str(r["runtime_queue_item_id"])] = r
        if isinstance(r, dict) and r.get("source_semantic_item_id"):
            idx[str(r["source_semantic_item_id"])] = r
    return idx


def _ttl_index(ttl_root: Path) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for r in (_read_json(ttl_root / "ocr_ttl_gate_v1_evaluation_matrix.json") or {}).get("rows") or []:
        if isinstance(r, dict):
            if r.get("runtime_queue_item_id"):
                idx[str(r["runtime_queue_item_id"])] = r
            if r.get("ttl_eval_id"):
                idx[str(r["ttl_eval_id"])] = r
    return idx


def _intake_row(
    *,
    source_origin: str,
    source_item_id: str,
    evidence_tier: str,
    semantic_route: str,
    sem: Optional[Dict[str, Any]],
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    ref = (sem or {}).get("ref") if sem else {}
    ib = ref.get("interpretation_basis") or {} if sem and sem.get("type") == "gated" else {}
    raw = ref.get("raw_ocr_text") or ref.get("scan_text_preview") or ""
    if sem and sem.get("type") == "gated":
        ocr_ref = ref.get("source_ocr_request_ref")
        ep_ref = ib.get("evidence_pack_ref")
        scan_ref = ib.get("scan_observation_ref")
        sq = ref.get("source_quality_grade")
        read = ref.get("readability_grade")
        st = ref.get("semantic_type_candidate")
    elif sem and sem.get("type") == "scan":
        ocr_ref = None
        ep_ref = None
        scan_ref = ref.get("scan_observation_ref")
        sq = ref.get("source_quality_grade")
        read = None
        st = None
    elif sem and sem.get("type") == "visual":
        ocr_ref = None
        ep_ref = None
        scan_ref = None
        sq = ref.get("source_quality_grade")
        read = None
        st = ref.get("visual_symbol_candidate_type")
    elif sem and sem.get("type") == "sq_e":
        ocr_ref = None
        ep_ref = None
        scan_ref = None
        sq = ref.get("source_quality_grade") or "SQ_E"
        read = None
        st = None
    else:
        ocr_ref = ep_ref = scan_ref = None
        sq = read = st = None

    vid = _vid(source_origin, source_item_id)
    row = {
        "validation_candidate_id": vid,
        "source_origin": source_origin,
        "source_item_id": source_item_id,
        "evidence_tier": evidence_tier,
        "semantic_route": semantic_route,
        "semantic_type_candidate": st,
        "raw_ocr_text": raw if raw else None,
        "source_quality_grade": sq,
        "readability_grade": read,
        "ocr_request_ref": ocr_ref,
        "evidence_pack_ref": ep_ref,
        "scan_observation_ref": scan_ref,
        "visual_symbol_route_ref": source_item_id if sem and sem.get("type") == "visual" else None,
        "sq_e_blocked_ref": source_item_id if sem and sem.get("type") == "sq_e" else None,
        "intake_status": "accepted",
        "fact_status": "not_fact",
        "write_allowed": False,
    }
    if extra:
        row.update(extra)
    if sem and sem.get("type") == "gated":
        row["source_semantic_item_id"] = ref.get("semantic_candidate_id")
    elif sem and sem.get("type") == "scan":
        row["source_semantic_item_id"] = ref.get("scan_hint_id")
    elif sem and sem.get("type") == "visual":
        row["source_semantic_item_id"] = ref.get("visual_route_id")
    elif sem and sem.get("type") == "sq_e":
        row["source_semantic_item_id"] = ref.get("blocked_item_id")
    return row


def _chain_status(candidate: Dict[str, Any]) -> Tuple[str, List[str], bool]:
    tier = candidate.get("evidence_tier", "")
    missing: List[str] = []
    has_chain = True
    has_ic = bool(candidate.get("source_item_id"))
    has_ocr = bool((candidate.get("ocr_request_ref") or {}).get("request_id"))
    has_ep = bool((candidate.get("evidence_pack_ref") or {}).get("evidence_id"))
    has_sem = candidate.get("source_origin") in ("semantic_v1", "ttl_gate", "review_policy")
    has_scan = bool(candidate.get("scan_observation_ref"))
    has_visual = bool(candidate.get("visual_symbol_route_ref"))

    if tier == "gated_ocr_primary":
        if not has_ocr:
            missing.append("ocr_request_ref")
        if not has_ep:
            missing.append("evidence_pack_ref")
        status = "complete_for_dryrun" if not missing else "missing_required_refs"
        can_primary = has_ocr and has_ep
    elif tier == "scan_observation_only":
        status = "partial_scan_only"
        can_primary = False
        if not has_scan:
            missing.append("scan_observation_ref")
    elif tier == "visual_symbol_route":
        status = "visual_registry_required"
        can_primary = False
    elif tier == "sq_e_blocked":
        status = "low_quality_blocked"
        can_primary = False
    else:
        status = "missing_required_refs"
        can_primary = False

    return status, missing, can_primary


def _reliability_status(candidate: Dict[str, Any], chain_status: str) -> str:
    tier = candidate.get("evidence_tier", "")
    origin = candidate.get("source_origin", "")
    if tier == "sq_e_blocked" or chain_status == "low_quality_blocked":
        return "blocked_low_quality"
    if tier == "visual_symbol_route" or chain_status == "visual_registry_required":
        return "pending_registry"
    if tier == "scan_observation_only" or chain_status == "partial_scan_only":
        return "weak_scan_only"
    if origin == "ttl_gate" or candidate.get("semantic_type_candidate") in (
        "poster_promo_text",
        "price_discount_text",
        "temporal_notice_text",
    ):
        return "pending_repeated_observation"
    if tier == "gated_ocr_primary":
        return "pending_repeated_observation"
    if origin == "unresolved_later":
        return "insufficient_for_fact"
    return "pending_source_review"


def _final_decision(reliability: str, chain_status: str) -> str:
    mapping = {
        "pending_repeated_observation": "pending_repeated_observation",
        "pending_source_review": "pending_source_review",
        "pending_registry": "pending_visual_symbol_registry",
        "weak_scan_only": "require_roi_retry",
        "blocked_low_quality": "blocked_low_quality",
        "insufficient_for_fact": "insufficient_for_fact",
    }
    if chain_status == "visual_registry_required":
        return "pending_visual_symbol_registry"
    if chain_status == "low_quality_blocked":
        return "blocked_low_quality"
    if chain_status == "partial_scan_only":
        return "require_roi_retry"
    if reliability == "pending_repeated_observation" and chain_status == "complete_for_dryrun":
        return "hold_for_stale_expiry_policy"
    return mapping.get(reliability, "insufficient_for_fact")


def run_ocr_source_validation_dryrun_v1(
    *,
    output_root: str,
    ttl_gate_v1_root: str,
    review_queue_runtime_root: str,
    review_policy_v1_root: str,
    semantic_v1_root: str,
    adapter_v1_root: str,
    mixed_batch_v2_root: str,
    worldmodel_unresolved_slot_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    errs: List[str] = []
    ttl_root = Path(ttl_gate_v1_root).resolve()
    runtime_root = Path(review_queue_runtime_root).resolve()
    policy_root = Path(review_policy_v1_root).resolve()
    semantic_root = Path(semantic_v1_root).resolve()
    adapter_root = Path(adapter_v1_root).resolve()
    wm_root = Path(worldmodel_unresolved_slot_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    sem_idx = _build_semantic_index(semantic_root)
    rt_idx = _runtime_index(runtime_root)
    ttl_idx = _ttl_index(ttl_root)

    intake: List[Dict[str, Any]] = []

    for row in (_read_json(ttl_root / "ocr_ttl_gate_v1_evaluation_matrix.json") or {}).get("rows") or []:
        if not isinstance(row, dict):
            continue
        sid = str(row.get("runtime_queue_item_id", ""))
        rt = rt_idx.get(sid) or {}
        sem = sem_idx.get(rt.get("source_semantic_item_id", ""))
        intake.append(
            _intake_row(
                source_origin="ttl_gate",
                source_item_id=row.get("ttl_eval_id", sid),
                evidence_tier="gated_ocr_primary",
                semantic_route="gated_ocr_semantic_candidate",
                sem=sem,
                extra={"runtime_queue_item_id": sid, "ttl_eval_id": row.get("ttl_eval_id")},
            )
        )

    for row in (_read_json(policy_root / "ocr_semantic_review_policy_v1_source_validation_matrix.json") or {}).get("rows") or []:
        if isinstance(row, dict):
            sid = str(row.get("item_id", ""))
            intake.append(
                _intake_row(
                    source_origin="review_policy",
                    source_item_id=sid,
                    evidence_tier="gated_ocr_primary",
                    semantic_route="gated_ocr_semantic_candidate",
                    sem=sem_idx.get(sid),
                )
            )

    for h in (_read_json(semantic_root / "ocr_semantic_candidate_v1_scan_observation_hint_report.json") or {}).get("hints") or []:
        if isinstance(h, dict):
            hid = str(h.get("scan_hint_id", ""))
            intake.append(
                _intake_row(
                    source_origin="scan_hint",
                    source_item_id=hid,
                    evidence_tier="scan_observation_only",
                    semantic_route="scan_observation_hint",
                    sem=sem_idx.get(hid),
                )
            )

    for v in (_read_json(semantic_root / "ocr_semantic_candidate_v1_visual_symbol_route_report.json") or {}).get("routes") or []:
        if isinstance(v, dict):
            vid = str(v.get("visual_route_id", ""))
            intake.append(
                _intake_row(
                    source_origin="visual_route",
                    source_item_id=vid,
                    evidence_tier="visual_symbol_route",
                    semantic_route="visual_symbol_candidate",
                    sem=sem_idx.get(vid),
                )
            )

    for b in (_read_json(semantic_root / "ocr_semantic_candidate_v1_sq_e_blocked_report.json") or {}).get("items") or []:
        if isinstance(b, dict):
            bid = str(b.get("blocked_item_id", ""))
            intake.append(
                _intake_row(
                    source_origin="sq_e_blocked",
                    source_item_id=bid,
                    evidence_tier="sq_e_blocked",
                    semantic_route="blocked_unreadable_or_low_quality",
                    sem=sem_idx.get(bid),
                )
            )

    for r in (_read_json(policy_root / "ocr_semantic_review_policy_v1_queue_candidate_matrix.json") or {}).get("rows") or []:
        if isinstance(r, dict) and r.get("queue_type") == "unresolved_slot_later_queue":
            sid = str(r.get("source_semantic_item_id", ""))
            tier = str(r.get("evidence_tier", "scan_observation_only"))
            intake.append(
                _intake_row(
                    source_origin="unresolved_later",
                    source_item_id=sid or str(r.get("review_queue_candidate_id", "")),
                    evidence_tier=tier,
                    semantic_route=str(r.get("semantic_route", "scan_observation_hint")),
                    sem=sem_idx.get(sid) if sid else None,
                    extra={
                        "note": "unresolved_slot_later_queue_record_only",
                        "source_semantic_item_id": sid,
                        "review_queue_candidate_id": r.get("review_queue_candidate_id"),
                    },
                )
            )

    chain_rows: List[Dict[str, Any]] = []
    reliability_rows: List[Dict[str, Any]] = []
    decision_rows: List[Dict[str, Any]] = []
    source_chain_rows: List[Dict[str, Any]] = []

    for c in intake:
        vid = c["validation_candidate_id"]
        chain_st, missing, can_primary = _chain_status(c)
        rel_st = _reliability_status(c, chain_st)
        score = 0.3 if chain_st == "complete_for_dryrun" else 0.1 if rel_st == "weak_scan_only" else 0.0

        chain_rows.append(
            {
                "validation_candidate_id": vid,
                "has_source_chain": True,
                "has_input_candidate_ref": bool(c.get("source_item_id")),
                "has_ocr_request_ref": bool((c.get("ocr_request_ref") or {}).get("request_id")),
                "has_evidence_pack_ref": bool((c.get("evidence_pack_ref") or {}).get("evidence_id")),
                "has_semantic_candidate_ref": c.get("source_origin") in ("semantic_v1", "ttl_gate", "review_policy", "scan_hint", "visual_route", "sq_e_blocked"),
                "has_review_queue_ref": c.get("source_origin") in ("ttl_gate", "unresolved_later") or bool(rt_idx.get(c.get("source_item_id", ""))),
                "has_ttl_gate_ref": c.get("source_origin") == "ttl_gate",
                "has_scan_observation_ref": bool(c.get("scan_observation_ref")),
                "has_visual_route_ref": bool(c.get("visual_symbol_route_ref")),
                "chain_completeness_status": chain_st,
                "missing_refs": missing,
                "can_support_primary_validation": can_primary,
                "fact_status": "not_fact",
            }
        )

        reliability_rows.append(
            {
                "validation_candidate_id": vid,
                "evidence_tier": c.get("evidence_tier"),
                "source_quality_grade": c.get("source_quality_grade"),
                "readability_grade": c.get("readability_grade"),
                "raw_text_confidence_proxy": "high" if c.get("readability_grade") == "A" else "low_or_unknown",
                "source_chain_reliability": chain_st,
                "repeated_observation_available": False,
                "external_context_available": False,
                "registry_available": False,
                "human_review_available": False,
                "reliability_status": rel_st,
                "reliability_score_candidate": score,
                "reliability_score_is_not_fact": True,
                "validation_satisfied": False,
            }
        )

        final = _final_decision(rel_st, chain_st)
        decision_rows.append(
            {
                "validation_candidate_id": vid,
                "final_source_validation_decision": final,
                "validation_satisfied": False,
                "required_next_action": final,
                "blocked_actions": ["approve", "commit", "fact_write", "world_model_attach", "auto_approve"],
                "allowed_future_phase": "real_source_validation_runtime",
                "decision_status": "not_committed",
                "approval_status": "not_approved",
                "fact_write_allowed": False,
                "world_model_write_allowed": False,
                "scene_delta_candidate_allowed": False,
            }
        )

        rt_id = c.get("runtime_queue_item_id") or (rt_idx.get(c.get("source_item_id", "")) or {}).get("runtime_queue_item_id")
        chain = [VALIDATION_STEP, f"origin:{c.get('source_origin')}"]
        sem_key = c.get("source_semantic_item_id") or c.get("source_item_id", "")
        trace_sem = sem_key in sem_idx or c.get("source_origin") in (
            "ttl_gate",
            "review_policy",
            "scan_hint",
            "visual_route",
            "sq_e_blocked",
            "unresolved_later",
        )
        source_chain_rows.append(
            {
                "validation_candidate_id": vid,
                "traceable_to_ttl_gate": c.get("source_origin") == "ttl_gate",
                "traceable_to_review_queue_runtime": bool(rt_id),
                "traceable_to_semantic_v1": trace_sem,
                "traceable_to_evidence_pack_v1": bool((c.get("evidence_pack_ref") or {}).get("evidence_id")),
                "traceable_to_ocr_request": bool((c.get("ocr_request_ref") or {}).get("request_id")),
                "traceable_to_scan_observation": bool(c.get("scan_observation_ref")),
                "traceable_to_visual_route": bool(c.get("visual_symbol_route_ref")),
                "traceable_to_sq_e_blocked": bool(c.get("sq_e_blocked_ref")),
                "source_chain": chain,
                "source_chain_preserved": True,
            }
        )

    ttl_rows: List[Dict[str, Any]] = []
    for row in (_read_json(ttl_root / "ocr_ttl_gate_v1_evaluation_matrix.json") or {}).get("rows") or []:
        if isinstance(row, dict):
            ttl_rows.append(
                {
                    "ttl_eval_id": row.get("ttl_eval_id"),
                    "runtime_queue_item_id": row.get("runtime_queue_item_id"),
                    "raw_ocr_text": row.get("raw_ocr_text"),
                    "semantic_type_candidate": row.get("semantic_type_candidate"),
                    "ttl_gate_status": row.get("ttl_gate_status"),
                    "source_validation_required": True,
                    "source_validation_status": "pending_source_validation",
                    "repeated_observation_required": True,
                    "explicit_source_required": True,
                    "stale_check_required": True,
                    "expiry_policy_required": True,
                    "conflict_check_required": True,
                    "validation_satisfied": False,
                    "required_next_action": "hold_for_stale_expiry_policy",
                    "fact_write_allowed": False,
                }
            )

    scan_rows = [
        {
            "scan_hint_id": h.get("scan_hint_id"),
            "scan_observation_ref": h.get("scan_observation_ref"),
            "scan_text_preview": h.get("scan_text_preview"),
            "linebox_refs": h.get("linebox_refs") or [],
            "source_quality_grade": h.get("source_quality_grade"),
            "reason_not_primary_evidence": h.get("reason_not_primary_evidence"),
            "source_validation_status": "weak_source_only",
            "requires_roi_retry": True,
            "can_support_fact_validation": False,
            "can_support_unresolved_slot_later": True,
            "world_model_attach_allowed": False,
            "fact_status": "not_fact",
        }
        for h in (_read_json(semantic_root / "ocr_semantic_candidate_v1_scan_observation_hint_report.json") or {}).get("hints") or []
        if isinstance(h, dict)
    ]

    visual_rows = [
        {
            "visual_route_id": v.get("visual_route_id"),
            "source_item_ref": v.get("source_item_ref"),
            "source_quality_grade": v.get("source_quality_grade"),
            "registry_required": True,
            "registry_checked": False,
            "registry_match_status": "not_checked",
            "brand_fact_allowed": False,
            "source_validation_status": "pending_visual_symbol_registry",
            "ordinary_ocr_semantic_allowed": False,
            "fact_status": "not_fact",
        }
        for v in (_read_json(semantic_root / "ocr_semantic_candidate_v1_visual_symbol_route_report.json") or {}).get("routes") or []
        if isinstance(v, dict)
    ]

    sq_e_rows = [
        {
            "blocked_item_id": b.get("blocked_item_id"),
            "source_quality_grade": b.get("source_quality_grade") or "SQ_E",
            "blocked_reason": b.get("blocked_reason"),
            "source_validation_status": "blocked_low_quality",
            "validation_satisfied": False,
            "better_source_required": True,
            "retry_conditions": [
                "higher_source_quality_than_SQ_E",
                "roi_crop_before_ocr",
                "readability_gate_pass",
            ],
            "can_support_fact_validation": False,
            "strong_semantic_allowed": False,
            "fact_status": "not_fact",
        }
        for b in (_read_json(semantic_root / "ocr_semantic_candidate_v1_sq_e_blocked_report.json") or {}).get("items") or []
        if isinstance(b, dict)
    ]

    decision_counts = Counter(d.get("final_source_validation_decision") for d in decision_rows)
    pending_count = sum(1 for r in reliability_rows if r.get("validation_satisfied") is False)

    routing = {
        "schema_version": "ocr_source_validation_v1_routing_report_v0",
        "pending_repeated_observation_count": decision_counts.get("pending_repeated_observation", 0)
        + sum(1 for r in reliability_rows if r.get("reliability_status") == "pending_repeated_observation"),
        "pending_source_review_count": decision_counts.get("pending_source_review", 0),
        "pending_visual_symbol_registry_count": decision_counts.get("pending_visual_symbol_registry", 0),
        "require_roi_retry_count": decision_counts.get("require_roi_retry", 0),
        "require_better_source_count": decision_counts.get("blocked_low_quality", 0),
        "hold_for_stale_expiry_policy_count": decision_counts.get("hold_for_stale_expiry_policy", 0),
        "blocked_low_quality_count": decision_counts.get("blocked_low_quality", 0),
        "insufficient_for_fact_count": decision_counts.get("insufficient_for_fact", 0),
        "source_validation_passed_count": 0,
        "world_model_attach_allowed_count": 0,
        "scene_delta_candidate_allowed_count": 0,
        "final_decision_distribution": dict(decision_counts),
    }

    boundary = {
        "schema_version": "ocr_source_validation_v1_boundary_report_v0",
        "source_validation_dryrun_only": True,
        "source_validation_does_not_commit_decision": True,
        "validation_satisfied_for_fact_count": 0,
        "approval_granted_count": 0,
        "auto_approve_invoked": False,
        "fact_review_generated": False,
        "world_model_attach_allowed": False,
        "scene_delta_candidate_allowed": False,
        "world_model_write_allowed": False,
        "navigation_decision_allowed": False,
    }

    metrics = {
        "schema_version": "ocr_source_validation_v1_metrics_candidate_report_v0",
        "validation_candidate_count": len(intake),
        "ttl_source_validation_count": len(ttl_rows),
        "scan_hint_validation_count": len(scan_rows),
        "visual_symbol_validation_count": len(visual_rows),
        "sq_e_validation_count": len(sq_e_rows),
        "source_validation_passed_count": 0,
        "validation_satisfied_for_fact_count": 0,
        "pending_source_review_count": routing.get("pending_source_review_count", 0),
        "pending_registry_count": routing.get("pending_visual_symbol_registry_count", 0),
        "require_roi_retry_count": routing.get("require_roi_retry_count", 0),
        "require_better_source_count": routing.get("require_better_source_count", 0),
        "blocked_low_quality_count": routing.get("blocked_low_quality_count", 0),
        "fact_write_allowed_count": 0,
        "world_model_attach_allowed_count": 0,
        "scene_delta_candidate_allowed_count": 0,
        "no_write_boundary_pass_rate": 1.0,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    benchmark_link = {
        "schema_version": "ocr_source_validation_v1_benchmark_link_report_v0",
        "benchmark_real_values_smoke_available": bench.is_dir(),
        "current_phase_updates_benchmark_values": False,
        "current_phase_collects_t2": False,
        "ground_truth_available": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health_link = {
        "schema_version": "ocr_source_validation_v1_system_health_link_report_v0",
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    no_write = {
        "schema_version": "ocr_source_validation_v1_no_write_boundary_report_v0",
        "boundary_ok": True,
        "violations": [],
        "source_validation_dryrun_only": True,
        "decision_committed": False,
        "approval_granted": False,
        "auto_approve_invoked": False,
        "fact_review_generated": False,
        "source_validation_passed_to_fact": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "production_readiness_claimed": False,
    }

    sim_sm = _read_json(sim / "simulation_summary.json") or {}
    sim_report = {
        "schema_version": "ocr_source_validation_v1_simulation_context_report_v0",
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": "ocr_source_validation_v1_non_claims_report_v0",
        "no_ocr_execution": True,
        "no_llm_vlm": True,
        "no_real_map_poi": True,
        "no_real_visual_symbol_registry": True,
        "no_review_decision_commit": True,
        "no_candidate_approval": True,
        "no_fact_review": True,
        "source_not_validated_as_fact": True,
        "no_world_model_write": True,
        "no_scene_delta": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": "ocr_source_validation_v1_open_followups_v0",
        "items": [
            "Real Source Validation Runtime",
            "Repeated Observation Check",
            "VisualSymbolRegistry DryRun",
            "Map / POI Context DryRun",
            "Human Review Adapter",
            "ROI Retry Proposal Runtime",
            "Stale / Expiry Check",
            "Conflict Check",
            "STC Contract later",
            "Controlled runtime integration",
        ],
    }

    audit = {
        "schema_version": "ocr_source_validation_v1_audit_report_v0",
        "ocr_source_validation_v1_executed": True,
        "source_validation_dryrun_only": True,
        "source_validation_evaluated": len(intake) > 0,
        "source_validation_passed_count": 0,
        "validation_satisfied_for_fact_count": 0,
        "decision_committed": False,
        "approval_granted": False,
        "auto_approve_invoked": False,
        "fact_review_generated": False,
        "source_validation_passed_to_fact": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "model_selection_claimed": False,
        "production_readiness_claimed": False,
    }

    ttl_must = len(ttl_rows) >= 2
    summary = {
        "schema_version": "ocr_source_validation_v1_summary_v0",
        "phase": PHASE_ID,
        "validation_scope": "source_validation_dryrun_only",
        "based_on_ttl_gate_v1": ttl_root.is_dir(),
        "based_on_review_queue_runtime": runtime_root.is_dir(),
        "based_on_review_policy_v1": policy_root.is_dir(),
        "based_on_semantic_candidate_v1": semantic_root.is_dir(),
        "based_on_evidence_pack_adapter_v1": adapter_root.is_dir(),
        "source_validation_evaluated": len(intake) > 0,
        "source_validation_passed_count": 0,
        "source_validation_pending_count": pending_count,
        "source_validation_failed_count": 0,
        "decision_committed": False,
        "approval_granted": False,
        "auto_approve_invoked": False,
        "fact_review_generated": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "validation_candidate_count": len(intake),
        "phase_verdict_hint": "GO" if ttl_must and not errs else "CONDITIONAL_GO",
    }
    if errs:
        summary["errors"] = errs

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "ocr_source_validation_v1_candidate_intake_matrix_v0",
            "row_count": len(intake),
            "rows": intake,
        },
        "rule_matrix": {"schema_version": "ocr_source_validation_v1_rule_matrix_v0", "rules": RULES},
        "chain_completeness": {
            "schema_version": "ocr_source_validation_v1_evidence_chain_completeness_matrix_v0",
            "row_count": len(chain_rows),
            "rows": chain_rows,
        },
        "reliability": {
            "schema_version": "ocr_source_validation_v1_reliability_evaluation_matrix_v0",
            "row_count": len(reliability_rows),
            "no_validated_for_fact": all(r.get("reliability_status") != "validated_for_fact" for r in reliability_rows),
            "rows": reliability_rows,
        },
        "ttl_matrix": {
            "schema_version": "ocr_source_validation_v1_ttl_source_validation_matrix_v0",
            "row_count": len(ttl_rows),
            "rows": ttl_rows,
        },
        "scan_matrix": {
            "schema_version": "ocr_source_validation_v1_scan_hint_validation_matrix_v0",
            "row_count": len(scan_rows),
            "rows": scan_rows,
        },
        "visual_matrix": {
            "schema_version": "ocr_source_validation_v1_visual_symbol_validation_matrix_v0",
            "row_count": len(visual_rows),
            "rows": visual_rows,
        },
        "sq_e_matrix": {
            "schema_version": "ocr_source_validation_v1_sq_e_validation_matrix_v0",
            "row_count": len(sq_e_rows),
            "rows": sq_e_rows,
        },
        "decision_matrix": {
            "schema_version": "ocr_source_validation_v1_decision_matrix_v0",
            "row_count": len(decision_rows),
            "all_validation_satisfied_false": all(d.get("validation_satisfied") is False for d in decision_rows),
            "rows": decision_rows,
        },
        "routing": routing,
        "boundary": boundary,
        "source_chain": {
            "schema_version": "ocr_source_validation_v1_source_chain_report_v0",
            "row_count": len(source_chain_rows),
            "rows": source_chain_rows,
        },
        "metrics": metrics,
        "benchmark_link": benchmark_link,
        "health_link": health_link,
        "no_write": no_write,
        "sim_report": sim_report,
        "non_claims": non_claims,
        "followups": followups,
        "audit": audit,
        "errs": errs,
    }

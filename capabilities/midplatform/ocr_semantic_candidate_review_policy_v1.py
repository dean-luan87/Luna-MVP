# -*- coding: utf-8 -*-
"""OCR Semantic Candidate Review Policy v1 — next-action routing only.

Phase-OCR-Semantic-Candidate-Review-Policy-v1-001
Consumes Semantic Candidate v1 outputs; defines policy/queue/next-action — no decisions committed.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "OCR-Semantic-Candidate-Review-Policy-v1-001"
POLICY_STEP = "ocr_semantic_candidate_review_policy_v1"

TTL_TYPES = {"poster_promo_text", "price_discount_text", "temporal_notice_text"}
ENTITY_VALIDATION_TYPES = {
    "brand_sign",
    "public_facility_sign",
    "bank_branch_sign",
    "store_sign",
    "poster_promo_text",
}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _detect_temporal(raw: str) -> bool:
    return bool(re.search(r"\d{4}[-/年]|\d{1,2}月|有效期|截止|至\s*\d", raw or ""))


def _detect_commercial(raw: str) -> bool:
    return bool(re.search(r"折|优惠|特价|元|促销|活动", raw or ""))


def _policy_route_for_gated(semantic_type: str) -> str:
    if semantic_type in TTL_TYPES:
        return "ttl_review_later"
    if semantic_type == "unknown_text_or_unreadable":
        return "better_source_required"
    if semantic_type == "public_facility_sign":
        return "public_facility_semantic_first"
    return "source_validation_later"


def _final_decision(semantic_type: str, evidence_tier: str, semantic_route: str) -> str:
    if evidence_tier == "sq_e_blocked" or semantic_route == "blocked_unreadable_or_low_quality":
        return "require_better_source"
    if evidence_tier == "scan_observation_only":
        return "require_roi_retry"
    if evidence_tier == "visual_symbol_route":
        return "require_visual_symbol_registry"
    if semantic_type in TTL_TYPES:
        return "require_ttl_review"
    if semantic_type == "unknown_text_or_unreadable":
        return "require_better_source"
    if semantic_type in ENTITY_VALIDATION_TYPES or semantic_type == "public_facility_sign":
        return "require_source_validation"
    return "hold_for_review"


def _queue_type_for(
    *,
    evidence_tier: str,
    semantic_type: str,
    is_scan: bool,
    is_visual: bool,
    is_blocked: bool,
) -> str:
    if is_blocked or evidence_tier == "sq_e_blocked":
        return "better_source_queue"
    if is_visual or evidence_tier == "visual_symbol_route":
        return "visual_symbol_registry_queue"
    if is_scan or evidence_tier == "scan_observation_only":
        return "roi_retry_queue"
    if semantic_type in TTL_TYPES:
        return "ttl_review_queue"
    if semantic_type == "unknown_text_or_unreadable":
        return "better_source_queue"
    if semantic_type in ENTITY_VALIDATION_TYPES:
        return "source_validation_queue"
    return "hold_for_review_queue"


def _priority(queue_type: str) -> str:
    order = {
        "better_source_queue": "high",
        "ttl_review_queue": "medium",
        "source_validation_queue": "medium",
        "visual_symbol_registry_queue": "medium",
        "roi_retry_queue": "low",
        "unresolved_slot_later_queue": "low",
        "hold_for_review_queue": "low",
    }
    return order.get(queue_type, "low")


def run_ocr_semantic_candidate_review_policy_v1(
    *,
    output_root: str,
    semantic_v1_root: str,
    adapter_v1_root: str,
    mixed_batch_v2_root: str,
    linebox_sq_root: str,
    worldmodel_unresolved_slot_root: str,
    contract_root: str,
    readability_governance_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    errs: List[str] = []
    sem = Path(semantic_v1_root).resolve()
    adapter = Path(adapter_v1_root).resolve()
    v2 = Path(mixed_batch_v2_root).resolve()
    linebox = Path(linebox_sq_root).resolve()
    wm_slot = Path(worldmodel_unresolved_slot_root).resolve()
    contract = Path(contract_root).resolve()
    readability = Path(readability_governance_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    for label, p in [("semantic_v1", sem), ("adapter_v1", adapter)]:
        if not p.is_dir():
            errs.append(f"missing_root:{label}")

    gated_doc = _read_json(sem / "ocr_semantic_candidate_v1_gated_ocr_collection.json") or {}
    scan_doc = _read_json(sem / "ocr_semantic_candidate_v1_scan_observation_hint_report.json") or {}
    visual_doc = _read_json(sem / "ocr_semantic_candidate_v1_visual_symbol_route_report.json") or {}
    blocked_doc = _read_json(sem / "ocr_semantic_candidate_v1_sq_e_blocked_report.json") or {}

    gated = [c for c in (gated_doc.get("candidates") or []) if isinstance(c, dict)]
    scan_hints = [h for h in (scan_doc.get("hints") or []) if isinstance(h, dict)]
    visual_routes = [v for v in (visual_doc.get("routes") or []) if isinstance(v, dict)]
    blocked_items = [b for b in (blocked_doc.get("items") or []) if isinstance(b, dict)]

    intake_rows: List[Dict[str, Any]] = []

    def _intake_row(**kwargs: Any) -> Dict[str, Any]:
        base = {
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        base.update(kwargs)
        return base

    for c in gated:
        ib = c.get("interpretation_basis") or {}
        st = c.get("semantic_type_candidate", "")
        intake_rows.append(
            _intake_row(
                input_item_id=c.get("semantic_candidate_id"),
                input_item_type="OCRSemanticCandidate_v1",
                evidence_tier="gated_ocr_primary",
                semantic_route="gated_ocr_semantic_candidate",
                semantic_type_candidate=st,
                source_quality_grade=c.get("source_quality_grade"),
                readability_grade=c.get("readability_grade"),
                raw_ocr_text=c.get("raw_ocr_text"),
                ocr_request_ref=c.get("source_ocr_request_ref"),
                evidence_pack_ref=ib.get("evidence_pack_ref"),
                scan_observation_ref=ib.get("scan_observation_ref"),
                visual_symbol_route_ref=None,
                eligible_for_review_policy=True,
                review_policy_route=_policy_route_for_gated(st),
            )
        )

    for h in scan_hints:
        intake_rows.append(
            _intake_row(
                input_item_id=h.get("scan_hint_id"),
                input_item_type="scan_observation_semantic_hint",
                evidence_tier="scan_observation_only",
                semantic_route="scan_observation_hint",
                semantic_type_candidate=None,
                source_quality_grade=h.get("source_quality_grade"),
                readability_grade=None,
                raw_ocr_text=h.get("scan_text_preview"),
                ocr_request_ref=None,
                evidence_pack_ref=None,
                scan_observation_ref=h.get("scan_observation_ref"),
                visual_symbol_route_ref=None,
                eligible_for_review_policy=True,
                review_policy_route="roi_or_unresolved_review_later",
            )
        )

    for v in visual_routes:
        intake_rows.append(
            _intake_row(
                input_item_id=v.get("visual_route_id"),
                input_item_type="visual_symbol_route_candidate",
                evidence_tier="visual_symbol_route",
                semantic_route="visual_symbol_candidate",
                semantic_type_candidate=v.get("visual_symbol_candidate_type"),
                source_quality_grade=v.get("source_quality_grade"),
                readability_grade=None,
                raw_ocr_text=None,
                ocr_request_ref=None,
                evidence_pack_ref=None,
                scan_observation_ref=None,
                visual_symbol_route_ref=v.get("visual_route_id"),
                eligible_for_review_policy=True,
                review_policy_route="visual_symbol_registry_later",
            )
        )

    for b in blocked_items:
        intake_rows.append(
            _intake_row(
                input_item_id=b.get("blocked_item_id"),
                input_item_type="blocked_unreadable_or_low_quality",
                evidence_tier="sq_e_blocked",
                semantic_route="blocked_unreadable_or_low_quality",
                semantic_type_candidate=None,
                source_quality_grade=b.get("source_quality_grade"),
                readability_grade=None,
                raw_ocr_text=None,
                ocr_request_ref=None,
                evidence_pack_ref=None,
                scan_observation_ref=None,
                visual_symbol_route_ref=None,
                eligible_for_review_policy=True,
                review_policy_route="better_source_required",
            )
        )

    rule_matrix = {
        "schema_version": "ocr_semantic_review_policy_v1_rule_matrix_v0",
        "rules": [
            {
                "rule_id": "gated_poster_promo_requires_ttl",
                "applies_to": ["gated_ocr_primary"],
                "condition": "semantic_type_candidate==poster_promo_text",
                "required_next_action": "ttl_review_queue",
                "blocked_action": ["world_model_attach", "scene_delta_candidate", "fact_commit"],
                "ttl_required": True,
                "source_validation_required": True,
                "review_required": True,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "gated_price_discount_requires_ttl",
                "applies_to": ["gated_ocr_primary"],
                "condition": "semantic_type_candidate==price_discount_text",
                "required_next_action": "ttl_review_queue",
                "blocked_action": ["world_model_attach", "fact_commit"],
                "ttl_required": True,
                "source_validation_required": True,
                "review_required": True,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "gated_temporal_notice_requires_ttl",
                "applies_to": ["gated_ocr_primary"],
                "condition": "semantic_type_candidate==temporal_notice_text",
                "required_next_action": "ttl_review_queue",
                "blocked_action": ["world_model_attach", "fact_commit"],
                "ttl_required": True,
                "source_validation_required": True,
                "review_required": True,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "gated_unknown_requires_better_source",
                "applies_to": ["gated_ocr_primary"],
                "condition": "semantic_type_candidate==unknown_text_or_unreadable",
                "required_next_action": "better_source_queue",
                "blocked_action": ["strong_entity_candidate", "world_model_attach"],
                "ttl_required": False,
                "source_validation_required": True,
                "review_required": True,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "scan_hint_requires_roi_proposal",
                "applies_to": ["scan_observation_only"],
                "condition": "input_item_type==scan_observation_semantic_hint",
                "required_next_action": "roi_retry_queue",
                "blocked_action": ["fact_review", "world_model_attach", "navigation_decision"],
                "ttl_required": False,
                "source_validation_required": False,
                "review_required": False,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "scan_hint_can_link_unresolved_slot_later",
                "applies_to": ["scan_observation_only"],
                "condition": "scan_text_preview_present",
                "required_next_action": "unresolved_slot_later_queue",
                "blocked_action": ["slot_generation_in_this_phase", "world_model_write"],
                "ttl_required": False,
                "source_validation_required": False,
                "review_required": False,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "visual_symbol_requires_registry",
                "applies_to": ["visual_symbol_route"],
                "condition": "evidence_tier==visual_symbol_route",
                "required_next_action": "visual_symbol_registry_queue",
                "blocked_action": ["brand_fact_commit", "ordinary_ocr_semantic"],
                "ttl_required": False,
                "source_validation_required": True,
                "review_required": True,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "visual_symbol_no_brand_fact_without_registry",
                "applies_to": ["visual_symbol_route"],
                "condition": "registry_match_absent",
                "required_next_action": "visual_symbol_registry_queue",
                "blocked_action": ["brand_fact_commit"],
                "ttl_required": False,
                "source_validation_required": True,
                "review_required": True,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "sq_e_requires_better_source",
                "applies_to": ["sq_e_blocked"],
                "condition": "source_quality_grade==SQ_E",
                "required_next_action": "better_source_queue",
                "blocked_action": ["ocr_request", "strong_semantic", "fact_commit"],
                "ttl_required": False,
                "source_validation_required": False,
                "review_required": False,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "low_quality_blocks_fact_review",
                "applies_to": ["sq_e_blocked", "scan_observation_only"],
                "condition": "source_quality_grade in [SQ_E,SQ_D] or scan_only",
                "required_next_action": "block_fact_path",
                "blocked_action": ["fact_review", "entity_commit"],
                "ttl_required": False,
                "source_validation_required": False,
                "review_required": False,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "mixed_region_blocks_strong_entity",
                "applies_to": ["sq_e_blocked", "scan_observation_only"],
                "condition": "blocked_reason contains mixed",
                "required_next_action": "better_source_queue",
                "blocked_action": ["strong_entity_candidate"],
                "ttl_required": False,
                "source_validation_required": False,
                "review_required": False,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "missing_spatial_anchor_blocks_worldmodel",
                "applies_to": ["gated_ocr_primary"],
                "condition": "spatial_coordinates.gps_lat is null",
                "required_next_action": "hold_for_review",
                "blocked_action": ["world_model_attach"],
                "ttl_required": False,
                "source_validation_required": True,
                "review_required": True,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "public_facility_requires_semantic_first",
                "applies_to": ["gated_ocr_primary"],
                "condition": "semantic_type_candidate==public_facility_sign",
                "required_next_action": "source_validation_queue",
                "blocked_action": ["ordinary_ocr_fact_first"],
                "ttl_required": False,
                "source_validation_required": True,
                "review_required": True,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "no_world_model_attach_in_this_phase",
                "applies_to": ["*"],
                "condition": "always",
                "required_next_action": "policy_only",
                "blocked_action": ["world_model_attach", "world_model_write"],
                "ttl_required": False,
                "source_validation_required": False,
                "review_required": False,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
            {
                "rule_id": "no_scene_delta_candidate_in_this_phase",
                "applies_to": ["*"],
                "condition": "always",
                "required_next_action": "policy_only",
                "blocked_action": ["scene_delta_candidate", "scene_delta_write"],
                "ttl_required": False,
                "source_validation_required": False,
                "review_required": False,
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            },
        ],
    }

    queue_rows: List[Dict[str, Any]] = []
    ttl_rows: List[Dict[str, Any]] = []
    validation_rows: List[Dict[str, Any]] = []
    decision_rows: List[Dict[str, Any]] = []

    for row in intake_rows:
        item_id = row["input_item_id"]
        tier = row["evidence_tier"]
        st = row.get("semantic_type_candidate")
        raw = str(row.get("raw_ocr_text") or "")
        is_scan = row["input_item_type"] == "scan_observation_semantic_hint"
        is_visual = row["input_item_type"] == "visual_symbol_route_candidate"
        is_blocked = row["input_item_type"] == "blocked_unreadable_or_low_quality"

        qtype = _queue_type_for(
            evidence_tier=tier,
            semantic_type=st or "",
            is_scan=is_scan,
            is_visual=is_visual,
            is_blocked=is_blocked,
        )
        if is_scan and row.get("source_quality_grade") == "SQ_E":
            queue_rows.append(
                {
                    "review_queue_candidate_id": f"rq_{item_id}_unresolved",
                    "source_semantic_item_id": item_id,
                    "evidence_tier": tier,
                    "semantic_route": row.get("semantic_route"),
                    "semantic_type_candidate": st,
                    "queue_type": "unresolved_slot_later_queue",
                    "queue_priority": "low",
                    "required_gates": ["roi_retry", "unresolved_slot_later"],
                    "blocked_actions": ["fact_review", "world_model_attach"],
                    "review_status": "pending_policy_review",
                    "approval_status": "not_approved",
                    "fact_status": "not_fact",
                    "write_allowed": False,
                }
            )

        gates = []
        if st in TTL_TYPES:
            gates.append("ttl")
        if st in ENTITY_VALIDATION_TYPES or is_visual:
            gates.append("source_validation")
        if is_visual:
            gates.append("visual_symbol_registry")
        if is_scan:
            gates.append("roi_retry")
        if is_blocked or st == "unknown_text_or_unreadable":
            gates.append("better_source")

        queue_rows.append(
            {
                "review_queue_candidate_id": f"rq_{item_id}",
                "source_semantic_item_id": item_id,
                "evidence_tier": tier,
                "semantic_route": row.get("semantic_route"),
                "semantic_type_candidate": st,
                "queue_type": qtype,
                "queue_priority": _priority(qtype),
                "required_gates": gates or ["hold"],
                "blocked_actions": [
                    "world_model_attach",
                    "scene_delta_candidate",
                    "fact_commit",
                    "auto_approve",
                ],
                "review_status": "pending_policy_review",
                "approval_status": "not_approved",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        if tier == "gated_ocr_primary" and st:
            ttl_req = st in TTL_TYPES
            ttl_rows.append(
                {
                    "item_id": item_id,
                    "semantic_type_candidate": st,
                    "raw_ocr_text": raw,
                    "ttl_required": ttl_req,
                    "ttl_reason": "commercial_or_temporal_text_policy" if ttl_req else None,
                    "explicit_validity_period_detected": _detect_temporal(raw),
                    "temporal_text_detected": _detect_temporal(raw),
                    "commercial_claim_detected": _detect_commercial(raw) or st in TTL_TYPES,
                    "ttl_policy_satisfied": False,
                    "world_model_write_allowed": False,
                    "scene_delta_candidate_allowed": False,
                }
            )
            validation_rows.append(
                {
                    "item_id": item_id,
                    "semantic_type_candidate": st,
                    "entity_type_candidate": next(
                        (c.get("entity_type_candidate") for c in gated if c.get("semantic_candidate_id") == item_id),
                        None,
                    ),
                    "source_validation_required": st in ENTITY_VALIDATION_TYPES or ttl_req,
                    "validation_reason": "entity_or_commercial_text_requires_validation",
                    "required_sources": [
                        "repeated_observation",
                        "human_review",
                        "better_roi_crop",
                    ],
                    "validation_satisfied": False,
                    "fact_status": "not_fact",
                    "write_allowed": False,
                }
            )

        final = _final_decision(st or "", tier, row.get("semantic_route", ""))
        blocked = ["world_model_attach", "scene_delta_candidate", "fact_commit", "auto_approve"]
        if is_scan or is_blocked:
            blocked.append("fact_review")
        if is_visual:
            blocked.extend(["brand_fact_commit", "ordinary_ocr_semantic"])

        decision_rows.append(
            {
                "input_item_id": item_id,
                "evidence_tier": tier,
                "semantic_route": row.get("semantic_route"),
                "semantic_type_candidate": st,
                "final_policy_decision": final,
                "required_next_action": final,
                "blocked_actions": blocked,
                "required_gates": gates or ["hold"],
                "can_generate_fact_review": False,
                "can_generate_worldmodel_attach": False,
                "can_generate_scene_delta": False,
                "approval_status": "not_approved",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    visual_registry_rows = [
        {
            "visual_route_id": v.get("visual_route_id"),
            "source_item_ref": v.get("source_item_ref"),
            "source_quality_grade": v.get("source_quality_grade"),
            "visual_symbol_candidate_type": v.get("visual_symbol_candidate_type"),
            "registry_required": True,
            "brand_fact_allowed": False,
            "ordinary_ocr_semantic_allowed": False,
            "next_action": "visual_symbol_registry_later",
            "review_required": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        for v in visual_routes
    ]

    scan_roi_rows = [
        {
            "scan_hint_id": h.get("scan_hint_id"),
            "scan_observation_ref": h.get("scan_observation_ref"),
            "scan_text_preview": h.get("scan_text_preview"),
            "linebox_refs": h.get("linebox_refs") or [],
            "source_quality_grade": h.get("source_quality_grade"),
            "reason_not_primary_evidence": h.get("reason_not_primary_evidence"),
            "roi_retry_required": True,
            "unresolved_slot_candidate_allowed_later": True,
            "fact_review_allowed": False,
            "world_model_attach_allowed": False,
            "suggested_roi_types": ["linebox_crop", "quality_gated_roi", "poster_subregion"],
            "required_next_action": "roi_proposal_later",
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        for h in scan_hints
    ]

    sq_e_rows = [
        {
            "blocked_item_id": b.get("blocked_item_id"),
            "source_quality_grade": b.get("source_quality_grade") or "SQ_E",
            "blocked_reason": b.get("blocked_reason"),
            "better_source_required": True,
            "retry_conditions": [
                "higher_source_quality_than_SQ_E",
                "roi_crop_before_ocr",
                "readability_gate_pass",
            ],
            "fact_review_allowed": False,
            "strong_semantic_allowed": False,
            "unresolved_slot_candidate_allowed_later": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        for b in blocked_items
    ]

    linkage_items: List[Dict[str, Any]] = []
    for h in scan_hints:
        linkage_items.append(
            {
                "source_item_ref": h.get("source_id") or h.get("scan_hint_id"),
                "potential_slot_type": "scan_without_gated_ocr",
                "unresolved_reason_candidate": "scan_hint_text_no_gated_pack",
                "slot_link_allowed_later": True,
                "slot_generation_allowed_in_this_phase": False,
                "world_model_write_allowed": False,
                "required_future_observation": "gated_roi_ocr",
            }
        )
    for b in blocked_items:
        linkage_items.append(
            {
                "source_item_ref": b.get("source_item_ref"),
                "potential_slot_type": "blocked_unreadable",
                "unresolved_reason_candidate": b.get("blocked_reason"),
                "slot_link_allowed_later": True,
                "slot_generation_allowed_in_this_phase": False,
                "world_model_write_allowed": False,
                "required_future_observation": "better_source_or_frame",
            }
        )
    for c in gated:
        if c.get("semantic_type_candidate") == "unknown_text_or_unreadable":
            linkage_items.append(
                {
                    "source_item_ref": c.get("semantic_candidate_id"),
                    "potential_slot_type": "unknown_text_observation",
                    "unresolved_reason_candidate": "gated_ocr_unknown_or_partial",
                    "slot_link_allowed_later": True,
                    "slot_generation_allowed_in_this_phase": False,
                    "world_model_write_allowed": False,
                    "required_future_observation": "better_roi_or_frame",
                }
            )
    for v in visual_routes:
        linkage_items.append(
            {
                "source_item_ref": v.get("source_item_ref"),
                "potential_slot_type": "visual_symbol_unresolved",
                "unresolved_reason_candidate": "registry_match_required",
                "slot_link_allowed_later": True,
                "slot_generation_allowed_in_this_phase": False,
                "world_model_write_allowed": False,
                "required_future_observation": "visual_symbol_registry",
            }
        )

    qtype_counts = Counter(q.get("queue_type") for q in queue_rows)
    decision_counts = Counter(d.get("final_policy_decision") for d in decision_rows)

    governance_routing = {
        "schema_version": "ocr_semantic_review_policy_v1_governance_routing_report_v0",
        "ttl_review_count": qtype_counts.get("ttl_review_queue", 0),
        "source_validation_count": qtype_counts.get("source_validation_queue", 0),
        "visual_symbol_registry_count": qtype_counts.get("visual_symbol_registry_queue", 0),
        "roi_retry_count": qtype_counts.get("roi_retry_queue", 0),
        "better_source_count": qtype_counts.get("better_source_queue", 0),
        "unresolved_slot_later_count": qtype_counts.get("unresolved_slot_later_queue", 0),
        "hold_for_review_count": qtype_counts.get("hold_for_review_queue", 0) + decision_counts.get("hold_for_review", 0),
        "blocked_fact_path_count": sum(
            1 for d in decision_rows if "fact_review" in (d.get("blocked_actions") or [])
        ),
        "world_model_attach_allowed_count": 0,
        "scene_delta_candidate_allowed_count": 0,
        "final_policy_decision_distribution": dict(decision_counts),
    }

    boundary = {
        "schema_version": "ocr_semantic_review_policy_v1_boundary_report_v0",
        "review_policy_does_not_commit_decision": True,
        "approval_granted_count": 0,
        "auto_approve_invoked": False,
        "fact_review_generated": False,
        "world_model_attach_allowed": False,
        "scene_delta_candidate_allowed": False,
        "world_model_write_allowed": False,
        "navigation_decision_allowed": False,
    }

    metrics = {
        "schema_version": "ocr_semantic_review_policy_v1_metrics_candidate_report_v0",
        "input_item_count": len(intake_rows),
        "review_queue_candidate_count": len(queue_rows),
        "ttl_review_count": qtype_counts.get("ttl_review_queue", 0),
        "source_validation_count": qtype_counts.get("source_validation_queue", 0),
        "visual_symbol_registry_count": qtype_counts.get("visual_symbol_registry_queue", 0),
        "roi_retry_count": qtype_counts.get("roi_retry_queue", 0),
        "better_source_count": qtype_counts.get("better_source_queue", 0),
        "unresolved_slot_later_count": qtype_counts.get("unresolved_slot_later_queue", 0),
        "approval_granted_count": 0,
        "fact_write_allowed_count": 0,
        "world_model_attach_allowed_count": 0,
        "scene_delta_candidate_allowed_count": 0,
        "no_write_boundary_pass_rate": 1.0,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    benchmark_link = {
        "schema_version": "ocr_semantic_review_policy_v1_benchmark_link_report_v0",
        "benchmark_real_values_smoke_available": bench.is_dir(),
        "current_phase_updates_benchmark_values": False,
        "current_phase_collects_t2": False,
        "ground_truth_available": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health_link = {
        "schema_version": "ocr_semantic_review_policy_v1_system_health_link_report_v0",
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    no_write = {
        "schema_version": "ocr_semantic_review_policy_v1_no_write_boundary_report_v0",
        "boundary_ok": True,
        "violations": [],
        "policy_only": True,
        "review_decision_committed": False,
        "approval_granted": False,
        "auto_approve_invoked": False,
        "fact_review_generated": False,
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
        "schema_version": "ocr_semantic_review_policy_v1_simulation_context_report_v0",
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": "ocr_semantic_review_policy_v1_non_claims_report_v0",
        "no_ocr_execution": True,
        "no_llm_vlm_semantic_model": True,
        "no_review_decision_commit": True,
        "no_candidate_approval": True,
        "no_fact_review_generation": True,
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
        "schema_version": "ocr_semantic_review_policy_v1_open_followups_v0",
        "items": [
            "Review Queue Runtime DryRun",
            "TTL Gate v1 for OCR Semantic Candidate",
            "Source Validation DryRun",
            "ROI Retry Proposal",
            "VisualSymbolRegistry integration",
            "Unresolved Slot dry-run from scan observation",
            "PublicFacility semantic-first runtime extension",
            "SystemHealth provider runtime dry-run",
            "Ground Truth Annotation Schema",
            "Benchmark T2 collector",
            "Controlled runtime integration",
        ],
    }

    audit = {
        "schema_version": "ocr_semantic_review_policy_v1_audit_report_v0",
        "ocr_semantic_review_policy_v1_executed": True,
        "policy_only": True,
        "review_policy_consumes_semantic_v1": True,
        "tier_aware_review_policy_defined": True,
        "review_decision_committed": False,
        "approval_granted": False,
        "auto_approve_invoked": False,
        "fact_review_generated": False,
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

    summary = {
        "schema_version": "ocr_semantic_candidate_review_policy_v1_summary_v0",
        "phase": PHASE_ID,
        "policy_scope": "review_policy_and_next_action_routing_only",
        "based_on_semantic_candidate_v1": sem.is_dir(),
        "based_on_evidence_pack_adapter_v1": adapter.is_dir(),
        "based_on_mixed_batch_v2": v2.is_dir(),
        "based_on_source_quality_gate": linebox.is_dir(),
        "based_on_worldmodel_unresolved_slot_contract": wm_slot.is_dir(),
        "review_policy_consumes_semantic_v1": True,
        "tier_aware_review_policy_defined": True,
        "ttl_policy_required_for_promo_or_temporal": True,
        "visual_symbol_requires_registry": True,
        "scan_hint_not_reviewed_as_fact": True,
        "sq_e_blocked_requires_better_source": True,
        "unknown_text_requires_better_source": True,
        "world_model_attach_allowed": False,
        "scene_delta_candidate_allowed": False,
        "review_decision_committed": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "input_item_count": len(intake_rows),
        "review_queue_candidate_count": len(queue_rows),
        "phase_verdict_hint": "GO" if not errs else "CONDITIONAL_GO",
    }
    if errs:
        summary["errors"] = errs

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "ocr_semantic_review_policy_v1_input_intake_matrix_v0",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": rule_matrix,
        "queue_matrix": {
            "schema_version": "ocr_semantic_review_policy_v1_queue_candidate_matrix_v0",
            "candidate_count": len(queue_rows),
            "all_approval_status_not_approved": all(q.get("approval_status") == "not_approved" for q in queue_rows),
            "rows": queue_rows,
        },
        "ttl_matrix": {
            "schema_version": "ocr_semantic_review_policy_v1_ttl_requirement_matrix_v0",
            "row_count": len(ttl_rows),
            "rows": ttl_rows,
        },
        "validation_matrix": {
            "schema_version": "ocr_semantic_review_policy_v1_source_validation_matrix_v0",
            "row_count": len(validation_rows),
            "all_validation_satisfied_false": all(v.get("validation_satisfied") is False for v in validation_rows),
            "rows": validation_rows,
        },
        "visual_registry": {
            "schema_version": "ocr_semantic_review_policy_v1_visual_symbol_registry_routing_matrix_v0",
            "row_count": len(visual_registry_rows),
            "rows": visual_registry_rows,
        },
        "scan_roi": {
            "schema_version": "ocr_semantic_review_policy_v1_scan_hint_roi_retry_matrix_v0",
            "row_count": len(scan_roi_rows),
            "all_fact_review_allowed_false": all(r.get("fact_review_allowed") is False for r in scan_roi_rows),
            "rows": scan_roi_rows,
        },
        "sq_e_matrix": {
            "schema_version": "ocr_semantic_review_policy_v1_sq_e_better_source_matrix_v0",
            "row_count": len(sq_e_rows),
            "all_strong_semantic_allowed_false": all(r.get("strong_semantic_allowed") is False for r in sq_e_rows),
            "rows": sq_e_rows,
        },
        "decision_matrix": {
            "schema_version": "ocr_semantic_review_policy_v1_decision_matrix_v0",
            "row_count": len(decision_rows),
            "rows": decision_rows,
        },
        "boundary": boundary,
        "unresolved_linkage": {
            "schema_version": "ocr_semantic_review_policy_v1_unresolved_slot_linkage_policy_v0",
            "worldmodel_contract_root": str(wm_slot),
            "slot_generation_allowed_in_this_phase": False,
            "item_count": len(linkage_items),
            "items": linkage_items,
        },
        "governance_routing": governance_routing,
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

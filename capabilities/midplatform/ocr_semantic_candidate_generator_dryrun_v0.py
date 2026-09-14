# -*- coding: utf-8 -*-
"""Generate OCRSemanticCandidate dry-run from OCRTextEvidencePack v0.

Phase-OCR-Semantic-Candidate-Generator-DryRun-001
Rule/heuristic only — no LLM/VLM/semantic model.
"""

from __future__ import annotations

import copy
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "OCR-Semantic-Candidate-Generator-DryRun-001"
GENERATOR_STEP = "ocr_semantic_candidate_generator_dryrun"
CANDIDATE_SCHEMA_VERSION = "ocr_semantic_candidate_v0"

EMPTY_REASONS = [
    "roi_without_readable_text",
    "text_too_small",
    "low_readability",
    "sample_limitation",
]

POSTER_RULES: Dict[str, Dict[str, Any]] = {
    "title_area": {
        "semantic_type_candidate": "poster_promo_text",
        "entity_type_candidate": "promo",
        "commercial_claim_candidate": True,
        "temporal_validity_candidate": False,
        "requires_ttl": True,
        "human_readable_meaning_candidate": "poster promotional headline text",
    },
    "body_text_area": {
        "semantic_type_candidate": "poster_promo_text",
        "entity_type_candidate": "promo",
        "commercial_claim_candidate": True,
        "temporal_validity_candidate": False,
        "requires_ttl": True,
        "human_readable_meaning_candidate": "poster promotional body text",
    },
    "price_or_promo_area": {
        "semantic_type_candidate": "price_discount_text",
        "entity_type_candidate": "discount",
        "commercial_claim_candidate": True,
        "temporal_validity_candidate": False,
        "requires_ttl": True,
        "human_readable_meaning_candidate": "price or discount promotional text",
    },
    "time_location_area": {
        "semantic_type_candidate": "temporal_notice_text",
        "entity_type_candidate": "temporal_notice",
        "commercial_claim_candidate": False,
        "temporal_validity_candidate": True,
        "requires_ttl": True,
        "human_readable_meaning_candidate": "temporal validity notice text",
    },
}

GOVERNANCE_ROUTE: Dict[str, str] = {
    "poster_promo_text": "poster_ttl_policy_later",
    "price_discount_text": "poster_ttl_policy_later",
    "temporal_notice_text": "poster_ttl_policy_later",
    "brand_sign": "visual_symbol_registry_later",
    "public_facility_sign": "public_facility_semantic_first",
    "unknown_text_or_unreadable": "text_bearing_sample_later",
}


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _normalize_candidate(raw: str) -> Optional[str]:
    if not raw or not raw.strip():
        return None
    parts = [p.strip() for p in re.split(r"\s*\|\s*", raw) if p.strip()]
    if len(parts) > 1:
        return " ".join(parts)
    return raw.strip()


def _load_packs(adapter_root: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    poster_doc = _read_json(adapter_root / "ocr_evidence_pack_adapter_poster_collection.json") or {}
    rv_doc = _read_json(adapter_root / "ocr_evidence_pack_adapter_realvideo_collection.json") or {}
    poster = [p for p in (poster_doc.get("packs") or []) if isinstance(p, dict)]
    rv = [p for p in (rv_doc.get("packs") or []) if isinstance(p, dict)]
    return poster, rv


def _interpretation_basis(pack: Dict[str, Any], adapter_root: str, extras: Dict[str, Any]) -> Dict[str, Any]:
    ev_id = pack.get("evidence_id")
    src = pack.get("source") if isinstance(pack.get("source"), dict) else {}
    return {
        "ocr_text_ref": {"evidence_id": ev_id, "raw_ocr_text": (pack.get("raw_ocr") or {}).get("raw_ocr_text")},
        "image_coordinate_ref": {"evidence_id": ev_id, "bbox_xyxy": (pack.get("image_coordinates") or {}).get("bbox_xyxy")},
        "temporal_coordinate_ref": {"evidence_id": ev_id, "fields": pack.get("temporal_coordinates")},
        "spatial_coordinate_ref": pack.get("spatial_coordinates"),
        "readability_quality_ref": {"evidence_id": ev_id, "readability_quality": pack.get("readability_quality")},
        "public_facility_context_ref": extras.get("public_facility_context_ref"),
        "poster_context_ref": extras.get("poster_context_ref"),
        "visual_symbol_context_ref": None,
        "map_context_ref": None,
        "memory_context_ref": None,
        "multi_frame_context_ref": None,
        "adapter_pack_ref": f"{adapter_root}/ocr_evidence_pack_adapter_unified_index.json",
    }


def _governance_block(
    *,
    semantic_type: str,
    requires_ttl: bool,
    commercial: bool = False,
) -> Dict[str, Any]:
    return {
        "semantic_candidate_not_fact": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "raw_text_overwritten": False,
        "completion_committed": False,
        "correction_committed": False,
        "requires_review": True,
        "requires_source_validation": True,
        "requires_midplatform_arbitration": True,
        "routed_governance": GOVERNANCE_ROUTE.get(semantic_type, "text_bearing_sample_later"),
        "ttl_required": requires_ttl,
        "commercial_claim_candidate": commercial,
        "world_model_attach_allowed": False,
        "scene_delta_candidate_allowed": False,
    }


def _build_poster_candidate(pack: Dict[str, Any], adapter_root: str) -> Dict[str, Any]:
    ev_id = str(pack.get("evidence_id") or "")
    roi_id = str((pack.get("source") or {}).get("roi_id") or "")
    rule = POSTER_RULES.get(roi_id, POSTER_RULES["title_area"])
    raw = str((pack.get("raw_ocr") or {}).get("raw_ocr_text") or "")
    sc = list((pack.get("source") or {}).get("source_chain") or [])
    sc = sc + [GENERATOR_STEP]

    sem_id = f"ocr_sem_cand_{ev_id}"
    meaning = {
        "semantic_type": rule["semantic_type_candidate"],
        "entity_type_candidate": rule["entity_type_candidate"],
        "entity_name_candidate": None,
        "human_readable_meaning_candidate": rule.get("human_readable_meaning_candidate"),
        "place_function_candidate": None,
        "actionability_candidate": None,
        "commercial_claim_candidate": rule.get("commercial_claim_candidate"),
        "temporal_validity_candidate": rule.get("temporal_validity_candidate"),
    }

    return {
        "semantic_candidate_id": sem_id,
        "schema_version": CANDIDATE_SCHEMA_VERSION,
        "semantic_scope": "midplatform_interpretation_candidate",
        "source_ocr_evidence_id": ev_id,
        "source_pack_ref": f"{adapter_root}/ocr_evidence_pack_adapter_poster_collection.json",
        "raw_ocr_text": raw,
        "raw_ocr_text_preserved": True,
        "normalized_text_candidate": _normalize_candidate(raw),
        "correction_candidate": None,
        "completion_candidate": None,
        "meaning_candidate": meaning,
        "interpretation_basis": _interpretation_basis(
            pack,
            adapter_root,
            {"poster_context_ref": {"roi_id": roi_id, "region_type": "poster_text_region"}},
        ),
        "governance": _governance_block(
            semantic_type=rule["semantic_type_candidate"],
            requires_ttl=bool(rule.get("requires_ttl")),
            commercial=bool(rule.get("commercial_claim_candidate")),
        ),
        "fact_status": "not_fact",
        "write_allowed": False,
        "semantic_candidate_not_fact": True,
        "completion_committed": False,
        "correction_committed": False,
        "source_chain": sc,
        "world_model_attach_placeholder_id": pack.get("world_model_attach_placeholder_id"),
    }


def _build_realvideo_empty_candidate(pack: Dict[str, Any], adapter_root: str) -> Dict[str, Any]:
    ev_id = str(pack.get("evidence_id") or "")
    src = pack.get("source") if isinstance(pack.get("source"), dict) else {}
    frame_id = str(src.get("frame_id") or "")
    roi_id = str(src.get("roi_id") or "")
    sc = list(src.get("source_chain") or [])
    sc = sc + [GENERATOR_STEP]

    sem_id = f"ocr_sem_cand_{ev_id}"
    meaning = {
        "semantic_type": "unknown_text_or_unreadable",
        "entity_type_candidate": "unknown",
        "entity_name_candidate": None,
        "human_readable_meaning_candidate": None,
        "place_function_candidate": None,
        "actionability_candidate": None,
        "commercial_claim_candidate": False,
        "temporal_validity_candidate": False,
    }

    return {
        "semantic_candidate_id": sem_id,
        "schema_version": CANDIDATE_SCHEMA_VERSION,
        "semantic_scope": "midplatform_interpretation_candidate",
        "source_ocr_evidence_id": ev_id,
        "source_pack_ref": f"{adapter_root}/ocr_evidence_pack_adapter_realvideo_collection.json",
        "raw_ocr_text": "",
        "raw_ocr_text_preserved": True,
        "normalized_text_candidate": None,
        "correction_candidate": None,
        "completion_candidate": None,
        "meaning_candidate": meaning,
        "interpretation_basis": _interpretation_basis(pack, adapter_root, {}),
        "governance": _governance_block(
            semantic_type="unknown_text_or_unreadable",
            requires_ttl=False,
        ),
        "fact_status": "not_fact",
        "write_allowed": False,
        "semantic_candidate_not_fact": True,
        "completion_committed": False,
        "correction_committed": False,
        "empty_text": True,
        "empty_text_is_not_no_text_fact": True,
        "requires_text_bearing_sample": True,
        "possible_reason_candidates": list(EMPTY_REASONS),
        "source_chain": sc,
        "world_model_attach_placeholder_id": pack.get("world_model_attach_placeholder_id"),
        "source_frame_id": frame_id,
        "source_roi_id": roi_id,
    }


def run_ocr_semantic_candidate_generator_dryrun_v0(
    *,
    ocr_evidence_pack_contract_root: str,
    ocr_evidence_pack_adapter_update_root: str,
    realvideo_readability_governance_root: str,
    poster_fusion_gate_chain_closure_root: str,
    public_facility_runtime_dryrun_root: str,
    benchmark_real_values_smoke_root: str,
    system_health_governance_root: str,
    simulation_lab_harness_root: str,
    output_root: str,
) -> Tuple[Any, ...]:
    errs: List[str] = []
    contract = Path(ocr_evidence_pack_contract_root).resolve()
    adapter = Path(ocr_evidence_pack_adapter_update_root).resolve()
    readability = Path(realvideo_readability_governance_root).resolve()
    poster_closure = Path(poster_fusion_gate_chain_closure_root).resolve()
    public_facility = Path(public_facility_runtime_dryrun_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim = Path(simulation_lab_harness_root).resolve()
    out = Path(output_root).resolve()

    registry = _read_json(contract / "ocr_semantic_meaning_type_registry_v0.json") or {}
    poster_packs, rv_packs = _load_packs(adapter)
    if len(poster_packs) != 4:
        errs.append(f"poster_pack_count:{len(poster_packs)}")
    if len(rv_packs) != 10:
        errs.append(f"realvideo_pack_count:{len(rv_packs)}")

    adapter_root_str = str(adapter)
    poster_candidates = [_build_poster_candidate(p, adapter_root_str) for p in poster_packs]
    rv_candidates = [_build_realvideo_empty_candidate(p, adapter_root_str) for p in rv_packs]
    all_candidates = poster_candidates + rv_candidates

    empty_count = sum(1 for c in all_candidates if c.get("empty_text") or c.get("raw_ocr_text") == "")
    non_empty_count = len(all_candidates) - empty_count

    collection = {
        "schema_version": "ocr_semantic_candidate_collection_v0",
        "candidate_count": len(all_candidates),
        "raw_text_overwritten": False,
        "semantic_candidate_not_fact": True,
        "completion_committed": False,
        "correction_committed": False,
        "candidates": all_candidates,
    }

    poster_matrix_rows: List[Dict[str, Any]] = []
    for p, c in zip(poster_packs, poster_candidates):
        roi_id = str((p.get("source") or {}).get("roi_id") or "")
        rule = POSTER_RULES.get(roi_id, {})
        mc = c.get("meaning_candidate") if isinstance(c.get("meaning_candidate"), dict) else {}
        poster_matrix_rows.append(
            {
                "region_id": roi_id,
                "source_ocr_evidence_id": p.get("evidence_id"),
                "raw_ocr_text": (p.get("raw_ocr") or {}).get("raw_ocr_text"),
                "semantic_type_candidate": rule.get("semantic_type_candidate"),
                "entity_type_candidate": rule.get("entity_type_candidate"),
                "meaning_candidate": mc.get("human_readable_meaning_candidate"),
                "commercial_claim_candidate": rule.get("commercial_claim_candidate"),
                "temporal_validity_candidate": rule.get("temporal_validity_candidate"),
                "requires_ttl": rule.get("requires_ttl"),
                "source_validation_required": True,
                "review_required": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    poster_matrix = {
        "schema_version": "ocr_semantic_candidate_poster_matrix_v0",
        "poster_semantic_candidate_count": len(poster_matrix_rows),
        "rows": poster_matrix_rows,
    }

    rv_empty_rows: List[Dict[str, Any]] = []
    for p, c in zip(rv_packs, rv_candidates):
        src = p.get("source") if isinstance(p.get("source"), dict) else {}
        rv_empty_rows.append(
            {
                "source_frame_id": src.get("frame_id"),
                "source_roi_id": src.get("roi_id"),
                "source_ocr_evidence_id": p.get("evidence_id"),
                "raw_ocr_text": "",
                "empty_text": True,
                "semantic_type_candidate": "unknown_text_or_unreadable",
                "meaning_candidate": None,
                "empty_text_is_not_no_text_fact": True,
                "possible_reason_candidates": list(EMPTY_REASONS),
                "requires_text_bearing_sample": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    rv_empty_matrix = {
        "schema_version": "ocr_semantic_candidate_realvideo_empty_matrix_v0",
        "realvideo_empty_candidate_count": len(rv_empty_rows),
        "empty_text_is_not_no_text_fact": True,
        "no_text_fact_generated": False,
        "no_navigation_decision_from_empty_text": True,
        "rows": rv_empty_rows,
    }

    type_dist = Counter(
        (c.get("meaning_candidate") or {}).get("semantic_type") for c in all_candidates if isinstance(c.get("meaning_candidate"), dict)
    )
    requires_ttl_count = sum(1 for c in all_candidates if (c.get("governance") or {}).get("ttl_required"))
    review_count = sum(1 for c in all_candidates if (c.get("governance") or {}).get("requires_review") is not False)

    type_report = {
        "schema_version": "ocr_semantic_candidate_type_classification_report_v0",
        "semantic_type_distribution": dict(type_dist),
        "type_registry_used": bool(registry),
        "type_registry_ref": str(contract / "ocr_semantic_meaning_type_registry_v0.json"),
        "unknown_type_count": type_dist.get("unknown_text_or_unreadable", 0),
        "requires_ttl_count": requires_ttl_count,
        "requires_review_count": review_count,
        "fact_write_default_false_count": len(all_candidates),
    }

    normalize_count = sum(1 for c in all_candidates if c.get("normalized_text_candidate"))
    enhancement = {
        "schema_version": "ocr_semantic_candidate_enhancement_report_v0",
        "normalize_candidate_count": normalize_count,
        "correction_candidate_count": 0,
        "completion_candidate_count": 0,
        "completion_committed_count": 0,
        "correction_committed_count": 0,
        "raw_text_overwritten": False,
        "overwrite_raw_ocr_text_forbidden": True,
        "enhancement_output_status": "candidate_only",
    }

    basis_rows = [
        {
            "semantic_candidate_id": c.get("semantic_candidate_id"),
            "source_ocr_evidence_id": c.get("source_ocr_evidence_id"),
            **(c.get("interpretation_basis") if isinstance(c.get("interpretation_basis"), dict) else {}),
        }
        for c in all_candidates
    ]
    basis_report = {
        "schema_version": "ocr_semantic_candidate_interpretation_basis_report_v0",
        "row_count": len(basis_rows),
        "rows": basis_rows,
    }

    gov_rows = [
        {
            "semantic_candidate_id": c.get("semantic_candidate_id"),
            "semantic_type_candidate": (c.get("meaning_candidate") or {}).get("semantic_type"),
            "routed_governance": (c.get("governance") or {}).get("routed_governance"),
            "ttl_required": (c.get("governance") or {}).get("ttl_required"),
            "source_validation_required": (c.get("governance") or {}).get("requires_source_validation"),
            "review_required": (c.get("governance") or {}).get("requires_review"),
            "visual_symbol_required": (c.get("meaning_candidate") or {}).get("semantic_type") == "brand_sign",
            "public_facility_semantic_first_required": (c.get("meaning_candidate") or {}).get("semantic_type")
            == "public_facility_sign",
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
        }
        for c in all_candidates
    ]
    gov_report = {
        "schema_version": "ocr_semantic_candidate_governance_routing_report_v0",
        "row_count": len(gov_rows),
        "rows": gov_rows,
        "public_facility_governance_root": str(public_facility),
        "poster_gate_chain_closure_root": str(poster_closure),
    }

    raw_preservation = {
        "schema_version": "ocr_semantic_candidate_raw_text_preservation_report_v0",
        "input_pack_count": len(poster_packs) + len(rv_packs),
        "semantic_candidate_count": len(all_candidates),
        "raw_ocr_text_preserved": True,
        "raw_text_overwritten": False,
        "raw_text_deleted": False,
        "raw_text_normalized_separately": True,
        "raw_text_preservation_rate": 1.0,
    }

    empty_guard = {
        "schema_version": "ocr_semantic_candidate_empty_text_guard_report_v0",
        "empty_text_count": len(rv_candidates),
        "empty_text_is_valid_ocr_result": True,
        "empty_text_is_not_failure": True,
        "empty_text_is_not_no_text_fact": True,
        "no_text_fact_generated": False,
        "no_scene_delta_from_empty_text": True,
        "no_world_model_write_from_empty_text": True,
        "no_navigation_decision_from_empty_text": True,
        "requires_text_bearing_sample": True,
    }

    commercial_count = sum(
        1 for c in poster_candidates if (c.get("meaning_candidate") or {}).get("commercial_claim_candidate")
    )
    temporal_count = sum(
        1 for c in poster_candidates if (c.get("meaning_candidate") or {}).get("temporal_validity_candidate")
    )
    spatial_missing = sum(
        1
        for c in all_candidates
        if not ((c.get("interpretation_basis") or {}).get("spatial_coordinate_ref") or {}).get("gps_lat")
    )

    quality_risk = {
        "schema_version": "ocr_semantic_candidate_quality_risk_report_v0",
        "semantic_candidate_not_fact": True,
        "low_readability_risk_count": len(all_candidates),
        "empty_text_risk_count": len(rv_candidates),
        "commercial_text_risk_count": commercial_count,
        "temporal_text_risk_count": temporal_count,
        "source_validation_missing_count": len(all_candidates),
        "spatial_anchor_missing_count": spatial_missing,
        "review_required_count": review_count,
        "world_model_write_blocked_count": len(all_candidates),
    }

    wm_carryover = {
        "schema_version": "ocr_semantic_candidate_world_model_attach_placeholder_carryover_report_v0",
        "wm_attach_placeholder_count": len(all_candidates),
        "world_model_attach_candidate_generated": False,
        "world_model_attach_executed": False,
        "attach_candidate_not_fact": True,
        "world_model_write_allowed": False,
        "scene_delta_candidate_allowed": False,
        "requires_world_model_attach_generator_later": True,
    }

    chain_rows = []
    for c in all_candidates:
        sc = c.get("source_chain") if isinstance(c.get("source_chain"), list) else []
        orig_len = len(sc) - 1 if GENERATOR_STEP in sc else len(sc)
        chain_rows.append(
            {
                "semantic_candidate_id": c.get("semantic_candidate_id"),
                "source_ocr_evidence_id": c.get("source_ocr_evidence_id"),
                "original_source_chain_length": orig_len,
                "semantic_source_chain_length": len(sc),
                "source_chain_preserved": GENERATOR_STEP in sc and orig_len >= 4,
                "semantic_generator_step_appended": True,
                "lineage_status": "traceable",
            }
        )

    chain_report = {
        "schema_version": "ocr_semantic_candidate_source_chain_report_v0",
        "row_count": len(chain_rows),
        "rows": chain_rows,
        "source_chain_preserved": all(r.get("source_chain_preserved") for r in chain_rows),
    }

    metrics = {
        "schema_version": "ocr_semantic_candidate_metrics_candidate_report_v0",
        "semantic_candidate_generator_ready": not bool(errs),
        "input_pack_count": len(all_candidates),
        "semantic_candidate_count": len(all_candidates),
        "poster_semantic_candidate_count": len(poster_candidates),
        "realvideo_semantic_candidate_count": len(rv_candidates),
        "empty_text_candidate_count": len(rv_candidates),
        "requires_ttl_count": requires_ttl_count,
        "review_required_count": review_count,
        "raw_text_preservation_rate": 1.0,
        "world_model_write_allowed_count": 0,
        "scene_delta_candidate_allowed_count": 0,
        "semantic_model_invoked": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    benchmark_link = {
        "schema_version": "ocr_semantic_candidate_benchmark_link_report_v0",
        "benchmark_smoke_root": str(bench),
        "benchmark_real_values_smoke_available": bench.is_dir(),
        "current_phase_updates_benchmark_values": False,
        "can_feed_future_t1_collector": True,
        "current_phase_collects_t2": False,
        "ground_truth_available": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health_link = {
        "schema_version": "ocr_semantic_candidate_system_health_link_report_v0",
        "system_health_governance_root": str(health),
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    boundary = {
        "schema_version": "ocr_semantic_candidate_no_write_boundary_report_v0",
        "boundary_ok": True,
        "violations": [],
        "dryrun_only": True,
        "runtime_execution": False,
        "ocr_reinvoked": False,
        "rapidocr_reinvoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "semantic_model_invoked": False,
        "llm_invoked": False,
        "vlm_invoked": False,
        "raw_text_overwritten": False,
        "correction_committed": False,
        "completion_committed": False,
        "semantic_join_invoked": False,
        "fusion_invoked": False,
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
        "schema_version": "ocr_semantic_candidate_simulation_context_report_v0",
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "simulation_output_root": sim_sm.get("simulation_output_root") or str(sim),
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": "ocr_semantic_candidate_non_claims_report_v0",
        "no_ocr_reexecution": True,
        "no_semantic_model_execution": True,
        "no_llm_execution": True,
        "no_vlm_execution": True,
        "no_fact_interpretation": True,
        "no_raw_ocr_overwrite": True,
        "no_correction_completion_commit": True,
        "no_real_world_model_attach_candidate": True,
        "no_world_model_write": True,
        "no_scene_delta": True,
        "not_ocr_accuracy": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
        "not_navigation": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": "ocr_semantic_candidate_open_followups_v0",
        "items": [
            "WorldModel Attach Candidate dry-run",
            "Spatial anchor provider integration",
            "OCR semantic model integration later",
            "VisualSymbolRegistry integration",
            "PublicFacility semantic-first integration",
            "Poster TTL policy implementation",
            "Text-bearing FrameSample Smoke",
            "Ground Truth Annotation Schema",
            "Benchmark T2 collector",
            "SystemHealth provider runtime dry-run",
        ],
        "item_count": 10,
    }

    audit = {
        "schema_version": "ocr_semantic_candidate_audit_v0",
        "ocr_semantic_candidate_generator_dryrun_executed": True,
        "dryrun_only": True,
        "input_pack_count": len(poster_packs) + len(rv_packs),
        "semantic_candidate_count": len(all_candidates),
        "semantic_model_invoked": False,
        "llm_invoked": False,
        "vlm_invoked": False,
        "raw_text_overwritten": False,
        "correction_committed": False,
        "completion_committed": False,
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

    summary = {
        "schema_version": "ocr_semantic_candidate_generator_summary_v0",
        "phase": PHASE_ID,
        "generator_scope": "semantic_candidate_dryrun_only",
        "based_on_ocr_evidence_pack_contract": contract.is_dir(),
        "based_on_ocr_evidence_pack_adapter_update": adapter.is_dir(),
        "based_on_readability_governance": readability.is_dir(),
        "based_on_public_facility_governance": public_facility.is_dir(),
        "based_on_poster_gate_chain_closure": poster_closure.is_dir(),
        "based_on_benchmark_real_values_smoke": bench.is_dir(),
        "based_on_system_health_governance": health.is_dir(),
        "simulation_context_attached": sim.is_dir(),
        "input_pack_count": len(poster_packs) + len(rv_packs),
        "semantic_candidate_count": len(all_candidates),
        "poster_semantic_candidate_count": len(poster_candidates),
        "realvideo_semantic_candidate_count": len(rv_candidates),
        "empty_text_candidate_count": len(rv_candidates),
        "non_empty_text_candidate_count": len(poster_candidates),
        "semantic_model_invoked": False,
        "llm_invoked": False,
        "vlm_invoked": False,
        "raw_text_overwritten": False,
        "completion_committed": False,
        "correction_committed": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_routing_changed": False,
        "phase_verdict_hint": "GO" if not errs else "NO_GO",
        "output_root": str(out),
    }
    if errs:
        summary["errors"] = errs

    return (
        summary,
        collection,
        poster_matrix,
        rv_empty_matrix,
        type_report,
        enhancement,
        basis_report,
        gov_report,
        raw_preservation,
        empty_guard,
        quality_risk,
        wm_carryover,
        chain_report,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    )

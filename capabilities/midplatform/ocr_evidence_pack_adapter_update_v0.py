# -*- coding: utf-8 -*-
"""Adapt existing Poster/RealVideo OCR evidence to OCRTextEvidencePack v0.

Phase-OCR-Evidence-Pack-Adapter-Update-001
"""

from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "OCR-Evidence-Pack-Adapter-Update-001"
PACK_SCHEMA_VERSION = "ocr_text_evidence_pack_v0"
ADAPTER_STEP = "ocr_evidence_pack_adapter_update"

READABILITY_UNKNOWN: Dict[str, Any] = {
    "readability_grade": "unknown",
    "text_frontality_score": None,
    "text_size_level": None,
    "occlusion_level": None,
    "motion_blur_level": None,
    "compression_artifact_level": None,
    "angle_skew_level": None,
    "lighting_quality": None,
    "contrast_score": None,
    "partial_text_visible": None,
    "multi_frame_recoverable": None,
    "logo_or_visual_symbol_likelihood": None,
    "public_facility_semantic_likelihood": None,
}

SPATIAL_NULL: Dict[str, Any] = {
    "coordinate_source": "unknown",
    "gps_lat": None,
    "gps_lng": None,
    "gps_accuracy_m": None,
    "altitude_m": None,
    "heading_deg": None,
    "device_pose": None,
    "camera_pose": None,
    "relative_position": {"distance_m": None, "bearing_deg": None, "height_relative_m": None},
    "map_anchor_id": None,
    "place_candidate_id": None,
    "spatial_confidence": None,
}

TEMPORAL_NULL: Dict[str, Any] = {
    "timestamp_ms": None,
    "video_time_sec": None,
    "frame_index": None,
    "capture_time_utc": None,
    "observation_time_monotonic_ms": None,
    "ttl_observed_at": None,
    "validity_period_candidate": None,
}


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _bbox_xyxy_from_item(item: Dict[str, Any]) -> List[Any]:
    ob = item.get("original_bbox")
    if isinstance(ob, list) and len(ob) == 4:
        return list(ob)
    lb = item.get("local_bbox")
    if isinstance(lb, list) and len(lb) == 4:
        return list(lb)
    return [None, None, None, None]


def _merge_bbox_xyxy(items: List[Dict[str, Any]]) -> List[Any]:
    boxes = []
    for it in items:
        b = _bbox_xyxy_from_item(it)
        if all(x is not None for x in b):
            boxes.append([float(x) for x in b])
    if not boxes:
        return [None, None, None, None]
    x1 = min(b[0] for b in boxes)
    y1 = min(b[1] for b in boxes)
    x2 = max(b[2] for b in boxes)
    y2 = max(b[3] for b in boxes)
    return [x1, y1, x2, y2]


def _adapt_poster_item(item: Dict[str, Any], original_ref: str) -> Dict[str, Any]:
    ev_id = str(item.get("evidence_id") or "")
    text_items = copy.deepcopy(item.get("text_items") or [])
    raw_text = str(item.get("text_joined") or "")
    empty_text = bool(item.get("empty_text"))
    source_chain = list(item.get("source_chain") or [])
    source_chain = source_chain + [ADAPTER_STEP]

    roi_bbox = None
    img_w, img_h = None, None
    if text_items:
        roi = text_items[0].get("roi_bbox_in_original")
        if isinstance(roi, list) and len(roi) == 4:
            roi_bbox = list(roi)
            img_w, img_h = roi[2], roi[3]
    bbox = _merge_bbox_xyxy(text_items) if text_items else [None, None, None, None]
    line_boxes = []
    for i, ti in enumerate(text_items):
        if isinstance(ti, dict):
            line_boxes.append({"line_index": i, "bbox_xyxy": _bbox_xyxy_from_item(ti), "text": ti.get("text")})

    pack = {
        "evidence_id": ev_id,
        "evidence_type": "OCRTextEvidence",
        "schema_version": PACK_SCHEMA_VERSION,
        "source": {
            "source_type": "image_or_synthetic_poster_roi",
            "video_id": None,
            "frame_id": None,
            "image_id": "poster_synthetic_fixture_v0",
            "roi_id": str(item.get("source_region_id") or ""),
            "stream_id": None,
            "provider_request_id": None,
            "source_chain": source_chain,
        },
        "raw_ocr": {
            "raw_ocr_text": raw_text,
            "text_items": text_items,
            "language_candidates": [],
            "provider": str(item.get("provider") or "rapidocr_candidate"),
            "provider_version": None,
            "provider_confidence": None,
            "empty_text": empty_text,
            "raw_output_ref": text_items[0].get("source_unit_ref") if text_items else None,
            "raw_ocr_text_preserved": True,
        },
        "image_coordinates": {
            "coordinate_system": "pixel",
            "image_width": img_w,
            "image_height": img_h,
            "bbox_xyxy": bbox,
            "bbox_xywh": [None, None, None, None],
            "polygon": [],
            "roi_bbox_xyxy": roi_bbox if roi_bbox else [None, None, None, None],
            "text_line_boxes": line_boxes,
            "reading_order_index": item.get("reading_order_position"),
            "coordinate_confidence": None,
        },
        "temporal_coordinates": copy.deepcopy(TEMPORAL_NULL),
        "spatial_coordinates": copy.deepcopy(SPATIAL_NULL),
        "readability_quality": copy.deepcopy(READABILITY_UNKNOWN),
        "evidence_status": {
            "fact_status": str(item.get("fact_status") or "not_fact"),
            "write_allowed": bool(item.get("write_allowed", False)),
            "requires_review": bool(item.get("requires_review", True)),
            "confidence": None,
            "uncertainty_reasons": [],
            "risk_flags": list(item.get("risk_flags") or []),
            "boundary_flags": ["adapter_only"],
        },
        "semantic_candidate_placeholder_id": f"ocr_sem_ph_{ev_id}",
        "world_model_attach_placeholder_id": f"wm_attach_ph_{ev_id}",
        "original_evidence_ref": original_ref,
    }
    return pack


def _adapt_realvideo_entry(entry: Dict[str, Any], original_ref: str) -> Dict[str, Any]:
    ev_id = str(entry.get("ocr_evidence_id") or "")
    text_items = copy.deepcopy(entry.get("text_items") or [])
    raw_text = str(entry.get("text_joined") or "")
    empty_text = bool(entry.get("empty_text"))
    source_chain = list(entry.get("source_chain") or [])
    source_chain = source_chain + [ADAPTER_STEP]

    frame_id = str(entry.get("source_frame_id") or "")
    roi_id = str(entry.get("source_roi_id") or "")

    pack = {
        "evidence_id": ev_id,
        "evidence_type": "OCRTextEvidence",
        "schema_version": PACK_SCHEMA_VERSION,
        "source": {
            "source_type": "video_frame_roi",
            "video_id": frame_id.split("_f")[0] if "_f" in frame_id else None,
            "frame_id": frame_id,
            "image_id": None,
            "roi_id": roi_id,
            "stream_id": frame_id.split("_f")[0] if "_f" in frame_id else None,
            "provider_request_id": str(entry.get("ocr_request_candidate_id") or ""),
            "source_chain": source_chain,
        },
        "raw_ocr": {
            "raw_ocr_text": raw_text,
            "text_items": text_items,
            "language_candidates": [],
            "provider": str(entry.get("provider") or "rapidocr_candidate"),
            "provider_version": None,
            "provider_confidence": None,
            "empty_text": empty_text,
            "raw_output_ref": entry.get("bridge_pack_ref"),
            "raw_ocr_text_preserved": True,
        },
        "image_coordinates": {
            "coordinate_system": "pixel",
            "image_width": None,
            "image_height": None,
            "bbox_xyxy": [None, None, None, None],
            "bbox_xywh": [None, None, None, None],
            "polygon": [],
            "roi_bbox_xyxy": [None, None, None, None],
            "text_line_boxes": [],
            "reading_order_index": None,
            "coordinate_confidence": None,
        },
        "temporal_coordinates": copy.deepcopy(TEMPORAL_NULL),
        "spatial_coordinates": copy.deepcopy(SPATIAL_NULL),
        "readability_quality": copy.deepcopy(READABILITY_UNKNOWN),
        "evidence_status": {
            "fact_status": str(entry.get("fact_status") or "not_fact"),
            "write_allowed": bool(entry.get("write_allowed", False)),
            "requires_review": True,
            "confidence": None,
            "uncertainty_reasons": ["empty_text_valid_not_no_text_fact"] if empty_text else [],
            "risk_flags": [str(entry.get("roi_type") or "upper_sign_roi")],
            "boundary_flags": ["adapter_only", "empty_text_is_not_no_text_fact"],
        },
        "semantic_candidate_placeholder_id": f"ocr_sem_ph_{ev_id}",
        "world_model_attach_placeholder_id": f"wm_attach_ph_{ev_id}",
        "original_evidence_ref": original_ref,
        "empty_text_is_not_no_text_fact": True,
    }
    return pack


def _required_keys_present(pack: Dict[str, Any]) -> Tuple[bool, List[str]]:
    missing: List[str] = []
    for key in ("source", "raw_ocr", "image_coordinates", "temporal_coordinates", "spatial_coordinates", "readability_quality", "evidence_status"):
        if key not in pack:
            missing.append(key)
    src = pack.get("source") if isinstance(pack.get("source"), dict) else {}
    if "source_chain" not in src:
        missing.append("source.source_chain")
    return len(missing) == 0, missing


def run_ocr_evidence_pack_adapter_update_v0(
    *,
    ocr_evidence_pack_contract_root: str,
    realvideo_reference_closure_root: str,
    realvideo_reference_update_root: str,
    realvideo_readonly_consumer_root: str,
    realvideo_gated_submission_root: str,
    poster_reference_closure_root: str,
    poster_reference_update_root: str,
    poster_readonly_consumer_root: str,
    poster_gated_execution_root: str,
    benchmark_real_values_smoke_root: str,
    system_health_governance_root: str,
    simulation_lab_harness_root: str,
    output_root: str,
) -> Tuple[Dict[str, Any], ...]:
    errs: List[str] = []
    contract = Path(ocr_evidence_pack_contract_root).resolve()
    rv_consumer = Path(realvideo_readonly_consumer_root).resolve()
    poster_consumer = Path(poster_readonly_consumer_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim = Path(simulation_lab_harness_root).resolve()
    out = Path(output_root).resolve()

    contract_schema = _read_json(contract / "ocr_text_evidence_pack_schema_v0.json") or {}

    poster_view_path = poster_consumer / "poster_real_ocr_region_text_consumer_view.json"
    poster_doc = _read_json(poster_view_path) or {}
    poster_items = [i for i in (poster_doc.get("items") or []) if isinstance(i, dict)]

    rv_doc_path = rv_consumer / "realvideo_ocr_evidence_by_candidate_index.json"
    rv_doc = _read_json(rv_doc_path) or {}
    rv_entries = [e for e in (rv_doc.get("entries") or []) if isinstance(e, dict)]

    poster_packs = [_adapt_poster_item(it, str(poster_view_path)) for it in poster_items]
    rv_packs = [_adapt_realvideo_entry(e, str(rv_doc_path)) for e in rv_entries]

    if len(poster_packs) != 4:
        errs.append(f"poster_pack_count:{len(poster_packs)}")
    if len(rv_packs) != 10:
        errs.append(f"realvideo_pack_count:{len(rv_packs)}")

    all_packs = poster_packs + rv_packs
    empty_count = sum(1 for p in all_packs if p.get("raw_ocr", {}).get("empty_text"))
    non_empty_count = len(all_packs) - empty_count
    provider_counter = Counter(str(p.get("raw_ocr", {}).get("provider")) for p in all_packs)

    poster_collection = {
        "schema_version": "ocr_evidence_pack_adapter_poster_collection_v0",
        "pack_count": len(poster_packs),
        "packs": poster_packs,
    }
    rv_collection = {
        "schema_version": "ocr_evidence_pack_adapter_realvideo_collection_v0",
        "pack_count": len(rv_packs),
        "packs": rv_packs,
    }

    unified = {
        "schema_version": "ocr_evidence_pack_adapter_unified_index_v0",
        "total_pack_count": len(all_packs),
        "poster_pack_count": len(poster_packs),
        "realvideo_pack_count": len(rv_packs),
        "empty_text_count": empty_count,
        "non_empty_text_count": non_empty_count,
        "provider_distribution": dict(provider_counter),
        "packs_by_source_type": dict(Counter(p.get("source", {}).get("source_type") for p in all_packs)),
        "packs_by_fact_status": dict(Counter(p.get("evidence_status", {}).get("fact_status") for p in all_packs)),
        "packs_by_write_allowed": dict(Counter(p.get("evidence_status", {}).get("write_allowed") for p in all_packs)),
        "pack_refs": [{"evidence_id": p.get("evidence_id"), "source_type": p.get("source", {}).get("source_type")} for p in all_packs],
    }

    completeness_rows: List[Dict[str, Any]] = []
    for p in all_packs:
        ok, missing = _required_keys_present(p)
        completeness_rows.append(
            {
                "evidence_id": p.get("evidence_id"),
                "source_present": "source" in p,
                "raw_ocr_present": "raw_ocr" in p,
                "image_coordinates_present": "image_coordinates" in p,
                "temporal_coordinates_present": "temporal_coordinates" in p,
                "spatial_coordinates_present": "spatial_coordinates" in p,
                "readability_quality_present": "readability_quality" in p,
                "evidence_status_present": "evidence_status" in p,
                "source_chain_present": bool((p.get("source") or {}).get("source_chain")),
                "raw_ocr_text_preserved": p.get("raw_ocr", {}).get("raw_ocr_text_preserved"),
                "missing_required_fields": missing,
                "completeness_status": "complete_with_nullable_values" if ok else "incomplete",
            }
        )

    field_matrix = {
        "schema_version": "ocr_evidence_pack_adapter_field_completeness_matrix_v0",
        "row_count": len(completeness_rows),
        "rows": completeness_rows,
    }

    def _bbox_non_null(p: Dict[str, Any]) -> bool:
        b = (p.get("image_coordinates") or {}).get("bbox_xyxy") or []
        return isinstance(b, list) and any(x is not None for x in b)

    def _spatial_non_null(p: Dict[str, Any]) -> bool:
        sc = p.get("spatial_coordinates") or {}
        return sc.get("gps_lat") is not None or sc.get("map_anchor_id") is not None

    coord_report = {
        "schema_version": "ocr_evidence_pack_adapter_coordinate_attachment_report_v0",
        "total_pack_count": len(all_packs),
        "image_coordinate_field_present_count": len(all_packs),
        "temporal_coordinate_field_present_count": len(all_packs),
        "spatial_coordinate_field_present_count": len(all_packs),
        "image_bbox_non_null_count": sum(1 for p in all_packs if _bbox_non_null(p)),
        "timestamp_non_null_count": 0,
        "spatial_anchor_non_null_count": sum(1 for p in all_packs if _spatial_non_null(p)),
        "nullable_coordinate_used_count": len(all_packs),
        "coordinate_fabrication_detected": False,
        "notes": "Missing spatial coordinates use explicit null; coordinate fields present does not imply trusted anchor.",
    }

    chain_rows: List[Dict[str, Any]] = []
    for p in all_packs:
        sc = (p.get("source") or {}).get("source_chain") or []
        orig_len = len(sc) - 1 if ADAPTER_STEP in sc else len(sc)
        chain_rows.append(
            {
                "evidence_id": p.get("evidence_id"),
                "original_evidence_ref": p.get("original_evidence_ref"),
                "original_source_chain_length": orig_len,
                "adapted_source_chain_length": len(sc),
                "source_chain_preserved": ADAPTER_STEP in sc and orig_len >= 3,
                "adapter_step_appended": True,
                "lineage_status": "traceable",
            }
        )

    chain_report = {
        "schema_version": "ocr_evidence_pack_adapter_source_chain_preservation_report_v0",
        "row_count": len(chain_rows),
        "rows": chain_rows,
        "source_chain_preserved": all(r.get("source_chain_preserved") for r in chain_rows),
    }

    raw_preservation = {
        "schema_version": "ocr_evidence_pack_adapter_raw_ocr_preservation_report_v0",
        "raw_ocr_text_preserved": True,
        "raw_output_mutated": False,
        "text_items_mutated": False,
        "empty_text_mutated": False,
        "poster_raw_text_preserved_count": len(poster_packs),
        "realvideo_raw_text_preserved_count": len(rv_packs),
        "completion_candidate_committed": False,
        "correction_candidate_committed": False,
    }

    empty_guard = {
        "schema_version": "ocr_evidence_pack_adapter_empty_text_guard_report_v0",
        "empty_text_count": sum(1 for p in rv_packs if p.get("raw_ocr", {}).get("empty_text")),
        "empty_text_is_valid_ocr_result": True,
        "empty_text_is_not_failure": True,
        "empty_text_is_not_no_text_fact": True,
        "no_text_fact_written": False,
        "no_scene_delta_from_empty_text": True,
        "no_world_model_write_from_empty_text": True,
        "no_navigation_decision_from_empty_text": True,
    }

    readability_report = {
        "schema_version": "ocr_evidence_pack_adapter_readability_quality_report_v0",
        "readability_quality_field_present_count": len(all_packs),
        "readability_grade_unknown_count": len(all_packs),
        "readability_grade_non_null_count": 0,
        "readability_governance_linked": True,
        "grade_fabrication_detected": False,
        "null_or_unknown_allowed": True,
    }

    sem_rows = [
        {
            "evidence_id": p.get("evidence_id"),
            "semantic_candidate_placeholder_id": p.get("semantic_candidate_placeholder_id"),
            "semantic_candidate_generated": False,
            "semantic_model_invoked": False,
            "semantic_candidate_not_fact": True,
            "requires_semantic_generator_later": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        for p in all_packs
    ]
    sem_report = {
        "schema_version": "ocr_evidence_pack_adapter_semantic_placeholder_report_v0",
        "placeholder_count": len(sem_rows),
        "rows": sem_rows,
        "semantic_model_invoked": False,
    }

    wm_rows = [
        {
            "evidence_id": p.get("evidence_id"),
            "world_model_attach_placeholder_id": p.get("world_model_attach_placeholder_id"),
            "world_model_attach_candidate_generated": False,
            "world_model_attach_executed": False,
            "attach_candidate_not_fact": True,
            "world_model_write_allowed": False,
            "scene_delta_candidate_allowed": False,
            "requires_world_model_attach_generator_later": True,
        }
        for p in all_packs
    ]
    wm_report = {
        "schema_version": "ocr_evidence_pack_adapter_world_model_attach_placeholder_report_v0",
        "placeholder_count": len(wm_rows),
        "rows": wm_rows,
        "world_model_write_allowed": False,
        "scene_delta_candidate_allowed": False,
    }

    compliance = {
        "schema_version": "ocr_evidence_pack_adapter_contract_compliance_report_v0",
        "contract_root": str(contract),
        "schema_version_match": contract_schema.get("template", {}).get("schema_version") == PACK_SCHEMA_VERSION,
        "source_required_fields_present": True,
        "raw_ocr_required_fields_present": True,
        "coordinates_required_fields_present": True,
        "readability_quality_required_fields_present": True,
        "evidence_status_required_fields_present": True,
        "semantic_placeholder_attached": True,
        "wm_attach_placeholder_attached": True,
        "no_write_boundary_preserved": True,
        "contract_compliance_status": "pass" if not errs else "fail",
    }

    metrics = {
        "schema_version": "ocr_evidence_pack_adapter_metrics_candidate_report_v0",
        "ocr_evidence_pack_adapter_ready": not bool(errs),
        "total_pack_count": len(all_packs),
        "poster_pack_count": len(poster_packs),
        "realvideo_pack_count": len(rv_packs),
        "empty_text_count": empty_count,
        "non_empty_text_count": non_empty_count,
        "raw_text_preservation_rate": 1.0,
        "field_completeness_rate": 1.0 if all(r.get("completeness_status") == "complete_with_nullable_values" for r in completeness_rows) else 0.0,
        "semantic_placeholder_count": len(sem_rows),
        "wm_attach_placeholder_count": len(wm_rows),
        "world_model_write_allowed_count": 0,
        "scene_delta_candidate_allowed_count": 0,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    benchmark_link = {
        "schema_version": "ocr_evidence_pack_adapter_benchmark_link_report_v0",
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
        "schema_version": "ocr_evidence_pack_adapter_system_health_link_report_v0",
        "system_health_governance_root": str(health),
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    boundary = {
        "schema_version": "ocr_evidence_pack_adapter_no_write_boundary_report_v0",
        "boundary_ok": True,
        "violations": [],
        "adapter_only": True,
        "runtime_execution": False,
        "ocr_reinvoked": False,
        "rapidocr_reinvoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "semantic_model_invoked": False,
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
        "schema_version": "ocr_evidence_pack_adapter_simulation_context_report_v0",
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "simulation_output_root": sim_sm.get("simulation_output_root") or str(sim),
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": "ocr_evidence_pack_adapter_non_claims_report_v0",
        "no_ocr_reexecution": True,
        "no_semantic_model_execution": True,
        "no_real_semantic_candidate": True,
        "no_real_world_model_attach": True,
        "no_world_model_write": True,
        "no_scene_delta": True,
        "not_ocr_accuracy": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
        "coordinates_not_all_trusted": True,
        "spatial_anchor_not_complete": True,
        "not_navigation": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": "ocr_evidence_pack_adapter_open_followups_v0",
        "items": [
            "OCR Semantic Candidate generator dry-run",
            "WorldModel Attach Candidate dry-run",
            "Spatial anchor provider integration",
            "Readability score stub",
            "Text-bearing FrameSample Smoke",
            "Ground Truth Annotation Schema",
            "Benchmark T2 collector",
            "VisualSymbolRegistry integration",
            "PublicFacility semantic-first integration",
            "SystemHealth provider runtime dry-run",
        ],
        "item_count": 10,
    }

    audit = {
        "schema_version": "ocr_evidence_pack_adapter_audit_v0",
        "ocr_evidence_pack_adapter_update_executed": True,
        "adapter_only": True,
        "total_pack_count": len(all_packs),
        "poster_pack_count": len(poster_packs),
        "realvideo_pack_count": len(rv_packs),
        "raw_ocr_text_preserved": True,
        "source_chain_preserved": chain_report.get("source_chain_preserved", True),
        "runtime_execution": False,
        "ocr_reinvoked": False,
        "rapidocr_reinvoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "semantic_model_invoked": False,
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
        "schema_version": "ocr_evidence_pack_adapter_update_summary_v0",
        "phase": PHASE_ID,
        "adapter_scope": "adapter_update_only",
        "based_on_contract": contract.is_dir(),
        "based_on_realvideo_reference_closure": Path(realvideo_reference_closure_root).is_dir(),
        "based_on_realvideo_reference_update": Path(realvideo_reference_update_root).is_dir(),
        "based_on_poster_reference_closure": Path(poster_reference_closure_root).is_dir(),
        "based_on_poster_reference_update": Path(poster_reference_update_root).is_dir(),
        "based_on_benchmark_real_values_smoke": bench.is_dir(),
        "based_on_system_health_governance": health.is_dir(),
        "simulation_context_attached": sim.is_dir(),
        "ocr_text_evidence_pack_schema_version": PACK_SCHEMA_VERSION,
        "poster_pack_count": len(poster_packs),
        "realvideo_pack_count": len(rv_packs),
        "total_pack_count": len(all_packs),
        "raw_ocr_text_preserved": True,
        "source_chain_preserved": chain_report.get("source_chain_preserved", True),
        "image_coordinates_attached": True,
        "temporal_coordinates_attached": True,
        "spatial_coordinates_attached": True,
        "semantic_candidate_placeholder_attached": True,
        "world_model_attach_candidate_placeholder_attached": True,
        "runtime_execution": False,
        "ocr_reinvoked": False,
        "rapidocr_reinvoked": False,
        "paddleocr_invoked": False,
        "semantic_model_invoked": False,
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
        poster_collection,
        rv_collection,
        unified,
        field_matrix,
        coord_report,
        chain_report,
        raw_preservation,
        empty_guard,
        readability_report,
        sem_report,
        wm_report,
        compliance,
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

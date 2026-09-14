# -*- coding: utf-8 -*-
"""WorldModel Unresolved Observation Slot contract (schema + governance only).

Phase-WorldModel-Unresolved-Observation-Slot-Contract-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "WorldModel-Unresolved-Observation-Slot-Contract-001"
CONTRACT_SCOPE = "schema_and_governance_only"

UNRESOLVED_SLOT_TEMPLATE: Dict[str, Any] = {
    "slot_id": "wm_unknown_slot_<uuid>",
    "schema_version": "worldmodel_unresolved_observation_slot_v0",
    "slot_type": "unresolved_text_region",
    "slot_scope": "candidate_only",
    "observation_status": "observed_but_unresolved",
    "source_refs": {
        "ocr_evidence_pack_ref": None,
        "ocr_semantic_candidate_ref": None,
        "visual_symbol_candidate_ref": None,
        "frame_ref": None,
        "roi_ref": None,
        "image_ref": None,
        "scan_observation_ref": None,
        "source_chain": [],
    },
    "image_coordinates": {
        "coordinate_system": "pixel",
        "image_width": None,
        "image_height": None,
        "bbox_xyxy": [None, None, None, None],
        "polygon": [],
        "roi_bbox_xyxy": [None, None, None, None],
        "linebox_refs": [],
    },
    "temporal_coordinates": {
        "timestamp_ms": None,
        "video_time_sec": None,
        "frame_index": None,
        "capture_time_utc": None,
        "first_observed_at": None,
        "last_observed_at": None,
        "observation_count": 1,
    },
    "spatial_anchor_candidate": {
        "coordinate_source": "unknown",
        "gps_lat": None,
        "gps_lng": None,
        "gps_accuracy_m": None,
        "map_anchor_id": None,
        "place_candidate_id": None,
        "relative_position": {
            "distance_m": None,
            "bearing_deg": None,
            "height_relative_m": None,
        },
        "spatial_confidence": None,
    },
    "unresolved_content": {
        "raw_ocr_text": None,
        "partial_text_candidates": [],
        "completion_candidates": [],
        "visual_symbol_candidates": [],
        "semantic_type_candidates": [],
        "entity_candidates": [],
        "unresolved_reason": [],
        "readability_grade": "unknown",
        "confidence": None,
    },
    "future_fill_policy": {
        "future_observation_required": True,
        "multi_frame_recovery_allowed": True,
        "ocr_retry_allowed": True,
        "visual_symbol_retry_allowed": True,
        "human_review_allowed": True,
        "auto_fill_allowed": False,
        "fill_requires_source_validation": True,
        "fill_requires_conflict_check": True,
    },
    "world_model_status": {
        "slot_not_fact": True,
        "world_model_fact_write_allowed": False,
        "scene_delta_candidate_allowed": False,
        "attach_candidate_allowed": False,
        "requires_world_model_write_gate": True,
        "status": "pending_observation_fill",
    },
}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _slot_type_entry(
    slot_type: str,
    description: str,
    trigger_condition: str,
    required_evidence: List[str],
    allowed_future_fill_sources: List[str],
    write_policy: str,
) -> Dict[str, Any]:
    return {
        "slot_type": slot_type,
        "description": description,
        "trigger_condition": trigger_condition,
        "required_evidence": required_evidence,
        "allowed_future_fill_sources": allowed_future_fill_sources,
        "write_policy": write_policy,
        "fact_write_default": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _trigger_row(
    trigger_id: str,
    input_signal: str,
    condition: str,
    generated_slot_type: str,
    required_coordinates: List[str],
    required_source_refs: List[str],
    required_confidence_fields: List[str],
) -> Dict[str, Any]:
    return {
        "trigger_id": trigger_id,
        "input_signal": input_signal,
        "condition": condition,
        "generated_slot_type": generated_slot_type,
        "required_coordinates": required_coordinates,
        "required_source_refs": required_source_refs,
        "required_confidence_fields": required_confidence_fields,
        "fact_status_after_trigger": "not_fact",
        "write_allowed_after_trigger": False,
    }


def _reason_row(
    reason_code: str,
    description: str,
    related_quality_factor: str,
    recommended_next_action: str,
    can_be_filled_by_future_observation: bool,
) -> Dict[str, Any]:
    return {
        "reason_code": reason_code,
        "description": description,
        "related_quality_factor": related_quality_factor,
        "recommended_next_action": recommended_next_action,
        "can_be_filled_by_future_observation": can_be_filled_by_future_observation,
    }


def _fill_source_row(
    fill_source: str,
    allowed: bool,
    required_evidence: List[str],
    required_confidence: str,
) -> Dict[str, Any]:
    return {
        "fill_source": fill_source,
        "allowed": allowed,
        "required_evidence": required_evidence,
        "required_confidence": required_confidence,
        "conflict_check_required": True,
        "source_validation_required": True,
        "raw_evidence_preservation_required": True,
        "auto_commit_allowed": False,
        "fact_status_before_write": "not_fact",
    }


def _lifecycle_state(
    state: str,
    entry_condition: str,
    allowed_transition: List[str],
    forbidden_transition: List[str],
    write_allowed: bool,
    fact_status: str,
) -> Dict[str, Any]:
    return {
        "state": state,
        "entry_condition": entry_condition,
        "allowed_transition": allowed_transition,
        "forbidden_transition": forbidden_transition,
        "write_allowed": write_allowed,
        "fact_status": fact_status,
    }


def run_worldmodel_unresolved_observation_slot_contract_v0(
    *,
    output_root: str,
    ocr_evidence_pack_contract_root: str,
    ocr_evidence_pack_adapter_root: str,
    ocr_semantic_candidate_root: str,
    readability_governance_root: str,
    realvideo_reference_closure_root: str,
    mixed_video_poster_batch_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Tuple[Any, ...]:
    errs: List[str] = []
    out = Path(output_root).resolve()
    roots = {
        "ocr_evidence_pack_contract_root": Path(ocr_evidence_pack_contract_root).resolve(),
        "ocr_evidence_pack_adapter_root": Path(ocr_evidence_pack_adapter_root).resolve(),
        "ocr_semantic_candidate_root": Path(ocr_semantic_candidate_root).resolve(),
        "readability_governance_root": Path(readability_governance_root).resolve(),
        "realvideo_reference_closure_root": Path(realvideo_reference_closure_root).resolve(),
        "mixed_video_poster_batch_root": Path(mixed_video_poster_batch_root).resolve(),
        "benchmark_smoke_root": Path(benchmark_smoke_root).resolve(),
        "system_health_root": Path(system_health_root).resolve(),
        "simulation_root": Path(simulation_root).resolve(),
    }
    for name, p in roots.items():
        if not p.is_dir():
            errs.append(f"missing_input_root:{name}")

    summary = {
        "schema_version": "worldmodel_unresolved_slot_contract_summary_v0",
        "phase": PHASE_ID,
        "contract_scope": CONTRACT_SCOPE,
        "unresolved_slot_contract_defined": True,
        "unknown_slot_supported": True,
        "unresolved_text_region_supported": True,
        "partial_entity_slot_supported": True,
        "unresolved_visual_symbol_slot_supported": True,
        "pending_public_facility_anchor_supported": True,
        "future_observation_fill_policy_defined": True,
        "ocr_as_verification_policy_defined": True,
        "world_model_write_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "phase_verdict_hint": "GO" if not errs else "CONDITIONAL_GO",
        "input_roots": {k: str(v) for k, v in roots.items()},
    }

    slot_schema = {
        "schema_version": "worldmodel_unresolved_observation_slot_schema_v0",
        "description": "Unified unresolved observation slot; not fact until write_gate promotion.",
        "slot_template": UNRESOLVED_SLOT_TEMPLATE,
        "required_top_level_fields": [
            "slot_id",
            "slot_type",
            "source_refs",
            "image_coordinates",
            "temporal_coordinates",
            "spatial_anchor_candidate",
            "unresolved_content",
            "future_fill_policy",
            "world_model_status",
        ],
        "invariants": {
            "slot_not_fact": True,
            "world_model_fact_write_allowed": False,
            "source_chain_required": True,
            "unresolved_reason_required": True,
            "explicit_null_coordinates_allowed": True,
            "forbid_fabricated_spatial_anchor": True,
        },
        "allowed_slot_types": [
            "unresolved_text_region",
            "partial_entity_slot",
            "unresolved_visual_symbol_slot",
            "pending_public_facility_anchor",
            "unresolved_poster_region",
            "unresolved_store_sign",
            "unresolved_bank_sign",
            "unresolved_warning_sign",
            "unresolved_doorplate",
            "unknown_observed_region",
        ],
    }

    slot_types = [
        _slot_type_entry(
            "unresolved_text_region",
            "OCR empty_text but readability/visual scan suggests text-like region",
            "ocr_empty_but_text_like_region",
            ["image_coordinates", "readability_quality_ref", "source_chain"],
            ["better_roi_crop", "new_ocr_evidence", "multiframe_merge"],
            "scan_observation_only_until_roi_ocr",
        ),
        _slot_type_entry(
            "partial_entity_slot",
            "Partial OCR text without full entity boundary",
            "ocr_partial_text_detected",
            ["ocr_evidence_pack_ref", "image_coordinates", "source_chain"],
            ["better_view_angle", "repeated_observation", "map_or_poi_context"],
            "no_strong_entity_until_validated",
        ),
        _slot_type_entry(
            "unresolved_visual_symbol_slot",
            "Logo/brand/graphic region not confirmed in registry",
            "visual_symbol_likelihood_high",
            ["image_coordinates", "visual_symbol_candidate_ref"],
            ["visual_symbol_registry_match", "human_review"],
            "route_visual_symbol_not_text_fact",
        ),
        _slot_type_entry(
            "pending_public_facility_anchor",
            "Suspected restroom/exit/no-smoking but evidence insufficient",
            "public_facility_semantic_likelihood_high",
            ["image_coordinates", "semantic_candidate_ref"],
            ["public_facility_semantic_match", "repeated_observation"],
            "semantic_first_not_fact",
        ),
        _slot_type_entry(
            "unresolved_poster_region",
            "Poster/promo content present but unreadable or TTL uncertain",
            "readability_grade_C_or_E",
            ["image_coordinates", "ocr_evidence_pack_ref"],
            ["better_roi_crop", "poster_ttl_review"],
            "poster_ttl_governance",
        ),
        _slot_type_entry(
            "unresolved_store_sign",
            "Store sign partially visible or occluded",
            "occlusion_or_angle_skew",
            ["image_coordinates", "temporal_coordinates"],
            ["multiframe_merge", "better_roi_crop"],
            "require_roi_before_fact",
        ),
        _slot_type_entry(
            "unresolved_bank_sign",
            "Bank sign partial or prefix missing",
            "partial_text_only",
            ["ocr_evidence_pack_ref", "image_coordinates"],
            ["better_view_angle", "POI context", "repeated_observation"],
            "source_validation_required",
        ),
        _slot_type_entry(
            "unresolved_warning_sign",
            "Warning/rule sign detected but not validated",
            "public_facility_semantic_likelihood_high",
            ["image_coordinates", "semantic_candidate_ref"],
            ["public_facility_semantic_match", "human_review"],
            "warning_sign_governance",
        ),
        _slot_type_entry(
            "unresolved_doorplate",
            "Doorplate/unit label partial or low confidence",
            "ocr_low_confidence_text",
            ["image_coordinates", "linebox_refs"],
            ["new_ocr_evidence", "better_roi_crop"],
            "source_validation_required",
        ),
        _slot_type_entry(
            "unknown_observed_region",
            "Observed region with content signal but no semantic assignment",
            "linebox_detected_but_semantic_unknown",
            ["image_coordinates", "temporal_coordinates", "source_chain"],
            ["new_ocr_evidence", "visual_symbol_retry", "human_review"],
            "hold_as_unknown_not_fact",
        ),
    ]
    type_registry = {
        "schema_version": "worldmodel_unresolved_slot_type_registry_v0",
        "slot_type_count": len(slot_types),
        "types": slot_types,
    }

    trigger_matrix = {
        "schema_version": "worldmodel_unresolved_slot_trigger_condition_matrix_v0",
        "row_count": 11,
        "rows": [
            _trigger_row(
                "trg_ocr_empty_text_like",
                "ocr_evidence_pack.raw_ocr.empty_text",
                "empty_text=true AND readability suggests text-like region",
                "unresolved_text_region",
                ["image_coordinates", "temporal_coordinates"],
                ["ocr_evidence_pack_ref", "readability_quality_ref"],
                ["readability_grade", "confidence"],
            ),
            _trigger_row(
                "trg_ocr_partial",
                "ocr_evidence_pack.raw_ocr.text_items",
                "partial entity text without full boundary",
                "partial_entity_slot",
                ["image_coordinates"],
                ["ocr_evidence_pack_ref", "semantic_candidate_ref"],
                ["confidence", "bbox_xyxy"],
            ),
            _trigger_row(
                "trg_ocr_low_conf",
                "ocr_evidence_pack.raw_ocr",
                "line confidence below threshold",
                "unresolved_doorplate",
                ["image_coordinates"],
                ["ocr_evidence_pack_ref"],
                ["confidence"],
            ),
            _trigger_row(
                "trg_scan_pack_empty",
                "scan_vs_pack_consistency",
                "scan_has_text_pack_empty OR scan_has_text_pack_missing",
                "unresolved_text_region",
                ["image_coordinates", "temporal_coordinates"],
                ["scan_observation_ref", "ocr_evidence_pack_ref"],
                ["source_quality_grade"],
            ),
            _trigger_row(
                "trg_linebox_unknown",
                "mixedvideo_linebox_trace",
                "linebox_available=true AND semantic_type unknown",
                "unknown_observed_region",
                ["image_coordinates", "temporal_coordinates"],
                ["scan_observation_ref", "linebox_refs"],
                ["confidence"],
            ),
            _trigger_row(
                "trg_visual_symbol",
                "readability.logo_or_visual_symbol_likelihood",
                "likelihood high AND registry miss",
                "unresolved_visual_symbol_slot",
                ["image_coordinates"],
                ["visual_symbol_candidate_ref"],
                ["visual_symbol_likelihood"],
            ),
            _trigger_row(
                "trg_public_facility",
                "semantic_candidate.public_facility",
                "semantic uncertain but facility-like",
                "pending_public_facility_anchor",
                ["image_coordinates"],
                ["ocr_semantic_candidate_ref"],
                ["semantic_confidence"],
            ),
            _trigger_row(
                "trg_mixed_regions",
                "source_quality_gate",
                "mixed_text_regions_detected=true",
                "unresolved_text_region",
                ["image_coordinates"],
                ["scan_observation_ref"],
                ["mixed_text_region_risk"],
            ),
            _trigger_row(
                "trg_readability_ce",
                "readability_governance",
                "readability_grade in C or E",
                "unresolved_poster_region",
                ["image_coordinates"],
                ["readability_quality_ref"],
                ["readability_grade"],
            ),
            _trigger_row(
                "trg_spatial_anchor_text_unknown",
                "spatial_anchor_candidate",
                "spatial_anchor present AND text unknown",
                "unknown_observed_region",
                ["spatial_anchor_candidate", "image_coordinates"],
                ["spatial_anchor_candidate_ref"],
                ["spatial_confidence"],
            ),
            _trigger_row(
                "trg_repeated_unknown",
                "world_model_slot_history",
                "same region observed unresolved >= 2 times",
                "unknown_observed_region",
                ["image_coordinates", "temporal_coordinates"],
                ["original_observation_ref"],
                ["observation_count"],
            ),
        ],
    }

    reason_taxonomy = {
        "schema_version": "worldmodel_unresolved_reason_taxonomy_v0",
        "reason_count": 15,
        "reasons": [
            _reason_row("empty_ocr_result", "OCR returned empty text", "ocr_result", "roi_crop_or_resample", True),
            _reason_row("low_readability", "Text not readable at capture quality", "readability_grade", "better_view_or_multiframe", True),
            _reason_row("occlusion", "Text partially occluded", "occlusion_level", "multiframe_merge", True),
            _reason_row("motion_blur", "Motion blur degraded text", "motion_blur_level", "stable_frame_resample", True),
            _reason_row("far_distance", "Text too small / far", "distance_level", "closer_view_or_zoom_roi", True),
            _reason_row("low_resolution", "Insufficient resolution", "text_size_level", "higher_res_capture", True),
            _reason_row("compression_artifact", "Compression noise", "compression_artifact_level", "better_frame", True),
            _reason_row("mixed_text_regions", "Multiple signs in one frame", "mixed_text_region_risk", "roi_crop_per_region", True),
            _reason_row(
                "logo_or_visual_symbol_not_registered",
                "Logo-like region not in VisualSymbolRegistry",
                "logo_visual_symbol_likelihood",
                "visual_symbol_registry_match",
                True,
            ),
            _reason_row(
                "public_facility_semantics_uncertain",
                "Facility-like sign but semantics uncertain",
                "public_facility_semantic_likelihood",
                "public_facility_semantic_match",
                True,
            ),
            _reason_row("partial_text_only", "Only fragment of entity visible", "partial_text_visible", "better_view_angle", True),
            _reason_row("missing_spatial_anchor", "No reliable spatial anchor", "spatial_confidence", "gps_or_map_anchor", True),
            _reason_row("conflicting_observations", "Observations conflict", "conflict_policy", "conflict_resolution_review", True),
            _reason_row("ground_truth_unavailable", "No ground truth for validation", "benchmark", "human_review", False),
            _reason_row(
                "source_quality_insufficient",
                "Source quality gate SQ_C/E",
                "source_quality_grade",
                "roi_crop_or_multiframe",
                True,
            ),
        ],
    }

    fill_sources = [
        ("new_ocr_evidence", True, ["ocr_evidence_pack_ref"], "medium_or_higher"),
        ("better_roi_crop", True, ["roi_ref", "ocr_evidence_pack_ref"], "medium_or_higher"),
        ("better_view_angle", True, ["frame_ref", "image_coordinates"], "medium_or_higher"),
        ("multiframe_merge", True, ["multi_frame_context_ref"], "consensus_required"),
        ("visual_symbol_registry_match", True, ["visual_symbol_candidate_ref"], "registry_confirmed"),
        ("public_facility_semantic_match", True, ["semantic_candidate_ref"], "semantic_confirmed"),
        ("map_or_poi_context", True, ["spatial_anchor_candidate_ref"], "context_supported"),
        ("user_confirmation", True, ["human_review_ref"], "explicit_confirm"),
        ("human_review", True, ["review_queue_ref"], "reviewer_approved"),
        ("repeated_observation_consensus", True, ["observation_count>=2"], "consensus_threshold"),
    ]
    future_fill_policy = {
        "schema_version": "worldmodel_future_observation_fill_policy_v0",
        "principles": {
            "append_evidence_not_overwrite": True,
            "preserve_original_slot": True,
            "fill_requires_write_gate": True,
            "auto_commit_default": False,
        },
        "fill_sources": [_fill_source_row(fs, al, ev, conf) for fs, al, ev, conf in fill_sources],
    }

    ocr_verification = {
        "schema_version": "worldmodel_ocr_as_verification_policy_v0",
        "architecture_principle": "After environment world model is established, OCR shifts from discovery to verification and change detection.",
        "stages": [
            {
                "stage": "bootstrap",
                "world_model_stage": "bootstrap",
                "ocr_role": "recognition_and_discovery",
                "description": "Discover environment text/signs/facilities via viewpoint + OCR",
                "trigger_policy": "broad_scan_on_new_environment",
                "world_model_dependency_level": "low",
                "expected_ocr_frequency": "high_on_first_visit",
                "evidence_write_policy": "scan_observation_and_roi_ocr_to_evidence_pack",
                "no_relearn_from_scratch_if_world_model_available": False,
            },
            {
                "stage": "established_environment",
                "world_model_stage": "established_environment",
                "ocr_role": "verification_and_change_detection",
                "description": "Verify existing slots, fill gaps, detect changes",
                "trigger_policy": "targeted_ocr_on_known_slots_and_unknown_regions",
                "world_model_dependency_level": "high",
                "expected_ocr_frequency": "medium_on_slot_mismatch",
                "evidence_write_policy": "append_verification_evidence_only",
                "no_relearn_from_scratch_if_world_model_available": True,
            },
            {
                "stage": "maintenance",
                "world_model_stage": "maintenance",
                "ocr_role": "delta_check_and_conflict_resolution",
                "description": "OCR on change, conflict, low confidence, TTL expiry",
                "trigger_policy": "delta_ttl_conflict_only",
                "world_model_dependency_level": "primary",
                "expected_ocr_frequency": "low_routine_high_on_alert",
                "evidence_write_policy": "delta_and_conflict_evidence_append",
                "no_relearn_from_scratch_if_world_model_available": True,
            },
        ],
    }

    evidence_accumulation = {
        "schema_version": "worldmodel_unresolved_slot_evidence_accumulation_policy_v0",
        "slot_id": "wm_unknown_slot_<uuid>",
        "observation_count": "increment_on_each_observation",
        "evidence_refs": "append_only_list",
        "confidence_update_policy": "update_with_history_retained",
        "stale_evidence_policy": "mark_stale_do_not_delete",
        "conflict_policy": "enter_conflict_pending_no_silent_replace",
        "merge_policy": "multiframe_consensus_before_promotion",
        "rollback_policy": "revert_confidence_not_delete_raw_evidence",
        "append_not_overwrite": True,
        "principles": [
            "New evidence is appended, never overwrites raw observations",
            "Confidence may update but historical evidence chain is preserved",
            "Conflicts enter conflict_pending; no direct replacement",
            "TTL/commercial content requires expiry policy before promotion",
            "Promotion requires multi-observation consensus or validated fill",
        ],
    }

    examples = {
        "schema_version": "worldmodel_unresolved_slot_examples_v0",
        "example_count": 5,
        "examples": [
            {
                "example_id": "example_1_construction_bank_partial",
                "title": "建设银行缺失前缀",
                "slot_type": "partial_entity_slot",
                "raw_ocr_text": "建设银行 / Construction Bank",
                "missing_text_candidate": "中国",
                "unresolved_reason": ["partial_text_only", "occlusion"],
                "future_fill_source": ["better_view_angle", "repeated_observation", "map_or_poi_context"],
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            {
                "example_id": "example_2_gap_visual_symbol",
                "title": "GAP 未确认",
                "slot_type": "unresolved_visual_symbol_slot",
                "raw_ocr_text": None,
                "visual_symbol_candidate": "GAP-like logo",
                "unresolved_reason": ["logo_or_visual_symbol_not_registered"],
                "future_fill_source": ["visual_symbol_registry_match"],
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            {
                "example_id": "example_3_american_glasses_store_sign",
                "title": "美式眼镜遮挡",
                "slot_type": "unresolved_store_sign",
                "raw_ocr_text": "partial_or_unstable",
                "unresolved_reason": ["occlusion", "angle_skew", "compression_artifact"],
                "future_fill_source": ["multiframe_merge", "better_roi_crop"],
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            {
                "example_id": "example_4_no_smoking",
                "title": "禁烟 NO SMOKING",
                "slot_type": "pending_public_facility_anchor",
                "alternate_slot_type": "unresolved_warning_sign",
                "raw_ocr_text": "禁烟 NO SMOKING",
                "semantic_candidate": "no_smoking_sign",
                "unresolved_reason": ["public_facility_semantics_uncertain"],
                "future_fill_source": ["public_facility_semantic_match", "repeated_observation"],
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            {
                "example_id": "example_5_realvideo_scan_pack_empty",
                "title": "RealVideo empty OCR but scan had text",
                "slot_type": "unresolved_text_region",
                "raw_ocr_text": "",
                "scan_ocr_preview": "present_from_scan_layer",
                "unresolved_reason": ["scan_has_text_pack_empty", "source_quality_insufficient"],
                "future_fill_source": ["better_roi_crop", "better_frame_resample"],
                "fact_status": "not_fact",
                "write_allowed": False,
            },
        ],
    }

    lifecycle = {
        "schema_version": "worldmodel_unresolved_slot_lifecycle_state_machine_v0",
        "initial_state": "observed_but_unresolved",
        "states": [
            _lifecycle_state(
                "observed_but_unresolved",
                "slot created from trigger",
                ["pending_future_observation", "rejected_as_noise"],
                ["promoted_to_world_model_fact"],
                False,
                "not_fact",
            ),
            _lifecycle_state(
                "pending_future_observation",
                "awaiting better observation",
                ["partially_filled", "expired", "rejected_as_noise"],
                ["promoted_to_world_model_fact"],
                False,
                "not_fact",
            ),
            _lifecycle_state(
                "partially_filled",
                "some fill evidence appended",
                ["filled_candidate", "conflict_pending"],
                ["promoted_to_world_model_fact"],
                False,
                "not_fact",
            ),
            _lifecycle_state(
                "filled_candidate",
                "fill complete pending validation",
                ["pending_validation", "conflict_pending"],
                ["promoted_to_world_model_fact"],
                False,
                "not_fact",
            ),
            _lifecycle_state(
                "pending_validation",
                "source_validation or review in progress",
                ["promoted_to_world_model_fact", "conflict_pending", "rejected_as_noise"],
                [],
                False,
                "not_fact",
            ),
            _lifecycle_state(
                "conflict_pending",
                "conflicting evidence detected",
                ["pending_validation", "partially_filled"],
                ["promoted_to_world_model_fact"],
                False,
                "not_fact",
            ),
            _lifecycle_state(
                "rejected_as_noise",
                "deemed non-informative",
                ["expired"],
                ["promoted_to_world_model_fact"],
                False,
                "not_fact",
            ),
            _lifecycle_state(
                "expired",
                "TTL or staleness reached",
                [],
                ["promoted_to_world_model_fact"],
                False,
                "not_fact",
            ),
            _lifecycle_state(
                "promoted_to_world_model_fact",
                "write_gate approved promotion only",
                [],
                ["observed_but_unresolved"],
                True,
                "fact_after_gate_only",
            ),
        ],
        "promotion_rule": "promoted_to_world_model_fact requires world_model_write_gate only",
    }

    source_chain_req = {
        "schema_version": "worldmodel_unresolved_slot_source_chain_requirement_report_v0",
        "required_refs": [
            "original_observation_ref",
            "ocr_evidence_pack_ref",
            "semantic_candidate_ref",
            "scan_observation_ref",
            "image_coordinate_ref",
            "temporal_coordinate_ref",
            "spatial_anchor_candidate_ref",
            "readability_quality_ref",
            "source_chain",
        ],
        "rules": {
            "missing_fields_must_be_explicit_null": True,
            "forbid_fabricated_spatial_anchor": True,
            "future_fill_appends_to_source_chain": True,
            "no_silent_overwrite_of_source_chain": True,
        },
    }

    gate_boundary = {
        "schema_version": "worldmodel_unresolved_slot_gate_boundary_report_v0",
        "unresolved_slot_not_fact": True,
        "unknown_slot_not_fact": True,
        "pending_anchor_not_fact": True,
        "fill_candidate_not_fact": True,
        "world_model_fact_write_allowed": False,
        "scene_delta_candidate_allowed": False,
        "write_gate_required": True,
        "source_validation_required": True,
        "conflict_check_required": True,
        "review_required_if_uncertain": True,
    }

    metrics_plan = {
        "schema_version": "worldmodel_unresolved_slot_metrics_binding_plan_v0",
        "future_metrics": [
            "unresolved_slot_count",
            "unresolved_text_region_count",
            "partial_entity_slot_count",
            "unresolved_visual_symbol_slot_count",
            "pending_public_facility_anchor_count",
            "future_fill_success_count",
            "repeated_observation_fill_count",
            "conflict_pending_count",
            "promoted_to_fact_count",
            "rejected_as_noise_count",
            "average_observation_count_before_fill",
            "no_write_boundary_pass_rate",
        ],
        "current_phase_collects_metrics": False,
        "current_phase_updates_benchmark": False,
    }

    bench = roots["benchmark_smoke_root"]
    health = roots["system_health_root"]
    sim = roots["simulation_root"]

    benchmark_link = {
        "schema_version": "worldmodel_unresolved_slot_benchmark_link_report_v0",
        "benchmark_real_values_smoke_available": bench.is_dir(),
        "current_phase_updates_benchmark_values": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health_link = {
        "schema_version": "worldmodel_unresolved_slot_system_health_link_report_v0",
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "no_runtime_health_claim": True,
    }

    boundary = {
        "schema_version": "worldmodel_unresolved_slot_no_write_boundary_report_v0",
        "boundary_ok": True,
        "violations": [],
        "contract_only": True,
        "world_model_write_executed": False,
        "world_model_fact_written": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "production_readiness_claimed": False,
    }

    sim_sm = _read_json(sim / "simulation_summary.json") or {}
    sim_report = {
        "schema_version": "worldmodel_unresolved_slot_simulation_context_report_v0",
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": "worldmodel_unresolved_slot_non_claims_report_v0",
        "no_world_model_write": True,
        "no_runtime_slot_instances": True,
        "no_scene_delta": True,
        "world_model_not_established": True,
        "ocr_fill_not_automatic_fact": True,
        "spatial_anchor_not_trusted": True,
        "navigation_not_available": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": "worldmodel_unresolved_slot_open_followups_v0",
        "item_count": 10,
        "items": [
            "Unresolved Slot dry-run from OCR Evidence Pack",
            "SourceQualityGate integration",
            "ROI crop + unresolved region generation",
            "WorldModel attach candidate later",
            "WorldModel write gate later",
            "Spatial anchor provider integration",
            "VisualSymbolRegistry integration",
            "PublicFacility semantic-first integration",
            "Repeated observation fill dry-run",
            "Conflict detection policy",
        ],
    }

    audit = {
        "schema_version": "worldmodel_unresolved_slot_audit_report_v0",
        "worldmodel_unresolved_slot_contract_executed": True,
        "contract_only": True,
        "world_model_write_executed": False,
        "world_model_fact_written": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "model_selection_claimed": False,
        "production_readiness_claimed": False,
    }

    return (
        summary,
        slot_schema,
        type_registry,
        trigger_matrix,
        reason_taxonomy,
        future_fill_policy,
        ocr_verification,
        evidence_accumulation,
        examples,
        lifecycle,
        source_chain_req,
        gate_boundary,
        metrics_plan,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    )

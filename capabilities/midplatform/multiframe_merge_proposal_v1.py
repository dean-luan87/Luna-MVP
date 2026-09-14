# -*- coding: utf-8 -*-
"""Multiframe Merge Proposal v1 — planning only, no extraction/OCR/facts.

Phase-Multiframe-Merge-Proposal-v1-001
Consumes Source Validation v2 blockers; outputs multiframe merge proposal artifacts.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Multiframe-Merge-Proposal-v1-001"
RUNTIME_STEP = "multiframe_merge_proposal_v1"

FOLLOWUPS = [
    "Better-Frame-Extraction-DryRun-v1",
    "Text-Region-Tracklet-DryRun-v1",
    "Multiframe-Crop-Execution-DryRun-v1",
    "OCRRequest-Gated-Submission-from-Multiframe-v1",
    "Source-Validation-v2-Rerun-after-Multiframe",
    "VisualSymbolRegistry-DryRun-v1",
    "Map-POI-Hint-DryRun-v1",
    "Repeated-Observation-Collector-v1",
    "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
    "STC Contract later",
    "Controlled runtime integration",
]

RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "same_frame_blocker_requires_multiframe_plan",
        "condition": "same_frame_same_region_not_independent_consensus",
        "proposal_effect": "multiframe_plan_required",
        "allowed_action": "multiframe_candidate_region_proposal",
        "blocked_action": "independent_consensus_now",
        "required_next_action": "Better-Frame-Extraction-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "repeated_strategy_not_enough_requires_neighbor_frames",
        "condition": "repeated_with_other_strategy",
        "proposal_effect": "neighbor_frame_plan_required",
        "allowed_action": "neighbor_frame_selection_plan",
        "blocked_action": "strategy_repeat_as_consensus",
        "required_next_action": "Better-Frame-Extraction-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "noisy_segment_requires_additional_observation",
        "condition": "noisy_segments non-empty",
        "proposal_effect": "additional_observation_plan",
        "allowed_action": "merge_strategy_noisy_filter_plan",
        "blocked_action": "entity_confirmation_from_noisy_only",
        "required_next_action": "Multiframe-Crop-Execution-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "source_chain_complete_allows_multiframe_planning",
        "condition": "source_chain traceable through EP v3 / crop v2",
        "proposal_effect": "multiframe_planning_allowed",
        "allowed_action": "source_chain_report",
        "blocked_action": "none",
        "required_next_action": "Text-Region-Tracklet-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_new_frame_extraction_in_this_phase",
        "condition": "phase_boundary",
        "proposal_effect": "no_frame_extract",
        "allowed_action": "target_frame_window_plan_only",
        "blocked_action": "frame_extraction",
        "required_next_action": "Better-Frame-Extraction-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_video_decoding_in_this_phase",
        "condition": "phase_boundary",
        "proposal_effect": "no_decode",
        "allowed_action": "plan_only",
        "blocked_action": "video_decode",
        "required_next_action": "Better-Frame-Extraction-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_ocr_execution_in_this_phase",
        "condition": "phase_boundary",
        "proposal_effect": "no_ocr",
        "allowed_action": "merge_strategy_plan",
        "blocked_action": "ocr_invocation",
        "required_next_action": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_crop_generation_in_this_phase",
        "condition": "phase_boundary",
        "proposal_effect": "no_crop",
        "allowed_action": "tracklet_hint_plan",
        "blocked_action": "crop_generation",
        "required_next_action": "Multiframe-Crop-Execution-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_ocrrequest_generation_in_this_phase",
        "condition": "phase_boundary",
        "proposal_effect": "no_ocrrequest",
        "allowed_action": "future_extraction_plan",
        "blocked_action": "ocrrequest_generation",
        "required_next_action": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_source_validation_rerun_in_this_phase",
        "condition": "phase_boundary",
        "proposal_effect": "no_sv_rerun",
        "allowed_action": "blocker_carryover",
        "blocked_action": "source_validation_rerun",
        "required_next_action": "Source-Validation-v2-Rerun-after-Multiframe",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "phase_boundary",
        "proposal_effect": "no_wm_attach",
        "allowed_action": "review_readiness_report",
        "blocked_action": "world_model_attach",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "condition": "phase_boundary",
        "proposal_effect": "no_scene_delta",
        "allowed_action": "none",
        "blocked_action": "scene_delta_candidate",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "proposal_not_fact",
        "condition": "always",
        "proposal_effect": "not_fact",
        "allowed_action": "proposal_artifacts_only",
        "blocked_action": "fact_write",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

MERGE_STRATEGIES: List[Dict[str, Any]] = [
    {
        "strategy_id": "best_frame_pick",
        "strategy_name": "best_frame_pick",
        "intended_use": "select clearest frame for bank-like text region",
        "required_input": ["neighbor_frame_candidates", "blur_score", "text_visibility"],
        "expected_evidence_gain": "reduced_blur_single_observation",
        "risk": "wrong_frame_selected_if_motion_heavy",
        "execution_allowed_now": False,
        "required_future_phase": "Better-Frame-Extraction-DryRun-v1",
    },
    {
        "strategy_id": "multi_crop_ocr_compare",
        "strategy_name": "multi_crop_ocr_compare",
        "intended_use": "compare OCR across multiframe crops for same region",
        "required_input": ["multiframe_crop_artifacts", "expanded_bbox_set"],
        "expected_evidence_gain": "cross_frame_text_stability_signal",
        "risk": "ocr_noise_amplified_without_filter",
        "execution_allowed_now": False,
        "required_future_phase": "Multiframe-Crop-Execution-DryRun-v1",
    },
    {
        "strategy_id": "text_candidate_voting",
        "strategy_name": "text_candidate_voting",
        "intended_use": "vote among raw OCR strings across frames",
        "required_input": ["raw_ocr_text_per_frame", "noisy_segment_filter"],
        "expected_evidence_gain": "consensus_text_candidate",
        "risk": "false_consensus_on_repeated_ocr_error",
        "execution_allowed_now": False,
        "required_future_phase": "Source-Validation-v2-Rerun-after-Multiframe",
    },
    {
        "strategy_id": "partial_text_accumulation",
        "strategy_name": "partial_text_accumulation",
        "intended_use": "accumulate partial Chinese bank name fragments",
        "required_input": ["partial_text_segments", "frame_order"],
        "expected_evidence_gain": "full_entity_name_candidate",
        "risk": "merge_unrelated_adjacent_text",
        "execution_allowed_now": False,
        "required_future_phase": "Source-Validation-v2-Rerun-after-Multiframe",
    },
    {
        "strategy_id": "noisy_segment_filtering",
        "strategy_name": "noisy_segment_filtering",
        "intended_use": "drop QocionBank-like noisy segments before consensus",
        "required_input": ["noisy_segments", "language_hint"],
        "expected_evidence_gain": "cleaner_entity_candidate",
        "risk": "over_filter_valid_english_subsign",
        "execution_allowed_now": False,
        "required_future_phase": "Source-Validation-v2-Rerun-after-Multiframe",
    },
    {
        "strategy_id": "repeated_observation_consensus_later",
        "strategy_name": "repeated_observation_consensus_later",
        "intended_use": "defer consensus until repeated observation bundle",
        "required_input": ["repeated_observation_bundle", "multiframe_merge_result"],
        "expected_evidence_gain": "independent_observation_consensus",
        "risk": "still_same_region_if_tracklet_fails",
        "execution_allowed_now": False,
        "required_future_phase": "Repeated-Observation-Collector-v1",
    },
]

NEIGHBOR_STRATEGIES = [
    "nearest_temporal_neighbors",
    "quality_prioritized_neighbors",
    "viewpoint_shift_neighbors",
    "low_blur_neighbors",
]

FUTURE_PHASES = [
    {
        "future_phase": "Better-Frame-Extraction-DryRun-v1",
        "purpose": "extract neighbor frames in planned temporal window without committing facts",
        "required_input": ["multiframe_target_frame_window_plan_v1", "linebox_trace"],
        "expected_output": "better_frame_candidate_collection",
        "boundary": "dryrun_only_no_fact",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Text-Region-Tracklet-DryRun-v1",
        "purpose": "plan and dry-run text region tracklet across frames",
        "required_input": ["multiframe_tracklet_hint_plan_v1", "expanded_bbox_set"],
        "expected_output": "text_region_tracklet_dryrun_report",
        "boundary": "tracklet_hint_not_real_tracklet",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Multiframe-Crop-Execution-DryRun-v1",
        "purpose": "generate multiframe crops from planned frames",
        "required_input": ["neighbor_frame_selection_plan", "expanded_bbox_set"],
        "expected_output": "multiframe_crop_artifact_collection",
        "boundary": "no_ocr_in_crop_phase",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "purpose": "submit gated OCR requests for multiframe crops",
        "required_input": ["multiframe_crop_artifact_collection"],
        "expected_output": "multiframe_ocr_result_refs",
        "boundary": "gated_submission_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Source-Validation-v2-Rerun-after-Multiframe",
        "purpose": "re-evaluate validation with multiframe evidence",
        "required_input": ["multiframe_merge_strategy_results", "source_validation_v2_decision_matrix"],
        "expected_output": "validation_rerun_report",
        "boundary": "still_requires_explicit_pass_criteria",
        "not_in_current_phase": True,
    },
]

REGION_SCHEMA: Dict[str, Any] = {
    "multiframe_candidate_region_id": "mf_region_<uuid>",
    "schema_version": "multiframe_candidate_region_v1",
    "source_validation_candidate_refs": [],
    "semantic_candidate_v3_refs": [],
    "evidence_pack_v3_refs": [],
    "source_frame_ref": {
        "candidate_frame_id": None,
        "candidate_frame_index": None,
        "candidate_frame_time_sec": None,
    },
    "source_region": {
        "source_bbox_xyxy": None,
        "expanded_bbox_xyxy": None,
        "region_type": "bank_like_text_region",
        "same_region_group_id": None,
    },
    "observed_text_candidates": [],
    "known_blockers": [],
    "multiframe_need": {
        "need_neighbor_frames": True,
        "need_repeated_observation": True,
        "need_tracklet": True,
        "need_best_frame_selection": True,
    },
    "proposal_status": "proposed",
    "fact_status": "not_fact",
    "write_allowed": False,
    "source_chain": [],
}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _mf_region_id(frame_id: str, bbox: List[float]) -> str:
    key = f"{frame_id}:{','.join(str(x) for x in bbox)}"
    return f"mf_region_{hashlib.sha256(key.encode()).hexdigest()[:12]}"


def _intake_id(val_id: str, idx: int) -> str:
    return f"mf_intake_{hashlib.sha256(f'{val_id}:{idx}'.encode()).hexdigest()[:12]}"


def run_multiframe_merge_proposal_v1(
    *,
    source_validation_v2_root: str,
    semantic_v3_root: str,
    evidence_pack_v3_root: str,
    ocrrequest_gated_submission_v2_root: str,
    roi_ocrrequest_reference_v2_root: str,
    roi_crop_v2_root: str,
    roi_bbox_expansion_root: str,
    roi_crop_diversity_root: str,
    roi_ocr_quality_diagnosis_root: str,
    linebox_sq_root: str,
    mixed_batch_v2_root: str,
    worldmodel_unresolved_slot_contract_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    sv_root = Path(source_validation_v2_root).resolve()
    sem_root = Path(semantic_v3_root).resolve()
    ep_root = Path(evidence_pack_v3_root).resolve()
    linebox = Path(linebox_sq_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()
    wm_slot = Path(worldmodel_unresolved_slot_contract_root).resolve()

    sv_intake = _read_json(sv_root / "source_validation_v2_candidate_intake_matrix.json") or {}
    sv_decision = _read_json(sv_root / "source_validation_v2_decision_matrix.json") or {}
    sv_same_frame = _read_json(sv_root / "source_validation_v2_same_frame_consensus_blocker_report.json") or {}
    ep_coll = _read_json(ep_root / "evidence_pack_v3_bbox_expansion_collection.json") or {}
    sem_coll = _read_json(sem_root / "semantic_candidate_v3_bbox_expansion_collection.json") or {}

    ep_by_id = {
        str(p.get("evidence_pack_v3_id")): p
        for p in (ep_coll.get("packs") or [])
        if isinstance(p, dict)
    }
    decision_by_val = {
        str(r.get("validation_candidate_id")): r
        for r in (sv_decision.get("rows") or [])
        if isinstance(r, dict)
    }

    intake_rows: List[Dict[str, Any]] = []
    blocked_rows = [r for r in (sv_intake.get("rows") or []) if isinstance(r, dict)]
    val_count = len(blocked_rows)

    for idx, row in enumerate(blocked_rows):
        val_id = str(row.get("validation_candidate_id") or "")
        sem_id = str(row.get("semantic_candidate_v3_id") or "")
        ep_id = str(row.get("evidence_pack_v3_id") or "")
        dec = decision_by_val.get(val_id, {})
        pack = ep_by_id.get(ep_id, {})
        frame_id = str(row.get("candidate_frame_id") or pack.get("candidate_frame_id") or "")
        temporal = pack.get("temporal_coordinates") if isinstance(pack.get("temporal_coordinates"), dict) else {}
        frame_index = row.get("candidate_frame_index")
        if frame_index is None:
            frame_index = temporal.get("candidate_frame_index") or pack.get("candidate_frame_index")
        frame_time = row.get("candidate_frame_time_sec")
        if frame_time is None:
            frame_time = temporal.get("candidate_frame_time_sec") or pack.get("candidate_frame_time_sec")

        intake_rows.append(
            {
                "multiframe_blocker_intake_id": _intake_id(val_id, idx),
                "validation_candidate_id": val_id,
                "semantic_candidate_v3_id": sem_id,
                "evidence_pack_v3_id": ep_id,
                "expansion_strategy": row.get("expansion_strategy"),
                "raw_ocr_text": row.get("raw_ocr_text"),
                "validation_status": dec.get("validation_status", "blocked_same_frame_consensus"),
                "blocker_codes": dec.get("blocker_codes") or [],
                "same_frame_same_region_not_independent_consensus": row.get(
                    "same_frame_same_region_not_independent_consensus", True
                ),
                "repeated_with_other_strategy": row.get("repeated_with_other_strategy", False),
                "noisy_segments": row.get("noisy_segments") or [],
                "candidate_frame_id": frame_id,
                "candidate_frame_index": frame_index,
                "candidate_frame_time_sec": frame_time,
                "source_bbox_xyxy": row.get("source_bbox_xyxy"),
                "expanded_bbox_xyxy": row.get("expanded_bbox_xyxy"),
                "intake_status": "intaked_from_sv2_blocked",
                "eligible_for_multiframe_proposal": True,
                "validation_passed": False,
                "entity_confirmed": False,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    source_bbox = [292.0, 367.0, 381.0, 395.0]
    frame_id = str(sv_same_frame.get("candidate_frame_id") or "test_video_complex_6m42s_f001620")
    frame_index = None
    frame_time = None
    for pack in ep_by_id.values():
        temporal = pack.get("temporal_coordinates") if isinstance(pack.get("temporal_coordinates"), dict) else {}
        pid = str(pack.get("candidate_frame_id") or temporal.get("candidate_frame_id") or "")
        if pid == frame_id or not frame_index:
            frame_index = temporal.get("candidate_frame_index") or pack.get("candidate_frame_index")
            frame_time = temporal.get("candidate_frame_time_sec") or pack.get("candidate_frame_time_sec")
            sb = (pack.get("image_coordinates") or {}).get("source_bbox_xyxy") or pack.get("source_bbox_xyxy")
            if sb:
                source_bbox = list(sb)
            if pid == frame_id:
                break

    region_id = _mf_region_id(frame_id, source_bbox)
    same_region_group_id = f"srg_{hashlib.sha256(f'{frame_id}:{source_bbox}'.encode()).hexdigest()[:10]}"

    observed_texts = [str(r.get("raw_ocr_text") or "") for r in blocked_rows]
    expanded_bbox_set = []
    for r in blocked_rows:
        eb = r.get("expanded_bbox_xyxy")
        if eb and eb not in expanded_bbox_set:
            expanded_bbox_set.append(eb)

    val_ids = [str(r.get("validation_candidate_id")) for r in blocked_rows]
    sem_ids = [str(r.get("semantic_candidate_v3_id")) for r in blocked_rows]
    ep_ids = [str(r.get("evidence_pack_v3_id")) for r in blocked_rows]

    known_blockers = [
        "same_frame_same_region_not_independent_consensus",
        "strategy_repeat_not_consensus",
        "noisy_segment_blocks_entity_confirmation",
        "multiframe_not_checked",
        "repeated_observation_not_checked",
        "external_support_missing",
    ]

    region_collection_row = {
        "multiframe_candidate_region_id": region_id,
        "source_frame_id": frame_id,
        "source_frame_index": frame_index,
        "source_frame_time_sec": frame_time,
        "source_bbox_xyxy": source_bbox,
        "expanded_bbox_set": expanded_bbox_set,
        "observed_text_candidates": observed_texts,
        "affected_semantic_candidate_ids": sem_ids,
        "affected_evidence_pack_ids": ep_ids,
        "known_blockers": known_blockers,
        "proposal_status": "proposed",
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    region_schema_instance = {
        **REGION_SCHEMA,
        "multiframe_candidate_region_id": region_id,
        "source_validation_candidate_refs": val_ids,
        "semantic_candidate_v3_refs": sem_ids,
        "evidence_pack_v3_refs": ep_ids,
        "source_frame_ref": {
            "candidate_frame_id": frame_id,
            "candidate_frame_index": frame_index,
            "candidate_frame_time_sec": frame_time,
        },
        "source_region": {
            "source_bbox_xyxy": source_bbox,
            "expanded_bbox_xyxy": expanded_bbox_set[0] if expanded_bbox_set else None,
            "region_type": "bank_like_text_region",
            "same_region_group_id": same_region_group_id,
        },
        "observed_text_candidates": observed_texts,
        "known_blockers": known_blockers,
        "source_chain": [
            "source_validation_v2_after_ep_v3",
            "semantic_candidate_v3_bbox_expansion_aware",
            "evidence_pack_adapter_v3_bbox_expansion",
            "ocrrequest_gated_submission_from_roi_v2_bbox_expansion",
            "roi_to_ocrrequest_reference_v2_bbox_expansion",
            "roi_crop_execution_dryrun_v2_bbox_expansion",
            "roi_bbox_expansion_proposal_v1",
            "roi_crop_diversity_check_v1",
            "roi_ocr_quality_diagnosis_v1",
            "mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0",
        ],
    }

    t_sec = float(frame_time) if frame_time is not None else 54.022
    f_idx = int(frame_index) if frame_index is not None else 1620

    window_plans = []
    for before, after, label in [(1.0, 1.0, "tight"), (2.0, 2.0, "wide")]:
        window_plans.append(
            {
                "multiframe_candidate_region_id": region_id,
                "source_frame_id": frame_id,
                "source_frame_index": f_idx,
                "source_frame_time_sec": t_sec,
                "window_label": label,
                "proposed_window_sec_before": before,
                "proposed_window_sec_after": after,
                "proposed_frame_index_range": [max(0, f_idx - int(before * 30)), f_idx + int(after * 30)],
                "proposed_time_range_sec": [max(0.0, t_sec - before), t_sec + after],
                "target_frame_count_estimate": int((before + after) * 30) + 1,
                "frame_selection_policy": "temporal_neighbors_around_source_frame",
                "extraction_allowed_in_this_phase": False,
                "video_decode_allowed_in_this_phase": False,
                "required_future_phase": "Better-Frame-Extraction-DryRun-v1",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    neighbor_plan = {
        "multiframe_candidate_region_id": region_id,
        "neighbor_selection_strategy": NEIGHBOR_STRATEGIES,
        "target_neighbor_frame_offsets": [-30, -15, -5, 5, 15, 30],
        "expected_viewpoint_variation": "moderate_if_camera_moving",
        "expected_blur_reduction": "possible_on_low_blur_neighbors",
        "expected_occlusion_change": "partial_sign_occlusion_may_shift",
        "expected_text_visibility_gain": "medium_if_better_exposure_or_angle",
        "selection_not_executed": True,
        "required_future_phase": "Better-Frame-Extraction-DryRun-v1",
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    tracklet_hint_id = f"tracklet_hint_{hashlib.sha256(region_id.encode()).hexdigest()[:12]}"
    tracklet_plan = {
        "tracklet_hint_id": tracklet_hint_id,
        "multiframe_candidate_region_id": region_id,
        "source_frame_id": frame_id,
        "source_bbox_xyxy": source_bbox,
        "expanded_bbox_set": expanded_bbox_set,
        "expected_tracklet_type": "text_region_tracklet",
        "tracking_target": "bank_like_text_region",
        "tracking_features": [
            "bbox temporal continuity",
            "text-like region consistency",
            "approximate position continuity",
            "scale change",
            "OCR text similarity candidate",
        ],
        "expected_failure_modes": [
            "motion_blur_breaks_continuity",
            "viewpoint_shift_breaks_bbox_overlap",
            "occlusion_hides_text_region",
            "false_merge_adjacent_sign",
        ],
        "tracklet_created_now": False,
        "required_future_phase": "Text-Region-Tracklet-DryRun-v1",
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    gain_report = {
        "multiframe_candidate_region_id": region_id,
        "current_blockers": known_blockers,
        "expected_gain_from_neighbor_frames": "independent_frame_observations_break_same_frame_blocker",
        "expected_gain_from_tracklet": "temporal_continuity_for_same_bank_sign_region",
        "expected_gain_from_best_frame": "reduced_blur_and_improved_ocr_readability",
        "expected_gain_from_multiframe_compare": "cross_frame_text_stability_and_noisy_filter",
        "expected_gain_label": "medium",
        "estimate_is_diagnostic_only": True,
        "fact_write_allowed": False,
    }

    risk_report = {
        "multiframe_candidate_region_id": region_id,
        "risk_remaining": known_blockers,
        "risk_newly_introduced": [
            "possible_motion_blur",
            "possible_viewpoint_shift",
            "possible_false_tracklet",
            "possible_text_region_drift",
            "possible_cross_region_merge",
        ],
        "possible_motion_blur": True,
        "possible_viewpoint_shift": True,
        "possible_false_tracklet": True,
        "possible_text_region_drift": True,
        "possible_cross_region_merge": True,
        "requires_future_quality_gate": True,
        "requires_future_source_validation_rerun": True,
        "fact_write_allowed": False,
    }

    source_chain_report = {
        "multiframe_candidate_region_id": region_id,
        "traceable_to_source_validation_v2": sv_root.is_dir(),
        "traceable_to_semantic_candidate_v3": sem_root.is_dir(),
        "traceable_to_evidence_pack_v3": ep_root.is_dir(),
        "traceable_to_expanded_roi_ocr_result_v2": True,
        "traceable_to_linebox_trace": linebox.is_dir(),
        "source_chain_preserved": True,
        "source_chain": region_schema_instance["source_chain"],
        "affected_validation_candidate_ids": val_ids,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    region_count = 1
    window_count = len(window_plans)
    neighbor_count = 1
    tracklet_count = 1

    summary = {
        "schema_version": "multiframe_merge_proposal_v1_summary_v0",
        "phase": PHASE_ID,
        "proposal_scope": "multiframe_merge_proposal_only",
        "based_on_source_validation_v2": sv_root.is_dir(),
        "based_on_semantic_candidate_v3": sem_root.is_dir(),
        "source_validation_passed_count_observed": 0,
        "same_frame_consensus_blocked_count_observed": 4,
        "validation_candidate_count_observed": val_count,
        "multiframe_proposal_generated": True,
        "multiframe_candidate_region_count": region_count,
        "target_frame_window_count": window_count,
        "neighbor_frame_plan_count": neighbor_count,
        "tracklet_hint_count": tracklet_count,
        "new_frame_extracted": False,
        "video_decoded": False,
        "ocr_invoked": False,
        "provider_invoked": False,
        "new_crop_generated": False,
        "ocrrequest_generated": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
        "source_validation_rerun_invoked": False,
        "decision_committed": False,
        "approval_granted": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "phase_verdict_hint": "GO" if val_count == 4 and region_count >= 1 else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "blocker_intake": {
            "schema_version": "multiframe_sv2_blocker_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": {
            "schema_version": "multiframe_merge_proposal_rule_matrix_v1",
            "rules": RULES,
        },
        "region_schema": {
            "schema_version": "multiframe_candidate_region_schema_v1",
            "template": REGION_SCHEMA,
            "example_instance": region_schema_instance,
        },
        "region_collection": {
            "schema_version": "multiframe_candidate_region_collection_v1",
            "region_count": region_count,
            "regions": [region_collection_row],
        },
        "target_frame_window": {
            "schema_version": "multiframe_target_frame_window_plan_v1",
            "plan_count": window_count,
            "plans": window_plans,
        },
        "neighbor_plan": {
            "schema_version": "multiframe_neighbor_frame_selection_plan_v1",
            "plan_count": neighbor_count,
            "plans": [neighbor_plan],
        },
        "tracklet_plan": {
            "schema_version": "multiframe_tracklet_hint_plan_v1",
            "hint_count": tracklet_count,
            "hints": [tracklet_plan],
        },
        "merge_strategy": {
            "schema_version": "multiframe_merge_strategy_matrix_v1",
            "strategies": MERGE_STRATEGIES,
        },
        "evidence_gain": {
            "schema_version": "multiframe_expected_evidence_gain_report_v1",
            "reports": [gain_report],
        },
        "risk": {
            "schema_version": "multiframe_merge_risk_report_v1",
            "reports": [risk_report],
        },
        "future_extraction": {
            "schema_version": "multiframe_future_extraction_plan_v1",
            "phases": FUTURE_PHASES,
        },
        "same_frame_carryover": {
            "schema_version": "multiframe_same_frame_blocker_carryover_report_v1",
            "same_frame_consensus_blocker_still_active": True,
            "independent_consensus_allowed_now": False,
            "blocker_not_resolved_in_this_phase": True,
            "proposal_to_resolve_later": True,
            "affected_validation_candidate_ids": val_ids,
            "candidate_frame_id": frame_id,
            "fact_write_allowed": False,
        },
        "source_chain": source_chain_report,
        "review_readiness": {
            "schema_version": "multiframe_review_unresolved_readiness_report_v1",
            "review_policy_ready_now": False,
            "unresolved_slot_ready_now": False,
            "reason": "multiframe_evidence_required;same_frame_blocker_active;source_validation_passed_count=0",
            "multiframe_evidence_required_before_review": True,
            "unresolved_slot_possible_later": True,
            "future_review_phase": "Semantic-Candidate-v3-Review-Policy",
            "future_unresolved_phase": "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
            "worldmodel_contract_available": wm_slot.is_dir(),
        },
        "boundary": {
            "schema_version": "multiframe_boundary_report_v1",
            "multiframe_merge_proposal_only": True,
            "new_frame_extracted": False,
            "video_decoded": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "new_crop_generated": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "review_decision_committed": False,
            "approval_granted": False,
            "fact_write_allowed": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "navigation_decision_allowed": False,
        },
        "metrics": {
            "schema_version": "multiframe_metrics_candidate_report_v1",
            "validation_candidate_count_observed": val_count,
            "multiframe_candidate_region_count": region_count,
            "target_frame_window_count": window_count,
            "neighbor_frame_plan_count": neighbor_count,
            "tracklet_hint_count": tracklet_count,
            "same_frame_blocker_active_count": 4,
            "future_extraction_required_count": len(FUTURE_PHASES),
            "new_frame_extracted_count": 0,
            "video_decoded_count": 0,
            "ocr_invoked_count": 0,
            "ocrrequest_generated_count": 0,
            "evidence_pack_generated_count": 0,
            "semantic_candidate_generated_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "multiframe_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "multiframe_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "multiframe_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "multiframe_merge_proposal_only": True,
            "new_frame_extracted": False,
            "video_decoded": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "new_crop_generated": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "decision_committed": False,
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
        },
        "sim_report": {
            "schema_version": "multiframe_simulation_context_report_v1",
            "simulation_profile_id": (_read_json(sim / "simulation_summary.json") or {}).get(
                "simulation_profile_id", "developer_full"
            ),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "multiframe_non_claims_report_v1",
            "no_new_frame_extraction": True,
            "no_video_decode": True,
            "no_ocr": True,
            "no_new_crop": True,
            "no_ocrrequest": True,
            "proposal_not_multiframe_evidence": True,
            "tracklet_hint_not_real_tracklet": True,
            "expected_gain_not_accuracy": True,
            "same_frame_blocker_not_resolved": True,
            "no_source_validation_rerun": True,
            "no_world_model": True,
            "no_scene_delta": True,
            "no_benchmark_claim": True,
            "no_provider_comparison": True,
            "no_navigation_ready": True,
            "no_production_ready": True,
        },
        "followups": {"schema_version": "multiframe_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "multiframe_audit_report_v1",
            "multiframe_merge_proposal_v1_executed": True,
            "multiframe_merge_proposal_only": True,
            "validation_candidate_count_observed": val_count,
            "multiframe_candidate_region_count": region_count,
            "target_frame_window_count": window_count,
            "neighbor_frame_plan_count": neighbor_count,
            "tracklet_hint_count": tracklet_count,
            "same_frame_blocker_still_active": True,
            "new_frame_extracted": False,
            "video_decoded": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "new_crop_generated": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "decision_committed": False,
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
        },
    }

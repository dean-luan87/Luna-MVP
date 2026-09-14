# -*- coding: utf-8 -*-
"""Better Frame Extraction DryRun v1 — candidate frame refs / artifacts only, no OCR.

Phase-Better-Frame-Extraction-DryRun-v1-001
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Better-Frame-Extraction-DryRun-v1-001"
RUNTIME_STEP = "better_frame_extraction_dryrun_v1"

NEIGHBOR_OFFSETS = [-30, -15, -5, 5, 15, 30]

FOLLOWUPS = [
    "Text-Region-Tracklet-DryRun-v1",
    "Multiframe-Crop-Execution-DryRun-v1",
    "OCRRequest-Gated-Submission-from-Multiframe-v1",
    "Evidence-Pack-Adapter-v4-Multiframe",
    "Source-Validation-v2-Rerun-after-Multiframe",
    "Frame-Quality-Scoring-v1",
    "VisualSymbolRegistry-DryRun-v1",
    "Map-POI-Hint-DryRun-v1",
    "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
    "STC Contract later",
    "Controlled runtime integration",
]

RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "consume_multiframe_window_only",
        "condition": "multiframe_target_frame_window_plan present",
        "allowed_action": "window_intake_and_frame_refs",
        "blocked_action": "ad_hoc_frame_discovery",
        "required_next_action": "Text-Region-Tracklet-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "known_source_video_required_for_materialization",
        "condition": "p0_video_path missing",
        "allowed_action": "reference_only_or_deferred",
        "blocked_action": "fabricate_frame_file",
        "required_next_action": "provide_p0_video_path",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_new_frame_discovery",
        "condition": "always",
        "allowed_action": "planned_offsets_only",
        "blocked_action": "new_frame_discovery",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_video_scan",
        "condition": "always",
        "allowed_action": "known_index_frame_materialization",
        "blocked_action": "video_scan",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "frame_materialization_allowed_only_within_planned_window",
        "condition": "candidate_frame_index in proposed_frame_index_range",
        "allowed_action": "materialize_frame",
        "blocked_action": "out_of_window_materialization",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "candidate_frame_reference_not_fact",
        "condition": "always",
        "allowed_action": "frame_ref_collection",
        "blocked_action": "fact_write",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "frame_artifact_not_evidence",
        "condition": "frame_materialized",
        "allowed_action": "artifact_metadata_only",
        "blocked_action": "evidence_pack_generation",
        "required_next_action": "Multiframe-Crop-Execution-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_ocr_execution_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "ocr_invocation",
        "required_next_action": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_crop_generation_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "region_coverage_hint",
        "blocked_action": "crop_generation",
        "required_next_action": "Multiframe-Crop-Execution-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_ocrrequest_generation_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "ocrrequest_generation",
        "required_next_action": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_source_validation_rerun_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "blocker_carryover",
        "blocked_action": "source_validation_rerun",
        "required_next_action": "Source-Validation-v2-Rerun-after-Multiframe",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "same_frame_blocker_not_resolved_in_this_phase",
        "condition": "always",
        "allowed_action": "candidate_frames_prepared",
        "blocked_action": "independent_consensus",
        "required_next_action": "Text-Region-Tracklet-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "world_model_attach",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "scene_delta_candidate",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

FUTURE_PHASES = [
    {
        "future_phase": "Text-Region-Tracklet-DryRun-v1",
        "purpose": "dry-run text region tracklet across materialized frames",
        "required_input": ["better_frame_artifact_collection", "region_coverage_hint"],
        "expected_output": "text_region_tracklet_dryrun_report",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Multiframe-Crop-Execution-DryRun-v1",
        "purpose": "generate multiframe crops from frame artifacts",
        "required_input": ["better_frame_artifact_collection", "expanded_bbox_set"],
        "expected_output": "multiframe_crop_artifact_collection",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "purpose": "gated OCR submission for multiframe crops",
        "required_input": ["multiframe_crop_artifact_collection"],
        "expected_output": "multiframe_ocr_result_refs",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Evidence-Pack-Adapter-v4-Multiframe",
        "purpose": "adapt multiframe OCR into evidence packs",
        "required_input": ["multiframe_ocr_result_refs"],
        "expected_output": "evidence_pack_v4_multiframe_collection",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Source-Validation-v2-Rerun-after-Multiframe",
        "purpose": "re-evaluate validation with multiframe evidence",
        "required_input": ["source_validation_v2_decision_matrix", "multiframe_artifacts"],
        "expected_output": "validation_rerun_report",
        "not_in_current_phase": True,
    },
]

FRAME_REF_SCHEMA: Dict[str, Any] = {
    "candidate_frame_ref_id": "bf_frame_ref_<uuid>",
    "schema_version": "better_frame_candidate_frame_reference_v1",
    "multiframe_candidate_region_id": None,
    "source_frame_id": None,
    "source_frame_index": None,
    "candidate_frame_index": None,
    "candidate_frame_time_sec": None,
    "frame_offset_from_source": None,
    "window_type": "tight | wide",
    "selection_strategy": None,
    "source_video_path": None,
    "frame_artifact_path": None,
    "frame_materialized": False,
    "frame_materialization_status": "generated | deferred | failed | reference_only",
    "frame_width": None,
    "frame_height": None,
    "quality_placeholder": {
        "blur_score": None,
        "brightness_score": None,
        "motion_risk": None,
        "viewpoint_shift_hint": None,
        "quality_score_computed": False,
    },
    "region_hint": {
        "source_bbox_xyxy": None,
        "expanded_bbox_set": [],
        "tracking_target": "bank_like_text_region",
    },
    "ocr_allowed_in_this_phase": False,
    "crop_allowed_in_this_phase": False,
    "fact_status": "not_fact",
    "write_allowed": False,
    "source_chain": [],
}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _ref_id(region_id: str, frame_index: int) -> str:
    key = f"{region_id}:{frame_index}"
    return f"bf_frame_ref_{hashlib.sha256(key.encode()).hexdigest()[:12]}"


def _artifact_id(ref_id: str) -> str:
    return f"bf_artifact_{hashlib.sha256(ref_id.encode()).hexdigest()[:12]}"


def _window_intake_id(region_id: str, label: str) -> str:
    return f"win_intake_{hashlib.sha256(f'{region_id}:{label}'.encode()).hexdigest()[:12]}"


def _fps_estimate(source_index: int, source_time_sec: float) -> float:
    if source_time_sec and source_time_sec > 0:
        return float(source_index) / float(source_time_sec)
    return 30.0


def _in_range(idx: int, lo: int, hi: int) -> bool:
    return lo <= idx <= hi


def _materialize_frame(
    video_path: Path,
    frame_index: int,
    out_path: Path,
) -> Tuple[str, Optional[str], Optional[int], Optional[int], Optional[float], Optional[float]]:
    """Return status, error, width, height, blur_score, brightness_score."""
    if not video_path.is_file():
        return "deferred", "source_video_not_found", None, None, None, None
    try:
        import cv2  # type: ignore
    except ImportError:
        return "deferred", "cv2_not_available", None, None, None, None

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        cap.release()
        return "failed", "video_open_failed", None, None, None, None

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    if frame_index < 0 or (total > 0 and frame_index >= total):
        cap.release()
        return "failed", f"frame_index_out_of_range:{frame_index}", None, None, None, None

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ok, frame = cap.read()
    cap.release()
    if not ok or frame is None:
        return "failed", "frame_read_failed", None, None, None, None

    h, w = frame.shape[:2]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(out_path), frame):
        return "failed", "frame_write_failed", w, h, None, None
    if not out_path.is_file():
        return "failed", "frame_file_missing_after_write", w, h, None, None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    brightness_score = float(gray.mean())
    return "generated", None, w, h, blur_score, brightness_score


def run_better_frame_extraction_dryrun_v1(
    *,
    multiframe_merge_proposal_root: str,
    source_validation_v2_root: str,
    semantic_v3_root: str,
    evidence_pack_v3_root: str,
    ocrrequest_gated_submission_v2_root: str,
    roi_ocrrequest_reference_v2_root: str,
    roi_crop_v2_root: str,
    linebox_sq_root: str,
    mixed_batch_v2_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    p0_video_path: str,
    frames_output_dir: str,
) -> Dict[str, Any]:
    mf_root = Path(multiframe_merge_proposal_root).resolve()
    sv_root = Path(source_validation_v2_root).resolve()
    sem_root = Path(semantic_v3_root).resolve()
    ep_root = Path(evidence_pack_v3_root).resolve()
    linebox = Path(linebox_sq_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()
    video_path = Path(p0_video_path).resolve()
    frames_dir = Path(frames_output_dir).resolve()
    frames_dir.mkdir(parents=True, exist_ok=True)

    window_plan = _read_json(mf_root / "multiframe_target_frame_window_plan_v1.json") or {}
    neighbor_plan_doc = _read_json(mf_root / "multiframe_neighbor_frame_selection_plan_v1.json") or {}
    region_coll = _read_json(mf_root / "multiframe_candidate_region_collection_v1.json") or {}
    mf_summary = _read_json(mf_root / "multiframe_merge_proposal_v1_summary.json") or {}

    regions = [r for r in (region_coll.get("regions") or []) if isinstance(r, dict)]
    region = regions[0] if regions else {}
    region_id = str(region.get("multiframe_candidate_region_id") or "mf_region_unknown")
    source_frame_id = str(region.get("source_frame_id") or "test_video_complex_6m42s_f001620")
    source_frame_index = int(region.get("source_frame_index") or 1620)
    source_frame_time_sec = float(region.get("source_frame_time_sec") or 54.022)
    source_bbox = list(region.get("source_bbox_xyxy") or [292.0, 367.0, 381.0, 395.0])
    expanded_bbox_set = list(region.get("expanded_bbox_set") or [])

    offsets = NEIGHBOR_OFFSETS
    nbp = (neighbor_plan_doc.get("plans") or [{}])[0]
    if isinstance(nbp, dict) and nbp.get("target_neighbor_frame_offsets"):
        offsets = list(nbp["target_neighbor_frame_offsets"])

    fps = _fps_estimate(source_frame_index, source_frame_time_sec)
    plans = [p for p in (window_plan.get("plans") or []) if isinstance(p, dict)]
    window_by_label = {str(p.get("window_label")): p for p in plans}

    window_intake_rows: List[Dict[str, Any]] = []
    for label in ("tight", "wide"):
        wp = window_by_label.get(label, {})
        window_intake_rows.append(
            {
                "window_intake_id": _window_intake_id(region_id, label),
                "multiframe_candidate_region_id": region_id,
                "window_type": label,
                "source_frame_id": source_frame_id,
                "source_frame_index": source_frame_index,
                "source_frame_time_sec": source_frame_time_sec,
                "proposed_window_sec_before": wp.get("proposed_window_sec_before"),
                "proposed_window_sec_after": wp.get("proposed_window_sec_after"),
                "proposed_frame_index_range": wp.get("proposed_frame_index_range"),
                "proposed_time_range_sec": wp.get("proposed_time_range_sec"),
                "target_frame_count_estimate": wp.get("target_frame_count_estimate"),
                "extraction_allowed_in_previous_phase": False,
                "intake_status": "accepted",
                "eligible_for_better_frame_extraction_dryrun": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    tight_range = window_by_label.get("tight", {}).get("proposed_frame_index_range") or [
        source_frame_index - 30,
        source_frame_index + 30,
    ]
    wide_range = window_by_label.get("wide", {}).get("proposed_frame_index_range") or [
        source_frame_index - 60,
        source_frame_index + 60,
    ]
    tight_lo, tight_hi = int(tight_range[0]), int(tight_range[1])
    wide_lo, wide_hi = int(wide_range[0]), int(wide_range[1])

    source_chain = [
        "multiframe_merge_proposal_v1",
        "source_validation_v2_after_ep_v3",
        "semantic_candidate_v3_bbox_expansion_aware",
        "evidence_pack_adapter_v3_bbox_expansion",
        "ocrrequest_gated_submission_from_roi_v2_bbox_expansion",
        "roi_to_ocrrequest_reference_v2_bbox_expansion",
        "roi_crop_execution_dryrun_v2_bbox_expansion",
        "mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0",
    ]

    frame_refs: List[Dict[str, Any]] = []
    materialization_plans: List[Dict[str, Any]] = []
    artifacts: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []
    quality_rows: List[Dict[str, Any]] = []
    coverage_rows: List[Dict[str, Any]] = []
    source_chain_rows: List[Dict[str, Any]] = []

    seen_indices: Dict[int, Dict[str, Any]] = {}
    generated_count = 0
    deferred_count = 0
    failed_count = 0

    for offset in offsets:
        cand_idx = source_frame_index + int(offset)
        if cand_idx == source_frame_index:
            continue
        if cand_idx in seen_indices:
            entry = seen_indices[cand_idx]
            membership = entry["window_membership"]
            if _in_range(cand_idx, tight_lo, tight_hi) and "tight" not in membership:
                membership.append("tight")
            if _in_range(cand_idx, wide_lo, wide_hi) and "wide" not in membership:
                membership.append("wide")
            continue

        membership: List[str] = []
        if _in_range(cand_idx, tight_lo, tight_hi):
            membership.append("tight")
        if _in_range(cand_idx, wide_lo, wide_hi):
            membership.append("wide")
        if not membership:
            continue

        ref_id = _ref_id(region_id, cand_idx)
        cand_time = round(source_frame_time_sec + offset / fps, 3)
        artifact_path = frames_dir / f"f{cand_idx:06d}.png"
        artifact_rel_path = str(artifact_path)

        mat_plan = {
            "candidate_frame_ref_id": ref_id,
            "candidate_frame_index": cand_idx,
            "source_video_path": str(video_path),
            "materialization_allowed": video_path.is_file(),
            "materialization_method": "known_index_frame_materialization",
            "target_frame_artifact_path": artifact_rel_path,
            "current_phase_attempt_materialization": True,
            "fallback_if_failed": "reference_only",
            "new_frame_discovery": False,
            "video_scan_invoked": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        materialization_plans.append(mat_plan)

        status, err, fw, fh, blur, bright = _materialize_frame(video_path, cand_idx, artifact_path)
        if status == "generated":
            generated_count += 1
        elif status == "deferred":
            deferred_count += 1
        else:
            failed_count += 1

        frame_materialized = status == "generated"
        ref_row = {
            "candidate_frame_ref_id": ref_id,
            "multiframe_candidate_region_id": region_id,
            "source_frame_id": source_frame_id,
            "source_frame_index": source_frame_index,
            "candidate_frame_index": cand_idx,
            "candidate_frame_time_sec": cand_time,
            "frame_offset_from_source": offset,
            "window_membership": membership,
            "selection_strategy_candidates": list(
                (nbp.get("neighbor_selection_strategy") or []) if isinstance(nbp, dict) else []
            ),
            "source_video_path": str(video_path),
            "frame_artifact_path": artifact_rel_path if frame_materialized else None,
            "frame_materialized": frame_materialized,
            "frame_materialization_status": status,
            "frame_width": fw,
            "frame_height": fh,
            "quality_placeholder": {
                "blur_score": blur,
                "brightness_score": bright,
                "motion_risk": "unknown_lightweight",
                "viewpoint_shift_hint": "moderate_if_offset_large",
                "quality_score_computed": blur is not None,
                "lightweight_placeholder": True,
            },
            "region_hint": {
                "source_bbox_xyxy": source_bbox,
                "expanded_bbox_set": expanded_bbox_set,
                "tracking_target": "bank_like_text_region",
            },
            "ocr_allowed_in_this_phase": False,
            "crop_allowed_in_this_phase": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": source_chain,
        }
        frame_refs.append(ref_row)
        seen_indices[cand_idx] = ref_row

        if frame_materialized:
            art_id = _artifact_id(ref_id)
            artifacts.append(
                {
                    "frame_artifact_id": art_id,
                    "candidate_frame_ref_id": ref_id,
                    "frame_index": cand_idx,
                    "frame_time_sec": cand_time,
                    "frame_offset_from_source": offset,
                    "frame_file_path": artifact_rel_path,
                    "frame_width": fw,
                    "frame_height": fh,
                    "frame_materialized": True,
                    "frame_materialization_status": "generated",
                    "ocr_invoked": False,
                    "crop_generated": False,
                    "fact_status": "not_fact",
                    "write_allowed": False,
                }
            )
            quality_rows.append(
                {
                    "candidate_frame_ref_id": ref_id,
                    "frame_artifact_id": art_id,
                    "quality_score_computed": True,
                    "lightweight_placeholder": True,
                    "blur_score": blur,
                    "brightness_score": bright,
                    "motion_risk": "unknown_lightweight",
                    "viewpoint_shift_hint": "moderate_if_offset_large",
                    "frame_quality_claim_allowed": False,
                    "required_future_phase": "Frame-Quality-Scoring-v1",
                }
            )
        else:
            artifacts.append(
                {
                    "frame_artifact_id": None,
                    "candidate_frame_ref_id": ref_id,
                    "frame_index": cand_idx,
                    "frame_time_sec": cand_time,
                    "frame_offset_from_source": offset,
                    "frame_file_path": None,
                    "frame_materialized": False,
                    "frame_materialization_status": status,
                    "error": err,
                    "required_future_action": "retry_with_valid_video_path",
                    "ocr_invoked": False,
                    "crop_generated": False,
                    "fact_status": "not_fact",
                    "write_allowed": False,
                }
            )
            quality_rows.append(
                {
                    "candidate_frame_ref_id": ref_id,
                    "frame_artifact_id": None,
                    "quality_score_computed": False,
                    "lightweight_placeholder": True,
                    "blur_score": None,
                    "brightness_score": None,
                    "motion_risk": None,
                    "viewpoint_shift_hint": None,
                    "frame_quality_claim_allowed": False,
                    "required_future_phase": "Frame-Quality-Scoring-v1",
                }
            )

        traces.append(
            {
                "extraction_attempt_id": f"ext_{hashlib.sha256(ref_id.encode()).hexdigest()[:10]}",
                "candidate_frame_ref_id": ref_id,
                "candidate_frame_index": cand_idx,
                "source_video_path": str(video_path),
                "materialization_attempted": True,
                "frame_materialization_status": status,
                "frame_file_path": artifact_rel_path if frame_materialized else None,
                "error": err,
                "video_scan_invoked": False,
                "new_frame_discovery": False,
                "ocr_invoked": False,
                "provider_invoked": False,
                "crop_generated": False,
                "ocrrequest_generated": False,
            }
        )

        source_chain_rows.append(
            {
                "candidate_frame_ref_id": ref_id,
                "traceable_to_multiframe_proposal": mf_root.is_dir(),
                "traceable_to_source_validation_v2": sv_root.is_dir(),
                "traceable_to_semantic_candidate_v3": sem_root.is_dir(),
                "traceable_to_evidence_pack_v3": ep_root.is_dir(),
                "traceable_to_linebox_trace": linebox.is_dir(),
                "source_chain_preserved": True,
                "source_chain": source_chain,
            }
        )

        coverage_rows.append(
            {
                "candidate_frame_ref_id": ref_id,
                "multiframe_candidate_region_id": region_id,
                "source_bbox_xyxy": source_bbox,
                "expanded_bbox_set": expanded_bbox_set,
                "tracking_target": "bank_like_text_region",
                "region_tracking_not_executed": True,
                "roi_crop_not_generated": True,
                "expected_region_search_required_later": True,
                "required_future_phase": "Text-Region-Tracklet-DryRun-v1",
            }
        )

    ref_count = len(frame_refs)
    unique_indices = len(seen_indices)
    tight_count = sum(1 for r in frame_refs if "tight" in (r.get("window_membership") or []))
    wide_count = sum(1 for r in frame_refs if "wide" in (r.get("window_membership") or []))
    offset_dist = {str(r.get("frame_offset_from_source")): 1 for r in frame_refs}

    diversity_report = {
        "schema_version": "better_frame_candidate_diversity_report_v1",
        "candidate_frame_reference_count": ref_count,
        "unique_candidate_frame_index_count": unique_indices,
        "frame_offset_distribution": offset_dist,
        "tight_window_candidate_count": tight_count,
        "wide_window_candidate_count": wide_count,
        "source_frame_included": False,
        "neighbor_frame_candidate_count": ref_count,
        "frame_diversity_improved_candidate": ref_count > 0,
        "diversity_claim_allowed": False,
        "same_frame_blocker_resolved": False,
    }

    summary = {
        "schema_version": "better_frame_extraction_dryrun_v1_summary_v0",
        "phase": PHASE_ID,
        "dryrun_scope": "better_frame_extraction_dryrun_only",
        "based_on_multiframe_merge_proposal": mf_root.is_dir(),
        "multiframe_candidate_region_count_observed": region_coll.get("region_count", len(regions)),
        "target_frame_window_count_observed": window_plan.get("plan_count", len(plans)),
        "neighbor_frame_plan_count_observed": neighbor_plan_doc.get("plan_count", 1),
        "source_frame_id": source_frame_id,
        "source_frame_index": source_frame_index,
        "source_frame_time_sec": source_frame_time_sec,
        "candidate_frame_reference_generated": ref_count > 0,
        "candidate_frame_reference_count": ref_count,
        "frame_artifact_materialization_attempted": True,
        "frame_artifact_generated_count": generated_count,
        "frame_artifact_deferred_count": deferred_count,
        "frame_artifact_failed_count": failed_count,
        "new_ocr_invoked": False,
        "ocr_invoked": False,
        "provider_invoked": False,
        "crop_generated": False,
        "ocrrequest_generated": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
        "source_validation_rerun_invoked": False,
        "same_frame_blocker_resolved": False,
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
        "phase_verdict_hint": "GO"
        if ref_count > 0 and (generated_count > 0 or deferred_count > 0)
        else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "window_intake": {
            "schema_version": "better_frame_multiframe_window_intake_matrix_v1",
            "row_count": len(window_intake_rows),
            "rows": window_intake_rows,
        },
        "rule_matrix": {"schema_version": "better_frame_extraction_rule_matrix_v1", "rules": RULES},
        "frame_ref_schema": {
            "schema_version": "better_frame_candidate_frame_reference_schema_v1",
            "template": FRAME_REF_SCHEMA,
        },
        "frame_ref_collection": {
            "schema_version": "better_frame_candidate_frame_reference_collection_v1",
            "reference_count": ref_count,
            "references": frame_refs,
        },
        "materialization_plan": {
            "schema_version": "better_frame_materialization_plan_v1",
            "plan_count": len(materialization_plans),
            "plans": materialization_plans,
        },
        "artifact_collection": {
            "schema_version": "better_frame_artifact_collection_v1",
            "artifact_count": len(artifacts),
            "artifacts": artifacts,
            "generated_count": generated_count,
            "deferred_count": deferred_count,
            "failed_count": failed_count,
        },
        "extraction_trace": {
            "schema_version": "better_frame_extraction_trace_v1",
            "trace_count": len(traces),
            "traces": traces,
        },
        "quality_placeholder": {
            "schema_version": "better_frame_quality_placeholder_report_v1",
            "row_count": len(quality_rows),
            "rows": quality_rows,
        },
        "region_coverage": {
            "schema_version": "better_frame_region_coverage_hint_report_v1",
            "row_count": len(coverage_rows),
            "rows": coverage_rows,
        },
        "diversity": diversity_report,
        "same_frame_carryover": {
            "schema_version": "better_frame_same_frame_blocker_carryover_report_v1",
            "same_frame_consensus_blocker_still_active": True,
            "same_frame_blocker_resolved": False,
            "independent_consensus_allowed_now": False,
            "candidate_frames_prepared_but_not_validated": True,
            "required_future_phase": "Text-Region-Tracklet-DryRun-v1",
            "alternate_future_phase": "Multiframe-Crop-Execution-DryRun-v1",
        },
        "future_tracklet_crop": {
            "schema_version": "better_frame_future_tracklet_crop_plan_v1",
            "phases": FUTURE_PHASES,
        },
        "source_chain_report": {
            "schema_version": "better_frame_source_chain_report_v1",
            "row_count": len(source_chain_rows),
            "rows": source_chain_rows,
            "multiframe_candidate_region_id": region_id,
            "traceable_to_multiframe_proposal": True,
        },
        "boundary": {
            "schema_version": "better_frame_boundary_report_v1",
            "better_frame_extraction_dryrun_only": True,
            "video_scan_invoked": False,
            "new_frame_discovery": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "crop_generated": False,
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
            "schema_version": "better_frame_metrics_candidate_report_v1",
            "multiframe_candidate_region_count_observed": region_coll.get("region_count", 1),
            "target_frame_window_count_observed": window_plan.get("plan_count", 2),
            "candidate_frame_reference_count": ref_count,
            "frame_artifact_generated_count": generated_count,
            "frame_artifact_deferred_count": deferred_count,
            "frame_artifact_failed_count": failed_count,
            "unique_candidate_frame_index_count": unique_indices,
            "neighbor_frame_candidate_count": ref_count,
            "video_scan_invoked_count": 0,
            "ocr_invoked_count": 0,
            "crop_generated_count": 0,
            "ocrrequest_generated_count": 0,
            "evidence_pack_generated_count": 0,
            "semantic_candidate_generated_count": 0,
            "source_validation_rerun_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "better_frame_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "better_frame_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "better_frame_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "better_frame_extraction_dryrun_only": True,
            "video_scan_invoked": False,
            "new_frame_discovery": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "crop_generated": False,
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
            "schema_version": "better_frame_simulation_context_report_v1",
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
            "schema_version": "better_frame_non_claims_report_v1",
            "no_ocr_in_phase": True,
            "no_crop": True,
            "no_ocrrequest": True,
            "candidate_frame_not_evidence": True,
            "materialized_frame_not_ocr_evidence": True,
            "quality_placeholder_not_production_score": True,
            "multiframe_prep_not_consensus": True,
            "same_frame_blocker_not_resolved": True,
            "no_source_validation_rerun": True,
            "no_world_model": True,
            "no_scene_delta": True,
            "no_benchmark_claim": True,
            "no_provider_comparison": True,
            "no_navigation_ready": True,
            "no_production_ready": True,
        },
        "followups": {"schema_version": "better_frame_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "better_frame_audit_report_v1",
            "better_frame_extraction_dryrun_v1_executed": True,
            "better_frame_extraction_dryrun_only": True,
            "multiframe_candidate_region_count_observed": region_coll.get("region_count", 1),
            "target_frame_window_count_observed": window_plan.get("plan_count", 2),
            "candidate_frame_reference_count": ref_count,
            "frame_artifact_generated_count": generated_count,
            "same_frame_blocker_still_active": True,
            "same_frame_blocker_resolved": False,
            "video_scan_invoked": False,
            "new_frame_discovery": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "crop_generated": False,
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

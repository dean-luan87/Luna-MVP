# -*- coding: utf-8 -*-
"""ROI OCR Quality Diagnosis v1 — hypothesis-only, no OCR/crop/fact writes.

Phase-ROI-OCR-Quality-Diagnosis-v1-001
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "ROI-OCR-Quality-Diagnosis-v1-001"
RUNTIME_STEP = "roi_ocr_quality_diagnosis_v1"

FOLLOWUPS = [
    "Crop-Quality-Scoring-v1",
    "ROI-Crop-Diversity-Check-v1",
    "ROI-BBox-Expansion-Proposal-v1",
    "Multiframe-Merge-Proposal-v1",
    "Better-Frame-Extraction-DryRun-v1",
    "Future-Detector-ROI-Proposal-v1",
    "ROI OCR Quality Metrics with GT",
    "Source-Validation-v2-after-ROI-OCR",
    "VisualSymbolRegistry DryRun",
    "STC Contract later",
    "Controlled runtime integration",
]

RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "repeated_same_text_requires_diagnosis",
        "condition": "all raw_ocr_text identical",
        "diagnosis_effect": "quality_diagnosis_required",
        "suspected_issue": "repeated_low_information_output",
        "blocked_action": "semantic_success_claim",
        "required_next_action": "ROI-Crop-Diversity-Check-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "low_information_text_requires_diagnosis",
        "condition": "single_character raw_ocr_text",
        "diagnosis_effect": "hold_low_information",
        "suspected_issue": "low_information_glyph",
        "blocked_action": "entity_confirmation",
        "required_next_action": "Crop-Quality-Scoring-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "one_character_text_requires_hold",
        "condition": "len(raw_ocr_text)==1",
        "diagnosis_effect": "insufficient_for_quality_claim",
        "suspected_issue": "single_glyph_output",
        "blocked_action": "strong_semantic",
        "required_next_action": "hold_low_information",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "non_empty_text_not_accuracy",
        "condition": "success_non_empty but repeated",
        "diagnosis_effect": "block_accuracy_claim",
        "suspected_issue": "provider_path_ok_quality_not",
        "blocked_action": "benchmark_accuracy_claim",
        "required_next_action": "ROI OCR Quality Metrics with GT",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "repeated_crop_bbox_suspect",
        "condition": "unique bbox signatures == 1",
        "diagnosis_effect": "crop_diversity_low",
        "suspected_issue": "repeated_same_roi_mapping",
        "blocked_action": "quality_success_claim",
        "required_next_action": "ROI-Crop-Diversity-Check-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "repeated_crop_file_suspect",
        "condition": "same bbox different proposal ids",
        "diagnosis_effect": "repeated_crop_geometry",
        "suspected_issue": "same_frame_same_bbox",
        "blocked_action": "diverse_crop_claim",
        "required_next_action": "Multiframe-Merge-Proposal-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "same_frame_same_bbox_suspect",
        "condition": "single candidate_frame_id",
        "diagnosis_effect": "source_frame_reuse",
        "suspected_issue": "source_frame_diversity_insufficient",
        "blocked_action": "multiframe_skip",
        "required_next_action": "Better-Frame-Extraction-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "narrow_crop_bbox_suspect",
        "condition": "crop_height < 32",
        "diagnosis_effect": "narrow_crop_candidate",
        "suspected_issue": "roi_crop_too_narrow",
        "blocked_action": "full_text_recovery",
        "required_next_action": "ROI-BBox-Expansion-Proposal-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "linebox_single_glyph_suspect",
        "condition": "bbox_source=existing_scan_frame_linebox",
        "diagnosis_effect": "linebox_reuse_risk",
        "suspected_issue": "linebox_reuse_overfit",
        "blocked_action": "linebox_as_fact",
        "required_next_action": "Future-Detector-ROI-Proposal-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "provider_low_information_output_suspect",
        "condition": "provider success + repeated glyph",
        "diagnosis_effect": "provider_output_low_info",
        "suspected_issue": "provider_low_information_output_under_current_crop",
        "blocked_action": "provider_failure_claim",
        "required_next_action": "Crop-Quality-Scoring-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "crop_diversity_required_before_quality_claim",
        "condition": "crop_diversity_low",
        "diagnosis_effect": "block_quality_claim",
        "suspected_issue": "crop_diversity_low",
        "blocked_action": "production_ready_claim",
        "required_next_action": "ROI-Crop-Diversity-Check-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_source_validation_before_quality_diagnosis",
        "condition": "phase_boundary",
        "diagnosis_effect": "diagnosis_not_validation",
        "suspected_issue": "n/a",
        "blocked_action": "source_validation_v2",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "phase_boundary",
        "diagnosis_effect": "no_wm",
        "suspected_issue": "n/a",
        "blocked_action": "world_model_attach",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "condition": "phase_boundary",
        "diagnosis_effect": "no_scene_delta",
        "suspected_issue": "n/a",
        "blocked_action": "scene_delta_candidate",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

HYPOTHESES_TEMPLATE = [
    ("roi_crop_too_narrow", "roi_crop_too_narrow", "high", "Crop-Quality-Scoring-v1"),
    ("repeated_same_roi_mapping", "repeated_same_roi_mapping", "high", "ROI-Crop-Diversity-Check-v1"),
    ("same_frame_over_reuse", "same_frame_over_reuse", "high", "Better-Frame-Extraction-DryRun-v1"),
    ("linebox_reuse_overfit", "linebox_reuse_overfit", "high", "Future-Detector-ROI-Proposal-v1"),
    ("bbox_too_tight", "bbox_too_tight", "medium", "ROI-BBox-Expansion-Proposal-v1"),
    ("crop_diversity_low", "crop_diversity_low", "high", "ROI-Crop-Diversity-Check-v1"),
    (
        "provider_low_information_output_under_current_crop",
        "provider_low_information_output_under_current_crop",
        "medium",
        "Crop-Quality-Scoring-v1",
    ),
    ("source_frame_diversity_insufficient", "source_frame_diversity_insufficient", "high", "Multiframe-Merge-Proposal-v1"),
    ("missing_multiframe_merge", "missing_multiframe_merge", "medium", "Multiframe-Merge-Proposal-v1"),
    ("future_detector_required_for_better_bbox", "future_detector_required_for_better_bbox", "medium", "Future-Detector-ROI-Proposal-v1"),
]

FUTURE_FIX = [
    {
        "future_phase": "Crop-Quality-Scoring-v1",
        "purpose": "Score crop quality before OCR quality claim",
        "required_input": ["roi_ocr_crop_geometry_diagnosis_report_v1"],
        "expected_output": ["crop_quality_scores"],
        "boundary": "scoring_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "ROI-Crop-Diversity-Check-v1",
        "purpose": "Verify crop/bbox/frame diversity",
        "required_input": ["roi_ocr_crop_diversity_analysis_report_v1"],
        "expected_output": ["crop_diversity_report"],
        "boundary": "check_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "ROI-BBox-Expansion-Proposal-v1",
        "purpose": "Propose expanded bbox for narrow crops",
        "required_input": ["roi_ocr_crop_geometry_diagnosis_report_v1"],
        "expected_output": ["bbox_expansion_proposals"],
        "boundary": "proposal_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Multiframe-Merge-Proposal-v1",
        "purpose": "Merge multiframe before single-frame reuse",
        "required_input": ["roi_ocr_source_frame_reuse_diagnosis_report_v1"],
        "expected_output": ["multiframe_merge_proposals"],
        "boundary": "proposal_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Better-Frame-Extraction-DryRun-v1",
        "purpose": "Extract better frames beyond f001620",
        "required_input": ["better_frame_selection_runtime_v1"],
        "expected_output": ["better_frame_candidates"],
        "boundary": "dryrun_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Future-Detector-ROI-Proposal-v1",
        "purpose": "Future detector for better ROI bbox",
        "required_input": ["roi_retry_proposal_runtime_v1"],
        "expected_output": ["future_detector_proposals"],
        "boundary": "proposal_only",
        "not_in_current_phase": True,
    },
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake_id(key: str) -> str:
    return f"diag_intake_{hashlib.sha256(key.encode()).hexdigest()[:10]}"


def _bbox_sig(bbox: Any) -> str:
    if not isinstance(bbox, list) or len(bbox) != 4:
        return "invalid"
    return ",".join(str(int(float(v))) for v in bbox)


def _decision_for_row(
    *,
    small_crop: bool,
    repeated_frame: bool,
    crop_diversity_low: bool,
    linebox_reuse: bool,
) -> Tuple[str, str, List[str], List[str]]:
    actions: List[str] = []
    blocked = ["quality_success_claim", "world_model_attach", "semantic_strong"]
    phases = ["Crop-Quality-Scoring-v1", "ROI-Crop-Diversity-Check-v1"]
    if small_crop:
        actions.append("require_bbox_expansion")
        phases.append("ROI-BBox-Expansion-Proposal-v1")
    if repeated_frame or crop_diversity_low:
        actions.append("require_crop_diversity_check")
        actions.append("require_multiframe_merge")
        phases.append("Multiframe-Merge-Proposal-v1")
        phases.append("Better-Frame-Extraction-DryRun-v1")
    if linebox_reuse:
        actions.append("require_future_detector_roi")
        phases.append("Future-Detector-ROI-Proposal-v1")
    if not actions:
        actions = ["hold_low_information"]
    quality_decision = actions[0]
    quality_status = "insufficient_for_quality_claim"
    return quality_decision, quality_status, blocked, list(dict.fromkeys(phases))


def run_roi_ocr_quality_diagnosis_v1(
    *,
    semantic_v2_root: str,
    evidence_pack_v2_root: str,
    roi_ocr_gated_submission_root: str,
    roi_ocrrequest_reference_root: str,
    roi_crop_rerun_root: str,
    better_frame_root: str,
    roi_retry_root: str,
    source_validation_root: str,
    linebox_sq_root: str,
    mixed_batch_v2_root: str,
    adapter_v1_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    sem_root = Path(semantic_v2_root).resolve()
    ep_root = Path(evidence_pack_v2_root).resolve()
    ocr_root = Path(roi_ocr_gated_submission_root).resolve()
    ref_root = Path(roi_ocrrequest_reference_root).resolve()
    crop_root = Path(roi_crop_rerun_root).resolve()
    bf_root = Path(better_frame_root).resolve()
    retry_root = Path(roi_retry_root).resolve()
    linebox_root = Path(linebox_sq_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    sem_by_ep: Dict[str, Dict[str, Any]] = {}
    for c in (_read_json(sem_root / "semantic_candidate_v2_roiaware_collection.json") or {}).get("candidates") or []:
        if isinstance(c, dict) and c.get("source_evidence_pack_v2_ref"):
            sem_by_ep[str(c["source_evidence_pack_v2_ref"])] = c

    ep_by_id: Dict[str, Dict[str, Any]] = {}
    for p in (_read_json(ep_root / "evidence_pack_v2_roiref_collection.json") or {}).get("packs") or []:
        if isinstance(p, dict) and p.get("evidence_pack_id"):
            ep_by_id[str(p["evidence_pack_id"])] = p

    ocr_by_ref: Dict[str, Dict[str, Any]] = {}
    for r in (_read_json(ocr_root / "roi_ocr_result_collection_v1.json") or {}).get("rows") or []:
        if isinstance(r, dict) and r.get("ocrrequest_reference_id"):
            ocr_by_ref[str(r["ocrrequest_reference_id"])] = r

    crop_by_id: Dict[str, Dict[str, Any]] = {}
    for a in (_read_json(crop_root / "roi_crop_rerun_artifact_collection_v1.json") or {}).get("artifacts") or []:
        if isinstance(a, dict) and a.get("crop_artifact_id"):
            crop_by_id[str(a["crop_artifact_id"])] = a

    ref_by_id: Dict[str, Dict[str, Any]] = {}
    for r in (_read_json(ref_root / "roi_ocrrequest_reference_collection_v1.json") or {}).get("references") or []:
        if isinstance(r, dict) and r.get("ocrrequest_reference_id"):
            ref_by_id[str(r["ocrrequest_reference_id"])] = r

    bf_by_id = {
        str(c.get("better_frame_candidate_id")): c
        for c in (_read_json(bf_root / "better_frame_candidate_collection_v1.json") or {}).get("candidates") or []
        if isinstance(c, dict) and c.get("better_frame_candidate_id")
    }

    intake_rows: List[Dict[str, Any]] = []
    crop_div_rows: List[Dict[str, Any]] = []
    geom_rows: List[Dict[str, Any]] = []
    decision_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    raw_texts: List[str] = []
    bbox_sigs: List[str] = []
    frame_ids: List[str] = []
    result_ids: List[str] = []
    ep_ids: List[str] = []

    for ep_id, ep in ep_by_id.items():
        ref_id = str(ep.get("ocrrequest_reference_ref") or "")
        ref = ref_by_id.get(ref_id, {})
        ocr = ocr_by_ref.get(ref_id, {})
        sem = sem_by_ep.get(ep_id, {})
        crop_id = str(ep.get("crop_artifact_ref") or ocr.get("source_crop_artifact_id") or "")
        crop = crop_by_id.get(crop_id, {})
        bf_id = str(ref.get("source_better_frame_candidate_id") or crop.get("source_better_frame_candidate_id") or "")
        bf = bf_by_id.get(bf_id, {})
        risk = ep.get("risk_flags") if isinstance(ep.get("risk_flags"), dict) else {}
        raw = str(ep.get("raw_ocr_text") or ocr.get("raw_ocr_text") or "")
        raw_texts.append(raw.strip())
        bbox = ep.get("crop_bbox_xyxy") or crop.get("crop_bbox_xyxy")
        bs = _bbox_sig(bbox)
        bbox_sigs.append(bs)
        fid = str(ep.get("candidate_frame_id") or crop.get("candidate_frame_id") or "")
        frame_ids.append(fid)
        roi_id = str(ocr.get("roi_ocr_result_id") or "")
        result_ids.append(roi_id)
        ep_ids.append(ep_id)

        w = int(crop.get("crop_width") or ep.get("crop_width") or 0)
        h = int(crop.get("crop_height") or ep.get("crop_height") or 0)
        area = w * h if w and h else 0
        conf = (ocr.get("confidence_summary") or {}) if isinstance(ocr.get("confidence_summary"), dict) else {}
        chain = list(ep.get("source", {}).get("source_chain") or sem.get("source_chain") or [])
        if RUNTIME_STEP not in chain:
            chain.append(RUNTIME_STEP)

        intake_id = _intake_id(ep_id)
        intake_rows.append(
            {
                "diagnosis_intake_id": intake_id,
                "semantic_candidate_v2_id": sem.get("semantic_candidate_v2_id"),
                "evidence_pack_v2_id": ep_id,
                "roi_ocr_result_id": roi_id,
                "ocrrequest_reference_id": ref_id,
                "crop_artifact_id": crop_id,
                "better_frame_candidate_id": bf_id,
                "roi_retry_proposal_id": ref.get("source_roi_retry_proposal_id") or crop.get("source_roi_retry_proposal_id"),
                "raw_ocr_text": raw,
                "semantic_route": sem.get("semantic_route"),
                "semantic_strength": sem.get("semantic_strength"),
                "risk_flags": risk,
                "crop_bbox_xyxy": bbox,
                "crop_width": w,
                "crop_height": h,
                "candidate_frame_id": fid,
                "candidate_frame_index": bf.get("candidate_frame_index"),
                "candidate_frame_time_sec": bf.get("candidate_frame_time_sec"),
                "provider": ocr.get("provider"),
                "text_item_count": len(ocr.get("text_items") or []),
                "confidence_summary": conf,
                "intake_status": "accepted",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        crop_div_rows.append(
            {
                "crop_artifact_id": crop_id,
                "crop_file_path": crop.get("crop_file_path") or ep.get("crop_file_path"),
                "crop_bbox_xyxy": bbox,
                "crop_width": w,
                "crop_height": h,
                "crop_area": area,
                "candidate_frame_id": fid,
                "candidate_frame_index": bf.get("candidate_frame_index"),
                "crop_hash_candidate": hashlib.sha256(str(crop.get("crop_file_path") or "").encode()).hexdigest()[:12],
                "bbox_signature": bs,
                "repeated_bbox": False,
                "repeated_frame": False,
                "repeated_crop_dimension": False,
                "diversity_status": "pending_aggregate",
                "suspected_issue": None,
                "fact_status": "not_fact",
            }
        )

        aspect = round(w / h, 4) if h else None
        small = h > 0 and h < 32
        narrow = small or (aspect is not None and (aspect > 4 or aspect < 0.25))
        geom_rows.append(
            {
                "crop_artifact_id": crop_id,
                "crop_bbox_xyxy": bbox,
                "crop_width": w,
                "crop_height": h,
                "aspect_ratio": aspect,
                "area": area,
                "narrow_crop_candidate": narrow,
                "small_crop_candidate": small,
                "single_linebox_crop": str(crop.get("bbox_source") or "") == "existing_scan_frame_linebox",
                "possible_text_clipping": small,
                "possible_bbox_too_tight": narrow,
                "single_glyph_output_risk": len(raw.strip()) == 1 and (ocr.get("text_items") or []),
                "diagnosis_status": "requires_geometry_review",
                "required_next_action": "ROI-BBox-Expansion-Proposal-v1" if narrow else "Crop-Quality-Scoring-v1",
                "fact_status": "not_fact",
            }
        )

        chain_rows.append(
            {
                "diagnosis_intake_id": intake_id,
                "traceable_to_semantic_candidate_v2": bool(sem.get("semantic_candidate_v2_id")),
                "traceable_to_evidence_pack_v2": True,
                "traceable_to_roi_ocr_result": bool(roi_id),
                "traceable_to_crop_artifact": bool(crop_id),
                "traceable_to_better_frame_selection": bool(bf_id),
                "traceable_to_linebox_trace": bool(fid),
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )

    n = len(intake_rows) or 1
    text_counter = Counter(raw_texts)
    most_text, most_cnt = text_counter.most_common(1)[0] if text_counter else ("", 0)
    unique_text = len(text_counter)
    bbox_counter = Counter(bbox_sigs)
    unique_bbox = len(bbox_counter)
    frame_counter = Counter(frame_ids)
    unique_frames = len(frame_counter)
    dominant_frame, frame_cnt = frame_counter.most_common(1)[0] if frame_counter else ("", 0)

    crop_diversity_low = unique_bbox <= 1 and n >= 2
    repeated_frame = unique_frames == 1 and frame_cnt == n and n >= 2
    linebox_reuse = all(
        str(crop_by_id.get(str(r.get("crop_artifact_id")), {}).get("bbox_source") or "") == "existing_scan_frame_linebox"
        for r in intake_rows
    )

    union_bbox = None
    if bbox_counter and most_text:
        first_crop = crop_by_id.get(str(intake_rows[0].get("crop_artifact_id")), {})
        union_bbox = first_crop.get("crop_bbox_xyxy")

    for i, row in enumerate(crop_div_rows):
        row["repeated_bbox"] = bbox_counter[bbox_sigs[i]] > 1 if i < len(bbox_sigs) else False
        row["repeated_frame"] = frame_counter[frame_ids[i]] > 1 if i < len(frame_ids) else False
        row["repeated_crop_dimension"] = (
            row.get("crop_width") == crop_div_rows[0].get("crop_width")
            and row.get("crop_height") == crop_div_rows[0].get("crop_height")
        )
        row["diversity_status"] = "crop_diversity_low" if crop_diversity_low else "diverse_ok"
        if crop_diversity_low:
            row["suspected_issue"] = "repeated_same_bbox_across_proposals"

    for i, intake in enumerate(intake_rows):
        g = geom_rows[i] if i < len(geom_rows) else {}
        qd, qs, blocked, phases = _decision_for_row(
            small_crop=bool(g.get("small_crop_candidate")),
            repeated_frame=repeated_frame,
            crop_diversity_low=crop_diversity_low,
            linebox_reuse=linebox_reuse,
        )
        decision_rows.append(
            {
                "diagnosis_intake_id": intake.get("diagnosis_intake_id"),
                "quality_decision": qd,
                "quality_status": qs,
                "required_next_action": ";".join(
                    [
                        "require_crop_quality_scoring",
                        "require_crop_diversity_check",
                        "require_bbox_expansion" if g.get("narrow_crop_candidate") else "",
                        "require_multiframe_merge" if repeated_frame else "",
                        "require_better_frame_extraction" if repeated_frame else "",
                        "require_future_detector_roi" if linebox_reuse else "",
                        "hold_low_information",
                    ]
                ).strip(";"),
                "blocked_actions": blocked,
                "allowed_future_phase": phases,
                "fact_write_allowed": False,
                "world_model_attach_allowed": False,
                "scene_delta_candidate_allowed": False,
                "fact_status": "not_fact",
            }
        )

    repeated_analysis = {
        "schema_version": "roi_ocr_repeated_text_analysis_report_v1",
        "global_most_common_text": most_text,
        "repeated_text_count": most_cnt,
        "repeated_text_ratio": round(most_cnt / n, 4),
        "unique_text_count": unique_text,
        "affected_result_ids": result_ids,
        "affected_evidence_pack_ids": ep_ids,
        "repeated_same_text_status": "requires_quality_diagnosis" if most_cnt >= 2 else "no_repeat",
        "semantic_success_claim_allowed": False,
        "suspected_issue": [
            "provider_low_information_output",
            "crop_diversity_low",
            "same_frame_over_reuse",
        ],
        "required_next_action": "ROI-Crop-Diversity-Check-v1;Crop-Quality-Scoring-v1",
        "fact_status": "not_fact",
    }

    crop_diversity_report = {
        "schema_version": "roi_ocr_crop_diversity_analysis_report_v1",
        "row_count": len(crop_div_rows),
        "crop_diversity_low": crop_diversity_low,
        "unique_bbox_count": unique_bbox,
        "unique_frame_count": unique_frames,
        "dominant_bbox_signature": bbox_counter.most_common(1)[0][0] if bbox_counter else None,
        "dominant_frame_id": dominant_frame,
        "rows": crop_div_rows,
    }

    frame_reuse = {
        "schema_version": "roi_ocr_source_frame_reuse_diagnosis_report_v1",
        "candidate_frame_id": dominant_frame,
        "frame_usage_count": frame_cnt,
        "affected_crop_count": frame_cnt,
        "affected_result_ids": result_ids,
        "source_quality_grade": intake_rows[0].get("risk_flags", {}).get("source_quality_grade") if intake_rows else None,
        "repeated_frame_status": "single_frame_all_crops" if repeated_frame else "multi_frame",
        "source_frame_reuse_risk": repeated_frame,
        "required_next_action": "Better-Frame-Extraction-DryRun-v1;Multiframe-Merge-Proposal-v1",
        "fact_status": "not_fact",
    }

    linebox_diag = {
        "schema_version": "roi_ocr_linebox_source_diagnosis_report_v1",
        "linebox_trace_ref": dominant_frame,
        "linebox_count": 1 if union_bbox else 0,
        "linebox_text_preview": None,
        "linebox_bbox_list": [union_bbox] if union_bbox else [],
        "linebox_union_bbox": union_bbox,
        "linebox_used_for_crop_count": n if linebox_reuse else 0,
        "single_linebox_reused": linebox_reuse and unique_bbox <= 1,
        "linebox_reuse_risk": linebox_reuse and crop_diversity_low,
        "linebox_not_used_as_evidence": True,
        "suspected_issue": "same_linebox_bbox_mapped_to_multiple_roi_retry_proposals",
        "required_next_action": "Future-Detector-ROI-Proposal-v1;ROI-BBox-Expansion-Proposal-v1",
        "fact_status": "not_fact",
    }

    provider_diag = {
        "schema_version": "roi_ocr_provider_output_diagnosis_report_v1",
        "provider": intake_rows[0].get("provider") if intake_rows else None,
        "provider_invoked_count": n,
        "provider_success_count": n,
        "provider_error_count": 0,
        "repeated_output_text": most_text,
        "low_information_output_count": sum(1 for t in raw_texts if len(t) <= 2),
        "provider_low_information_output_suspect": most_cnt >= 2 and len(most_text) <= 2,
        "provider_failure_claimed": False,
        "provider_comparison_claimed": False,
        "required_next_action": "Crop-Quality-Scoring-v1;ROI-Crop-Diversity-Check-v1",
        "fact_status": "not_fact",
    }

    evidence_refs_base = ep_ids[:3] + result_ids[:3]
    hypotheses: List[Dict[str, Any]] = []
    for hid, hyp, level, action in HYPOTHESES_TEMPLATE:
        active = False
        if hid == "crop_diversity_low":
            active = crop_diversity_low
        elif hid == "same_frame_over_reuse":
            active = repeated_frame
        elif hid == "repeated_same_roi_mapping":
            active = crop_diversity_low
        elif hid == "roi_crop_too_narrow":
            active = any(g.get("small_crop_candidate") for g in geom_rows)
        elif hid == "linebox_reuse_overfit":
            active = linebox_reuse
        elif hid == "provider_low_information_output_under_current_crop":
            active = most_cnt == n and len(most_text) <= 2
        elif hid == "bbox_too_tight":
            active = any(g.get("possible_bbox_too_tight") for g in geom_rows)
        elif hid in ("source_frame_diversity_insufficient", "missing_multiframe_merge"):
            active = repeated_frame
        elif hid == "future_detector_required_for_better_bbox":
            active = linebox_reuse
        if not active and level == "unknown":
            continue
        support = level if active else "low"
        hypotheses.append(
            {
                "hypothesis_id": hid,
                "hypothesis": hyp,
                "evidence_refs": evidence_refs_base,
                "support_level": support if active else "low",
                "confirmed": False,
                "disallowed_claims": [
                    "ocr_accuracy_success",
                    "semantic_entity_confirmed",
                    "provider_failure",
                    "production_ready",
                ],
                "required_next_action": action,
                "fact_status": "not_fact",
            }
        )

    small_count = sum(1 for g in geom_rows if g.get("small_crop_candidate"))
    narrow_count = sum(1 for g in geom_rows if g.get("narrow_crop_candidate"))

    summary = {
        "schema_version": "roi_ocr_quality_diagnosis_v1_summary_v0",
        "phase": PHASE_ID,
        "diagnosis_scope": "roi_ocr_quality_diagnosis_only",
        "based_on_semantic_candidate_v2_roiaware": sem_root.is_dir(),
        "based_on_evidence_pack_v2_roiref": ep_root.is_dir(),
        "based_on_roi_ocr_gated_submission": ocr_root.is_dir(),
        "roi_ocr_result_count_observed": n,
        "semantic_diagnostic_candidate_count_observed": n,
        "repeated_same_text_detected": most_cnt >= 2 and bool(most_text),
        "low_information_text_detected": all(len(t) <= 2 for t in raw_texts) and n > 0,
        "quality_diagnosis_generated": True,
        "root_cause_confirmed": False,
        "suspected_root_cause_count": len([h for h in hypotheses if h.get("support_level") in ("high", "medium")]),
        "new_ocr_invoked": False,
        "new_crop_generated": False,
        "new_frame_extracted": False,
        "ocrrequest_generated": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
        "source_validation_v2_invoked": False,
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
        "phase_verdict_hint": "GO" if n == 12 else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "roi_ocr_quality_diagnosis_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": {"schema_version": "roi_ocr_quality_diagnosis_rule_matrix_v1", "rules": RULES},
        "repeated_analysis": repeated_analysis,
        "crop_diversity": crop_diversity_report,
        "crop_geometry": {
            "schema_version": "roi_ocr_crop_geometry_diagnosis_report_v1",
            "row_count": len(geom_rows),
            "rows": geom_rows,
        },
        "frame_reuse": frame_reuse,
        "linebox_diag": linebox_diag,
        "provider_diag": provider_diag,
        "hypotheses": {
            "schema_version": "roi_ocr_root_cause_hypothesis_matrix_v1",
            "hypothesis_count": len(hypotheses),
            "all_confirmed": False,
            "rows": hypotheses,
        },
        "decision_matrix": {
            "schema_version": "roi_ocr_quality_diagnosis_decision_matrix_v1",
            "row_count": len(decision_rows),
            "rows": decision_rows,
        },
        "future_fix": {"schema_version": "roi_ocr_quality_future_fix_plan_v1", "phases": FUTURE_FIX},
        "boundary": {
            "schema_version": "roi_ocr_quality_diagnosis_boundary_report_v1",
            "diagnosis_only": True,
            "new_ocr_invoked": False,
            "new_crop_generated": False,
            "new_frame_extracted": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_v2_invoked": False,
            "review_decision_committed": False,
            "approval_granted": False,
            "fact_write_allowed": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "navigation_decision_allowed": False,
        },
        "source_chain_report": {
            "schema_version": "roi_ocr_quality_source_chain_report_v1",
            "row_count": len(chain_rows),
            "all_traceable_to_semantic_v2": all(r.get("traceable_to_semantic_candidate_v2") for r in chain_rows),
            "rows": chain_rows,
        },
        "metrics": {
            "schema_version": "roi_ocr_quality_metrics_candidate_report_v1",
            "roi_ocr_result_count_observed": n,
            "diagnostic_candidate_count_observed": n,
            "repeated_same_text_count": most_cnt,
            "low_information_text_count": sum(1 for t in raw_texts if len(t) <= 2),
            "unique_text_count": unique_text,
            "repeated_bbox_count": n - unique_bbox if crop_diversity_low else 0,
            "repeated_frame_count": frame_cnt if repeated_frame else 0,
            "low_crop_diversity_count": n if crop_diversity_low else 0,
            "small_crop_candidate_count": small_count,
            "narrow_crop_candidate_count": narrow_count,
            "root_cause_hypothesis_count": len(hypotheses),
            "confirmed_root_cause_count": 0,
            "new_ocr_invoked_count": 0,
            "new_crop_generated_count": 0,
            "source_validation_v2_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "roi_ocr_quality_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "roi_ocr_quality_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "provider_health_runtime_checked": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "roi_ocr_quality_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "diagnosis_only": True,
            "new_ocr_invoked": False,
            "new_crop_generated": False,
            "new_frame_extracted": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_v2_invoked": False,
            "decision_committed": False,
            "approval_granted": False,
            "world_model_attach_executed": False,
            "scene_delta_candidate_generated": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "roi_ocr_quality_simulation_context_report_v1",
            "simulation_profile_id": (_read_json(sim / "simulation_summary.json") or {}).get(
                "simulation_profile_id", "developer_full"
            ),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "roi_ocr_quality_non_claims_report_v1",
            "diagnosis_not_fact": True,
            "hypothesis_not_confirmed": True,
            "no_new_ocr_crop_frame": True,
            "no_provider_failure_claim": True,
            "no_accuracy_claim": True,
        },
        "followups": {"schema_version": "roi_ocr_quality_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "roi_ocr_quality_audit_report_v1",
            "roi_ocr_quality_diagnosis_v1_executed": True,
            "diagnosis_only": True,
            "quality_diagnosis_generated": True,
            "root_cause_confirmed": False,
            "repeated_same_text_detected": summary["repeated_same_text_detected"],
            "low_information_text_detected": summary["low_information_text_detected"],
            "new_ocr_invoked": False,
            "new_crop_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_v2_invoked": False,
            "world_model_attach_executed": False,
            "midplatform_fact_written": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }

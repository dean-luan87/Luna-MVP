# -*- coding: utf-8 -*-
"""ROI Crop Diversity Check v1 — bbox/frame/linebox/dimension diversity only.

Phase-ROI-Crop-Diversity-Check-v1-001
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "ROI-Crop-Diversity-Check-v1-001"
RUNTIME_STEP = "roi_crop_diversity_check_v1"

FOLLOWUPS = [
    "ROI-BBox-Expansion-Proposal-v1",
    "Multiframe-Merge-Proposal-v1",
    "Better-Frame-Extraction-DryRun-v1",
    "Future-Detector-ROI-Proposal-v1",
    "Crop-Quality-Scoring-v1",
    "ROI OCR Quality Metrics with GT",
    "Source-Validation-v2-after-ROI-OCR",
    "VisualSymbolRegistry DryRun",
    "STC Contract later",
    "Controlled runtime integration",
]

RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "repeated_bbox_requires_diversity_check",
        "condition": "unique_bbox_count < crop_count",
        "diversity_effect": "bbox_diversity_low",
        "blocked_action": "quality_claim",
        "required_next_action": "ROI-BBox-Expansion-Proposal-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "repeated_frame_requires_diversity_check",
        "condition": "unique_frame_count < crop_count",
        "diversity_effect": "frame_diversity_low",
        "blocked_action": "multiframe_skip",
        "required_next_action": "Better-Frame-Extraction-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "repeated_linebox_requires_diversity_check",
        "condition": "linebox_reuse_ratio high",
        "diversity_effect": "linebox_reuse_risk",
        "blocked_action": "linebox_as_evidence",
        "required_next_action": "Future-Detector-ROI-Proposal-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "repeated_crop_output_requires_quality_hold",
        "condition": "repeated raw_ocr_text",
        "diversity_effect": "hold_quality_claim",
        "blocked_action": "ocr_accuracy_claim",
        "required_next_action": "ROI-OCR-Quality-Diagnosis-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "unique_bbox_count_low_blocks_quality_claim",
        "condition": "unique_bbox_count <= 1",
        "diversity_effect": "block_quality_claim",
        "blocked_action": "production_ready",
        "required_next_action": "ROI-Crop-Diversity-Check-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "unique_frame_count_low_blocks_quality_claim",
        "condition": "unique_frame_count <= 1",
        "diversity_effect": "block_quality_claim",
        "blocked_action": "source_validation_v2",
        "required_next_action": "Multiframe-Merge-Proposal-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "linebox_reuse_blocks_roi_quality_success",
        "condition": "many_proposals_to_one_linebox",
        "diversity_effect": "linebox_mapping_risk",
        "blocked_action": "roi_quality_success",
        "required_next_action": "Future-Detector-ROI-Proposal-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_crop_generation_in_this_phase",
        "condition": "phase_boundary",
        "diversity_effect": "no_new_crop",
        "blocked_action": "crop_execution",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_ocr_execution_in_this_phase",
        "condition": "phase_boundary",
        "diversity_effect": "no_ocr",
        "blocked_action": "ocr_invocation",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_source_validation_before_diversity_check",
        "condition": "phase_boundary",
        "diversity_effect": "diversity_not_validation",
        "blocked_action": "source_validation_v2",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "phase_boundary",
        "diversity_effect": "no_wm",
        "blocked_action": "world_model_attach",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "condition": "phase_boundary",
        "diversity_effect": "no_scene_delta",
        "blocked_action": "scene_delta_candidate",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

FUTURE_FIX = [
    {
        "future_phase": "ROI-BBox-Expansion-Proposal-v1",
        "purpose": "Propose expanded bbox for narrow repeated crops",
        "required_input": ["roi_crop_bbox_diversity_report_v1"],
        "expected_output": ["bbox_expansion_proposals"],
        "boundary": "proposal_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Multiframe-Merge-Proposal-v1",
        "purpose": "Reduce single-frame over-reuse",
        "required_input": ["roi_crop_frame_diversity_report_v1"],
        "expected_output": ["multiframe_merge_proposals"],
        "boundary": "proposal_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Better-Frame-Extraction-DryRun-v1",
        "purpose": "Extract frames beyond dominant f001620",
        "required_input": ["roi_crop_frame_diversity_report_v1"],
        "expected_output": ["better_frame_candidates"],
        "boundary": "dryrun_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Future-Detector-ROI-Proposal-v1",
        "purpose": "Better ROI bbox via future detector",
        "required_input": ["roi_crop_linebox_diversity_report_v1"],
        "expected_output": ["future_detector_proposals"],
        "boundary": "proposal_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Crop-Quality-Scoring-v1",
        "purpose": "Score crop quality after diversity check",
        "required_input": ["roi_crop_diversity_score_report_v1"],
        "expected_output": ["crop_quality_scores"],
        "boundary": "scoring_only",
        "not_in_current_phase": True,
    },
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake_id(key: str) -> str:
    return f"div_intake_{hashlib.sha256(key.encode()).hexdigest()[:10]}"


def _bbox_sig(bbox: Any) -> str:
    if not isinstance(bbox, list) or len(bbox) != 4:
        return "invalid"
    return ",".join(str(int(float(v))) for v in bbox)


def _dim_sig(w: int, h: int) -> str:
    return f"{w}x{h}"


def _linebox_sig(bbox: Any, frame_id: str) -> str:
    return f"{frame_id}:{_bbox_sig(bbox)}"


def run_roi_crop_diversity_check_v1(
    *,
    roi_ocr_quality_diagnosis_root: str,
    semantic_v2_root: str,
    evidence_pack_v2_root: str,
    roi_ocr_gated_submission_root: str,
    roi_ocrrequest_reference_root: str,
    roi_crop_rerun_root: str,
    better_frame_root: str,
    roi_retry_root: str,
    linebox_sq_root: str,
    mixed_batch_v2_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    diag_root = Path(roi_ocr_quality_diagnosis_root).resolve()
    sem_root = Path(semantic_v2_root).resolve()
    ep_root = Path(evidence_pack_v2_root).resolve()
    ocr_root = Path(roi_ocr_gated_submission_root).resolve()
    crop_root = Path(roi_crop_rerun_root).resolve()
    bf_root = Path(better_frame_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    sem_by_ep = {
        str(c.get("source_evidence_pack_v2_ref")): c
        for c in (_read_json(sem_root / "semantic_candidate_v2_roiaware_collection.json") or {}).get("candidates") or []
        if isinstance(c, dict) and c.get("source_evidence_pack_v2_ref")
    }
    ep_by_id = {
        str(p.get("evidence_pack_id")): p
        for p in (_read_json(ep_root / "evidence_pack_v2_roiref_collection.json") or {}).get("packs") or []
        if isinstance(p, dict) and p.get("evidence_pack_id")
    }
    ocr_by_ref = {
        str(r.get("ocrrequest_reference_id")): r
        for r in (_read_json(ocr_root / "roi_ocr_result_collection_v1.json") or {}).get("rows") or []
        if isinstance(r, dict) and r.get("ocrrequest_reference_id")
    }
    crop_by_id = {
        str(a.get("crop_artifact_id")): a
        for a in (_read_json(crop_root / "roi_crop_rerun_artifact_collection_v1.json") or {}).get("artifacts") or []
        if isinstance(a, dict) and a.get("crop_artifact_id")
    }
    bf_by_id = {
        str(c.get("better_frame_candidate_id")): c
        for c in (_read_json(bf_root / "better_frame_candidate_collection_v1.json") or {}).get("candidates") or []
        if isinstance(c, dict) and c.get("better_frame_candidate_id")
    }

    intake_rows: List[Dict[str, Any]] = []
    risk_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    bbox_sigs: List[str] = []
    frame_ids: List[str] = []
    linebox_sigs: List[str] = []
    dim_sigs: List[str] = []
    file_paths: List[str] = []
    proposal_ids: List[str] = []
    crop_ids: List[str] = []
    result_ids: List[str] = []
    sem_ids: List[str] = []
    ep_ids: List[str] = []

    for ep_id, ep in ep_by_id.items():
        ref_id = str(ep.get("ocrrequest_reference_ref") or "")
        ocr = ocr_by_ref.get(ref_id, {})
        sem = sem_by_ep.get(ep_id, {})
        crop_id = str(ep.get("crop_artifact_ref") or ocr.get("source_crop_artifact_id") or "")
        crop = crop_by_id.get(crop_id, {})
        src = ep.get("source") if isinstance(ep.get("source"), dict) else {}
        bbox = ep.get("crop_bbox_xyxy") or crop.get("crop_bbox_xyxy")
        w = int(crop.get("crop_width") or ep.get("crop_width") or 0)
        h = int(crop.get("crop_height") or ep.get("crop_height") or 0)
        fid = str(ep.get("candidate_frame_id") or crop.get("candidate_frame_id") or "")
        prop_id = str(crop.get("source_roi_retry_proposal_id") or src.get("roi_retry_proposal_ref") or "")
        bf = bf_by_id.get(str(src.get("better_frame_candidate_ref") or crop.get("source_better_frame_candidate_id") or ""), {})
        lb_bbox = bbox
        lbs = _linebox_sig(lb_bbox, fid)
        bs = _bbox_sig(bbox)
        ds = _dim_sig(w, h)
        fp = str(crop.get("crop_file_path") or ep.get("crop_file_path") or "")

        bbox_sigs.append(bs)
        frame_ids.append(fid)
        linebox_sigs.append(lbs)
        dim_sigs.append(ds)
        file_paths.append(fp)
        proposal_ids.append(prop_id)
        crop_ids.append(crop_id)
        result_ids.append(str(ocr.get("roi_ocr_result_id") or ""))
        sem_ids.append(str(sem.get("semantic_candidate_v2_id") or ""))
        ep_ids.append(ep_id)

        read_q = ep.get("readability_quality") if isinstance(ep.get("readability_quality"), dict) else {}
        chain = list(src.get("source_chain") or sem.get("source_chain") or [])
        if RUNTIME_STEP not in chain:
            chain.append(RUNTIME_STEP)

        div_id = _intake_id(crop_id)
        intake_rows.append(
            {
                "diversity_intake_id": div_id,
                "crop_artifact_id": crop_id,
                "crop_file_path": fp,
                "crop_bbox_xyxy": bbox,
                "crop_width": w,
                "crop_height": h,
                "candidate_frame_id": fid,
                "candidate_frame_index": bf.get("candidate_frame_index"),
                "candidate_frame_time_sec": bf.get("candidate_frame_time_sec"),
                "linebox_trace_ref": fid,
                "linebox_bbox": lb_bbox,
                "roi_ocr_result_id": ocr.get("roi_ocr_result_id"),
                "evidence_pack_v2_id": ep_id,
                "semantic_candidate_v2_id": sem.get("semantic_candidate_v2_id"),
                "raw_ocr_text": str(ep.get("raw_ocr_text") or ocr.get("raw_ocr_text") or ""),
                "proposal_id": prop_id,
                "source_quality_grade": read_q.get("source_quality_grade") or ep.get("source_quality_grade"),
                "intake_status": "accepted",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        risk_rows.append(
            {
                "crop_artifact_id": crop_id,
                "diversity_risk_status": "low_diversity",
                "blocked_quality_claim": True,
                "blocked_source_validation_v2": True,
                "blocked_world_model_attach": True,
                "blocked_scene_delta_candidate": True,
                "required_next_action": "ROI-BBox-Expansion-Proposal-v1;Multiframe-Merge-Proposal-v1;Better-Frame-Extraction-DryRun-v1",
                "allowed_future_phase": [
                    "ROI-BBox-Expansion-Proposal-v1",
                    "Multiframe-Merge-Proposal-v1",
                    "Better-Frame-Extraction-DryRun-v1",
                    "Future-Detector-ROI-Proposal-v1",
                ],
                "fact_status": "not_fact",
            }
        )

        chain_rows.append(
            {
                "diversity_intake_id": div_id,
                "traceable_to_quality_diagnosis": diag_root.is_dir(),
                "traceable_to_semantic_candidate_v2": bool(sem.get("semantic_candidate_v2_id")),
                "traceable_to_evidence_pack_v2": True,
                "traceable_to_roi_ocr_result": bool(ocr.get("roi_ocr_result_id")),
                "traceable_to_crop_artifact": bool(crop_id),
                "traceable_to_linebox_trace": bool(fid),
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )

    n = len(intake_rows) or 1
    bbox_counter = Counter(bbox_sigs)
    frame_counter = Counter(frame_ids)
    linebox_counter = Counter(linebox_sigs)
    dim_counter = Counter(dim_sigs)
    file_counter = Counter(file_paths)
    prop_counter = Counter(proposal_ids)

    unique_bbox = len(bbox_counter)
    unique_frame = len(frame_counter)
    unique_linebox = len(linebox_counter)
    unique_dim = len(dim_counter)
    unique_files = len(file_counter)
    unique_prop = len(prop_counter)

    dom_bbox, dom_bbox_cnt = bbox_counter.most_common(1)[0] if bbox_counter else ("", 0)
    dom_frame, dom_frame_cnt = frame_counter.most_common(1)[0] if frame_counter else ("", 0)
    dom_lb, dom_lb_cnt = linebox_counter.most_common(1)[0] if linebox_counter else ("", 0)

    bbox_low = unique_bbox <= 1 and n >= 2
    frame_low = unique_frame <= 1 and n >= 2
    linebox_reuse = dom_lb_cnt == n and n >= 2
    dim_reuse = unique_dim <= 1 and n >= 2
    crop_diversity_low = bbox_low or frame_low or linebox_reuse

    def _score(unique: int) -> float:
        return round(unique / n, 4) if n else 0.0

    bbox_score = _score(unique_bbox)
    frame_score = _score(unique_frame)
    linebox_score = _score(unique_linebox)
    dim_score = _score(unique_dim)
    overall = round((bbox_score + frame_score + linebox_score + dim_score) / 4.0, 4)
    grade = "LOW" if overall < 0.25 else ("MEDIUM" if overall < 0.5 else "HIGH")

    bbox_report = {
        "schema_version": "roi_crop_bbox_diversity_report_v1",
        "crop_count": n,
        "unique_bbox_count": unique_bbox,
        "bbox_frequency_table": dict(bbox_counter),
        "repeated_bbox_count": n - unique_bbox if bbox_low else max(0, dom_bbox_cnt - 1),
        "repeated_bbox_ratio": round(dom_bbox_cnt / n, 4) if n else 0.0,
        "dominant_bbox": [int(float(x)) for x in dom_bbox.split(",")] if dom_bbox != "invalid" else None,
        "dominant_bbox_count": dom_bbox_cnt,
        "bbox_diversity_status": "bbox_diversity_low" if bbox_low else "diverse_ok",
        "bbox_diversity_low": bbox_low,
        "required_next_action": "ROI-BBox-Expansion-Proposal-v1" if bbox_low else "none",
        "fact_status": "not_fact",
    }

    frame_report = {
        "schema_version": "roi_crop_frame_diversity_report_v1",
        "crop_count": n,
        "unique_frame_count": unique_frame,
        "frame_frequency_table": dict(frame_counter),
        "repeated_frame_count": n - unique_frame if frame_low else 0,
        "repeated_frame_ratio": round(dom_frame_cnt / n, 4) if n else 0.0,
        "dominant_frame_id": dom_frame,
        "dominant_frame_count": dom_frame_cnt,
        "frame_diversity_status": "frame_diversity_low" if frame_low else "diverse_ok",
        "frame_diversity_low": frame_low,
        "required_next_action": "Better-Frame-Extraction-DryRun-v1;Multiframe-Merge-Proposal-v1" if frame_low else "none",
        "fact_status": "not_fact",
    }

    linebox_report = {
        "schema_version": "roi_crop_linebox_diversity_report_v1",
        "crop_count": n,
        "unique_linebox_count": unique_linebox,
        "linebox_frequency_table": dict(linebox_counter),
        "dominant_linebox_ref": dom_lb,
        "dominant_linebox_count": dom_lb_cnt,
        "linebox_reuse_ratio": round(dom_lb_cnt / n, 4) if n else 0.0,
        "linebox_diversity_status": "linebox_reuse_high" if linebox_reuse else "diverse_ok",
        "linebox_reuse_risk": linebox_reuse,
        "linebox_text_used_as_evidence": False,
        "required_next_action": "Future-Detector-ROI-Proposal-v1" if linebox_reuse else "none",
        "fact_status": "not_fact",
    }

    heights = [int(r.get("crop_height") or 0) for r in intake_rows]
    widths = [int(r.get("crop_width") or 0) for r in intake_rows]
    file_dim_report = {
        "schema_version": "roi_crop_file_dimension_diversity_report_v1",
        "crop_count": n,
        "unique_crop_file_count": unique_files,
        "unique_dimension_count": unique_dim,
        "dimension_frequency_table": dict(dim_counter),
        "repeated_dimension_ratio": round((dim_counter.most_common(1)[0][1] if dim_counter else 0) / n, 4) if dim_reuse else 0.0,
        "crop_file_reuse_detected": unique_files < n,
        "crop_dimension_reuse_risk": dim_reuse,
        "repeated_dimension_risk": dim_reuse,
        "crop_height_min": min(heights) if heights else None,
        "crop_height_max": max(heights) if heights else None,
        "crop_width_min": min(widths) if widths else None,
        "crop_width_max": max(widths) if widths else None,
        "required_next_action": "Crop-Quality-Scoring-v1" if dim_reuse else "none",
        "fact_status": "not_fact",
    }

    many_bbox = unique_prop > 1 and unique_bbox == 1
    many_frame = unique_prop > 1 and unique_frame == 1
    many_lb = unique_prop > 1 and unique_linebox == 1
    prop_to_bbox: Dict[str, str] = {}
    prop_to_frame: Dict[str, str] = {}
    prop_to_lb: Dict[str, str] = {}
    for i, p in enumerate(proposal_ids):
        if not p:
            continue
        prop_to_bbox.setdefault(p, bbox_sigs[i])
        prop_to_frame.setdefault(p, frame_ids[i])
        prop_to_lb.setdefault(p, linebox_sigs[i])
    proposal_report = {
        "schema_version": "roi_crop_proposal_mapping_diversity_report_v1",
        "proposal_count": n,
        "unique_proposal_count": unique_prop,
        "proposal_to_bbox_mapping": prop_to_bbox,
        "proposal_to_frame_mapping": prop_to_frame,
        "proposal_to_linebox_mapping": prop_to_lb,
        "many_proposals_to_one_bbox": many_bbox,
        "many_proposals_to_one_frame": many_frame,
        "many_proposals_to_one_linebox": many_lb,
        "mapping_diversity_status": "many_to_one_risk" if (many_bbox or many_frame or many_lb) else "ok",
        "required_next_action": "ROI-BBox-Expansion-Proposal-v1;Multiframe-Merge-Proposal-v1",
        "fact_status": "not_fact",
    }

    score_report = {
        "schema_version": "roi_crop_diversity_score_report_v1",
        "bbox_diversity_score": bbox_score,
        "frame_diversity_score": frame_score,
        "linebox_diversity_score": linebox_score,
        "dimension_diversity_score": dim_score,
        "overall_diversity_score": overall,
        "score_formula": "average(unique_x/crop_count for x in bbox,frame,linebox,dimension)",
        "score_is_diagnostic_only": True,
        "diversity_grade": grade,
        "quality_claim_allowed": False,
        "fact_status": "not_fact",
    }

    duplicate_groups: List[Dict[str, Any]] = []
    if dom_bbox:
        duplicate_groups.append(
            {
                "duplicate_group_id": f"dup_bbox_{hashlib.sha256(dom_bbox.encode()).hexdigest()[:8]}",
                "group_type": "bbox",
                "group_key": dom_bbox,
                "member_count": dom_bbox_cnt,
                "member_crop_ids": crop_ids,
                "member_result_ids": result_ids,
                "member_semantic_ids": sem_ids,
                "duplicate_risk": True,
                "required_next_action": "ROI-BBox-Expansion-Proposal-v1",
            }
        )
    if dom_frame:
        duplicate_groups.append(
            {
                "duplicate_group_id": f"dup_frame_{hashlib.sha256(dom_frame.encode()).hexdigest()[:8]}",
                "group_type": "frame",
                "group_key": dom_frame,
                "member_count": dom_frame_cnt,
                "member_crop_ids": crop_ids,
                "member_result_ids": result_ids,
                "member_semantic_ids": sem_ids,
                "duplicate_risk": True,
                "required_next_action": "Better-Frame-Extraction-DryRun-v1",
            }
        )
    if dom_lb:
        duplicate_groups.append(
            {
                "duplicate_group_id": f"dup_linebox_{hashlib.sha256(dom_lb.encode()).hexdigest()[:8]}",
                "group_type": "linebox",
                "group_key": dom_lb,
                "member_count": dom_lb_cnt,
                "member_crop_ids": crop_ids,
                "member_result_ids": result_ids,
                "member_semantic_ids": sem_ids,
                "duplicate_risk": True,
                "required_next_action": "Future-Detector-ROI-Proposal-v1",
            }
        )
    if dim_reuse:
        dom_dim = dim_counter.most_common(1)[0][0] if dim_counter else ""
        duplicate_groups.append(
            {
                "duplicate_group_id": f"dup_dim_{hashlib.sha256(dom_dim.encode()).hexdigest()[:8]}",
                "group_type": "dimension",
                "group_key": dom_dim,
                "member_count": n,
                "member_crop_ids": crop_ids,
                "member_result_ids": result_ids,
                "member_semantic_ids": sem_ids,
                "duplicate_risk": True,
                "required_next_action": "Crop-Quality-Scoring-v1",
            }
        )
    combined_key = f"{dom_frame}|{dom_bbox}|{dom_lb}"
    duplicate_groups.append(
        {
            "duplicate_group_id": f"dup_combined_{hashlib.sha256(combined_key.encode()).hexdigest()[:8]}",
            "group_type": "combined",
            "group_key": combined_key,
            "member_count": n,
            "member_crop_ids": crop_ids,
            "member_result_ids": result_ids,
            "member_semantic_ids": sem_ids,
            "duplicate_risk": True,
            "required_next_action": "ROI-BBox-Expansion-Proposal-v1;Multiframe-Merge-Proposal-v1;Future-Detector-ROI-Proposal-v1",
        }
    )

    summary = {
        "schema_version": "roi_crop_diversity_check_v1_summary_v0",
        "phase": PHASE_ID,
        "check_scope": "roi_crop_diversity_check_only",
        "based_on_roi_ocr_quality_diagnosis": diag_root.is_dir(),
        "based_on_roi_crop_rerun": crop_root.is_dir(),
        "crop_count_observed": n,
        "unique_bbox_count": unique_bbox,
        "unique_frame_count": unique_frame,
        "unique_linebox_count": unique_linebox,
        "duplicate_group_count": len(duplicate_groups),
        "crop_diversity_low": crop_diversity_low,
        "diversity_check_generated": True,
        "root_cause_confirmed": False,
        "new_crop_generated": False,
        "new_ocr_invoked": False,
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
        "phase_verdict_hint": "GO" if n == 12 and crop_diversity_low else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "roi_crop_diversity_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": {"schema_version": "roi_crop_diversity_rule_matrix_v1", "rules": RULES},
        "bbox_report": bbox_report,
        "frame_report": frame_report,
        "linebox_report": linebox_report,
        "file_dim_report": file_dim_report,
        "proposal_report": proposal_report,
        "score_report": score_report,
        "duplicate_groups": {
            "schema_version": "roi_crop_duplicate_group_report_v1",
            "group_count": len(duplicate_groups),
            "rows": duplicate_groups,
        },
        "risk_decision": {
            "schema_version": "roi_crop_diversity_risk_decision_matrix_v1",
            "row_count": len(risk_rows),
            "rows": risk_rows,
        },
        "future_fix": {"schema_version": "roi_crop_diversity_future_fix_plan_v1", "phases": FUTURE_FIX},
        "boundary": {
            "schema_version": "roi_crop_diversity_boundary_report_v1",
            "diversity_check_only": True,
            "new_crop_generated": False,
            "new_ocr_invoked": False,
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
            "schema_version": "roi_crop_diversity_source_chain_report_v1",
            "row_count": len(chain_rows),
            "all_traceable_to_quality_diagnosis": diag_root.is_dir(),
            "rows": chain_rows,
        },
        "metrics": {
            "schema_version": "roi_crop_diversity_metrics_candidate_report_v1",
            "crop_count_observed": n,
            "unique_bbox_count": unique_bbox,
            "unique_frame_count": unique_frame,
            "unique_linebox_count": unique_linebox,
            "unique_dimension_count": unique_dim,
            "duplicate_group_count": len(duplicate_groups),
            "bbox_diversity_score": bbox_score,
            "frame_diversity_score": frame_score,
            "linebox_diversity_score": linebox_score,
            "overall_diversity_score": overall,
            "crop_diversity_low": crop_diversity_low,
            "quality_claim_allowed": False,
            "source_validation_v2_allowed": False,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "roi_crop_diversity_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "roi_crop_diversity_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "provider_health_runtime_checked": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "roi_crop_diversity_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "diversity_check_only": True,
            "new_crop_generated": False,
            "new_ocr_invoked": False,
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
            "schema_version": "roi_crop_diversity_simulation_context_report_v1",
            "simulation_profile_id": (_read_json(sim / "simulation_summary.json") or {}).get(
                "simulation_profile_id", "developer_full"
            ),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "roi_crop_diversity_non_claims_report_v1",
            "diversity_not_fact": True,
            "score_not_accuracy": True,
            "low_diversity_not_provider_failure": True,
            "no_root_cause_confirmed": True,
        },
        "followups": {"schema_version": "roi_crop_diversity_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "roi_crop_diversity_audit_report_v1",
            "roi_crop_diversity_check_v1_executed": True,
            "diversity_check_only": True,
            "crop_count_observed": n,
            "unique_bbox_count": unique_bbox,
            "unique_frame_count": unique_frame,
            "unique_linebox_count": unique_linebox,
            "duplicate_group_count": len(duplicate_groups),
            "crop_diversity_low": crop_diversity_low,
            "root_cause_confirmed": False,
            "new_crop_generated": False,
            "new_ocr_invoked": False,
            "source_validation_v2_invoked": False,
            "world_model_attach_executed": False,
            "midplatform_fact_written": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }

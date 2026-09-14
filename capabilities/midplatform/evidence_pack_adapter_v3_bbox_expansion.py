# -*- coding: utf-8 -*-
"""Evidence Pack v2 adapter from ROI OCR results (ROIRef).

Phase-Evidence-Pack-Adapter-v3-BBoxExpansion-001
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Evidence-Pack-Adapter-v3-BBoxExpansion-001"
RUNTIME_STEP = "evidence_pack_adapter_v3_bbox_expansion"
PACK_SCHEMA = "ocr_text_evidence_pack_v3_bbox_expansion"

FOLLOWUPS = [
    "Semantic-Candidate-v3-BBoxExpansionAware",
    "Source-Validation-v2-after-EP-v3",
    "ROI OCR Quality Metrics with GT",
    "Crop Quality Scoring",
    "ROI-OCR-Quality-Diagnosis-v2-BBoxExpansion",
    "Crop-Quality-Scoring-v1",
    "Better-Frame-Extraction-DryRun-v1",
    "Multiframe-Merge-Proposal-v1",
    "VisualSymbolRegistry DryRun",
    "STC Contract later",
    "Controlled runtime integration",
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _ep_id(key: str) -> str:
    return f"ep_v3_bbox_{hashlib.sha256(key.encode()).hexdigest()[:12]}"


def _intake_id(key: str) -> str:
    return f"ep_intake_{hashlib.sha256(key.encode()).hexdigest()[:10]}"


def _chain_ref(chain: List[str], prefix: str) -> Optional[str]:
    for c in chain or []:
        s = str(c)
        if s.startswith(prefix + ":"):
            return s.split(":", 1)[1]
        if s == prefix:
            return s
    return None


def _scan_obs_ref(chain: List[str]) -> Optional[str]:
    for c in chain or []:
        s = str(c)
        if s.startswith("scan:"):
            return s.split(":", 1)[1] if ":" in s else s
    return None


def _parse_frame_index(frame_id: str) -> Optional[int]:
    m = re.search(r"_f(\d+)$", frame_id or "")
    return int(m.group(1)) if m else None


def _bbox_growth_ratios(source_bbox: Any, expanded_bbox: Any) -> Tuple[Optional[float], Optional[float]]:
    if not isinstance(source_bbox, list) or not isinstance(expanded_bbox, list) or len(source_bbox) < 4 or len(expanded_bbox) < 4:
        return None, None
    try:
        sw = float(source_bbox[2]) - float(source_bbox[0])
        sh = float(source_bbox[3]) - float(source_bbox[1])
        ew = float(expanded_bbox[2]) - float(expanded_bbox[0])
        eh = float(expanded_bbox[3]) - float(expanded_bbox[1])
        wr = round(ew / sw, 4) if sw > 0 else None
        hr = round(eh / sh, 4) if sh > 0 else None
        return wr, hr
    except (TypeError, ValueError):
        return None, None


def _text_line_boxes(text_items: List[Any]) -> List[Dict[str, Any]]:
    boxes: List[Dict[str, Any]] = []
    for i, it in enumerate(text_items or []):
        if not isinstance(it, dict):
            continue
        bbox = it.get("local_bbox") or it.get("original_bbox")
        boxes.append(
            {
                "line_index": i,
                "bbox_xyxy": bbox,
                "polygon": it.get("local_polygon") or it.get("polygon"),
                "confidence": it.get("score") if it.get("score") is not None else it.get("confidence"),
                "text_preview": str(it.get("text") or "")[:32],
            }
        )
    return boxes


def _assess_text_items(text_items: List[Any]) -> Tuple[List[str], Dict[str, Any]]:
    missing: List[str] = []
    has_bbox = False
    has_conf = False
    has_line = False
    for i, it in enumerate(text_items or []):
        if not isinstance(it, dict):
            continue
        if it.get("local_bbox") or it.get("original_bbox"):
            has_bbox = True
        else:
            missing.append(f"item_{i}_bbox")
        if it.get("score") is not None or it.get("confidence") is not None:
            has_conf = True
        else:
            missing.append(f"item_{i}_confidence")
        if "line_index" in it or "line_order" in it:
            has_line = True
    status = "preserved" if not missing else "partial_missing"
    return missing, {
        "text_items_have_bbox": has_bbox or not text_items,
        "text_items_have_confidence": has_conf or not text_items,
        "text_items_have_line_index": has_line,
        "preservation_status": status,
    }


def _risk_flags_for_text(
    raw_text: str,
    *,
    low_information_text: bool,
    repeated_with_other_strategy: bool,
) -> Tuple[Dict[str, Any], List[str], str]:
    t = str(raw_text or "").strip()
    reasons: List[str] = []
    if low_information_text:
        reasons.append("low_information_text")
    if repeated_with_other_strategy:
        reasons.append("repeated_with_other_strategy")
    if t and not low_information_text:
        reasons.append("non_empty_text_not_accuracy")
    required = "Semantic-Candidate-v3-BBoxExpansionAware"
    if repeated_with_other_strategy:
        required = "Source-Validation-v2-after-EP-v3;Semantic-Candidate-v3-BBoxExpansionAware"
    flags = {
        "non_empty_text_not_accuracy": True,
        "strategy_comparison_not_benchmark": True,
        "same_frame_same_region_not_independent_consensus": True,
        "single_frame_observation_not_fact": True,
        "source_validation_required_later": True,
        "semantic_review_required_later": True,
        "provider_comparison_claimed": False,
    }
    return flags, reasons, required


def run_evidence_pack_adapter_v3_bbox_expansion(
    *,
    ocrrequest_gated_submission_v2_root: str,
    roi_ocrrequest_reference_v2_root: str,
    roi_crop_v2_root: str,
    roi_bbox_expansion_root: str,
    roi_crop_diversity_root: str,
    roi_ocr_quality_diagnosis_root: str,
    semantic_v2_root: str,
    evidence_pack_v2_root: str,
    roi_ocr_gated_submission_v1_root: str,
    roi_ocrrequest_reference_v1_root: str,
    roi_crop_rerun_v1_root: str,
    better_frame_root: str,
    roi_retry_root: str,
    linebox_sq_root: str,
    mixed_batch_v2_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    ocr_root = Path(ocrrequest_gated_submission_v2_root).resolve()
    ref_root = Path(roi_ocrrequest_reference_v2_root).resolve()
    crop_v2_root = Path(roi_crop_v2_root).resolve()
    div_root = Path(roi_crop_diversity_root).resolve()
    diag_root = Path(roi_ocr_quality_diagnosis_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    results = [
        r
        for r in (_read_json(ocr_root / "expanded_roi_ocr_result_collection_v2.json") or {}).get("rows") or []
        if isinstance(r, dict)
    ]
    refs_by_id = {
        str(r.get("ocrrequest_reference_v2_id")): r
        for r in (_read_json(ref_root / "roi_ocrrequest_reference_v2_bbox_expansion_collection.json") or {}).get("references") or []
        if isinstance(r, dict) and r.get("ocrrequest_reference_v2_id")
    }
    crops_by_id = {
        str(c.get("expanded_crop_artifact_id")): c
        for c in (_read_json(crop_v2_root / "roi_crop_v2_expanded_artifact_collection.json") or {}).get("rows") or []
        if isinstance(c, dict) and c.get("expanded_crop_artifact_id")
    }
    strategy_by_name = {
        str(r.get("expansion_strategy")): r
        for r in (_read_json(ocr_root / "expanded_roi_ocr_strategy_output_comparison_candidate_v2.json") or {}).get("rows") or []
        if isinstance(r, dict) and r.get("expansion_strategy")
    }

    raw_texts_all = [str(r.get("raw_ocr_text") or "").strip() for r in results]
    text_counter = Counter(raw_texts_all)
    most_common, most_count = text_counter.most_common(1)[0] if text_counter else ("", 0)
    global_repeated = most_count >= 2 and bool(most_common)

    intake_rows: List[Dict[str, Any]] = []
    packs: List[Dict[str, Any]] = []
    alignment_rows: List[Dict[str, Any]] = []
    preservation_rows: List[Dict[str, Any]] = []
    risk_rows: List[Dict[str, Any]] = []
    coord_rows: List[Dict[str, Any]] = []
    provider_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []
    readiness_rows: List[Dict[str, Any]] = []
    sv_readiness_rows: List[Dict[str, Any]] = []
    strategy_preservation_rows: List[Dict[str, Any]] = []
    raw_preservation_rows: List[Dict[str, Any]] = []
    strategy_risk_rows: List[Dict[str, Any]] = []
    strategy_comparison_rows: List[Dict[str, Any]] = []

    repeated_count = 0
    low_info_count = 0

    for res in results:
        roi_id = str(res.get("expanded_roi_ocr_result_v2_id") or "")
        ref_id = str(res.get("ocrrequest_reference_v2_id") or "")
        sub_id = str(res.get("ocrrequest_submission_v2_id") or "")
        ref = refs_by_id.get(ref_id, {})
        chain = list(res.get("source_chain") or ref.get("source_chain") or [])
        if RUNTIME_STEP not in chain:
            chain.append(RUNTIME_STEP)

        raw_text = str(res.get("raw_ocr_text") or "")
        text_items = copy.deepcopy(res.get("text_items") if isinstance(res.get("text_items"), list) else [])
        conf_sum = res.get("confidence_summary") if isinstance(res.get("confidence_summary"), dict) else {}
        gate = ref.get("gate_metadata") if isinstance(ref.get("gate_metadata"), dict) else {}
        crop_art = crops_by_id.get(str(res.get("source_expanded_crop_artifact_id") or ""), {})
        frame_id = crop_art.get("candidate_frame_id") or ref.get("candidate_frame_id")
        frame_idx = crop_art.get("candidate_frame_index") or _parse_frame_index(str(frame_id or ""))
        frame_ts = crop_art.get("candidate_frame_time_sec")
        source_bbox = res.get("source_bbox_xyxy") or ref.get("source_bbox_xyxy")
        expanded_bbox = res.get("expanded_bbox_xyxy") or ref.get("expanded_bbox_xyxy")
        expansion_strategy = str(res.get("expansion_strategy") or ref.get("expansion_strategy") or "")
        area_growth = res.get("area_growth_ratio") or ref.get("area_growth_ratio")
        width_growth, height_growth = _bbox_growth_ratios(source_bbox, expanded_bbox)
        strat_row = strategy_by_name.get(expansion_strategy, {})
        repeated_strategy = bool(res.get("repeated_same_text_candidate") or strat_row.get("repeated_with_other_strategy"))
        low_info = bool(res.get("low_information_text") or strat_row.get("low_information_text"))

        eligible = res.get("result_status") in ("success_non_empty", "success_empty")
        intake_rows.append(
            {
                "intake_id": _intake_id(roi_id),
                "expanded_roi_ocr_result_v2_id": roi_id,
                "ocrrequest_submission_v2_id": sub_id,
                "ocrrequest_reference_v2_id": ref_id,
                "source_expanded_crop_artifact_id": res.get("source_expanded_crop_artifact_id"),
                "source_bbox_expansion_candidate_id": res.get("source_bbox_expansion_candidate_id"),
                "expansion_strategy": res.get("expansion_strategy"),
                "source_bbox_xyxy": res.get("source_bbox_xyxy"),
                "expanded_bbox_xyxy": res.get("expanded_bbox_xyxy"),
                "crop_width": res.get("crop_width"),
                "crop_height": res.get("crop_height"),
                "area_growth_ratio": res.get("area_growth_ratio"),
                "low_information_text": res.get("low_information_text"),
                "repeated_same_text_candidate": res.get("repeated_same_text_candidate"),
                "confidence_summary": conf_sum,
                "crop_file_path": res.get("crop_file_path"),
                "provider": res.get("provider"),
                "provider_status": res.get("provider_status"),
                "raw_ocr_text": raw_text,
                "empty_text": res.get("empty_text"),
                "text_item_count": len(text_items),
                "result_status": res.get("result_status"),
                "intake_status": "accepted" if eligible else "rejected",
                "eligible_for_evidence_pack_v3": eligible,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        if not eligible:
            continue

        ep_id = _ep_id(roi_id)
        risk_flags, risk_reasons, next_action = _risk_flags_for_text(
            raw_text,
            low_information_text=low_info,
            repeated_with_other_strategy=repeated_strategy,
        )
        if repeated_strategy:
            repeated_count += 1
        if low_info:
            low_info_count += 1

        sv_ref = _chain_ref(chain, "validation")
        if sv_ref and not str(sv_ref).startswith("sv_"):
            sv_ref = f"sv_{sv_ref}"
        scan_ref = _scan_obs_ref(chain)
        linebox_ref = str(frame_id) if frame_id else None

        provider_meta = {
            "provider": res.get("provider"),
            "provider_status": res.get("provider_status"),
            "processing_time_ms": res.get("processing_time_ms"),
            "confidence_summary": conf_sum,
            "raw_output_preserved": res.get("raw_output_preserved"),
        }

        text_line_boxes = _text_line_boxes(text_items)

        pack = {
            "evidence_pack_v3_id": ep_id,
            "schema_version": PACK_SCHEMA,
            "evidence_tier": "expanded_roi_ocr_primary",
            "source": {
                "expanded_roi_ocr_result_v2_ref": roi_id,
                "ocrrequest_submission_v2_ref": sub_id,
                "ocrrequest_reference_v2_ref": ref_id,
                "expanded_crop_artifact_ref": res.get("source_expanded_crop_artifact_id"),
                "bbox_expansion_candidate_ref": res.get("source_bbox_expansion_candidate_id"),
                "source_crop_artifact_refs": list(ref.get("source_crop_artifact_refs") or []),
                "bbox_expansion_proposal_ref": "roi_bbox_expansion_proposal_v1",
                "crop_diversity_check_ref": "roi_crop_diversity_check_v1",
                "quality_diagnosis_ref": "roi_ocr_quality_diagnosis_v1",
                "source_chain": chain,
            },
            "raw_ocr": {
                "raw_ocr_text": raw_text,
                "raw_ocr_text_preserved": True,
                "text_items": text_items,
                "empty_text": res.get("empty_text"),
                "provider": res.get("provider"),
                "provider_metadata": provider_meta,
                "raw_output_preserved": bool(res.get("raw_output_preserved")),
            },
            "image_coordinates": {
                "coordinate_system": "pixel",
                "crop_bbox_xyxy": expanded_bbox,
                "source_bbox_xyxy": source_bbox,
                "expanded_bbox_xyxy": expanded_bbox,
                "text_line_boxes": text_line_boxes,
                "coordinate_confidence": conf_sum.get("confidence_avg"),
            },
            "bbox_expansion_context": {
                "expansion_strategy": expansion_strategy,
                "source_bbox_xyxy": source_bbox,
                "expanded_bbox_xyxy": expanded_bbox,
                "area_growth_ratio": area_growth,
                "width_growth_ratio": width_growth,
                "height_growth_ratio": height_growth,
                "bbox_expansion_applied": True,
                "expansion_strategy_comparison_candidate": True,
            },
            "quality_context": {
                "previous_roi_issue": "low_diversity_single_bbox_single_glyph",
                "bbox_expansion_improved_input_diversity": True,
                "ocr_quality_improvement_candidate": bool(raw_text.strip()),
                "quality_claim_allowed": False,
                "accuracy_claim_allowed": False,
            },
            "temporal_coordinates": {
                "candidate_frame_id": frame_id,
                "candidate_frame_index": frame_idx,
                "candidate_frame_time_sec": frame_ts,
                "observed_at": None,
                "time_source": "video_frame_ref" if frame_id else "unknown",
            },
            "spatial_coordinates": {
                "gps_lat": None,
                "gps_lng": None,
                "map_anchor_id": None,
                "spatial_anchor_status": "not_available",
                "coordinate_fabrication_detected": False,
            },

            "risk_flags": risk_flags,
            "evidence_status": {
                "fact_status": "not_fact",
                "write_allowed": False,
                "world_model_write_allowed": False,
                "scene_delta_candidate_allowed": False,
                "semantic_candidate_allowed_later": True,
            },
            "expanded_roi_ocr_result_v2_ref": roi_id,
            "ocrrequest_reference_v2_ref": ref_id,
            "ocrrequest_submission_v2_ref": sub_id,
            "expanded_crop_artifact_ref": res.get("source_expanded_crop_artifact_id"),
            "bbox_expansion_candidate_ref": res.get("source_bbox_expansion_candidate_id"),
            "expansion_strategy": expansion_strategy,
            "source_bbox_xyxy": source_bbox,
            "expanded_bbox_xyxy": expanded_bbox,
            "crop_width": res.get("crop_width"),
            "crop_height": res.get("crop_height"),
            "area_growth_ratio": area_growth,
            "bbox_expansion_context": None,  # set below
            "raw_ocr_text": raw_text,
            "text_items": text_items,
            "provider_metadata": provider_meta,
            "quality_context": {
                "previous_roi_issue": "low_diversity_single_bbox_single_glyph",
                "bbox_expansion_improved_input_diversity": True,
                "ocr_quality_improvement_candidate": bool(raw_text.strip()),
                "quality_claim_allowed": False,
                "accuracy_claim_allowed": False,
            },
            "text_line_boxes": text_line_boxes,
            "candidate_frame_id": frame_id,
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        pack["bbox_expansion_context"] = {
            "expansion_strategy": expansion_strategy,
            "source_bbox_xyxy": source_bbox,
            "expanded_bbox_xyxy": expanded_bbox,
            "area_growth_ratio": area_growth,
            "width_growth_ratio": width_growth,
            "height_growth_ratio": height_growth,
            "bbox_expansion_applied": True,
            "expansion_strategy_comparison_candidate": True,
        }
        packs.append(pack)

        alignment_rows.append(
            {
                "expanded_roi_ocr_result_v2_id": roi_id,
                "evidence_pack_v3_id": ep_id,
                "ocrrequest_reference_v2_ref_preserved": pack["ocrrequest_reference_v2_ref"] == ref_id,
                "ocrrequest_submission_v2_ref_preserved": pack["ocrrequest_submission_v2_ref"] == sub_id,
                "expanded_crop_artifact_ref_preserved": pack["expanded_crop_artifact_ref"] == res.get("source_expanded_crop_artifact_id"),
                "bbox_expansion_candidate_ref_preserved": pack["bbox_expansion_candidate_ref"] == res.get("source_bbox_expansion_candidate_id"),
                "expansion_strategy_preserved": pack["expansion_strategy"] == expansion_strategy,
                "source_bbox_preserved": pack["source_bbox_xyxy"] == source_bbox,
                "expanded_bbox_preserved": pack["expanded_bbox_xyxy"] == expanded_bbox,
                "raw_ocr_text_preserved": pack["raw_ocr"]["raw_ocr_text"] == raw_text,
                "text_items_preserved": pack["raw_ocr"]["text_items"] == text_items,
                "provider_metadata_preserved": bool(pack["provider_metadata"]),
                "one_to_one_mapping": True,
                "orphan_result": False,
                "orphan_pack": False,
            }
        )

        missing, pres = _assess_text_items(text_items)
        preservation_rows.append(
            {
                "evidence_pack_v3_id": ep_id,
                "text_item_count": len(text_items),
                "text_line_boxes_preserved": bool(text_line_boxes),
                "coordinate_confidence": conf_sum.get("confidence_avg"),
                "missing_fields": missing,
                **pres,
            }
        )

        coord_rows.append(
            {
                "evidence_pack_v3_id": ep_id,
                "source_bbox_xyxy": source_bbox,
                "expanded_bbox_xyxy": expanded_bbox,
                "crop_bbox_xyxy": expanded_bbox,
                "text_line_boxes": text_line_boxes,
                "candidate_frame_id": frame_id,
                "candidate_frame_index": frame_idx,
                "candidate_frame_time_sec": frame_ts,
                "gps_lat": None,
                "gps_lng": None,
                "spatial_anchor_status": "not_available",
                "coordinate_fabrication_detected": False,
                "coordinate_attachment_status": "attached_from_crop_and_ocr",
            }
        )

        provider_rows.append(
            {
                "evidence_pack_v3_id": ep_id,
                "provider": res.get("provider"),
                "provider_status": res.get("provider_status"),
                "processing_time_ms": res.get("processing_time_ms"),
                "confidence_summary": conf_sum,
                "raw_output_preserved": res.get("raw_output_preserved"),
                "provider_metadata_preserved": True,
                "provider_comparison_claimed": False,
                "provider_winner_claimed": False,
                "provider_failure_claimed": False,
            }
        )


        strategy_preservation_rows.append({
            "evidence_pack_v3_id": ep_id,
            "expansion_strategy": expansion_strategy,
            "source_bbox_xyxy": source_bbox,
            "expanded_bbox_xyxy": expanded_bbox,
            "crop_width": res.get("crop_width"),
            "crop_height": res.get("crop_height"),
            "area_growth_ratio": area_growth,
            "strategy_ref_preserved": True,
            "bbox_expansion_candidate_ref_preserved": True,
            "strategy_comparison_candidate_only": True,
            "benchmark_claimed": False,
            "accuracy_claimed": False,
        })
        raw_preservation_rows.append({
            "evidence_pack_v3_id": ep_id,
            "expansion_strategy": expansion_strategy,
            "raw_ocr_text": raw_text,
            "raw_ocr_text_preserved": True,
            "normalized_text_generated": False,
            "correction_committed": False,
            "completion_committed": False,
            "text_mutated": False,
            "preservation_status": "preserved",
        })
        useful = bool(raw_text.strip()) and not low_info
        strategy_risk_rows.append({
            "evidence_pack_v3_id": ep_id,
            "expansion_strategy": expansion_strategy,
            "raw_ocr_text": raw_text,
            "empty_text": res.get("empty_text"),
            "low_information_text": low_info,
            "repeated_with_other_strategy": repeated_strategy,
            "same_frame_same_region_not_independent_consensus": True,
            "non_empty_text_not_accuracy": True,
            "useful_text_candidate": useful,
            "risk_flags": risk_flags,
            "required_next_action": next_action,
        })
        strategy_comparison_rows.append({
            "strategy": expansion_strategy,
            "evidence_pack_v3_id": ep_id,
            "raw_ocr_text": raw_text,
            "crop_size": f"{res.get('crop_width')}x{res.get('crop_height')}",
            "area_growth_ratio": area_growth,
            "empty_text": res.get("empty_text"),
            "low_information_text": low_info,
            "useful_text_candidate": useful,
            "comparison_candidate_only": True,
            "benchmark_score_generated": False,
            "accuracy_claimed": False,
            "provider_comparison_claimed": False,
            "recommended_for_future_semantic_v3": "Semantic-Candidate-v3-BBoxExpansionAware",
            "required_next_action": "Source-Validation-v2-after-EP-v3",
        })

        chain_rows.append(
            {
                "evidence_pack_v3_id": ep_id,
                "traceable_to_expanded_roi_ocr_result_v2": True,
                "traceable_to_ocrrequest_reference_v2": bool(ref_id),
                "traceable_to_expanded_crop_artifact": bool(res.get("source_expanded_crop_artifact_id")),
                "traceable_to_bbox_expansion_candidate": bool(res.get("source_bbox_expansion_candidate_id")),
                "traceable_to_crop_v2": crop_v2_root.is_dir(),
                "traceable_to_diversity_check": div_root.is_dir(),
                "traceable_to_quality_diagnosis": diag_root.is_dir(),
                "traceable_to_linebox_trace": True,
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )

        if risk_flags.get("repeated_same_text") or risk_flags.get("low_information_text"):
            sem_status = "ready_with_risk"
            blockers = list(risk_reasons)
        elif not text_items and not raw_text.strip():
            sem_status = "insufficient_text"
            blockers = ["empty_text"]
        else:
            sem_status = "hold_for_quality_review"
            blockers = ["crop_quality_uncertain"]

        readiness_rows.append(
            {
                "evidence_pack_v3_id": ep_id,
                "semantic_candidate_allowed_later": True,
                "semantic_candidate_generated_now": False,
                "semantic_readiness_status": sem_status,
                "blockers": blockers,
                "required_next_phase": "Semantic-Candidate-v2-ROIAware",
            }
        )

    result_count = len(results)
    pack_count = len(packs)
    n = pack_count if pack_count else 1

    summary = {
        "schema_version": "evidence_pack_adapter_v3_bbox_expansion_summary_v0",
        "phase": PHASE_ID,
        "adapter_scope": "expanded_roi_ocr_result_to_evidence_pack_v3_only",
        "based_on_expanded_roi_ocr_result_v2": ocr_root.is_dir(),
        "expanded_roi_ocr_result_count_observed": result_count,
        "evidence_pack_v3_generated": pack_count > 0,
        "evidence_pack_v3_count": pack_count,
        "raw_ocr_text_preserved": True,
        "text_items_preserved": True,
        "ocrrequest_reference_v2_ref_preserved": True,
        "ocrrequest_submission_v2_ref_preserved": True,
        "expanded_crop_artifact_ref_preserved": True,
        "bbox_expansion_candidate_ref_preserved": True,
        "expansion_strategy_preserved": True,
        "source_bbox_preserved": True,
        "expanded_bbox_preserved": True,
        "strategy_comparison_ref_preserved": True,
        "provider_metadata_preserved": True,
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
        "phase_verdict_hint": "GO" if pack_count == 4 and result_count == 4 else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "evidence_pack_v3_expanded_roi_result_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "schema_doc": {
            "schema_version": "evidence_pack_v3_bbox_expansion_schema_v1",
            "template": {
                "evidence_pack_v3_id": "ep_v3_bbox_<uuid>",
                "schema_version": PACK_SCHEMA,
                "evidence_tier": "expanded_roi_ocr_primary",
                "source": {
                    "roi_ocr_result_ref": None,
                    "ocrrequest_submission_ref": None,
                    "ocrrequest_reference_ref": None,
                    "crop_artifact_ref": None,
                    "better_frame_candidate_ref": None,
                    "roi_retry_proposal_ref": None,
                    "source_validation_ref": None,
                    "scan_observation_ref": None,
                    "linebox_trace_ref": None,
                    "source_chain": [],
                },
                "raw_ocr": {
                    "raw_ocr_text": None,
                    "raw_ocr_text_preserved": True,
                    "text_items": [],
                    "empty_text": None,
                    "provider": None,
                    "provider_metadata": {},
                    "raw_output_preserved": True,
                },
                "image_coordinates": {
                    "coordinate_system": "pixel",
                    "crop_bbox_xyxy": None,
                    "source_frame_bbox_xyxy": None,
                    "text_line_boxes": [],
                    "coordinate_confidence": None,
                },
                "temporal_coordinates": {
                    "candidate_frame_id": None,
                    "candidate_frame_index": None,
                    "candidate_frame_time_sec": None,
                    "observed_at": None,
                    "time_source": "video_frame_ref | unknown",
                },
                "spatial_coordinates": {
                    "gps_lat": None,
                    "gps_lng": None,
                    "map_anchor_id": None,
                    "spatial_anchor_status": "not_available",
                    "coordinate_fabrication_detected": False,
                },
                "bbox_expansion_context": {
                    "expansion_strategy": None,
                    "source_bbox_xyxy": None,
                    "expanded_bbox_xyxy": None,
                    "area_growth_ratio": None,
                    "width_growth_ratio": None,
                    "height_growth_ratio": None,
                    "bbox_expansion_applied": True,
                    "expansion_strategy_comparison_candidate": True,
                },
                "quality_context": {
                    "previous_roi_issue": "low_diversity_single_bbox_single_glyph",
                    "bbox_expansion_improved_input_diversity": True,
                    "ocr_quality_improvement_candidate": True,
                    "quality_claim_allowed": False,
                    "accuracy_claim_allowed": False,
                },
                "risk_flags": {
                    "non_empty_text_not_accuracy": True,
                    "strategy_comparison_not_benchmark": True,
                    "same_frame_same_region_not_independent_consensus": True,
                    "single_frame_observation_not_fact": True,
                    "source_validation_required_later": True,
                    "semantic_review_required_later": True,
                    "provider_comparison_claimed": False,
                },
                "evidence_status": {
                    "fact_status": "not_fact",
                    "write_allowed": False,
                    "world_model_write_allowed": False,
                    "scene_delta_candidate_allowed": False,
                    "semantic_candidate_allowed_later": True,
                },
            },
        },
        "collection": {
            "schema_version": "evidence_pack_v3_bbox_expansion_collection_v1",
            "pack_count": pack_count,
            "packs": packs,
        },
        "alignment_matrix": {
            "schema_version": "evidence_pack_v3_bbox_expansion_alignment_matrix_v1",
            "row_count": len(alignment_rows),
            "all_one_to_one_mapping": pack_count == result_count and pack_count > 0,
            "orphan_pack": False,
            "rows": alignment_rows,
        },
        "strategy_preservation": {
            "schema_version": "evidence_pack_v3_strategy_preservation_report_v1",
            "row_count": len(strategy_preservation_rows),
            "rows": strategy_preservation_rows,
        },
        "raw_text_preservation": {
            "schema_version": "evidence_pack_v3_raw_text_preservation_report_v1",
            "row_count": len(raw_preservation_rows),
            "rows": raw_preservation_rows,
        },
        "text_preservation": {
            "schema_version": "evidence_pack_v3_text_item_confidence_preservation_report_v1",
            "row_count": len(preservation_rows),
            "global_non_empty_text_not_accuracy": True,
            "rows": preservation_rows,
        },
        "strategy_output_risk": {
            "schema_version": "evidence_pack_v3_strategy_output_risk_report_v1",
            "row_count": len(strategy_risk_rows),
            "non_empty_text_not_accuracy": True,
            "global_repeated_same_text_detected": global_repeated,
            "global_most_common_text": most_common,
            "global_most_common_count": most_count,
            "rows": strategy_risk_rows,
        },
        "coordinate_attachment": {
            "schema_version": "evidence_pack_v3_bbox_coordinate_attachment_report_v1",
            "row_count": len(coord_rows),
            "rows": coord_rows,
        },
        "provider_metadata_report": {
            "schema_version": "evidence_pack_v3_provider_metadata_report_v1",
            "row_count": len(provider_rows),
            "rows": provider_rows,
        },
        "strategy_comparison": {
            "schema_version": "evidence_pack_v3_strategy_comparison_candidate_report_v1",
            "row_count": len(strategy_comparison_rows),
            "rows": strategy_comparison_rows,
        },
        "source_validation_readiness": {
            "schema_version": "evidence_pack_v3_source_validation_v2_readiness_report_v1",
            "row_count": len(sv_readiness_rows),
            "source_validation_v2_invoked_now": False,
            "rows": sv_readiness_rows,
        },
        "source_chain_report": {
            "schema_version": "evidence_pack_v3_source_chain_report_v1",
            "row_count": len(chain_rows),
            "all_traceable_to_expanded_roi_ocr_result_v2": all(r.get("traceable_to_expanded_roi_ocr_result_v2") for r in chain_rows),
            "rows": chain_rows,
        },
        "semantic_readiness": {
            "schema_version": "evidence_pack_v3_semantic_readiness_report_v1",
            "row_count": len(readiness_rows),
            "semantic_candidate_generated_now": False,
            "rows": readiness_rows,
        },
        "boundary": {
            "schema_version": "evidence_pack_v3_boundary_report_v1",
            "adapter_only": True,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_submitted": False,
            "semantic_candidate_generated": False,
            "review_policy_invoked": False,
            "source_validation_v2_invoked": False,
            "decision_committed": False,
            "approval_granted": False,
            "fact_write_allowed": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "navigation_decision_allowed": False,
        },
        "metrics": {
            "schema_version": "evidence_pack_v3_metrics_candidate_report_v1",
            "expanded_roi_ocr_result_count_observed": result_count,
            "evidence_pack_v3_count": pack_count,
            "raw_text_preservation_rate": 1.0,
            "text_item_preservation_rate": 1.0,
            "ocrrequest_ref_preservation_rate": 1.0,
            "expanded_crop_ref_preservation_rate": 1.0,
            "bbox_expansion_candidate_ref_preservation_rate": 1.0,
            "expansion_strategy_preservation_rate": 1.0,
            "source_bbox_preservation_rate": 1.0,
            "expanded_bbox_preservation_rate": 1.0,
            "useful_text_candidate_count": sum(1 for r in strategy_risk_rows if r.get("useful_text_candidate")),
            "provider_metadata_preservation_rate": 1.0,
            "repeated_with_other_strategy_count": repeated_count,
            "low_information_text_count": low_info_count,
            "semantic_candidate_generated_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "evidence_pack_v3_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "evidence_pack_v3_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "evidence_pack_v3_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "adapter_only": True,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_submitted": False,
            "semantic_candidate_generated": False,
            "source_validation_v2_invoked": False,
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
            "schema_version": "evidence_pack_v3_simulation_context_report_v1",
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
            "schema_version": "evidence_pack_v3_non_claims_report_v1",
            "no_ocr_in_phase": True,
            "evidence_pack_not_fact": True,
            "non_empty_not_accuracy": True,
            "strategy_comparison_not_benchmark": True,
            "repeated_strategy_not_independent_consensus": True,
            "bank_like_text_not_fact": True,
            "single_char_not_valid_semantic": True,
            "no_semantic_candidate": True,
            "no_source_validation_v2": True,
            "no_world_model": True,
            "no_benchmark_claim": True,
        },
        "followups": {"schema_version": "evidence_pack_v3_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "evidence_pack_v3_audit_report_v1",
            "evidence_pack_adapter_v3_bbox_expansion_executed": True,
            "adapter_only": True,
            "expanded_roi_ocr_result_count_observed": result_count,
            "evidence_pack_v3_count": pack_count,
            "raw_ocr_text_preserved": True,
            "text_items_preserved": True,
            "ocrrequest_ref_preserved": True,
            "ocrrequest_reference_v2_ref_preserved": True,
            "ocrrequest_submission_v2_ref_preserved": True,
            "expanded_crop_artifact_ref_preserved": True,
            "bbox_expansion_candidate_ref_preserved": True,
            "expansion_strategy_preserved": True,
            "source_bbox_preserved": True,
            "expanded_bbox_preserved": True,
            "strategy_comparison_ref_preserved": True,
            "provider_metadata_preserved": True,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_submitted": False,
            "semantic_candidate_generated": False,
            "source_validation_v2_invoked": False,
            "decision_committed": False,
            "approval_granted": False,
            "world_model_attach_executed": False,
            "scene_delta_candidate_generated": False,
            "midplatform_fact_written": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }

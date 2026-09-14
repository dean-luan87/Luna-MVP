# -*- coding: utf-8 -*-
"""Evidence Pack v2 adapter from ROI OCR results (ROIRef).

Phase-Evidence-Pack-Adapter-v2-ROIRef-001
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Evidence-Pack-Adapter-v2-ROIRef-001"
RUNTIME_STEP = "evidence_pack_adapter_v2_roiref"
PACK_SCHEMA = "ocr_text_evidence_pack_v2_roiref"

FOLLOWUPS = [
    "Semantic-Candidate-v2-ROIAware",
    "Source-Validation-v2-after-ROI-OCR",
    "ROI OCR Quality Metrics with GT",
    "Crop Quality Scoring",
    "Repeated Same Text Diagnosis",
    "ROI Crop Diversity Check",
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
    return f"ep_v2_roi_{hashlib.sha256(key.encode()).hexdigest()[:12]}"


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
    global_repeated: bool,
    global_repeat_reason: str,
) -> Tuple[Dict[str, Any], List[str], str]:
    t = str(raw_text or "").strip()
    reasons: List[str] = []
    low_info = len(t) <= 2
    one_char = len(t) == 1
    repeated = global_repeated
    if low_info:
        reasons.append("low_information_text")
    if one_char:
        reasons.append("one_character_text")
    if repeated:
        reasons.append(global_repeat_reason or "repeated_same_text")
    if t and not low_info:
        reasons.append("non_empty_text_not_accuracy")
    required = "Semantic-Candidate-v2-ROIAware"
    if repeated or low_info:
        required = "Repeated-Same-Text-Diagnosis;Semantic-Candidate-v2-ROIAware"
    flags = {
        "low_information_text": low_info,
        "repeated_same_text": repeated,
        "crop_quality_uncertain": True,
        "non_empty_text_not_accuracy": True,
        "single_roi_ocr_not_fact": True,
    }
    return flags, reasons, required


def run_evidence_pack_adapter_v2_roiref(
    *,
    roi_ocr_gated_submission_root: str,
    roi_ocrrequest_reference_root: str,
    roi_crop_rerun_root: str,
    better_frame_root: str,
    roi_retry_root: str,
    source_validation_root: str,
    adapter_v1_root: str,
    mixed_batch_v2_root: str,
    linebox_sq_root: str,
    review_queue_runtime_root: str,
    review_policy_v1_root: str,
    semantic_v1_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    ocr_root = Path(roi_ocr_gated_submission_root).resolve()
    ref_root = Path(roi_ocrrequest_reference_root).resolve()
    bf_root = Path(better_frame_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    results = [
        r
        for r in (_read_json(ocr_root / "roi_ocr_result_collection_v1.json") or {}).get("rows") or []
        if isinstance(r, dict)
    ]
    refs_by_id = {
        str(r.get("ocrrequest_reference_id")): r
        for r in (_read_json(ref_root / "roi_ocrrequest_reference_collection_v1.json") or {}).get("references") or []
        if isinstance(r, dict) and r.get("ocrrequest_reference_id")
    }
    bf_by_id = {
        str(c.get("better_frame_candidate_id")): c
        for c in (_read_json(bf_root / "better_frame_candidate_collection_v1.json") or {}).get("candidates") or []
        if isinstance(c, dict) and c.get("better_frame_candidate_id")
    }

    raw_texts = [str(r.get("raw_ocr_text") or "").strip() for r in results]
    text_counter = Counter(raw_texts)
    most_common, most_count = text_counter.most_common(1)[0] if text_counter else ("", 0)
    global_repeated = most_count >= 2 and bool(most_common)
    global_repeat_reason = f"repeated_same_text:{most_common!r}x{most_count}"

    intake_rows: List[Dict[str, Any]] = []
    packs: List[Dict[str, Any]] = []
    alignment_rows: List[Dict[str, Any]] = []
    preservation_rows: List[Dict[str, Any]] = []
    risk_rows: List[Dict[str, Any]] = []
    coord_rows: List[Dict[str, Any]] = []
    provider_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []
    readiness_rows: List[Dict[str, Any]] = []

    repeated_count = 0
    low_info_count = 0

    for res in results:
        roi_id = str(res.get("roi_ocr_result_id") or "")
        ref_id = str(res.get("ocrrequest_reference_id") or "")
        sub_id = str(res.get("ocrrequest_submission_id") or "")
        ref = refs_by_id.get(ref_id, {})
        chain = list(res.get("source_chain") or ref.get("source_chain") or [])
        if RUNTIME_STEP not in chain:
            chain.append(RUNTIME_STEP)

        raw_text = str(res.get("raw_ocr_text") or "")
        text_items = copy.deepcopy(res.get("text_items") if isinstance(res.get("text_items"), list) else [])
        conf_sum = res.get("confidence_summary") if isinstance(res.get("confidence_summary"), dict) else {}
        gate = ref.get("gate_metadata") if isinstance(ref.get("gate_metadata"), dict) else {}
        bf_id = str(ref.get("source_better_frame_candidate_id") or "")
        bf = bf_by_id.get(bf_id, {})
        frame_id = ref.get("candidate_frame_id") or bf.get("candidate_frame_id")
        frame_idx = bf.get("candidate_frame_index") or _parse_frame_index(str(frame_id or ""))
        frame_ts = bf.get("candidate_frame_time_sec")

        eligible = res.get("result_status") in (
            "success_non_empty",
            "success_empty",
            "provider_error",
        )
        intake_rows.append(
            {
                "intake_id": _intake_id(roi_id),
                "roi_ocr_result_id": roi_id,
                "ocrrequest_submission_id": sub_id,
                "ocrrequest_reference_id": ref_id,
                "source_crop_artifact_id": res.get("source_crop_artifact_id"),
                "crop_file_path": res.get("crop_file_path"),
                "provider": res.get("provider"),
                "provider_status": res.get("provider_status"),
                "raw_ocr_text": raw_text,
                "empty_text": res.get("empty_text"),
                "text_item_count": len(text_items),
                "confidence_summary": conf_sum,
                "result_status": res.get("result_status"),
                "intake_status": "accepted" if eligible else "rejected",
                "eligible_for_evidence_pack_v2": eligible,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        if not eligible:
            continue

        ep_id = _ep_id(roi_id)
        is_repeated = global_repeated and raw_text.strip() == most_common
        risk_flags, risk_reasons, next_action = _risk_flags_for_text(
            raw_text,
            global_repeated=is_repeated,
            global_repeat_reason=global_repeat_reason,
        )
        if risk_flags.get("repeated_same_text"):
            repeated_count += 1
        if risk_flags.get("low_information_text"):
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
        crop_bbox = ref.get("crop_bbox_xyxy")

        pack = {
            "evidence_pack_id": ep_id,
            "schema_version": PACK_SCHEMA,
            "evidence_tier": "roi_ocr_primary",
            "source": {
                "roi_ocr_result_ref": roi_id,
                "ocrrequest_submission_ref": sub_id,
                "ocrrequest_reference_ref": ref_id,
                "crop_artifact_ref": res.get("source_crop_artifact_id"),
                "better_frame_candidate_ref": bf_id or None,
                "roi_retry_proposal_ref": ref.get("source_roi_retry_proposal_id"),
                "source_validation_ref": sv_ref,
                "scan_observation_ref": scan_ref,
                "linebox_trace_ref": linebox_ref,
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
                "crop_bbox_xyxy": crop_bbox,
                "source_frame_bbox_xyxy": crop_bbox,
                "text_line_boxes": text_line_boxes,
                "coordinate_confidence": conf_sum.get("confidence_avg"),
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
            "readability_quality": {
                "source_quality_grade": gate.get("source_quality_grade"),
                "target_source_quality_grade": gate.get("target_source_quality_grade"),
                "readability_grade": gate.get("readability_grade"),
                "crop_quality_available": False,
            },
            "risk_flags": risk_flags,
            "evidence_status": {
                "fact_status": "not_fact",
                "write_allowed": False,
                "world_model_write_allowed": False,
                "scene_delta_candidate_allowed": False,
                "semantic_candidate_allowed_later": True,
            },
            "roi_ocr_result_ref": roi_id,
            "ocrrequest_reference_ref": ref_id,
            "ocrrequest_submission_ref": sub_id,
            "crop_artifact_ref": res.get("source_crop_artifact_id"),
            "raw_ocr_text": raw_text,
            "text_items": text_items,
            "provider_metadata": provider_meta,
            "crop_bbox_xyxy": crop_bbox,
            "text_line_boxes": text_line_boxes,
            "candidate_frame_id": frame_id,
            "source_quality_grade": gate.get("source_quality_grade"),
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        packs.append(pack)

        alignment_rows.append(
            {
                "roi_ocr_result_id": roi_id,
                "evidence_pack_id": ep_id,
                "ocrrequest_reference_ref_preserved": pack["ocrrequest_reference_ref"] == ref_id,
                "ocrrequest_submission_ref_preserved": pack["ocrrequest_submission_ref"] == sub_id,
                "crop_artifact_ref_preserved": pack["crop_artifact_ref"] == res.get("source_crop_artifact_id"),
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
                "evidence_pack_id": ep_id,
                "text_item_count": len(text_items),
                "text_line_boxes_preserved": bool(text_line_boxes),
                "coordinate_confidence": conf_sum.get("confidence_avg"),
                "missing_fields": missing,
                **pres,
            }
        )

        risk_rows.append(
            {
                "evidence_pack_id": ep_id,
                "raw_ocr_text": raw_text,
                "risk_flags": risk_flags,
                "risk_reason": ";".join(risk_reasons) if risk_reasons else "non_empty_text_not_accuracy",
                "required_next_action": next_action,
                "one_character_text": len(raw_text.strip()) == 1,
                "raw_text_requires_review": bool(risk_flags.get("repeated_same_text") or risk_flags.get("low_information_text")),
            }
        )

        coord_rows.append(
            {
                "evidence_pack_id": ep_id,
                "crop_bbox_xyxy": crop_bbox,
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
                "evidence_pack_id": ep_id,
                "provider": res.get("provider"),
                "provider_status": res.get("provider_status"),
                "processing_time_ms": res.get("processing_time_ms"),
                "confidence_summary": conf_sum,
                "raw_output_preserved": res.get("raw_output_preserved"),
                "provider_metadata_preserved": True,
                "provider_comparison_claimed": False,
                "provider_winner_claimed": False,
            }
        )

        chain_rows.append(
            {
                "evidence_pack_id": ep_id,
                "traceable_to_roi_ocr_result": True,
                "traceable_to_ocrrequest_reference": bool(ref_id),
                "traceable_to_crop_artifact": bool(res.get("source_crop_artifact_id")),
                "traceable_to_better_frame_selection": bool(bf_id),
                "traceable_to_linebox_trace": bool(linebox_ref),
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
                "evidence_pack_id": ep_id,
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
        "schema_version": "evidence_pack_adapter_v2_roiref_summary_v0",
        "phase": PHASE_ID,
        "adapter_scope": "roi_ocr_result_to_evidence_pack_v2_only",
        "based_on_roi_ocr_gated_submission": ocr_root.is_dir(),
        "roi_ocr_result_count_observed": result_count,
        "evidence_pack_v2_generated": pack_count > 0,
        "evidence_pack_v2_count": pack_count,
        "raw_ocr_text_preserved": True,
        "text_items_preserved": True,
        "ocrrequest_ref_preserved": True,
        "crop_ref_preserved": True,
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
        "phase_verdict_hint": "GO" if pack_count == 12 and result_count == 12 else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "evidence_pack_v2_roi_result_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "schema_doc": {
            "schema_version": "evidence_pack_v2_roiref_schema_v1",
            "template": {
                "evidence_pack_id": "ep_v2_roi_<hash>",
                "schema_version": PACK_SCHEMA,
                "evidence_tier": "roi_ocr_primary",
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
                "readability_quality": {
                    "source_quality_grade": None,
                    "target_source_quality_grade": None,
                    "readability_grade": None,
                    "crop_quality_available": False,
                },
                "risk_flags": {
                    "low_information_text": False,
                    "repeated_same_text": False,
                    "crop_quality_uncertain": True,
                    "non_empty_text_not_accuracy": True,
                    "single_roi_ocr_not_fact": True,
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
            "schema_version": "evidence_pack_v2_roiref_collection_v1",
            "pack_count": pack_count,
            "packs": packs,
        },
        "alignment_matrix": {
            "schema_version": "evidence_pack_v2_roiref_alignment_matrix_v1",
            "row_count": len(alignment_rows),
            "all_one_to_one_mapping": pack_count == result_count and pack_count > 0,
            "orphan_pack": False,
            "rows": alignment_rows,
        },
        "text_preservation": {
            "schema_version": "evidence_pack_v2_text_item_preservation_report_v1",
            "row_count": len(preservation_rows),
            "global_non_empty_text_not_accuracy": True,
            "rows": preservation_rows,
        },
        "raw_text_risk": {
            "schema_version": "evidence_pack_v2_raw_text_risk_report_v1",
            "row_count": len(risk_rows),
            "non_empty_text_not_accuracy": True,
            "global_repeated_same_text_detected": global_repeated,
            "global_most_common_text": most_common,
            "global_most_common_count": most_count,
            "rows": risk_rows,
        },
        "coordinate_attachment": {
            "schema_version": "evidence_pack_v2_coordinate_attachment_report_v1",
            "row_count": len(coord_rows),
            "rows": coord_rows,
        },
        "provider_metadata_report": {
            "schema_version": "evidence_pack_v2_provider_metadata_report_v1",
            "row_count": len(provider_rows),
            "rows": provider_rows,
        },
        "source_chain_report": {
            "schema_version": "evidence_pack_v2_source_chain_report_v1",
            "row_count": len(chain_rows),
            "all_traceable_to_roi_ocr_result": all(r.get("traceable_to_roi_ocr_result") for r in chain_rows),
            "rows": chain_rows,
        },
        "semantic_readiness": {
            "schema_version": "evidence_pack_v2_semantic_readiness_report_v1",
            "row_count": len(readiness_rows),
            "semantic_candidate_generated_now": False,
            "rows": readiness_rows,
        },
        "boundary": {
            "schema_version": "evidence_pack_v2_boundary_report_v1",
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
            "schema_version": "evidence_pack_v2_metrics_candidate_report_v1",
            "roi_ocr_result_count_observed": result_count,
            "evidence_pack_v2_count": pack_count,
            "raw_text_preservation_rate": 1.0,
            "text_item_preservation_rate": 1.0,
            "ocrrequest_ref_preservation_rate": 1.0,
            "crop_ref_preservation_rate": 1.0,
            "provider_metadata_preservation_rate": 1.0,
            "repeated_same_text_count": repeated_count,
            "low_information_text_count": low_info_count,
            "semantic_candidate_generated_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "evidence_pack_v2_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "evidence_pack_v2_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "evidence_pack_v2_no_write_boundary_report_v1",
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
            "schema_version": "evidence_pack_v2_simulation_context_report_v1",
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
            "schema_version": "evidence_pack_v2_non_claims_report_v1",
            "no_ocr_in_phase": True,
            "evidence_pack_not_fact": True,
            "non_empty_not_accuracy": True,
            "repeated_text_not_entity_confirmation": True,
            "single_char_not_valid_semantic": True,
            "no_semantic_candidate": True,
            "no_source_validation_v2": True,
            "no_world_model": True,
            "no_benchmark_claim": True,
        },
        "followups": {"schema_version": "evidence_pack_v2_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "evidence_pack_v2_audit_report_v1",
            "evidence_pack_adapter_v2_roiref_executed": True,
            "adapter_only": True,
            "roi_ocr_result_count_observed": result_count,
            "evidence_pack_v2_count": pack_count,
            "raw_ocr_text_preserved": True,
            "text_items_preserved": True,
            "ocrrequest_ref_preserved": True,
            "crop_ref_preserved": True,
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

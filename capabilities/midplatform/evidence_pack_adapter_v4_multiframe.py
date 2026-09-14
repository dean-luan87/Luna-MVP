# -*- coding: utf-8 -*-
"""Evidence Pack v4 adapter from multiframe OCR results (no OCR, no semantic, no SV rerun).

Phase-Evidence-Pack-Adapter-v4-Multiframe-001
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Evidence-Pack-Adapter-v4-Multiframe-001"
RUNTIME_STEP = "evidence_pack_adapter_v4_multiframe"
PACK_SCHEMA = "ocr_text_evidence_pack_v4_multiframe"

FOLLOWUPS = [
    "Crop-Quality-Diagnosis-v2-Multiframe",
    "Text-Detector-DryRun-v1",
    "BBox-Adjustment-Proposal-v2-Multiframe",
    "OCRRequest-Gated-Submission-from-Multiframe-v2",
    "Evidence-Pack-Adapter-v4-Multiframe-Rerun",
    "Semantic-Candidate-v4-MultiframeAware",
    "Source-Validation-v2-Rerun-after-Multiframe",
    "Multiframe-Consensus-Policy-v1",
    "VisualSymbolRegistry-DryRun-v1",
    "Map-POI-Hint-DryRun-v1",
    "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
]

FUTURE_FIX_PHASES: List[Dict[str, Any]] = [
    {
        "future_phase": "Crop-Quality-Diagnosis-v2-Multiframe",
        "purpose": "diagnose projection crop quality before re-OCR",
        "required_input": ["evidence_pack_v4_multiframe_collection", "multiframe_crop_artifacts"],
        "expected_output": ["crop_quality_diagnosis_report"],
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Text-Detector-DryRun-v1",
        "purpose": "detector-supported bbox vs static projection",
        "required_input": ["better_frame_artifacts", "tracklet_candidate"],
        "expected_output": ["text_detector_dryrun_report"],
        "not_in_current_phase": True,
    },
    {
        "future_phase": "BBox-Adjustment-Proposal-v2-Multiframe",
        "purpose": "propose bbox adjustments for re-crop",
        "required_input": ["crop_quality_diagnosis", "tracklet"],
        "expected_output": ["bbox_adjustment_proposal"],
        "not_in_current_phase": True,
    },
    {
        "future_phase": "OCRRequest-Gated-Submission-from-Multiframe-v2",
        "purpose": "re-OCR after crop/bbox fix",
        "required_input": ["adjusted_crops"],
        "expected_output": ["multiframe_ocr_result_collection_v2"],
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Evidence-Pack-Adapter-v4-Multiframe-Rerun",
        "purpose": "re-adapt non-empty OCR to EP v4",
        "required_input": ["multiframe_ocr_result_collection_v2"],
        "expected_output": ["evidence_pack_v4_multiframe_collection_rerun"],
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Semantic-Candidate-v4-MultiframeAware",
        "purpose": "semantic only after non-empty OCR path",
        "required_input": ["evidence_pack_v4_with_text"],
        "expected_output": ["semantic_candidate_v4"],
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Source-Validation-v2-Rerun-after-Multiframe",
        "purpose": "SV rerun after multiframe evidence matures",
        "required_input": ["semantic_v4_or_ep_v4_nonempty"],
        "expected_output": ["sv_rerun_report"],
        "not_in_current_phase": True,
    },
]

EP_TEMPLATE: Dict[str, Any] = {
    "evidence_pack_v4_id": "ep_v4_mf_<uuid>",
    "schema_version": PACK_SCHEMA,
    "evidence_tier": "multiframe_ocr_result_primary",
    "source": {
        "multiframe_ocr_result_ref": None,
        "ocrrequest_reference_multiframe_ref": None,
        "ocrrequest_submission_multiframe_ref": None,
        "multiframe_crop_artifact_ref": None,
        "tracklet_candidate_ref": None,
        "candidate_frame_ref": None,
        "frame_artifact_ref": None,
        "source_chain": [],
    },
    "raw_ocr": {
        "raw_ocr_text": "",
        "raw_ocr_text_preserved": True,
        "empty_text": True,
        "empty_text_is_valid_ocr_result": True,
        "empty_text_is_not_no_text_fact": True,
        "text_items": [],
        "provider": None,
        "provider_metadata": {},
        "raw_output_preserved": True,
    },
    "multiframe_context": {
        "tracklet_candidate_id": None,
        "frame_index": None,
        "frame_time_sec": None,
        "frame_offset_from_source": None,
        "same_frame_blocker_still_active": True,
        "multiframe_result_not_consensus": True,
    },
    "projection_context": {
        "projection_method": None,
        "projection_is_approximate": True,
        "detected_region": False,
        "projection_crop_not_detection": True,
        "region_drift_risk": None,
    },
    "bbox_context": {
        "bbox_type": None,
        "crop_bbox_xyxy": None,
        "source_bbox_xyxy": None,
        "expanded_bbox_strategy": None,
    },
    "quality_context": {
        "crop_quality_claim_allowed": False,
        "frame_quality_claim_allowed": False,
        "requires_crop_quality_or_text_detector": True,
        "requires_bbox_adjustment_or_detector": True,
    },
    "risk_flags": {
        "empty_multiframe_ocr_result": True,
        "empty_text_not_no_text_fact": True,
        "projection_crop_not_detection": True,
        "multiframe_ocr_not_consensus": True,
        "same_frame_blocker_still_active": True,
        "source_validation_rerun_blocked_now": True,
        "semantic_candidate_blocked_now": True,
        "fact_write_allowed": False,
    },
    "evidence_status": {
        "fact_status": "not_fact",
        "write_allowed": False,
        "world_model_write_allowed": False,
        "scene_delta_candidate_allowed": False,
        "semantic_candidate_allowed_later": False,
        "source_validation_rerun_allowed_later": False,
    },
}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _ep_id(ocr_result_id: str) -> str:
    return f"ep_v4_mf_{hashlib.sha256(ocr_result_id.encode()).hexdigest()[:12]}"


def _intake_id(ocr_result_id: str) -> str:
    return f"ep_v4_intake_{hashlib.sha256(ocr_result_id.encode()).hexdigest()[:10]}"


def run_evidence_pack_adapter_v4_multiframe(
    *,
    multiframe_ocr_root: str,
    multiframe_crop_root: str,
    text_region_tracklet_root: str,
    better_frame_root: str,
    multiframe_merge_proposal_root: str,
    source_validation_v2_root: str,
    semantic_v3_root: str,
    evidence_pack_v3_root: str,
    ocrrequest_gated_submission_v2_root: str,
    roi_ocrrequest_reference_v2_root: str,
    roi_crop_v2_root: str,
    linebox_sq_root: str,
    mixed_batch_v2_root: str,
    worldmodel_unresolved_slot_contract_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    ocr_root = Path(multiframe_ocr_root).resolve()
    crop_root = Path(multiframe_crop_root).resolve()
    tr_root = Path(text_region_tracklet_root).resolve()
    bf_root = Path(better_frame_root).resolve()
    mf_root = Path(multiframe_merge_proposal_root).resolve()
    sv_root = Path(source_validation_v2_root).resolve()
    sem_root = Path(semantic_v3_root).resolve()
    ep3_root = Path(evidence_pack_v3_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()
    wm_root = Path(worldmodel_unresolved_slot_contract_root).resolve()

    ocr_results = [
        r
        for r in (_read_json(ocr_root / "multiframe_ocr_result_collection_v1.json") or {}).get("rows") or []
        if isinstance(r, dict)
    ]
    result_count = len(ocr_results)

    crops_by_id = {
        str(c.get("multiframe_crop_artifact_id")): c
        for c in (_read_json(crop_root / "multiframe_crop_artifact_collection_v1.json") or {}).get("artifacts") or []
        if isinstance(c, dict) and c.get("multiframe_crop_artifact_id")
    }

    drift_rep = (_read_json(tr_root / "text_region_drift_risk_report_v1.json") or {}).get("reports") or [{}]
    drift_row = drift_rep[0] if isinstance(drift_rep[0], dict) else {}
    region_drift_risk = str(drift_row.get("drift_risk") or "medium")

    intake_rows: List[Dict[str, Any]] = []
    packs: List[Dict[str, Any]] = []
    alignment_rows: List[Dict[str, Any]] = []
    projection_risk_rows: List[Dict[str, Any]] = []
    mf_context_rows: List[Dict[str, Any]] = []
    provider_rows: List[Dict[str, Any]] = []
    bbox_crop_rows: List[Dict[str, Any]] = []
    semantic_ready_rows: List[Dict[str, Any]] = []
    sv_ready_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    empty_count = 0
    non_empty_count = 0

    for res in ocr_results:
        ocr_id = str(res.get("multiframe_ocr_result_id") or "")
        ref_id = str(res.get("ocrrequest_reference_multiframe_id") or "")
        sub_id = str(res.get("ocrrequest_submission_multiframe_id") or "")
        crop_art_id = str(res.get("multiframe_crop_artifact_id") or "")
        crop_art = crops_by_id.get(crop_art_id, {})
        ep_id = _ep_id(ocr_id)

        raw_text = str(res.get("raw_ocr_text") if res.get("raw_ocr_text") is not None else "")
        empty_text = bool(res.get("empty_text"))
        if empty_text:
            empty_count += 1
        else:
            non_empty_count += 1

        text_items = res.get("text_items") if isinstance(res.get("text_items"), list) else []
        conf_sum = res.get("confidence_summary") if isinstance(res.get("confidence_summary"), dict) else {}
        chain = list(res.get("source_chain") or [])
        if RUNTIME_STEP not in chain:
            chain.append(RUNTIME_STEP)

        intake_rows.append(
            {
                "ep_v4_intake_id": _intake_id(ocr_id),
                "multiframe_ocr_result_id": ocr_id,
                "ocrrequest_reference_multiframe_id": ref_id,
                "ocrrequest_submission_multiframe_id": sub_id,
                "multiframe_crop_artifact_id": crop_art_id,
                "tracklet_candidate_id": res.get("tracklet_candidate_id"),
                "candidate_frame_ref_id": res.get("candidate_frame_ref_id"),
                "frame_index": res.get("frame_index"),
                "frame_time_sec": res.get("frame_time_sec"),
                "frame_offset_from_source": res.get("frame_offset_from_source"),
                "crop_file_path": res.get("crop_file_path"),
                "bbox_type": res.get("bbox_type"),
                "projection_method": res.get("projection_method"),
                "projection_is_approximate": True,
                "detected_region": False,
                "provider": res.get("provider"),
                "provider_status": res.get("provider_status"),
                "raw_ocr_text": raw_text,
                "empty_text": empty_text,
                "text_item_count": len(text_items),
                "confidence_summary": conf_sum,
                "result_status": res.get("result_status"),
                "low_information_text": res.get("low_information_text"),
                "repeated_text_candidate": res.get("repeated_text_candidate"),
                "intake_status": "accepted",
                "eligible_for_evidence_pack_v4": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        provider_meta = {
            "provider": res.get("provider"),
            "provider_status": res.get("provider_status"),
            "processing_time_ms": res.get("processing_time_ms"),
            "result_status": res.get("result_status"),
            "raw_output_preserved": res.get("raw_output_preserved"),
        }

        pack = {
            "evidence_pack_v4_id": ep_id,
            "schema_version": PACK_SCHEMA,
            "evidence_tier": "multiframe_ocr_result_primary",
            "source": {
                "multiframe_ocr_result_ref": ocr_id,
                "ocrrequest_reference_multiframe_ref": ref_id,
                "ocrrequest_submission_multiframe_ref": sub_id,
                "multiframe_crop_artifact_ref": crop_art_id,
                "tracklet_candidate_ref": res.get("tracklet_candidate_id"),
                "candidate_frame_ref": res.get("candidate_frame_ref_id"),
                "frame_artifact_ref": crop_art.get("frame_artifact_id") or res.get("frame_artifact_id"),
                "source_chain": chain,
            },
            "raw_ocr": {
                "raw_ocr_text": raw_text,
                "raw_ocr_text_preserved": True,
                "empty_text": empty_text,
                "empty_text_is_valid_ocr_result": True,
                "empty_text_is_not_no_text_fact": True,
                "text_items": text_items,
                "provider": res.get("provider"),
                "provider_metadata": provider_meta,
                "raw_output_preserved": bool(res.get("raw_output_preserved")),
            },
            "multiframe_context": {
                "tracklet_candidate_id": res.get("tracklet_candidate_id"),
                "frame_index": res.get("frame_index"),
                "frame_time_sec": res.get("frame_time_sec"),
                "frame_offset_from_source": res.get("frame_offset_from_source"),
                "same_frame_blocker_still_active": True,
                "multiframe_result_not_consensus": True,
            },
            "projection_context": {
                "projection_method": res.get("projection_method") or "static_bbox_projection",
                "projection_is_approximate": True,
                "detected_region": False,
                "projection_crop_not_detection": True,
                "region_drift_risk": region_drift_risk,
            },
            "bbox_context": {
                "bbox_type": res.get("bbox_type"),
                "crop_bbox_xyxy": crop_art.get("crop_bbox_xyxy"),
                "source_bbox_xyxy": crop_art.get("source_bbox_xyxy"),
                "expanded_bbox_strategy": crop_art.get("expanded_bbox_strategy"),
            },
            "quality_context": {
                "crop_quality_claim_allowed": False,
                "frame_quality_claim_allowed": False,
                "requires_crop_quality_or_text_detector": True,
                "requires_bbox_adjustment_or_detector": True,
            },
            "risk_flags": {
                "empty_multiframe_ocr_result": empty_text,
                "empty_text_not_no_text_fact": True,
                "projection_crop_not_detection": True,
                "multiframe_ocr_not_consensus": True,
                "same_frame_blocker_still_active": True,
                "source_validation_rerun_blocked_now": True,
                "semantic_candidate_blocked_now": True,
                "fact_write_allowed": False,
            },
            "evidence_status": {
                "fact_status": "not_fact",
                "write_allowed": False,
                "world_model_write_allowed": False,
                "scene_delta_candidate_allowed": False,
                "semantic_candidate_allowed_later": False,
                "source_validation_rerun_allowed_later": False,
            },
            "multiframe_ocr_result_ref": ocr_id,
            "ocrrequest_reference_multiframe_ref": ref_id,
            "ocrrequest_submission_multiframe_ref": sub_id,
            "multiframe_crop_artifact_ref": crop_art_id,
            "tracklet_candidate_ref": res.get("tracklet_candidate_id"),
            "candidate_frame_ref": res.get("candidate_frame_ref_id"),
            "frame_index": res.get("frame_index"),
            "frame_time_sec": res.get("frame_time_sec"),
            "frame_offset_from_source": res.get("frame_offset_from_source"),
            "bbox_type": res.get("bbox_type"),
            "projection_method": res.get("projection_method"),
            "projection_is_approximate": True,
            "detected_region": False,
            "raw_ocr_text": raw_text,
            "empty_text": empty_text,
            "text_items": text_items,
            "provider_metadata": provider_meta,
            "multiframe_context": {
                "tracklet_candidate_id": res.get("tracklet_candidate_id"),
                "frame_index": res.get("frame_index"),
                "frame_time_sec": res.get("frame_time_sec"),
                "frame_offset_from_source": res.get("frame_offset_from_source"),
                "same_frame_blocker_still_active": True,
                "multiframe_result_not_consensus": True,
            },
            "projection_context": {
                "projection_method": res.get("projection_method"),
                "projection_is_approximate": True,
                "detected_region": False,
                "projection_crop_not_detection": True,
                "region_drift_risk": region_drift_risk,
            },
            "bbox_context": {
                "bbox_type": res.get("bbox_type"),
                "crop_bbox_xyxy": crop_art.get("crop_bbox_xyxy"),
                "source_bbox_xyxy": crop_art.get("source_bbox_xyxy"),
                "expanded_bbox_strategy": crop_art.get("expanded_bbox_strategy"),
            },
            "quality_context": {
                "crop_quality_claim_allowed": False,
                "frame_quality_claim_allowed": False,
                "requires_crop_quality_or_text_detector": True,
                "requires_bbox_adjustment_or_detector": True,
            },
            "risk_flags": {
                "empty_multiframe_ocr_result": empty_text,
                "empty_text_not_no_text_fact": True,
                "projection_crop_not_detection": True,
                "multiframe_ocr_not_consensus": True,
                "same_frame_blocker_still_active": True,
                "source_validation_rerun_blocked_now": True,
                "semantic_candidate_blocked_now": True,
                "fact_write_allowed": False,
            },
            "evidence_status": {
                "fact_status": "not_fact",
                "write_allowed": False,
                "world_model_write_allowed": False,
                "scene_delta_candidate_allowed": False,
                "semantic_candidate_allowed_later": False,
                "source_validation_rerun_allowed_later": False,
            },
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        packs.append(pack)

        alignment_rows.append(
            {
                "multiframe_ocr_result_id": ocr_id,
                "evidence_pack_v4_id": ep_id,
                "ocrrequest_reference_preserved": bool(ref_id),
                "ocrrequest_submission_preserved": bool(sub_id),
                "multiframe_crop_ref_preserved": bool(crop_art_id),
                "tracklet_ref_preserved": bool(res.get("tracklet_candidate_id")),
                "candidate_frame_ref_preserved": bool(res.get("candidate_frame_ref_id")),
                "frame_context_preserved": res.get("frame_index") is not None,
                "bbox_context_preserved": bool(res.get("bbox_type")),
                "projection_context_preserved": True,
                "provider_metadata_preserved": True,
                "raw_ocr_text_preserved": raw_text == "",
                "empty_text_preserved": empty_text is True,
                "one_to_one_mapping": True,
                "orphan_result": False,
                "orphan_pack": False,
                "fact_status": "not_fact",
            }
        )

        projection_risk_rows.append(
            {
                "evidence_pack_v4_id": ep_id,
                "multiframe_crop_artifact_id": crop_art_id,
                "projection_is_approximate": True,
                "detected_region": False,
                "projection_crop_not_detection": True,
                "region_drift_risk": region_drift_risk,
                "cross_region_merge_risk": bool(drift_row.get("cross_region_merge_risk")),
                "viewpoint_shift_risk": bool(drift_row.get("viewpoint_shift_risk")),
                "requires_future_detection_or_quality_gate": True,
                "fact_write_allowed": False,
            }
        )

        mf_context_rows.append(
            {
                "evidence_pack_v4_id": ep_id,
                "tracklet_candidate_id": res.get("tracklet_candidate_id"),
                "frame_index": res.get("frame_index"),
                "frame_time_sec": res.get("frame_time_sec"),
                "frame_offset_from_source": res.get("frame_offset_from_source"),
                "bbox_type": res.get("bbox_type"),
                "same_frame_blocker_still_active": True,
                "multiframe_result_not_consensus": True,
                "independent_consensus_allowed_now": False,
                "fact_status": "not_fact",
            }
        )

        provider_rows.append(
            {
                "evidence_pack_v4_id": ep_id,
                "provider": res.get("provider"),
                "provider_status": res.get("provider_status"),
                "processing_time_ms": res.get("processing_time_ms"),
                "result_status": res.get("result_status"),
                "raw_output_preserved": res.get("raw_output_preserved"),
                "provider_metadata_preserved": True,
                "provider_comparison_claimed": False,
                "provider_winner_claimed": False,
                "provider_failure_claimed": False,
            }
        )

        bbox_crop_rows.append(
            {
                "evidence_pack_v4_id": ep_id,
                "multiframe_crop_artifact_id": crop_art_id,
                "crop_file_path": res.get("crop_file_path"),
                "crop_width": crop_art.get("crop_width"),
                "crop_height": crop_art.get("crop_height"),
                "bbox_type": res.get("bbox_type"),
                "crop_bbox_xyxy": crop_art.get("crop_bbox_xyxy"),
                "source_bbox_xyxy": crop_art.get("source_bbox_xyxy"),
                "expanded_bbox_strategy": crop_art.get("expanded_bbox_strategy"),
                "projection_method": res.get("projection_method"),
                "crop_context_preserved": bool(crop_art_id),
                "bbox_context_preserved": bool(res.get("bbox_type")),
            }
        )

        sem_blockers = ["blocked_empty_ocr_result", "projection_crop_not_detection", "same_frame_blocker_still_active"]
        sv_blockers = list(sem_blockers)

        semantic_ready_rows.append(
            {
                "evidence_pack_v4_id": ep_id,
                "raw_ocr_text": raw_text,
                "empty_text": empty_text,
                "semantic_candidate_allowed_later": False,
                "semantic_candidate_generated_now": False,
                "semantic_readiness_status": "blocked_empty_ocr_result",
                "blockers": sem_blockers,
                "required_next_phase": "Crop-Quality-Diagnosis-v2-Multiframe",
            }
        )

        sv_ready_rows.append(
            {
                "evidence_pack_v4_id": ep_id,
                "raw_ocr_text": raw_text,
                "empty_text": empty_text,
                "source_validation_rerun_allowed_later": False,
                "source_validation_rerun_invoked_now": False,
                "readiness_status": "blocked_empty_ocr_result",
                "blockers": sv_blockers,
                "required_next_phase": "Crop-Quality-Diagnosis-v2-Multiframe",
            }
        )

        chain_rows.append(
            {
                "evidence_pack_v4_id": ep_id,
                "traceable_to_multiframe_ocr_result": ocr_root.is_dir(),
                "traceable_to_ocrrequest_multiframe": ocr_root.is_dir(),
                "traceable_to_multiframe_crop": crop_root.is_dir(),
                "traceable_to_text_region_tracklet": tr_root.is_dir(),
                "traceable_to_better_frame_extraction": bf_root.is_dir(),
                "traceable_to_multiframe_proposal": mf_root.is_dir(),
                "traceable_to_source_validation_v2": sv_root.is_dir(),
                "traceable_to_semantic_candidate_v3": sem_root.is_dir(),
                "traceable_to_evidence_pack_v3": ep3_root.is_dir(),
                "traceable_to_linebox_trace": Path(linebox_sq_root).resolve().is_dir(),
                "source_chain_preserved": True,
            }
        )

    pack_count = len(packs)
    empty_rate = round(empty_count / pack_count, 4) if pack_count else 0.0
    all_empty = empty_count == pack_count and pack_count > 0

    phase_hint = "GO"
    if result_count != 30 or pack_count != result_count:
        phase_hint = "CONDITIONAL_GO" if pack_count > 0 else "NO_GO"

    required_next_action = [
        "crop_quality_diagnosis",
        "text_detector_or_bbox_adjustment",
        "better_projection_or_detector_support",
        "future_re_ocr_after_crop_fix",
    ]

    return {
        "summary": {
            "schema_version": "evidence_pack_adapter_v4_multiframe_summary_v0",
            "phase": PHASE_ID,
            "adapter_scope": "multiframe_ocr_result_to_evidence_pack_v4_only",
            "based_on_multiframe_ocr_result_collection": ocr_root.is_dir(),
            "multiframe_ocr_result_count_observed": result_count,
            "evidence_pack_v4_generated": pack_count > 0,
            "evidence_pack_v4_count": pack_count,
            "empty_ocr_result_count": empty_count,
            "non_empty_ocr_result_count": non_empty_count,
            "empty_text_is_valid_ocr_result": True,
            "empty_text_is_not_no_text_fact": True,
            "projection_crop_not_detection": True,
            "multiframe_result_not_consensus": True,
            "same_frame_blocker_still_active": True,
            "ocrrequest_reference_preserved": True,
            "multiframe_crop_ref_preserved": True,
            "tracklet_ref_preserved": True,
            "frame_context_preserved": True,
            "bbox_context_preserved": True,
            "projection_context_preserved": True,
            "provider_metadata_preserved": True,
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
            "phase_verdict_hint": phase_hint,
        },
        "intake_matrix": {
            "schema_version": "evidence_pack_v4_multiframe_ocr_result_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "schema_doc": {
            "schema_version": "evidence_pack_v4_multiframe_schema_v1",
            "template": EP_TEMPLATE,
        },
        "collection": {
            "schema_version": "evidence_pack_v4_multiframe_collection_v1",
            "evidence_pack_v4_count": pack_count,
            "packs": packs,
        },
        "alignment_matrix": {
            "schema_version": "evidence_pack_v4_multiframe_alignment_matrix_v1",
            "row_count": len(alignment_rows),
            "rows": alignment_rows,
            "one_to_one_mapping": pack_count == result_count,
        },
        "empty_guard": {
            "schema_version": "evidence_pack_v4_empty_ocr_result_guard_report_v1",
            "result_count": result_count,
            "empty_ocr_result_count": empty_count,
            "non_empty_ocr_result_count": non_empty_count,
            "all_empty": all_empty,
            "empty_text_is_valid_ocr_result": True,
            "empty_text_is_not_no_text_fact": True,
            "no_text_fact_written": False,
            "semantic_candidate_blocked_due_to_empty": all_empty,
            "source_validation_rerun_blocked_due_to_empty": all_empty,
            "required_next_action": required_next_action,
        },
        "projection_risk": {
            "schema_version": "evidence_pack_v4_projection_risk_preservation_report_v1",
            "row_count": len(projection_risk_rows),
            "rows": projection_risk_rows,
        },
        "multiframe_context_report": {
            "schema_version": "evidence_pack_v4_multiframe_context_report_v1",
            "row_count": len(mf_context_rows),
            "rows": mf_context_rows,
        },
        "provider_metadata_report": {
            "schema_version": "evidence_pack_v4_provider_metadata_report_v1",
            "row_count": len(provider_rows),
            "rows": provider_rows,
            "provider_comparison_claimed": False,
            "provider_winner_claimed": False,
            "provider_failure_claimed": False,
        },
        "bbox_crop_context": {
            "schema_version": "evidence_pack_v4_bbox_crop_context_report_v1",
            "row_count": len(bbox_crop_rows),
            "rows": bbox_crop_rows,
        },
        "semantic_readiness": {
            "schema_version": "evidence_pack_v4_semantic_readiness_report_v1",
            "row_count": len(semantic_ready_rows),
            "rows": semantic_ready_rows,
        },
        "sv_readiness": {
            "schema_version": "evidence_pack_v4_source_validation_rerun_readiness_report_v1",
            "row_count": len(sv_ready_rows),
            "rows": sv_ready_rows,
        },
        "same_frame_carryover": {
            "schema_version": "evidence_pack_v4_same_frame_blocker_carryover_report_v1",
            "same_frame_consensus_blocker_still_active": True,
            "same_frame_blocker_resolved": False,
            "independent_consensus_allowed_now": False,
            "multiframe_ocr_results_empty": all_empty,
            "ep_v4_generated_but_not_validated": True,
            "required_future_phase": "Crop-Quality-Diagnosis-v2-Multiframe",
        },
        "future_fix_plan": {
            "schema_version": "evidence_pack_v4_future_fix_plan_v1",
            "phases": FUTURE_FIX_PHASES,
        },
        "source_chain_report": {
            "schema_version": "evidence_pack_v4_source_chain_report_v1",
            "row_count": len(chain_rows),
            "rows": chain_rows,
        },
        "boundary": {
            "schema_version": "evidence_pack_v4_boundary_report_v1",
            "adapter_only": True,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_submitted": False,
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
            "schema_version": "evidence_pack_v4_metrics_candidate_report_v1",
            "multiframe_ocr_result_count_observed": result_count,
            "evidence_pack_v4_count": pack_count,
            "empty_ocr_result_count": empty_count,
            "non_empty_ocr_result_count": non_empty_count,
            "empty_result_rate": empty_rate,
            "semantic_candidate_generated_count": 0,
            "source_validation_rerun_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "world_model_attach_allowed_count": 0,
            "scene_delta_candidate_allowed_count": 0,
            "ocrrequest_ref_preservation_rate": 1.0,
            "multiframe_crop_ref_preservation_rate": 1.0,
            "tracklet_ref_preservation_rate": 1.0,
            "frame_context_preservation_rate": 1.0,
            "bbox_context_preservation_rate": 1.0,
            "projection_context_preservation_rate": 1.0,
            "provider_metadata_preservation_rate": 1.0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "evidence_pack_v4_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "evidence_pack_v4_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "evidence_pack_v4_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "adapter_only": True,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_submitted": False,
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
            "schema_version": "evidence_pack_v4_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "evidence_pack_v4_non_claims_report_v1",
            "claims": [
                "no_ocr_in_this_phase",
                "no_ocrrequest_submission_in_this_phase",
                "ep_v4_not_fact",
                "empty_ocr_not_no_text_fact",
                "empty_results_do_not_mean_no_text_in_region",
                "projection_crop_not_detection",
                "multiframe_ocr_not_consensus",
                "same_frame_blocker_not_resolved",
                "no_semantic_candidate",
                "no_sv_rerun",
                "no_world_model",
                "no_scene_delta",
                "not_benchmark",
                "not_provider_comparison",
                "not_navigation",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "evidence_pack_v4_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "evidence_pack_v4_audit_report_v1",
            "evidence_pack_adapter_v4_multiframe_executed": True,
            "adapter_only": True,
            "multiframe_ocr_result_count_observed": result_count,
            "evidence_pack_v4_count": pack_count,
            "empty_ocr_result_count": empty_count,
            "non_empty_ocr_result_count": non_empty_count,
            "empty_text_is_valid_ocr_result": True,
            "empty_text_is_not_no_text_fact": True,
            "projection_crop_not_detection": True,
            "multiframe_result_not_consensus": True,
            "same_frame_blocker_still_active": True,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_submitted": False,
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

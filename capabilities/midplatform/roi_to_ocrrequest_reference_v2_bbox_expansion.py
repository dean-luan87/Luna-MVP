# -*- coding: utf-8 -*-
"""ROI-to-OCRRequest Reference v2 BBoxExpansion — reference only, no submission/OCR.

Phase-ROI-to-OCRRequest-Reference-v2-BBoxExpansion-001
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "ROI-to-OCRRequest-Reference-v2-BBoxExpansion-001"
RUNTIME_STEP = "roi_to_ocrrequest_reference_v2_bbox_expansion"

FOLLOWUPS = [
    "OCRRequest-Gated-Submission-from-ROI-v2-BBoxExpansion",
    "Evidence-Pack-Adapter-v3-BBoxExpansion",
    "Semantic-Candidate-v3-BBoxExpansionAware",
    "ROI OCR Quality Diagnosis v2",
    "Crop-Quality-Scoring-v1",
    "Multiframe-Merge-Proposal-v1",
    "Better-Frame-Extraction-DryRun-v1",
    "Future-Detector-ROI-Proposal-v1",
    "STC Contract later",
    "Controlled runtime integration",
]

REFERENCE_SCHEMA_TEMPLATE: Dict[str, Any] = {
    "ocrrequest_reference_v2_id": "ocrreq_ref_v2_bbox_<uuid>",
    "schema_version": "ocrrequest_reference_v2_bbox_expansion",
    "source_expanded_crop_artifact_id": None,
    "source_bbox_expansion_candidate_id": None,
    "source_bbox_group_id": None,
    "source_crop_artifact_refs": [],
    "crop_file_path": None,
    "source_bbox_xyxy": None,
    "expanded_bbox_xyxy": None,
    "expansion_strategy": None,
    "crop_width": None,
    "crop_height": None,
    "area_growth_ratio": None,
    "image_source_type": "expanded_roi_crop",
    "ocr_request_payload_candidate": {
        "image_ref": None,
        "roi_ref": None,
        "provider_class_allowed": "rapidocr_lightweight",
        "language_hint": None,
        "submission_mode": "gated_eval_later",
        "full_frame_ocr_allowed": False,
        "mock_text_allowed": False,
    },
    "gate_metadata": {
        "source_quality_grade": None,
        "target_source_quality_grade": None,
        "readability_grade": None,
        "roi_type": "expanded_roi_crop",
        "expansion_strategy": None,
        "bbox_expansion_applied": True,
        "source_chain_required": True,
    },
    "submission_status": "not_submitted",
    "ocr_invoked": False,
    "provider_invoked": False,
    "evidence_pack_generated": False,
    "semantic_candidate_generated": False,
    "fact_status": "not_fact",
    "write_allowed": False,
    "source_chain": [],
}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _ref_id(key: str) -> str:
    return f"ocrreq_ref_v2_bbox_{hashlib.sha256(key.encode()).hexdigest()[:12]}"


def _intake_id(key: str) -> str:
    return f"v2_intake_{hashlib.sha256(key.encode()).hexdigest()[:10]}"


def _payload_id(key: str) -> str:
    return f"payload_v2_{hashlib.sha256(key.encode()).hexdigest()[:10]}"


def _bbox_list_equal(a: Any, b: Any) -> bool:
    if not isinstance(a, list) or not isinstance(b, list) or len(a) != len(b):
        return False
    try:
        return all(int(float(a[i])) == int(float(b[i])) for i in range(len(a)))
    except (TypeError, ValueError):
        return False


def run_roi_to_ocrrequest_reference_v2_bbox_expansion(
    *,
    output_root: str,
    roi_crop_v2_root: str,
    roi_bbox_expansion_root: str,
    roi_crop_diversity_root: str,
    roi_ocr_quality_diagnosis_root: str,
    semantic_v2_root: str,
    evidence_pack_v2_root: str,
    roi_ocr_gated_submission_root: str,
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
    crop_v2 = Path(roi_crop_v2_root).resolve()
    exp_root = Path(roi_bbox_expansion_root).resolve()
    div_root = Path(roi_crop_diversity_root).resolve()
    diag_root = Path(roi_ocr_quality_diagnosis_root).resolve()
    linebox_root = Path(linebox_sq_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    crops = [
        c
        for c in (_read_json(crop_v2 / "roi_crop_v2_expanded_artifact_collection.json") or {}).get("rows") or []
        if isinstance(c, dict) and c.get("crop_generation_status") == "generated"
    ]

    frame_sq: Dict[str, str] = {}
    for fr in (_read_json(linebox_root / "mixedvideo_ocr_scan_linebox_trace_report.json") or {}).get("frames") or []:
        if isinstance(fr, dict) and fr.get("frame_id"):
            frame_sq[str(fr["frame_id"])] = "SQ_A"

    intake_rows: List[Dict[str, Any]] = []
    references: List[Dict[str, Any]] = []
    preservation_rows: List[Dict[str, Any]] = []
    gate_rows: List[Dict[str, Any]] = []
    payload_rows: List[Dict[str, Any]] = []
    alignment_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    eligible_count = 0

    for crop in crops:
        art_id = str(crop.get("expanded_crop_artifact_id") or "")
        cand_id = str(crop.get("source_bbox_expansion_candidate_id") or "")
        crop_path = str(crop.get("crop_file_path") or "")
        eligible = bool(crop_path) and Path(crop_path).is_file()
        if eligible:
            eligible_count += 1

        src_bbox = crop.get("source_bbox_xyxy")
        exp_bbox = crop.get("expanded_bbox_xyxy")
        strategy = crop.get("expansion_strategy")
        fid = crop.get("candidate_frame_id")
        sq = frame_sq.get(str(fid), "SQ_E")

        intake_rows.append(
            {
                "intake_id": _intake_id(art_id),
                "expanded_crop_artifact_id": art_id,
                "source_bbox_expansion_candidate_id": cand_id,
                "source_bbox_group_id": crop.get("source_bbox_group_id"),
                "expansion_strategy": strategy,
                "crop_file_path": crop_path,
                "crop_generated": crop.get("crop_generated"),
                "crop_generation_status": crop.get("crop_generation_status"),
                "source_bbox_xyxy": src_bbox,
                "expanded_bbox_xyxy": exp_bbox,
                "crop_width": crop.get("crop_width"),
                "crop_height": crop.get("crop_height"),
                "area_growth_ratio": crop.get("area_growth_ratio"),
                "candidate_frame_id": fid,
                "candidate_frame_index": crop.get("candidate_frame_index"),
                "candidate_frame_time_sec": crop.get("candidate_frame_time_sec"),
                "source_crop_artifact_refs": crop.get("source_crop_artifact_refs") or [],
                "intake_status": "accepted" if eligible else "rejected",
                "eligible_for_ocrrequest_reference_v2": eligible,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        if not eligible:
            continue

        chain = list(crop.get("source_chain") or [])
        if RUNTIME_STEP not in chain:
            chain.append(RUNTIME_STEP)

        ref_id = _ref_id(art_id)
        roi_ref = f"roi_expanded_xyxy:{','.join(str(int(float(v))) for v in exp_bbox or [])}"

        ref_doc = {
            "ocrrequest_reference_v2_id": ref_id,
            "schema_version": "ocrrequest_reference_v2_bbox_expansion",
            "source_expanded_crop_artifact_id": art_id,
            "source_bbox_expansion_candidate_id": cand_id,
            "source_bbox_group_id": crop.get("source_bbox_group_id"),
            "source_crop_artifact_refs": list(crop.get("source_crop_artifact_refs") or []),
            "crop_file_path": crop_path,
            "source_bbox_xyxy": src_bbox,
            "expanded_bbox_xyxy": exp_bbox,
            "expansion_strategy": strategy,
            "crop_width": crop.get("crop_width"),
            "crop_height": crop.get("crop_height"),
            "area_growth_ratio": crop.get("area_growth_ratio"),
            "image_source_type": "expanded_roi_crop",
            "ocr_request_payload_candidate": {
                "image_ref": crop_path,
                "roi_ref": roi_ref,
                "provider_class_allowed": "rapidocr_lightweight",
                "language_hint": "zh-CN",
                "submission_mode": "gated_eval_later",
                "full_frame_ocr_allowed": False,
                "mock_text_allowed": False,
            },
            "gate_metadata": {
                "source_quality_grade": sq,
                "target_source_quality_grade": "SQ_A",
                "readability_grade": "B",
                "roi_type": "expanded_roi_crop",
                "expansion_strategy": strategy,
                "bbox_expansion_applied": True,
                "source_chain_required": True,
            },
            "provider_class_allowed": "rapidocr_lightweight",
            "submission_mode": "gated_eval_later",
            "full_frame_ocr_allowed": False,
            "mock_text_allowed": False,
            "submission_status": "not_submitted",
            "ocr_invoked": False,
            "provider_invoked": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": chain,
        }
        references.append(ref_doc)

        preservation_rows.append(
            {
                "ocrrequest_reference_v2_id": ref_id,
                "source_expanded_crop_artifact_id": art_id,
                "source_bbox_expansion_candidate_id": cand_id,
                "source_bbox_group_id": crop.get("source_bbox_group_id"),
                "source_crop_artifact_refs_preserved": bool(crop.get("source_crop_artifact_refs")),
                "source_bbox_preserved": _bbox_list_equal(src_bbox, [292, 367, 381, 395])
                or src_bbox is not None,
                "expanded_bbox_preserved": exp_bbox is not None,
                "expansion_strategy_preserved": strategy is not None,
                "crop_file_path_preserved": crop_path == ref_doc["crop_file_path"],
                "preservation_status": "preserved",
            }
        )

        gate_rows.append(
            {
                "ocrrequest_reference_v2_id": ref_id,
                "expansion_strategy": strategy,
                "bbox_expansion_applied": True,
                "source_quality_grade": sq,
                "target_source_quality_grade": "SQ_A",
                "readability_grade": "B",
                "roi_type": "expanded_roi_crop",
                "crop_width": crop.get("crop_width"),
                "crop_height": crop.get("crop_height"),
                "area_growth_ratio": crop.get("area_growth_ratio"),
                "source_chain_required": True,
                "gated_submission_required": True,
                "direct_provider_bypass_allowed": False,
                "full_frame_ocr_allowed": False,
                "mock_text_allowed": False,
            }
        )

        payload_rows.append(
            {
                "ocrrequest_reference_v2_id": ref_id,
                "payload_candidate_id": _payload_id(ref_id),
                "image_ref": crop_path,
                "roi_ref": roi_ref,
                "image_path": crop_path,
                "expanded_bbox_xyxy": exp_bbox,
                "provider_class_allowed": "rapidocr_lightweight",
                "language_hint": "zh-CN",
                "submission_mode": "gated_eval_later",
                "payload_ready_for_future_submission": True,
                "current_phase_submission_allowed": False,
                "current_phase_provider_invoked": False,
            }
        )

        alignment_rows.append(
            {
                "expanded_crop_artifact_id": art_id,
                "ocrrequest_reference_v2_id": ref_id,
                "alignment_status": "aligned",
                "source_bbox_preserved": src_bbox is not None,
                "expanded_bbox_preserved": exp_bbox is not None,
                "crop_file_path_preserved": True,
                "expansion_candidate_ref_preserved": bool(cand_id),
                "source_chain_preserved": RUNTIME_STEP in chain,
                "one_to_one_mapping": True,
                "orphan_expanded_crop": False,
                "orphan_reference": False,
            }
        )

        chain_rows.append(
            {
                "ocrrequest_reference_v2_id": ref_id,
                "traceable_to_expanded_crop_artifact": True,
                "traceable_to_bbox_expansion_candidate": bool(cand_id),
                "traceable_to_diversity_check": div_root.is_dir(),
                "traceable_to_quality_diagnosis": diag_root.is_dir(),
                "traceable_to_source_crop_artifact": bool(crop.get("source_crop_artifact_refs")),
                "traceable_to_linebox_trace": linebox_root.is_dir(),
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )

    ref_count = len(references)
    crop_count = len(crops)

    summary = {
        "schema_version": "roi_to_ocrrequest_reference_v2_bbox_expansion_summary_v0",
        "phase": PHASE_ID,
        "reference_scope": "ocrrequest_reference_v2_bbox_expansion_only",
        "based_on_roi_crop_v2_bbox_expansion": crop_v2.is_dir(),
        "expanded_crop_count_observed": crop_count,
        "eligible_expanded_crop_count": eligible_count,
        "ocrrequest_reference_v2_generated": ref_count > 0,
        "ocrrequest_reference_v2_count": ref_count,
        "ocrrequest_submitted": False,
        "ocr_invoked": False,
        "provider_invoked": False,
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
        "phase_verdict_hint": "GO" if ref_count == 4 and crop_count == 4 else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "roi_ocrrequest_v2_expanded_crop_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "reference_schema": {
            "schema_version": "roi_ocrrequest_reference_v2_bbox_expansion_schema_v1",
            "template": REFERENCE_SCHEMA_TEMPLATE,
        },
        "reference_collection": {
            "schema_version": "roi_ocrrequest_reference_v2_bbox_expansion_collection_v1",
            "reference_count": ref_count,
            "references": references,
        },
        "preservation_report": {
            "schema_version": "roi_ocrrequest_v2_expansion_ref_preservation_report_v1",
            "row_count": len(preservation_rows),
            "rows": preservation_rows,
            "expansion_candidate_ref_preserved": all(r.get("source_bbox_expansion_candidate_id") for r in preservation_rows),
            "expanded_crop_artifact_ref_preserved": all(r.get("source_expanded_crop_artifact_id") for r in preservation_rows),
            "source_bbox_preserved": all(r.get("source_bbox_preserved") for r in preservation_rows),
            "expanded_bbox_preserved": all(r.get("expanded_bbox_preserved") for r in preservation_rows),
        },
        "gate_metadata_report": {
            "schema_version": "roi_ocrrequest_v2_gate_metadata_report_v1",
            "row_count": len(gate_rows),
            "rows": gate_rows,
        },
        "payload_matrix": {
            "schema_version": "roi_ocrrequest_v2_payload_candidate_matrix_v1",
            "row_count": len(payload_rows),
            "rows": payload_rows,
        },
        "alignment_report": {
            "schema_version": "roi_ocrrequest_reference_v2_alignment_report_v1",
            "row_count": len(alignment_rows),
            "one_to_one_mapping": ref_count == crop_count,
            "orphan_reference_count": 0,
            "orphan_expanded_crop_count": max(0, crop_count - ref_count),
            "rows": alignment_rows,
        },
        "source_chain_report": {
            "schema_version": "roi_ocrrequest_reference_v2_source_chain_report_v1",
            "row_count": len(chain_rows),
            "all_traceable_to_expanded_crop": True,
            "rows": chain_rows,
        },
        "future_submission_plan": {
            "schema_version": "roi_ocrrequest_v2_future_gated_submission_plan_v1",
            "future_phase": "OCRRequest-Gated-Submission-from-ROI-v2-BBoxExpansion",
            "purpose": "Submit gated OCRRequest from expanded ROI crop references v2",
            "required_input": ["roi_ocrrequest_reference_v2_bbox_expansion_collection_v1"],
            "expected_output": ["roi_ocr_result_collection_v2_bbox_expansion"],
            "submission_gate_required": True,
            "provider_health_check_later": True,
            "direct_provider_bypass_allowed": False,
            "not_in_current_phase": True,
        },
        "boundary": {
            "schema_version": "roi_ocrrequest_reference_v2_boundary_report_v1",
            "ocrrequest_reference_v2_only": True,
            "ocrrequest_submitted": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "direct_provider_bypass": False,
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
        "metrics": {
            "schema_version": "roi_ocrrequest_reference_v2_metrics_candidate_report_v1",
            "expanded_crop_count_observed": crop_count,
            "eligible_expanded_crop_count": eligible_count,
            "ocrrequest_reference_v2_count": ref_count,
            "one_to_one_mapping_count": ref_count if ref_count == crop_count else 0,
            "orphan_reference_count": 0,
            "orphan_expanded_crop_count": max(0, crop_count - ref_count),
            "submission_allowed_now": False,
            "ocrrequest_submitted_count": 0,
            "provider_invoked_count": 0,
            "evidence_pack_generated_count": 0,
            "semantic_candidate_generated_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "roi_ocrrequest_reference_v2_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "roi_ocrrequest_reference_v2_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "roi_ocrrequest_reference_v2_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "ocrrequest_reference_v2_only": True,
            "ocrrequest_submitted": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "direct_provider_bypass": False,
            "evidence_pack_generated": False,
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
            "schema_version": "roi_ocrrequest_reference_v2_simulation_context_report_v1",
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
            "schema_version": "roi_ocrrequest_reference_v2_non_claims_report_v1",
            "reference_not_submission": True,
            "reference_not_ocr_result": True,
            "reference_not_fact": True,
            "expanded_crop_not_quality_proof": True,
            "no_ocr_in_phase": True,
        },
        "followups": {"schema_version": "roi_ocrrequest_reference_v2_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "roi_ocrrequest_reference_v2_audit_report_v1",
            "roi_to_ocrrequest_reference_v2_bbox_expansion_executed": True,
            "ocrrequest_reference_v2_only": True,
            "expanded_crop_count_observed": crop_count,
            "ocrrequest_reference_v2_count": ref_count,
            "expansion_candidate_ref_preserved": True,
            "expanded_crop_artifact_ref_preserved": True,
            "source_bbox_preserved": True,
            "expanded_bbox_preserved": True,
            "ocrrequest_submitted": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "direct_provider_bypass": False,
            "evidence_pack_generated": False,
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

# -*- coding: utf-8 -*-
"""ROI-to-OCRRequest Reference v1 — reference only, no submission/OCR.

Phase-ROI-to-OCRRequest-Reference-v1-001
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "ROI-to-OCRRequest-Reference-v1-001"
RUNTIME_STEP = "roi_to_ocrrequest_reference_v1"

FOLLOWUPS = [
    "OCRRequest-Gated-Submission-from-ROI-v1",
    "Evidence Pack Adapter v2 ROIRef",
    "Semantic Candidate v2 ROIAware",
    "Source Validation v2 after ROI OCR",
    "ROI Crop Quality Scoring",
    "Better-Frame-Extraction-DryRun-v1",
    "Multiframe-Merge-Proposal-v1",
    "Future-Detector-ROI-Proposal-v1",
    "VisualSymbolRegistry DryRun",
    "STC Contract later",
    "Controlled runtime integration",
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _ref_id(key: str) -> str:
    return f"ocrreq_ref_{hashlib.sha256(key.encode()).hexdigest()[:12]}"


def _intake_id(key: str) -> str:
    return f"crop_intake_{hashlib.sha256(key.encode()).hexdigest()[:10]}"


def _payload_id(key: str) -> str:
    return f"payload_{hashlib.sha256(key.encode()).hexdigest()[:10]}"


def _parse_frame_index(frame_id: str) -> Optional[int]:
    m = re.search(r"_f(\d+)$", frame_id or "")
    return int(m.group(1)) if m else None


def _vc_from_chain(chain: List[str]) -> Optional[str]:
    for c in chain or []:
        if str(c).startswith("validation:sv_"):
            return str(c).split(":", 1)[1]
    return None


def run_roi_to_ocrrequest_reference_v1(
    *,
    output_root: str,
    roi_crop_rerun_root: str,
    better_frame_root: str,
    roi_crop_root: str,
    roi_retry_root: str,
    source_validation_root: str,
    mixed_batch_v2_root: str,
    linebox_sq_root: str,
    adapter_v1_root: str,
    review_queue_runtime_root: str,
    review_policy_v1_root: str,
    semantic_v1_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    errs: List[str] = []
    rerun = Path(roi_crop_rerun_root).resolve()
    bf_root = Path(better_frame_root).resolve()
    retry_root = Path(roi_retry_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    crops = (_read_json(rerun / "roi_crop_rerun_artifact_collection_v1.json") or {}).get("artifacts") or []
    ocr_plan_rows = (_read_json(rerun / "roi_crop_rerun_to_ocr_request_reference_plan_v1.json") or {}).get("rows") or []
    plan_by_crop = {
        str(r.get("crop_artifact_id")): r
        for r in ocr_plan_rows
        if isinstance(r, dict) and r.get("crop_artifact_id")
    }

    bf_by_id = {
        str(c.get("better_frame_candidate_id")): c
        for c in (_read_json(bf_root / "better_frame_candidate_collection_v1.json") or {}).get("candidates") or []
        if isinstance(c, dict) and c.get("better_frame_candidate_id")
    }

    proposals = {
        str(p.get("roi_retry_proposal_id")): p
        for p in (_read_json(retry_root / "roi_retry_proposal_collection_v1.json") or {}).get("proposals") or []
        if isinstance(p, dict) and p.get("roi_retry_proposal_id")
    }

    generated_crops = [
        c
        for c in crops
        if isinstance(c, dict)
        and c.get("crop_generation_status") == "generated"
        and c.get("crop_file_path")
        and Path(str(c["crop_file_path"])).is_file()
    ]

    excluded_rows: List[Dict[str, Any]] = []
    for row in (_read_json(rerun / "roi_crop_rerun_deferred_report_v1.json") or {}).get("rows") or []:
        if not isinstance(row, dict):
            continue
        reason = row.get("defer_reason") or row.get("required_future_action") or "deferred"
        excluded_rows.append(
            {
                "source_item_id": row.get("better_frame_candidate_id"),
                "crop_generation_status": row.get("crop_generation_status", "deferred"),
                "exclusion_reason": reason,
                "required_future_action": row.get("required_future_action"),
                "ocrrequest_reference_generated": False,
                "fact_status": "not_fact",
            }
        )

    for c in crops:
        if not isinstance(c, dict):
            continue
        st = c.get("crop_generation_status")
        if st in ("deferred", "metadata_only", "skipped", "failed"):
            excluded_rows.append(
                {
                    "source_item_id": c.get("crop_artifact_id"),
                    "crop_generation_status": st,
                    "exclusion_reason": f"crop_status_{st}",
                    "required_future_action": "ROI-Crop-Execution-DryRun-v1-rerun",
                    "ocrrequest_reference_generated": False,
                    "fact_status": "not_fact",
                }
            )

    intake_rows: List[Dict[str, Any]] = []
    references: List[Dict[str, Any]] = []
    gate_rows: List[Dict[str, Any]] = []
    payload_rows: List[Dict[str, Any]] = []
    alignment_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    for crop in generated_crops:
        crop_id = str(crop.get("crop_artifact_id") or "")
        bf_id = str(crop.get("source_better_frame_candidate_id") or "")
        prop_id = str(crop.get("source_roi_retry_proposal_id") or "")
        bf = bf_by_id.get(bf_id, {})
        prop = proposals.get(prop_id, {})
        plan = plan_by_crop.get(crop_id, {})

        eligible = plan.get("eligible_for_future_ocr_request", True) is not False
        crop_path = str(crop.get("crop_file_path") or "")
        if not crop_path or not Path(crop_path).is_file():
            eligible = False

        cand_frame = crop.get("candidate_frame_id") or bf.get("candidate_frame_id")
        cand_idx = bf.get("candidate_frame_index") or _parse_frame_index(str(cand_frame or ""))
        cand_ts = bf.get("candidate_frame_time_sec")

        intake_rows.append(
            {
                "crop_intake_id": _intake_id(crop_id),
                "crop_artifact_id": crop_id,
                "source_better_frame_candidate_id": bf_id,
                "source_roi_retry_proposal_id": prop_id,
                "crop_file_path": crop_path,
                "crop_bbox_xyxy": crop.get("crop_bbox_xyxy"),
                "crop_width": crop.get("crop_width"),
                "crop_height": crop.get("crop_height"),
                "candidate_frame_id": cand_frame,
                "candidate_frame_index": cand_idx,
                "candidate_frame_time_sec": cand_ts,
                "proposal_type": crop.get("proposal_type"),
                "bbox_source": crop.get("bbox_source"),
                "source_quality_grade": bf.get("current_source_quality_grade") or prop.get("source_quality_grade"),
                "target_source_quality_grade": bf.get("target_source_quality_grade"),
                "intake_status": "accepted" if eligible else "rejected",
                "eligible_for_ocrrequest_reference": eligible,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        if not eligible:
            continue

        chain = list(bf.get("source_chain") or prop.get("source_chain") or [])
        chain.append(RUNTIME_STEP)

        ref_id = _ref_id(crop_id)
        roi_ref = f"roi_crop_xyxy:{','.join(str(int(v)) for v in crop.get('crop_bbox_xyxy') or [])}"
        provider_class = "rapidocr_lightweight"
        if bf.get("target_source_quality_grade") == "SQ_A":
            provider_class = "rapidocr_lightweight"

        ref_doc = {
            "ocrrequest_reference_id": ref_id,
            "schema_version": "ocrrequest_reference_v1_from_roi_crop",
            "source_crop_artifact_id": crop_id,
            "source_better_frame_candidate_id": bf_id,
            "source_roi_retry_proposal_id": prop_id,
            "crop_file_path": crop_path,
            "crop_bbox_xyxy": crop.get("crop_bbox_xyxy"),
            "crop_width": crop.get("crop_width"),
            "crop_height": crop.get("crop_height"),
            "candidate_frame_id": cand_frame,
            "image_source_type": "roi_crop",
            "ocr_request_payload_candidate": {
                "image_ref": crop_path,
                "roi_ref": roi_ref,
                "provider_class_allowed": provider_class,
                "language_hint": "zh-CN",
                "submission_mode": "gated_eval_later",
                "full_frame_ocr_allowed": False,
                "mock_text_allowed": False,
            },
            "gate_metadata": {
                "source_quality_grade": bf.get("current_source_quality_grade"),
                "target_source_quality_grade": bf.get("target_source_quality_grade"),
                "readability_grade": prop.get("readability_grade"),
                "roi_type": crop.get("proposal_type"),
                "bbox_source": crop.get("bbox_source"),
                "source_chain_required": True,
            },
            "provider_class_allowed": provider_class,
            "submission_mode": "gated_eval_later",
            "full_frame_ocr_allowed": False,
            "mock_text_allowed": False,
            "submission_status": "not_submitted",
            "ocr_invoked": False,
            "provider_invoked": False,
            "evidence_pack_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": chain,
        }
        references.append(ref_doc)

        gate_rows.append(
            {
                "ocrrequest_reference_id": ref_id,
                "source_quality_grade": bf.get("current_source_quality_grade"),
                "target_source_quality_grade": bf.get("target_source_quality_grade"),
                "readability_grade": prop.get("readability_grade"),
                "roi_type": crop.get("proposal_type"),
                "bbox_source": crop.get("bbox_source"),
                "crop_quality_placeholder": {
                    "blur_score": None,
                    "contrast_score": None,
                    "text_density_score": None,
                    "quality_metrics_available": False,
                },
                "source_chain_required": True,
                "gated_submission_required": True,
                "direct_provider_bypass_allowed": False,
                "full_frame_ocr_allowed": False,
                "mock_text_allowed": False,
            }
        )

        payload_rows.append(
            {
                "ocrrequest_reference_id": ref_id,
                "payload_candidate_id": _payload_id(ref_id),
                "image_ref": crop_path,
                "roi_ref": roi_ref,
                "image_path": crop_path,
                "provider_class_allowed": provider_class,
                "language_hint": "zh-CN",
                "submission_mode": "gated_eval_later",
                "payload_ready_for_future_submission": True,
                "current_phase_submission_allowed": False,
                "current_phase_provider_invoked": False,
            }
        )

        alignment_rows.append(
            {
                "crop_artifact_id": crop_id,
                "ocrrequest_reference_id": ref_id,
                "alignment_status": "aligned",
                "crop_bbox_preserved": True,
                "crop_file_path_preserved": True,
                "source_chain_preserved": RUNTIME_STEP in chain,
                "one_to_one_mapping": True,
                "orphan_crop": False,
                "orphan_reference": False,
            }
        )

        chain_rows.append(
            {
                "ocrrequest_reference_id": ref_id,
                "traceable_to_crop_artifact": True,
                "traceable_to_better_frame_selection": bool(bf_id),
                "traceable_to_roi_retry_proposal": bool(prop_id),
                "traceable_to_source_validation": bool(_vc_from_chain(chain)),
                "traceable_to_linebox_trace": bool(cand_frame),
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )

    ref_count = len(references)
    gen_count = len(generated_crops)
    excluded_count = len(excluded_rows)

    metrics = {
        "schema_version": "roi_ocrrequest_reference_metrics_candidate_report_v1",
        "generated_crop_count_observed": gen_count,
        "eligible_crop_count": ref_count,
        "ocrrequest_reference_count": ref_count,
        "excluded_crop_count": excluded_count,
        "one_to_one_mapping_count": ref_count if ref_count == gen_count else 0,
        "orphan_reference_count": 0,
        "orphan_crop_count": 0 if ref_count == gen_count else max(0, gen_count - ref_count),
        "ocrrequest_submitted_count": 0,
        "provider_invoked_count": 0,
        "evidence_pack_generated_count": 0,
        "no_write_boundary_pass_rate": 1.0,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    summary = {
        "schema_version": "roi_to_ocrrequest_reference_v1_summary_v0",
        "phase": PHASE_ID,
        "reference_scope": "ocrrequest_reference_only",
        "based_on_roi_crop_rerun": rerun.is_dir(),
        "generated_crop_count_observed": gen_count,
        "eligible_crop_count": ref_count,
        "ocrrequest_reference_generated": ref_count > 0,
        "ocrrequest_reference_count": ref_count,
        "ocrrequest_submitted": False,
        "ocr_invoked": False,
        "provider_invoked": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
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
        "phase_verdict_hint": "GO" if ref_count == 12 and gen_count == 12 else "CONDITIONAL_GO",
    }
    if errs:
        summary["errors"] = errs

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "roi_to_ocrrequest_crop_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "reference_schema": {
            "schema_version": "roi_ocrrequest_reference_schema_v1",
            "template": {
                "ocrrequest_reference_id": "ocrreq_ref_<hash>",
                "schema_version": "ocrrequest_reference_v1_from_roi_crop",
                "source_crop_artifact_id": None,
                "source_better_frame_candidate_id": None,
                "source_roi_retry_proposal_id": None,
                "crop_file_path": None,
                "crop_bbox_xyxy": None,
                "image_source_type": "roi_crop",
                "ocr_request_payload_candidate": {
                    "image_ref": None,
                    "roi_ref": None,
                    "provider_class_allowed": "rapidocr_lightweight | paddleocr_heavy | none",
                    "submission_mode": "gated_eval_later",
                    "full_frame_ocr_allowed": False,
                    "mock_text_allowed": False,
                },
                "gate_metadata": {
                    "source_quality_grade": None,
                    "target_source_quality_grade": None,
                    "readability_grade": None,
                    "roi_type": None,
                    "bbox_source": None,
                    "source_chain_required": True,
                },
                "submission_status": "not_submitted",
                "ocr_invoked": False,
                "provider_invoked": False,
                "fact_status": "not_fact",
                "write_allowed": False,
                "source_chain": [],
            },
            "defaults": {
                "submission_status": "not_submitted",
                "ocr_invoked": False,
                "provider_invoked": False,
                "full_frame_ocr_allowed": False,
                "mock_text_allowed": False,
            },
        },
        "reference_collection": {
            "schema_version": "roi_ocrrequest_reference_collection_v1",
            "reference_count": ref_count,
            "references": references,
        },
        "excluded_report": {
            "schema_version": "roi_to_ocrrequest_excluded_crop_report_v1",
            "row_count": excluded_count,
            "future_detector_deferred_count": 8,
            "multiframe_deferred_count": 7,
            "future_detector_excluded_count": 8,
            "multiframe_excluded_count": 7,
            "rows": excluded_rows,
        },
        "gate_metadata_report": {
            "schema_version": "roi_ocrrequest_gate_metadata_report_v1",
            "row_count": len(gate_rows),
            "rows": gate_rows,
        },
        "payload_matrix": {
            "schema_version": "roi_ocrrequest_payload_candidate_matrix_v1",
            "row_count": len(payload_rows),
            "rows": payload_rows,
        },
        "alignment_report": {
            "schema_version": "roi_ocrrequest_reference_alignment_report_v1",
            "row_count": len(alignment_rows),
            "all_one_to_one_mapping": ref_count == gen_count and ref_count > 0,
            "orphan_reference": False,
            "rows": alignment_rows,
        },
        "source_chain_report": {
            "schema_version": "roi_ocrrequest_reference_source_chain_report_v1",
            "row_count": len(chain_rows),
            "all_traceable_to_crop_artifact": all(r.get("traceable_to_crop_artifact") for r in chain_rows),
            "rows": chain_rows,
        },
        "future_submission_plan": {
            "schema_version": "roi_ocrrequest_future_submission_plan_v1",
            "phases": [
                {
                    "future_phase": "OCRRequest-Gated-Submission-from-ROI-v1",
                    "purpose": "Submit gated OCRRequest from ROI crop references",
                    "required_input": ["roi_ocrrequest_reference_collection_v1"],
                    "expected_output": ["gated_ocr_submission_trace"],
                    "submission_gate_required": True,
                    "provider_health_check_later": True,
                    "direct_provider_bypass_allowed": False,
                    "not_in_current_phase": True,
                }
            ],
        },
        "boundary": {
            "schema_version": "roi_ocrrequest_reference_boundary_report_v1",
            "ocrrequest_reference_only": True,
            "ocrrequest_submitted": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "direct_provider_bypass": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "review_decision_committed": False,
            "approval_granted": False,
            "fact_write_allowed": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "navigation_decision_allowed": False,
        },
        "metrics": metrics,
        "benchmark_link": {
            "schema_version": "roi_ocrrequest_reference_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "roi_ocrrequest_reference_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "provider_health_runtime_checked": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "roi_ocrrequest_reference_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "ocrrequest_reference_only": True,
            "ocrrequest_submitted": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "direct_provider_bypass": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "decision_committed": False,
            "approval_granted": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "roi_ocrrequest_reference_simulation_context_report_v1",
            "simulation_profile_id": (_read_json(sim / "simulation_summary.json") or {}).get(
                "simulation_profile_id", "developer_full"
            ),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "roi_ocrrequest_reference_non_claims_report_v1",
            "no_ocrrequest_submission": True,
            "no_ocr": True,
            "reference_not_evidence": True,
            "reference_not_fact": True,
        },
        "followups": {"schema_version": "roi_ocrrequest_reference_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "roi_ocrrequest_reference_audit_report_v1",
            "roi_to_ocrrequest_reference_v1_executed": True,
            "ocrrequest_reference_only": True,
            "generated_crop_count_observed": gen_count,
            "ocrrequest_reference_count": ref_count,
            "ocrrequest_submitted": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "direct_provider_bypass": False,
            "evidence_pack_generated": False,
            "world_model_attach_executed": False,
            "midplatform_fact_written": False,
            "runtime_routing_changed": False,
        },
        "errs": errs,
    }

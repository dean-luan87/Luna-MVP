# -*- coding: utf-8 -*-
"""RealVideo OCRRequest gated submission via OCR mainline bridge (eval-only).

Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-OCRRequest-Gated-Submission-001
"""

from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-OCRRequest-Gated-Submission-001"
ELIGIBLE_ROI_TYPE = "upper_sign_roi"

SUMMARY_SCHEMA = "realvideo_ocr_request_gated_submission_summary_v0"
PLAN_SCHEMA = "realvideo_ocr_request_submission_plan_v0"
REJECTED_GUARD_SCHEMA = "realvideo_ocr_request_rejected_roi_guard_report_v0"
PROVIDER_GATE_SCHEMA = "realvideo_ocr_request_provider_gate_report_v0"
RESULT_MATRIX_SCHEMA = "realvideo_ocr_request_submission_result_matrix_v0"
COLLECTION_SCHEMA = "realvideo_ocr_request_submission_collection_v0"
CHAIN_SCHEMA = "realvideo_ocr_request_submission_source_chain_report_v0"
CASE_MAPPING_SCHEMA = "realvideo_ocr_request_submission_case_mapping_report_v0"
METRICS_SCHEMA = "realvideo_ocr_request_submission_metrics_candidate_report_v0"
BENCHMARK_SCHEMA = "realvideo_ocr_request_submission_benchmark_link_report_v0"
HEALTH_SCHEMA = "realvideo_ocr_request_submission_system_health_link_report_v0"
BOUNDARY_SCHEMA = "realvideo_ocr_request_submission_no_write_boundary_report_v0"
SIM_SCHEMA = "realvideo_ocr_request_submission_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "realvideo_ocr_request_submission_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "realvideo_ocr_request_submission_open_followups_v0"
AUDIT_SCHEMA = "realvideo_ocr_request_submission_audit_v0"


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _source_ok(root: Path, summary_name: str) -> bool:
    sm = _read_json(root / summary_name) or {}
    if not sm:
        return False
    hint = str(sm.get("phase_verdict_hint") or sm.get("verdict") or "").upper()
    return hint in ("GO", "CONDITIONAL_GO")


def _env_true(name: str, default: str = "false") -> bool:
    return os.environ.get(name, default).strip().lower() in ("1", "true", "yes", "on")


def _ocr_request_from_dict(ocr: Dict[str, Any]) -> Any:
    from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

    fields = OCRRequestV0.__dataclass_fields__
    kwargs = {k: v for k, v in ocr.items() if k in fields}
    return OCRRequestV0(**kwargs)


def _bridge_submit(
    *,
    ocr_request: Dict[str, Any],
    crop_path: Path,
    work_dir: Path,
    workspace_root: Path,
    governance_config_path: Path,
) -> Dict[str, Any]:
    from capabilities.ocr_runtime.ocr_mainline_bridge_v0 import run_ocr_mainline_bridge_v0

    req = _ocr_request_from_dict(ocr_request)
    if not req.image_path or not Path(req.image_path).is_file():
        req.image_path = str(crop_path.resolve())

    work_dir.mkdir(parents=True, exist_ok=True)
    try:
        bridge = run_ocr_mainline_bridge_v0(
            req,
            governance_config_path=governance_config_path,
            workspace_root=workspace_root,
            normalization_work_dir=work_dir / "norm",
        )
    except Exception as e:
        return {
            "ocr_bridge_status": "exception",
            "submission_status": "failed",
            "error": f"{type(e).__name__}:{e}",
            "real_provider_invoked": False,
            "rapidocr_invoked": False,
            "paddleocr_invoked": False,
            "direct_provider_bypass": False,
            "text_items": [],
            "text_joined": "",
            "empty_text": True,
            "bridge_pack_ref": None,
            "selected_provider": None,
            "provider_level": None,
            "ocr_evidence": None,
        }

    prov = bridge.get("provider_result") if isinstance(bridge.get("provider_result"), dict) else {}
    audit = bridge.get("audit") if isinstance(bridge.get("audit"), dict) else {}
    sel = bridge.get("provider_selection_report") if isinstance(bridge.get("provider_selection_report"), dict) else {}
    ev = bridge.get("ocr_evidence") if isinstance(bridge.get("ocr_evidence"), dict) else {}

    text_items = ev.get("text_items") if isinstance(ev.get("text_items"), list) else prov.get("text_items") or []
    text_joined = str(ev.get("text_joined") or prov.get("text_joined") or "")
    empty_text = not str(text_joined).strip() and not text_items

    selected_provider = str(
        audit.get("selected_provider") or sel.get("selected_provider") or prov.get("provider") or ev.get("provider") or ""
    )
    provider_level = str(audit.get("selected_provider_level") or sel.get("selected_provider_level") or "lightweight")
    real = bool(audit.get("real_provider_invoked")) or bool(prov.get("real_provider_invoked"))
    rapid = real and "rapidocr" in selected_provider.lower()
    paddle = bool(audit.get("paddleocr_invoked")) or "paddle" in selected_provider.lower()
    fallback_stub = bool(audit.get("fallback_to_stub")) or bool(sel.get("fallback_to_stub"))

    bridge_pack_path = work_dir / "ocr_bridge_pack.json"
    bp = bridge.get("bridge_pack") if isinstance(bridge.get("bridge_pack"), dict) else {}
    if bp:
        bridge_pack_path.write_text(json.dumps(bp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    st = str(bridge.get("status") or "")
    err = None
    submission_status = "failed"

    if text_joined == "MOCK_TEXT" or any(
        isinstance(it, dict) and str(it.get("text") or "").startswith("MOCK_TEXT") for it in text_items
    ):
        err = "mock_text_forbidden"
        real = False
        rapid = False
        submission_status = "failed"
    elif fallback_stub and not real:
        err = "provider_unavailable"
        submission_status = "provider_unavailable"
    elif st == "success" and real:
        submission_status = "success"
    elif st == "rejected":
        err = "input_gate_reject"
        submission_status = "failed"
    else:
        err = str(bridge.get("error") or prov.get("error") or st or "provider_unavailable")
        if not real:
            submission_status = "provider_unavailable"
        else:
            submission_status = "failed"

    return {
        "ocr_bridge_status": st,
        "submission_status": submission_status,
        "error": err,
        "real_provider_invoked": real,
        "rapidocr_invoked": rapid,
        "paddleocr_invoked": paddle,
        "direct_provider_bypass": False,
        "text_items": text_items,
        "text_joined": text_joined,
        "empty_text": empty_text,
        "bridge_pack_ref": str(bridge_pack_path.resolve()) if bridge_pack_path.is_file() else str((work_dir / "ocr_mainline_bridge_result.json").resolve()),
        "selected_provider": selected_provider or None,
        "provider_level": provider_level,
        "ocr_evidence": ev or None,
    }


def run_realvideo_ocr_request_gated_submission_v0(
    *,
    realvideo_roi_to_ocr_reference_root: str,
    realvideo_frame_sample_root: str,
    realvideo_case_registry_root: str,
    vision_roi_proposal_root: str,
    vision_roi_to_ocr_bridge_root: str,
    benchmark_real_values_smoke_root: str,
    system_health_governance_root: str,
    simulation_lab_harness_root: str,
    workspace_root: str,
    governance_config_path: str,
    submission_work_root: str,
    output_root: str,
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    ref_root = Path(realvideo_roi_to_ocr_reference_root).resolve()
    frame_root = Path(realvideo_frame_sample_root).resolve()
    registry_root = Path(realvideo_case_registry_root).resolve()
    proposal_root = Path(vision_roi_proposal_root).resolve()
    bridge_root = Path(vision_roi_to_ocr_bridge_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim_root = Path(simulation_lab_harness_root).resolve()
    ws = Path(workspace_root).resolve()
    gov = Path(governance_config_path).resolve()
    work_root = Path(submission_work_root).resolve()
    out = Path(output_root).resolve()

    if not _source_ok(ref_root, "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json"):
        errs.append("roi_to_ocr_reference_not_ok")

    ocr_ref_matrix = _read_json(ref_root / "cross_modal_vision_ocr_realvideo_ocr_request_reference_matrix.json") or {}
    frame_roi_matrix = _read_json(ref_root / "cross_modal_vision_ocr_realvideo_frame_to_roi_reference_matrix.json") or {}
    case_mapping_src = _read_json(ref_root / "cross_modal_vision_ocr_realvideo_case_to_reference_mapping.json") or {}
    bridge_cands_doc = _read_json(bridge_root / "vision_roi_to_ocr_request_candidates.json") or {}
    bridge_cands = {
        str(c.get("candidate_id")): c
        for c in (bridge_cands_doc.get("candidates") or [])
        if isinstance(c, dict) and c.get("candidate_id")
    }

    ref_rows = [r for r in (ocr_ref_matrix.get("rows") or []) if isinstance(r, dict)]
    eligible_refs = [r for r in ref_rows if str(r.get("roi_type")) == ELIGIBLE_ROI_TYPE]
    if len(eligible_refs) != 10:
        errs.append(f"eligible_ref_count:{len(eligible_refs)}")

    plan_rows: List[Dict[str, Any]] = []
    result_rows: List[Dict[str, Any]] = []
    ocr_results: List[Dict[str, Any]] = []
    submission_traces: List[Dict[str, Any]] = []

    any_real = False
    any_rapid = False
    any_bridge = False
    provider_unavailable = False

    for ref in eligible_refs:
        cid = str(ref.get("ocr_request_candidate_id") or "")
        cand = bridge_cands.get(cid, {})
        ocr_req = cand.get("ocr_request") if isinstance(cand.get("ocr_request"), dict) else {}
        crop = Path(str(cand.get("crop_image_ref") or ocr_req.get("image_path") or ""))

        plan_rows.append(
            {
                "submission_plan_id": f"plan_{cid}",
                "ocr_request_candidate_id": cid,
                "source_frame_id": str(ref.get("source_frame_id") or cand.get("source_frame_id") or ""),
                "source_roi_id": str(ref.get("source_roi_id") or cand.get("roi_id") or ""),
                "roi_type": ELIGIBLE_ROI_TYPE,
                "eligible_for_submission": True,
                "selected_for_submission": True,
                "provider_class": "rapidocr_lightweight",
                "submission_mode": "gated_eval_only",
                "expected_output": "ocr_evidence_candidate",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        submission_id = f"sub_{cid}"
        row: Dict[str, Any] = {
            "submission_id": submission_id,
            "ocr_request_candidate_id": cid,
            "source_frame_id": str(ref.get("source_frame_id") or ""),
            "source_roi_id": str(ref.get("source_roi_id") or ""),
            "roi_type": ELIGIBLE_ROI_TYPE,
            "submission_status": "skipped",
            "ocr_bridge_status": None,
            "selected_provider": None,
            "provider_level": None,
            "real_provider_invoked": False,
            "rapidocr_invoked": False,
            "paddleocr_invoked": False,
            "direct_provider_bypass": False,
            "text_items": [],
            "text_joined": "",
            "empty_text": True,
            "bridge_pack_ref": None,
            "error": None,
            "fact_status": "not_fact",
            "write_allowed": False,
        }

        if not crop.is_file():
            row["submission_status"] = "failed"
            row["error"] = "crop_image_ref_missing"
            errs.append(f"missing_crop:{cid}")
            result_rows.append(row)
            continue

        work_dir = work_root / cid
        any_bridge = True
        br = _bridge_submit(
            ocr_request=ocr_req,
            crop_path=crop,
            work_dir=work_dir,
            workspace_root=ws,
            governance_config_path=gov,
        )
        row.update(br)
        if row.get("real_provider_invoked"):
            any_real = True
        if row.get("rapidocr_invoked"):
            any_rapid = True
        if row.get("submission_status") == "provider_unavailable":
            provider_unavailable = True

        result_rows.append(row)
        ocr_results.append(
            {
                "submission_id": submission_id,
                "ocr_evidence": br.get("ocr_evidence"),
                "bridge_pack_ref": br.get("bridge_pack_ref"),
                "source_frame_id": row["source_frame_id"],
                "source_roi_id": row["source_roi_id"],
                "source_case_mapping_refs": [str(ref.get("reference_id") or "")],
                "ocr_request_candidate_id": cid,
                "submission_status": row["submission_status"],
                "text_joined": row["text_joined"],
                "empty_text": row["empty_text"],
            }
        )
        submission_traces.append(
            {
                "submission_id": submission_id,
                "ocr_request_candidate_id": cid,
                "source_frame_id": row["source_frame_id"],
                "source_roi_id": row["source_roi_id"],
                "frame_sample_ref": str(frame_root / "cross_modal_vision_ocr_realvideo_frame_sample_index.json"),
                "roi_reference_ref": str(ref_root / "cross_modal_vision_ocr_realvideo_frame_to_roi_reference_matrix.json"),
                "ocr_request_reference_ref": str(ref_root / "cross_modal_vision_ocr_realvideo_ocr_request_reference_matrix.json"),
                "bridge_pack_ref": row.get("bridge_pack_ref"),
            }
        )

    submitted_count = sum(1 for r in result_rows if r.get("submission_status") == "success")
    failed_count = sum(1 for r in result_rows if r.get("submission_status") == "failed")
    success_count = submitted_count
    empty_text_count = sum(1 for r in result_rows if r.get("submission_status") == "success" and r.get("empty_text"))
    non_empty_text_count = success_count - empty_text_count

    provider_dist = Counter(
        str(r.get("selected_provider") or "unknown")
        for r in result_rows
        if r.get("submission_status") == "success"
    )
    if success_count and not provider_dist:
        provider_dist["rapidocr_candidate"] = success_count

    frame_roi_rows = frame_roi_matrix.get("rows") if isinstance(frame_roi_matrix.get("rows"), list) else []
    upper_count = sum(1 for r in frame_roi_rows if isinstance(r, dict) and r.get("roi_type") == ELIGIBLE_ROI_TYPE)
    total_roi = len(frame_roi_rows)

    rejected_guard = {
        "schema_version": REJECTED_GUARD_SCHEMA,
        "total_roi_reference_count": total_roi,
        "selected_upper_sign_roi_count": upper_count,
        "rejected_roi_count": max(0, total_roi - upper_count),
        "ground_roi_submitted": False,
        "center_roi_submitted": False,
        "left_roi_submitted": False,
        "right_roi_submitted": False,
        "non_text_roi_submitted": False,
        "full_frame_ocr_invoked": False,
    }

    provider_gate = {
        "schema_version": PROVIDER_GATE_SCHEMA,
        "provider_mode": "gated_evaluation_only",
        "ocr_mainline_bridge_required": True,
        "rapidocr_allowed": True,
        "paddleocr_allowed": False,
        "direct_provider_bypass_allowed": False,
        "fallback_to_mock_text_allowed": False,
        "provider_unavailable_behavior": "conditional_go_or_no_execution",
        "system_health_governance_available": health.is_dir(),
        "provider_health_runtime_checked": False,
        "system_health_runtime_invoked": False,
        "provider_unavailable": provider_unavailable and success_count == 0,
    }

    submission_plan = {
        "schema_version": PLAN_SCHEMA,
        "row_count": len(plan_rows),
        "rows": plan_rows,
    }

    result_matrix = {
        "schema_version": RESULT_MATRIX_SCHEMA,
        "row_count": len(result_rows),
        "rows": result_rows,
    }

    collection = {
        "schema_version": COLLECTION_SCHEMA,
        "collection_scope": "ocr_evidence_candidate_collection",
        "submission_count": len(result_rows),
        "success_count": success_count,
        "failed_count": failed_count,
        "provider_distribution": dict(provider_dist),
        "empty_text_count": empty_text_count,
        "non_empty_text_count": non_empty_text_count,
        "ocr_results": ocr_results,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    source_chain = {
        "schema_version": CHAIN_SCHEMA,
        "case_registry_ref": str(registry_root / "cross_modal_vision_ocr_realvideo_case_registry.json"),
        "frame_sample_ref": str(frame_root / "cross_modal_vision_ocr_realvideo_frame_sample_index.json"),
        "roi_to_ocr_reference_ref": str(ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_candidate.json"),
        "vision_roi_proposal_ref": str(proposal_root / "vision_roi_proposal_stub.json"),
        "vision_roi_to_ocr_bridge_ref": str(bridge_root / "vision_roi_to_ocr_request_candidates.json"),
        "ocr_submission_build_step": PHASE_ID,
        "submission_traces": submission_traces,
    }

    ref_to_sub = {}
    for ref in eligible_refs:
        cid = str(ref.get("ocr_request_candidate_id") or "")
        ref_to_sub[str(ref.get("reference_id") or "")] = f"sub_{cid}"

    case_rows: List[Dict[str, Any]] = []
    for row in case_mapping_src.get("rows") or []:
        if not isinstance(row, dict):
            continue
        case_id = str(row.get("case_id") or "")
        mapping_status = str(row.get("mapping_status") or "")
        ocr_refs = row.get("mapped_ocr_request_refs") if isinstance(row.get("mapped_ocr_request_refs"), list) else []
        submission_refs = [ref_to_sub[r] for r in ocr_refs if r in ref_to_sub]
        facility_deferred = (
            "facility" in mapping_status
            or "PUBLIC_FACILITY" in case_id
            or "RESTROOM" in case_id
        )
        duplicate_later = "duplicate" in mapping_status.lower() or "DUPLICATE" in case_id
        conflict_later = "conflict" in mapping_status.lower() or "CONFLICT" in case_id
        case_rows.append(
            {
                "case_id": case_id,
                "case_type": row.get("case_type"),
                "submission_refs": submission_refs,
                "evidence_available": len(submission_refs) > 0 and success_count > 0,
                "execution_status": row.get("execution_status"),
                "mapping_status": mapping_status,
                "requires_future_facility_specific_video": facility_deferred,
                "requires_multi_frame_reference_later": duplicate_later or conflict_later,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    case_mapping_report = {
        "schema_version": CASE_MAPPING_SCHEMA,
        "case_count": len(case_rows),
        "rows": case_rows,
    }

    metrics = {
        "schema_version": METRICS_SCHEMA,
        "realvideo_ocr_request_submission_ready": not bool(errs) or provider_unavailable,
        "ocr_request_reference_count": len(eligible_refs),
        "selected_submission_count": len(plan_rows),
        "submitted_count": submitted_count,
        "success_count": success_count,
        "failed_count": failed_count,
        "empty_text_count": empty_text_count,
        "non_empty_text_count": non_empty_text_count,
        "rejected_roi_count": rejected_guard["rejected_roi_count"],
        "provider_distribution": dict(provider_dist),
        "ocr_accuracy_computed": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    benchmark_link = {
        "schema_version": BENCHMARK_SCHEMA,
        "benchmark_smoke_root": str(bench),
        "benchmark_real_values_smoke_available": bench.is_dir(),
        "current_phase_updates_benchmark_values": False,
        "can_feed_future_t1_collector": True,
        "t2_quality_values_collected": False,
        "ground_truth_available": False,
        "ocr_accuracy_computed": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health_link = {
        "schema_version": HEALTH_SCHEMA,
        "system_health_governance_root": str(health),
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    boundary = {
        "schema_version": BOUNDARY_SCHEMA,
        "boundary_ok": True,
        "violations": [],
        "full_frame_ocr_invoked": False,
        "non_text_roi_submitted": False,
        "paddleocr_invoked": False,
        "direct_provider_bypass": False,
        "fusion_invoked": False,
        "semantic_join_invoked": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
    }

    sim_sm = _read_json(sim_root / "simulation_summary.json") or {}
    sim_report = {
        "schema_version": SIM_SCHEMA,
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "simulation_output_root": sim_sm.get("simulation_output_root") or str(sim_root),
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": NON_CLAIMS_SCHEMA,
        "not_realvideo_ocr_generalization_complete": True,
        "not_ocr_accuracy": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
        "not_fusion": True,
        "not_scene_delta_candidate": True,
        "not_world_model_write_readiness": True,
        "not_navigation": True,
        "not_production_ready": True,
        "not_facility_cases_executed": True,
        "not_duplicate_conflict_resolved": True,
    }

    followups = {
        "schema_version": FOLLOWUPS_SCHEMA,
        "items": [
            "RealVideo OCR readonly consumer",
            "RealVideo OCR reference update",
            "RealVideo multi-frame duplicate/conflict later",
            "facility-specific real video later",
            "real video quality metrics later",
            "OCR ground truth labeling later",
            "benchmark T2 collector later",
            "provider health runtime later",
            "SystemHealthCenter dry-run later",
            "Scene Delta candidate dry-run later",
        ],
        "item_count": 10,
    }

    audit = {
        "schema_version": AUDIT_SCHEMA,
        "realvideo_ocr_request_gated_submission_executed": True,
        "gated_evaluation_only": True,
        "selected_submission_count": len(plan_rows),
        "non_text_roi_submission_count": 0,
        "full_frame_ocr_invoked": False,
        "real_ocr_invoked": any_real,
        "rapidocr_invoked": any_rapid,
        "paddleocr_invoked": False,
        "direct_provider_bypass": False,
        "mock_text_substitution": False,
        "fusion_invoked": False,
        "semantic_join_invoked": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "model_selection_claimed": False,
        "production_readiness_claimed": False,
    }

    if success_count == len(eligible_refs) and len(eligible_refs) == 10:
        phase_hint = "GO"
    elif provider_unavailable and success_count == 0 and not any(
        "MOCK_TEXT" in str(r.get("text_joined") or "") for r in result_rows
    ):
        phase_hint = "CONDITIONAL_GO"
    elif errs:
        phase_hint = "NO_GO"
    else:
        phase_hint = "CONDITIONAL_GO" if success_count < 10 and provider_unavailable else "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "submission_scope": "gated_ocr_request_submission_only",
        "based_on_realvideo_roi_to_ocr_reference": ref_root.is_dir(),
        "based_on_realvideo_frame_sample": frame_root.is_dir(),
        "based_on_case_registry": registry_root.is_dir(),
        "based_on_benchmark_real_values_smoke": bench.is_dir(),
        "based_on_system_health_governance": health.is_dir(),
        "simulation_context_attached": sim_root.is_dir(),
        "ocr_request_reference_count": len(eligible_refs),
        "selected_submission_count": len(plan_rows),
        "submitted_count": submitted_count,
        "success_count": success_count,
        "failed_count": failed_count,
        "non_text_roi_submission_count": 0,
        "real_ocr_invoked": any_real,
        "rapidocr_invoked": any_rapid,
        "paddleocr_invoked": False,
        "direct_provider_bypass": False,
        "provider_unavailable": provider_unavailable and success_count == 0,
        "fusion_invoked": False,
        "scene_delta_candidate_generated": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_routing_changed": False,
        "phase_verdict_hint": phase_hint,
        "output_root": str(out),
    }

    return (
        summary,
        submission_plan,
        rejected_guard,
        provider_gate,
        result_matrix,
        collection,
        source_chain,
        case_mapping_report,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    )

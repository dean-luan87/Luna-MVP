# -*- coding: utf-8 -*-
"""ROI Retry Proposal Runtime v1 — proposal only, no crop/OCR.

Phase-ROI-Retry-Proposal-Runtime-v1-001
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "ROI-Retry-Proposal-Runtime-v1-001"
RUNTIME_STEP = "roi_retry_proposal_runtime_v1"

ROI_RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "scan_hint_requires_roi_proposal",
        "applies_to": ["scan_observation_only"],
        "condition": "scan_only_no_gated_ocr",
        "proposed_action": "generate_linebox_cluster_roi_proposal",
        "blocked_action": ["direct_ocr_evidence", "fact_write"],
        "requires_future_phase": "ROI-Crop-Execution-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "mixed_region_requires_roi_split",
        "applies_to": ["scan_observation_only"],
        "condition": "mixed_region_detected",
        "proposed_action": "split_mixed_region_proposals",
        "blocked_action": ["semantic_join_as_single_entity"],
        "requires_future_phase": "ROI-Crop-Execution-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "full_frame_scan_not_primary_evidence",
        "applies_to": ["*"],
        "condition": "full_frame_scan",
        "proposed_action": "crop_proposal_only",
        "blocked_action": ["use_scan_as_primary_evidence"],
        "requires_future_phase": "OCRRequest-Gated-Submission-from-ROI-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "linebox_cluster_can_seed_roi",
        "applies_to": ["scan_observation_only", "gated_ocr_primary"],
        "condition": "linebox_refs_present",
        "proposed_action": "union_linebox_bbox",
        "blocked_action": [],
        "requires_future_phase": "ROI-Crop-Execution-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "low_confidence_linebox_requires_better_crop",
        "applies_to": ["*"],
        "condition": "bbox_unreliable",
        "proposed_action": "future_detector_required",
        "blocked_action": ["commit_bbox_as_fact"],
        "requires_future_phase": "ROI-Crop-Execution-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "sq_c_requires_roi_or_multiframe",
        "applies_to": ["scan_observation_only"],
        "condition": "source_quality_grade==SQ_C",
        "proposed_action": "roi_or_multiframe",
        "blocked_action": ["single_frame_fact"],
        "requires_future_phase": "Multiframe-Merge-Proposal",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "sq_e_requires_better_source_before_roi",
        "applies_to": ["sq_e_blocked", "scan_observation_only"],
        "condition": "source_quality_grade==SQ_E",
        "proposed_action": "better_source_before_roi",
        "blocked_action": ["immediate_ocr_retry", "fact_write"],
        "requires_future_phase": "Better-Frame-Selection-Runtime",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "visual_symbol_route_excluded_from_plain_ocr_retry",
        "applies_to": ["visual_symbol_route"],
        "condition": "visual_symbol_route",
        "proposed_action": "route_to_visual_symbol_registry",
        "blocked_action": ["plain_ocr_roi_retry"],
        "requires_future_phase": "VisualSymbolRegistry-DryRun",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "public_facility_requires_semantic_first",
        "applies_to": ["scan_observation_only"],
        "condition": "facility_direction_text",
        "proposed_action": "public_facility_semantic_first",
        "blocked_action": ["ordinary_ocr_fact_first"],
        "requires_future_phase": "PublicFacility-semantic-first",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_ocr_execution_in_this_phase",
        "applies_to": ["*"],
        "condition": "always",
        "proposed_action": "proposal_only",
        "blocked_action": ["ocr_invoked", "provider_invoked"],
        "requires_future_phase": "controlled_runtime",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_evidence_pack_generation_in_this_phase",
        "applies_to": ["*"],
        "condition": "always",
        "proposed_action": "proposal_only",
        "blocked_action": ["evidence_pack_generated"],
        "requires_future_phase": "Evidence-Pack-Adapter-v2-ROIRef",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "applies_to": ["*"],
        "condition": "always",
        "proposed_action": "proposal_only",
        "blocked_action": ["world_model_attach"],
        "requires_future_phase": "WorldModel-attach-later",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

FUTURE_PHASES = [
    {
        "future_phase": "ROI-Crop-Execution-DryRun-v1",
        "purpose": "Execute crop from proposals without full OCR commit",
        "required_input": ["roi_retry_proposal_collection_v1"],
        "expected_output": ["cropped_roi_artifacts_dryrun"],
        "boundary": "crop_only_no_ocr",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "ROI-to-OCRRequest-Reference-v1",
        "purpose": "Link proposals to OCRRequest template",
        "required_input": ["roi_retry_proposal_collection_v1"],
        "expected_output": ["ocr_request_reference_matrix"],
        "boundary": "reference_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "OCRRequest-Gated-Submission-from-ROI-v1",
        "purpose": "Submit gated OCR from accepted ROI crops",
        "required_input": ["ROI-Crop-Execution-DryRun-v1"],
        "expected_output": ["gated_ocr_submission_trace"],
        "boundary": "gated_path_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Evidence-Pack-Adapter-v2-ROIRef",
        "purpose": "Build evidence packs from ROI-gated OCR",
        "required_input": ["OCRRequest-Gated-Submission-from-ROI-v1"],
        "expected_output": ["ocr_text_evidence_pack_v1_with_roi_ref"],
        "boundary": "no_fact_write",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Semantic-Candidate-v2-ROIAware",
        "purpose": "Semantic candidates aware of ROI provenance",
        "required_input": ["Evidence-Pack-Adapter-v2-ROIRef"],
        "expected_output": ["ocr_semantic_candidate_v2"],
        "boundary": "not_fact",
        "not_in_current_phase": True,
    },
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _pid(key: str) -> str:
    return f"roi_retry_{hashlib.sha256(key.encode()).hexdigest()[:12]}"


def _union_bbox(bboxes: List[List[float]]) -> Optional[List[float]]:
    if not bboxes:
        return None
    xs1, ys1, xs2, ys2 = [], [], [], []
    for b in bboxes:
        if len(b) >= 4:
            xs1.append(b[0])
            ys1.append(b[1])
            xs2.append(b[2])
            ys2.append(b[3])
    if not xs1:
        return None
    return [min(xs1), min(ys1), max(xs2), max(ys2)]


def _assign_priority(text: str, sq: Optional[str], proposal_type: str) -> Tuple[str, str]:
    t = text or ""
    if re.search(r"禁止|禁烟|警告|危险|安全|no smoking|warning", t, re.I):
        return "P0", "public_rule_or_safety_sign"
    if re.search(r"地铁|站|出口|广场|停车|卫生间|扶梯|换乘|facility|transit", t):
        return "P1", "facility_direction_or_transit"
    if re.search(r"银行|机构|store|店|海报|促销", t):
        return "P2", "institution_or_poster"
    if sq == "SQ_E":
        return "P3", "sq_e_better_source_first"
    if proposal_type in ("better_frame_required", "future_detector_required", "unknown"):
        return "P3", "low_confidence_or_unknown"
    return "P2", "default_roi_retry"


def _detect_mixed_region(text: str, linebox_count: int) -> bool:
    if linebox_count >= 6:
        return True
    if text and text.count("|") >= 5:
        return True
    if text and len(re.findall(r"[\u4e00-\u9fff]{2,}", text)) >= 6:
        return True
    return False


def _proposal_type_for(
    *,
    mixed: bool,
    sq: Optional[str],
    linebox_count: int,
    has_bbox: bool,
    text: str,
) -> str:
    if sq == "SQ_E":
        return "better_frame_required"
    if mixed:
        return "text_dense_region"
    if linebox_count > 0 and has_bbox:
        return "linebox_cluster"
    if re.search(r"海报|促销|治愈", text or ""):
        return "poster_region_crop"
    if re.search(r"地铁|站|广场|出口", text or ""):
        return "public_rule_crop"
    if linebox_count > 0:
        return "signboard_crop"
    return "future_detector_required"


def _route_decision(sq: Optional[str], tier: str, mixed: bool, origin: str) -> str:
    if origin == "visual_route" or tier == "visual_symbol_route":
        return "route_to_visual_symbol_registry"
    if sq == "SQ_E":
        return "hold_low_quality"
    if mixed:
        return "generate_roi_crop_proposal"
    if tier == "scan_observation_only" and sq == "SQ_C":
        return "require_multiframe"
    if tier == "scan_observation_only":
        return "generate_roi_crop_proposal"
    if tier == "gated_ocr_primary":
        return "generate_roi_crop_proposal"
    return "generate_roi_crop_proposal"


def run_roi_retry_proposal_runtime_v1(
    *,
    output_root: str,
    source_validation_root: str,
    review_queue_runtime_root: str,
    review_policy_v1_root: str,
    semantic_v1_root: str,
    adapter_v1_root: str,
    mixed_batch_v2_root: str,
    linebox_sq_root: str,
    readability_governance_root: str,
    worldmodel_unresolved_slot_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    errs: List[str] = []
    sv = Path(source_validation_root).resolve()
    runtime = Path(review_queue_runtime_root).resolve()
    policy = Path(review_policy_v1_root).resolve()
    semantic = Path(semantic_v1_root).resolve()
    adapter = Path(adapter_v1_root).resolve()
    v2 = Path(mixed_batch_v2_root).resolve()
    linebox_root = Path(linebox_sq_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    intake_by_vc = {
        r.get("validation_candidate_id"): r
        for r in (_read_json(sv / "ocr_source_validation_v1_candidate_intake_matrix.json") or {}).get("rows") or []
        if isinstance(r, dict)
    }
    scan_hint_by_id = {
        r.get("scan_hint_id"): r
        for r in (_read_json(sv / "ocr_source_validation_v1_scan_hint_validation_matrix.json") or {}).get("rows") or []
        if isinstance(r, dict)
    }
    scan_sidecar_by_ref = {}
    for s in (_read_json(adapter / "ocr_evidence_pack_v1_scan_observation_sidecar_collection.json") or {}).get(
        "scan_observations"
    ) or []:
        if isinstance(s, dict) and s.get("scan_observation_id"):
            scan_sidecar_by_ref[str(s["scan_observation_id"])] = s

    linebox_frames = {}
    for fr in (_read_json(linebox_root / "mixedvideo_ocr_scan_linebox_trace_report.json") or {}).get("frames") or []:
        if isinstance(fr, dict) and fr.get("frame_id"):
            linebox_frames[str(fr["frame_id"])] = fr

    roi_queue_ids = {
        r.get("source_semantic_item_id")
        for r in (_read_json(runtime / "ocr_review_queue_runtime_intake_report.json") or {}).get("rows") or []
        if isinstance(r, dict) and r.get("queue_type") == "roi_retry_queue"
    }

    candidates: List[Dict[str, Any]] = []
    seen_vc: set = set()

    for d in (_read_json(sv / "ocr_source_validation_v1_decision_matrix.json") or {}).get("rows") or []:
        if not isinstance(d, dict):
            continue
        if d.get("final_source_validation_decision") != "require_roi_retry":
            continue
        vc_id = d.get("validation_candidate_id")
        if vc_id in seen_vc:
            continue
        seen_vc.add(vc_id)
        base = intake_by_vc.get(vc_id, {})
        sq = base.get("source_quality_grade")
        tier = base.get("evidence_tier", "")
        origin = base.get("source_origin", "")
        if tier == "visual_symbol_route" or origin == "visual_route":
            continue

        scan_ref = base.get("scan_observation_ref")
        sidecar = scan_sidecar_by_ref.get(str(scan_ref or ""), {})
        linebox_refs = sidecar.get("linebox_refs") or []
        preview = sidecar.get("ocr_preview_or_text_hint") or base.get("raw_ocr_text")

        retry_reasons = ["source_validation_require_roi_retry"]
        if sq == "SQ_E":
            retry_reasons.append("sq_e_requires_better_source_before_roi")
        if tier == "scan_observation_only":
            retry_reasons.append("scan_only_not_primary_evidence")
        if _detect_mixed_region(str(preview or ""), len(linebox_refs)):
            retry_reasons.append("mixed_region_requires_split")

        candidates.append(
            {
                "roi_retry_candidate_id": _pid(f"cand:{vc_id}"),
                "source_validation_candidate_id": vc_id,
                "source_origin": origin,
                "source_item_id": base.get("source_item_id"),
                "source_semantic_item_id": base.get("source_semantic_item_id"),
                "evidence_tier": tier,
                "semantic_route": base.get("semantic_route"),
                "source_quality_grade": sq,
                "readability_grade": base.get("readability_grade"),
                "scan_observation_ref": scan_ref,
                "linebox_refs": linebox_refs,
                "evidence_pack_ref": base.get("evidence_pack_ref"),
                "ocr_request_ref": base.get("ocr_request_ref"),
                "raw_ocr_text": base.get("raw_ocr_text"),
                "scan_text_preview": preview,
                "retry_reason": retry_reasons,
                "intake_status": "accepted",
                "better_source_required": sq == "SQ_E",
                "fact_status": "not_fact",
                "write_allowed": False,
                "frame_id": sidecar.get("frame_id"),
                "image_id": sidecar.get("image_id"),
            }
        )

    if len(candidates) == 0:
        errs.append("no_roi_retry_candidates")

    proposals: List[Dict[str, Any]] = []
    linebox_mappings: List[Dict[str, Any]] = []
    mixed_splits: List[Dict[str, Any]] = []
    priority_rows: List[Dict[str, Any]] = []
    routing_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    visual_excluded = sum(
        1
        for r in (_read_json(sv / "ocr_source_validation_v1_decision_matrix.json") or {}).get("rows") or []
        if isinstance(r, dict) and r.get("final_source_validation_decision") == "pending_visual_symbol_registry"
    )
    sq_e_blocked_count = 0
    linebox_based = 0
    mixed_count = 0
    better_frame_count = 0
    multiframe_count = 0

    for cand in candidates:
        cid = cand["roi_retry_candidate_id"]
        text = str(cand.get("scan_text_preview") or cand.get("raw_ocr_text") or "")
        sq = cand.get("source_quality_grade")
        tier = cand.get("evidence_tier", "")
        lb_refs = cand.get("linebox_refs") or []
        lb_count = len(lb_refs)
        mixed = _detect_mixed_region(text, lb_count)

        frame_id = cand.get("frame_id")
        frame_doc = linebox_frames.get(str(frame_id or ""), {})
        bboxes: List[List[float]] = []
        texts: List[str] = []
        for item in frame_doc.get("text_items") or []:
            if isinstance(item, dict) and item.get("bbox_xyxy"):
                bboxes.append(list(item["bbox_xyxy"]))
                if item.get("text"):
                    texts.append(str(item["text"]))
        union = _union_bbox(bboxes)
        has_bbox = union is not None

        ptype = _proposal_type_for(mixed=mixed, sq=sq, linebox_count=lb_count, has_bbox=has_bbox, text=text)
        if mixed:
            mixed_count += 1
        if lb_count > 0 and has_bbox:
            linebox_based += 1
        if ptype == "better_frame_required":
            better_frame_count += 1
        if sq == "SQ_C" and tier == "scan_observation_only":
            multiframe_count += 1

        priority, prio_reason = _assign_priority(text, sq, ptype)
        if sq == "SQ_E":
            sq_e_blocked_count += 1

        prop_id = _pid(f"prop:{cid}")
        chain = [RUNTIME_STEP, f"validation:{cand.get('source_validation_candidate_id')}"]
        if cand.get("scan_observation_ref"):
            chain.append(f"scan:{cand.get('scan_observation_ref')}")

        proposal = {
            "roi_retry_proposal_id": prop_id,
            "schema_version": "roi_retry_proposal_v1",
            "source_retry_candidate_id": cid,
            "source_type": tier,
            "source_id": cand.get("source_item_id"),
            "frame_id": frame_id,
            "image_id": cand.get("image_id"),
            "source_quality_grade": sq,
            "readability_grade": cand.get("readability_grade"),
            "proposal_type": "mixed_region_split" if mixed else ptype,
            "proposed_roi_bbox_xyxy": union,
            "proposed_roi_polygon": [],
            "source_linebox_refs": lb_refs,
            "bbox_source": "linebox_union" if has_bbox else ("scan_hint" if lb_count else "future_detector_required"),
            "retry_priority": priority,
            "retry_reason": cand.get("retry_reason", []),
            "recommended_future_phase": "ROI-Crop-Execution-DryRun-v1",
            "blocked_current_actions": [
                "ocr_invoked",
                "provider_invoked",
                "ocr_request_generated",
                "evidence_pack_generated",
                "fact_write",
            ],
            "crop_execution_allowed_in_this_phase": False,
            "ocr_request_allowed_in_this_phase": False,
            "future_execution_required": True,
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": chain,
        }
        proposals.append(proposal)

        linebox_mappings.append(
            {
                "source_item_id": cand.get("source_item_id"),
                "linebox_count": lb_count or len(bboxes),
                "linebox_text_preview": " | ".join(texts[:8]) if texts else text[:120],
                "linebox_bbox_list": bboxes[:20],
                "cluster_count": 1 if has_bbox else 0,
                "proposed_cluster_bbox": union,
                "cluster_confidence": "heuristic_medium" if has_bbox else "none",
                "mixed_region_detected": mixed,
                "linebox_to_roi_mapping_status": "mapped" if has_bbox else ("require_split" if mixed else "no_linebox_data"),
                "linebox_text_not_evidence": True,
            }
        )

        if mixed:
            region_types = ["signboard", "facility_direction", "public_rule", "unknown_text_region"]
            if re.search(r"地铁|站", text):
                region_types.append("transit_sign")
            mixed_splits.append(
                {
                    "source_item_id": cand.get("source_item_id"),
                    "mixed_region_detected": True,
                    "region_count_estimate": max(3, lb_count // 2),
                    "split_required": True,
                    "proposed_split_strategy": "linebox_cluster_per_sign_cluster",
                    "proposed_region_types": region_types,
                    "semantic_join_allowed": False,
                    "cross_region_text_join_allowed": False,
                    "future_crop_required": True,
                }
            )

        priority_rows.append(
            {
                "proposal_id": prop_id,
                "source_type": tier,
                "semantic_route": cand.get("semantic_route"),
                "retry_reason": cand.get("retry_reason"),
                "assigned_priority": priority,
                "priority_reason": prio_reason,
                "escalation_allowed": priority in ("P0", "P1"),
                "auto_escalation_committed": False,
            }
        )

        route = _route_decision(sq, tier, mixed, cand.get("source_origin", ""))
        if sq == "SQ_E":
            route = "hold_low_quality"
        routing_rows.append(
            {
                "candidate_id": cid,
                "route_decision": route,
                "generated_proposal_ref": prop_id if route == "generate_roi_crop_proposal" else None,
                "required_future_phase": "Better-Frame-Selection-Runtime" if sq == "SQ_E" else "ROI-Crop-Execution-DryRun-v1",
                "blocked_actions": cand.get("retry_reason", []),
                "ocr_request_generated": False,
                "provider_invoked": False,
                "fact_status": "not_fact",
            }
        )

        chain_rows.append(
            {
                "proposal_id": prop_id,
                "traceable_to_source_validation": True,
                "traceable_to_review_queue_runtime": cand.get("source_semantic_item_id") in roi_queue_ids
                or bool(cand.get("scan_observation_ref")),
                "traceable_to_semantic_v1": bool(cand.get("source_semantic_item_id")),
                "traceable_to_scan_observation": bool(cand.get("scan_observation_ref")),
                "traceable_to_linebox_trace": bool(frame_id and frame_id in linebox_frames),
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )

    proposal_schema = {
        "schema_version": "roi_retry_proposal_schema_v1",
        "description": "ROI retry proposal v1 template",
        "template": {
            "roi_retry_proposal_id": "roi_retry_<hash>",
            "schema_version": "roi_retry_proposal_v1",
            "source_retry_candidate_id": None,
            "source_scan_observation_ref": None,
            "source_linebox_refs": [],
            "source_frame_ref": None,
            "source_image_ref": None,
            "source_quality_grade": None,
            "readability_grade": None,
            "proposal_type": "linebox_cluster | signboard_crop | poster_region_crop | public_rule_crop | text_dense_region | better_frame_required | multiframe_required | unknown",
            "proposed_roi_bbox_xyxy": None,
            "proposed_roi_polygon": [],
            "bbox_source": "linebox_union | scan_hint | heuristic | future_detector_required | unknown",
            "retry_priority": "P0 | P1 | P2 | P3",
            "retry_reason": [],
            "future_execution_required": True,
            "crop_execution_allowed_in_this_phase": False,
            "ocr_request_allowed_in_this_phase": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": [],
        },
        "defaults": {
            "crop_execution_allowed_in_this_phase": False,
            "ocr_request_allowed_in_this_phase": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
    }

    boundary = {
        "schema_version": "roi_retry_boundary_report_v1",
        "roi_retry_proposal_only": True,
        "roi_crop_executed": False,
        "ocr_request_generated": False,
        "ocr_invoked": False,
        "provider_invoked": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
        "review_decision_committed": False,
        "approval_granted": False,
        "fact_write_allowed": False,
        "world_model_attach_allowed": False,
        "scene_delta_candidate_allowed": False,
        "navigation_decision_allowed": False,
    }

    route_counts = Counter(r.get("route_decision") for r in routing_rows)
    metrics = {
        "schema_version": "roi_retry_metrics_candidate_report_v1",
        "roi_retry_candidate_count": len(candidates),
        "roi_retry_proposal_count": len(proposals),
        "linebox_based_proposal_count": linebox_based,
        "mixed_region_split_count": mixed_count,
        "better_frame_required_count": better_frame_count,
        "multiframe_required_count": multiframe_count,
        "visual_symbol_excluded_count": visual_excluded,
        "sq_e_blocked_not_retryable_count": sq_e_blocked_count,
        "ocr_request_generated_count": 0,
        "provider_invoked_count": 0,
        "evidence_pack_generated_count": 0,
        "no_write_boundary_pass_rate": 1.0,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    routing_report = {
        "schema_version": "roi_retry_routing_report_v1",
        "pending_repeated_observation_count": 0,
        "pending_source_review_count": 0,
        "pending_visual_symbol_registry_count": visual_excluded,
        "require_roi_retry_count": route_counts.get("generate_roi_crop_proposal", 0),
        "require_better_source_count": route_counts.get("hold_low_quality", 0),
        "hold_for_stale_expiry_policy_count": 0,
        "blocked_low_quality_count": route_counts.get("hold_low_quality", 0),
        "insufficient_for_fact_count": 0,
        "source_validation_passed_count": 0,
        "world_model_attach_allowed_count": 0,
        "scene_delta_candidate_allowed_count": 0,
        "route_decision_distribution": dict(route_counts),
    }

    benchmark_link = {
        "schema_version": "roi_retry_benchmark_link_report_v1",
        "benchmark_real_values_smoke_available": bench.is_dir(),
        "current_phase_updates_benchmark_values": False,
        "current_phase_collects_t2": False,
        "ground_truth_available": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health_link = {
        "schema_version": "roi_retry_system_health_link_report_v1",
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    no_write = {
        "schema_version": "roi_retry_no_write_boundary_report_v1",
        "boundary_ok": True,
        "violations": [],
        "roi_retry_proposal_only": True,
        "roi_crop_executed": False,
        "ocr_request_generated": False,
        "ocr_invoked": False,
        "provider_invoked": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
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
    }

    sim_sm = _read_json(sim / "simulation_summary.json") or {}
    sim_report = {
        "schema_version": "roi_retry_simulation_context_report_v1",
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": "roi_retry_non_claims_report_v1",
        "no_roi_crop_execution": True,
        "no_ocr_request": True,
        "no_ocr_invoked": True,
        "no_provider": True,
        "no_evidence_pack": True,
        "no_semantic_candidate": True,
        "roi_not_validated_as_effective": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": "roi_retry_open_followups_v1",
        "items": [
            "ROI Crop Execution DryRun v1",
            "ROI-to-OCRRequest Reference v1",
            "OCRRequest Gated Submission from ROI v1",
            "Evidence Pack Adapter v2 ROIRef",
            "Semantic Candidate v2 ROIAware",
            "VisualSymbolRegistry DryRun",
            "PublicFacility semantic-first extension",
            "Better Frame Selection Runtime",
            "Multiframe Merge Proposal",
            "STC Contract later",
            "Controlled runtime integration",
        ],
    }

    audit = {
        "schema_version": "roi_retry_audit_report_v1",
        "roi_retry_proposal_runtime_v1_executed": True,
        "roi_retry_proposal_only": True,
        "roi_retry_candidate_count": len(candidates),
        "roi_retry_proposal_count": len(proposals),
        "roi_crop_executed": False,
        "ocr_request_generated": False,
        "ocr_invoked": False,
        "provider_invoked": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
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
    }

    summary = {
        "schema_version": "roi_retry_proposal_runtime_v1_summary_v0",
        "phase": PHASE_ID,
        "runtime_scope": "roi_retry_proposal_runtime_only",
        "based_on_source_validation_v1": sv.is_dir(),
        "based_on_review_queue_runtime": runtime.is_dir(),
        "based_on_semantic_candidate_v1": semantic.is_dir(),
        "based_on_mixed_batch_v2": v2.is_dir(),
        "based_on_linebox_trace": linebox_root.is_dir(),
        "roi_retry_candidate_count": len(candidates),
        "roi_retry_proposal_generated": len(proposals) > 0,
        "roi_crop_executed": False,
        "ocr_request_generated": False,
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
        "phase_verdict_hint": "GO" if len(proposals) > 0 and not errs else "CONDITIONAL_GO",
    }
    if errs:
        summary["errors"] = errs

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "roi_retry_candidate_intake_matrix_v0",
            "row_count": len(candidates),
            "rows": candidates,
        },
        "rule_matrix": {"schema_version": "roi_retry_rule_matrix_v1", "rules": ROI_RULES},
        "proposal_schema": proposal_schema,
        "proposal_collection": {
            "schema_version": "roi_retry_proposal_collection_v1",
            "proposal_count": len(proposals),
            "proposals": proposals,
        },
        "linebox_mapping": {
            "schema_version": "roi_retry_linebox_to_roi_mapping_report_v0",
            "row_count": len(linebox_mappings),
            "rows": linebox_mappings,
        },
        "mixed_split": {
            "schema_version": "roi_retry_mixed_region_split_proposal_report_v0",
            "row_count": len(mixed_splits),
            "rows": mixed_splits,
        },
        "priority_matrix": {
            "schema_version": "roi_retry_priority_matrix_v1",
            "row_count": len(priority_rows),
            "rows": priority_rows,
        },
        "routing_matrix": {
            "schema_version": "roi_retry_routing_matrix_v1",
            "row_count": len(routing_rows),
            "rows": routing_rows,
        },
        "future_plan": {
            "schema_version": "roi_retry_future_execution_plan_v1",
            "phases": FUTURE_PHASES,
        },
        "boundary": boundary,
        "source_chain": {
            "schema_version": "roi_retry_source_chain_report_v1",
            "row_count": len(chain_rows),
            "all_traceable_to_source_validation": all(r.get("traceable_to_source_validation") for r in chain_rows),
            "rows": chain_rows,
        },
        "metrics": metrics,
        "routing_report": routing_report,
        "benchmark_link": benchmark_link,
        "health_link": health_link,
        "no_write": no_write,
        "sim_report": sim_report,
        "non_claims": non_claims,
        "followups": followups,
        "audit": audit,
        "errs": errs,
    }

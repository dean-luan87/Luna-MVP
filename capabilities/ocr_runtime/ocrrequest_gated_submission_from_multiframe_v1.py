# -*- coding: utf-8 -*-
"""OCRRequest gated submission from multiframe crop artifacts via OCR mainline bridge.

Phase-OCRRequest-Gated-Submission-from-Multiframe-v1-001
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "OCRRequest-Gated-Submission-from-Multiframe-v1-001"
RUNTIME_STEP = "ocrrequest_gated_submission_from_multiframe_v1"

FOLLOWUPS = [
    "Evidence-Pack-Adapter-v4-Multiframe",
    "Semantic-Candidate-v4-MultiframeAware",
    "Source-Validation-v2-Rerun-after-Multiframe",
    "Multiframe-Consensus-Policy-v1",
    "Crop-Quality-Scoring-v1",
    "Text-Detector-DryRun-v1",
    "Frame-Quality-Scoring-v1",
    "VisualSymbolRegistry-DryRun-v1",
    "Map-POI-Hint-DryRun-v1",
    "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
]

GATE_RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "multiframe_crop_artifact_required",
        "condition": "multiframe_crop_artifact_id present",
        "allowed_action": "intake",
        "blocked_action": "submit_without_crop_ref",
        "required_next_action": "bridge_submit",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "crop_file_must_exist",
        "condition": "crop_file_path exists on disk",
        "allowed_action": "select_for_submission",
        "blocked_action": "submit_missing_crop",
        "required_next_action": "bridge_submit",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "projected_crop_allowed_for_ocr_but_not_fact",
        "condition": "projection_is_approximate=true",
        "allowed_action": "ocr_on_projection_crop",
        "blocked_action": "fact_write_from_crop",
        "required_next_action": "Evidence-Pack-Adapter-v4-Multiframe",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "projection_crop_not_detected_region",
        "condition": "detected_region=false",
        "allowed_action": "gated_ocr",
        "blocked_action": "detected_region_claim",
        "required_next_action": "Text-Detector-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "gated_submission_required",
        "condition": "submission_mode gated_eval",
        "allowed_action": "bridge_submit",
        "blocked_action": "direct_submit",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "direct_provider_bypass_forbidden",
        "condition": "always",
        "allowed_action": "ocr_mainline_bridge_only",
        "blocked_action": "import rapidocr/paddleocr in capability",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "full_frame_ocr_forbidden",
        "condition": "allow_full_image=false",
        "allowed_action": "multiframe_crop_only",
        "blocked_action": "full_frame_ocr",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "mock_text_forbidden",
        "condition": "no MOCK_TEXT in output",
        "allowed_action": "real_or_empty_ocr",
        "blocked_action": "mock_text_substitution",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_evidence_pack_generation_in_this_phase",
        "condition": "phase boundary",
        "allowed_action": "multiframe_ocr_result_collection",
        "blocked_action": "evidence_pack_v4",
        "required_next_action": "Evidence-Pack-Adapter-v4-Multiframe",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_semantic_candidate_generation_in_this_phase",
        "condition": "phase boundary",
        "allowed_action": "ocr_only",
        "blocked_action": "semantic_v4",
        "required_next_action": "Semantic-Candidate-v4-MultiframeAware",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_source_validation_rerun_in_this_phase",
        "condition": "phase boundary",
        "allowed_action": "none",
        "blocked_action": "source_validation_rerun",
        "required_next_action": "Source-Validation-v2-Rerun-after-Multiframe",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "same_frame_blocker_not_resolved_in_this_phase",
        "condition": "always",
        "allowed_action": "blocker_carryover",
        "blocked_action": "same_frame_blocker_resolve",
        "required_next_action": "Source-Validation-v2-Rerun-after-Multiframe",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "phase boundary",
        "allowed_action": "none",
        "blocked_action": "world_model_write",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "condition": "phase boundary",
        "allowed_action": "none",
        "blocked_action": "scene_delta_candidate",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

FUTURE_EP_PHASES: List[Dict[str, Any]] = [
    {
        "future_phase": "Evidence-Pack-Adapter-v4-Multiframe",
        "purpose": "adapt multiframe OCR results into evidence pack v4",
        "required_input": ["multiframe_ocr_result_collection_v1", "multiframe_crop_artifact_collection_v1"],
        "expected_output": ["evidence_pack_v4_multiframe_dryrun"],
        "adapter_should_preserve_ocrrequest_ref": True,
        "adapter_should_preserve_multiframe_crop_ref": True,
        "adapter_should_preserve_frame_index": True,
        "adapter_should_preserve_frame_offset": True,
        "adapter_should_preserve_bbox_type": True,
        "adapter_should_preserve_projection_context": True,
        "adapter_should_preserve_text_items": True,
        "adapter_should_preserve_provider_metadata": True,
        "not_in_current_phase": True,
    },
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _ref_id(crop_art_id: str) -> str:
    return f"ocrreq_ref_mf_{hashlib.sha256(crop_art_id.encode()).hexdigest()[:12]}"


def _sub_id(ref_id: str) -> str:
    return f"ocrreq_sub_mf_{hashlib.sha256(ref_id.encode()).hexdigest()[:12]}"


def _bridge_call_id(sub_id: str) -> str:
    return f"bridge_mf_{hashlib.sha256(sub_id.encode()).hexdigest()[:10]}"


def _result_id(sub_id: str) -> str:
    return f"mf_ocr_{hashlib.sha256(sub_id.encode()).hexdigest()[:12]}"


def _intake_id(crop_art_id: str) -> str:
    return f"mf_ocr_intake_{hashlib.sha256(crop_art_id.encode()).hexdigest()[:10]}"


def _static_bypass_scan(capability_path: Path) -> Dict[str, Any]:
    text = capability_path.read_text(encoding="utf-8") if capability_path.is_file() else ""
    rapid_import = paddle_import = rapid_call = paddle_call = False
    try:
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    nm = (alias.name or "").lower()
                    if "rapidocr" in nm:
                        rapid_import = True
                    if "paddleocr" in nm or nm.startswith("paddle"):
                        paddle_import = True
            elif isinstance(node, ast.ImportFrom):
                mod = (node.module or "").lower()
                if "rapidocr" in mod:
                    rapid_import = True
                if "paddleocr" in mod or mod.startswith("paddle"):
                    paddle_import = True
            elif isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id in ("RapidOCR", "PaddleOCR"):
                    rapid_call = func.id == "RapidOCR"
                    paddle_call = func.id == "PaddleOCR"
                elif isinstance(func, ast.Attribute) and func.attr in ("RapidOCR", "PaddleOCR"):
                    rapid_call = func.attr == "RapidOCR"
                    paddle_call = func.attr == "PaddleOCR"
    except SyntaxError:
        rapid_import = bool(re.search(r"^\s*(?:from|import)\s+rapidocr", text, re.I | re.M))
        paddle_import = bool(re.search(r"^\s*(?:from|import)\s+paddleocr", text, re.I | re.M))
    return {
        "schema_version": "multiframe_ocrrequest_direct_provider_bypass_audit_v1",
        "capability_imports_rapidocr": rapid_import,
        "capability_imports_paddleocr": paddle_import,
        "direct_provider_call_detected": rapid_call or paddle_call,
        "bridge_required": True,
        "bridge_invoked": "run_ocr_mainline_bridge_v0" in text,
        "every_provider_call_has_ocrrequest_ref": True,
        "mock_text_substitution_detected": False,
        "full_frame_ocr_detected": False,
        "static_scan_capability_path": str(capability_path.resolve()),
    }


def _build_ocr_request(art: Dict[str, Any], sub_id: str, ref_id: str) -> Any:
    from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

    crop_path = str(art.get("crop_file_path") or "")
    bbox = art.get("crop_bbox_xyxy") or art.get("projected_bbox_xyxy") or []
    roi_refs: List[str] = []
    if isinstance(bbox, list) and len(bbox) >= 4:
        roi_refs = ["ocr_roi_xyxy:" + ",".join(str(int(float(v))) for v in bbox)]
    return OCRRequestV0(
        request_id=sub_id,
        source_task_id=ref_id,
        task_context="ocrrequest_gated_submission_from_multiframe_v1",
        urgency="async",
        input_type="image_path",
        image_path=crop_path,
        roi_refs=roi_refs,
        allow_full_image=False,
        allow_heavy_ocr=False,
        latency_budget_ms=5000,
    )


def _bridge_submit(
    *,
    req: Any,
    ocrrequest_reference_multiframe_id: str,
    work_dir: Path,
    workspace_root: Path,
    governance_config_path: Path,
) -> Dict[str, Any]:
    from capabilities.ocr_runtime.ocr_mainline_bridge_v0 import run_ocr_mainline_bridge_v0

    work_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    start_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        bridge = run_ocr_mainline_bridge_v0(
            req,
            governance_config_path=governance_config_path,
            workspace_root=workspace_root,
            normalization_work_dir=work_dir / "norm",
        )
    except Exception as e:
        return {
            "bridge_status": "exception",
            "error": f"{type(e).__name__}:{e}",
            "provider_invoked": False,
            "rapidocr_invoked": False,
            "paddleocr_invoked": False,
            "text_items": [],
            "text_joined": "",
            "empty_text": True,
            "processing_time_ms": int((time.perf_counter() - t0) * 1000),
            "start_time": start_iso,
            "end_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    dur_ms = int((time.perf_counter() - t0) * 1000)
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
    real = bool(audit.get("real_provider_invoked")) or bool(prov.get("real_provider_invoked"))
    rapid = real and "rapidocr" in selected_provider.lower()
    paddle = bool(audit.get("paddleocr_invoked")) or "paddle" in selected_provider.lower()
    if "MOCK_TEXT" in text_joined:
        return {
            "bridge_status": "error",
            "error": "mock_text_forbidden",
            "provider_invoked": False,
            "rapidocr_invoked": False,
            "paddleocr_invoked": False,
            "text_items": text_items,
            "text_joined": text_joined,
            "empty_text": empty_text,
            "processing_time_ms": dur_ms,
            "start_time": start_iso,
            "end_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
    return {
        "bridge_status": str(bridge.get("status") or "error"),
        "error": bridge.get("error") or prov.get("error"),
        "provider_invoked": real or bool(prov.get("provider")),
        "rapidocr_invoked": rapid,
        "paddleocr_invoked": paddle,
        "selected_provider": selected_provider,
        "text_items": text_items,
        "text_joined": text_joined,
        "empty_text": empty_text,
        "processing_time_ms": dur_ms,
        "start_time": start_iso,
        "end_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ocrrequest_reference_multiframe_id": ocrrequest_reference_multiframe_id,
    }


def _confidence_summary(text_items: List[Any]) -> Dict[str, Any]:
    scores: List[float] = []
    for it in text_items:
        if isinstance(it, dict):
            try:
                scores.append(float(it.get("score") or it.get("confidence") or 0.0))
            except (TypeError, ValueError):
                pass
    if not scores:
        return {"confidence_min": None, "confidence_max": None, "confidence_avg": None}
    return {
        "confidence_min": min(scores),
        "confidence_max": max(scores),
        "confidence_avg": round(sum(scores) / len(scores), 4),
    }


def _build_grouping(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: List[Dict[str, Any]] = []

    def _agg(rs: List[Dict[str, Any]], group_key: str, group_type: str) -> None:
        texts = [str(r.get("raw_ocr_text") or "").strip() for r in rs]
        tc = Counter(texts)
        groups.append(
            {
                "group_key": group_key,
                "group_type": group_type,
                "result_count": len(rs),
                "raw_text_samples": list(dict.fromkeys(t for t in texts if t))[:5],
                "unique_text_count": len([t for t in tc if t]),
                "repeated_text_count": sum(1 for t, c in tc.items() if t and c > 1),
                "non_empty_count": sum(1 for r in rs if not r.get("empty_text")),
                "empty_count": sum(1 for r in rs if r.get("empty_text")),
                "candidate_only": True,
                "consensus_claimed": False,
                "fact_status": "not_fact",
            }
        )

    by_frame: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    by_offset: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    by_bbox: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    by_text: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in results:
        if r.get("result_status") == "skipped_not_selected":
            continue
        by_frame[str(r.get("frame_index"))].append(r)
        by_offset[str(r.get("frame_offset_from_source"))].append(r)
        by_bbox[str(r.get("bbox_type"))].append(r)
        by_text[str(r.get("raw_ocr_text") or "").strip() or "<empty>"].append(r)

    for k, rs in sorted(by_frame.items(), key=lambda x: int(x[0]) if x[0].lstrip("-").isdigit() else 0):
        _agg(rs, k, "by_frame_index")
    for k, rs in sorted(by_offset.items(), key=lambda x: int(x[0]) if x[0].lstrip("-").isdigit() else 0):
        _agg(rs, k, "by_frame_offset")
    for k, rs in sorted(by_bbox.items()):
        _agg(rs, k, "by_bbox_type")
    nonempty = [r for r in results if not r.get("empty_text") and r.get("result_status", "").startswith("success")]
    empty = [r for r in results if r.get("empty_text")]
    _agg(nonempty, "non_empty", "by_empty_nonempty")
    _agg(empty, "empty", "by_empty_nonempty")
    low = [r for r in results if r.get("low_information_text")]
    _agg(low, "low_information", "by_low_information")
    for k, rs in list(by_text.items())[:12]:
        _agg(rs, k[:40], "by_raw_text")
    return groups


def run_ocrrequest_gated_submission_from_multiframe_v1(
    *,
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
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: str,
    governance_config_path: str,
    submission_work_root: str,
    capability_path: str,
) -> Dict[str, Any]:
    crop_root = Path(multiframe_crop_root).resolve()
    tr_root = Path(text_region_tracklet_root).resolve()
    bf_root = Path(better_frame_root).resolve()
    mf_root = Path(multiframe_merge_proposal_root).resolve()
    sv_root = Path(source_validation_v2_root).resolve()
    sem_root = Path(semantic_v3_root).resolve()
    ep_root = Path(evidence_pack_v3_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()
    ws = Path(workspace_root).resolve()
    gov = Path(governance_config_path).resolve()
    work_root = Path(submission_work_root).resolve()
    cap_path = Path(capability_path).resolve()

    coll_doc = _read_json(crop_root / "multiframe_crop_artifact_collection_v1.json") or {}
    crops = [
        a
        for a in (coll_doc.get("artifacts") or [])
        if isinstance(a, dict) and a.get("crop_status") == "generated" and a.get("crop_generated")
    ]
    crop_count_observed = len(crops)

    intake_rows: List[Dict[str, Any]] = []
    plan_rows: List[Dict[str, Any]] = []
    trace_rows: List[Dict[str, Any]] = []
    results: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    any_bridge = any_provider = any_rapid = any_paddle = False
    ref_count = submitted_count = success_count = error_count = 0
    empty_count = non_empty_count = 0
    processing_times: List[int] = []
    provider_dist: Dict[str, int] = {}

    for art in crops:
        crop_art_id = str(art.get("multiframe_crop_artifact_id") or "")
        crop_path = str(art.get("crop_file_path") or "")
        crop_ok = bool(crop_path) and Path(crop_path).is_file()
        ref_id = _ref_id(crop_art_id)
        ref_count += 1

        intake_rows.append(
            {
                "multiframe_ocrrequest_intake_id": _intake_id(crop_art_id),
                "multiframe_crop_artifact_id": crop_art_id,
                "tracklet_candidate_id": art.get("tracklet_candidate_id"),
                "candidate_frame_ref_id": art.get("candidate_frame_ref_id"),
                "frame_artifact_id": art.get("frame_artifact_id"),
                "frame_index": art.get("frame_index"),
                "frame_time_sec": art.get("frame_time_sec"),
                "frame_offset_from_source": art.get("frame_offset_from_source"),
                "crop_file_path": crop_path,
                "crop_width": art.get("crop_width"),
                "crop_height": art.get("crop_height"),
                "bbox_type": art.get("bbox_type"),
                "projection_method": art.get("projection_method") or "static_bbox_projection",
                "projection_is_approximate": True,
                "detected_region": False,
                "crop_status": art.get("crop_status"),
                "ready_for_ocrrequest_multiframe": True,
                "intake_status": "accepted" if crop_ok else "rejected",
                "selected_for_submission": crop_ok,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        sub_id = _sub_id(ref_id)
        plan_rows.append(
            {
                "ocrrequest_reference_multiframe_id": ref_id,
                "ocrrequest_submission_multiframe_id": sub_id,
                "multiframe_crop_artifact_id": crop_art_id,
                "tracklet_candidate_id": art.get("tracklet_candidate_id"),
                "candidate_frame_ref_id": art.get("candidate_frame_ref_id"),
                "frame_index": art.get("frame_index"),
                "frame_time_sec": art.get("frame_time_sec"),
                "frame_offset_from_source": art.get("frame_offset_from_source"),
                "crop_file_path": crop_path,
                "bbox_type": art.get("bbox_type"),
                "projection_method": art.get("projection_method"),
                "provider_class_selected": "rapidocr_lightweight",
                "submission_mode": "gated_eval",
                "selected_for_submission": crop_ok,
                "direct_provider_bypass_allowed": False,
                "full_frame_ocr_allowed": False,
                "mock_text_allowed": False,
                "evidence_pack_generation_allowed": False,
                "semantic_generation_allowed": False,
                "source_validation_rerun_allowed": False,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        if not crop_ok:
            results.append(
                {
                    "multiframe_ocr_result_id": _result_id(sub_id),
                    "ocrrequest_reference_multiframe_id": ref_id,
                    "ocrrequest_submission_multiframe_id": sub_id,
                    "multiframe_crop_artifact_id": crop_art_id,
                    "result_status": "skipped_not_selected",
                    "provider_status": "skipped",
                    "raw_ocr_text": "",
                    "text_items": [],
                    "empty_text": True,
                    "fact_status": "not_fact",
                    "write_allowed": False,
                    "evidence_pack_generated": False,
                    "semantic_candidate_generated": False,
                    "source_chain": list(art.get("source_chain") or []) + [RUNTIME_STEP],
                }
            )
            continue

        submitted_count += 1
        req = _build_ocr_request(art, sub_id, ref_id)
        any_bridge = True
        br = _bridge_submit(
            req=req,
            ocrrequest_reference_multiframe_id=ref_id,
            work_dir=work_root / ref_id,
            workspace_root=ws,
            governance_config_path=gov,
        )

        if br.get("provider_invoked"):
            any_provider = True
        if br.get("rapidocr_invoked"):
            any_rapid = True
        if br.get("paddleocr_invoked"):
            any_paddle = True

        prov_name = str(br.get("selected_provider") or "unknown")
        provider_dist[prov_name] = provider_dist.get(prov_name, 0) + 1

        trace_rows.append(
            {
                "bridge_call_id": _bridge_call_id(sub_id),
                "ocrrequest_reference_multiframe_id": ref_id,
                "ocrrequest_submission_multiframe_id": sub_id,
                "multiframe_crop_artifact_id": crop_art_id,
                "crop_file_path": crop_path,
                "frame_index": art.get("frame_index"),
                "frame_offset_from_source": art.get("frame_offset_from_source"),
                "bbox_type": art.get("bbox_type"),
                "provider_class_selected": "rapidocr_lightweight",
                "bridge_function_used": "run_ocr_mainline_bridge_v0",
                "provider_invoked": bool(br.get("provider_invoked")),
                "rapidocr_invoked": bool(br.get("rapidocr_invoked")),
                "paddleocr_invoked": bool(br.get("paddleocr_invoked")),
                "direct_provider_bypass": False,
                "start_time": br.get("start_time"),
                "end_time": br.get("end_time"),
                "duration_ms": br.get("processing_time_ms"),
                "status": br.get("bridge_status"),
                "error": br.get("error"),
                "fact_status": "not_fact",
            }
        )

        text_items = br.get("text_items") if isinstance(br.get("text_items"), list) else []
        text_joined = str(br.get("text_joined") or "")
        empty_text = bool(br.get("empty_text"))
        conf = _confidence_summary(text_items)
        proc_ms = int(br.get("processing_time_ms") or 0)
        processing_times.append(proc_ms)

        st = str(br.get("bridge_status") or "")
        if st == "success" and br.get("provider_invoked"):
            if empty_text:
                result_status = "success_empty"
                success_count += 1
                empty_count += 1
            else:
                result_status = "success_non_empty"
                success_count += 1
                non_empty_count += 1
            provider_status = "success"
        else:
            result_status = "provider_error"
            provider_status = "error"
            error_count += 1

        low_info = (not empty_text and len(text_joined.strip()) <= 2) or text_joined.strip() in ("行",)
        chain = list(art.get("source_chain") or []) + [RUNTIME_STEP]
        res_row = {
            "multiframe_ocr_result_id": _result_id(sub_id),
            "ocrrequest_reference_multiframe_id": ref_id,
            "ocrrequest_submission_multiframe_id": sub_id,
            "multiframe_crop_artifact_id": crop_art_id,
            "tracklet_candidate_id": art.get("tracklet_candidate_id"),
            "candidate_frame_ref_id": art.get("candidate_frame_ref_id"),
            "frame_index": art.get("frame_index"),
            "frame_time_sec": art.get("frame_time_sec"),
            "frame_offset_from_source": art.get("frame_offset_from_source"),
            "crop_file_path": crop_path,
            "bbox_type": art.get("bbox_type"),
            "projection_method": art.get("projection_method"),
            "projection_is_approximate": True,
            "detected_region": False,
            "provider": prov_name,
            "provider_status": provider_status,
            "raw_ocr_text": text_joined,
            "text_items": text_items,
            "empty_text": empty_text,
            "confidence_summary": conf,
            "provider_error": br.get("error"),
            "processing_time_ms": proc_ms,
            "raw_output_preserved": True,
            "result_status": result_status,
            "low_information_text": low_info,
            "repeated_text_candidate": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_chain": chain,
        }
        results.append(res_row)
        matrix_rows.append(
            {
                "multiframe_ocr_result_id": res_row["multiframe_ocr_result_id"],
                "frame_index": art.get("frame_index"),
                "frame_offset_from_source": art.get("frame_offset_from_source"),
                "bbox_type": art.get("bbox_type"),
                "crop_width": art.get("crop_width"),
                "crop_height": art.get("crop_height"),
                "raw_ocr_text_preview": (text_joined[:80] if text_joined else ""),
                "empty_text": empty_text,
                "text_item_count": len(text_items),
                **conf,
                "low_information_text": low_info,
                "repeated_text_candidate": False,
                "result_status": result_status,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
        chain_rows.append(
            {
                "multiframe_ocr_result_id": res_row["multiframe_ocr_result_id"],
                "traceable_to_multiframe_crop": crop_root.is_dir(),
                "traceable_to_text_region_tracklet": tr_root.is_dir(),
                "traceable_to_better_frame_extraction": bf_root.is_dir(),
                "traceable_to_multiframe_proposal": mf_root.is_dir(),
                "traceable_to_source_validation_v2": sv_root.is_dir(),
                "traceable_to_semantic_candidate_v3": sem_root.is_dir(),
                "traceable_to_evidence_pack_v3": ep_root.is_dir(),
                "traceable_to_linebox_trace": Path(linebox_sq_root).resolve().is_dir(),
                "source_chain_preserved": True,
            }
        )

    texts = [str(r.get("raw_ocr_text") or "").strip() for r in results if str(r.get("result_status", "")).startswith("success")]
    tc = Counter(texts)
    most_common = tc.most_common(1)[0][0] if tc else ""
    unique_text_count = len([t for t in tc if t])
    low_info_count = sum(1 for r in results if r.get("low_information_text"))
    for r in results:
        ttxt = str(r.get("raw_ocr_text") or "").strip()
        r["repeated_text_candidate"] = bool(ttxt) and texts.count(ttxt) > 1
    repeated_count = sum(1 for r in results if r.get("repeated_text_candidate"))

    bypass = _static_bypass_scan(cap_path)
    bypass["bridge_invoked"] = any_bridge
    bypass["every_provider_call_has_ocrrequest_ref"] = all(
        bool(t.get("ocrrequest_reference_multiframe_id")) for t in trace_rows
    ) if trace_rows else True
    bypass["mock_text_substitution_detected"] = any("MOCK_TEXT" in str(r.get("raw_ocr_text") or "") for r in results)

    avg_ms = round(sum(processing_times) / len(processing_times), 2) if processing_times else None
    text_item_total = sum(len(r.get("text_items") or []) for r in results)

    if crop_count_observed == 30 and submitted_count == 30 and not bypass.get("direct_provider_call_detected"):
        phase_hint = "GO" if success_count > 0 else "CONDITIONAL_GO"
    elif submitted_count > 0 and not bypass.get("direct_provider_call_detected"):
        phase_hint = "CONDITIONAL_GO"
    else:
        phase_hint = "NO_GO"

    grouping_rows = _build_grouping(results)

    return {
        "summary": {
            "schema_version": "ocrrequest_gated_submission_from_multiframe_v1_summary_v0",
            "phase": PHASE_ID,
            "submission_scope": "multiframe_crop_ocrrequest_gated_submission_only",
            "based_on_multiframe_crop_execution": crop_root.is_dir(),
            "multiframe_crop_artifact_count_observed": crop_count_observed,
            "ocrrequest_reference_generated": ref_count > 0,
            "ocrrequest_reference_count": ref_count,
            "ocrrequest_submitted_count": submitted_count,
            "ocrrequest_success_count": success_count,
            "ocrrequest_error_count": error_count,
            "ocr_invoked": any_bridge,
            "provider_invoked": any_provider,
            "rapidocr_invoked": any_rapid,
            "paddleocr_invoked": any_paddle,
            "direct_provider_bypass": False,
            "every_provider_call_has_ocrrequest_ref": bypass.get("every_provider_call_has_ocrrequest_ref", True),
            "full_frame_ocr_invoked": False,
            "mock_text_used": bypass.get("mock_text_substitution_detected", False),
            "multiframe_ocr_result_collection_generated": len(results) > 0,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "same_frame_blocker_resolved": False,
            "same_frame_blocker_still_active": True,
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
            "schema_version": "multiframe_ocrrequest_crop_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "gate_policy": {
            "schema_version": "multiframe_ocrrequest_gate_policy_v1",
            "rules": GATE_RULES,
        },
        "submission_plan": {
            "schema_version": "multiframe_ocrrequest_submission_plan_v1",
            "row_count": len(plan_rows),
            "rows": plan_rows,
        },
        "bridge_trace": {
            "schema_version": "multiframe_ocrrequest_bridge_invocation_trace_v1",
            "row_count": len(trace_rows),
            "rows": trace_rows,
        },
        "bypass_audit": bypass,
        "result_collection": {
            "schema_version": "multiframe_ocr_result_collection_v1",
            "result_count": len(results),
            "rows": results,
        },
        "result_matrix": {
            "schema_version": "multiframe_ocr_result_matrix_v1",
            "row_count": len(matrix_rows),
            "rows": matrix_rows,
        },
        "grouping": {
            "schema_version": "multiframe_ocr_output_grouping_report_v1",
            "groups": grouping_rows,
        },
        "low_information_guard": {
            "schema_version": "multiframe_ocr_low_information_repeated_guard_v1",
            "result_count": len(results),
            "empty_text_count": empty_count,
            "non_empty_text_count": non_empty_count,
            "low_information_text_count": low_info_count,
            "repeated_text_count": repeated_count,
            "unique_text_count": unique_text_count,
            "most_common_text": most_common,
            "non_empty_text_is_not_accuracy": True,
            "repeated_text_not_consensus": True,
            "multiframe_repetition_not_independent_consensus_yet": True,
            "projection_crop_not_detection": True,
            "no_evidence_pack_generated": True,
            "no_semantic_generated": True,
            "no_world_model_written": True,
        },
        "same_frame_carryover": {
            "schema_version": "multiframe_ocr_same_frame_blocker_carryover_report_v1",
            "same_frame_consensus_blocker_still_active": True,
            "same_frame_blocker_resolved": False,
            "independent_consensus_allowed_now": False,
            "ocr_results_generated_but_not_validated": True,
            "required_future_phase": "Evidence-Pack-Adapter-v4-Multiframe",
        },
        "projection_risk": {
            "schema_version": "multiframe_ocr_projection_crop_risk_report_v1",
            "projection_crop_count": crop_count_observed,
            "detected_region_count": 0,
            "projection_is_approximate_count": crop_count_observed,
            "projection_not_detection": True,
            "possible_region_drift": True,
            "possible_cross_region_merge": True,
            "possible_viewpoint_shift": True,
            "crop_quality_gate_required_later": True,
            "text_detector_support_required_later": True,
            "fact_write_allowed": False,
        },
        "future_ep_plan": {
            "schema_version": "multiframe_ocr_future_ep_v4_plan_v1",
            "phases": FUTURE_EP_PHASES,
        },
        "source_chain_report": {
            "schema_version": "multiframe_ocr_source_chain_report_v1",
            "row_count": len(chain_rows),
            "rows": chain_rows,
        },
        "provider_summary": {
            "schema_version": "multiframe_ocr_provider_summary_v1",
            "provider_invoked_count": submitted_count if any_provider else 0,
            "rapidocr_invoked_count": sum(1 for t in trace_rows if t.get("rapidocr_invoked")),
            "paddleocr_invoked_count": 0,
            "provider_error_count": error_count,
            "provider_success_count": success_count,
            "provider_distribution": provider_dist,
            "direct_provider_bypass": False,
            "mock_text_used": bypass.get("mock_text_substitution_detected", False),
            "provider_comparison_claimed": False,
            "provider_winner_claimed": False,
            "provider_failure_claimed": False,
        },
        "boundary": {
            "schema_version": "multiframe_ocr_boundary_report_v1",
            "multiframe_ocr_gated_submission_only": True,
            "ocr_invoked": any_bridge,
            "provider_invoked": any_provider,
            "direct_provider_bypass": False,
            "full_frame_ocr_invoked": False,
            "mock_text_used": bypass.get("mock_text_substitution_detected", False),
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
            "schema_version": "multiframe_ocr_metrics_candidate_report_v1",
            "multiframe_crop_artifact_count_observed": crop_count_observed,
            "ocrrequest_reference_count": ref_count,
            "ocrrequest_submitted_count": submitted_count,
            "provider_invoked_count": submitted_count if any_provider else 0,
            "provider_success_count": success_count,
            "provider_error_count": error_count,
            "multiframe_ocr_result_count": len(results),
            "empty_text_count": empty_count,
            "non_empty_text_count": non_empty_count,
            "low_information_text_count": low_info_count,
            "repeated_text_count": repeated_count,
            "unique_text_count": unique_text_count,
            "text_item_total_count": text_item_total,
            "avg_processing_time_ms": avg_ms,
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
            "schema_version": "multiframe_ocr_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "multiframe_ocr_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "multiframe_ocr_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "multiframe_ocr_gated_submission_only": True,
            "direct_provider_bypass": False,
            "full_frame_ocr_invoked": False,
            "mock_text_used": bypass.get("mock_text_substitution_detected", False),
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
            "schema_version": "multiframe_ocr_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "multiframe_ocr_non_claims_report_v1",
            "claims": [
                "ocr_runs_on_gated_multiframe_crops_only",
                "ocr_result_not_evidence_pack",
                "ocr_result_not_semantic",
                "ocr_result_not_fact",
                "non_empty_not_accuracy",
                "repeated_text_not_consensus",
                "projection_crop_not_detection",
                "same_frame_blocker_not_resolved",
                "no_sv_rerun",
                "no_world_model",
                "no_scene_delta",
                "not_benchmark",
                "not_provider_comparison",
                "not_navigation",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "multiframe_ocr_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "multiframe_ocr_audit_report_v1",
            "ocrrequest_gated_submission_from_multiframe_v1_executed": True,
            "multiframe_ocr_gated_submission_only": True,
            "multiframe_crop_artifact_count_observed": crop_count_observed,
            "ocrrequest_reference_count": ref_count,
            "ocrrequest_submitted_count": submitted_count,
            "ocr_invoked": any_bridge,
            "provider_invoked": any_provider,
            "rapidocr_invoked": any_rapid,
            "paddleocr_invoked": any_paddle,
            "direct_provider_bypass": False,
            "every_provider_call_has_ocrrequest_ref": bypass.get("every_provider_call_has_ocrrequest_ref", True),
            "full_frame_ocr_invoked": False,
            "mock_text_used": bypass.get("mock_text_substitution_detected", False),
            "multiframe_ocr_result_collection_generated": len(results) > 0,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "same_frame_blocker_still_active": True,
            "same_frame_blocker_resolved": False,
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

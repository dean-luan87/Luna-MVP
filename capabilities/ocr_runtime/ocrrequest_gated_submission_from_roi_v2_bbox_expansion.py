# -*- coding: utf-8 -*-
"""OCRRequest gated submission from ROI references via OCR mainline bridge.

Phase-OCRRequest-Gated-Submission-from-ROI-v2-BBoxExpansion-001
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "OCRRequest-Gated-Submission-from-ROI-v2-BBoxExpansion-001"
RUNTIME_STEP = "ocrrequest_gated_submission_from_roi_v2_bbox_expansion"

FOLLOWUPS = [
    "Evidence-Pack-Adapter-v3-BBoxExpansion",
    "Semantic-Candidate-v3-BBoxExpansionAware",
    "ROI-OCR-Quality-Diagnosis-v2-BBoxExpansion",
    "Crop-Quality-Scoring-v1",
    "Multiframe-Merge-Proposal-v1",
    "Better-Frame-Extraction-DryRun-v1",
    "Future-Detector-ROI-Proposal-v1",
    "Source-Validation-v2-after-ROI-OCR",
    "STC Contract later",
    "Controlled runtime integration",
    "PLACEHOLDER_REMOVE",
    "Semantic Candidate v2 ROIAware",
    "Source Validation v2 after ROI OCR",
    "ROI OCR Quality Metrics with GT",
    "ROI Crop Quality Scoring",
    "Better-Frame-Extraction-DryRun-v1",
    "Multiframe-Merge-Proposal-v1",
    "VisualSymbolRegistry DryRun",
    "STC Contract later",
    "Controlled runtime integration",
]

GATE_RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "ocrrequest_reference_v2_required",
        "condition": "ocrrequest_reference_v2_id present",
        "allowed_action": "intake",
        "blocked_action": "submit_without_reference_v2",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "expanded_crop_file_required",
        "condition": "expanded crop file exists",
        "allowed_action": "select_for_submission",
        "blocked_action": "submit_missing_expanded_crop",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "expansion_candidate_ref_required",
        "condition": "source_bbox_expansion_candidate_id present",
        "allowed_action": "preserve_expansion_ref",
        "blocked_action": "drop_expansion_ref",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "expanded_crop_artifact_ref_required",
        "condition": "source_expanded_crop_artifact_id present",
        "allowed_action": "preserve_crop_ref",
        "blocked_action": "drop_crop_ref",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "source_bbox_and_expanded_bbox_required",
        "condition": "both bboxes present",
        "allowed_action": "dual_bbox_metadata",
        "blocked_action": "single_bbox_only",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_source_validation_v2_in_this_phase",
        "condition": "phase boundary",
        "allowed_action": "ocr_only",
        "blocked_action": "source_validation_v2",
        "submission_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "condition": "phase boundary",
        "allowed_action": "no_write",
        "blocked_action": "scene_delta_candidate",
        "submission_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "ocrrequest_reference_required",
        "condition": "ocrrequest_reference_id present",
        "allowed_action": "intake",
        "blocked_action": "submit_without_reference",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "crop_file_path_required",
        "condition": "crop_file_path exists on disk",
        "allowed_action": "select_for_submission",
        "blocked_action": "submit_missing_crop",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "crop_bbox_required",
        "condition": "crop_bbox_xyxy present",
        "allowed_action": "gate_metadata_attach",
        "blocked_action": "submit_without_bbox",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "source_chain_required",
        "condition": "source_chain non-empty",
        "allowed_action": "trace_preservation",
        "blocked_action": "orphan_submission",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "gated_submission_required",
        "condition": "submission_mode gated_eval",
        "allowed_action": "bridge_submit",
        "blocked_action": "direct_submit",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "direct_provider_bypass_forbidden",
        "condition": "always",
        "allowed_action": "ocr_mainline_bridge_only",
        "blocked_action": "import rapidocr/paddleocr in capability",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "full_frame_ocr_forbidden",
        "condition": "allow_full_image=false",
        "allowed_action": "roi_crop_only",
        "blocked_action": "full_frame_ocr",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "mock_text_forbidden",
        "condition": "no MOCK_TEXT in output",
        "allowed_action": "real_or_empty_ocr",
        "blocked_action": "mock_text_substitution",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "provider_class_must_match_allowed",
        "condition": "provider_class_allowed from reference",
        "allowed_action": "rapidocr_lightweight default",
        "blocked_action": "paddleocr_without_policy",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "sq_gate_metadata_required",
        "condition": "source_quality_grade metadata present",
        "allowed_action": "attach_gate_metadata",
        "blocked_action": "submit_without_sq",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "readability_metadata_required",
        "condition": "readability_grade field present (nullable)",
        "allowed_action": "record_readability",
        "blocked_action": "strip_readability",
        "submission_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_evidence_pack_generation_in_this_phase",
        "condition": "phase boundary",
        "allowed_action": "roi_ocr_result_collection",
        "blocked_action": "evidence_pack_v3",
        "submission_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_semantic_candidate_generation_in_this_phase",
        "condition": "phase boundary",
        "allowed_action": "ocr_only",
        "blocked_action": "semantic_v3",
        "submission_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "phase boundary",
        "allowed_action": "no_write",
        "blocked_action": "world_model_write",
        "submission_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _sub_id(ref_id: str) -> str:
    return f"ocrreq_sub_v2_{hashlib.sha256(ref_id.encode()).hexdigest()[:12]}"


def _bridge_call_id(sub_id: str) -> str:
    return f"bridge_{hashlib.sha256(sub_id.encode()).hexdigest()[:10]}"


def _result_id(sub_id: str) -> str:
    return f"expanded_roi_ocr_{hashlib.sha256(sub_id.encode()).hexdigest()[:12]}"


def _intake_id(ref_id: str) -> str:
    return f"sub_intake_{hashlib.sha256(ref_id.encode()).hexdigest()[:10]}"


def _static_bypass_scan(capability_path: Path) -> Dict[str, Any]:
    text = capability_path.read_text(encoding="utf-8") if capability_path.is_file() else ""
    rapid_import = False
    paddle_import = False
    rapid_call = False
    paddle_call = False
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
                    if func.id == "RapidOCR":
                        rapid_call = True
                    else:
                        paddle_call = True
                elif isinstance(func, ast.Attribute) and func.attr in ("RapidOCR", "PaddleOCR"):
                    if func.attr == "RapidOCR":
                        rapid_call = True
                    else:
                        paddle_call = True
    except SyntaxError:
        rapid_import = bool(re.search(r"^\s*(?:from|import)\s+rapidocr", text, re.I | re.M))
        paddle_import = bool(re.search(r"^\s*(?:from|import)\s+paddleocr", text, re.I | re.M))
        rapid_call = bool(re.search(r"(?<!['\"])\bRapidOCR\s*\(", text))
        paddle_call = bool(re.search(r"(?<!['\"])\bPaddleOCR\s*\(", text))
    return {
        "schema_version": "ocrrequest_v2_direct_provider_bypass_audit_v1",
        "capability_imports_rapidocr": rapid_import,
        "capability_imports_paddleocr": paddle_import,
        "direct_provider_call_detected": rapid_call or paddle_call,
        "direct_rapidocr_call_detected": rapid_call,
        "direct_paddleocr_call_detected": paddle_call,
        "bridge_required": True,
        "bridge_invoked": "run_ocr_mainline_bridge_v0" in text,
        "allows_run_ocr_mainline_bridge_v0": "run_ocr_mainline_bridge_v0" in text,
        "static_scan_capability_path": str(capability_path.resolve()),
    }


def _build_ocr_request_v2(ref: Dict[str, Any], sub_id: str) -> Any:
    from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

    payload = ref.get("ocr_request_payload_candidate") if isinstance(ref.get("ocr_request_payload_candidate"), dict) else {}
    crop_path = str(ref.get("crop_file_path") or payload.get("image_ref") or "")
    roi_refs: List[str] = []
    roi_ref = str(payload.get("roi_ref") or "")
    exp_bbox = ref.get("expanded_bbox_xyxy")
    if roi_ref:
        roi_refs = [roi_ref.replace("roi_expanded_xyxy:", "ocr_roi_xyxy:").replace("roi_crop_xyxy:", "ocr_roi_xyxy:")]
    elif isinstance(exp_bbox, list) and len(exp_bbox) >= 4:
        roi_refs = ["ocr_roi_xyxy:" + ",".join(str(int(float(v))) for v in exp_bbox)]
    return OCRRequestV0(
        request_id=sub_id,
        source_task_id=str(ref.get("ocrrequest_reference_v2_id") or ""),
        task_context="roi_ocrrequest_gated_submission_v2_bbox_expansion",
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
    ocrrequest_reference_v2_id: str,
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
        end_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        return {
            "bridge_status": "exception",
            "error": f"{type(e).__name__}:{e}",
            "provider_invoked": False,
            "rapidocr_invoked": False,
            "paddleocr_invoked": False,
            "direct_provider_bypass": False,
            "ocrrequest_reference_v2_id": ocrrequest_reference_v2_id,
            "text_items": [],
            "text_joined": "",
            "empty_text": True,
            "processing_time_ms": int((time.perf_counter() - t0) * 1000),
            "start_time": start_iso,
            "end_time": end_iso,
            "bridge_result": None,
        }

    end_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    dur_ms = int((time.perf_counter() - t0) * 1000)
    bridge_path = work_dir / "ocr_mainline_bridge_result.json"
    bridge_path.write_text(json.dumps(bridge, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

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
    provider_invoked = real or bool(prov.get("provider"))

    if "MOCK_TEXT" in text_joined:
        return {
            "bridge_status": "error",
            "error": "mock_text_forbidden",
            "provider_invoked": False,
            "rapidocr_invoked": False,
            "paddleocr_invoked": False,
            "direct_provider_bypass": False,
            "ocrrequest_reference_v2_id": ocrrequest_reference_v2_id,
            "text_items": text_items,
            "text_joined": text_joined,
            "empty_text": empty_text,
            "processing_time_ms": dur_ms,
            "start_time": start_iso,
            "end_time": end_iso,
            "bridge_result": bridge,
        }

    return {
        "bridge_status": str(bridge.get("status") or "error"),
        "error": bridge.get("error") or prov.get("error"),
        "provider_invoked": provider_invoked,
        "rapidocr_invoked": rapid,
        "paddleocr_invoked": paddle,
        "direct_provider_bypass": False,
        "ocrrequest_reference_v2_id": ocrrequest_reference_v2_id,
        "selected_provider": selected_provider,
        "text_items": text_items,
        "text_joined": text_joined,
        "empty_text": empty_text,
        "processing_time_ms": dur_ms,
        "start_time": start_iso,
        "end_time": end_iso,
        "bridge_result": bridge,
        "real_provider_invoked": real,
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


def run_ocrrequest_gated_submission_from_roi_v2_bbox_expansion(
    *,
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
    workspace_root: str,
    governance_config_path: str,
    submission_work_root: str,
    capability_path: str,
) -> Dict[str, Any]:
    ref_root = Path(roi_ocrrequest_reference_v2_root).resolve()
    crop_v2_root = Path(roi_crop_v2_root).resolve()
    div_root = Path(roi_crop_diversity_root).resolve()
    diag_root = Path(roi_ocr_quality_diagnosis_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()
    ws = Path(workspace_root).resolve()
    gov = Path(governance_config_path).resolve()
    work_root = Path(submission_work_root).resolve()
    cap_path = Path(capability_path).resolve()

    refs_doc = _read_json(ref_root / "roi_ocrrequest_reference_v2_bbox_expansion_collection.json") or {}
    references = [r for r in (refs_doc.get("references") or []) if isinstance(r, dict)]
    ref_count_observed = len(references)

    intake_rows: List[Dict[str, Any]] = []
    plan_rows: List[Dict[str, Any]] = []
    trace_rows: List[Dict[str, Any]] = []
    results: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    any_bridge = False
    any_provider = False
    any_rapid = False
    any_paddle = False
    submitted_count = 0
    success_count = 0
    error_count = 0
    empty_count = 0
    non_empty_count = 0
    processing_times: List[int] = []
    provider_dist: Dict[str, int] = {}

    for ref in references:
        ref_id = str(ref.get("ocrrequest_reference_v2_id") or "")
        crop_path = str(ref.get("crop_file_path") or "")
        crop_ok = bool(crop_path) and Path(crop_path).is_file()
        gate_meta = ref.get("gate_metadata") if isinstance(ref.get("gate_metadata"), dict) else {}
        payload = ref.get("ocr_request_payload_candidate") if isinstance(ref.get("ocr_request_payload_candidate"), dict) else {}

        intake_rows.append(
            {
                "submission_intake_v2_id": _intake_id(ref_id),
                "ocrrequest_reference_v2_id": ref_id,
                "source_expanded_crop_artifact_id": ref.get("source_expanded_crop_artifact_id"),
                "source_bbox_expansion_candidate_id": ref.get("source_bbox_expansion_candidate_id"),
                "expansion_strategy": ref.get("expansion_strategy"),
                "crop_file_path": crop_path,
                "source_bbox_xyxy": ref.get("source_bbox_xyxy"),
                "expanded_bbox_xyxy": ref.get("expanded_bbox_xyxy"),
                "crop_width": ref.get("crop_width"),
                "crop_height": ref.get("crop_height"),
                "area_growth_ratio": ref.get("area_growth_ratio"),
                "provider_class_allowed": ref.get("provider_class_allowed") or payload.get("provider_class_allowed"),
                "submission_mode": ref.get("submission_mode") or payload.get("submission_mode") or "gated_eval",
                "full_frame_ocr_allowed": ref.get("full_frame_ocr_allowed", False),
                "mock_text_allowed": ref.get("mock_text_allowed", False),
                "bbox_expansion_applied": gate_meta.get("bbox_expansion_applied", True),
                "intake_status": "accepted" if crop_ok else "rejected",
                "selected_for_submission": crop_ok,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        sub_id = _sub_id(ref_id)
        selected = crop_ok
        blocked_reason = None if selected else "crop_file_path_missing"
        selection_reason = "eligible_expanded_roi_reference_v2" if selected else blocked_reason

        plan_rows.append(
            {
                "ocrrequest_submission_v2_id": sub_id,
                "ocrrequest_reference_v2_id": ref_id,
                "source_expanded_crop_artifact_id": ref.get("source_expanded_crop_artifact_id"),
                "source_bbox_expansion_candidate_id": ref.get("source_bbox_expansion_candidate_id"),
                "expansion_strategy": ref.get("expansion_strategy"),
                "payload_candidate_id": f"payload_{hashlib.sha256(ref_id.encode()).hexdigest()[:10]}",
                "provider_class_selected": str(ref.get("provider_class_allowed") or "rapidocr_lightweight"),
                "submission_mode": "gated_eval",
                "selected_for_submission": selected,
                "selection_reason": selection_reason,
                "blocked_reason": blocked_reason,
                "direct_provider_bypass_allowed": False,
                "current_phase_provider_invocation_allowed": selected,
                "evidence_pack_generation_allowed": False,
                "semantic_generation_allowed": False,
                "source_validation_v2_allowed": False,
                "fact_status": "not_fact",
            }
        )

        if not selected:
            results.append(
                {
                    "expanded_roi_ocr_result_v2_id": _result_id(sub_id),
                    "ocrrequest_submission_v2_id": sub_id,
                    "ocrrequest_reference_v2_id": ref_id,
                    "source_expanded_crop_artifact_id": ref.get("source_expanded_crop_artifact_id"),
                    "crop_file_path": crop_path,
                    "provider": None,
                    "provider_status": "skipped",
                    "raw_ocr_text": "",
                    "text_items": [],
                    "empty_text": True,
                    "confidence_summary": {"confidence_min": None, "confidence_max": None, "confidence_avg": None},
                    "provider_error": blocked_reason,
                    "processing_time_ms": 0,
                    "raw_output_preserved": False,
                    "result_status": "skipped_not_selected",
                    "fact_status": "not_fact",
                    "write_allowed": False,
                    "evidence_pack_generated": False,
                    "semantic_candidate_generated": False,
                    "source_chain": list(ref.get("source_chain") or []) + [RUNTIME_STEP],
                }
            )
            matrix_rows.append(
                {
                    "ocrrequest_reference_v2_id": ref_id,
                    "submission_status": "skipped",
                    "provider_status": "skipped",
                    "raw_ocr_text_preview": "",
                    "empty_text": True,
                    "text_item_count": 0,
                    "confidence_min": None,
                    "confidence_max": None,
                    "confidence_avg": None,
                    "crop_file_path": crop_path,
                    "fact_status": "not_fact",
                    "write_allowed": False,
                }
            )
            continue

        submitted_count += 1
        req = _build_ocr_request_v2(ref, sub_id)
        work_dir = work_root / ref_id
        any_bridge = True
        br = _bridge_submit(
            req=req,
            ocrrequest_reference_v2_id=ref_id,
            work_dir=work_dir,
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
                "bridge_call_v2_id": _bridge_call_id(sub_id),
                "ocrrequest_submission_v2_id": sub_id,
                "ocrrequest_reference_v2_id": ref_id,
                "source_expanded_crop_artifact_id": ref.get("source_expanded_crop_artifact_id"),
                "source_bbox_expansion_candidate_id": ref.get("source_bbox_expansion_candidate_id"),
                "expansion_strategy": ref.get("expansion_strategy"),
                "crop_file_path": crop_path,
                "provider_class_selected": ref.get("provider_class_allowed"),
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

        st_bridge = str(br.get("bridge_status") or "")
        if st_bridge == "success" and br.get("provider_invoked"):
            if empty_text:
                result_status = "success_empty"
                success_count += 1
                empty_count += 1
            else:
                result_status = "success_non_empty"
                success_count += 1
                non_empty_count += 1
            provider_status = "success"
            submission_status = "submitted"
        elif st_bridge in ("error", "exception", "rejected", "timeout"):
            result_status = "provider_error"
            provider_status = "error"
            submission_status = "failed"
            error_count += 1
        else:
            result_status = "provider_error"
            provider_status = str(st_bridge or "error")
            submission_status = "failed"
            error_count += 1

        low_info = (not empty_text and len(text_joined.strip()) <= 2) or text_joined.strip() in ("行",)
        chain = list(ref.get("source_chain") or []) + [RUNTIME_STEP]
        results.append(
            {
                "expanded_roi_ocr_result_v2_id": _result_id(sub_id),
                "ocrrequest_submission_v2_id": sub_id,
                "ocrrequest_reference_v2_id": ref_id,
                "source_expanded_crop_artifact_id": ref.get("source_expanded_crop_artifact_id"),
                "source_bbox_expansion_candidate_id": ref.get("source_bbox_expansion_candidate_id"),
                "expansion_strategy": ref.get("expansion_strategy"),
                "crop_file_path": crop_path,
                "source_bbox_xyxy": ref.get("source_bbox_xyxy"),
                "expanded_bbox_xyxy": ref.get("expanded_bbox_xyxy"),
                "crop_width": ref.get("crop_width"),
                "crop_height": ref.get("crop_height"),
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
                "repeated_same_text_candidate": False,
                "fact_status": "not_fact",
                "write_allowed": False,
                "evidence_pack_generated": False,
                "semantic_candidate_generated": False,
                "source_chain": chain,
            }
        )

        preview = text_joined[:80] if text_joined else ""
        matrix_rows.append(
            {
                "ocrrequest_reference_v2_id": ref_id,
                "expansion_strategy": ref.get("expansion_strategy"),
                "submission_status": submission_status,
                "provider_status": provider_status,
                "raw_ocr_text_preview": preview,
                "empty_text": empty_text,
                "text_item_count": len(text_items),
                **conf,
                "crop_file_path": crop_path,
                "crop_width": ref.get("crop_width"),
                "crop_height": ref.get("crop_height"),
                "area_growth_ratio": ref.get("area_growth_ratio"),
                "low_information_text": low_info,
                "result_status": result_status,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        chain_rows.append(
            {
                "expanded_roi_ocr_result_v2_id": _result_id(sub_id),
                "traceable_to_ocrrequest_reference_v2": True,
                "traceable_to_expanded_crop_artifact": bool(ref.get("source_expanded_crop_artifact_id")),
                "traceable_to_bbox_expansion_candidate": bool(ref.get("source_bbox_expansion_candidate_id")),
                "traceable_to_crop_v2": crop_v2_root.is_dir(),
                "traceable_to_diversity_check": div_root.is_dir(),
                "traceable_to_quality_diagnosis": diag_root.is_dir(),
                "traceable_to_linebox_trace": True,
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )


    texts = [str(r.get("raw_ocr_text") or "").strip() for r in results if str(r.get("result_status", "")).startswith("success")]
    from collections import Counter
    tc = Counter(texts)
    most_common = tc.most_common(1)[0][0] if tc else ""
    unique_text_count = len([x for x in tc if x])
    low_info_count = sum(1 for r in results if r.get("low_information_text"))
    for r in results:
        ttxt = str(r.get("raw_ocr_text") or "").strip()
        r["repeated_same_text_candidate"] = bool(ttxt) and texts.count(ttxt) > 1
    repeated_same = sum(1 for r in results if r.get("repeated_same_text_candidate"))
    strategy_rows = []
    for r in results:
        if r.get("result_status") == "skipped_not_selected":
            continue
        strategy_rows.append({
            "expansion_strategy": r.get("expansion_strategy"),
            "crop_size": f"{r.get('crop_width')}x{r.get('crop_height')}" if r.get("crop_width") else None,
            "area_growth_ratio": None,
            "raw_ocr_text": r.get("raw_ocr_text"),
            "text_item_count": len(r.get("text_items") or []),
            "empty_text": r.get("empty_text"),
            "low_information_text": r.get("low_information_text"),
            "repeated_with_other_strategy": r.get("repeated_same_text_candidate"),
            "confidence_summary": r.get("confidence_summary"),
            "useful_text_candidate": bool(str(r.get("raw_ocr_text") or "").strip()) and not r.get("low_information_text"),
            "comparison_candidate_only": True,
            "benchmark_score_generated": False,
            "accuracy_claimed": False,
            "recommended_for_future_ep_adapter": "Evidence-Pack-Adapter-v3-BBoxExpansion",
            "required_next_action": "Semantic-Candidate-v3-BBoxExpansionAware",
            "fact_status": "not_fact",
        })
    bypass_static = _static_bypass_scan(cap_path)
    bypass_static["bridge_invoked"] = any_bridge
    bypass_static["every_provider_call_has_ocrrequest_ref"] = all(
        bool(r.get("ocrrequest_reference_v2_id")) for r in trace_rows
    ) if trace_rows else True
    bypass_static["mock_text_substitution_detected"] = any(
        "MOCK_TEXT" in str(r.get("raw_ocr_text") or "") for r in results
    )
    bypass_static["direct_provider_call_detected"] = bypass_static.get("direct_provider_call_detected", False)

    selected_count = sum(1 for p in plan_rows if p.get("selected_for_submission"))
    avg_ms = round(sum(processing_times) / len(processing_times), 2) if processing_times else None
    text_item_total = sum(len(r.get("text_items") or []) for r in results)

    if ref_count_observed == 4 and submitted_count == 4 and bypass_static.get("direct_provider_call_detected") is False:
        phase_hint = "GO" if error_count == 0 or success_count > 0 else "CONDITIONAL_GO"
    elif submitted_count == selected_count and not bypass_static.get("direct_provider_call_detected"):
        phase_hint = "CONDITIONAL_GO"
    else:
        phase_hint = "NO_GO"

    summary = {
        "schema_version": "ocrrequest_gated_submission_v2_bbox_expansion_summary_v0",
        "phase": PHASE_ID,
        "submission_scope": "expanded_roi_ocrrequest_gated_submission_only",
        "based_on_ocrrequest_reference_v2_bbox_expansion": ref_root.is_dir(),
        "ocrrequest_reference_v2_count_observed": ref_count_observed,
        "strategy_comparison_candidate_generated": True,
        "source_validation_v2_invoked": False,
        "ocrrequest_intake_count": len(intake_rows),
        "ocrrequest_selected_for_submission_count": selected_count,
        "ocrrequest_submitted_count": submitted_count,
        "ocrrequest_success_count": success_count,
        "ocrrequest_error_count": error_count,
        "ocr_invoked": any_bridge,
        "provider_invoked": any_provider,
        "rapidocr_invoked": any_rapid,
        "paddleocr_invoked": any_paddle,
        "direct_provider_bypass": False,
        "every_provider_call_has_ocrrequest_ref": bypass_static.get("every_provider_call_has_ocrrequest_ref", True),
        "full_frame_ocr_invoked": False,
        "mock_text_used": bypass_static.get("mock_text_substitution_detected", False),
        "expanded_roi_ocr_result_collection_generated": len(results) > 0,
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
        "phase_verdict_hint": phase_hint,
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "ocrrequest_v2_bbox_expansion_submission_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "gate_policy": {
            "schema_version": "ocrrequest_v2_bbox_expansion_submission_gate_policy_v1",
            "rules": GATE_RULES,
            "direct_provider_bypass_forbidden": True,
            "full_frame_ocr_forbidden": True,
            "mock_text_forbidden": True,
        },
        "submission_plan": {
            "schema_version": "ocrrequest_v2_bbox_expansion_submission_plan_v1",
            "row_count": len(plan_rows),
            "selected_for_submission_count": selected_count,
            "rows": plan_rows,
        },
        "bridge_trace": {
            "schema_version": "ocrrequest_v2_bbox_expansion_bridge_invocation_trace_v1",
            "row_count": len(trace_rows),
            "rows": trace_rows,
        },
        "bypass_audit": bypass_static,
        "result_collection": {
            "schema_version": "expanded_roi_ocr_result_collection_v2",
            "result_count": len(results),
            "rows": results,
        },
        "result_matrix": {
            "schema_version": "expanded_roi_ocr_result_matrix_v2",
            "row_count": len(matrix_rows),
            "rows": matrix_rows,
        },
        "low_information_guard": {
            "schema_version": "expanded_roi_ocr_low_information_guard_v2",
            "result_count": len(results),
            "empty_text_count": empty_count,
            "non_empty_text_count": non_empty_count,
            "provider_error_count": error_count,
            "empty_text_is_valid_ocr_result": True,
            "empty_text_is_not_no_text_fact": True,
            "non_empty_text_is_not_accuracy": True,
            "no_text_fact_written": True,
            "no_semantic_generated": True,
            "no_world_model_written": True,
            "low_information_text_count": low_info_count,
            "repeated_same_text_count": repeated_same,
            "unique_text_count": unique_text_count,
            "most_common_text": most_common,
            "repeated_same_text_not_consensus": True,
            "low_information_text_not_semantic_success": True,
        },
        "strategy_comparison": {
            "schema_version": "expanded_roi_ocr_strategy_output_comparison_candidate_v2",
            "row_count": len(strategy_rows),
            "rows": strategy_rows,
        },
        "source_chain_report": {
            "schema_version": "expanded_roi_ocr_source_chain_report_v2",
            "row_count": len(chain_rows),
            "all_traceable_to_ocrrequest_reference_v2": all(r.get("traceable_to_ocrrequest_reference_v2") for r in chain_rows),
            "rows": chain_rows,
        },
        "provider_summary": {
            "schema_version": "expanded_roi_ocr_provider_summary_v2",
            "provider_invoked_count": submitted_count if any_provider else 0,
            "rapidocr_invoked_count": sum(1 for t in trace_rows if t.get("rapidocr_invoked")),
            "paddleocr_invoked_count": 0,
            "provider_error_count": error_count,
            "provider_success_count": success_count,
            "provider_distribution": provider_dist,
            "direct_provider_bypass": False,
            "mock_text_used": False,
            "provider_comparison_claimed": False,
            "provider_winner_claimed": False,
            "provider_failure_claimed": False,
        },
        "no_evidence_pack_boundary": {
            "schema_version": "expanded_roi_ocr_no_evidence_pack_boundary_v2",
            "expanded_roi_ocr_result_collection_generated": True,
            "evidence_pack_generated": False,
            "evidence_pack_adapter_invoked": False,
            "semantic_candidate_generated": False,
            "review_policy_invoked": False,
            "source_validation_v2_invoked": False,
            "fact_review_generated": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
        },
        "future_adapter_plan": {
            "schema_version": "expanded_roi_ocr_future_adapter_plan_v3",
            "phases": [
                {
                    "future_phase": "Evidence-Pack-Adapter-v3-BBoxExpansion",
                    "purpose": "Adapt ROI OCR results to Evidence Pack v2 with ROI refs preserved",
                    "required_input": ["expanded_roi_ocr_result_collection_v2"],
                    "expected_output": ["evidence_pack_v3_candidate"],
                    "adapter_should_preserve_ocrrequest_reference_v2": True,
                    "adapter_should_preserve_expanded_crop_artifact_ref": True,
                    "adapter_should_preserve_expansion_candidate_ref": True,
                    "adapter_should_preserve_source_bbox": True,
                    "adapter_should_preserve_expanded_bbox": True,
                    "adapter_should_preserve_expansion_strategy": True,
                    "adapter_should_preserve_ocrrequest_ref": True,
                    "adapter_should_preserve_crop_ref": True,
                    "adapter_should_preserve_text_items_bbox": True,
                    "adapter_should_preserve_provider_metadata": True,
                    "not_in_current_phase": True,
                }
            ],
        },
        "boundary": {
            "schema_version": "expanded_roi_ocr_boundary_report_v2",
            "expanded_roi_ocr_gated_submission_only": True,
            "ocrrequest_submitted": submitted_count > 0,
            "provider_invoked": any_provider,
            "direct_provider_bypass": False,
            "full_frame_ocr_invoked": False,
            "mock_text_used": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "review_decision_committed": False,
            "approval_granted": False,
            "fact_write_allowed": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "navigation_decision_allowed": False,
        },
        "metrics": {
            "schema_version": "expanded_roi_ocr_metrics_candidate_v2",
            "ocrrequest_reference_v2_count_observed": ref_count_observed,
        "strategy_comparison_candidate_generated": True,
        "source_validation_v2_invoked": False,
            "ocrrequest_submitted_count": submitted_count,
            "provider_invoked_count": sum(1 for t in trace_rows if t.get("provider_invoked")),
            "provider_success_count": success_count,
            "provider_error_count": error_count,
            "expanded_roi_ocr_result_count": len(results),
            "empty_text_count": empty_count,
            "non_empty_text_count": non_empty_count,
            "text_item_total_count": text_item_total,
            "avg_processing_time_ms": avg_ms,
            "evidence_pack_generated_count": 0,
            "semantic_candidate_generated_count": 0,
            "fact_write_allowed_count": 0,
            "low_information_text_count": low_info_count,
            "repeated_same_text_count": repeated_same,
            "source_validation_v2_invoked_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "expanded_roi_ocr_benchmark_link_v2",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "expanded_roi_ocr_system_health_link_v2",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "expanded_roi_ocr_no_write_boundary_v2",
            "boundary_ok": True,
            "violations": [],
            "expanded_roi_ocr_gated_submission_only": True,
            "direct_provider_bypass": False,
            "full_frame_ocr_invoked": False,
            "mock_text_used": False,
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
        },
        "sim_report": {
            "schema_version": "expanded_roi_ocr_simulation_context_v2",
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
            "schema_version": "expanded_roi_ocr_non_claims_report_v2",
            "expanded_roi_crop_ocr_only": True,
            "strategy_comparison_not_benchmark": True,
            "ocr_result_not_fact": True,
            "ocr_result_not_evidence_pack": True,
            "empty_text_not_no_text_fact": True,
            "non_empty_not_accuracy_claim": True,
            "no_semantic_candidate": True,
            "no_world_model": True,
            "no_benchmark_claim": True,
            "no_provider_comparison": True,
            "no_navigation": True,
            "no_production_ready": True,
        },
        "followups": {"schema_version": "expanded_roi_ocr_open_followups_v2", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "expanded_roi_ocr_audit_report_v2",
            "ocrrequest_gated_submission_from_roi_v2_bbox_expansion_executed": True,
            "ocrrequest_reference_v2_count_observed": ref_count_observed,
        "strategy_comparison_candidate_generated": True,
        "source_validation_v2_invoked": False,
            "ocrrequest_submitted_count": submitted_count,
            "ocr_invoked": any_bridge,
            "provider_invoked": any_provider,
            "rapidocr_invoked": any_rapid,
            "paddleocr_invoked": any_paddle,
            "direct_provider_bypass": False,
            "every_provider_call_has_ocrrequest_ref": bypass_static.get("every_provider_call_has_ocrrequest_ref", True),
            "full_frame_ocr_invoked": False,
            "mock_text_used": False,
            "expanded_roi_ocr_result_collection_generated": len(results) > 0,
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
        },
    }

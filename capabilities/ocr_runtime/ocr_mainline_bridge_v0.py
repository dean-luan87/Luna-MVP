# -*- coding: utf-8 -*-
"""Minimal OCR mainline bridge v0 — request → gate → (normalization) → stub → evidence → bridge candidate → audit."""

from __future__ import annotations

import datetime as _dt
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.ocr_runtime.ocr_image_input_gate_v0 import run_image_input_gate_v0
from capabilities.ocr_runtime.ocr_provider_registry_v0 import build_default_ocr_provider_registry_v0
from capabilities.ocr_runtime.ocr_provider_selection_v0 import merge_audit_provider_selection_v0, select_ocr_provider_v0
from capabilities.ocr_runtime.ocr_request_contract_v0 import (
    OCRRequestV0,
    parse_all_roi_bboxes_xyxy_v0,
    parse_roi_bbox_xyxy_v0,
    validate_ocr_request_v0,
)
from capabilities.ocr_runtime.ocr_runtime_audit_v0 import default_ocr_runtime_audit_v0


def _rejected_evidence_and_pack(req: OCRRequestV0, gate: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    rc = list(gate.get("reason_codes") or []) if isinstance(gate.get("reason_codes"), list) else []
    evidence: Dict[str, Any] = {
        "schema_version": "ocr_evidence_minimal_v0",
        "request_id": req.request_id,
        "trace_id": req.trace_id,
        "evidence_status": "no_evidence",
        "reason_codes": rc,
        "text_joined": "",
        "text_items": [],
        "provider": None,
        "call_method": "none_provider_not_invoked",
    }
    pack: Dict[str, Any] = {
        "schema_version": "ocr_evidence_pack_candidate_v0",
        "request_id": req.request_id,
        "trace_id": req.trace_id,
        "pack_status": "rejected_no_evidence",
        "raw_text_joined": "",
        "raw_text_candidates": [],
        "provider_trace": {"invoked": False},
    }
    return evidence, pack


def _env_true(name: str, default: str = "false") -> bool:
    return os.environ.get(name, default).strip().lower() in ("1", "true", "yes", "on")


def _minimal_stcm_deadline(req: OCRRequestV0) -> Dict[str, Any]:
    return {
        "schema_version": "stcm_model_call_deadline_v0",
        "deadline_class": "ocr_mainline_minimal",
        "latency_budget_ms": int(req.latency_budget_ms),
        "urgency": req.urgency,
        "trace_id": req.trace_id,
        "request_id": req.request_id,
        "created_at": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
    }


def _build_minimal_ocr_evidence(
    provider_out: Dict[str, Any],
    req: OCRRequestV0,
    *,
    input_pack: Optional[Dict[str, Any]] = None,
    merge_out: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    pol = input_pack.get("processing_policy") if isinstance(input_pack, dict) and isinstance(input_pack.get("processing_policy"), dict) else {}

    if merge_out and isinstance(merge_out, dict):
        items = merge_out.get("merged_text_items") if isinstance(merge_out.get("merged_text_items"), list) else []
        joined = str(merge_out.get("text_joined") or "")
        cm = str(provider_out.get("call_method") or "stub")
        evidence: Dict[str, Any] = {
            "schema_version": "ocr_evidence_minimal_v0",
            "request_id": req.request_id,
            "trace_id": req.trace_id,
            "provider": str(provider_out.get("provider") or "ocr_stub"),
            "text_joined": joined,
            "text_items": items,
            "call_method": cm,
            "tile_evidence_items": merge_out.get("tile_evidence_items"),
            "reading_order_candidate": merge_out.get("reading_order_candidate"),
            "coverage_summary": merge_out.get("coverage_summary"),
            "partial_evidence_completion": merge_out.get("partial_evidence_completion"),
        }
        if str(pol.get("strategy") or "") == "tile":
            evidence["evidence_scope"] = pol.get("evidence_scope")
            evidence["full_image_claim_allowed"] = bool(pol.get("full_image_claim_allowed"))
            evidence["reading_order_confidence"] = pol.get("reading_order_confidence")
            roc = merge_out.get("reading_order_candidate") if isinstance(merge_out.get("reading_order_candidate"), dict) else {}
            if roc.get("confidence"):
                evidence["reading_order_confidence"] = roc.get("confidence")
            evidence["text_coverage_disclosure"] = (
                "partial_tile_sync_budget_truncation" if pol.get("evidence_scope") == "partial_image" else "tile_set_complete_stub_not_native_full_image"
            )
        return evidence

    items = provider_out.get("text_items") if isinstance(provider_out.get("text_items"), list) else []
    joined = str(provider_out.get("text_joined") or "")
    if str(pol.get("strategy") or "") == "tile":
        prefix = "[PARTIAL_TILE_EVIDENCE_STUB] " if pol.get("evidence_scope") == "partial_image" else "[TILED_IMAGE_STUB_NOT_FULL_IMAGE] "
        joined = prefix + joined
    cm = str(provider_out.get("call_method") or "stub")
    evidence = {
        "schema_version": "ocr_evidence_minimal_v0",
        "request_id": req.request_id,
        "trace_id": req.trace_id,
        "provider": str(provider_out.get("provider") or "ocr_stub"),
        "text_joined": joined,
        "text_items": items,
        "call_method": cm,
    }
    if str(pol.get("strategy") or "") == "tile":
        evidence["evidence_scope"] = pol.get("evidence_scope")
        evidence["full_image_claim_allowed"] = bool(pol.get("full_image_claim_allowed"))
        evidence["reading_order_confidence"] = pol.get("reading_order_confidence")
        evidence["text_coverage_disclosure"] = (
            "partial_tile_sync_budget_truncation" if pol.get("evidence_scope") == "partial_image" else "tile_set_complete_stub_not_native_full_image"
        )
    if str(pol.get("strategy") or "") == "roi_list":
        roc = provider_out.get("reading_order_candidate")
        if isinstance(roc, dict):
            evidence["reading_order_candidate"] = roc
        pref = provider_out.get("provider_raw_ref")
        if isinstance(pref, dict) and isinstance(pref.get("per_roi_provider_status"), list):
            evidence["per_roi_provider_status"] = pref.get("per_roi_provider_status")
    return evidence


def _build_bridge_pack_candidate(
    evidence: Dict[str, Any],
    req: OCRRequestV0,
    *,
    input_pack: Optional[Dict[str, Any]] = None,
    merge_out: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    joined = str(evidence.get("text_joined") or "")
    cands: List[Dict[str, Any]] = []
    for i, it in enumerate(evidence.get("text_items") or []):
        if not isinstance(it, dict):
            continue
        cands.append(
            {
                "line_order": i,
                "text": str(it.get("text") or ""),
                "confidence": float(it.get("score") or 0.0),
            }
        )
    pol = input_pack.get("processing_policy") if isinstance(input_pack, dict) and isinstance(input_pack.get("processing_policy"), dict) else {}
    cm = str(evidence.get("call_method") or "stub")
    bp: Dict[str, Any] = {
        "schema_version": "ocr_evidence_pack_candidate_v0",
        "request_id": req.request_id,
        "trace_id": req.trace_id,
        "raw_text_joined": str(merge_out.get("raw_text_joined_core") or "") if merge_out else joined,
        "raw_text_candidates": merge_out.get("raw_text_candidates") if merge_out and isinstance(merge_out.get("raw_text_candidates"), list) else cands,
        "provider_trace": {"provider": evidence.get("provider"), "call_method": cm},
    }
    if merge_out and isinstance(merge_out, dict):
        bp["eligible_text_evidence"] = merge_out.get("eligible_text_evidence") or []
        bp["tile_evidence_summary"] = merge_out.get("tile_evidence_summary")
        bp["tile_coverage"] = input_pack.get("tile_coverage") if isinstance(input_pack, dict) else None
        bp["source_reference_chain"] = list((input_pack or {}).get("source_chain") or []) if isinstance(input_pack, dict) else []
        bp["audit"] = {
            "tile_evidence_generated": True,
            "tile_evidence_item_count": len(merge_out.get("tile_evidence_items") or []),
            "coordinate_reconstruction_applied": True,
        }
    if str(pol.get("strategy") or "") == "tile":
        bp["evidence_scope"] = pol.get("evidence_scope")
        bp["full_image_claim_allowed"] = bool(pol.get("full_image_claim_allowed"))
        bp["reading_order_confidence"] = evidence.get("reading_order_confidence") or pol.get("reading_order_confidence")
        bp["text_coverage_disclosure"] = evidence.get("text_coverage_disclosure")
        bp["reading_order_candidate"] = evidence.get("reading_order_candidate")
        if merge_out and isinstance(merge_out, dict):
            bp["partial_evidence_completion"] = merge_out.get("partial_evidence_completion")
    elif str(pol.get("strategy") or "") in ("roi", "roi_list"):
        elig: List[Dict[str, Any]] = []
        for i, it in enumerate(evidence.get("text_items") or []):
            if not isinstance(it, dict):
                continue
            row: Dict[str, Any] = {
                "line_order": i,
                "text": str(it.get("text") or ""),
                "confidence": float(it.get("score") or 0.0),
                "local_bbox": it.get("local_bbox"),
                "local_polygon": it.get("local_polygon"),
                "original_bbox": it.get("original_bbox"),
                "original_polygon": it.get("original_polygon"),
                "coordinate_lift_applied": bool(it.get("coordinate_lift_applied")),
                "source_unit_ref": it.get("source_unit_ref"),
                "roi_bbox_in_original": it.get("roi_bbox_in_original"),
                "no_provider_geometry": it.get("no_provider_geometry"),
            }
            if str(pol.get("strategy") or "") == "roi_list":
                row["unit_id"] = it.get("unit_id")
                row["roi_id"] = it.get("roi_id")
            elig.append(row)
        bp["eligible_text_evidence"] = elig
    return bp


def _should_merge_tile_stub_evidence(input_pack: Optional[Dict[str, Any]]) -> bool:
    if not isinstance(input_pack, dict):
        return False
    pol = input_pack.get("processing_policy") if isinstance(input_pack.get("processing_policy"), dict) else {}
    if str(pol.get("strategy") or "") != "tile":
        return False
    units = input_pack.get("input_units") if isinstance(input_pack.get("input_units"), list) else []
    return bool(units) and all(isinstance(u, dict) and u.get("unit_type") == "tile" for u in units)


def run_ocr_mainline_bridge_v0(
    req: OCRRequestV0,
    *,
    governance_config_path: Path,
    workspace_root: Path,
    normalization_pipeline_enabled: bool = True,
    normalization_work_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    audit: Dict[str, Any] = default_ocr_runtime_audit_v0()

    def _base_error(status: str, err: str, **extra: Any) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "schema_version": "ocr_mainline_bridge_result_v0",
            "request_id": req.request_id,
            "trace_id": req.trace_id,
            "status": status,
            "error": err,
            "input_gate": {},
            "stcm_deadline": {},
            "provider_result": {},
            "ocr_evidence": {},
            "bridge_pack": {},
            "audit": audit,
        }
        out.update(extra)
        return out

    if not _env_true("LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0", "false"):
        return _base_error("error", "feature_disabled:LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0")

    ok, errs = validate_ocr_request_v0(req)
    if not ok:
        return {**_base_error("error", "request_validation_failed"), "validation_errors": errs}

    env_real = _env_true("LUNA_ENABLE_OCR_REAL_PROVIDER_V0", "false")
    env_paddle = _env_true("LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0", "false")
    env_rapid = _env_true("LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0", "false")
    env_stub = _env_true("LUNA_ENABLE_OCR_STUB_PROVIDER_V0", "true")

    if env_paddle and not env_real:
        reg0 = build_default_ocr_provider_registry_v0()
        sel0 = select_ocr_provider_v0(
            request=req,
            registry=reg0,
            input_pack=None,
            env_enable_stub=env_stub,
            env_enable_real=env_real,
            env_paddle_runtime=env_paddle,
            env_rapid_runtime=env_rapid,
        )
        merge_audit_provider_selection_v0(audit, sel0.selection_report)
        return {
            **_base_error("error", "misconfiguration_paddle_runtime_without_real_provider"),
            "provider_selection_report": sel0.selection_report,
            "input_gate": {},
            "stcm_deadline": _minimal_stcm_deadline(req),
            "provider_result": {},
            "ocr_evidence": {},
            "bridge_pack": {},
        }

    img = Path(req.image_path).expanduser().resolve()
    gate = run_image_input_gate_v0(
        image_path=img,
        governance_config_path=governance_config_path,
        allow_full_image=bool(req.allow_full_image),
        enable_normalization_branch=bool(normalization_pipeline_enabled),
        enable_tile_planner_branch=_env_true("LUNA_ENABLE_OCR_TILE_PLANNER_V0", "false"),
    )
    deadline = _minimal_stcm_deadline(req)

    if gate.get("gate_verdict") == "REJECT":
        ev, bp = _rejected_evidence_and_pack(req, gate)
        return {
            "schema_version": "ocr_mainline_bridge_result_v0",
            "request_id": req.request_id,
            "trace_id": req.trace_id,
            "status": "rejected",
            "input_gate": gate,
            "stcm_deadline": deadline,
            "provider_result": {},
            "ocr_evidence": ev,
            "bridge_pack": bp,
            "audit": audit,
            "normalization_pipeline_enabled": normalization_pipeline_enabled,
        }

    pipe_out: Dict[str, Any] = {}
    provider_pack: Optional[Dict[str, Any]] = None
    if normalization_pipeline_enabled:
        from capabilities.ocr_runtime.ocr_image_normalization_pipeline_v0 import run_ocr_image_normalization_pipeline_v0

        work = normalization_work_dir or (workspace_root / ".ocr_norm_work" / req.request_id)
        roi_bboxes: Optional[List[List[int]]] = None
        if str(req.input_type) == "roi":
            b = parse_roi_bbox_xyxy_v0(list(req.roi_refs or []))
            roi_bboxes = [b] if b else None
        elif str(req.input_type) == "roi_list":
            roi_bboxes = parse_all_roi_bboxes_xyxy_v0(list(req.roi_refs or []))
        pipe_out = run_ocr_image_normalization_pipeline_v0(
            image_path=img,
            gate=gate,
            governance_config_path=governance_config_path,
            normalization_work_dir=work,
            request_id=req.request_id,
            trace_id=req.trace_id,
            roi_bboxes_xyxy=roi_bboxes,
        )
        na = pipe_out.get("normalization_audit") if isinstance(pipe_out.get("normalization_audit"), dict) else {}
        for k, v in na.items():
            audit[k] = v
        provider_pack = pipe_out.get("provider_input_pack") if isinstance(pipe_out.get("provider_input_pack"), dict) else None
        if isinstance(provider_pack, dict):
            ppol = provider_pack.get("processing_policy") if isinstance(provider_pack.get("processing_policy"), dict) else {}
            uu = provider_pack.get("input_units") if isinstance(provider_pack.get("input_units"), list) else []
            if str(ppol.get("strategy") or "") in ("roi", "roi_list"):
                audit["roi_unit_count"] = len(uu)
                audit["multi_roi_processed"] = str(ppol.get("strategy") or "") == "roi_list"

    pipe_slice: Dict[str, Any] = {}
    if pipe_out:
        pipe_slice = {
            k: pipe_out[k]
            for k in (
                "metadata_probe",
                "input_decision",
                "coordinate_transform_matrix",
                "source_chain",
                "tile_plan",
            )
            if k in pipe_out
        }

    reg = build_default_ocr_provider_registry_v0()
    sel = select_ocr_provider_v0(
        request=req,
        registry=reg,
        input_pack=provider_pack,
        env_enable_stub=env_stub,
        env_enable_real=env_real,
        env_paddle_runtime=env_paddle,
        env_rapid_runtime=env_rapid,
    )
    merge_audit_provider_selection_v0(audit, sel.selection_report)
    if not sel.ok or sel.adapter is None:
        err_body: Dict[str, Any] = {
            "schema_version": "ocr_mainline_bridge_result_v0",
            "request_id": req.request_id,
            "trace_id": req.trace_id,
            "status": "error",
            "error": sel.error_code or "provider_selection_failed",
            "input_gate": gate,
            "stcm_deadline": deadline,
            "provider_result": {},
            "ocr_evidence": {},
            "bridge_pack": {},
            "audit": audit,
            "provider_selection_report": sel.selection_report,
            "normalization_pipeline_enabled": normalization_pipeline_enabled,
        }
        err_body.update(pipe_slice)
        if pipe_out and isinstance(pipe_out.get("provider_input_pack"), dict):
            err_body["ocr_provider_input_pack"] = pipe_out["provider_input_pack"]
        return err_body

    prov = sel.adapter.run(provider_pack, req, deadline)
    if isinstance(prov, dict) and isinstance(provider_pack, dict):
        pstat = str(prov.get("status") or "success")
        if pstat in ("success", "empty"):
            from capabilities.ocr_runtime.ocr_roi_coordinate_lift_v0 import (
                apply_roi_coordinate_lift_to_provider_result_v0,
                merge_roi_lift_audit_v0,
            )

            prov, lift_rep = apply_roi_coordinate_lift_to_provider_result_v0(prov, provider_pack)
            merge_roi_lift_audit_v0(audit, lift_rep)
    if isinstance(prov, dict) and prov.get("real_provider_invoked") is True:
        audit["real_provider_invoked"] = True
        if isinstance(sel.selection_report, dict):
            sel.selection_report["real_provider_invoked"] = True
    pst = str(prov.get("status") or "success")
    if pst == "timeout":
        return {
            "schema_version": "ocr_mainline_bridge_result_v0",
            "request_id": req.request_id,
            "trace_id": req.trace_id,
            "status": "timeout",
            "input_gate": gate,
            "stcm_deadline": deadline,
            "provider_result": prov,
            "ocr_evidence": {},
            "bridge_pack": {},
            "audit": audit,
            "provider_selection_report": sel.selection_report,
            "ocr_provider_input_pack": provider_pack,
            **pipe_slice,
        }
    if pst == "error":
        return {
            "schema_version": "ocr_mainline_bridge_result_v0",
            "request_id": req.request_id,
            "trace_id": req.trace_id,
            "status": "error",
            "input_gate": gate,
            "stcm_deadline": deadline,
            "provider_result": prov,
            "ocr_evidence": {},
            "bridge_pack": {},
            "audit": audit,
            "provider_selection_report": sel.selection_report,
            "ocr_provider_input_pack": provider_pack,
            **pipe_slice,
        }

    merge_out: Optional[Dict[str, Any]] = None
    if pst == "success" and _should_merge_tile_stub_evidence(provider_pack):
        from capabilities.ocr_runtime.ocr_tile_evidence_merge_stub_v0 import merge_tile_stub_evidence_v0

        merge_out = merge_tile_stub_evidence_v0(
            provider_out=prov,
            input_pack=provider_pack if isinstance(provider_pack, dict) else {},
            tile_plan=pipe_out.get("tile_plan") if isinstance(pipe_out, dict) else None,
        )
        audit["tile_evidence_generated"] = True
        audit["tile_evidence_item_count"] = len(merge_out.get("tile_evidence_items") or [])
        audit["coordinate_reconstruction_applied"] = True

    evidence = _build_minimal_ocr_evidence(prov, req, input_pack=provider_pack, merge_out=merge_out)
    bp = _build_bridge_pack_candidate(evidence, req, input_pack=provider_pack, merge_out=merge_out)

    result: Dict[str, Any] = {
        "schema_version": "ocr_mainline_bridge_result_v0",
        "request_id": req.request_id,
        "trace_id": req.trace_id,
        "status": "success",
        "input_gate": gate,
        "stcm_deadline": deadline,
        "provider_result": prov,
        "ocr_evidence": evidence,
        "bridge_pack": bp,
        "audit": audit,
        "provider_selection_report": sel.selection_report,
        "normalization_pipeline_enabled": normalization_pipeline_enabled,
    }
    if pipe_out:
        result.update(pipe_slice)
        if "provider_input_pack" in pipe_out:
            result["ocr_provider_input_pack"] = pipe_out["provider_input_pack"]
    if merge_out and isinstance(result.get("source_chain"), list):
        result["source_chain"].extend(["tile_evidence_merged", "coordinate_reconstruction_applied"])
    elif merge_out:
        result["source_chain"] = list(result.get("source_chain") or []) + ["tile_evidence_merged", "coordinate_reconstruction_applied"]
    if merge_out:
        result["ocr_tile_evidence_merge_stub"] = merge_out
    return result

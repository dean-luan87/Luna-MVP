# -*- coding: utf-8 -*-
"""Gated RapidOCR submission from Vision ROI OCRRequest candidates (eval-only).

Phase-OCR-Real-RapidOCR-Submission-From-Vision-ROI-Gated-001
"""

from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.ocr_runtime.ocr_mainline_bridge_v0 import run_ocr_mainline_bridge_v0
from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

PLAN_SCHEMA = "rapidocr_submission_plan_from_vision_roi_v0"
MATRIX_SCHEMA = "rapidocr_submission_result_matrix_v0"
COLLECTION_SCHEMA = "rapidocr_submission_from_vision_roi_collection_v0"
PROVIDER_SUMMARY_SCHEMA = "rapidocr_submission_provider_summary_v0"
AUDIT_SCHEMA = "rapidocr_submission_from_vision_roi_audit_v0"
SUMMARY_SCHEMA = "rapidocr_submission_from_vision_roi_summary_v0"


def _env_true(name: str, default: str = "false") -> bool:
    return os.environ.get(name, default).strip().lower() in ("1", "true", "yes", "on")


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(p: Path, obj: object) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _ocr_request_from_candidate_dict(ocr: Dict[str, Any]) -> OCRRequestV0:
    fields = OCRRequestV0.__dataclass_fields__
    kwargs = {k: v for k, v in ocr.items() if k in fields}
    return OCRRequestV0(**kwargs)


def _bridge_row_fields(bridge_result: Dict[str, Any]) -> Dict[str, Any]:
    aud = bridge_result.get("audit") if isinstance(bridge_result.get("audit"), dict) else {}
    sel = bridge_result.get("provider_selection_report") if isinstance(bridge_result.get("provider_selection_report"), dict) else {}
    prov = bridge_result.get("provider_result") if isinstance(bridge_result.get("provider_result"), dict) else {}
    ev = bridge_result.get("ocr_evidence") if isinstance(bridge_result.get("ocr_evidence"), dict) else {}

    selected_provider = str(
        aud.get("selected_provider") or sel.get("selected_provider") or ev.get("provider") or ""
    )
    selected_provider_level = str(aud.get("selected_provider_level") or sel.get("selected_provider_level") or "")
    real_invoked = bool(aud.get("real_provider_invoked")) or bool(prov.get("real_provider_invoked"))
    fallback = bool(aud.get("fallback_to_stub")) or bool(sel.get("fallback_to_stub"))
    rapidocr_enabled = bool(aud.get("rapidocr_runtime_provider_enabled")) or bool(
        sel.get("rapidocr_runtime_provider_enabled")
    )
    rapidocr_invoked = real_invoked and "rapidocr" in selected_provider.lower()
    if not rapidocr_invoked and real_invoked and selected_provider:
        rapidocr_invoked = "rapidocr" in str(ev.get("call_method") or "").lower()

    items = ev.get("text_items") if isinstance(ev.get("text_items"), list) else []
    text_joined = str(ev.get("text_joined") or "")

    return {
        "selected_provider": selected_provider,
        "selected_provider_level": selected_provider_level,
        "real_provider_invoked": real_invoked,
        "rapidocr_runtime_provider_enabled": rapidocr_enabled,
        "rapidocr_invoked": rapidocr_invoked,
        "paddleocr_invoked": bool(aud.get("paddleocr_invoked")) or bool(aud.get("paddleocr_runtime_provider_enabled")),
        "fallback_to_stub": fallback and not real_invoked,
        "evidence_text_joined": text_joined,
        "text_item_count": len(items),
        "empty_text": not str(text_joined).strip(),
    }


def build_rapidocr_submission_plan_v0(
    *,
    source_bridge_root: Path,
    candidates: List[Dict[str, Any]],
) -> Dict[str, Any]:
    reason_codes: List[str] = []
    gates_ok = True

    for name in (
        "LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0",
        "LUNA_ENABLE_OCR_REAL_PROVIDER_V0",
        "LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0",
    ):
        if not _env_true(name, "false"):
            gates_ok = False
            reason_codes.append(f"gate_disabled:{name}")

    if not _env_true("LUNA_ENABLE_OCR_STUB_PROVIDER_V0", "true"):
        reason_codes.append("stub_fallback_disabled:LUNA_ENABLE_OCR_STUB_PROVIDER_V0")

    if _env_true("LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0", "false"):
        gates_ok = False
        reason_codes.append("paddle_runtime_must_be_disabled")

    if not _env_true("LUNA_OCR_SUBMISSION_EVAL_ONLY", "false"):
        reason_codes.append("eval_only_flag_not_set:LUNA_OCR_SUBMISSION_EVAL_ONLY")
    else:
        reason_codes.append("eval_only:LUNA_OCR_SUBMISSION_EVAL_ONLY")

    reason_codes.append(f"lightweight_max_edge_px:{os.environ.get('LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX', '512')}")

    selected = [c for c in candidates if isinstance(c, dict) and c.get("candidate_status") == "not_submitted"]
    if not selected:
        reason_codes.append("no_not_submitted_candidates")

    return {
        "schema_version": PLAN_SCHEMA,
        "source_bridge_root": str(source_bridge_root.resolve()),
        "candidate_count": len(candidates),
        "selected_candidate_count": len(selected),
        "submission_mode": "gated_eval_only",
        "ocr_provider_mode": "rapidocr_lightweight",
        "real_provider_requested": True,
        "rapidocr_runtime_provider_enabled": _env_true("LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0", "false"),
        "paddleocr_runtime_provider_enabled": _env_true("LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0", "false"),
        "fallback_to_stub_allowed": _env_true("LUNA_ENABLE_OCR_STUB_PROVIDER_V0", "true"),
        "submit_allowed": gates_ok and len(selected) > 0,
        "reason_codes": reason_codes,
    }


def build_provider_summary_v0(result_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    provider_counts: Counter[str] = Counter()
    examples: List[str] = []
    rapidocr_success = 0
    stub_fallback = 0
    empty_text = 0
    errors = 0
    latencies: List[float] = []

    for row in result_rows:
        prov = str(row.get("selected_provider") or "unknown")
        provider_counts[prov] += 1
        tj = str(row.get("evidence_text_joined") or "")
        if tj and len(examples) < 5:
            examples.append(tj[:120])
        if row.get("submission_status") == "submitted":
            if row.get("real_provider_invoked") and row.get("rapidocr_invoked"):
                rapidocr_success += 1
            elif row.get("fallback_to_stub"):
                stub_fallback += 1
            if row.get("empty_text"):
                empty_text += 1
        if row.get("submission_status") in ("failed", "rejected_by_gate", "blocked_by_gate"):
            errors += 1
        lat = row.get("provider_latency_ms")
        if isinstance(lat, (int, float)) and lat >= 0:
            latencies.append(float(lat))

    return {
        "schema_version": PROVIDER_SUMMARY_SCHEMA,
        "selected_provider_distribution": dict(provider_counts),
        "rapidocr_success_count": rapidocr_success,
        "stub_fallback_count": stub_fallback,
        "empty_text_count": empty_text,
        "error_count": errors,
        "average_latency_ms": round(sum(latencies) / len(latencies), 2) if latencies else None,
        "text_joined_examples": examples,
    }


def build_rapidocr_submission_audit_v0(
    *,
    result_rows: List[Dict[str, Any]],
    any_bridge_invoked: bool,
) -> Dict[str, Any]:
    any_rapid = any(r.get("rapidocr_invoked") for r in result_rows)
    any_real = any(r.get("real_provider_invoked") for r in result_rows)
    any_fallback = any(r.get("fallback_to_stub") for r in result_rows)

    return {
        "schema": AUDIT_SCHEMA,
        "rapidocr_submission_from_vision_roi_executed": True,
        "eval_only": _env_true("LUNA_OCR_SUBMISSION_EVAL_ONLY", "false"),
        "ocr_mainline_bridge_invoked": any_bridge_invoked,
        "real_provider_requested": True,
        "rapidocr_runtime_provider_enabled": _env_true("LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0", "false"),
        "paddleocr_runtime_provider_enabled": _env_true("LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0", "false"),
        "paddleocr_invoked": False,
        "direct_rapidocr_invoked": False,
        "rapidocr_invoked": any_rapid,
        "real_provider_invoked": any_real,
        "fallback_to_stub_observed": any_fallback,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "cross_modal_fusion_invoked": False,
        "vision_runtime_modified": False,
        "vision_provider_registry_default_changed": False,
    }


def run_rapidocr_submission_from_vision_roi_v0(
    *,
    vision_roi_to_ocr_bridge_root: str,
    workspace_root: Path,
    governance_config_path: Path,
    submission_work_root: Path,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    errs: List[str] = []
    bridge_root = Path(vision_roi_to_ocr_bridge_root).resolve()
    cand_p = bridge_root / "vision_roi_to_ocr_request_candidates.json"
    if not cand_p.is_file():
        empty_audit = build_rapidocr_submission_audit_v0(result_rows=[], any_bridge_invoked=False)
        return (
            {"schema_version": SUMMARY_SCHEMA, "errors": ["missing:vision_roi_to_ocr_request_candidates.json"]},
            {},
            {},
            {},
            {},
            empty_audit,
            ["missing_candidates_file"],
        )

    cand_doc = _read_json(cand_p)
    candidates = cand_doc.get("candidates") if isinstance(cand_doc.get("candidates"), list) else []
    plan = build_rapidocr_submission_plan_v0(source_bridge_root=bridge_root, candidates=candidates)

    result_rows: List[Dict[str, Any]] = []
    ocr_results: List[Dict[str, Any]] = []
    any_bridge = False

    if not plan.get("submit_allowed"):
        errs.append("submission_not_allowed")

    selected = [c for c in candidates if isinstance(c, dict) and c.get("candidate_status") == "not_submitted"]

    for cand in selected:
        cid = str(cand.get("candidate_id") or "")
        ocr_dict = cand.get("ocr_request") if isinstance(cand.get("ocr_request"), dict) else {}
        req = _ocr_request_from_candidate_dict(ocr_dict)
        ocr_request_id = str(ocr_dict.get("request_id") or req.request_id)

        row: Dict[str, Any] = {
            "candidate_id": cid,
            "source_frame_id": str(cand.get("source_frame_id") or ""),
            "roi_id": str(cand.get("roi_id") or ""),
            "roi_type": str(cand.get("roi_type") or ""),
            "crop_image_ref": str(cand.get("crop_image_ref") or ""),
            "ocr_request_id": ocr_request_id,
            "submission_status": "skipped",
            "ocr_bridge_status": None,
            "selected_provider": None,
            "selected_provider_level": None,
            "real_provider_invoked": False,
            "rapidocr_runtime_provider_enabled": plan.get("rapidocr_runtime_provider_enabled"),
            "rapidocr_invoked": False,
            "paddleocr_invoked": False,
            "fallback_to_stub": False,
            "bridge_pack_ref": None,
            "evidence_text_joined": "",
            "text_item_count": 0,
            "empty_text": True,
            "provider_latency_ms": None,
            "error": None,
        }

        if not plan.get("submit_allowed"):
            row["submission_status"] = "blocked_by_gate"
            row["error"] = "submit_not_allowed"
            result_rows.append(row)
            continue

        crop = Path(str(cand.get("crop_image_ref") or ""))
        if not crop.is_file():
            row["submission_status"] = "failed"
            row["error"] = "crop_image_ref_missing"
            errs.append(f"missing_crop:{cid}")
            result_rows.append(row)
            continue

        work_dir = (submission_work_root / cid).resolve()
        work_dir.mkdir(parents=True, exist_ok=True)
        any_bridge = True

        try:
            bridge_result = run_ocr_mainline_bridge_v0(
                req,
                governance_config_path=governance_config_path,
                workspace_root=workspace_root,
                normalization_work_dir=work_dir / "norm",
            )
        except Exception as e:
            row["submission_status"] = "failed"
            row["ocr_bridge_status"] = "exception"
            row["error"] = f"{type(e).__name__}:{e}"
            errs.append(f"bridge_exception:{cid}")
            result_rows.append(row)
            continue

        bridge_path = work_dir / "ocr_mainline_bridge_result.json"
        _write_json(bridge_path, bridge_result)
        bp = bridge_result.get("bridge_pack") if isinstance(bridge_result.get("bridge_pack"), dict) else {}
        if bp:
            _write_json(work_dir / "ocr_bridge_pack.json", bp)

        fields = _bridge_row_fields(bridge_result)
        row.update(fields)
        row["ocr_bridge_status"] = str(bridge_result.get("status") or "")
        prov = bridge_result.get("provider_result") if isinstance(bridge_result.get("provider_result"), dict) else {}
        if prov.get("latency_ms") is not None:
            row["provider_latency_ms"] = prov.get("latency_ms")

        st = row["ocr_bridge_status"]
        if st == "success":
            row["submission_status"] = "submitted"
            row["bridge_pack_ref"] = str((work_dir / "ocr_bridge_pack.json").resolve())
        elif st == "rejected":
            row["submission_status"] = "rejected_by_gate"
            row["bridge_pack_ref"] = str(bridge_path.resolve())
            row["error"] = "input_gate_reject"
        else:
            row["submission_status"] = "failed"
            row["bridge_pack_ref"] = str(bridge_path.resolve())
            row["error"] = str(bridge_result.get("error") or st)

        ocr_results.append(
            {
                "candidate_id": cid,
                "roi_id": row["roi_id"],
                "ocr_request_id": ocr_request_id,
                "submission_status": row["submission_status"],
                "ocr_bridge_status": row["ocr_bridge_status"],
                "selected_provider": row["selected_provider"],
                "real_provider_invoked": row["real_provider_invoked"],
                "rapidocr_invoked": row["rapidocr_invoked"],
                "fallback_to_stub": row["fallback_to_stub"],
                "bridge_pack_ref": row["bridge_pack_ref"],
                "ocr_evidence": bridge_result.get("ocr_evidence"),
                "bridge_pack": bp,
            }
        )
        result_rows.append(row)

    success_count = sum(1 for r in result_rows if r.get("submission_status") == "submitted")
    failed_count = len(result_rows) - success_count
    rapidocr_success_count = sum(
        1
        for r in result_rows
        if r.get("submission_status") == "submitted" and r.get("rapidocr_invoked") and not r.get("fallback_to_stub")
    )
    stub_fallback_count = sum(1 for r in result_rows if r.get("fallback_to_stub"))
    empty_text_count = sum(1 for r in result_rows if r.get("submission_status") == "submitted" and r.get("empty_text"))

    collection = {
        "schema_version": COLLECTION_SCHEMA,
        "source": "vision_roi_to_ocr_request_bridge",
        "source_bridge_root": str(bridge_root),
        "submission_count": len(result_rows),
        "success_count": success_count,
        "failed_count": failed_count,
        "rapidocr_success_count": rapidocr_success_count,
        "stub_fallback_count": stub_fallback_count,
        "empty_text_count": empty_text_count,
        "ocr_results": ocr_results,
    }

    matrix = {"schema_version": MATRIX_SCHEMA, "row_count": len(result_rows), "rows": result_rows}
    provider_summary = build_provider_summary_v0(result_rows)
    audit = build_rapidocr_submission_audit_v0(result_rows=result_rows, any_bridge_invoked=any_bridge)

    phase_verdict = "GO"
    if rapidocr_success_count <= 0 and stub_fallback_count > 0:
        phase_verdict = "CONDITIONAL_GO"
    if success_count <= 0 and result_rows:
        phase_verdict = "CONDITIONAL_GO"
    if success_count > 0 and (rapidocr_success_count > 0 or any(r.get("real_provider_invoked") for r in result_rows)):
        phase_verdict = "GO"
    if errs and success_count <= 0:
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-OCR-Real-RapidOCR-Submission-From-Vision-ROI-Gated-001",
        "vision_roi_to_ocr_bridge_root": str(bridge_root),
        "workspace_root": str(workspace_root.resolve()),
        "governance_config_path": str(governance_config_path.resolve()),
        "candidate_count": int(plan.get("candidate_count") or 0),
        "selected_candidate_count": int(plan.get("selected_candidate_count") or 0),
        "submission_count": len(result_rows),
        "success_count": success_count,
        "rapidocr_success_count": rapidocr_success_count,
        "stub_fallback_count": stub_fallback_count,
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return summary, plan, matrix, collection, provider_summary, audit, errs

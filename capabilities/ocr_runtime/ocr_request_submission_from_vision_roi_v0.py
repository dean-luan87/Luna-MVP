# -*- coding: utf-8 -*-
"""Gated OCRRequest submission from Vision ROI bridge candidates (eval-only).

Phase-OCR-Request-Submission-Gated-Smoke-001
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.ocr_runtime.ocr_mainline_bridge_v0 import run_ocr_mainline_bridge_v0
from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

PLAN_SCHEMA = "ocr_request_submission_plan_from_vision_roi_v0"
MATRIX_SCHEMA = "ocr_request_submission_result_matrix_v0"
COLLECTION_SCHEMA = "ocr_submission_from_vision_roi_collection_v0"
AUDIT_SCHEMA = "ocr_request_submission_from_vision_roi_audit_v0"
SUMMARY_SCHEMA = "ocr_request_submission_from_vision_roi_summary_v0"


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


def _bridge_audit_flags(bridge_result: Dict[str, Any]) -> Dict[str, bool]:
    aud = bridge_result.get("audit") if isinstance(bridge_result.get("audit"), dict) else {}
    sel = bridge_result.get("provider_selection_report") if isinstance(bridge_result.get("provider_selection_report"), dict) else {}
    provider = str((bridge_result.get("ocr_evidence") or {}).get("provider") or sel.get("selected_provider") or "")
    status = str(bridge_result.get("status") or "")
    stub_invoked = status == "success" and provider in ("ocr_stub", "stub")
    return {
        "ocr_provider_invoked": stub_invoked or bool(aud.get("fallback_to_stub")),
        "rapidocr_invoked": bool(aud.get("rapidocr_runtime_provider_enabled")),
        "paddleocr_invoked": bool(aud.get("paddleocr_invoked")) or bool(aud.get("paddleocr_runtime_provider_enabled")),
        "real_provider_invoked": bool(aud.get("real_provider_invoked")),
    }


def build_submission_plan_v0(
    *,
    source_bridge_root: Path,
    candidates: List[Dict[str, Any]],
    ocr_provider_mode: str = "stub",
) -> Dict[str, Any]:
    reason_codes: List[str] = []
    gates_ok = True

    if not _env_true("LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0", "false"):
        gates_ok = False
        reason_codes.append("gate_disabled:LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0")
    if not _env_true("LUNA_ENABLE_OCR_STUB_PROVIDER_V0", "true") and ocr_provider_mode == "stub":
        gates_ok = False
        reason_codes.append("gate_disabled:LUNA_ENABLE_OCR_STUB_PROVIDER_V0")
    if _env_true("LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0", "false"):
        reason_codes.append("paddle_runtime_explicitly_disabled")
    if not _env_true("LUNA_OCR_SUBMISSION_EVAL_ONLY", "false"):
        reason_codes.append("eval_only_flag_not_set:LUNA_OCR_SUBMISSION_EVAL_ONLY")
    else:
        reason_codes.append("eval_only:LUNA_OCR_SUBMISSION_EVAL_ONLY")

    if _env_true("LUNA_ENABLE_OCR_REAL_PROVIDER_V0", "false"):
        reason_codes.append("real_provider_disabled_by_default")
    if _env_true("LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0", "false"):
        reason_codes.append("rapidocr_runtime_disabled")

    selected = [c for c in candidates if isinstance(c, dict) and c.get("candidate_status") == "not_submitted"]
    if not selected:
        reason_codes.append("no_not_submitted_candidates")

    return {
        "schema_version": PLAN_SCHEMA,
        "source_bridge_root": str(source_bridge_root.resolve()),
        "candidate_count": len(candidates),
        "selected_candidate_count": len(selected),
        "submission_mode": "gated_eval_only",
        "ocr_provider_mode": ocr_provider_mode,
        "submit_allowed": gates_ok and len(selected) > 0,
        "reason_codes": reason_codes,
    }


def build_submission_audit_v0(
    *,
    result_rows: List[Dict[str, Any]],
    any_bridge_invoked: bool,
) -> Dict[str, Any]:
    agg = {
        "ocr_provider_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "real_provider_invoked": False,
    }
    for row in result_rows:
        if row.get("ocr_provider_invoked") is True:
            agg["ocr_provider_invoked"] = True
        if row.get("rapidocr_invoked") is True:
            agg["rapidocr_invoked"] = True
        if row.get("paddleocr_invoked") is True:
            agg["paddleocr_invoked"] = True

    return {
        "schema": AUDIT_SCHEMA,
        "ocr_request_submission_executed": True,
        "eval_only": _env_true("LUNA_OCR_SUBMISSION_EVAL_ONLY", "false"),
        "ocr_mainline_bridge_invoked": any_bridge_invoked,
        "ocr_provider_invoked": agg["ocr_provider_invoked"],
        "rapidocr_invoked": agg["rapidocr_invoked"],
        "paddleocr_invoked": agg["paddleocr_invoked"],
        "vision_runtime_modified": False,
        "vision_provider_registry_default_changed": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "cross_modal_fusion_invoked": False,
    }


def run_ocr_request_submission_from_vision_roi_v0(
    *,
    vision_roi_to_ocr_bridge_root: str,
    workspace_root: Path,
    governance_config_path: Path,
    submission_work_root: Path,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    errs: List[str] = []
    bridge_root = Path(vision_roi_to_ocr_bridge_root).resolve()
    cand_p = bridge_root / "vision_roi_to_ocr_request_candidates.json"
    if not cand_p.is_file():
        return (
            {"schema_version": SUMMARY_SCHEMA, "errors": ["missing:vision_roi_to_ocr_request_candidates.json"]},
            {},
            {},
            {},
            build_submission_audit_v0(result_rows=[], any_bridge_invoked=False),
            ["missing_candidates_file"],
        )

    cand_doc = _read_json(cand_p)
    candidates = cand_doc.get("candidates") if isinstance(cand_doc.get("candidates"), list) else []
    plan = build_submission_plan_v0(source_bridge_root=bridge_root, candidates=candidates)

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
            "ocr_provider_invoked": False,
            "rapidocr_invoked": False,
            "paddleocr_invoked": False,
            "bridge_pack_ref": None,
            "evidence_text_joined": "",
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

        flags = _bridge_audit_flags(bridge_result)
        row.update(flags)
        row["ocr_bridge_status"] = str(bridge_result.get("status") or "")
        ev = bridge_result.get("ocr_evidence") if isinstance(bridge_result.get("ocr_evidence"), dict) else {}
        row["evidence_text_joined"] = str(ev.get("text_joined") or "")

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
                "bridge_pack_ref": row["bridge_pack_ref"],
                "ocr_evidence": ev,
                "bridge_pack": bp,
            }
        )
        result_rows.append(row)

    success_count = sum(1 for r in result_rows if r.get("submission_status") == "submitted")
    failed_count = len(result_rows) - success_count

    collection = {
        "schema_version": COLLECTION_SCHEMA,
        "source": "vision_roi_to_ocr_request_bridge",
        "source_bridge_root": str(bridge_root),
        "submission_count": len(result_rows),
        "success_count": success_count,
        "failed_count": failed_count,
        "ocr_results": ocr_results,
    }

    matrix = {
        "schema_version": MATRIX_SCHEMA,
        "row_count": len(result_rows),
        "rows": result_rows,
    }

    audit = build_submission_audit_v0(result_rows=result_rows, any_bridge_invoked=any_bridge)

    phase_verdict = "GO"
    if success_count <= 0 and result_rows:
        phase_verdict = "CONDITIONAL_GO"
    if not result_rows and not plan.get("submit_allowed"):
        phase_verdict = "CONDITIONAL_GO"
    if errs and success_count <= 0:
        phase_verdict = "NO_GO" if not result_rows else phase_verdict

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-OCR-Request-Submission-Gated-Smoke-001",
        "vision_roi_to_ocr_bridge_root": str(bridge_root),
        "workspace_root": str(workspace_root.resolve()),
        "governance_config_path": str(governance_config_path.resolve()),
        "candidate_count": int(plan.get("candidate_count") or 0),
        "selected_candidate_count": int(plan.get("selected_candidate_count") or 0),
        "submission_count": len(result_rows),
        "success_count": success_count,
        "failed_count": failed_count,
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return summary, plan, matrix, collection, audit, errs

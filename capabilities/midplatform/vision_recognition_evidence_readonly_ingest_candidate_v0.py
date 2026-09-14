# -*- coding: utf-8 -*-
"""MidPlatform Vision recognition evidence read-only ingest candidate (evaluation).

No MidPlatform fact writes, no Scene Delta, no WorldModel, no AI interpretation,
no navigation, no real vision / YOLO / Supervision mainline / VLM / OCR.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple

INGEST_CANDIDATE_SCHEMA = "midplatform_vision_recognition_ingest_candidate_v0"
INGEST_AUDIT_SCHEMA = "midplatform_vision_recognition_ingest_audit_v0"

KNOWN_ROI_TYPE_SUFFIXES: Tuple[str, ...] = (
    "center_roi",
    "ground_roi",
    "upper_sign_roi",
    "left_roi",
    "right_roi",
)


def roi_type_from_roi_id_v0(roi_id: str) -> str:
    rid = str(roi_id or "")
    for suf in KNOWN_ROI_TYPE_SUFFIXES:
        if rid.endswith("_" + suf):
            return suf
    return "unknown_roi_type"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_evidence_pack_root_v0(consumer_root: Path) -> Path:
    """Use consumer summary's ``vision_recognition_evidence_pack_root`` when present."""
    sum_p = consumer_root / "vision_recognition_evidence_readonly_consumer_summary.json"
    if sum_p.is_file():
        data = _read_json(sum_p)
        ref = str(data.get("vision_recognition_evidence_pack_root") or "").strip()
        if ref:
            return Path(ref).resolve()
    raise FileNotFoundError(
        f"missing or empty vision_recognition_evidence_pack_root in {sum_p} "
        "(required to load per-item evidence matrix for ingest rows)"
    )


def build_midplatform_vision_recognition_ingest_matrix_v0(
    evidence_matrix_rows: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for r in evidence_matrix_rows:
        if not isinstance(r, dict):
            continue
        roi_id = str(r.get("roi_id") or "")
        rows.append(
            {
                "evidence_id": str(r.get("evidence_id") or ""),
                "source_frame_id": str(r.get("source_frame_id") or ""),
                "roi_id": roi_id,
                "roi_type": roi_type_from_roi_id_v0(roi_id),
                "label": str(r.get("label") or ""),
                "confidence": r.get("confidence"),
                "synthetic": r.get("synthetic"),
                "stub_provider": r.get("stub_provider"),
                "fact_status": str(r.get("fact_status") or ""),
                "bbox_in_frame": r.get("bbox_in_frame"),
            }
        )
    return rows


def build_midplatform_vision_recognition_ingest_candidate_v0(
    *,
    consumer_view: Dict[str, Any],
    by_frame_matrix: Dict[str, Any],
    by_roi_matrix: Dict[str, Any],
    geometry_summary: Dict[str, Any],
    source_consumer_view_ref: str,
) -> Tuple[Dict[str, Any], List[str]]:
    errs: List[str] = []
    if not str(source_consumer_view_ref or "").strip():
        errs.append("missing_source_consumer_view_ref")

    n = int(consumer_view.get("evidence_count_observed") or 0)
    if n < 1:
        errs.append("evidence_count_lt_1")

    prov = str(consumer_view.get("provider") or "")
    pl = str(consumer_view.get("provider_level") or "")
    if prov != "vision_stub":
        errs.append("provider_must_be_vision_stub")
    if pl != "stub":
        errs.append("provider_level_must_be_stub")

    fs = consumer_view.get("fact_status_summary") or {}
    if int(fs.get("not_fact") or 0) != n:
        errs.append("fact_status_summary_not_fact_mismatch")

    syn = consumer_view.get("synthetic_summary") or {}
    if int(syn.get("synthetic_count") or 0) != n:
        errs.append("synthetic_count_mismatch")
    if int(syn.get("stub_provider_count") or 0) != n:
        errs.append("stub_provider_count_mismatch")

    by_f = consumer_view.get("evidence_by_frame")
    if not isinstance(by_f, dict) or not by_f:
        errs.append("evidence_by_frame_empty")

    by_r = consumer_view.get("evidence_by_roi_type")
    if not isinstance(by_r, dict) or not by_r:
        errs.append("evidence_by_roi_type_empty")

    if not isinstance(geometry_summary, dict) or not geometry_summary:
        errs.append("geometry_summary_empty")

    scs = consumer_view.get("source_chain_summary")
    if not isinstance(scs, dict):
        errs.append("source_chain_summary_missing")

    if not isinstance(by_frame_matrix.get("rows"), list):
        errs.append("by_frame_matrix_rows_missing")
    if not isinstance(by_roi_matrix.get("rows"), list):
        errs.append("by_roi_matrix_rows_missing")

    candidate: Dict[str, Any] = {
        "schema_version": INGEST_CANDIDATE_SCHEMA,
        "candidate_id": f"mp_vision_ingest_{uuid.uuid4().hex}",
        "source": "vision_recognition_evidence_pack",
        "source_consumer_view_ref": str(source_consumer_view_ref),
        "ingest_scope": "read_only_candidate",
        "evidence_count": n,
        "provider": prov,
        "provider_level": pl,
        "fact_status_summary": dict(fs) if isinstance(fs, dict) else {},
        "synthetic_summary": dict(syn) if isinstance(syn, dict) else {},
        "evidence_by_frame": by_f if isinstance(by_f, dict) else {},
        "evidence_by_roi_type": by_r if isinstance(by_r, dict) else {},
        "geometry_summary": geometry_summary,
        "source_chain_summary": scs if isinstance(scs, dict) else {},
        "allowed_next_actions": [
            "manual_review",
            "vision_scene_delta_candidate_later",
            "real_provider_retest_later",
        ],
        "forbidden_actions": {
            "write_midplatform_fact": True,
            "write_scene_delta": True,
            "write_world_model": True,
            "invoke_ai_interpretation": True,
            "invoke_navigation_decision": True,
            "invoke_real_vision_provider": True,
        },
    }
    return candidate, errs


def build_midplatform_vision_recognition_ingest_source_chain_summary_v0(
    consumer_view: Dict[str, Any],
) -> Dict[str, Any]:
    scs = consumer_view.get("source_chain_summary") or {}
    return {
        "schema": "midplatform_vision_recognition_ingest_source_chain_summary_v0",
        "upstream_source_chain": scs if isinstance(scs, dict) else {},
        "midplatform_ingest_layer": "readonly_candidate_v0",
    }


def build_midplatform_vision_recognition_ingest_audit_v0() -> Dict[str, Any]:
    return {
        "schema": INGEST_AUDIT_SCHEMA,
        "midplatform_vision_ingest_candidate_generated": True,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "real_vision_provider_invoked": False,
        "yolo_invoked": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
    }


def build_midplatform_vision_recognition_ingest_summary_v0(
    *,
    input_consumer_root: str,
    candidate: Dict[str, Any],
    validation_errors: List[str],
    ingest_candidate_path: str,
) -> Dict[str, Any]:
    return {
        "schema": "midplatform_vision_recognition_ingest_candidate_summary_v0",
        "phase": "Phase-MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001",
        "input_vision_readonly_consumer_root": input_consumer_root,
        "candidate_id": candidate.get("candidate_id"),
        "ingest_candidate_path": ingest_candidate_path,
        "validation_ok": len(validation_errors) == 0,
        "validation_errors": list(validation_errors),
        "evidence_count": candidate.get("evidence_count"),
        "ingest_scope": candidate.get("ingest_scope"),
    }


def run_midplatform_vision_recognition_readonly_ingest_candidate_bundle_v0(
    consumer_root: Path,
) -> Dict[str, Any]:
    """Load consumer artifacts + evidence matrix; return all midplatform bundle parts."""
    root = consumer_root.resolve()
    view_p = root / "vision_recognition_evidence_readonly_consumer_view.json"
    bfm_p = root / "vision_recognition_evidence_by_frame_matrix.json"
    brm_p = root / "vision_recognition_evidence_by_roi_matrix.json"
    geom_p = root / "vision_recognition_evidence_geometry_summary.json"
    caud_p = root / "vision_recognition_evidence_readonly_consumer_audit_report.json"

    for p in (view_p, bfm_p, brm_p, geom_p, caud_p):
        if not p.is_file():
            raise FileNotFoundError(p)

    pack_root = resolve_evidence_pack_root_v0(root)
    emx_p = pack_root / "vision_recognition_evidence_matrix.json"
    if not emx_p.is_file():
        raise FileNotFoundError(emx_p)

    view = _read_json(view_p)
    bfm = _read_json(bfm_p)
    brm = _read_json(brm_p)
    geom = _read_json(geom_p)
    _read_json(caud_p)

    emx = _read_json(emx_p)
    matrix_rows = emx.get("rows") if isinstance(emx.get("rows"), list) else []
    ingest_rows = build_midplatform_vision_recognition_ingest_matrix_v0(
        [r for r in matrix_rows if isinstance(r, dict)]
    )

    candidate, val_errs = build_midplatform_vision_recognition_ingest_candidate_v0(
        consumer_view=view if isinstance(view, dict) else {},
        by_frame_matrix=bfm if isinstance(bfm, dict) else {},
        by_roi_matrix=brm if isinstance(brm, dict) else {},
        geometry_summary=geom if isinstance(geom, dict) else {},
        source_consumer_view_ref=str(view_p.resolve()),
    )

    chain_out = build_midplatform_vision_recognition_ingest_source_chain_summary_v0(
        view if isinstance(view, dict) else {}
    )
    audit = build_midplatform_vision_recognition_ingest_audit_v0()

    return {
        "candidate": candidate,
        "ingest_matrix": {"schema": "midplatform_vision_recognition_ingest_matrix_v0", "rows": ingest_rows},
        "source_chain_summary": chain_out,
        "audit": audit,
        "validation_errors": val_errs,
        "input_paths": {
            "vision_recognition_evidence_readonly_consumer_view.json": str(view_p),
            "vision_recognition_evidence_by_frame_matrix.json": str(bfm_p),
            "vision_recognition_evidence_by_roi_matrix.json": str(brm_p),
            "vision_recognition_evidence_geometry_summary.json": str(geom_p),
            "vision_recognition_evidence_readonly_consumer_audit_report.json": str(caud_p),
            "vision_recognition_evidence_matrix.json": str(emx_p),
        },
    }

# -*- coding: utf-8 -*-
"""Scene Delta generic executor prechain closure (OCR + Vision).

Phase-MidPlatform-SceneDelta-Generic-Chain-Closure-001 — read-only aggregation; no executor; no writes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CHAIN_CLOSURE_SCHEMA = "scene_delta_generic_chain_closure_v0"
SUPPORTED_SOURCE_TYPES = ("ocr_evidence", "vision_recognition_evidence")

DEFAULT_GENERIC_CHAIN_ROOTS: Dict[str, Dict[str, str]] = {
    "vision_recognition_evidence": {
        "dryrun_root": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_dryrun_from_vision_smoke_v0",
        "generic_trace_root": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_trace_stub_from_generic_dryrun_vision_smoke_v0",
        "generic_mock_handshake_root": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_mock_handshake_generic_vision_smoke_v0",
        "generic_contract_conformance_root": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_contract_conformance_generic_vision_smoke_v0",
    },
    "ocr_evidence": {
        "dryrun_root": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_dryrun_verifier_smoke_v0",
        "generic_trace_root": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_trace_stub_from_generic_dryrun_ocr_smoke_v0",
        "generic_mock_handshake_root": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_mock_handshake_generic_ocr_smoke_v0",
        "generic_contract_conformance_root": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_contract_conformance_generic_ocr_smoke_v0",
    },
}

LAYER_VERIFIER_FILES: Dict[str, str] = {
    "dryrun": "",  # resolved per source_type
    "generic_trace": "scene_delta_executor_trace_stub_generic_verifier_report.json",
    "generic_mock_handshake": "scene_delta_mock_handshake_generic_verifier_report.json",
    "generic_contract_conformance": "scene_delta_executor_contract_conformance_generic_verifier_report.json",
}

DRYRUN_VERIFIER_BY_SOURCE: Dict[str, str] = {
    "vision_recognition_evidence": "scene_delta_write_candidate_dryrun_from_vision_verifier_report.json",
    "ocr_evidence": "scene_delta_write_candidate_dryrun_verifier_report.json",
}

NO_WRITE_BOUNDARY_KEYS = (
    "scene_delta_executor_invoked",
    "scene_delta_written",
    "database_write_invoked",
    "rehearsal_log_written",
    "wal_append_invoked",
    "midplatform_fact_written",
    "world_model_written",
    "ai_interpretation_invoked",
    "navigation_decision_invoked",
    "ocr_provider_invoked",
    "ocr_routing_changed",
    "real_vision_provider_invoked",
    "yolo_invoked",
    "supervision_mainline_invoked",
    "vlm_invoked",
)


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _safe_read(p: Path) -> Optional[Any]:
    if not p.is_file():
        return None
    try:
        return _read_json(p)
    except Exception:
        return None


def _verifier_at(root: Path, rel: str) -> Tuple[Optional[str], List[str]]:
    if not rel:
        return None, ["verifier_file_not_configured"]
    vp = root / rel
    if not vp.is_file():
        return None, [f"missing_verifier:{vp}"]
    rep = _safe_read(vp)
    if not isinstance(rep, dict):
        return None, ["verifier_invalid"]
    verdict = str(rep.get("verdict") or "")
    blockers = list(rep.get("blockers") or []) if isinstance(rep.get("blockers"), list) else []
    return verdict, blockers


def build_generic_chain_phase_matrix_v0(roots_by_source: Dict[str, Dict[str, str]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for source_type in SUPPORTED_SOURCE_TYPES:
        cfg = roots_by_source.get(source_type) or {}
        dr = Path(cfg.get("dryrun_root") or "")
        tr = Path(cfg.get("generic_trace_root") or "")
        mh = Path(cfg.get("generic_mock_handshake_root") or "")
        cf = Path(cfg.get("generic_contract_conformance_root") or "")

        dry_v, dry_b = _verifier_at(dr, DRYRUN_VERIFIER_BY_SOURCE[source_type])
        trace_v, trace_b = _verifier_at(tr, LAYER_VERIFIER_FILES["generic_trace"])
        mock_v, mock_b = _verifier_at(mh, LAYER_VERIFIER_FILES["generic_mock_handshake"])
        conf_v, conf_b = _verifier_at(cf, LAYER_VERIFIER_FILES["generic_contract_conformance"])

        layer_verdicts = {
            "dryrun": dry_v,
            "generic_trace": trace_v,
            "generic_mock_handshake": mock_v,
            "generic_contract_conformance": conf_v,
        }
        all_blockers = list(dry_b) + list(trace_b) + list(mock_b) + list(conf_b)
        all_go = all(v == "GO" for v in layer_verdicts.values() if v is not None)

        rows.append(
            {
                "source_type": source_type,
                "dryrun_root": str(dr),
                "generic_trace_root": str(tr),
                "generic_mock_handshake_root": str(mh),
                "generic_contract_conformance_root": str(cf),
                "layer_verifier_verdicts": layer_verdicts,
                "blockers": all_blockers,
                "status": "ok" if all_go and not all_blockers else "check_required",
            }
        )
    return rows


def _dryrun_summary_path(source_type: str) -> str:
    if source_type == "vision_recognition_evidence":
        return "scene_delta_write_candidate_dryrun_from_vision_summary.json"
    return "scene_delta_write_candidate_dryrun_summary.json"


def build_generic_lineage_matrix_v0(roots_by_source: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = []
    for source_type in SUPPORTED_SOURCE_TYPES:
        cfg = roots_by_source.get(source_type) or {}
        dr = Path(cfg.get("dryrun_root") or "")
        tr = Path(cfg.get("generic_trace_root") or "")
        mh = Path(cfg.get("generic_mock_handshake_root") or "")
        cf = Path(cfg.get("generic_contract_conformance_root") or "")

        dsum = _safe_read(dr / _dryrun_summary_path(source_type))
        tst = _safe_read(tr / "scene_delta_executor_trace_stub_generic.json")
        tsum = _safe_read(tr / "scene_delta_executor_trace_stub_generic_summary.json")
        mreq = _safe_read(mh / "scene_delta_mock_executor_request_generic.json")
        mack = _safe_read(mh / "scene_delta_mock_executor_ack_generic.json")
        csum = _safe_read(cf / "scene_delta_executor_contract_conformance_generic_summary.json")
        gap = _safe_read(cf / "scene_delta_executor_contract_gap_report_generic.json")

        evidence_count = None
        if isinstance(dsum, dict):
            evidence_count = dsum.get("evidence_count")

        entries.append(
            {
                "source_type": source_type,
                "dry_run_id": (dsum or {}).get("dry_run_id") if isinstance(dsum, dict) else None,
                "source_candidate_id": (dsum or {}).get("source_candidate_id")
                if isinstance(dsum, dict)
                else (tst or {}).get("source_candidate_id") if isinstance(tst, dict) else None,
                "trace_id": (tst or {}).get("trace_id") if isinstance(tst, dict) else (tsum or {}).get("trace_id"),
                "mock_request_id": (mreq or {}).get("request_id") if isinstance(mreq, dict) else None,
                "mock_ack_id": (mack or {}).get("ack_id") if isinstance(mack, dict) else None,
                "contract_reference_mode": (csum or {}).get("contract_reference_mode")
                if isinstance(csum, dict)
                else (gap or {}).get("contract_reference_mode") if isinstance(gap, dict) else None,
                "conformance_level": (gap or {}).get("conformance_level") if isinstance(gap, dict) else None,
                "evidence_count": evidence_count,
            }
        )

    return {"schema": "scene_delta_generic_chain_lineage_matrix_v0", "entries": entries}


def _audit_paths_for_source(source_type: str, cfg: Dict[str, str]) -> List[Tuple[str, Path]]:
    dr = Path(cfg.get("dryrun_root") or "")
    tr = Path(cfg.get("generic_trace_root") or "")
    mh = Path(cfg.get("generic_mock_handshake_root") or "")
    cf = Path(cfg.get("generic_contract_conformance_root") or "")

    if source_type == "vision_recognition_evidence":
        dry_audit = dr / "scene_delta_write_candidate_from_vision_no_write_audit_report.json"
    else:
        dry_audit = dr / "scene_delta_write_candidate_no_write_audit_report.json"

    return [
        ("dryrun", dry_audit),
        ("generic_trace", tr / "scene_delta_executor_trace_stub_generic_audit_report.json"),
        ("generic_mock_handshake", mh / "scene_delta_mock_handshake_audit_report_generic.json"),
        ("generic_contract_conformance", cf / "scene_delta_executor_contract_conformance_audit_report_generic.json"),
    ]


def build_generic_no_write_boundary_matrix_v0(
    roots_by_source: Dict[str, Dict[str, str]],
) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    violations: List[str] = []

    for source_type in SUPPORTED_SOURCE_TYPES:
        cfg = roots_by_source.get(source_type) or {}
        layer_audits: Dict[str, Dict[str, Any]] = {}
        for layer, apath in _audit_paths_for_source(source_type, cfg):
            aud = _safe_read(apath)
            layer_audits[layer] = aud if isinstance(aud, dict) else {}

        row: Dict[str, Any] = {"source_type": source_type, "layer_audits_present": {k: bool(v) for k, v in layer_audits.items()}}

        for key in NO_WRITE_BOUNDARY_KEYS:
            key_ok = True
            for layer, aud in layer_audits.items():
                if key not in aud:
                    continue
                if aud.get(key) is not False:
                    key_ok = False
                    violations.append(f"{source_type}:{layer}:{key}={aud.get(key)}")
            row[key] = key_ok

        rows.append(row)

    return {
        "schema": "scene_delta_generic_no_write_boundary_matrix_v0",
        "rows": rows,
        "violations": violations,
        "boundary_ok": len(violations) == 0,
    }


def build_generic_capability_closure_report_v0() -> Dict[str, Any]:
    return {
        "schema": "scene_delta_generic_capability_closure_report_v0",
        "capabilities_proven": [
            "OCR and Vision dry-run outputs can feed generic executor trace stub (auto-detect dry-run schema).",
            "Generic trace stub (trace_stub_only, no_write_guarantee) feeds generic mock handshake for both source_type values.",
            "Generic mock request/ACK pass local_skeleton contract conformance for ocr_evidence and vision_recognition_evidence.",
            "End-to-end generic prechain maintains no-write across dry-run, trace stub, mock handshake, and contract conformance audits.",
            "source_type is preserved and distinguishable through lineage (dry_run_id, trace_id, mock_request_id, mock_ack_id).",
            "Legacy OCR-only executor prechain scripts remain for compatibility; new work should default to generic paths.",
        ],
        "recommended_default_path": "generic",
        "legacy_ocr_only_path": "retained_for_compatibility_not_default",
    }


def build_generic_non_claims_report_v0() -> Dict[str, Any]:
    return {
        "schema": "scene_delta_generic_non_claims_report_v0",
        "claims": {
            "production_scene_delta_executor_available": False,
            "production_openapi_or_proto_aligned": False,
            "scene_delta_write_path_production_ready": False,
            "database_write_available": False,
            "wal_or_rehearsal_log_write_available": False,
            "midplatform_fact_write_available": False,
            "world_model_write_available": False,
            "ai_interpretation_available": False,
            "navigation_decision_available": False,
            "real_ocr_provider_available_on_this_chain": False,
            "real_vision_provider_available_on_this_chain": False,
        },
        "narrative": [
            "This generic chain closure does NOT assert production Scene Delta executor availability.",
            "This generic chain closure does NOT assert production OpenAPI or proto contract alignment.",
            "This generic chain closure does NOT assert Scene Delta write path is enabled.",
            "This generic chain closure does NOT assert database, WAL, or rehearsal log writes.",
            "This generic chain closure does NOT assert MidPlatform fact or WorldModel writes.",
            "This generic chain closure does NOT assert AI interpretation or navigation decision on this chain.",
            "This generic chain closure does NOT assert real OCR or Vision provider invocation on this prechain.",
        ],
    }


def build_generic_open_followups_v0() -> Dict[str, Any]:
    return {
        "schema": "scene_delta_generic_open_followups_v0",
        "items": [
            "Import real Scene Delta executor OpenAPI / proto and bind conformance beyond local_skeleton.",
            "Upgrade generic contract conformance from local_skeleton to production contract reference mode.",
            "Vision real provider gated adapter (YOLO / lightweight paths) with explicit no-write smoke gates.",
            "Supervision structure reference analysis (Phase Vision-Supervision-Structure-Reference-Analysis-001).",
            "Performance Controller integration on evidence → Scene Delta paths.",
            "CrossModal Evidence Fusion across OCR and Vision evidence packs.",
            "Vision ROI → OCRRequest bridge for shared spatial units.",
            "Generic chain closure re-run after each new generic prechain phase lands.",
        ],
    }


def run_generic_chain_closure_v0(
    roots_by_source: Dict[str, Dict[str, str]],
) -> Tuple[
    Dict[str, Any],
    List[Dict[str, Any]],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []

    for source_type in SUPPORTED_SOURCE_TYPES:
        cfg = roots_by_source.get(source_type)
        if not isinstance(cfg, dict):
            errs.append(f"missing_config:{source_type}")
            continue
        for key in ("dryrun_root", "generic_trace_root", "generic_mock_handshake_root", "generic_contract_conformance_root"):
            p = Path(str(cfg.get(key) or ""))
            if not p.is_dir():
                errs.append(f"missing_root_dir:{source_type}:{key}:{p}")

    phase_matrix = build_generic_chain_phase_matrix_v0(roots_by_source)
    for row in phase_matrix:
        st = row.get("source_type")
        lv = row.get("layer_verifier_verdicts") if isinstance(row.get("layer_verifier_verdicts"), dict) else {}
        for layer, verdict in lv.items():
            if verdict != "GO":
                errs.append(f"verdict_not_go:{st}:{layer}:{verdict}")
        if row.get("blockers"):
            errs.append(f"blockers_non_empty:{st}")

    lineage = build_generic_lineage_matrix_v0(roots_by_source)
    for ent in lineage.get("entries") if isinstance(lineage.get("entries"), list) else []:
        if not isinstance(ent, dict):
            continue
        st = ent.get("source_type")
        for key in ("dry_run_id", "source_candidate_id", "trace_id", "mock_ack_id", "contract_reference_mode"):
            if not str(ent.get(key) or "").strip():
                errs.append(f"lineage_missing:{st}:{key}")
        if str(ent.get("contract_reference_mode") or "") != "local_skeleton":
            errs.append(f"contract_reference_mode_not_local_skeleton:{st}")

    nw = build_generic_no_write_boundary_matrix_v0(roots_by_source)
    if not nw.get("boundary_ok"):
        errs.append("no_write_boundary_violations")

    summary = {
        "schema_version": "scene_delta_generic_chain_closure_summary_v0",
        "phase": "Phase-MidPlatform-SceneDelta-Generic-Chain-Closure-001",
        "chain_closure_schema": CHAIN_CLOSURE_SCHEMA,
        "source_types": list(SUPPORTED_SOURCE_TYPES),
        "roots_by_source": dict(roots_by_source),
        "errors": list(errs),
    }

    return (
        summary,
        phase_matrix,
        lineage,
        nw,
        build_generic_capability_closure_report_v0(),
        build_generic_non_claims_report_v0(),
        build_generic_open_followups_v0(),
        errs,
    )

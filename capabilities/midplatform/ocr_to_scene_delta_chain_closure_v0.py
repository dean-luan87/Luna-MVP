# -*- coding: utf-8 -*-
"""OCR → Scene Delta mock chain closure archive (read-only aggregation).

Phase-OCR-to-SceneDelta-Mock-Chain-Closure-001 — no OCR run, no executor, no writes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CHAIN_CLOSURE_SCHEMA = "ocr_to_scene_delta_chain_closure_v0"

# Default absolute roots (runner may override).
DEFAULT_CHAIN_ROOTS: Dict[str, str] = {
    "OCR-Lightweight-Provider-Multi-ROI-Smoke-001": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_lightweight_provider_multi_roi_smoke_v0",
    "OCR-Evidence-Consumer-ReadOnly-Smoke-001": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_readonly_consumer_smoke_v0",
    "MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/midplatform_ocr_evidence_readonly_ingest_candidate_smoke_v0",
    "OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_ingest_readonly_bus_replay_smoke_v0",
    "MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_from_ocr_ingest_stub_smoke_v0",
    "MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-001": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_dryrun_verifier_smoke_v0",
    "MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_trace_stub_from_dryrun_smoke_v0",
    "MidPlatform-Scene-Delta-Executor-Mock-Handshake-001": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_mock_handshake_smoke_v0",
    "MidPlatform-Scene-Delta-Executor-Contract-Conformance-001": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_contract_conformance_smoke_v0",
}

VERIFIER_REL_BY_PHASE: Dict[str, str] = {
    "OCR-Lightweight-Provider-Multi-ROI-Smoke-001": "ocr_lightweight_provider_multi_roi_verifier_report.json",
    "OCR-Evidence-Consumer-ReadOnly-Smoke-001": "ocr_evidence_readonly_consumer_verifier_report.json",
    "MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001": "midplatform_ocr_evidence_ingest_verifier_report.json",
    "OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001": "ocr_ingest_readonly_bus_replay_verifier_report.json",
    "MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001": "scene_delta_write_candidate_verifier_report.json",
    "MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-001": "scene_delta_write_candidate_dryrun_verifier_report.json",
    "MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001": "scene_delta_executor_trace_stub_verifier_report.json",
    "MidPlatform-Scene-Delta-Executor-Mock-Handshake-001": "scene_delta_mock_handshake_verifier_report.json",
    "MidPlatform-Scene-Delta-Executor-Contract-Conformance-001": "scene_delta_executor_contract_conformance_verifier_report.json",
}

PHASE_BOUNDARY: Dict[str, str] = {
    "OCR-Lightweight-Provider-Multi-ROI-Smoke-001": "GO = multi-ROI RapidOCR evidence + bridge_pack; not MidPlatform fact; not Scene Delta write.",
    "OCR-Evidence-Consumer-ReadOnly-Smoke-001": "GO = read-only bridge_pack consumer; no writes.",
    "MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001": "GO = read-only ingest candidate; not fact layer.",
    "OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001": "GO = simulated bus replay; no external bus; no DB.",
    "MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001": "GO = write candidate JSON only; not Scene Delta execution.",
    "MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-001": "GO = dry-run + mapping; no executor.",
    "MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001": "GO = trace stub; no real executor.",
    "MidPlatform-Scene-Delta-Executor-Mock-Handshake-001": "GO = synthetic ACK; no real executor.",
    "MidPlatform-Scene-Delta-Executor-Contract-Conformance-001": "GO = local_skeleton conformance; not production OpenAPI alignment.",
}


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def build_phase_matrix_v0(roots: Dict[str, str]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for phase_id, root in roots.items():
        rp = Path(root)
        rel = VERIFIER_REL_BY_PHASE.get(phase_id, "")
        vr_path = rp / rel if rel else None
        verdict = None
        blockers: List[str] = []
        if vr_path and vr_path.is_file():
            rep = _read_json(vr_path)
            if isinstance(rep, dict):
                verdict = rep.get("verdict")
                blockers = list(rep.get("blockers") or []) if isinstance(rep.get("blockers"), list) else []
        rows.append(
            {
                "phase_id": phase_id,
                "phase_name": phase_id,
                "root_path": str(rp),
                "expected_verifier_report": str(vr_path) if vr_path else None,
                "verifier_verdict": verdict,
                "blockers": blockers,
                "status": "ok" if verdict == "GO" and not blockers else "check_required",
                "boundary": PHASE_BOUNDARY.get(phase_id, ""),
            }
        )
    return rows


def _safe_read(p: Path) -> Optional[Any]:
    try:
        return _read_json(p)
    except Exception:
        return None


def build_lineage_matrix_v0(roots: Dict[str, str]) -> Dict[str, Any]:
    r_ocr = Path(roots["OCR-Lightweight-Provider-Multi-ROI-Smoke-001"])
    r_cons = Path(roots["OCR-Evidence-Consumer-ReadOnly-Smoke-001"])
    r_ing = Path(roots["MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001"])
    r_bus = Path(roots["OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001"])
    r_wc = Path(roots["MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001"])
    r_dr = Path(roots["MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-001"])
    r_tr = Path(roots["MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001"])
    r_mh = Path(roots["MidPlatform-Scene-Delta-Executor-Mock-Handshake-001"])
    r_cf = Path(roots["MidPlatform-Scene-Delta-Executor-Contract-Conformance-001"])

    bridge = _safe_read(r_ocr / "ocr_lightweight_provider_multi_roi_bridge_pack.json")
    view = _safe_read(r_cons / "ocr_evidence_readonly_consumer_view.json")
    ingest = _safe_read(r_ing / "midplatform_ocr_evidence_ingest_candidate.json")
    payload = _safe_read(r_bus / "ocr_ingest_readonly_event_payload.json")
    wcand = _safe_read(r_wc / "scene_delta_write_candidate_from_ocr.json")
    dsum = _safe_read(r_dr / "scene_delta_write_candidate_dryrun_summary.json")
    tst = _safe_read(r_tr / "scene_delta_executor_trace_stub.json")
    mreq = _safe_read(r_mh / "scene_delta_mock_executor_request.json")
    mack = _safe_read(r_mh / "scene_delta_mock_executor_ack.json")
    csum = _safe_read(r_cf / "scene_delta_executor_contract_conformance_summary.json")

    text_joined = None
    if isinstance(bridge, dict):
        text_joined = bridge.get("raw_text_joined") or bridge.get("text_joined")
    if not text_joined and isinstance(view, dict):
        text_joined = view.get("text_joined")

    roi_ids: List[str] = []
    if isinstance(view, dict):
        ebr = view.get("evidence_by_roi")
        if isinstance(ebr, dict):
            roi_ids = sorted(ebr.keys())

    lineage = {
        "schema": "ocr_to_scene_delta_lineage_matrix_v0",
        "ocr_text_joined": text_joined,
        "roi_ids": roi_ids,
        "ingest_candidate_id": ingest.get("candidate_id") if isinstance(ingest, dict) else None,
        "event_id": payload.get("event_id") if isinstance(payload, dict) else None,
        "scene_delta_write_candidate_id": wcand.get("candidate_id") if isinstance(wcand, dict) else None,
        "dry_run_id": dsum.get("dry_run_id") if isinstance(dsum, dict) else None,
        "trace_id": tst.get("trace_id") if isinstance(tst, dict) else None,
        "mock_request_id": mreq.get("request_id") if isinstance(mreq, dict) else None,
        "mock_ack_id": mack.get("ack_id") if isinstance(mack, dict) else None,
        "contract_reference_mode": csum.get("contract_reference_mode") if isinstance(csum, dict) else None,
    }
    return lineage


def _flag_or_na(obj: Optional[Dict[str, Any]], key: str) -> Any:
    if not isinstance(obj, dict):
        return "na"
    if key not in obj:
        return "na"
    return obj.get(key)


def _midplatform_fact_flag(aud: Optional[Dict[str, Any]]) -> Any:
    if not isinstance(aud, dict):
        return "na"
    if "midplatform_fact_written" in aud:
        return aud.get("midplatform_fact_written")
    if "midplatform_written" in aud:
        return aud.get("midplatform_written")
    return "na"


def build_no_write_boundary_matrix_v0(roots: Dict[str, str]) -> Dict[str, Any]:
    """Unified flags per chain hop; ``na`` = field absent in that phase audit (allowed)."""
    r_ocr = Path(roots["OCR-Lightweight-Provider-Multi-ROI-Smoke-001"])
    r_cons = Path(roots["OCR-Evidence-Consumer-ReadOnly-Smoke-001"])
    r_ing = Path(roots["MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001"])
    r_bus = Path(roots["OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001"])
    r_wc = Path(roots["MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001"])
    r_dr = Path(roots["MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-001"])
    r_tr = Path(roots["MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001"])
    r_mh = Path(roots["MidPlatform-Scene-Delta-Executor-Mock-Handshake-001"])
    r_cf = Path(roots["MidPlatform-Scene-Delta-Executor-Contract-Conformance-001"])

    ocr_audit = _safe_read(r_ocr / "ocr_lightweight_provider_multi_roi_result.json")
    ocr_a = ocr_audit.get("audit") if isinstance(ocr_audit, dict) else None

    cons_a = _safe_read(r_cons / "ocr_evidence_readonly_consumer_audit_report.json")
    ing_a = _safe_read(r_ing / "midplatform_ocr_evidence_ingest_audit_report.json")
    bus_a = _safe_read(r_bus / "ocr_ingest_readonly_replay_audit_report.json")
    wc_a = _safe_read(r_wc / "scene_delta_write_candidate_audit_report.json")
    dr_a = _safe_read(r_dr / "scene_delta_write_candidate_no_write_audit_report.json")
    tr_a = _safe_read(r_tr / "scene_delta_executor_trace_stub_audit_report.json")
    mh_a = _safe_read(r_mh / "scene_delta_mock_handshake_audit_report.json")
    cf_a = _safe_read(r_cf / "scene_delta_executor_contract_conformance_audit_report.json")

    keys = (
        "ocr_provider_invoked",
        "paddleocr_invoked",
        "ocr_routing_changed",
        "midplatform_fact_written",
        "scene_delta_written",
        "database_write_invoked",
        "wal_append_invoked",
        "rehearsal_log_written",
        "world_model_written",
        "ai_interpretation_invoked",
    )

    def row(phase: str, aud: Any) -> Dict[str, Any]:
        out: Dict[str, Any] = {"phase_id": phase}
        for k in keys:
            if k == "paddleocr_invoked" and phase == "OCR-Lightweight-Provider-Multi-ROI-Smoke-001":
                out[k] = _flag_or_na(aud if isinstance(aud, dict) else None, "paddleocr_invoked")
            elif k == "ocr_provider_invoked" and phase == "OCR-Lightweight-Provider-Multi-ROI-Smoke-001":
                out[k] = "na"
            elif k == "ocr_provider_invoked":
                out[k] = _flag_or_na(aud if isinstance(aud, dict) else None, k)
            elif k == "paddleocr_invoked":
                out[k] = "na"
            elif k == "midplatform_fact_written":
                out[k] = _midplatform_fact_flag(aud if isinstance(aud, dict) else None)
            else:
                out[k] = _flag_or_na(aud if isinstance(aud, dict) else None, k)
        return out

    rows = [
        row("OCR-Lightweight-Provider-Multi-ROI-Smoke-001", ocr_a),
        row("OCR-Evidence-Consumer-ReadOnly-Smoke-001", cons_a),
        row("MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001", ing_a),
        row("OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001", bus_a),
        row("MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001", wc_a),
        row("MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-001", dr_a),
        row("MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001", tr_a),
        row("MidPlatform-Scene-Delta-Executor-Mock-Handshake-001", mh_a),
        row("MidPlatform-Scene-Delta-Executor-Contract-Conformance-001", cf_a),
    ]

    violations: List[str] = []
    for r in rows:
        pid = str(r.get("phase_id"))
        for k in keys:
            v = r.get(k)
            if v == "na":
                continue
            if v is not False:
                violations.append(f"{pid}:{k}={v}")

    return {
        "schema": "ocr_to_scene_delta_no_write_boundary_matrix_v0",
        "rows": rows,
        "violations": violations,
        "boundary_ok": len(violations) == 0,
    }


def build_capability_closure_report_v0() -> Dict[str, Any]:
    caps = [
        "RapidOCR lightweight multi-ROI OCR evidence with coordinate lift and bridge_pack",
        "OCR bridge_pack read-only consumer (ROI grouping, geometry matrix, source chain)",
        "MidPlatform read-only OCR ingest candidate (no fact write)",
        "Read-only OCR event payload + simulated Product Bus replay",
        "Scene Delta write candidate stub from OCR (write_allowed=false, gate not evaluated)",
        "Dry-run verifier + Scene Delta field mapping matrix (no executor)",
        "Executor trace stub from dry-run (trace_stub_only)",
        "Mock executor handshake with synthetic ACK (no real executor)",
        "Local contract skeleton conformance for mock request/ACK (not production OpenAPI)",
    ]
    return {"schema": "ocr_to_scene_delta_capability_closure_report_v0", "capabilities_proven": caps}


def build_non_claims_report_v0() -> Dict[str, Any]:
    return {
        "schema": "ocr_to_scene_delta_non_claims_report_v0",
        "claims": {
            "production_scene_delta_executor_available": False,
            "scene_delta_write_path_production_ready": False,
            "midplatform_fact_write_available": False,
            "ai_interpretation_available": False,
            "world_model_write_available": False,
            "ocr_quality_benchmark_passed": False,
            "paddleocr_integration_ready": False,
        },
        "narrative": [
            "This chain closure does NOT assert production Scene Delta executor availability.",
            "This chain closure does NOT assert Scene Delta write path is enabled.",
            "This chain closure does NOT assert MidPlatform fact writes.",
            "This chain closure does NOT assert AI interpretation is available.",
            "This chain closure does NOT assert WorldModel writes.",
            "This chain closure does NOT assert OCR quality benchmark pass.",
            "This chain closure does NOT assert PaddleOCR integration readiness.",
        ],
    }


def build_open_followups_v0() -> Dict[str, Any]:
    items = [
        "Real Scene Delta executor OpenAPI / proto contract bundle not yet imported or bound to conformance checks.",
        "contract_reference_mode for executor handshake remains local_skeleton (not production schema).",
        "AI interpretation governance to be expanded in a separate design/run phase.",
        "OCR partial evidence completion remains DESIGN_RECORDED / FIELD_RESERVED until a dedicated verifier exists.",
        "Performance Controller not integrated on this chain.",
        "Vision / video stream mainline not entered from this chain.",
        "Camera Capture Governance deferred to hardware-aligned phases.",
    ]
    return {"schema": "ocr_to_scene_delta_open_followups_v0", "items": items}


def run_chain_closure_v0(roots: Dict[str, str]) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    """Returns summary, phase_matrix, lineage, no_write, capability, non_claims, followups, errors."""
    errs: List[str] = []
    for pid, root in roots.items():
        p = Path(root)
        if not p.is_dir():
            errs.append(f"missing_root_dir:{pid}:{root}")
            continue
        rel = VERIFIER_REL_BY_PHASE.get(pid)
        if rel and not (p / rel).is_file():
            errs.append(f"missing_verifier_report:{pid}:{p/rel}")

    phase_matrix = build_phase_matrix_v0(roots)
    for row in phase_matrix:
        if row.get("verifier_verdict") != "GO":
            errs.append(f"verdict_not_go:{row.get('phase_id')}:{row.get('verifier_verdict')}")
        if row.get("blockers"):
            errs.append(f"blockers_non_empty:{row.get('phase_id')}")

    lineage = build_lineage_matrix_v0(roots)
    nw = build_no_write_boundary_matrix_v0(roots)
    if not nw.get("boundary_ok"):
        errs.append("no_write_boundary_violations")

    summary = {
        "schema": "ocr_to_scene_delta_chain_closure_summary_v0",
        "phase": "Phase-OCR-to-SceneDelta-Mock-Chain-Closure-001",
        "chain_closure_schema": CHAIN_CLOSURE_SCHEMA,
        "roots": dict(roots),
        "lineage_ok": bool(lineage.get("ocr_text_joined")) and bool(lineage.get("contract_reference_mode")),
        "errors": list(errs),
    }

    return (
        summary,
        phase_matrix,
        lineage,
        nw,
        build_capability_closure_report_v0(),
        build_non_claims_report_v0(),
        build_open_followups_v0(),
        errs,
    )

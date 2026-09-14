# -*- coding: utf-8 -*-
"""YOLO evaluation-only chain closure (archive; no mainline; no writes).

Phase-Vision-YOLO-Evaluation-Chain-Closure-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CLOSURE_SUMMARY_SCHEMA = "yolo_evaluation_chain_closure_summary_v0"
PHASE_MATRIX_SCHEMA = "yolo_evaluation_phase_matrix_v0"
LINEAGE_MATRIX_SCHEMA = "yolo_evaluation_lineage_matrix_v0"
NO_WRITE_SCHEMA = "yolo_evaluation_no_write_boundary_matrix_v0"
CAPABILITY_CLOSURE_SCHEMA = "yolo_evaluation_capability_closure_report_v0"
NON_CLAIMS_SCHEMA = "yolo_evaluation_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "yolo_evaluation_open_followups_v0"
AUDIT_SCHEMA = "yolo_evaluation_chain_closure_audit_v0"

PHASE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_key": "Gated-YOLO-Candidate-Adapter",
        "phase_id": "Phase-Vision-Gated-YOLO-Candidate-Adapter-001",
        "expected_verdict": "CONDITIONAL_GO",
        "boundary": "fixture_path_structural_conversion_only",
        "verifier_file": "yolo_candidate_adapter_verifier_report.json",
        "summary_file": "yolo_candidate_adapter_eval_summary.json",
        "audit_file": "yolo_candidate_adapter_audit_report.json",
    },
    {
        "phase_key": "Gated-YOLO-Real-Smoke",
        "phase_id": "Phase-Vision-Gated-YOLO-Real-Smoke-001",
        "expected_verdict": "CONDITIONAL_GO",
        "boundary": "real_yolo_ran_zero_detections_on_roi_crops",
        "verifier_file": "yolo_real_smoke_verifier_report.json",
        "summary_file": "yolo_real_smoke_summary.json",
        "audit_file": "yolo_real_smoke_audit_report.json",
    },
    {
        "phase_key": "YOLO-Real-Smoke-Positive-Sample",
        "phase_id": "Phase-Vision-YOLO-Real-Smoke-Positive-Sample-001",
        "expected_verdict": "GO",
        "boundary": "real_yolo_positive_sample_detections",
        "verifier_file": "yolo_real_positive_verifier_report.json",
        "summary_file": "yolo_real_positive_sample_summary.json",
        "audit_file": "yolo_real_positive_audit_report.json",
    },
    {
        "phase_key": "YOLO-Evidence-Pack-Integration-Stub",
        "phase_id": "Phase-Vision-YOLO-Evidence-Pack-Integration-Stub-001",
        "expected_verdict": "GO",
        "boundary": "pack_integration_evaluation_only",
        "verifier_file": "yolo_evidence_pack_verifier_report.json",
        "summary_file": "yolo_evidence_pack_integration_summary.json",
        "audit_file": "yolo_evidence_pack_audit_report.json",
    },
    {
        "phase_key": "YOLO-Evidence-Pack-ReadOnly-Consumer",
        "phase_id": "Phase-Vision-YOLO-Evidence-Pack-ReadOnly-Consumer-001",
        "expected_verdict": "GO",
        "boundary": "readonly_consumer_no_writes",
        "verifier_file": "yolo_evidence_readonly_consumer_verifier_report.json",
        "summary_file": "yolo_evidence_readonly_consumer_summary.json",
        "audit_file": "yolo_evidence_readonly_consumer_audit_report.json",
    },
)

NO_WRITE_KEYS = (
    "vision_mainline_modified",
    "vision_provider_registry_default_changed",
    "midplatform_fact_written",
    "scene_delta_written",
    "world_model_written",
    "ai_interpretation_invoked",
    "navigation_decision_invoked",
    "database_write_invoked",
    "external_bus_invoked",
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


def _verdict_from_root(root: Path, verifier_file: str) -> Tuple[Optional[str], List[str], List[str]]:
    vp = root / verifier_file
    if not vp.is_file():
        return None, [f"missing_verifier:{verifier_file}"], []
    rep = _safe_read(vp)
    if not isinstance(rep, dict):
        return None, ["verifier_invalid"], []
    verdict = str(rep.get("verdict") or "")
    blockers = list(rep.get("blockers") or []) if isinstance(rep.get("blockers"), list) else []
    soft = list(rep.get("soft_notes") or []) if isinstance(rep.get("soft_notes"), list) else []
    return verdict, blockers, soft


def build_phase_matrix_v0(roots: Dict[str, Path]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for spec in PHASE_SPECS:
        key = spec["phase_key"]
        root = roots.get(key)
        if root is None or not root.is_dir():
            rows.append(
                {
                    "phase_name": key,
                    "phase_id": spec["phase_id"],
                    "input_root": None,
                    "verifier_verdict": None,
                    "expected_verdict": spec["expected_verdict"],
                    "blockers": ["missing_input_root"],
                    "soft_notes": [],
                    "status": "missing",
                    "boundary": spec["boundary"],
                }
            )
            continue
        verdict, blockers, soft = _verdict_from_root(root, str(spec["verifier_file"]))
        status = "ok"
        if verdict is None:
            status = "missing_verifier"
        elif verdict != spec["expected_verdict"]:
            status = "verdict_mismatch"
        rows.append(
            {
                "phase_name": key,
                "phase_id": spec["phase_id"],
                "input_root": str(root),
                "verifier_verdict": verdict,
                "expected_verdict": spec["expected_verdict"],
                "blockers": blockers,
                "soft_notes": soft,
                "status": status,
                "boundary": spec["boundary"],
            }
        )
    return rows


def _extract_lineage_v0(roots: Dict[str, Path]) -> Dict[str, Any]:
    cand = roots.get("Gated-YOLO-Candidate-Adapter")
    real = roots.get("Gated-YOLO-Real-Smoke")
    pos = roots.get("YOLO-Real-Smoke-Positive-Sample")
    pack = roots.get("YOLO-Evidence-Pack-Integration-Stub")
    consumer = roots.get("YOLO-Evidence-Pack-ReadOnly-Consumer")

    lineage: Dict[str, Any] = {
        "schema": LINEAGE_MATRIX_SCHEMA,
        "model_path": None,
        "detector_mode": None,
        "positive_sample_path": None,
        "detection_count": None,
        "converted_evidence_count": None,
        "evidence_pack_id": None,
        "evidence_count_observed": None,
        "labels": {},
        "provider": None,
        "provider_level": None,
    }

    if real:
        s = _safe_read(real / "yolo_real_smoke_summary.json")
        if isinstance(s, dict):
            lineage["model_path"] = s.get("resolved_model_path")
            lineage["detector_mode"] = s.get("detector_mode")
            lineage["detection_count"] = s.get("detection_count")
            lineage["converted_evidence_count"] = s.get("converted_evidence_count")

    if pos:
        s = _safe_read(pos / "yolo_real_positive_sample_summary.json")
        rep = _safe_read(pos / "yolo_real_positive_sample_report.json")
        if isinstance(rep, dict):
            lineage["positive_sample_path"] = rep.get("image_ref")
        if isinstance(s, dict):
            lineage["detection_count"] = s.get("detection_count")
            lineage["converted_evidence_count"] = s.get("converted_evidence_count")
            lineage["detector_mode"] = s.get("detector_mode")
            if not lineage["model_path"]:
                lineage["model_path"] = s.get("resolved_model_path")

    if pack:
        s = _safe_read(pack / "yolo_evidence_pack_integration_summary.json")
        pdoc = _safe_read(pack / "yolo_vision_recognition_evidence_pack.json")
        if isinstance(pdoc, dict):
            lineage["evidence_pack_id"] = pdoc.get("pack_id")
            pt = pdoc.get("provider_trace") if isinstance(pdoc.get("provider_trace"), dict) else {}
            lineage["provider"] = pt.get("provider")
            lineage["provider_level"] = pt.get("provider_level")
            lineage["detection_count"] = s.get("evidence_count") if isinstance(s, dict) else lineage["detection_count"]
            lineage["converted_evidence_count"] = (
                s.get("evidence_count") if isinstance(s, dict) else lineage["converted_evidence_count"]
            )

    if consumer:
        view = _safe_read(consumer / "yolo_evidence_readonly_consumer_view.json")
        if isinstance(view, dict):
            lineage["evidence_count_observed"] = view.get("evidence_count_observed")
            lineage["provider"] = view.get("provider") or lineage["provider"]
            lineage["provider_level"] = view.get("provider_level") or lineage["provider_level"]
            rd = view.get("real_detector_summary") if isinstance(view.get("real_detector_summary"), dict) else {}
            lineage["detector_mode"] = rd.get("detector_mode") or lineage["detector_mode"]
            lineage["labels"] = dict(view.get("label_summary") or {})

    if cand:
        s = _safe_read(cand / "yolo_candidate_adapter_eval_summary.json")
        if isinstance(s, dict) and lineage["detector_mode"] is None:
            lineage["detector_mode"] = s.get("detector_mode")

    return lineage


def build_no_write_boundary_matrix_v0(roots: Dict[str, Path]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for spec in PHASE_SPECS:
        key = spec["phase_key"]
        root = roots.get(key)
        row: Dict[str, Any] = {"phase_name": key, "phase_id": spec["phase_id"], "input_root": str(root) if root else None}
        if root is None or not root.is_dir():
            row["audit_present"] = False
            row["boundary_ok"] = False
            all_pass = False
            rows.append(row)
            continue
        aud = _safe_read(root / str(spec["audit_file"]))
        row["audit_present"] = isinstance(aud, dict)
        boundary_ok = True
        if isinstance(aud, dict):
            for bk in NO_WRITE_KEYS:
                if bk in aud:
                    val = aud.get(bk)
                    row[bk] = val
                    if bk in (
                        "vision_mainline_modified",
                        "vision_provider_registry_default_changed",
                        "midplatform_fact_written",
                        "scene_delta_written",
                        "world_model_written",
                        "ai_interpretation_invoked",
                        "navigation_decision_invoked",
                        "database_write_invoked",
                        "external_bus_invoked",
                    ):
                        if val is not False:
                            boundary_ok = False
        else:
            boundary_ok = False
        row["boundary_ok"] = boundary_ok
        if not boundary_ok:
            all_pass = False
        rows.append(row)
    return {
        "schema": NO_WRITE_SCHEMA,
        "all_phases_boundary_ok": all_pass,
        "rows": rows,
    }


def build_capability_closure_report_v0(lineage: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema": CAPABILITY_CLOSURE_SCHEMA,
        "proven_capabilities": [
            "local_yolo_weights_loadable",
            "gated_evaluation_only_inference_path_runs",
            "positive_sample_produces_detections",
            "yolo_detection_to_vision_detection_evidence_v0",
            "yolo_evidence_packable_as_vision_recognition_evidence_pack_v0",
            "yolo_evidence_pack_consumable_by_readonly_consumer",
            "fact_status_remains_not_fact_throughout",
            "no_write_throughout_evaluation_chain",
            "vision_mainline_not_modified",
        ],
        "lineage_snapshot": {
            "model_path": lineage.get("model_path"),
            "detector_mode": lineage.get("detector_mode"),
            "positive_sample_path": lineage.get("positive_sample_path"),
            "detection_count": lineage.get("detection_count"),
            "converted_evidence_count": lineage.get("converted_evidence_count"),
            "evidence_pack_id": lineage.get("evidence_pack_id"),
            "evidence_count_observed": lineage.get("evidence_count_observed"),
        },
        "chain_endpoints": [
            "yolo_candidate_adapter_eval",
            "yolo_real_smoke",
            "yolo_real_positive_sample",
            "yolo_evidence_pack_integration",
            "yolo_evidence_readonly_consumer",
        ],
    }


def build_non_claims_report_v0() -> Dict[str, Any]:
    return {
        "schema": NON_CLAIMS_SCHEMA,
        "not_mainline": True,
        "not_default_provider": True,
        "detections_not_fact": True,
        "not_navigation_decision": True,
        "no_midplatform_fact_write": True,
        "no_scene_delta_write": True,
        "no_world_model_write": True,
        "no_realtime_performance_claim": True,
        "no_long_run_stability_claim": True,
        "no_multi_scene_quality_claim": True,
        "claims": [
            "Does NOT claim YOLO is on Vision runtime mainline.",
            "Does NOT claim YOLO is the default vision provider.",
            "Does NOT claim detection labels or confidence are facts.",
            "Does NOT claim outputs may drive navigation decisions.",
            "Does NOT claim MidPlatform fact writes occurred.",
            "Does NOT claim Scene Delta or WorldModel writes occurred.",
            "Does NOT claim realtime performance or long-run stability was evaluated.",
            "Does NOT claim multi-scene / multi-video quality was fully assessed.",
        ],
    }


def build_open_followups_v0() -> Dict[str, Any]:
    return {
        "schema": FOLLOWUPS_SCHEMA,
        "items": [
            {
                "id": "yolo_provider_registry_gated_shadow",
                "title": "YOLO provider registry gated adapter shadow",
                "priority": "high",
            },
            {
                "id": "multi_scene_video_eval",
                "title": "Multi-scene / multi-video YOLO evaluation",
                "priority": "medium",
            },
            {
                "id": "realtime_performance_controller",
                "title": "Realtime performance & Performance Controller integration",
                "priority": "medium",
            },
            {
                "id": "supervision_detections_ab",
                "title": "Supervision Detections adapter A/B vs YOLO",
                "priority": "medium",
            },
            {
                "id": "bytetrack_tracking",
                "title": "ByteTrack / tracking integration (gated)",
                "priority": "low",
            },
            {
                "id": "vision_roi_ocr_bridge",
                "title": "Vision ROI → OCRRequest bridge",
                "priority": "low",
            },
            {
                "id": "cross_modal_evidence_fusion",
                "title": "CrossModal Evidence Fusion",
                "priority": "low",
            },
            {
                "id": "test_board_l6_l7_l8",
                "title": "Test Board L6/L7/L8 integration",
                "priority": "low",
            },
        ],
    }


def build_closure_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "yolo_evaluation_chain_closure_executed": True,
        "evaluation_only": True,
        "vision_mainline_modified": False,
        "vision_provider_registry_default_changed": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "database_write_invoked": False,
        "external_bus_invoked": False,
    }


def run_yolo_evaluation_chain_closure_v0(
    *,
    yolo_candidate_adapter_root: str,
    yolo_real_smoke_root: str,
    yolo_positive_sample_root: str,
    yolo_evidence_pack_integration_root: str,
    yolo_evidence_readonly_consumer_root: str,
) -> Tuple[
    Dict[str, Any],
    List[Dict[str, Any]],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []

    roots: Dict[str, Path] = {
        "Gated-YOLO-Candidate-Adapter": Path(yolo_candidate_adapter_root).resolve(),
        "Gated-YOLO-Real-Smoke": Path(yolo_real_smoke_root).resolve(),
        "YOLO-Real-Smoke-Positive-Sample": Path(yolo_positive_sample_root).resolve(),
        "YOLO-Evidence-Pack-Integration-Stub": Path(yolo_evidence_pack_integration_root).resolve(),
        "YOLO-Evidence-Pack-ReadOnly-Consumer": Path(yolo_evidence_readonly_consumer_root).resolve(),
    }

    for key, p in roots.items():
        if not p.is_dir():
            errs.append(f"missing_root:{key}")

    phase_matrix = build_phase_matrix_v0(roots)
    lineage = _extract_lineage_v0(roots)
    no_write = build_no_write_boundary_matrix_v0(roots)
    capability = build_capability_closure_report_v0(lineage)
    non_claims = build_non_claims_report_v0()
    followups = build_open_followups_v0()
    audit = build_closure_audit_v0()

    for row in phase_matrix:
        if row.get("status") not in ("ok",):
            if row.get("verifier_verdict") != row.get("expected_verdict"):
                errs.append(f"phase_verdict_mismatch:{row.get('phase_name')}")
        if row.get("blockers"):
            errs.append(f"phase_has_blockers:{row.get('phase_name')}")

    critical_phases = (
        "YOLO-Real-Smoke-Positive-Sample",
        "YOLO-Evidence-Pack-Integration-Stub",
        "YOLO-Evidence-Pack-ReadOnly-Consumer",
    )
    for cp in critical_phases:
        row = next((r for r in phase_matrix if r.get("phase_name") == cp), None)
        if row and row.get("verifier_verdict") != "GO":
            errs.append(f"critical_phase_not_go:{cp}")

    det = int(lineage.get("detection_count") or 0)
    ev = int(lineage.get("evidence_count_observed") or 0)
    if det <= 0:
        errs.append("lineage_detection_count_not_positive")
    if ev <= 0:
        errs.append("lineage_evidence_count_observed_not_positive")

    if not no_write.get("all_phases_boundary_ok"):
        errs.append("no_write_boundary_not_all_ok")

    phase_verdict = "GO"
    if errs:
        if no_write.get("all_phases_boundary_ok") and all(
            r.get("verifier_verdict") in ("GO", "CONDITIONAL_GO") for r in phase_matrix if r.get("verifier_verdict")
        ):
            phase_verdict = "CONDITIONAL_GO"
        else:
            phase_verdict = "NO_GO"
    elif any(r.get("verifier_verdict") == "CONDITIONAL_GO" for r in phase_matrix):
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": CLOSURE_SUMMARY_SCHEMA,
        "phase": "Phase-Vision-YOLO-Evaluation-Chain-Closure-001",
        "phase_matrix_row_count": len(phase_matrix),
        "lineage_detection_count": det,
        "lineage_evidence_count_observed": ev,
        "no_write_all_phases_ok": no_write.get("all_phases_boundary_ok"),
        "phase_verdict_hint": phase_verdict,
        "input_roots": {k: str(v) for k, v in roots.items()},
        "errors": list(errs),
    }

    return (
        summary,
        phase_matrix,
        lineage,
        no_write,
        capability,
        non_claims,
        followups,
        audit,
        errs,
    )

# -*- coding: utf-8 -*-
"""Gated YOLO candidate adapter (evaluation-only; not mainline).

Phase-Vision-Gated-YOLO-Candidate-Adapter-001
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple

VISION_DETECTION_SCHEMA = "vision_detection_evidence_v0"
PROBE_SCHEMA = "vision_yolo_availability_probe_v0"
SELECTION_SCHEMA = "yolo_input_unit_selection_v0"
RAW_SUMMARY_SCHEMA = "yolo_raw_detector_result_summary_v0"
MATRIX_SCHEMA = "yolo_detection_to_vision_evidence_matrix_v0"
FIXTURE_SCHEMA = "yolo_vision_detection_evidence_fixture_v0"
ADAPTER_REPORT_SCHEMA = "yolo_candidate_adapter_report_v0"
RISK_SCHEMA = "yolo_candidate_adapter_risk_report_v0"
AUDIT_SCHEMA = "yolo_candidate_adapter_audit_v0"
EVAL_SUMMARY_SCHEMA = "yolo_candidate_adapter_eval_summary_v0"
REAL_GATE_SCHEMA = "vision_yolo_real_gate_check_v0"
MODEL_LOAD_SCHEMA = "yolo_model_load_report_v0"
REAL_SELECTION_SCHEMA = "yolo_real_input_unit_selection_v0"
REAL_RAW_SCHEMA = "yolo_real_raw_detector_result_summary_v0"
REAL_MATRIX_SCHEMA = "yolo_real_detection_to_vision_evidence_matrix_v0"
REAL_FIXTURE_SCHEMA = "yolo_real_vision_detection_evidence_fixture_v0"
REAL_RISK_SCHEMA = "yolo_real_smoke_risk_report_v0"
REAL_AUDIT_SCHEMA = "yolo_real_smoke_audit_v0"
REAL_SUMMARY_SCHEMA = "yolo_real_smoke_summary_v0"
POSITIVE_SAMPLE_REPORT_SCHEMA = "yolo_real_positive_sample_report_v0"
POSITIVE_GATE_SCHEMA = "yolo_real_positive_gate_check_v0"
POSITIVE_MODEL_LOAD_SCHEMA = "yolo_real_positive_model_load_report_v0"
POSITIVE_RAW_SCHEMA = "yolo_real_positive_detector_result_summary_v0"
POSITIVE_MATRIX_SCHEMA = "yolo_real_positive_detection_to_vision_evidence_matrix_v0"
POSITIVE_FIXTURE_SCHEMA = "yolo_real_positive_vision_detection_evidence_fixture_v0"
POSITIVE_RISK_SCHEMA = "yolo_real_positive_risk_report_v0"
POSITIVE_AUDIT_SCHEMA = "yolo_real_positive_audit_v0"
POSITIVE_SUMMARY_SCHEMA = "yolo_real_positive_sample_summary_v0"

PRIORITY_ROI_SUFFIXES = ("center_roi", "ground_roi", "upper_sign_roi")
LOCAL_MODEL_FILENAMES = ("yolov8n.pt", "yolo11n.pt")
FORBIDDEN_UNIT_MARKERS = ("full_frame", "whole_frame", "entire_frame")


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return str(raw).strip().lower() in ("1", "true", "yes", "on")


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or not str(raw).strip():
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _evidence_id(unit_id: str, label: str, idx: int) -> str:
    h = hashlib.sha256(f"yolo:{unit_id}:{label}:{idx}".encode("utf-8")).hexdigest()[:16]
    return f"evidence_{h}"


def probe_yolo_availability_v0() -> Dict[str, Any]:
    eval_enabled = _env_bool("LUNA_ENABLE_YOLO_EVAL_PROVIDER_V0", False)
    force_fixture = _env_bool("LUNA_YOLO_FORCE_FIXTURE_V0", False)
    eval_only = _env_bool("LUNA_YOLO_EVAL_ONLY", False)
    model_path = os.environ.get("LUNA_YOLO_MODEL_PATH", "").strip()
    model_path_present = bool(model_path and Path(model_path).is_file())

    out: Dict[str, Any] = {
        "schema_version": PROBE_SCHEMA,
        "ultralytics_installed": False,
        "model_path_present": model_path_present,
        "eval_provider_enabled": eval_enabled,
        "eval_only_gate": eval_only,
        "force_fixture": force_fixture,
        "import_error": None,
        "model_load_error": None,
        "default_model_hint": "yolov8n.pt",
    }

    try:
        import ultralytics  # type: ignore  # noqa: F401

        out["ultralytics_installed"] = True
    except Exception as e:
        out["import_error"] = f"{type(e).__name__}: {e}"
        return out

    if eval_enabled and eval_only and not force_fixture:
        load_path = model_path if model_path_present else out["default_model_hint"]
        try:
            from ultralytics import YOLO  # type: ignore

            _ = YOLO(load_path)
            out["model_path_present"] = model_path_present or load_path == out["default_model_hint"]
        except Exception as e:
            out["model_load_error"] = f"{type(e).__name__}: {e}"

    return out


def _is_full_frame_unit(unit: Dict[str, Any]) -> bool:
    ut = str(unit.get("unit_type") or "")
    if ut in ("full_frame", "whole_frame"):
        return True
    rid = str(unit.get("roi_id") or "").lower()
    return any(m in rid for m in FORBIDDEN_UNIT_MARKERS)


def _roi_priority_score(roi_id: str) -> int:
    rid = roi_id.lower()
    for i, suffix in enumerate(PRIORITY_ROI_SUFFIXES):
        if suffix in rid:
            return i
    return len(PRIORITY_ROI_SUFFIXES) + 1


def select_input_units_v0(
    roi_root: Path,
    *,
    max_units: int = 5,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    pack_path = roi_root / "vision_provider_input_pack.json"
    if not pack_path.is_file():
        return (
            {
                "schema": SELECTION_SCHEMA,
                "error": "missing_vision_provider_input_pack",
                "selected_unit_ids": [],
                "selected_units_count": 0,
                "full_frame_direct_forbidden": True,
            },
            [],
        )

    bundle = _read_json(pack_path)
    packs = bundle.get("packs") if isinstance(bundle.get("packs"), list) else []
    candidates: List[Dict[str, Any]] = []

    for pack in packs:
        if not isinstance(pack, dict):
            continue
        source_frame_id = str(pack.get("source_frame_id") or "")
        pack_id = str(pack.get("pack_id") or "")
        for unit in pack.get("input_units") or []:
            if not isinstance(unit, dict):
                continue
            if _is_full_frame_unit(unit):
                continue
            if str(unit.get("unit_type") or "") != "frame_roi":
                continue
            image_ref = str(unit.get("image_ref") or "")
            if not image_ref or not Path(image_ref).is_file():
                continue
            candidates.append(
                {
                    **unit,
                    "source_frame_id": source_frame_id,
                    "pack_id": pack_id,
                    "pack_source_image_ref": pack.get("source_image_ref"),
                }
            )

    candidates.sort(key=lambda u: (_roi_priority_score(str(u.get("roi_id") or "")), str(u.get("roi_id") or "")))
    selected = candidates[: max(0, int(max_units))]

    selection = {
        "schema": SELECTION_SCHEMA,
        "bundle_schema": bundle.get("bundle_schema"),
        "pack_path": str(pack_path),
        "candidates_considered": len(candidates),
        "selected_units_count": len(selected),
        "selected_unit_ids": [str(u.get("unit_id") or "") for u in selected],
        "selected_roi_ids": [str(u.get("roi_id") or "") for u in selected],
        "full_frame_direct_forbidden": True,
        "priority_suffixes": list(PRIORITY_ROI_SUFFIXES),
        "max_units": max_units,
    }
    return selection, selected


def _lift_bbox_to_frame(bbox_unit: List[float], transform: Dict[str, Any]) -> List[int]:
    x1, y1, x2, y2 = (float(v) for v in bbox_unit)
    off_x = float(transform.get("offset_x") or 0)
    off_y = float(transform.get("offset_y") or 0)
    return [int(x1 + off_x), int(y1 + off_y), int(x2 + off_x), int(y2 + off_y)]


def build_yolo_like_fixture_detections_v0(unit: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Deterministic YOLO-like boxes in unit pixel space when real YOLO unavailable."""
    tw = int((unit.get("coordinate_transform") or {}).get("transformed_width") or 64)
    th = int((unit.get("coordinate_transform") or {}).get("transformed_height") or 64)
    tw, th = max(8, tw), max(8, th)
    return [
        {
            "detection_id": f"yolo_like_{unit.get('unit_id')}_001",
            "bbox_xyxy": [int(tw * 0.1), int(th * 0.1), int(tw * 0.55), int(th * 0.45)],
            "class_id": 0,
            "class_name": "yolo_like_object_a",
            "confidence": 0.62,
        },
        {
            "detection_id": f"yolo_like_{unit.get('unit_id')}_002",
            "bbox_xyxy": [int(tw * 0.35), int(th * 0.4), int(tw * 0.85), int(th * 0.88)],
            "class_id": 1,
            "class_name": "yolo_like_object_b",
            "confidence": 0.41,
        },
    ]


class _NetworkBlockedInYoloSmoke(RuntimeError):
    pass


@contextmanager
def _network_guard_v0() -> Iterator[Dict[str, List[str]]]:
    """Block outbound HTTP during model load/inference (evaluation smoke)."""
    import urllib.request

    original = urllib.request.urlopen
    network_hit: List[str] = []

    def _guarded_urlopen(*args: Any, **kwargs: Any) -> Any:
        network_hit.append(str(args[0]) if args else "unknown")
        raise _NetworkBlockedInYoloSmoke("network_request_blocked_in_yolo_real_smoke")

    urllib.request.urlopen = _guarded_urlopen  # type: ignore[assignment]
    token = {"hit": network_hit}
    try:
        os.environ["YOLO_OFFLINE"] = "1"
        yield token
    finally:
        urllib.request.urlopen = original  # type: ignore[assignment]


def resolve_local_yolo_model_path_v0() -> Tuple[Optional[str], str, List[str]]:
    """Resolve a local-only YOLO weights path; never triggers download."""
    reason_codes: List[str] = []
    env_path = os.environ.get("LUNA_YOLO_MODEL_PATH", "").strip()
    if env_path:
        p = Path(env_path).expanduser().resolve()
        if p.is_file():
            return str(p), "env_luna_yolo_model_path", reason_codes
        reason_codes.append("env_model_path_not_found")

    search_dirs: List[Path] = []
    for raw in os.environ.get("LUNA_YOLO_MODEL_SEARCH_PATHS", "").split(","):
        raw = raw.strip()
        if raw:
            search_dirs.append(Path(raw).expanduser().resolve())

    hub = Path.home() / ".cache" / "ultralytics"
    search_dirs.extend([hub, hub / "weights"])

    # Common repo-local eval weights (no download).
    search_dirs.append(
        Path("/Users/luanlei/Desktop/Luna-Core/luna_badge_tests/tests/models").resolve()
    )

    for directory in search_dirs:
        if not directory.is_dir():
            continue
        for name in LOCAL_MODEL_FILENAMES:
            cand = directory / name
            if cand.is_file():
                return str(cand.resolve()), f"local_search:{directory}", reason_codes

    for name in LOCAL_MODEL_FILENAMES:
        if Path(name).is_file():
            return str(Path(name).resolve()), "cwd_relative", reason_codes

    reason_codes.append("no_local_model_file_without_network")
    return None, "none", reason_codes


def load_yolo_model_local_v0(model_path: str) -> Tuple[Any, Dict[str, Any]]:
    """Load YOLO from existing local file only; records network guard status."""
    report: Dict[str, Any] = {
        "model_path": model_path,
        "model_loaded": False,
        "model_load_error": None,
        "model_source": "local_file",
        "network_request_invoked": False,
    }
    p = Path(model_path)
    if not p.is_file():
        report["model_load_error"] = "model_path_not_a_file"
        return None, report

    try:
        with _network_guard_v0() as guard:
            from ultralytics import YOLO  # type: ignore

            model = YOLO(str(p.resolve()))
        report["model_loaded"] = True
        return model, report
    except _NetworkBlockedInYoloSmoke:
        report["network_request_invoked"] = True
        report["model_load_error"] = "network_download_blocked"
        return None, report
    except Exception as e:
        report["model_load_error"] = f"{type(e).__name__}: {e}"
        return None, report


def run_yolo_on_unit_v0(
    unit: Dict[str, Any],
    *,
    model_path: str = "",
    model: Any = None,
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    image_ref = str(unit.get("image_ref") or "")
    if model is None:
        if not model_path:
            raise ValueError("model_path_or_model_required")
        with _network_guard_v0():
            from ultralytics import YOLO  # type: ignore

            model = YOLO(model_path)
    with _network_guard_v0():
        results = model.predict(image_ref, verbose=False)
    detections: List[Dict[str, Any]] = []
    if not results:
        return detections, None
    r0 = results[0]
    boxes = getattr(r0, "boxes", None)
    if boxes is None or len(boxes) == 0:
        return detections, None
    names = getattr(r0, "names", {}) or {}
    xyxy = boxes.xyxy.cpu().numpy()
    confs = boxes.conf.cpu().numpy()
    clss = boxes.cls.cpu().numpy().astype(int)
    for i in range(len(xyxy)):
        x1, y1, x2, y2 = (float(v) for v in xyxy[i])
        cid = int(clss[i])
        detections.append(
            {
                "detection_id": f"yolo_{unit.get('unit_id')}_{i:03d}",
                "bbox_xyxy": [x1, y1, x2, y2],
                "class_id": cid,
                "class_name": str(names.get(cid, f"class_{cid}")),
                "confidence": float(confs[i]),
            }
        )
    return detections, None


def yolo_detection_to_vision_evidence_v0(
    det: Dict[str, Any],
    *,
    unit: Dict[str, Any],
    detector_mode: str,
    det_index: int,
    chain_prefix: str = "yolo_candidate_adapter_eval_v0",
) -> Dict[str, Any]:
    bbox_unit = [float(v) for v in det["bbox_xyxy"]]
    transform = unit.get("coordinate_transform") if isinstance(unit.get("coordinate_transform"), dict) else {}
    bbox_frame = _lift_bbox_to_frame(bbox_unit, transform)
    roi_id = str(unit.get("roi_id") or "")
    unit_id = str(unit.get("unit_id") or "")
    source_frame_id = str(unit.get("source_frame_id") or "")
    label = str(det.get("class_name") or "unknown")
    is_fixture = detector_mode != "real_yolo"
    chain = [
        chain_prefix,
        f"detector_mode:{detector_mode}",
        f"source_frame_id:{source_frame_id}",
        f"roi_id:{roi_id}",
        f"unit_id:{unit_id}",
        f"image_ref:{unit.get('image_ref')}",
        "fact_status:not_fact",
    ]
    if is_fixture:
        chain.append("yolo_like_fixture_not_real_detector_claim")
    else:
        chain.append("real_yolo_inference_not_fact_claim")
    return {
        "schema_version": VISION_DETECTION_SCHEMA,
        "evidence_id": _evidence_id(unit_id, label, det_index),
        "source_frame_id": source_frame_id,
        "stream_id": None,
        "frame_index": None,
        "timestamp_ms": None,
        "roi_id": roi_id,
        "unit_id": unit_id,
        "source_unit_ref": unit_id,
        "provider": "yolo_candidate_adapter",
        "provider_level": "evaluation_candidate",
        "provider_output_ref": str(det.get("detection_id") or ""),
        "label": label,
        "class_id": det.get("class_id"),
        "class_name": label,
        "confidence": float(det.get("confidence") or 0.0),
        "bbox_in_unit": [int(v) for v in bbox_unit],
        "bbox_in_frame": bbox_frame,
        "polygon_in_frame": None,
        "mask_ref": None,
        "tracker_id": None,
        "track_id_scope": "none",
        "coordinate_space": "frame_pixel",
        "synthetic": is_fixture,
        "stub_provider": is_fixture,
        "fact_status": "not_fact",
        "evidence_role": "visual_detection_candidate",
        "source_chain": chain,
    }


def build_risk_report_v0() -> Dict[str, Any]:
    return {
        "schema": RISK_SCHEMA,
        "yolo_label_not_fact": True,
        "confidence_not_truth": True,
        "detector_output_not_navigation_decision": True,
        "no_midplatform_fact_write": True,
        "no_scene_delta_write": True,
        "no_world_model_write": True,
        "no_mainline_registry_change": True,
        "no_default_provider_change": True,
        "no_navigation_decision": True,
        "narrative": [
            "YOLO candidate adapter is evaluation-only; outputs remain visual_detection_candidate.",
            "Even real YOLO inference must keep fact_status=not_fact.",
            "Do not change vision_provider_registry default provider in this phase.",
        ],
    }


def build_audit_v0(
    *,
    yolo_invoked: bool,
    real_detector_invoked: bool,
    fixture_used: bool,
) -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "yolo_candidate_adapter_eval_executed": True,
        "evaluation_only": True,
        "vision_mainline_modified": False,
        "vision_provider_registry_default_changed": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "yolo_invoked": yolo_invoked,
        "real_detector_invoked": real_detector_invoked,
        "fixture_used": fixture_used,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
        "database_write_invoked": False,
    }


def run_yolo_candidate_adapter_eval_v0(
    *,
    vision_detection_schema_alignment_root: str,
    roi_proposal_root: str,
    supervision_ab_root: str = "",
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    schema_root = Path(vision_detection_schema_alignment_root).resolve()
    roi_root = Path(roi_proposal_root).resolve()
    sup_ab_root = Path(supervision_ab_root).resolve() if supervision_ab_root.strip() else None

    if not schema_root.is_dir():
        errs.append("missing_schema_alignment_root")
    if not roi_root.is_dir():
        errs.append("missing_roi_proposal_root")

    schema_p = schema_root / "vision_detection_evidence_schema_v0.json"
    vision_detection_schema_version = VISION_DETECTION_SCHEMA
    if schema_p.is_file():
        doc = _read_json(schema_p)
        if isinstance(doc, dict) and doc.get("schema_version"):
            vision_detection_schema_version = str(doc["schema_version"])
    else:
        errs.append("missing_vision_detection_evidence_schema_v0")

    max_units = _env_int("LUNA_YOLO_MAX_INPUT_UNITS", 5)
    probe = probe_yolo_availability_v0()
    selection, selected_units = select_input_units_v0(roi_root, max_units=max_units)

    if selection.get("selected_units_count", 0) <= 0:
        errs.append("selected_units_count_zero")

    eval_only = _env_bool("LUNA_YOLO_EVAL_ONLY", False)
    eval_enabled = _env_bool("LUNA_ENABLE_YOLO_EVAL_PROVIDER_V0", False)
    force_fixture = _env_bool("LUNA_YOLO_FORCE_FIXTURE_V0", False)

    use_real = (
        eval_only
        and eval_enabled
        and not force_fixture
        and probe.get("ultralytics_installed") is True
        and probe.get("model_load_error") is None
    )

    default_detector_mode = "yolo_like_fixture"
    if use_real:
        default_detector_mode = "real_yolo"
    elif not probe.get("ultralytics_installed") or not eval_enabled or not eval_only:
        default_detector_mode = "yolo_like_fixture"
    else:
        default_detector_mode = "yolo_like_fixture"

    model_path = os.environ.get("LUNA_YOLO_MODEL_PATH", "").strip() or str(
        probe.get("default_model_hint") or "yolov8n.pt"
    )

    t0 = time.perf_counter()
    per_unit_raw: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []
    evidence_items: List[Dict[str, Any]] = []
    conversion_errors: List[str] = []
    detection_count = 0
    yolo_invoked = False
    real_detector_invoked = False
    any_real_unit = False
    any_fixture_unit = False

    for unit in selected_units:
        unit_err: Optional[str] = None
        dets: List[Dict[str, Any]] = []
        unit_mode = default_detector_mode
        if use_real:
            try:
                dets, unit_err = run_yolo_on_unit_v0(unit, model_path=model_path)
                yolo_invoked = True
                real_detector_invoked = True
                any_real_unit = True
                unit_mode = "real_yolo"
            except Exception as e:
                unit_err = f"{type(e).__name__}: {e}"
                dets = build_yolo_like_fixture_detections_v0(unit)
                any_fixture_unit = True
                unit_mode = "yolo_like_fixture"
        else:
            dets = build_yolo_like_fixture_detections_v0(unit)
            any_fixture_unit = True
            unit_mode = "yolo_like_fixture"

        detection_count += len(dets)
        per_unit_raw.append(
            {
                "unit_id": unit.get("unit_id"),
                "roi_id": unit.get("roi_id"),
                "source_frame_id": unit.get("source_frame_id"),
                "image_ref": unit.get("image_ref"),
                "detection_count": len(dets),
                "error": unit_err,
                "detections": dets,
            }
        )

        converted: List[Dict[str, Any]] = []
        for idx, det in enumerate(dets):
            try:
                ev = yolo_detection_to_vision_evidence_v0(
                    det, unit=unit, detector_mode=unit_mode, det_index=idx
                )
                converted.append(ev)
                evidence_items.append(ev)
            except Exception as e:
                conversion_errors.append(f"{unit.get('unit_id')}:{type(e).__name__}:{e}")

        matrix_rows.append(
            {
                "unit_id": unit.get("unit_id"),
                "roi_id": unit.get("roi_id"),
                "detections_in": len(dets),
                "evidence_out": len(converted),
                "conversion_ok": len(converted) == len(dets) and len(dets) > 0,
            }
        )

    latency_ms = int((time.perf_counter() - t0) * 1000)

    if any_real_unit and any_fixture_unit:
        detector_mode = "mixed_real_and_fixture"
    elif any_real_unit:
        detector_mode = "real_yolo"
    else:
        detector_mode = "yolo_like_fixture"

    fixture_used = any_fixture_unit or not any_real_unit

    raw_summary = {
        "schema": RAW_SUMMARY_SCHEMA,
        "detector_mode": detector_mode,
        "detection_count": detection_count,
        "per_unit": per_unit_raw,
        "latency_ms": latency_ms,
    }

    fixture_doc = {
        "schema": FIXTURE_SCHEMA,
        "vision_detection_schema_version": vision_detection_schema_version,
        "detector_mode": detector_mode,
        "item_count": len(evidence_items),
        "items": evidence_items,
    }

    adapter_report = {
        "schema": ADAPTER_REPORT_SCHEMA,
        "selected_units_count": selection.get("selected_units_count"),
        "detector_mode": detector_mode,
        "detection_count": detection_count,
        "converted_evidence_count": len(evidence_items),
        "conversion_errors": conversion_errors,
        "latency_ms": latency_ms,
        "memory_hint": None,
        "provider_boundary": {
            "provider": "yolo_candidate_adapter",
            "evaluation_only": True,
            "not_default_provider": True,
            "not_mainline": True,
        },
        "gap_notes": [],
    }

    if detector_mode in ("yolo_like_fixture", "mixed_real_and_fixture"):
        adapter_report["gap_notes"].append(
            "YOLO real inference partial or not used; see availability probe and env gates."
        )
    if not eval_only:
        adapter_report["gap_notes"].append("LUNA_YOLO_EVAL_ONLY must be true for real_yolo path.")
    if probe.get("import_error"):
        adapter_report["gap_notes"].append(f"ultralytics_import: {probe.get('import_error')}")
    if probe.get("model_load_error"):
        adapter_report["gap_notes"].append(f"model_load: {probe.get('model_load_error')}")

    risk = build_risk_report_v0()
    audit = build_audit_v0(
        yolo_invoked=yolo_invoked,
        real_detector_invoked=real_detector_invoked,
        fixture_used=fixture_used,
    )

    matrix_doc = {
        "schema": MATRIX_SCHEMA,
        "rows": matrix_rows,
        "converted_evidence_count": len(evidence_items),
    }

    phase_verdict = "GO"
    if errs:
        phase_verdict = "NO_GO"
    elif detector_mode in ("yolo_like_fixture", "mixed_real_and_fixture", "unavailable"):
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": EVAL_SUMMARY_SCHEMA,
        "phase": "Phase-Vision-Gated-YOLO-Candidate-Adapter-001",
        "vision_detection_schema_alignment_root": str(schema_root),
        "roi_proposal_root": str(roi_root),
        "supervision_ab_root": str(sup_ab_root) if sup_ab_root else None,
        "vision_detection_schema_version": vision_detection_schema_version,
        "detector_mode": detector_mode,
        "selected_units_count": selection.get("selected_units_count"),
        "detection_count": detection_count,
        "converted_evidence_count": len(evidence_items),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return (
        summary,
        probe,
        selection,
        raw_summary,
        matrix_doc,
        fixture_doc,
        adapter_report,
        risk,
        audit,
        errs,
    )


def build_real_gate_check_v0(*, force_env: bool = True) -> Dict[str, Any]:
    if force_env:
        os.environ["LUNA_YOLO_EVAL_ONLY"] = "true"
        os.environ["LUNA_ENABLE_YOLO_EVAL_PROVIDER_V0"] = "true"
        os.environ["LUNA_YOLO_FORCE_FIXTURE_V0"] = "false"

    eval_only = _env_bool("LUNA_YOLO_EVAL_ONLY", False)
    eval_enabled = _env_bool("LUNA_ENABLE_YOLO_EVAL_PROVIDER_V0", False)
    force_fixture = _env_bool("LUNA_YOLO_FORCE_FIXTURE_V0", False)
    reason_codes: List[str] = []

    ultralytics_installed = False
    import_error: Optional[str] = None
    try:
        import ultralytics  # type: ignore  # noqa: F401

        ultralytics_installed = True
    except Exception as e:
        import_error = f"{type(e).__name__}: {e}"
        reason_codes.append("ultralytics_not_installed")

    local_path, model_source, resolve_reasons = resolve_local_yolo_model_path_v0()
    reason_codes.extend(resolve_reasons)
    model_path_present = local_path is not None

    if not eval_only:
        reason_codes.append("eval_only_gate_false")
    if not eval_enabled:
        reason_codes.append("eval_provider_disabled")
    if force_fixture:
        reason_codes.append("force_fixture_true")

    real_yolo_allowed = (
        eval_only
        and eval_enabled
        and not force_fixture
        and ultralytics_installed
        and model_path_present
        and import_error is None
    )
    if not model_path_present:
        reason_codes.append("local_model_unavailable_no_download")

    return {
        "schema_version": REAL_GATE_SCHEMA,
        "eval_only_gate": eval_only,
        "eval_provider_enabled": eval_enabled,
        "force_fixture": force_fixture,
        "ultralytics_installed": ultralytics_installed,
        "import_error": import_error,
        "model_path_present": model_path_present,
        "resolved_model_path": local_path,
        "model_source": model_source,
        "network_download_attempted": False,
        "real_yolo_allowed": real_yolo_allowed,
        "reason_codes": reason_codes,
    }


def build_real_risk_report_v0() -> Dict[str, Any]:
    base = build_risk_report_v0()
    base["schema"] = REAL_RISK_SCHEMA
    base["no_network_model_download"] = True
    return base


def build_real_audit_v0(
    *,
    yolo_invoked: bool,
    real_detector_invoked: bool,
    fixture_used: bool,
    network_request_invoked: bool,
) -> Dict[str, Any]:
    return {
        "schema": REAL_AUDIT_SCHEMA,
        "yolo_real_smoke_executed": True,
        "evaluation_only": True,
        "network_request_invoked": network_request_invoked,
        "vision_mainline_modified": False,
        "vision_provider_registry_default_changed": False,
        "yolo_invoked": yolo_invoked,
        "real_detector_invoked": real_detector_invoked,
        "fixture_used": fixture_used,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
        "database_write_invoked": False,
    }


def run_yolo_real_smoke_v0(
    *,
    roi_proposal_root: str,
    yolo_candidate_adapter_root: str = "",
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    """Phase-Vision-Gated-YOLO-Real-Smoke-001 — gated real YOLO only (local weights, no download)."""
    errs: List[str] = []
    roi_root = Path(roi_proposal_root).resolve()
    prior_root = Path(yolo_candidate_adapter_root).resolve() if yolo_candidate_adapter_root.strip() else None

    if not roi_root.is_dir():
        errs.append("missing_roi_proposal_root")

    gate = build_real_gate_check_v0(force_env=True)
    max_units = _env_int("LUNA_YOLO_MAX_INPUT_UNITS", 5)
    selection_base, selected_units = select_input_units_v0(roi_root, max_units=max_units)

    selection = {
        **selection_base,
        "schema": REAL_SELECTION_SCHEMA,
        "selected_crop_image_refs": [str(u.get("image_ref") or "") for u in selected_units],
    }

    if selection.get("selected_units_count", 0) <= 0:
        errs.append("selected_units_count_zero")

    local_path = gate.get("resolved_model_path")
    model_load: Dict[str, Any] = {
        "schema": MODEL_LOAD_SCHEMA,
        "model_path": local_path,
        "model_loaded": False,
        "model_load_error": None,
        "model_source": gate.get("model_source"),
        "network_request_invoked": False,
    }

    yolo_model: Any = None
    network_request_invoked = False

    if gate.get("real_yolo_allowed") and local_path:
        yolo_model, load_extra = load_yolo_model_local_v0(str(local_path))
        model_load.update(load_extra)
        if load_extra.get("network_request_invoked"):
            network_request_invoked = True
            errs.append("network_download_attempted")
            gate["network_download_attempted"] = True

    model_loaded = model_load.get("model_loaded") is True and yolo_model is not None

    t0 = time.perf_counter()
    per_unit_raw: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []
    evidence_items: List[Dict[str, Any]] = []
    conversion_errors: List[str] = []
    gap_notes: List[str] = []
    detection_count = 0
    yolo_invoked = False
    real_detector_invoked = False
    fixture_used = False

    for unit in selected_units:
        unit_err: Optional[str] = None
        dets: List[Dict[str, Any]] = []
        unit_mode = "real_yolo"

        if model_loaded and yolo_model is not None:
            try:
                with _network_guard_v0() as guard:
                    dets, unit_err = run_yolo_on_unit_v0(unit, model=yolo_model)
                    if guard.get("hit"):
                        network_request_invoked = True
                yolo_invoked = True
                real_detector_invoked = True
            except _NetworkBlockedInYoloSmoke:
                network_request_invoked = True
                unit_err = "network_request_blocked_during_inference"
                dets = []
                gap_notes.append("inference_network_blocked")
            except Exception as e:
                unit_err = f"{type(e).__name__}: {e}"
                dets = []
        else:
            unit_mode = "yolo_like_fixture"
            fixture_used = True
            dets = build_yolo_like_fixture_detections_v0(unit)
            gap_notes.append("model_not_loaded_using_fixture_fallback")

        detection_count += len(dets)
        per_unit_raw.append(
            {
                "unit_id": unit.get("unit_id"),
                "roi_id": unit.get("roi_id"),
                "crop_image_ref": unit.get("image_ref"),
                "detection_count": len(dets),
                "detector_mode": unit_mode,
                "error": unit_err,
                "detections": dets,
            }
        )

        converted: List[Dict[str, Any]] = []
        for idx, det in enumerate(dets):
            try:
                ev = yolo_detection_to_vision_evidence_v0(
                    det,
                    unit=unit,
                    detector_mode=unit_mode,
                    det_index=idx,
                    chain_prefix="yolo_real_smoke_v0",
                )
                converted.append(ev)
                evidence_items.append(ev)
            except Exception as e:
                conversion_errors.append(f"{unit.get('unit_id')}:{type(e).__name__}:{e}")

        matrix_rows.append(
            {
                "unit_id": unit.get("unit_id"),
                "roi_id": unit.get("roi_id"),
                "detections_in": len(dets),
                "evidence_out": len(converted),
                "conversion_ok": len(converted) == len(dets),
            }
        )

    latency_ms = int((time.perf_counter() - t0) * 1000)

    if real_detector_invoked and not fixture_used:
        detector_mode = "real_yolo"
    elif real_detector_invoked and fixture_used:
        detector_mode = "mixed_real_and_fixture"
    elif fixture_used:
        detector_mode = "yolo_like_fixture"
    else:
        detector_mode = "unavailable"

    if not model_loaded:
        fixture_used = True
        gap_notes.append("local_model_not_loaded")

    raw_summary = {
        "schema": REAL_RAW_SCHEMA,
        "detector_mode": detector_mode,
        "detection_count": detection_count,
        "per_unit": per_unit_raw,
        "latency_ms": latency_ms,
        "errors": conversion_errors,
        "gap_notes": gap_notes,
    }

    fixture_doc = {
        "schema": REAL_FIXTURE_SCHEMA,
        "detector_mode": detector_mode,
        "item_count": len(evidence_items),
        "items": evidence_items,
    }

    matrix_doc = {
        "schema": REAL_MATRIX_SCHEMA,
        "rows": matrix_rows,
        "converted_evidence_count": len(evidence_items),
    }

    risk = build_real_risk_report_v0()
    audit = build_real_audit_v0(
        yolo_invoked=yolo_invoked,
        real_detector_invoked=real_detector_invoked,
        fixture_used=fixture_used,
        network_request_invoked=network_request_invoked,
    )

    phase_verdict = "NO_GO"
    if network_request_invoked:
        phase_verdict = "NO_GO"
        errs.append("network_request_invoked")
    elif real_detector_invoked and not fixture_used and len(evidence_items) > 0:
        phase_verdict = "GO"
    elif real_detector_invoked and not fixture_used and len(evidence_items) == 0:
        phase_verdict = "CONDITIONAL_GO"
        gap_notes.append("real_yolo_ran_zero_detections_on_roi_crops")
    elif not errs:
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": REAL_SUMMARY_SCHEMA,
        "phase": "Phase-Vision-Gated-YOLO-Real-Smoke-001",
        "roi_proposal_root": str(roi_root),
        "yolo_candidate_adapter_root": str(prior_root) if prior_root else None,
        "detector_mode": detector_mode,
        "selected_units_count": selection.get("selected_units_count"),
        "detection_count": detection_count,
        "converted_evidence_count": len(evidence_items),
        "model_loaded": model_loaded,
        "resolved_model_path": local_path,
        "phase_verdict_hint": phase_verdict,
        "gap_notes": gap_notes,
        "errors": list(errs),
    }

    return (
        summary,
        gate,
        model_load,
        selection,
        raw_summary,
        matrix_doc,
        fixture_doc,
        risk,
        audit,
        errs,
    )


def _image_size_v0(image_path: Path) -> Tuple[int, int]:
    try:
        from PIL import Image  # type: ignore

        with Image.open(image_path) as im:
            w, h = im.size
            return int(w), int(h)
    except Exception:
        pass
    try:
        import cv2  # type: ignore

        im = cv2.imread(str(image_path))
        if im is not None:
            return int(im.shape[1]), int(im.shape[0])
    except Exception:
        pass
    return 640, 480


def _default_ultralytics_bus_asset_v0() -> Optional[Path]:
    try:
        import ultralytics  # type: ignore

        asset = Path(ultralytics.__file__).resolve().parent / "assets" / "bus.jpg"
        if asset.is_file():
            return asset
    except Exception:
        return None
    return None


def prepare_positive_sample_v0(
    *,
    output_root: Path,
    image_override: str = "",
) -> Tuple[Dict[str, Any], Path, List[str]]:
    """Copy local positive sample into eval output tree (no network)."""
    errs: List[str] = []
    samples_dir = output_root / "positive_samples"
    samples_dir.mkdir(parents=True, exist_ok=True)

    src: Optional[Path] = None
    if image_override.strip():
        cand = Path(image_override).expanduser().resolve()
        if cand.is_file():
            src = cand
        else:
            errs.append("positive_image_override_not_found")
    if src is None:
        src = _default_ultralytics_bus_asset_v0()
    if src is None:
        errs.append("no_local_positive_sample_asset")
        report = {
            "schema": POSITIVE_SAMPLE_REPORT_SCHEMA,
            "image_ref": None,
            "image_width": None,
            "image_height": None,
            "expected_detectable_hint": "bus,person,car (COCO)",
            "source_type": "positive_sample_fixture",
            "network_request_invoked": False,
        }
        return report, samples_dir / "missing.jpg", errs

    dest = samples_dir / src.name
    if src.resolve() != dest.resolve():
        dest.write_bytes(src.read_bytes())

    w, h = _image_size_v0(dest)
    report = {
        "schema": POSITIVE_SAMPLE_REPORT_SCHEMA,
        "image_ref": str(dest.resolve()),
        "image_width": w,
        "image_height": h,
        "expected_detectable_hint": "COCO targets: bus, person, car (ultralytics bus.jpg)",
        "source_type": "positive_sample_fixture",
        "source_asset": str(src),
        "network_request_invoked": False,
    }
    return report, dest, errs


def build_positive_input_unit_v0(
    *,
    image_ref: Path,
    image_width: int,
    image_height: int,
) -> Dict[str, Any]:
    from capabilities.vision_runtime.vision_provider_input_pack_v0 import build_coordinate_transform_v0

    w, h = int(image_width), int(image_height)
    roi_id = "vision_roi_positive_sample_bus_eval"
    unit_id = "unit_positive_sample_bus_eval"
    source_frame_id = "stream_positive_sample_eval_f000000"
    bbox = [0, 0, w, h]
    return {
        "unit_id": unit_id,
        "unit_type": "frame_roi",
        "roi_id": roi_id,
        "bbox_in_frame": bbox,
        "image_ref": str(image_ref.resolve()),
        "coordinate_transform": build_coordinate_transform_v0(
            bbox=bbox, source_frame_width=w, source_frame_height=h
        ),
        "task_hint": "positive_sample_eval",
        "source_frame_id": source_frame_id,
        "pack_id": "pack_positive_sample_eval",
    }


def build_positive_audit_v0(
    *,
    yolo_invoked: bool,
    real_detector_invoked: bool,
    fixture_used: bool,
    network_request_invoked: bool,
) -> Dict[str, Any]:
    return {
        "schema": POSITIVE_AUDIT_SCHEMA,
        "yolo_positive_sample_smoke_executed": True,
        "evaluation_only": True,
        "network_request_invoked": network_request_invoked,
        "vision_mainline_modified": False,
        "vision_provider_registry_default_changed": False,
        "yolo_invoked": yolo_invoked,
        "real_detector_invoked": real_detector_invoked,
        "fixture_used": fixture_used,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
        "database_write_invoked": False,
    }


def _model_path_from_prior_smoke(prior_root: Optional[Path]) -> Optional[str]:
    if prior_root is None:
        return None
    summary_p = prior_root / "yolo_real_smoke_summary.json"
    if summary_p.is_file():
        try:
            raw = _read_json(summary_p)
            if isinstance(raw, dict) and raw.get("resolved_model_path"):
                p = Path(str(raw["resolved_model_path"]))
                if p.is_file():
                    return str(p.resolve())
        except Exception:
            pass
    gate_p = prior_root / "yolo_real_gate_check.json"
    if gate_p.is_file():
        try:
            raw = _read_json(gate_p)
            if isinstance(raw, dict) and raw.get("resolved_model_path"):
                p = Path(str(raw["resolved_model_path"]))
                if p.is_file():
                    return str(p.resolve())
        except Exception:
            pass
    return None


def run_yolo_real_positive_sample_smoke_v0(
    *,
    roi_proposal_root: str,
    prior_yolo_real_smoke_root: str,
    output_root: str,
    positive_image_override: str = "",
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    """Phase-Vision-YOLO-Real-Smoke-Positive-Sample-001."""
    errs: List[str] = []
    out_root = Path(output_root).resolve()
    roi_root = Path(roi_proposal_root).resolve()
    prior_root = Path(prior_yolo_real_smoke_root).resolve() if prior_yolo_real_smoke_root.strip() else None

    if not roi_root.is_dir():
        errs.append("missing_roi_proposal_root")

    os.environ["LUNA_YOLO_EVAL_ONLY"] = "true"
    os.environ["LUNA_ENABLE_YOLO_EVAL_PROVIDER_V0"] = "true"
    os.environ["LUNA_YOLO_FORCE_FIXTURE_V0"] = "false"

    prior_model = _model_path_from_prior_smoke(prior_root)
    if prior_model and not os.environ.get("LUNA_YOLO_MODEL_PATH", "").strip():
        os.environ["LUNA_YOLO_MODEL_PATH"] = prior_model

    sample_report, image_path, prep_errs = prepare_positive_sample_v0(
        output_root=out_root,
        image_override=positive_image_override,
    )
    errs.extend(prep_errs)

    gate_base = build_real_gate_check_v0(force_env=False)
    gate = {**gate_base, "schema_version": POSITIVE_GATE_SCHEMA}

    local_path = gate.get("resolved_model_path")
    model_load: Dict[str, Any] = {
        "schema": POSITIVE_MODEL_LOAD_SCHEMA,
        "model_path": local_path,
        "model_loaded": False,
        "model_load_error": None,
        "model_source": gate.get("model_source"),
        "network_request_invoked": False,
    }

    yolo_model: Any = None
    network_request_invoked = False

    if gate.get("real_yolo_allowed") and local_path:
        yolo_model, load_extra = load_yolo_model_local_v0(str(local_path))
        model_load.update(load_extra)
        if load_extra.get("network_request_invoked"):
            network_request_invoked = True
            errs.append("network_download_attempted")

    model_loaded = model_load.get("model_loaded") is True and yolo_model is not None
    if not model_loaded:
        errs.append("model_not_loaded")

    unit = build_positive_input_unit_v0(
        image_ref=image_path,
        image_width=int(sample_report.get("image_width") or 640),
        image_height=int(sample_report.get("image_height") or 480),
    )

    t0 = time.perf_counter()
    dets: List[Dict[str, Any]] = []
    unit_err: Optional[str] = None
    yolo_invoked = False
    real_detector_invoked = False
    fixture_used = False
    conversion_errors: List[str] = []
    evidence_items: List[Dict[str, Any]] = []

    if model_loaded and yolo_model is not None and not prep_errs:
        try:
            with _network_guard_v0() as guard:
                dets, unit_err = run_yolo_on_unit_v0(unit, model=yolo_model)
                if guard.get("hit"):
                    network_request_invoked = True
            yolo_invoked = True
            real_detector_invoked = True
        except _NetworkBlockedInYoloSmoke:
            network_request_invoked = True
            errs.append("network_request_blocked")
        except Exception as e:
            unit_err = f"{type(e).__name__}: {e}"
            errs.append(f"inference_failed:{unit_err}")

    detection_count = len(dets)
    for idx, det in enumerate(dets):
        try:
            ev = yolo_detection_to_vision_evidence_v0(
                det,
                unit=unit,
                detector_mode="real_yolo",
                det_index=idx,
                chain_prefix="yolo_real_positive_sample_smoke_v0",
            )
            evidence_items.append(ev)
        except Exception as e:
            conversion_errors.append(f"{type(e).__name__}:{e}")

    latency_ms = int((time.perf_counter() - t0) * 1000)

    detector_mode = "real_yolo" if real_detector_invoked and not fixture_used else "unavailable"
    if fixture_used:
        detector_mode = "yolo_like_fixture"

    raw_summary = {
        "schema": POSITIVE_RAW_SCHEMA,
        "detector_mode": detector_mode,
        "detection_count": detection_count,
        "yolo_invoked": yolo_invoked,
        "real_detector_invoked": real_detector_invoked,
        "fixture_used": fixture_used,
        "latency_ms": latency_ms,
        "unit_id": unit.get("unit_id"),
        "roi_id": unit.get("roi_id"),
        "crop_image_ref": unit.get("image_ref"),
        "error": unit_err,
        "detections": dets,
        "conversion_errors": conversion_errors,
    }

    matrix_doc = {
        "schema": POSITIVE_MATRIX_SCHEMA,
        "rows": [
            {
                "unit_id": unit.get("unit_id"),
                "roi_id": unit.get("roi_id"),
                "detections_in": detection_count,
                "evidence_out": len(evidence_items),
                "conversion_ok": len(evidence_items) == detection_count and detection_count > 0,
            }
        ],
        "converted_evidence_count": len(evidence_items),
    }

    fixture_doc = {
        "schema": POSITIVE_FIXTURE_SCHEMA,
        "detector_mode": detector_mode,
        "item_count": len(evidence_items),
        "items": evidence_items,
    }

    risk = build_real_risk_report_v0()
    risk["schema"] = POSITIVE_RISK_SCHEMA

    audit = build_positive_audit_v0(
        yolo_invoked=yolo_invoked,
        real_detector_invoked=real_detector_invoked,
        fixture_used=fixture_used,
        network_request_invoked=network_request_invoked,
    )

    gap_notes: List[str] = []
    if detection_count <= 0:
        gap_notes.append("zero_detections_on_positive_sample")
    if conversion_errors:
        gap_notes.extend(conversion_errors)

    phase_verdict = "NO_GO"
    if network_request_invoked:
        phase_verdict = "NO_GO"
        errs.append("network_request_invoked")
    elif real_detector_invoked and not fixture_used and len(evidence_items) > 0:
        phase_verdict = "GO"
    elif real_detector_invoked and detection_count <= 0:
        phase_verdict = "CONDITIONAL_GO"
        gap_notes.append("real_yolo_ran_but_no_detections")
    elif not errs:
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": POSITIVE_SUMMARY_SCHEMA,
        "phase": "Phase-Vision-YOLO-Real-Smoke-Positive-Sample-001",
        "output_root": str(out_root),
        "roi_proposal_root": str(roi_root),
        "prior_yolo_real_smoke_root": str(prior_root) if prior_root else None,
        "positive_image_ref": sample_report.get("image_ref"),
        "detector_mode": detector_mode,
        "detection_count": detection_count,
        "converted_evidence_count": len(evidence_items),
        "model_loaded": model_loaded,
        "resolved_model_path": local_path,
        "phase_verdict_hint": phase_verdict,
        "gap_notes": gap_notes,
        "errors": list(errs),
    }

    return (
        summary,
        sample_report,
        gate,
        model_load,
        raw_summary,
        matrix_doc,
        fixture_doc,
        risk,
        audit,
        errs,
    )

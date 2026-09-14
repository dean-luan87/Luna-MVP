# -*- coding: utf-8 -*-
"""External Roboflow Supervision adapter experiment (evaluation-only, not mainline)."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


EXPERIMENT_SCHEMA = "external_supervision_adapter_experiment_v0"
ROI_CANDIDATE_SCHEMA_VERSION = "vision_roi_proposal_candidate_v0"


def load_first_frame_envelope_v0(ingest_root: Path) -> Dict[str, Any]:
    path = Path(ingest_root) / "video_frame_envelopes.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if isinstance(obj, dict):
            return obj
    raise FileNotFoundError(f"no envelope in {path}")


def probe_supervision_v0() -> Dict[str, Any]:
    """Import probe + shallow feature flags (no YOLO, no real detector)."""
    out: Dict[str, Any] = {
        "schema": "external_supervision_availability_probe_v0",
        "supervision_installed": False,
        "supervision_version": None,
        "import_error": None,
        "supported_features_probe": {
            "detections_class": False,
            "polygon_or_mask_helpers": False,
            "tracker_module_hint": False,
            "tracker_capability_note": "",
        },
    }
    try:
        import supervision as sv  # type: ignore

        out["supervision_installed"] = True
        out["supervision_version"] = str(getattr(sv, "__version__", "unknown"))
        out["supported_features_probe"]["detections_class"] = hasattr(sv, "Detections")
        poly = getattr(sv, "PolygonZone", None) or getattr(sv, "Point", None)
        out["supported_features_probe"]["polygon_or_mask_helpers"] = poly is not None or hasattr(sv, "mask")
        tr = False
        note = "tracker API not probed or unavailable in this supervision build"
        for attr in ("ByteTrack", "BoxMOT"):
            if hasattr(sv, attr):
                tr = True
                note = f"found supervision attribute: {attr}"
                break
        if not tr:
            try:
                importlib.import_module("supervision.tracker.byte_tracker")
                tr = True
                note = "supervision.tracker.byte_tracker import ok"
            except Exception as e:
                note = f"byte_tracker import: {type(e).__name__}"
        out["supported_features_probe"]["tracker_module_hint"] = tr
        out["supported_features_probe"]["tracker_capability_note"] = note
    except Exception as e:
        out["import_error"] = f"{type(e).__name__}: {e}"
    return out


def build_synthetic_detections_v0(*, frame_w: int, frame_h: int) -> List[Dict[str, Any]]:
    """2–3 synthetic boxes in frame pixel space (no model)."""
    w, h = max(1, int(frame_w)), max(1, int(frame_h))
    return [
        {
            "detection_id": "syn_001",
            "bbox_xyxy": [int(w * 0.05), int(h * 0.1), int(w * 0.45), int(h * 0.35)],
            "class_name": "sign",
            "confidence": 0.91,
            "mask_ref": None,
            "tracker_id": None,
        },
        {
            "detection_id": "syn_002",
            "bbox_xyxy": [int(w * 0.1), int(h * 0.55), int(w * 0.9), int(h * 0.92)],
            "class_name": "ground_band",
            "confidence": 0.72,
            "mask_ref": None,
            "tracker_id": None,
        },
        {
            "detection_id": "syn_003",
            "bbox_xyxy": [int(w * 0.55), int(h * 0.08), int(w * 0.95), int(h * 0.42)],
            "class_name": "nearfield",
            "confidence": 0.55,
            "mask_ref": None,
            "tracker_id": None,
        },
    ]


def build_vision_roi_proposal_candidate_v0(
    *,
    source_frame_id: str,
    source_image_ref: str,
    frame_envelope_ref: str,
    synthetic_detections: List[Dict[str, Any]],
) -> Dict[str, Any]:
    roi_items: List[Dict[str, Any]] = []
    for i, d in enumerate(synthetic_detections, start=1):
        x1, y1, x2, y2 = (int(v) for v in d["bbox_xyxy"])
        roi_items.append(
            {
                "roi_id": f"vision_roi_{i:03d}",
                "bbox_in_frame": [x1, y1, x2, y2],
                "class_name": str(d.get("class_name") or "unknown"),
                "confidence": float(d.get("confidence") or 0.0),
                "tracker_id": d.get("tracker_id"),
                "mask_ref": d.get("mask_ref"),
                "task_hint": "unknown",
                "coordinate_space": "frame_pixel",
            }
        )
    return {
        "schema_version": ROI_CANDIDATE_SCHEMA_VERSION,
        "source_frame_id": source_frame_id,
        "source_image_ref": source_image_ref,
        "proposal_source": "supervision_synthetic_adapter",
        "roi_items": roi_items,
        "source_chain": [
            frame_envelope_ref,
            "supervision_adapter_probe",
            "synthetic_detection_created",
            "roi_candidate_generated",
        ],
    }


def build_external_supervision_feature_matrix_v0(probe: Dict[str, Any]) -> Dict[str, Any]:
    sf = probe.get("supported_features_probe") if isinstance(probe.get("supported_features_probe"), dict) else {}
    return {
        "schema": "external_supervision_feature_matrix_v0",
        "supervision_installed": bool(probe.get("supervision_installed")),
        "supervision_version": probe.get("supervision_version"),
        "rows": [
            {"feature": "Detections API", "available": bool(sf.get("detections_class"))},
            {"feature": "polygon_or_mask_helpers", "available": bool(sf.get("polygon_or_mask_helpers"))},
            {"feature": "tracker_module_hint", "available": bool(sf.get("tracker_module_hint"))},
        ],
        "tracker_capability_note": str(sf.get("tracker_capability_note") or ""),
    }


def build_external_supervision_experiment_audit_v0(
    *,
    supervision_import_attempted: bool,
    yolo_invoked: bool = False,
    real_detector_invoked: bool = False,
) -> Dict[str, Any]:
    return {
        "schema": "external_supervision_experiment_audit_v0",
        "supervision_import_attempted": bool(supervision_import_attempted),
        "yolo_invoked": bool(yolo_invoked),
        "real_detector_invoked": bool(real_detector_invoked),
        "real_camera_invoked": False,
        "ocr_invoked": False,
        "vlm_invoked": False,
        "supervision_mainline_invoked": False,
        "vision_recognition_provider_invoked": False,
        "navigation_decision_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "runtime_mainline_modified": False,
    }


def run_external_supervision_adapter_experiment_v0(
    video_ingest_root: Path,
    output_root: Path,
) -> Tuple[Dict[str, Any], Dict[str, Any], List[Dict[str, Any]], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Returns summary, probe, synthetic_detections, roi_candidate, feature_matrix, audit, envelope."""
    video_ingest_root = Path(video_ingest_root).resolve()
    output_root = Path(output_root).resolve()

    env = load_first_frame_envelope_v0(video_ingest_root)
    frame_id = str(env.get("frame_id") or "")
    image_ref = str(env.get("image_ref") or "")
    fw = int(env.get("width") or 640)
    fh = int(env.get("height") or 480)
    frame_envelope_ref = f"frame_envelope_ref:{frame_id}"

    probe = probe_supervision_v0()
    synthetic = build_synthetic_detections_v0(frame_w=fw, frame_h=fh)
    roi = build_vision_roi_proposal_candidate_v0(
        source_frame_id=frame_id,
        source_image_ref=image_ref,
        frame_envelope_ref=frame_envelope_ref,
        synthetic_detections=synthetic,
    )
    feature_matrix = build_external_supervision_feature_matrix_v0(probe)
    audit = build_external_supervision_experiment_audit_v0(
        supervision_import_attempted=True,
        yolo_invoked=False,
        real_detector_invoked=False,
    )

    summary = {
        "schema": "external_supervision_adapter_experiment_summary_v0",
        "phase": "Phase-Vision-External-Supervision-Adapter-Experiment-001",
        "experiment_schema": EXPERIMENT_SCHEMA,
        "experiment_scope": "external_evaluation_only_not_mainline",
        "video_ingest_root": str(video_ingest_root),
        "output_root": str(output_root),
        "source_frame_id": frame_id,
        "source_image_ref": image_ref,
        "supervision_installed": bool(probe.get("supervision_installed")),
        "supervision_version": probe.get("supervision_version"),
        "roi_items_count": len(roi.get("roi_items") or []),
        "supervision_install_gap_report": {
            "complete": True,
            "import_error": probe.get("import_error"),
            "hint": "Install Roboflow supervision in the same Python env as the experiment runner to reach GO on import probe.",
            "pip_example": "pip install supervision",
        },
    }

    return summary, probe, synthetic, roi, feature_matrix, audit, env

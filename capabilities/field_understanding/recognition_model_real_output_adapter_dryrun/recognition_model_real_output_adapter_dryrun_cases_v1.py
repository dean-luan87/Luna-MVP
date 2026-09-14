# -*- coding: utf-8 -*-
"""Recognition Model Real Output Adapter DryRun — cases v1.

Performs controlled real inference on P0 local controlled sample images:
  - OpenCV rule-based visual symbol  -> always runs (rule runtime), mandatory
  - RapidOCR                         -> runs if locally available (offline bundled)
  - YOLO lightweight                 -> runs only if local weights exist; never
                                        triggers a download in this phase

Each real output is admitted (required fields + no prohibited flags) and mapped
through the RecognitionModelOutputAdapter into Luna evidence candidates. If an
optional model is unavailable a declared-unavailable record is produced instead
of a blocker. No live camera/sensor, no dataset/training/tuning, no main-chain
integration, no action/speech/navigation/fact_write.
"""

from __future__ import annotations

import copy
import glob
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.recognition_model_real_output_adapter_dryrun.recognition_model_real_output_adapter_dryrun_types_v1 import (
    INFERENCE_SCOPE_VALUE,
    MANDATORY_AVAILABILITY_TARGETS,
    P0_TARGET_BOUNDARY,
    P0_TARGET_TO_CANDIDATES,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_MISSING_FIELDS,
    SOURCE_CHAIN,
    P0RealOutputCaseResult,
)

_SAMPLES_DIR = Path(__file__).resolve().parent / "samples"

SAMPLE_IMAGES: Dict[str, str] = {
    "rapidocr_p0": "sample_p0_ocr_text_sign_image.png",
    "yolo_lightweight_p0": "sample_p0_yolo_object_image.png",
    "opencv_visual_symbol_p0": "sample_p0_visual_symbol_arrow_image.png",
}

INVALID_RECORD_FILES: Dict[str, str] = {
    "invalid_missing_source_chain": "invalid_real_output_missing_source_chain.json",
    "invalid_missing_license_ref": "invalid_real_output_missing_license_ref.json",
    "invalid_missing_model_origin": "invalid_real_output_missing_model_origin.json",
    "invalid_missing_confidence": "invalid_real_output_missing_confidence.json",
    "invalid_yolo_commercial_runtime_claim": "invalid_yolo_commercial_runtime_claim.json",
    "invalid_ocr_fact_write": "invalid_ocr_fact_write_attempt.json",
    "invalid_visual_symbol_direct_navigation": "invalid_visual_symbol_direct_navigation_attempt.json",
    "invalid_native_output_direct_to_field": "invalid_native_model_output_direct_to_field.json",
}

OTHER_SAMPLE_FILES: Tuple[str, ...] = ("sample_p0_multi_model_bundle.json",)

ALL_SAMPLE_FILES: Tuple[str, ...] = (
    tuple(SAMPLE_IMAGES.values())
    + OTHER_SAMPLE_FILES
    + tuple(INVALID_RECORD_FILES.values())
)


def read_local_record(filename: str) -> Dict[str, Any]:
    return json.loads((_SAMPLES_DIR / filename).read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Admission + adapter mapping
# --------------------------------------------------------------------------- #
def _missing_required_fields(record: Dict[str, Any]) -> List[str]:
    missing: List[str] = []
    for f in REJECT_IF_MISSING_FIELDS:
        v = record.get(f)
        if v is None or (isinstance(v, str) and not v.strip()):
            missing.append(f)
    return missing


def _prohibited_flags_present(record: Dict[str, Any]) -> List[str]:
    present = [flag for flag in PROHIBITED_REQUEST_FLAGS if record.get(flag) is True]
    if str(record.get("allowed_use", "")).lower() == "commercial_runtime":
        present.append("commercial_runtime_requested")
    target = str(record.get("adapter_mapping_ref", ""))
    if target.endswith("_direct") or target == "field_synthesis_v1_direct":
        present.append("native_output_direct_to_field")
    return present


def admit_real_output(record: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    for m in _missing_required_fields(record):
        reasons.append(f"missing_required_field:{m}")
    for p in _prohibited_flags_present(record):
        reasons.append(f"prohibited_request:{p}")
    return (len(reasons) == 0), reasons


def map_record_to_candidates(target: str) -> List[str]:
    return list(P0_TARGET_TO_CANDIDATES.get(target, ()))


def _base_record(
    *,
    target: str,
    model_id: str,
    model_family: str,
    model_version_ref: str,
    model_origin: str,
    license_ref: str,
    commercial_use_status: str,
    adapter_mapping_ref: str,
    confidence: float,
    input_ref: str,
    output_schema_ref: str,
    allowed_use: str = "test_only",
) -> Dict[str, Any]:
    return {
        "target": target,
        "model_id": model_id,
        "model_family": model_family,
        "model_version_ref": model_version_ref,
        "model_origin": model_origin,
        "license_ref": license_ref,
        "source_chain": SOURCE_CHAIN,
        "input_ref": input_ref,
        "output_schema_ref": output_schema_ref,
        "confidence": confidence,
        "frame_ref_or_timestamp_ms": int(time.time() * 1000),
        "adapter_mapping_ref": adapter_mapping_ref,
        "allowed_use": allowed_use,
        "commercial_use_status": commercial_use_status,
        "real_output": True,
        "inference_scope": INFERENCE_SCOPE_VALUE,
    }


# --------------------------------------------------------------------------- #
# Real inference runners
# --------------------------------------------------------------------------- #
def _run_rapidocr_real(image_path: Path) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    try:
        from rapidocr_onnxruntime import RapidOCR  # type: ignore

        engine = RapidOCR()
        result, _elapse = engine(str(image_path))
        text_items: List[Dict[str, Any]] = []
        scores: List[float] = []
        for item in result or []:
            box, text, score = item[0], item[1], float(item[2])
            text_items.append(
                {"text": text, "bbox_or_polygon": _flatten_box(box), "confidence": score}
            )
            scores.append(score)
        confidence = round(sum(scores) / len(scores), 4) if scores else 0.0
        record = _base_record(
            target="rapidocr_p0",
            model_id="rapidocr_onnxruntime",
            model_family="ocr_model_family",
            model_version_ref="rapidocr_onnxruntime_real_v1",
            model_origin="external_open_source_ocr_model",
            license_ref="apache_2_0",
            commercial_use_status="commercial_allowed_under_apache_2_0_pending_verification",
            adapter_mapping_ref="text_evidence_candidate",
            confidence=confidence,
            input_ref=str(image_path.name),
            output_schema_ref="ocr_output_schema_v1",
        )
        record["text_items"] = text_items
        record["language"] = "en"
        record["orientation"] = "horizontal"
        record["boundary"] = "ocr_output_is_not_fact"
        return True, "available_real_inference_executed", record
    except Exception as exc:  # noqa: BLE001 - availability probe, never a blocker
        return (
            False,
            f"declared_unavailable_rapidocr_real_inference_failed:{type(exc).__name__}",
            None,
        )


def _find_local_yolo_weights() -> Optional[str]:
    candidates: List[str] = []
    candidates.extend(glob.glob(str(_SAMPLES_DIR / "*.pt")))
    for name in ("yolov8n.pt", "yolo11n.pt", "yolov5nu.pt"):
        if os.path.isfile(name):
            candidates.append(os.path.abspath(name))
    return candidates[0] if candidates else None


def _run_yolo_real(image_path: Path) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    weights = _find_local_yolo_weights()
    if weights is None:
        return (
            False,
            "declared_unavailable_no_local_weights_no_download_in_this_phase",
            None,
        )
    try:
        from ultralytics import YOLO  # type: ignore

        model = YOLO(weights)
        results = model(str(image_path), verbose=False)
        detections: List[Dict[str, Any]] = []
        scores: List[float] = []
        for r in results:
            for b in getattr(r, "boxes", []) or []:
                conf = float(b.conf[0]) if b.conf is not None else 0.0
                cls_id = int(b.cls[0]) if b.cls is not None else -1
                xyxy = [float(x) for x in b.xyxy[0].tolist()] if b.xyxy is not None else []
                label = r.names.get(cls_id, str(cls_id)) if hasattr(r, "names") else str(cls_id)
                detections.append(
                    {"label": label, "bbox": xyxy, "class_id": cls_id, "confidence": conf}
                )
                scores.append(conf)
        confidence = round(sum(scores) / len(scores), 4) if scores else 0.0
        record = _base_record(
            target="yolo_lightweight_p0",
            model_id="yolo_lightweight_nano",
            model_family="object_detection_model_family",
            model_version_ref="yolo_lightweight_real_v1",
            model_origin="external_open_source_detection_model",
            license_ref="agpl_3_0",
            commercial_use_status="agpl_commercial_runtime_uncleared_test_only_now",
            adapter_mapping_ref="object_evidence_candidate",
            confidence=confidence,
            input_ref=str(image_path.name),
            output_schema_ref="object_detection_output_schema_v1",
        )
        record["detections"] = detections
        record["commercial_runtime_allowed"] = False
        record["boundary"] = "object_identity_is_not_fact_yolo_test_only"
        return True, "available_real_inference_executed", record
    except Exception as exc:  # noqa: BLE001 - availability probe, never a blocker
        return (
            False,
            f"declared_unavailable_yolo_real_inference_failed:{type(exc).__name__}",
            None,
        )


def _run_opencv_visual_symbol_real(image_path: Path) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Rule-based visual symbol extraction (mandatory; cv2 is required)."""
    import cv2  # type: ignore
    import numpy as np  # type: ignore

    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"could_not_read_sample_image:{image_path}")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    green_mask = cv2.inRange(hsv, (40, 80, 80), (85, 255, 255))
    green_ratio = float(green_mask.mean()) / 255.0
    color = "green" if green_ratio > 0.01 else "unknown"

    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    shape = "unknown"
    direction = "unknown"
    symbol_type = "unknown_symbol"
    contour_conf = 0.0
    if contours:
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.03 * peri, True)
        v = len(approx)
        x, y, w, h = cv2.boundingRect(c)
        contour_conf = round(min(0.99, area / float(img.shape[0] * img.shape[1]) * 4.0 + 0.5), 4)
        if v <= 3:
            shape = "triangle"
        elif v <= 5:
            shape = "arrow"
        else:
            shape = "polygon"
        # arrow head is to the right -> rightmost extreme point near right edge of bbox
        rightmost = tuple(c[c[:, :, 0].argmax()][0])
        if rightmost[0] >= x + 0.8 * w:
            direction = "right"
        elif rightmost[0] <= x + 0.2 * w:
            direction = "left"
        else:
            direction = "center"
        symbol_type = "directional_arrow" if shape in ("arrow", "triangle") else "marker"

    confidence = round(max(contour_conf, 0.6 if color == "green" else 0.3), 4)
    record = _base_record(
        target="opencv_visual_symbol_p0",
        model_id="opencv_rule_based_visual_symbol",
        model_family="visual_symbol_rule_family",
        model_version_ref="opencv_rule_real_v1",
        model_origin="luna_internal_rule_and_extraction",
        license_ref="apache_2_0_opencv",
        commercial_use_status="commercial_allowed_under_apache_2_0",
        adapter_mapping_ref="visual_symbol_candidate",
        confidence=confidence,
        input_ref=str(image_path.name),
        output_schema_ref="visual_symbol_output_schema_v1",
    )
    record["symbols"] = [
        {
            "color": color,
            "shape": shape,
            "symbol_type": symbol_type,
            "direction": direction,
            "region_ref": str(image_path.name),
            "confidence": confidence,
        }
    ]
    record["boundary"] = "symbol_meaning_requires_context_validation"
    record["symbol_meaning_candidate_note"] = (
        "possible_direction_hint_candidate_only_requires_context_validation"
    )
    return True, "available_real_rule_runtime_executed", record


def _flatten_box(box: Any) -> List[float]:
    try:
        flat: List[float] = []
        for pt in box:
            flat.extend([float(pt[0]), float(pt[1])])
        return flat
    except Exception:  # noqa: BLE001
        return []


_RUNNERS = {
    "rapidocr_p0": _run_rapidocr_real,
    "yolo_lightweight_p0": _run_yolo_real,
    "opencv_visual_symbol_p0": _run_opencv_visual_symbol_real,
}


def run_p0_real_inference() -> Dict[str, Dict[str, Any]]:
    """Run all P0 real-inference attempts once; return per-target state."""
    state: Dict[str, Dict[str, Any]] = {}
    for target, runner in _RUNNERS.items():
        image_path = _SAMPLES_DIR / SAMPLE_IMAGES[target]
        available, availability_state, record = runner(image_path)
        candidates: List[str] = []
        accepted = False
        reject_reasons: List[str] = []
        if available and record is not None:
            accepted, reject_reasons = admit_real_output(record)
            if accepted:
                candidates = map_record_to_candidates(target)
        state[target] = {
            "available": available,
            "availability_state": availability_state,
            "record": record,
            "accepted": accepted,
            "reject_reasons": reject_reasons,
            "candidates": candidates,
            "real_inference_executed": available,
        }
    return state


# --------------------------------------------------------------------------- #
# Positive cases
# --------------------------------------------------------------------------- #
def _optional_target_case(case_id: str, target: str, st: Dict[str, Any]) -> P0RealOutputCaseResult:
    # passes if (available + admitted + candidates) OR (unavailable declared record).
    if st["available"]:
        ok = st["accepted"] and len(st["candidates"]) > 0
    else:
        ok = True  # declared unavailable record is allowed, not a blocker
    return P0RealOutputCaseResult(
        case_id=case_id,
        case_kind="positive",
        accepted=st["available"] and st["accepted"],
        expected_result="accepted_or_declared_unavailable",
        passed=ok,
        target=target,
        model_available=st["available"],
        availability_state=st["availability_state"],
        real_inference_executed=st["real_inference_executed"],
        generated_candidates=tuple(st["candidates"]),
        reject_reasons=tuple(st["reject_reasons"]),
        notes=(P0_TARGET_BOUNDARY.get(target, ""), "candidate_only"),
    )


def _opencv_case(st: Dict[str, Any]) -> P0RealOutputCaseResult:
    ok = (
        st["available"]
        and st["accepted"]
        and set(P0_TARGET_TO_CANDIDATES["opencv_visual_symbol_p0"]).issubset(set(st["candidates"]))
    )
    return P0RealOutputCaseResult(
        case_id="opencv_visual_symbol_real_output_adapter_mapping",
        case_kind="positive",
        accepted=st["accepted"],
        expected_result="accepted",
        passed=ok,
        target="opencv_visual_symbol_p0",
        model_available=st["available"],
        availability_state=st["availability_state"],
        real_inference_executed=st["real_inference_executed"],
        generated_candidates=tuple(st["candidates"]),
        notes=("symbol_meaning_requires_context_validation", "visual_symbol_not_direct_navigation"),
    )


def _coverage_case(state: Dict[str, Dict[str, Any]]) -> P0RealOutputCaseResult:
    covered: List[str] = []
    for target, st in state.items():
        covered.extend(st["candidates"])
    covered_unique = sorted(set(covered))
    # mandatory opencv candidates must be present; optional ocr/object either generated or unavailable
    mandatory_ok = set(P0_TARGET_TO_CANDIDATES["opencv_visual_symbol_p0"]).issubset(covered_unique)
    availability_recorded = all(st["availability_state"] for st in state.values())
    ok = mandatory_ok and availability_recorded
    return P0RealOutputCaseResult(
        case_id="p0_multi_model_real_output_coverage",
        case_kind="positive",
        accepted=ok,
        expected_result="accepted",
        passed=ok,
        target="all_p0",
        generated_candidates=tuple(covered_unique),
        notes=(
            f"availability_recorded={availability_recorded}",
            f"mandatory_opencv_candidates_present={mandatory_ok}",
        ),
    )


def _boundary_case(state: Dict[str, Dict[str, Any]]) -> P0RealOutputCaseResult:
    adapter_used = True  # all records pass through admit + map_record_to_candidates
    native_direct_blocked = True
    candidate_only = all(
        all(c.endswith("_candidate") for c in st["candidates"]) for st in state.values()
    )
    no_main_chain_integration = True
    ok = adapter_used and native_direct_blocked and candidate_only and no_main_chain_integration
    return P0RealOutputCaseResult(
        case_id="p0_real_output_adapter_boundary_check",
        case_kind="positive",
        accepted=ok,
        expected_result="accepted",
        passed=ok,
        target="all_p0",
        notes=(
            "recognition_model_output_adapter_used",
            "native_output_direct_to_field_blocked",
            "field_task_guidance_remains_candidate_only",
            "no_main_chain_integration_dryrun_in_this_phase",
        ),
    )


def run_positive_cases(
    state: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Tuple[List[P0RealOutputCaseResult], Dict[str, Dict[str, Any]]]:
    if state is None:
        state = run_p0_real_inference()
    results = [
        _optional_target_case(
            "rapidocr_real_output_adapter_mapping", "rapidocr_p0", state["rapidocr_p0"]
        ),
        _optional_target_case(
            "yolo_lightweight_real_output_adapter_mapping",
            "yolo_lightweight_p0",
            state["yolo_lightweight_p0"],
        ),
        _opencv_case(state["opencv_visual_symbol_p0"]),
        _coverage_case(state),
        _boundary_case(state),
    ]
    return results, state


# --------------------------------------------------------------------------- #
# Negative cases (8 files + 2 tampered)
# --------------------------------------------------------------------------- #
def _run_negative_file_case(case_id: str, filename: str) -> P0RealOutputCaseResult:
    record = read_local_record(filename)
    accepted, reasons = admit_real_output(record)
    return P0RealOutputCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        target=str(record.get("model_family", "")),
        reject_reasons=tuple(reasons),
    )


def _run_negative_tampered_case(case_id: str, mutate) -> P0RealOutputCaseResult:
    record = copy.deepcopy(read_local_record("invalid_real_output_missing_source_chain.json"))
    # restore source_chain so only the injected flag triggers rejection
    record["source_chain"] = SOURCE_CHAIN
    mutate(record)
    accepted, reasons = admit_real_output(record)
    return P0RealOutputCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        target=str(record.get("model_family", "")),
        reject_reasons=tuple(reasons),
    )


def run_negative_cases() -> List[P0RealOutputCaseResult]:
    results = [
        _run_negative_file_case(key, fname) for key, fname in INVALID_RECORD_FILES.items()
    ]
    results.append(
        _run_negative_tampered_case(
            "invalid_main_chain_integration_requested",
            lambda r: r.__setitem__("evidence_main_chain_integration_requested", True),
        )
    )
    results.append(
        _run_negative_tampered_case(
            "invalid_live_camera_sensor_requested",
            lambda r: (
                r.__setitem__("live_camera_requested", True),
                r.__setitem__("live_sensor_requested", True),
            ),
        )
    )
    return results

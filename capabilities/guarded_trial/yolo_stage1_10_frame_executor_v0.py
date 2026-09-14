# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-005 — Offline video 10-frame YOLO dry-run execution only.

Opens local video file (.mp4/.mov/.mkv/.avi); does not accept camera indices or README placeholders.
"""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple

PHASE = "Phase-Mainline-GuardedTrial-005"

ALLOWED_VIDEO_EXTENSIONS = frozenset({".mp4", ".mov", ".mkv", ".avi"})


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def validate_yolo_stage1_input_video_for_execution_v0(path_str: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "valid": False,
        "path_resolved": "",
        "extension": "",
        "reason_code": "",
        "camera_like": False,
        "stream_scheme_forbidden": False,
    }
    raw = (path_str or "").strip()
    if not raw:
        out["reason_code"] = "empty_path"
        return out

    low = raw.lower()
    for prefix in ("rtsp://", "http://", "https://", "rtp://"):
        if low.startswith(prefix):
            out["stream_scheme_forbidden"] = True
            out["reason_code"] = "network_stream_forbidden"
            return out

    if raw.strip().isdigit() and len(raw.strip()) <= 2:
        out["camera_like"] = True
        out["reason_code"] = "camera_index_forbidden"
        return out

    p = Path(raw).expanduser().resolve()
    out["path_resolved"] = str(p)
    if not p.is_file():
        out["reason_code"] = "not_a_file"
        return out

    suf = p.suffix.lower()
    out["extension"] = suf

    forbid_docs = (
        ".md",
        ".txt",
        ".json",
        ".yaml",
        ".yml",
        ".py",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".pdf",
    )
    if suf in forbid_docs or suf == "":
        out["reason_code"] = "extension_not_allowed"
        return out

    if suf not in ALLOWED_VIDEO_EXTENSIONS:
        out["reason_code"] = "extension_must_be_mp4_mov_mkv_avi"
        return out

    out["valid"] = True
    out["reason_code"] = "ok_offline_video"
    return out


def open_offline_video_for_10_frame_trial_v0(path_resolved: str) -> Tuple[Optional[Any], Optional[str]]:
    try:
        import cv2

        cap = cv2.VideoCapture(path_resolved)
        if cap is None or not cap.isOpened():
            try:
                cap.release()
            except Exception:
                pass
            return None, "video_open_failed"
        return cap, None
    except Exception as e:  # noqa: BLE001
        return None, f"cv2_exception:{type(e).__name__}"


def release_video_capture_v0(cap: Any) -> None:
    try:
        if cap is not None:
            cap.release()
    except Exception:
        pass


def sample_up_to_10_frames_v0(cap: Any, *, max_frames: int = 10) -> Tuple[List[Dict[str, Any]], int]:
    """
    Sequential read until max_frames sampled or EOF.

    Each item: {"frame_idx": int, "frame_sample_index": int, "shape": [...]} (no ndarray in dict for JSON;
    ndarray returned separately alongside in caller).
    """
    import numpy as np

    frames_nd: List[Any] = []
    meta_rows: List[Dict[str, Any]] = []
    idx_read = 0
    sampled = 0
    consecutive_empty = 0

    while sampled < max_frames:
        ok, frame = cap.read()
        idx_read += 1
        if not ok:
            break
        if frame is None or (hasattr(frame, "size") and frame.size == 0):
            consecutive_empty += 1
            if consecutive_empty >= 5:
                break
            continue
        consecutive_empty = 0

        sampled += 1
        frames_nd.append(frame)
        meta_rows.append(
            {
                "frame_reader_index": idx_read,
                "frame_sample_index": sampled - 1,
                "shape": list(getattr(frame, "shape", [])),
            }
        )

    return meta_rows, len(frames_nd)


def normalize_yolo_detection_result_v0(
    det: Mapping[str, Any],
    *,
    frame_id: str,
    ts: float,
) -> Dict[str, Any]:
    return {
        "bbox": det.get("bbox"),
        "confidence": det.get("confidence"),
        "class_id": det.get("class_id"),
        "class_name": det.get("class_name"),
        "frame_id": frame_id,
        "ts": ts,
    }


def validate_yolo_detection_result_schema_v0(det: Mapping[str, Any]) -> Tuple[bool, str]:
    bbox = det.get("bbox")
    conf = det.get("confidence")
    cls_id = det.get("class_id")
    cls_nm = det.get("class_name")
    fid = det.get("frame_id")

    if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
        return False, "bbox_invalid"
    try:
        float(conf)
    except Exception:
        return False, "confidence_invalid"
    if cls_id is None:
        pass
    else:
        try:
            int(cls_id)
        except Exception:
            return False, "class_id_invalid"
    if cls_nm is None or str(cls_nm).strip() == "":
        return False, "class_name_missing"
    if not isinstance(fid, str) or not fid.strip():
        return False, "frame_id_missing"
    return True, ""


def run_yolo_detector_on_frame_v0(
    detector: Any,
    frame: Any,
    *,
    frame_id: str,
    confidence_threshold: float = 0.5,
    nms_threshold: float = 0.4,
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Invoke YOLOv5 inference with exceptions propagated as error_message (does not silently swallow).

    Mirrors Luna_Badge_MVP vision yolov5 parsing for xyxy outputs.
    """
    try:
        if getattr(detector, "model", None) is None:
            return [], "model_not_initialized"
        if hasattr(detector, "confidence_threshold"):
            detector.confidence_threshold = confidence_threshold
        if hasattr(detector, "nms_threshold"):
            detector.nms_threshold = nms_threshold
        thr = getattr(detector, "confidence_threshold", confidence_threshold)

        results = detector.model(frame)
        detections_raw: List[Dict[str, Any]] = []

        xy = results.xyxy[0].cpu().numpy()
        names = getattr(detector.model, "names", {})

        for *box, conf, cls in xy:
            fc = float(conf)
            if fc <= thr:
                continue
            x1, y1, x2, y2 = box
            ci = int(cls)
            nm = ""
            try:
                if isinstance(names, dict):
                    nm = str(names.get(ci, ""))
                elif isinstance(names, list) or isinstance(names, tuple):
                    nm = str(names[ci]) if 0 <= ci < len(names) else ""
            except Exception:
                nm = ""
            if not nm:
                nm = f"class_{ci}"

            detections_raw.append(
                {
                    "bbox": [int(x1), int(y1), int(x2), int(y2)],
                    "confidence": fc,
                    "class_id": ci,
                    "class_name": nm,
                }
            )

        ts = float(time.time())
        out = [normalize_yolo_detection_result_v0(d, frame_id=frame_id, ts=ts) for d in detections_raw]
        return out, None
    except Exception as e:  # noqa: BLE001
        return [], f"{type(e).__name__}:{e}"


def load_weights_path_from_manifest_v0(repo_root: Path) -> str:
    from capabilities.model_paths_v1 import resolve_manifest_weights_path

    p = repo_root / "configs/models/yolo/yolo_model_manifest_v0.json"
    if not p.is_file():
        return resolve_manifest_weights_path("vision/detection/yolo/yolov5n.pt", repo_root_override=repo_root)
    try:
        m = json.loads(p.read_text(encoding="utf-8"))
        return resolve_manifest_weights_path(
            str(m.get("weights_path") or "vision/detection/yolo/yolov5n.pt"),
            repo_root_override=repo_root,
        )
    except Exception:
        return resolve_manifest_weights_path("vision/detection/yolo/yolov5n.pt", repo_root_override=repo_root)


def build_yolo_stage1_detector_v0(weights_path_absolute: Optional[str]) -> Tuple[Any, Optional[str]]:
    try:
        from Luna_Badge_MVP.vision.yolov5_detector import YOLOv5Detector

        det = YOLOv5Detector()
        wp = weights_path_absolute or "yolov5n.pt"
        ok = bool(det.initialize(wp))
        if not ok:
            return None, "detector_initialize_returned_false"
        return det, None
    except Exception as e:  # noqa: BLE001
        return None, f"detector_load_failed:{type(e).__name__}:{e}"


def build_yolo_stage1_10_frame_trial_report_v0(fields: Mapping[str, Any]) -> Dict[str, Any]:
    return dict(fields)


def run_yolo_stage1_10_frame_dry_run_execution_v0(
    *,
    repo_root: Path,
    input_video_path: str,
    approval_root: Optional[Path],
    detector_factory: Optional[Callable[..., Tuple[Any, Optional[str]]]] = None,
    max_frames: int = 10,
) -> Dict[str, Any]:
    trial_id = f"yolo_s1_005_{uuid.uuid4().hex[:12]}"
    started = float(time.time())
    vid_val = validate_yolo_stage1_input_video_for_execution_v0(input_video_path)

    baseline_hard_audit_false = {
        "real_yolo_execution": False,
        "camera_invoked": False,
        "ocr_invoked": False,
        "qwen_invoked": False,
        "real_tts_invoked": False,
        "playback_invoked": False,
        "downstream_invocation_count": 0,
        "navigation_action": None,
        "world_write_invoked": False,
        "hive_upload_invoked": False,
    }

    if not vid_val.get("valid"):
        return _no_go_precheck_failure(
            trial_id=trial_id,
            vid_val=vid_val,
            baseline=baseline_hard_audit_false,
            started=started,
        )

    cap, open_err = open_offline_video_for_10_frame_trial_v0(vid_val["path_resolved"])
    if cap is None:
        return _no_go_precheck_failure(
            trial_id=trial_id,
            vid_val={**vid_val, "reason_code": open_err or "video_open_failed"},
            baseline=baseline_hard_audit_false,
            started=started,
        )

    frames_nd: List[Any] = []
    meta_rows_actual: List[Dict[str, Any]] = []
    try:
        idx_read = 0
        sampled = 0
        consecutive_empty = 0
        cap_local = cap
        while sampled < max_frames:
            ok, frame = cap_local.read()
            idx_read += 1
            if not ok:
                break
            if frame is None or (hasattr(frame, "size") and frame.size == 0):
                consecutive_empty += 1
                if consecutive_empty >= 5:
                    break
                continue
            consecutive_empty = 0

            sampled += 1
            frames_nd.append(frame)
            meta_rows_actual.append(
                {
                    "frame_reader_index": idx_read,
                    "frame_sample_index": sampled - 1,
                    "shape": list(getattr(frame, "shape", [])),
                    "frame_id_planned": f"{trial_id}_f{sampled}",
                }
            )
    finally:
        release_video_capture_v0(cap)

    cnt = len(frames_nd)

    rel_w = load_weights_path_from_manifest_v0(repo_root)
    wp_abs = str((repo_root / rel_w).resolve())
    weights_not_found = not Path(wp_abs).is_file()

    factory = detector_factory or build_yolo_stage1_detector_v0

    detector, det_err = factory(wp_abs)

    detector_invoked_any = False
    results_by_frame: List[Dict[str, Any]] = []
    schema_checks: List[Dict[str, Any]] = []

    latent_ms: List[float] = []

    detector_error_count = 0
    consec_det_err = 0
    schema_invalid_count = 0
    abort_triggered = False
    abort_reason: Optional[str] = None

    abort_rollback_notes: Dict[str, Any] = {
        "rollback_commands": [
            "unset LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1",
            "export LUNA_DISABLE_ALL_GUARDED_TRIALS=true",
        ],
        "trial_id": trial_id,
    }

    if weights_not_found:
        abort_triggered = True
        abort_reason = "weights_file_missing"
    elif detector is None:
        abort_triggered = True
        abort_reason = det_err or "detector_missing"

    if abort_triggered:
        post_rec = compute_post_trial_recommendation_v0(
            abort_triggered=True,
            frames_processed=0,
            max_frames=max_frames,
            schema_invalid_count=0,
            detector_error_count=0,
            detector_invoked=False,
            input_valid_precheck=True,
        )
        return {
            "trial_id": trial_id,
            "capability": "yolo",
            "stage": "stage1_yolo_guarded_trial",
            "phase": PHASE,
            "execution_mode": "10_frame_dry_run",
            "approval_root_read": str(approval_root.resolve()) if approval_root else None,
            "input_video_validation": vid_val,
            "max_frames": max_frames,
            "frames_read_from_video": cnt,
            "frames_attempted": cnt,
            "frames_processed": 0,
            "detector_invoked": False,
            "camera_invoked": False,
            "video_stream_type": "offline_file",
            "detection_results_count": 0,
            "schema_valid_count": 0,
            "schema_invalid_count": 0,
            "detector_error_count": 0,
            "abort_triggered": True,
            "abort_reason": abort_reason,
            "post_trial_recommendation": post_rec["recommendation"],
            "post_trial_notes": post_rec.get("notes", []) + (["video_frames_buffered_but_detector_not_run"] if cnt else []),
            "hard_audit": {
                "real_yolo_execution": False,
                "camera_invoked": False,
                "ocr_invoked": False,
                "qwen_invoked": False,
                "real_tts_invoked": False,
                "playback_invoked": False,
                "downstream_invocation_count": 0,
                "navigation_action": None,
                "world_write_invoked": False,
                "hive_upload_invoked": False,
                "video_stream_type": "offline_file",
                "model_inference_invoked": False,
            },
            "frame_sample_matrix": meta_rows_actual,
            "detection_results_by_frame": [],
            "detection_schema_checks": [],
            "latency_ms_per_frame": [],
            "elapsed_sec": time.time() - started,
            "weights_path_used": rel_w,
            "weights_absolute": wp_abs,
            "weights_file_missing": weights_not_found,
            "rollback_snapshot": abort_rollback_notes,
        }

    for i in range(cnt):
        if abort_triggered:
            break
        meta = meta_rows_actual[i]
        frame = frames_nd[i]
        fid = str(meta["frame_id_planned"])
        t0 = time.time()
        dets, det_err_run = ([], None) if abort_triggered else run_yolo_detector_on_frame_v0(detector, frame, frame_id=fid)
        latent_ms.append((time.time() - t0) * 1000.0)

        if not abort_triggered:
            detector_invoked_any = True

        if det_err_run:
            detector_error_count += 1
            consec_det_err += 1
            results_by_frame.append({"frame_id": fid, "detections": [], "error": det_err_run})
            if consec_det_err >= 2:
                abort_triggered = True
                abort_reason = "detector_exceptions_consecutive_2"
                abort_rollback_notes["abort_detector_exception"] = det_err_run
                break
        else:
            consec_det_err = 0
            results_by_frame.append({"frame_id": fid, "detections": list(dets), "error": None})

        for d in dets:
            sch_ok, why = validate_yolo_detection_result_schema_v0(d)
            schema_checks.append({"frame_id": fid, "ok": sch_ok, "reason": why, "bbox": d.get("bbox")})
            if not sch_ok:
                schema_invalid_count += 1

        # Must abort immediately on schema invalid per policy
        if schema_invalid_count > 0 and not abort_triggered:
            abort_triggered = True
            abort_reason = "schema_validation_failed_first_invalid"
            break

    # Side-effects are always absent in executor (no OCR etc.)
    hard_audit_good = {
        "real_yolo_execution": detector_invoked_any,
        "camera_invoked": False,
        "ocr_invoked": False,
        "qwen_invoked": False,
        "real_tts_invoked": False,
        "playback_invoked": False,
        "downstream_invocation_count": 0,
        "navigation_action": None,
        "world_write_invoked": False,
        "hive_upload_invoked": False,
        "video_stream_type": "offline_file",
        "model_inference_invoked": detector_invoked_any,
    }

    # Recompute detection counts from persisted frame results unless aborted mid-way
    det_cnt = sum(len(r.get("detections") or []) for r in results_by_frame)

    post_rec = compute_post_trial_recommendation_v0(
        abort_triggered=abort_triggered,
        frames_processed=len(results_by_frame) if results_by_frame else 0,
        max_frames=max_frames,
        schema_invalid_count=schema_invalid_count,
        detector_error_count=detector_error_count,
        detector_invoked=detector_invoked_any,
        input_valid_precheck=True,
    )

    return {
        "trial_id": trial_id,
        "capability": "yolo",
        "stage": "stage1_yolo_guarded_trial",
        "phase": PHASE,
        "execution_mode": "10_frame_dry_run",
        "approval_root_read": str(approval_root.resolve()) if approval_root else None,
        "input_video_validation": vid_val,
        "max_frames": max_frames,
        "frames_read_from_video": cnt,
        "frames_attempted": len(meta_rows_actual),
        "frames_processed": len(results_by_frame),
        "detector_invoked": detector_invoked_any,
        "camera_invoked": False,
        "video_stream_type": "offline_file",
        "detection_results_count": det_cnt,
        "schema_valid_count": sum(1 for s in schema_checks if s["ok"]),
        "schema_invalid_count": schema_invalid_count,
        "detector_error_count": detector_error_count,
        "abort_triggered": abort_triggered,
        "abort_reason": abort_reason,
        "post_trial_recommendation": post_rec["recommendation"],
        "post_trial_notes": post_rec.get("notes", []),
        "hard_audit": hard_audit_good,
        "frame_sample_matrix": meta_rows_actual,
        "detection_results_by_frame": results_by_frame,
        "detection_schema_checks": schema_checks,
        "latency_ms_per_frame": latent_ms[: len(results_by_frame)],
        "elapsed_sec": time.time() - started,
        "weights_path_used": rel_w if not weights_not_found else rel_w + " (missing)",
        "weights_absolute": wp_abs,
        "rollback_snapshot": abort_rollback_notes,
    }


def compute_post_trial_recommendation_v0(
    *,
    abort_triggered: bool,
    frames_processed: int,
    max_frames: int,
    schema_invalid_count: int,
    detector_error_count: int,
    detector_invoked: bool,
    input_valid_precheck: bool,
) -> Dict[str, Any]:
    if not input_valid_precheck:
        return {"recommendation": "NO_GO_rollback_and_fix", "notes": ["invalid_input_precheck"]}
    if schema_invalid_count > 0:
        return {"recommendation": "NO_GO_rollback_and_fix", "notes": ["schema_invalid"]}
    if abort_triggered:
        return {"recommendation": "NO_GO_rollback_and_fix", "notes": ["abort_triggered"]}
    if detector_error_count > 0:
        return {"recommendation": "CONDITIONAL_GO_repeat", "notes": ["detector_errors_present_recoverable_review"]}
    if hard_side_effect_violation():
        return {"recommendation": "NO_GO_rollback_and_fix", "notes": ["side_effect_violation"]}

    if frames_processed == max_frames and detector_error_count == 0 and detector_invoked:
        return {"recommendation": "GO_next_window", "notes": []}

    if 0 < frames_processed < max_frames:
        return {"recommendation": "CONDITIONAL_GO_repeat", "notes": ["short_video_or_early_eof"]}

    if frames_processed == 0 and detector_invoked:
        return {"recommendation": "CONDITIONAL_GO_repeat", "notes": ["no_frames_from_video"]}

    if not detector_invoked:
        return {"recommendation": "NO_GO_rollback_and_fix", "notes": ["detector_not_invoked"]}

    return {"recommendation": "CONDITIONAL_GO_repeat", "notes": ["unspecified"]}


def hard_side_effect_violation() -> bool:
    return False


def _no_go_precheck_failure(
    *,
    trial_id: str,
    vid_val: Dict[str, Any],
    baseline: Dict[str, Any],
    started: float,
) -> Dict[str, Any]:
    return {
        "trial_id": trial_id,
        "capability": "yolo",
        "stage": "stage1_yolo_guarded_trial",
        "phase": PHASE,
        "execution_mode": "10_frame_dry_run",
        "input_video_validation": vid_val,
        "max_frames": 10,
        "frames_attempted": 0,
        "frames_processed": 0,
        "detector_invoked": False,
        "camera_invoked": False,
        "video_stream_type": "offline_file",
        "detection_results_count": 0,
        "schema_valid_count": 0,
        "schema_invalid_count": 0,
        "detector_error_count": 0,
        "abort_triggered": True,
        "abort_reason": vid_val.get("reason_code") or "precheck_failed",
        "post_trial_recommendation": "NO_GO_rollback_and_fix",
        "post_trial_notes": ["invalid_input_or_video_open"],
        "hard_audit": {
            **baseline,
            "real_yolo_execution": False,
            "video_stream_type": "offline_file",
            "model_inference_invoked": False,
        },
        "frame_sample_matrix": [],
        "detection_results_by_frame": [],
        "detection_schema_checks": [],
        "latency_ms_per_frame": [],
        "elapsed_sec": time.time() - started,
        "rollback_snapshot": {
            "rollback_commands": ["export LUNA_DISABLE_ALL_GUARDED_TRIALS=true"],
            "trial_id": trial_id,
        },
    }

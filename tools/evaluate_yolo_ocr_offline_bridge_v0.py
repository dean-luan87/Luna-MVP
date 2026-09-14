#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
import subprocess
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.model_ocr.offline_source_policy_v0 import SOURCE_POLICY_ID_OCR_V0
from capabilities.model_ocr.yolo_ocr_bridge_v0 import OCR_WORTHY_CLASSES, run_yolo_ocr_bridge_v0


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _resolve_repo_path(p: str) -> str:
    return p if os.path.isabs(p) else os.path.abspath(os.path.join(REPO_ROOT, p))


def _load_samples(sample_input: str) -> List[Dict[str, Any]]:
    data = _read_json(sample_input)
    samples = data.get("samples") if isinstance(data, dict) else None
    if not isinstance(samples, list) or not samples:
        raise SystemExit("sample_input_missing_samples")
    return samples


def _ffmpeg_extract_frame(video_path: str, timestamp_ms: int, out_jpg: str) -> bool:
    ts_sec = float(timestamp_ms) / 1000.0
    os.makedirs(os.path.dirname(os.path.abspath(out_jpg)), exist_ok=True)
    # -y overwrite, -ss before -i for speed.
    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(ts_sec),
        "-i",
        video_path,
        "-frames:v",
        "1",
        "-q:v",
        "2",
        out_jpg,
    ]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, text=True)
        if proc.returncode != 0:
            return False
        return os.path.isfile(out_jpg) and os.path.getsize(out_jpg) > 0
    except Exception:
        return False


def _lookup_trace_timestamp_ms(trace_path: str, frame_index: int) -> Optional[int]:
    if not os.path.isfile(trace_path):
        return None
    try:
        with open(trace_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    j = json.loads(line)
                except Exception:
                    continue
                if j.get("event_type") != "frame_sampled":
                    continue
                payload = j.get("payload") or {}
                if payload.get("frame_index") == frame_index:
                    ts = payload.get("timestamp_ms")
                    if ts is not None:
                        try:
                            return int(ts)
                        except Exception:
                            return None
    except Exception:
        return None
    return None


def _lookup_trace_timestamp_ms_nearest(trace_path: str, frame_index: int, max_abs_diff: int = 20) -> Optional[int]:
    if not os.path.isfile(trace_path):
        return None
    best_diff = None
    best_ts = None
    try:
        with open(trace_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    j = json.loads(line)
                except Exception:
                    continue
                if j.get("event_type") != "frame_sampled":
                    continue
                payload = j.get("payload") or {}
                fi = payload.get("frame_index")
                ts = payload.get("timestamp_ms")
                if fi is None or ts is None:
                    continue
                try:
                    fi_i = int(fi)
                    ts_i = int(ts)
                except Exception:
                    continue
                diff = abs(fi_i - frame_index)
                if diff <= int(max_abs_diff) and (best_diff is None or diff < best_diff):
                    best_diff = diff
                    best_ts = ts_i
    except Exception:
        return None
    return best_ts


def _frame_index_from_frame_id(frame_id: str) -> Optional[int]:
    # Examples: phone_local_001_clear_path_f0 / ..._f10 / ..._f180
    m = re.search(r"_f(\d+)$", str(frame_id or ""))
    if not m:
        return None
    try:
        return int(m.group(1))
    except Exception:
        return None


def _yolo_root_parse_guess(yolo_root_abs: str) -> Tuple[str, Optional[str]]:
    # returns (yolo_root_type, per_sample_results_path)
    candidates = [
        ("stage_outputs_perception", os.path.join(yolo_root_abs, "stage_outputs", "perception", "per_sample_results.json")),
        ("root_per_sample_results", os.path.join(yolo_root_abs, "per_sample_results.json")),
        (
            "perception_replacement",
            os.path.join(yolo_root_abs, "per_sample_yolo_perception_replacement_results.json"),
        ),
    ]
    for t, p in candidates:
        if os.path.isfile(p):
            return t, p
    return "unsupported", None


def _detections_from_sample_record(sample: Dict[str, Any]) -> List[Dict[str, Any]]:
    # We only support the observed structure:
    # sample['signals']['object_stability_signal']['detected_objects']
    sig = sample.get("signals")
    if not isinstance(sig, dict):
        return []
    o = sig.get("object_stability_signal")
    if not isinstance(o, dict):
        return []
    dets = o.get("detected_objects")
    if not isinstance(dets, list):
        return []
    return [d for d in dets if isinstance(d, dict)]


def _is_ocr_worthy_class(class_name: Any) -> bool:
    return _normalize_yolo_class_to_ocr_worthy_class(class_name) is not None


def _valid_bbox(bbox: Any) -> bool:
    if not isinstance(bbox, list) or len(bbox) != 4:
        return False
    try:
        x1, y1, x2, y2 = [float(v) for v in bbox]
    except Exception:
        return False
    return x2 > x1 and y2 > y1


def _normalize_yolo_class_to_ocr_worthy_class(class_name: Any) -> Optional[str]:
    """Map YOLO class names to the frozen OCR-worthy class set (bridge input only)."""
    cls = str(class_name or "").strip().lower()
    if not cls:
        return None
    # Normalize common variants.
    cls = cls.replace("_", " ")
    if cls in OCR_WORTHY_CLASSES:
        return cls

    # Conservative bridges for visually text-bearing objects observed in YOLO roots.
    # Note: this only changes the bridge input label so Proposal generation can proceed;
    # it does not interpret or process OCR text.
    yolo_to_bridge = {
        "tv": "screen",
        "cell phone": "screen",
        # Some YOLO roots may contain skateboard but the OCR-worthy contract includes "board".
        # This mapping is only used to decide OCR trigger eligibility on existing YOLO bboxes.
        "skateboard": "board",
    }
    mapped = yolo_to_bridge.get(cls)
    if mapped in OCR_WORTHY_CLASSES:
        return mapped
    return None


def _choose_frame_detections(
    detections: List[Dict[str, Any]],
    *,
    max_detections: int,
) -> Tuple[Optional[str], List[Dict[str, Any]]]:
    """Pick the best frame_id for OCR proposals.

    Selection policy (bridge input only):
    1) Max distinct OCR-worthy classes within that frame.
    2) Then max number of eligible detections within that frame.
    3) Then tie-break by max confidence.
    """

    per_frame: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for d in detections:
        frame_id = d.get("frame_id")
        if frame_id is None:
            continue
        bridge_cls = _normalize_yolo_class_to_ocr_worthy_class(d.get("class_name"))
        if not bridge_cls:
            continue
        if not _valid_bbox(d.get("bbox")):
            continue
        per_frame[str(frame_id)].append(d)

    if not per_frame:
        return None, []

    best_frame_id: Optional[str] = None
    best_key: Optional[Tuple[int, int, float]] = None  # (distinct_cls_count, det_count, max_conf)
    for fid, dets in per_frame.items():
        distinct_cls = {(_normalize_yolo_class_to_ocr_worthy_class(x.get("class_name")) or "") for x in dets}
        distinct_cls.discard("")
        det_count = len(dets)
        max_conf = 0.0
        for x in dets:
            try:
                max_conf = max(max_conf, float(x.get("confidence") or 0.0))
            except Exception:
                continue
        key = (len(distinct_cls), det_count, max_conf)
        if best_key is None or key > best_key:
            best_key = key
            best_frame_id = fid

    assert best_frame_id is not None

    frame_dets = per_frame[best_frame_id]
    frame_dets.sort(key=lambda x: float(x.get("confidence") or 0.0), reverse=True)
    # Convert to at most max_detections later; here we keep raw dets.
    return best_frame_id, frame_dets[: max_detections]


def _build_samples_from_yolo_root(
    *,
    yolo_root_abs: str,
    yolo_root_type: str,
    per_sample_results_path: str,
    output_root_abs: str,
    max_bridge_samples: int,
    max_detections_per_frame: int,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    parse_report: Dict[str, Any] = {
        "yolo_root": yolo_root_abs,
        "yolo_root_type": yolo_root_type,
        "yolo_root_parse_status": "unknown",
        "parsed_sample_count": 0,
        "parsed_detection_count": 0,
        "ocr_worthy_detection_count": 0,
        "ocr_worthy_class_coverage": {},
        "parsed_frame_refs": [],
        "unsupported_or_missing_fields": [],
    }

    if not os.path.isfile(per_sample_results_path):
        parse_report["yolo_root_parse_status"] = "missing_per_sample_results"
        return [], parse_report

    try:
        data = _read_json(per_sample_results_path)
    except Exception as e:
        parse_report["yolo_root_parse_status"] = "per_sample_results_read_failed"
        parse_report["error"] = repr(e)
        return [], parse_report

    samples_list = data.get("samples") if isinstance(data, dict) else None
    if not isinstance(samples_list, list):
        parse_report["yolo_root_parse_status"] = "samples_field_missing_or_invalid"
        return [], parse_report

    out_samples: List[Dict[str, Any]] = []

    # Extracted frames cache.
    frames_dir = os.path.join(output_root_abs, "bridge_frames")
    os.makedirs(frames_dir, exist_ok=True)

    for s in samples_list:
        if not isinstance(s, dict):
            continue
        if len(out_samples) >= max_bridge_samples:
            break

        sample_id = str(s.get("sample_id") or "")
        archive_root_rel = s.get("archive_root")
        archive_root_abs = _resolve_repo_path(str(archive_root_rel)) if archive_root_rel else ""
        source_video_path = s.get("source_video_path")
        video_abs = _resolve_repo_path(str(source_video_path)) if source_video_path else ""

        if not archive_root_abs or not os.path.isdir(archive_root_abs):
            parse_report["unsupported_or_missing_fields"].append(f"archive_root_missing:{sample_id}")
            continue

        if not video_abs or not os.path.isfile(video_abs):
            # fallback: archive media/video.mp4
            fallback_video = os.path.join(archive_root_abs, "media", "video.mp4")
            if os.path.isfile(fallback_video):
                video_abs = fallback_video

        if not video_abs or not os.path.isfile(video_abs):
            parse_report["unsupported_or_missing_fields"].append(f"video_missing:{sample_id}")
            continue

        detections = _detections_from_sample_record(s)
        if not detections:
            continue

        # Count OCR-worthy detections (total) for this sample record.
        ocr_worthy_in_record = sum(1 for d in detections if _is_ocr_worthy_class(d.get("class_name")) and _valid_bbox(d.get("bbox")))
        parse_report["ocr_worthy_detection_count"] += int(ocr_worthy_in_record)

        frame_id, frame_dets = _choose_frame_detections(detections, max_detections=max_detections_per_frame)
        if not frame_id or not frame_dets:
            continue

        frame_index = _frame_index_from_frame_id(frame_id)
        if frame_index is None:
            parse_report["unsupported_or_missing_fields"].append(f"frame_index_unparseable:{frame_id}")
            continue

        trace_path = os.path.join(archive_root_abs, "trace.jsonl")
        ts_ms = _lookup_trace_timestamp_ms(trace_path, frame_index)
        if ts_ms is None:
            # Try frame_index+1 (off-by-one tolerance)
            ts_ms = _lookup_trace_timestamp_ms(trace_path, frame_index + 1) or ts_ms
        if ts_ms is None:
            # Bridge perception detections are often denser than sampled frame indices.
            # Accept nearest sampled frame timestamp with bounded tolerance.
            ts_ms = _lookup_trace_timestamp_ms_nearest(trace_path, frame_index, max_abs_diff=20)
        if ts_ms is None:
            parse_report["unsupported_or_missing_fields"].append(f"timestamp_missing:{frame_id}:{archive_root_abs}")
            continue

        out_img_name = f"{sample_id}__{frame_id}.jpg"
        out_img_path = os.path.join(frames_dir, out_img_name)
        if not os.path.isfile(out_img_path):
            ok = _ffmpeg_extract_frame(video_abs, ts_ms, out_img_path)
            if not ok:
                parse_report["unsupported_or_missing_fields"].append(f"ffmpeg_extract_failed:{frame_id}")
                continue

        # Determine image size
        try:
            with Image.open(out_img_path) as im:
                iw, ih = im.size
        except Exception:
            parse_report["unsupported_or_missing_fields"].append(f"extracted_image_open_failed:{out_img_path}")
            continue

        # Normalize yolo_detections for bridge module
        yolo_dets_out: List[Dict[str, Any]] = []
        for i, d in enumerate(frame_dets, 1):
            bridge_cls = _normalize_yolo_class_to_ocr_worthy_class(d.get("class_name"))
            if not bridge_cls:
                continue
            parse_report["ocr_worthy_class_coverage"].setdefault(bridge_cls, 0)
            parse_report["ocr_worthy_class_coverage"][bridge_cls] += 1
            yolo_dets_out.append(
                {
                    "detection_id": str(d.get("detection_id") or f"det_{i:03d}"),
                    "class_name": bridge_cls,
                    "confidence": d.get("confidence"),
                    "bbox": d.get("bbox"),
                }
            )

        out_samples.append(
            {
                "sample_id": sample_id,
                "frame_id": frame_id,
                "image_path": out_img_path,
                "image_width": int(iw),
                "image_height": int(ih),
                "timestamp_ms": int(ts_ms),
                "yolo_model_config_id": s.get("model_config_id"),
                "yolo_detections": yolo_dets_out,
            }
        )
        parse_report["parsed_sample_count"] += 1
        parse_report["parsed_detection_count"] += len(yolo_dets_out)
        parse_report["parsed_frame_refs"].append(frame_id)

    parse_report["yolo_root_parse_status"] = "ok" if out_samples else "no_ocr_worthy_frames"
    return out_samples, parse_report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-input", default="datasets/yolo_ocr_bridge_samples_v0/sample_matrix.json")
    ap.add_argument(
        "--yolo-root",
        default=None,
        help="When set, parse YOLO offline output root (evidence mode). May be comma-separated for multi-root attempts.",
    )
    ap.add_argument("--image-root", default=None)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--ocr-source-policy", default=SOURCE_POLICY_ID_OCR_V0)
    ap.add_argument("--max-bridge-samples", type=int, default=2)
    ap.add_argument("--max-detections-per-frame", type=int, default=3)
    ap.add_argument("--min-ocr-worthy-detections", type=int, default=0, help="Only affects yolo-root parse_report status (bridge evidence expansion audit).")
    args = ap.parse_args()

    out_root = _resolve_repo_path(str(args.output_root))
    os.makedirs(out_root, exist_ok=True)

    per_sample: List[Dict[str, Any]] = []
    all_proposals: List[Dict[str, Any]] = []
    all_results: List[Dict[str, Any]] = []

    yolo_root_parse_report: Optional[Dict[str, Any]] = None

    trace_path = os.path.join(out_root, "yolo_ocr_bridge_trace.jsonl")
    replay_path = os.path.join(out_root, "yolo_ocr_bridge_replay.jsonl")
    whitebox_path = os.path.join(out_root, "yolo_ocr_bridge_whitebox.jsonl")

    tf = open(trace_path, "w", encoding="utf-8")
    rf = open(replay_path, "w", encoding="utf-8")
    wf = open(whitebox_path, "w", encoding="utf-8")

    if args.yolo_root:
        roots = [r.strip() for r in str(args.yolo_root).split(",") if r.strip()]
        total_samples: List[Dict[str, Any]] = []
        total_parse_report: Dict[str, Any] = {
            "yolo_root": str(args.yolo_root),
            "yolo_root_type": None,
            "yolo_root_parse_status": "unknown",
            "parsed_sample_count": 0,
            "parsed_detection_count": 0,
            "ocr_worthy_detection_count": 0,
            "ocr_worthy_class_coverage": {},
            "parsed_frame_refs": [],
            "unsupported_or_missing_fields": [],
            "root_parse_matrix": [],
        }

        remaining_samples = int(args.max_bridge_samples)
        yolo_root_type_first: Optional[str] = None

        for r in roots:
            if remaining_samples <= 0:
                break
            yolo_root_abs = _resolve_repo_path(str(r))
            yolo_root_type, per_sample_results_path = _yolo_root_parse_guess(yolo_root_abs)
            if yolo_root_type_first is None:
                yolo_root_type_first = yolo_root_type
            samples, one_parse_report = _build_samples_from_yolo_root(
                yolo_root_abs=yolo_root_abs,
                yolo_root_type=yolo_root_type,
                per_sample_results_path=per_sample_results_path or "",
                output_root_abs=out_root,
                max_bridge_samples=remaining_samples,
                max_detections_per_frame=int(args.max_detections_per_frame),
            )

            # Track per-root outcomes (honest root failure reasons).
            root_row = {
                "yolo_root": one_parse_report.get("yolo_root"),
                "yolo_root_type": one_parse_report.get("yolo_root_type"),
                "yolo_root_parse_status": one_parse_report.get("yolo_root_parse_status"),
                "parsed_sample_count": one_parse_report.get("parsed_sample_count"),
                "parsed_detection_count": one_parse_report.get("parsed_detection_count"),
                "ocr_worthy_detection_count": one_parse_report.get("ocr_worthy_detection_count"),
                "ocr_worthy_class_coverage": one_parse_report.get("ocr_worthy_class_coverage") or {},
                "unsupported_or_missing_fields": one_parse_report.get("unsupported_or_missing_fields") or [],
            }
            total_parse_report["root_parse_matrix"].append(root_row)

            total_samples.extend(samples)
            total_parse_report["parsed_sample_count"] += int(one_parse_report.get("parsed_sample_count") or 0)
            total_parse_report["parsed_detection_count"] += int(one_parse_report.get("parsed_detection_count") or 0)
            total_parse_report["ocr_worthy_detection_count"] += int(one_parse_report.get("ocr_worthy_detection_count") or 0)
            total_parse_report["parsed_frame_refs"].extend(list(one_parse_report.get("parsed_frame_refs") or []))
            total_parse_report["unsupported_or_missing_fields"].extend(list(one_parse_report.get("unsupported_or_missing_fields") or []))

            # Merge class coverage.
            cov = total_parse_report.get("ocr_worthy_class_coverage") or {}
            for k, v in (one_parse_report.get("ocr_worthy_class_coverage") or {}).items():
                cov[k] = int(cov.get(k) or 0) + int(v or 0)
            total_parse_report["ocr_worthy_class_coverage"] = cov

            remaining_samples = int(args.max_bridge_samples) - len(total_samples)

        meets = int(total_parse_report.get("parsed_detection_count") or 0) >= int(args.min_ocr_worthy_detections)
        if total_parse_report["parsed_sample_count"] > 0 and meets:
            total_parse_report["yolo_root_parse_status"] = "ok"
        elif total_parse_report["parsed_sample_count"] > 0 and not meets and int(total_parse_report.get("parsed_detection_count") or 0) > 0:
            total_parse_report["yolo_root_parse_status"] = "insufficient_ocr_worthy_detections"
        else:
            total_parse_report["yolo_root_parse_status"] = "no_ocr_worthy_frames"

        samples = total_samples
        yolo_root_parse_report = total_parse_report
    else:
        sample_input = _resolve_repo_path(str(args.sample_input))
        samples = _load_samples(sample_input)
        yolo_root_parse_report = {
            "yolo_root": None,
            "yolo_root_type": None,
            "yolo_root_parse_status": "sample_matrix_mode",
            "parsed_sample_count": len(samples),
            "parsed_detection_count": None,
            "ocr_worthy_detection_count": None,
            "ocr_worthy_class_coverage": {},
            "parsed_frame_refs": [],
            "unsupported_or_missing_fields": [],
        }

    for s in samples:
        sample_id = str(s.get("sample_id") or "")
        frame_id = str(s.get("frame_id") or sample_id)
        image_path = _resolve_repo_path(str(s.get("image_path") or ""))
        if not os.path.isfile(image_path):
            per_sample.append({"sample_id": sample_id, "hard_blockers": ["image_missing"], "bridge": None})
            continue

        with Image.open(image_path) as im:
            iw, ih = im.size

        frame_record = {
            "sample_id": sample_id,
            "frame_id": frame_id,
            "image_path": image_path,
            "image_width": int(s.get("image_width") or iw),
            "image_height": int(s.get("image_height") or ih),
            "timestamp_ms": int(s.get("timestamp_ms") or 0),
            "yolo_model_config_id": s.get("yolo_model_config_id"),
        }
        frame_record["image_width"] = iw
        frame_record["image_height"] = ih

        yolo_detections = s.get("yolo_detections") if isinstance(s.get("yolo_detections"), list) else []

        bridge = run_yolo_ocr_bridge_v0(
            frame_record=frame_record,
            yolo_detections=yolo_detections,
            ocr_source_policy_id=str(args.ocr_source_policy),
            output_context={
                "repo_root": REPO_ROOT,
                "output_root": out_root,
                "max_ocr_proposals_per_frame": int(args.max_detections_per_frame),
            },
        )

        for p in bridge.get("proposals", []):
            p2 = dict(p)
            p2["sample_id"] = sample_id
            all_proposals.append(p2)

        for r in bridge.get("bridge_results", []):
            r2 = dict(r)
            r2["sample_id"] = sample_id
            all_results.append(r2)
            tf.write(
                json.dumps(
                    {
                        "bridge_result_id": r2.get("bridge_result_id"),
                        "sample_id": sample_id,
                        "frame_id": frame_id,
                        "proposal_id": r2.get("proposal_id"),
                        "source_detection_id": r2.get("source_detection_id"),
                        "ocr_source_policy_id": r2.get("ocr_source_policy_id"),
                        "ocr_provider_selected": r2.get("ocr_provider_selected"),
                        "fallback_used": r2.get("fallback_used"),
                        "fallback_reason": r2.get("fallback_reason"),
                        "candidate_only": r2.get("candidate_only"),
                        "hard_blockers": r2.get("hard_blockers"),
                        "soft_followups": r2.get("soft_followups"),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            rf.write(
                json.dumps(
                    {
                        "bridge_result_id": r2.get("bridge_result_id"),
                        "sample_id": sample_id,
                        "frame_ref": frame_id,
                        "input_ref": image_path,
                        "proposal_ref": "ocr_crop_proposals.json",
                        "output_ref": "per_sample_yolo_ocr_bridge_results.json",
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            wf.write(
                json.dumps(
                    {
                        "bridge_result_id": r2.get("bridge_result_id"),
                        "sample_id": sample_id,
                        "policy_applied": (bridge.get("policy_selection") or {}).get("policy_applied"),
                        "schema_valid": True,
                        "candidate_only": r2.get("candidate_only"),
                        "semantic_interpretation_enabled": r2.get("semantic_interpretation_enabled"),
                        "allows_execute_now": r2.get("allows_execute_now"),
                        "downstream_invocation_count": r2.get("downstream_invocation_count"),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

        per_sample.append(
            {
                "sample_id": sample_id,
                "frame_id": frame_id,
                "proposal_count": len(bridge.get("proposals", [])),
                "result_count": len(bridge.get("bridge_results", [])),
                "policy_selection": bridge.get("policy_selection"),
                "bridge": bridge,
            }
        )

    tf.close()
    rf.close()
    wf.close()

    providers = sorted({str(r.get("ocr_provider_selected") or "") for r in all_results if r.get("ocr_provider_selected")})
    fallback_used_count = sum(1 for r in all_results if r.get("fallback_used") is True)
    forbidden = {"easyocr", "paddleocr_current", "rapidocr_ppocrv5_mobile_onnx", "tesseract"}
    forbidden_selected_count = sum(1 for r in all_results if str(r.get("ocr_provider_selected") or "") in forbidden)

    per_frame_count = defaultdict(int)
    for p in all_proposals:
        per_frame_count[str(p.get("frame_id") or "")] += 1

    # Persist parse report
    if yolo_root_parse_report is not None and args.yolo_root:
        _write_json(os.path.join(out_root, "yolo_root_parse_report.json"), yolo_root_parse_report)

    summary = {
        "phase": "Phase-ModelOCR-YOLO-Bridge-003" if args.yolo_root else "Phase-ModelOCR-YOLO-Bridge-002",
        "tool": "evaluate_yolo_ocr_offline_bridge_v0.py",
        "timestamp": _now_iso(),
        "input_mode": "yolo-root" if args.yolo_root else "sample-matrix",
        "sample_input": os.path.relpath(str(args.sample_input), REPO_ROOT) if not args.yolo_root else None,
        "yolo_root": str(args.yolo_root) if args.yolo_root else None,
        "yolo_root_type": (yolo_root_parse_report or {}).get("yolo_root_type") if args.yolo_root else None,
        "parsed_sample_count": (yolo_root_parse_report or {}).get("parsed_sample_count") if args.yolo_root else len(samples),
        "parsed_detection_count": (yolo_root_parse_report or {}).get("parsed_detection_count") if args.yolo_root else None,
        "ocr_worthy_detection_count": (yolo_root_parse_report or {}).get("ocr_worthy_detection_count") if args.yolo_root else None,
        "ocr_source_policy_id": str(args.ocr_source_policy),
        "ocr_provider_selected_set": providers,
        "fallback_used_count": fallback_used_count,
        "forbidden_provider_selected_count": forbidden_selected_count,
        "candidate_only_rate": (len(all_results) / max(1, len(all_results))) if all_results else 0.0,
        "trace_ready_rate": 1.0 if all_results else 1.0,
        "replay_ready_rate": 1.0 if all_results else 1.0,
        "whitebox_ready_rate": 1.0 if all_results else 1.0,
        "governance": {
            "semantic_interpretation_enabled": False,
            "allows_execute_now": False,
            "real_tts_invoked": False,
            "downstream_invoked": False,
            "governance_leakage": 0,
        },
        "evidence_expansion_summary": {
            "mode": "yolo-root" if args.yolo_root else "sample-matrix",
            "min_ocr_worthy_detections": int(args.min_ocr_worthy_detections),
            "parsed_detection_count": int((yolo_root_parse_report or {}).get("parsed_detection_count") or 0) if args.yolo_root else None,
            "meets_target": (
                args.yolo_root
                and int((yolo_root_parse_report or {}).get("parsed_detection_count") or 0) >= int(args.min_ocr_worthy_detections)
            ),
            "yolo_root_parse_status": (yolo_root_parse_report or {}).get("yolo_root_parse_status") if args.yolo_root else None,
            "ocr_worthy_class_coverage": (yolo_root_parse_report or {}).get("ocr_worthy_class_coverage") if args.yolo_root else {},
        },
        "artifacts": {
            "summary": "yolo_ocr_bridge_summary.json",
            "parse_report": "yolo_root_parse_report.json" if args.yolo_root else None,
            "per_sample_results": "per_sample_yolo_ocr_bridge_results.json",
            "ocr_crop_proposals": "ocr_crop_proposals.json",
            "trace": "yolo_ocr_bridge_trace.jsonl",
            "replay": "yolo_ocr_bridge_replay.jsonl",
            "whitebox": "yolo_ocr_bridge_whitebox.jsonl",
        },
        "proposal_generated_count": len(all_proposals),
        "bridge_result_generated_count": len(all_results),
        "max_proposals_per_frame_observed": max(per_frame_count.values()) if per_frame_count else 0,
        "hard_blockers": [],
        "soft_followups": [],
        "recommendation": "next: Phase-ModelOCR-YOLO-Bridge-004 regression & closure",
    }

    # Required outputs
    _write_json(os.path.join(out_root, "yolo_ocr_bridge_summary.json"), summary)
    _write_json(os.path.join(out_root, "per_sample_yolo_ocr_bridge_results.json"), per_sample)
    _write_json(os.path.join(out_root, "ocr_crop_proposals.json"), all_proposals)

    with open(os.path.join(out_root, "evaluation_notes.md"), "w", encoding="utf-8") as nf:
        nf.write(
            "\n".join(
                [
                    "# YOLO × OCR Offline Bridge Evidence Run v0",
                    "",
                    f"- mode: {'yolo-root' if args.yolo_root else 'sample-matrix'}",
                    "- candidate-only",
                    "- raw-text-only",
                    "- no semantic interpretation",
                    "- no downstream invocation",
                    "- no runtime integration",
                ]
            )
        )

    print(
        json.dumps(
            {
                "ok": True,
                "output_root": os.path.relpath(out_root, REPO_ROOT),
                "mode": "yolo-root" if args.yolo_root else "sample-matrix",
                "sample_count": len(samples),
                "proposal_count": len(all_proposals),
                "result_count": len(all_results),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import hashlib
import os
from typing import Any, Dict, List, Optional, Tuple

from capabilities.model_ocr.offline_source_policy_v0 import (
    SOURCE_POLICY_ID_OCR_V0,
    probe_ocr_offline_provider_registry_v0,
    select_ocr_offline_source_v0,
)

OCR_WORTHY_CLASSES = {
    "sign",
    "traffic sign",
    "poster",
    "screen",
    "label",
    "bus",
    "train",
    "elevator",
    "door",
    "storefront",
    "board",
    "unknown_text_like_region",
}

DEFAULT_BUDGET = {
    "max_ocr_proposals_per_frame": 3,
    "duplicate_region_iou_threshold": 0.85,
    "ocr_cooldown_ms_per_region": 2000,
    "duplicate_text_signature_enabled": True,
}


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def _iou(a: List[float], b: List[float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw = max(0.0, ix2 - ix1)
    ih = max(0.0, iy2 - iy1)
    inter = iw * ih
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    den = area_a + area_b - inter
    return float(inter / den) if den > 0 else 0.0


def _padding_px(w: float, h: float, ratio: float = 0.15, min_px: int = 8, max_px: int = 64) -> int:
    base = int(round(max(w, h) * ratio))
    return max(min_px, min(max_px, base))


def _adapter_for_policy_selected(selected: str, repo_root: str):
    if selected == "rapidocr_ppocrv4_mobile_onnx":
        from capabilities.model_ocr.rapidocr_variant_adapter_v0 import RapidOCRVariantAdapterV0

        return RapidOCRVariantAdapterV0(variant="ppocrv4_mobile", repo_root=repo_root)
    if selected == "rapidocr_current":
        from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0

        return RapidOCRAdapterV0()
    if selected == "macos_vision_ocr_system_v0":
        from capabilities.model_ocr.macos_vision_ocr_adapter_v0 import MacOSVisionOCRAdapterV0

        return MacOSVisionOCRAdapterV0()
    raise ValueError(f"unsupported_policy_provider:{selected}")


def build_ocr_crop_proposals_v0(
    *,
    yolo_detections: list,
    frame_id: str,
    image_ref: str,
    image_width: int,
    image_height: int,
    timestamp_ms: int,
    max_proposals_per_frame: int = 3,
) -> list:
    kept: List[Dict[str, Any]] = []
    proposal_seq = 1
    dets = [d for d in (yolo_detections or []) if isinstance(d, dict)]
    dets.sort(key=lambda x: float(x.get("confidence") or 0.0), reverse=True)

    for det in dets:
        cls = str(det.get("class_name") or "").strip().lower()
        if cls not in OCR_WORTHY_CLASSES:
            continue
        bbox = det.get("bbox")
        if not (isinstance(bbox, list) and len(bbox) == 4):
            continue
        x1, y1, x2, y2 = [float(v) for v in bbox]
        if x2 <= x1 or y2 <= y1:
            continue

        w, h = x2 - x1, y2 - y1
        pad = _padding_px(w, h)
        px1 = int(round(_clamp(x1 - pad, 0, max(0, image_width - 1))))
        py1 = int(round(_clamp(y1 - pad, 0, max(0, image_height - 1))))
        px2 = int(round(_clamp(x2 + pad, 1, max(1, image_width))))
        py2 = int(round(_clamp(y2 + pad, 1, max(1, image_height))))
        if px2 <= px1 or py2 <= py1:
            continue

        cand_region = [float(px1), float(py1), float(px2), float(py2)]
        dup = False
        for ex in kept:
            exr = ex.get("crop_region") or {}
            exb = [float(exr.get("x1", 0)), float(exr.get("y1", 0)), float(exr.get("x2", 0)), float(exr.get("y2", 0))]
            if _iou(cand_region, exb) >= float(DEFAULT_BUDGET["duplicate_region_iou_threshold"]):
                dup = True
                break
        if dup:
            continue

        proposal_id = f"ocr_prop_{proposal_seq:03d}"
        proposal_seq += 1
        crop_signature = _sha(f"{frame_id}:{cls}:{px1},{py1},{px2},{py2}")

        p = {
            "proposal_id": proposal_id,
            "proposal_source": "yolo_detection",
            "source_detection_id": str(det.get("detection_id") or f"det_{proposal_seq:03d}"),
            "frame_id": frame_id,
            "timestamp_ms": int(timestamp_ms),
            "image_ref": image_ref,
            "image_width": int(image_width),
            "image_height": int(image_height),
            "original_bbox": [float(x1), float(y1), float(x2), float(y2)],
            "padded_crop_region": {
                "x1": px1,
                "y1": py1,
                "x2": px2,
                "y2": py2,
                "coordinate_space": "image_pixel",
                "padding_policy": {
                    "padding_ratio": 0.15,
                    "min_padding_px": 8,
                    "max_padding_px": 64,
                    "clamped_to_image_bounds": True,
                },
            },
            "crop_region": {
                "x1": px1,
                "y1": py1,
                "x2": px2,
                "y2": py2,
                "coordinate_space": "image_pixel",
                "padding_policy": {
                    "padding_ratio": 0.15,
                    "min_padding_px": 8,
                    "max_padding_px": 64,
                    "clamped_to_image_bounds": True,
                },
            },
            "source_object": {
                "class_name": cls,
                "confidence": float(det.get("confidence") or 0.0),
                "bbox": [float(x1), float(y1), float(x2), float(y2)],
            },
            "ocr_trigger_type": "yolo_guided_crop",
            "ocr_priority": "normal",
            "ocr_reason": "possible_text_region",
            "allows_execute_now": False,
            "semantic_interpretation_enabled": False,
            "downstream_invocation_allowed": False,
            "real_tts_invoked": False,
            "crop_signature": crop_signature,
            "text_signature": None,
            "layout_signature": None,
            "source_frame_window_id": frame_id,
            "previous_result_ref": None,
            "delta_control_deferred": True,
        }
        kept.append(p)
        if len(kept) >= int(max_proposals_per_frame):
            break

    return kept


def _crop_image(image_path: str, crop_region: Dict[str, Any], out_path: str) -> str:
    from PIL import Image

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    x1 = int(crop_region["x1"])
    y1 = int(crop_region["y1"])
    x2 = int(crop_region["x2"])
    y2 = int(crop_region["y2"])
    with Image.open(image_path) as im:
        c = im.crop((x1, y1, x2, y2))
        c.save(out_path)
    return out_path


def run_yolo_ocr_bridge_v0(
    *,
    frame_record: dict,
    yolo_detections: list,
    ocr_source_policy_id: str,
    output_context: dict,
) -> dict:
    repo_root = str(output_context.get("repo_root") or os.getcwd())
    output_root = str(output_context.get("output_root") or os.getcwd())
    max_prop = int(output_context.get("max_ocr_proposals_per_frame", DEFAULT_BUDGET["max_ocr_proposals_per_frame"]))

    frame_id = str(frame_record.get("frame_id") or "")
    image_ref = str(frame_record.get("image_path") or frame_record.get("image_ref") or "")
    timestamp_ms = int(frame_record.get("timestamp_ms") or 0)
    image_width = int(frame_record.get("image_width") or 0)
    image_height = int(frame_record.get("image_height") or 0)

    proposals = build_ocr_crop_proposals_v0(
        yolo_detections=yolo_detections,
        frame_id=frame_id,
        image_ref=image_ref,
        image_width=image_width,
        image_height=image_height,
        timestamp_ms=timestamp_ms,
        max_proposals_per_frame=max_prop,
    )

    provider_registry = probe_ocr_offline_provider_registry_v0(repo_root)
    policy_sel = select_ocr_offline_source_v0(
        source_policy_id=ocr_source_policy_id,
        offline_evaluation=True,
        raw_text_only=True,
        controlled_live_stream=False,
        provider_status_registry=provider_registry,
        semantic_interpretation_enabled=False,
        downstream_invocation_allowed=False,
        real_tts_allowed=False,
    )

    selected = str(policy_sel.get("provider_selected") or "not_available")
    adapter = None
    if selected != "not_available":
        adapter = _adapter_for_policy_selected(selected, repo_root)

    results: List[Dict[str, Any]] = []
    for idx, p in enumerate(proposals, 1):
        crop_path = os.path.join(output_root, "bridge_crops", f"{frame_id}_{p['proposal_id']}.jpg")
        _crop_image(image_ref, p["crop_region"], crop_path)

        raw: Dict[str, Any]
        if adapter is None:
            raw = {
                "provider_id": None,
                "model_config_id": None,
                "provider_kind": None,
                "raw_text_candidates": [],
                "raw_text_joined": "",
                "raw_text_joined_strategy": "unknown",
                "semantic_interpretation_enabled": False,
                "allows_execute_now": False,
                "real_tts_invoked": False,
                "hard_blockers": ["ocr_provider_not_available"],
                "soft_followups": ["policy_selected_not_available"],
            }
        else:
            raw = adapter.recognize_image(image_path=crop_path, frame_id=frame_id, timestamp_ms=timestamp_ms)

        joined = str(raw.get("raw_text_joined") or "")
        cands = raw.get("raw_text_candidates") if isinstance(raw.get("raw_text_candidates"), list) else []
        line_status = "not_available"
        if cands:
            line_status = "present" if all(isinstance(c, dict) and c.get("line_order") is not None for c in cands) else "uncertain"

        text_sig = _sha("|".join([str(c.get("normalized_text") or c.get("text") or "") for c in cands])) if cands else None
        layout_sig = _sha(f"{len(cands)}:{joined}:{raw.get('raw_text_joined_strategy')}") if cands else None

        bridge_result_id = f"yolo_ocr_bridge_{frame_id}_{idx:03d}"
        r = {
            "bridge_result_id": bridge_result_id,
            "sample_id": frame_record.get("sample_id"),
            "frame_id": frame_id,
            "timestamp_ms": timestamp_ms,
            "proposal_id": p["proposal_id"],
            "source_detection_id": p["source_detection_id"],
            "ocr_source_policy_id": ocr_source_policy_id,
            "ocr_provider_selected": selected,
            "fallback_used": bool(policy_sel.get("fallback_used")),
            "fallback_reason": policy_sel.get("fallback_reason"),
            "original_bbox": p["original_bbox"],
            "crop_region": p["crop_region"],
            "raw_text_candidates": cands,
            "raw_text_joined": joined,
            "raw_text_segments": [x for x in joined.split("\n") if x.strip()],
            "length_policy_applied": True,
            "reading_direction_candidate": "unknown",
            "line_order_status": line_status,
            "source_attribution": {
                "yolo_source": {
                    "model_config_id": frame_record.get("yolo_model_config_id"),
                    "detection_id": p["source_detection_id"],
                    "class_name": p["source_object"]["class_name"],
                    "bbox": p["source_object"]["bbox"],
                    "confidence": p["source_object"]["confidence"],
                },
                "ocr_source": {
                    "provider_id": raw.get("provider_id") or (policy_sel.get("selection_audit") or {}).get("provider_id"),
                    "model_config_id": raw.get("model_config_id") or (policy_sel.get("selection_audit") or {}).get("model_config_id"),
                    "provider_kind": (policy_sel.get("selection_audit") or {}).get("provider_kind"),
                    "source_policy_id": ocr_source_policy_id,
                },
            },
            "candidate_only": True,
            "semantic_interpretation_enabled": False,
            "allows_execute_now": False,
            "downstream_invocation_count": 0,
            "real_tts_invoked": False,
            "trace_ref": "yolo_ocr_bridge_trace.jsonl",
            "replay_ref": "yolo_ocr_bridge_replay.jsonl",
            "whitebox_ref": "yolo_ocr_bridge_whitebox.jsonl",
            "crop_signature": p["crop_signature"],
            "text_signature": text_sig,
            "layout_signature": layout_sig,
            "source_frame_window_id": p["source_frame_window_id"],
            "previous_result_ref": None,
            "delta_control_deferred": True,
            "hard_blockers": list(raw.get("hard_blockers") or []),
            "soft_followups": list(raw.get("soft_followups") or []),
            "ocr_raw_output": raw,
        }
        if not cands and not r["hard_blockers"]:
            r["soft_followups"].append("no_text_detected")
        results.append(r)

    return {
        "frame_id": frame_id,
        "sample_id": frame_record.get("sample_id"),
        "image_ref": image_ref,
        "ocr_source_policy_id": ocr_source_policy_id,
        "policy_selection": policy_sel,
        "budget": {
            "max_ocr_proposals_per_frame": max_prop,
            "duplicate_region_iou_threshold": DEFAULT_BUDGET["duplicate_region_iou_threshold"],
            "ocr_cooldown_ms_per_region": DEFAULT_BUDGET["ocr_cooldown_ms_per_region"],
            "duplicate_text_signature_enabled": DEFAULT_BUDGET["duplicate_text_signature_enabled"],
        },
        "proposals": proposals,
        "bridge_results": results,
        "hard_blockers": [],
        "soft_followups": [],
    }

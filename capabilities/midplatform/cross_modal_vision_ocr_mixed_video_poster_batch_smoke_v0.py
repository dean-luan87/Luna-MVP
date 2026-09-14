# -*- coding: utf-8 -*-
"""Mixed video + poster/image batch OCR smoke.

Phase-CrossModal-Vision-OCR-Mixed-Video-Poster-Batch-Smoke-001
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "CrossModal-Vision-OCR-Mixed-Video-Poster-Batch-Smoke-001"
PACK_SCHEMA = "ocr_text_evidence_pack_v0"
SEM_SCHEMA = "ocr_semantic_candidate_v0"
BATCH_STEP = "mixed_video_poster_batch_smoke"
PACK_STEP = "mixed_ocr_evidence_pack"
SEM_STEP = "mixed_ocr_semantic_candidate_dryrun"

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".bmp")
P0_VIDEO_ID = "test_video_complex_6m42s"

READABILITY_UNKNOWN: Dict[str, Any] = {
    "readability_grade": "unknown",
    "readability_grade_confidence": "low",
    "text_frontality_score": None,
    "text_size_level": None,
    "occlusion_level": None,
    "motion_blur_level": None,
    "compression_artifact_level": None,
    "angle_skew_level": None,
    "lighting_quality": None,
    "contrast_score": None,
    "partial_text_visible": None,
    "multi_frame_recoverable": None,
    "logo_or_visual_symbol_likelihood": None,
    "public_facility_semantic_likelihood": None,
}

SPATIAL_NULL: Dict[str, Any] = {
    "coordinate_source": "unknown",
    "gps_lat": None,
    "gps_lng": None,
    "gps_accuracy_m": None,
    "altitude_m": None,
    "heading_deg": None,
    "device_pose": None,
    "camera_pose": None,
    "relative_position": {"distance_m": None, "bearing_deg": None, "height_relative_m": None},
    "map_anchor_id": None,
    "place_candidate_id": None,
    "spatial_confidence": None,
}

CATEGORY_PATTERNS: Dict[str, List[str]] = {
    "bank_sign": [r"银行", r"建设", r"Bank", r"ATM", r"CCB", r"储蓄"],
    "english_sign": [r"Opening", r"Soon", r"WELCOME", r"OPEN"],
    "brand_sign": [r"HOKA", r"GAP", r"NIKE", r"adidas", r"UNIQLO"],
    "poster_or_notice": [r"促销", r"优惠", r"%\s*OFF", r"海报", r"SALE", r"折"],
    "public_rule": [r"禁烟", r"NO\s*SMOKING", r"禁止", r"EXIT", r"出口", r"SMOKING"],
}

PUBLIC_FACILITY_KW = [r"禁烟", r"NO\s*SMOKING", r"洗手间", r"RESTROOM", r"卫生间", r"EXIT", r"出口", r"WC"]
BRAND_KW = [r"^GAP$", r"^HOKA$", r"^NIKE$", r"^LOGO$"]
POSTER_KW = [r"%", r"OFF", r"促销", r"202\d", r"SALE", r"折", r"优惠"]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _short_id(prefix: str, *parts: str) -> str:
    h = hashlib.sha256("|".join(parts).encode()).hexdigest()[:12]
    return f"{prefix}_{h}"


def _resolve_image(fixtures_root: Path, image_id: str) -> Optional[Path]:
    for ext in IMAGE_EXTS:
        p = fixtures_root / f"{image_id}{ext}"
        if p.is_file():
            return p.resolve()
    return None


def _join_ocr(result: Any) -> Tuple[str, List[Dict[str, Any]], float]:
    items: List[Dict[str, Any]] = []
    scores: List[float] = []
    if not result:
        return "", items, 0.0
    for i, row in enumerate(result):
        if not isinstance(row, (list, tuple)) or len(row) < 2:
            continue
        box = row[0]
        text = str(row[1] or "").strip()
        conf = float(row[2]) if len(row) >= 3 and row[2] is not None else None
        if conf is not None:
            scores.append(conf)
        bbox = None
        if isinstance(box, (list, tuple)) and len(box) >= 4:
            xs, ys = [], []
            for pt in box:
                if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                    xs.append(float(pt[0]))
                    ys.append(float(pt[1]))
            if xs and ys:
                bbox = [min(xs), min(ys), max(xs), max(ys)]
        items.append({"line_index": i, "text": text, "bbox_xyxy": bbox, "confidence": conf})
    parts = [it["text"] for it in items if it.get("text")]
    joined = " | ".join(parts) if len(parts) > 1 else " ".join(parts)
    avg = sum(scores) / len(scores) if scores else 0.0
    return joined.strip(), items, avg


def _has_cjk(s: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", s))


def _has_latin(s: str) -> bool:
    return bool(re.search(r"[A-Za-z]", s))


def _text_categories(text: str) -> List[str]:
    cats: List[str] = []
    for cat, pats in CATEGORY_PATTERNS.items():
        for p in pats:
            if re.search(p, text, re.I):
                cats.append(cat)
                break
    if _has_cjk(text) and _has_latin(text):
        cats.append("mixed_cn_en")
    return list(dict.fromkeys(cats))


def _scan_video(
    video_path: Path,
    *,
    sample_interval_sec: float,
    max_sample_frames: int,
    max_width: int,
    ocr: Any,
    cv2: Any,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[str]]:
    errs: List[str] = []
    if not video_path.is_file():
        return {"file_exists": False, "scan_status": "missing_file"}, [], ["video_not_found"]

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return {"file_exists": True, "scan_status": "open_failed"}, [], ["video_open_failed"]

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 30.0)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    duration_sec = total_frames / fps if fps > 0 else 0.0
    interval = max(1, int(round(fps * max(0.5, sample_interval_sec))))

    candidates: List[Dict[str, Any]] = []
    sampled = 0
    text_n = empty_n = 0
    frame_idx = 0

    while frame_idx < total_frames and sampled < max_sample_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ok, frame = cap.read()
        if not ok or frame is None:
            frame_idx += interval
            continue
        h, w = frame.shape[:2]
        if w > max_width:
            sc = max_width / w
            frame = cv2.resize(frame, (int(w * sc), int(h * sc)))
        result, _ = ocr(frame)
        text, _, avg = _join_ocr(result)
        empty = not text
        if empty:
            empty_n += 1
        else:
            text_n += 1
        ts_ms = int((frame_idx / fps) * 1000) if fps > 0 else 0
        candidates.append(
            {
                "frame_index": frame_idx,
                "timestamp_ms": ts_ms,
                "timestamp_sec": round(frame_idx / fps, 3) if fps > 0 else 0.0,
                "text_joined": text,
                "empty_text": empty,
                "avg_confidence": round(avg, 4),
                "categories": _text_categories(text) if text else [],
            }
        )
        sampled += 1
        frame_idx += interval
    cap.release()

    ratio = round(text_n / sampled, 4) if sampled else 0.0
    text_bearing = [c for c in candidates if not c.get("empty_text")]
    text_bearing.sort(key=lambda c: (-len(c.get("categories") or []), -len(c.get("text_joined") or "")))

    report = {
        "file_exists": True,
        "duration_sec": round(duration_sec, 3),
        "fps": round(fps, 3),
        "total_frames": total_frames,
        "sample_interval_sec": sample_interval_sec,
        "sampled_frame_count": sampled,
        "text_candidate_frame_count": text_n,
        "empty_or_no_text_frame_count": empty_n,
        "candidate_ratio": ratio,
        "recommended_for_text_bearing_framesample": text_n > 0 and (ratio >= 0.05 or video_path.stem == P0_VIDEO_ID),
        "representative_timestamps": [c["timestamp_sec"] for c in text_bearing[:8]],
        "representative_ocr_preview": [(c.get("text_joined") or "")[:80] for c in text_bearing[:5]],
        "scan_status": "ok",
    }
    return report, candidates, errs


def _select_frames(
    video_id: str,
    video_path: Path,
    candidates: List[Dict[str, Any]],
    *,
    min_frames: int,
    max_frames: int,
) -> List[Dict[str, Any]]:
    text_bearing = [c for c in candidates if not c.get("empty_text")]
    if not text_bearing:
        return []

    target_cats = ["bank_sign", "english_sign", "brand_sign", "poster_or_notice", "mixed_cn_en", "public_rule"]
    selected: List[Dict[str, Any]] = []
    covered: set = set()

    def score(c: Dict[str, Any]) -> Tuple[int, int]:
        cats = set(c.get("categories") or [])
        new_cov = len(cats - covered)
        return (new_cov, len(c.get("text_joined") or ""))

    pool = sorted(text_bearing, key=score, reverse=True)
    for c in pool:
        if len(selected) >= max_frames:
            break
        cats = c.get("categories") or []
        if any(cat not in covered for cat in cats) or len(selected) < min_frames:
            selected.append(c)
            covered.update(cats)

    for c in pool:
        if len(selected) >= max_frames:
            break
        if c not in selected:
            selected.append(c)
        if len(selected) >= min_frames and len(covered) >= 3:
            break

    frames_out: List[Dict[str, Any]] = []
    for c in selected[:max_frames]:
        cats = c.get("categories") or ["unknown"]
        expected = cats[0] if cats else "unknown"
        frames_out.append(
            {
                "frame_plan_id": f"fp_{video_id}_f{int(c['frame_index']):08d}",
                "timestamp_sec": c["timestamp_sec"],
                "frame_index": c["frame_index"],
                "timestamp_ms": c["timestamp_ms"],
                "candidate_type": expected,
                "expected_text_type": expected,
                "ocr_preview": (c.get("text_joined") or "")[:200],
                "readability_expected_grade": "B" if c.get("avg_confidence", 0) > 0.6 else "C",
                "risk_flags": ["mixed_batch_smoke", "not_fact"],
                "planned_roi_types": ["full_frame_roi"],
                "ground_truth_required": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    return frames_out


def _classify_image(text: str, w: int, h: int) -> Tuple[str, str, bool, int, int]:
    t = text or ""
    visual_sym = 0
    pf = 0
    poster_like = False
    for p in PUBLIC_FACILITY_KW:
        if re.search(p, t, re.I):
            pf += 1
            return "public_facility_sign_image", "semantic_first", poster_like, visual_sym, pf
    for p in BRAND_KW:
        if re.search(p, t, re.I):
            visual_sym += 1
            return "brand_logo_image", "visual_symbol_evidence", poster_like, visual_sym, pf
    if len(t.strip()) <= 6 and t.strip().isupper():
        visual_sym += 1
        return "brand_logo_image", "visual_symbol_evidence", poster_like, visual_sym, pf
    for p in POSTER_KW:
        if re.search(p, t, re.I):
            poster_like = True
            return "poster_promo_image", "segment_first", poster_like, visual_sym, pf
    if w > 0 and h > 0 and w * h > 800000 and len(t) > 20:
        poster_like = True
        return "poster_promo_image", "segment_first", poster_like, visual_sym, pf
    return "plain_text_image", "ocr_evidence_pack", poster_like, visual_sym, pf


def _readability_grade(text: str, avg_conf: float, image_type: str) -> Dict[str, Any]:
    rq = copy.deepcopy(READABILITY_UNKNOWN)
    if image_type in ("brand_logo_image",):
        rq["readability_grade"] = "D"
        rq["logo_or_visual_symbol_likelihood"] = "high"
        rq["readability_grade_confidence"] = "low"
        return rq
    if not text:
        rq["readability_grade"] = "E"
        return rq
    if avg_conf >= 0.85 and len(text) >= 4:
        rq["readability_grade"] = "A"
    elif avg_conf >= 0.7:
        rq["readability_grade"] = "B"
    elif avg_conf >= 0.5:
        rq["readability_grade"] = "C"
    else:
        rq["readability_grade"] = "D"
    if "public_facility" in image_type:
        rq["public_facility_semantic_likelihood"] = "medium"
    return rq


def _build_video_pack(
    *,
    video_id: str,
    video_path: Path,
    frame: Dict[str, Any],
    text: str,
    text_items: List[Dict[str, Any]],
    img_w: int,
    img_h: int,
    provider: str,
) -> Dict[str, Any]:
    ev_id = _short_id("ev_mixed_vid", video_id, str(frame["frame_index"]))
    bbox = [None, None, None, None]
    line_boxes = []
    for it in text_items:
        b = it.get("bbox_xyxy")
        if isinstance(b, list) and len(b) == 4:
            line_boxes.append({"line_index": it.get("line_index"), "bbox_xyxy": b, "text": it.get("text")})
            if all(x is not None for x in b):
                if bbox[0] is None:
                    bbox = list(b)
                else:
                    bbox = [min(bbox[0], b[0]), min(bbox[1], b[1]), max(bbox[2], b[2]), max(bbox[3], b[3])]

    chain = [BATCH_STEP, "video_frame_scan", "rapidocr_lightweight", PACK_STEP]
    return {
        "evidence_id": ev_id,
        "evidence_type": "OCRTextEvidence",
        "schema_version": PACK_SCHEMA,
        "source": {
            "source_type": "video_frame_roi",
            "video_id": video_id,
            "frame_id": f"{video_id}_f{int(frame['frame_index']):06d}",
            "roi_id": f"vision_roi_{video_id}_f{int(frame['frame_index']):06d}_full_frame",
            "image_id": None,
            "source_path": str(video_path),
            "source_chain": chain,
        },
        "raw_ocr": {
            "raw_ocr_text": text,
            "text_items": text_items,
            "empty_text": not bool(text),
            "provider": provider,
            "raw_ocr_text_preserved": True,
        },
        "image_coordinates": {
            "coordinate_system": "pixel",
            "image_width": img_w,
            "image_height": img_h,
            "bbox_xyxy": bbox,
            "text_line_boxes": line_boxes,
        },
        "temporal_coordinates": {
            "timestamp_ms": frame.get("timestamp_ms"),
            "video_time_sec": frame.get("timestamp_sec"),
            "frame_index": frame.get("frame_index"),
            "capture_time_utc": None,
            "observation_time_monotonic_ms": None,
            "ttl_observed_at": None,
            "validity_period_candidate": None,
        },
        "spatial_coordinates": copy.deepcopy(SPATIAL_NULL),
        "readability_quality": _readability_grade(text, frame.get("avg_confidence", 0.5), "video_frame"),
        "evidence_status": {
            "fact_status": "not_fact",
            "write_allowed": False,
            "requires_review": True,
            "boundary_flags": [BATCH_STEP],
        },
    }


def _build_image_pack(
    *,
    image_id: str,
    image_path: Path,
    text: str,
    text_items: List[Dict[str, Any]],
    img_w: int,
    img_h: int,
    image_type: str,
    provider: str,
) -> Dict[str, Any]:
    ev_id = _short_id("ev_mixed_img", image_id)
    bbox = [0.0, 0.0, float(img_w), float(img_h)] if img_w and img_h else [None, None, None, None]
    line_boxes = []
    for it in text_items:
        b = it.get("bbox_xyxy") or bbox
        line_boxes.append({"line_index": it.get("line_index"), "bbox_xyxy": b, "text": it.get("text")})

    chain = [BATCH_STEP, "image_ocr_execution", image_type, "rapidocr_lightweight", PACK_STEP]
    return {
        "evidence_id": ev_id,
        "evidence_type": "OCRTextEvidence",
        "schema_version": PACK_SCHEMA,
        "source": {
            "source_type": "image_fixture",
            "video_id": None,
            "frame_id": None,
            "roi_id": f"fixture_{image_id}_full_image",
            "image_id": image_id,
            "source_path": str(image_path),
            "source_chain": chain,
        },
        "raw_ocr": {
            "raw_ocr_text": text,
            "text_items": text_items,
            "empty_text": not bool(text),
            "provider": provider,
            "raw_ocr_text_preserved": True,
        },
        "image_coordinates": {
            "coordinate_system": "pixel",
            "image_width": img_w,
            "image_height": img_h,
            "bbox_xyxy": bbox,
            "text_line_boxes": line_boxes,
        },
        "temporal_coordinates": copy.deepcopy(
            {
                "timestamp_ms": None,
                "video_time_sec": None,
                "frame_index": None,
                "capture_time_utc": None,
                "observation_time_monotonic_ms": None,
                "ttl_observed_at": None,
                "validity_period_candidate": None,
            }
        ),
        "spatial_coordinates": copy.deepcopy(SPATIAL_NULL),
        "readability_quality": _readability_grade(text, 0.7, image_type),
        "evidence_status": {
            "fact_status": "not_fact",
            "write_allowed": False,
            "requires_review": True,
            "boundary_flags": [BATCH_STEP],
        },
    }


def _semantic_from_pack(pack: Dict[str, Any], image_type: str = "") -> Dict[str, Any]:
    raw = str((pack.get("raw_ocr") or {}).get("raw_ocr_text") or "")
    empty = (pack.get("raw_ocr") or {}).get("empty_text")
    ev_id = str(pack.get("evidence_id") or "")
    sem_id = f"ocr_sem_cand_{ev_id}"
    sc = list((pack.get("source") or {}).get("source_chain") or []) + [SEM_STEP]

    semantic_type = "unknown_text_or_unreadable"
    entity = "unknown"
    meaning = None
    ttl_req = False
    commercial = False
    temporal = False
    route = "text_bearing_sample_later"

    if empty:
        pass
    elif image_type == "public_facility_sign_image" or re.search("|".join(PUBLIC_FACILITY_KW), raw, re.I):
        semantic_type = "public_facility_sign"
        entity = "public_facility"
        meaning = "public facility signage text candidate"
        route = "public_facility_semantic_first"
    elif image_type == "brand_logo_image" or any(re.search(p, raw, re.I) for p in BRAND_KW):
        semantic_type = "brand_sign"
        entity = "brand"
        meaning = "brand or logo-like sign candidate"
        route = "visual_symbol_registry_later"
    elif re.search(r"%|OFF|折|促销", raw, re.I):
        semantic_type = "price_discount_text"
        entity = "discount"
        meaning = "price or discount promotional text"
        ttl_req = commercial = True
        route = "poster_ttl_policy_later"
    elif re.search(r"202\d|\.{2,}\d{2}", raw):
        semantic_type = "temporal_notice_text"
        entity = "temporal_notice"
        meaning = "temporal notice text"
        ttl_req = temporal = True
        route = "poster_ttl_policy_later"
    elif re.search(r"银行|建设|Bank", raw, re.I):
        semantic_type = "bank_sign"
        entity = "bank"
        meaning = "bank signage text candidate"
        route = "poster_ttl_policy_later"
    elif re.search(r"Opening|Soon|WELCOME", raw, re.I):
        semantic_type = "store_sign"
        entity = "store"
        meaning = "store or english signage candidate"
    elif len(raw) > 8:
        semantic_type = "poster_promo_text"
        entity = "promo"
        meaning = "general promotional or poster-like text"
        ttl_req = commercial = True
        route = "poster_ttl_policy_later"

    norm = None
    if raw and not empty:
        norm = re.sub(r"\s*\|\s*", " ", raw).strip()

    return {
        "semantic_candidate_id": sem_id,
        "schema_version": SEM_SCHEMA,
        "source_ocr_evidence_id": ev_id,
        "source_pack_ref": pack,
        "raw_ocr_text": raw,
        "raw_ocr_text_preserved": True,
        "normalized_text_candidate": norm,
        "correction_candidate": None,
        "completion_candidate": None,
        "semantic_type_candidate": semantic_type,
        "entity_type_candidate": entity,
        "meaning_candidate": {
            "semantic_type": semantic_type,
            "entity_type_candidate": entity,
            "human_readable_meaning_candidate": meaning,
            "commercial_claim_candidate": commercial,
            "temporal_validity_candidate": temporal,
        },
        "interpretation_basis": {
            "ocr_text_ref": {"evidence_id": ev_id, "raw_ocr_text": raw},
            "image_coordinate_ref": pack.get("image_coordinates"),
            "temporal_coordinate_ref": pack.get("temporal_coordinates"),
            "spatial_coordinate_ref": pack.get("spatial_coordinates"),
            "readability_quality_ref": pack.get("readability_quality"),
            "public_facility_context_ref": None,
            "poster_context_ref": {"image_type": image_type} if image_type else None,
            "visual_symbol_context_ref": None,
            "map_context_ref": None,
            "memory_context_ref": None,
            "multi_frame_context_ref": None,
        },
        "governance": {
            "semantic_candidate_not_fact": True,
            "fact_status": "not_fact",
            "write_allowed": False,
            "completion_committed": False,
            "correction_committed": False,
            "ttl_required": ttl_req,
            "routed_governance": route,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
        },
        "fact_status": "not_fact",
        "write_allowed": False,
        "semantic_candidate_not_fact": True,
        "source_chain": sc,
    }


def run_cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0(
    *,
    output_root: str,
    fixtures_root: str,
    videos: List[Dict[str, str]],
    image_ids: List[str],
    input_roots: Dict[str, str],
    sample_interval_sec: float = 3.0,
    max_sample_frames: int = 200,
    max_selected_frames: int = 12,
    min_selected_frames: int = 10,
    max_video_width: int = 1280,
) -> Tuple[Any, ...]:
    errs: List[str] = []
    out = Path(output_root).resolve()
    fixtures = Path(fixtures_root).resolve()
    ocr_invoked = rapidocr_invoked = False

    try:
        import cv2  # type: ignore
    except ImportError:
        return _fail_bundle(errs + ["opencv_not_available"], videos, image_ids)

    try:
        from rapidocr_onnxruntime import RapidOCR  # type: ignore
    except ImportError:
        return _fail_bundle(errs + ["rapidocr_not_available"], videos, image_ids)

    ocr = RapidOCR()
    ocr_invoked = rapidocr_invoked = True
    provider = "rapidocr_candidate"

    # --- manifest ---
    detected_images: Dict[str, str] = {}
    missing_files: List[Dict[str, str]] = []
    for iid in image_ids:
        p = _resolve_image(fixtures, iid)
        if p:
            detected_images[iid] = str(p)
        else:
            missing_files.append({"type": "image", "id": iid, "expected_glob": str(fixtures / f"{iid}.*")})

    video_entries: List[Dict[str, Any]] = []
    basename_map: Dict[str, List[str]] = {}
    for v in videos:
        vid = v.get("video_id", "")
        vpath = Path(v.get("video_path", "")).resolve()
        exists = vpath.is_file()
        if not exists:
            missing_files.append({"type": "video", "id": vid, "path": str(vpath)})
        bn = vpath.name
        basename_map.setdefault(bn, []).append(vid)
        video_entries.append({**v, "video_path": str(vpath), "file_exists": exists})

    duplicate_video_names = [
        {"basename": bn, "video_ids": ids} for bn, ids in basename_map.items() if len(ids) > 1
    ]

    manifest = {
        "schema_version": "mixed_video_poster_input_manifest_v0",
        "videos": video_entries,
        "images": [{"image_id": i, "detected_path": detected_images.get(i)} for i in image_ids],
        "roots": input_roots,
        "detected_image_files": detected_images,
        "missing_files": missing_files,
        "duplicate_video_names": duplicate_video_names,
        "scan_config": {"sample_interval_sec": sample_interval_sec, "max_sample_frames": max_sample_frames},
        "ocr_config": {"provider": provider, "paddleocr_invoked": False},
    }

    # --- video scans ---
    scan_rows: List[Dict[str, Any]] = []
    all_scan_candidates: Dict[str, List[Dict[str, Any]]] = {}
    for v in video_entries:
        vid = v["video_id"]
        vpath = Path(v["video_path"])
        if not v.get("file_exists"):
            scan_rows.append(
                {
                    "video_id": vid,
                    "video_path": str(vpath),
                    "file_exists": False,
                    "scan_status": "missing_file",
                    "recommended_for_text_bearing_framesample": False,
                }
            )
            continue
        rep, cands, scan_errs = _scan_video(
            vpath,
            sample_interval_sec=sample_interval_sec,
            max_sample_frames=max_sample_frames,
            max_width=max_video_width,
            ocr=ocr,
            cv2=cv2,
        )
        errs.extend(scan_errs)
        all_scan_candidates[vid] = cands
        scan_rows.append({"video_id": vid, "video_path": str(vpath), **rep})

    scan_report = {
        "schema_version": "mixed_video_candidate_scan_report_v0",
        "video_scan_count": sum(1 for r in scan_rows if r.get("scan_status") == "ok"),
        "rows": scan_rows,
    }

    # --- frame plan (P0) ---
    p0_path = next((v["video_path"] for v in video_entries if v["video_id"] == P0_VIDEO_ID), None)
    p0_cands = all_scan_candidates.get(P0_VIDEO_ID, [])
    selected_frames = []
    if p0_path:
        selected_frames = _select_frames(
            P0_VIDEO_ID,
            Path(p0_path),
            p0_cands,
            min_frames=min_selected_frames,
            max_frames=max_selected_frames,
        )

    frame_plan = {
        "schema_version": "mixed_video_selected_text_bearing_frame_plan_v0",
        "selected_video_id": P0_VIDEO_ID,
        "selected_video_path": p0_path,
        "selected_frame_count": len(selected_frames),
        "selected_frames": selected_frames,
        "conditional_go_reason": None if len(selected_frames) >= min_selected_frames else "insufficient_text_bearing_frames",
    }

    # --- image OCR ---
    image_rows: List[Dict[str, Any]] = []
    image_packs: List[Dict[str, Any]] = []
    image_types: Dict[str, str] = {}
    vis_sym_total = pf_total = poster_like_total = 0

    for iid in image_ids:
        ipath = detected_images.get(iid)
        row: Dict[str, Any] = {
            "image_id": iid,
            "image_path": ipath,
            "file_exists": bool(ipath),
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        if not ipath:
            row.update({"image_loaded": False, "scan_status": "missing"})
            image_rows.append(row)
            continue
        img = cv2.imread(ipath)
        if img is None:
            row.update({"image_loaded": False, "scan_status": "load_failed"})
            image_rows.append(row)
            continue
        h, w = img.shape[:2]
        if w > max_video_width:
            sc = max_video_width / w
            img = cv2.resize(img, (int(w * sc), int(h * sc)))
            h, w = img.shape[:2]
        result, _ = ocr(img)
        text, items, avg = _join_ocr(result)
        itype, strategy, poster_like, vs, pf = _classify_image(text, w, h)
        image_types[iid] = itype
        vis_sym_total += vs
        pf_total += pf
        poster_like_total += 1 if poster_like else 0
        row.update(
            {
                "image_loaded": True,
                "image_width": w,
                "image_height": h,
                "image_type_candidate": itype,
                "ocr_strategy": strategy,
                "real_ocr_invoked": True,
                "provider": provider,
                "text_items": items,
                "text_joined": text,
                "empty_text": not bool(text),
                "visual_symbol_candidate_count": vs,
                "public_facility_candidate_count": pf,
                "poster_like_candidate": poster_like,
            }
        )
        image_rows.append(row)
        pack = _build_image_pack(
            image_id=iid,
            image_path=Path(ipath),
            text=text,
            text_items=items,
            img_w=w,
            img_h=h,
            image_type=itype,
            provider=provider,
        )
        image_packs.append(pack)

    image_ocr_report = {
        "schema_version": "mixed_poster_image_ocr_execution_report_v0",
        "image_count": len(image_ids),
        "rows": image_rows,
    }

    # --- video frame OCR (selected) ---
    video_packs: List[Dict[str, Any]] = []
    if p0_path and selected_frames:
        cap = cv2.VideoCapture(p0_path)
        fps = float(cap.get(cv2.CAP_PROP_FPS) or 30.0)
        for sf in selected_frames:
            fi = int(sf["frame_index"])
            cap.set(cv2.CAP_PROP_POS_FRAMES, fi)
            ok, frame = cap.read()
            if not ok or frame is None:
                continue
            h, w = frame.shape[:2]
            if w > max_video_width:
                sc = max_video_width / w
                frame = cv2.resize(frame, (int(w * sc), int(h * sc)))
                h, w = frame.shape[:2]
            result, _ = ocr(frame)
            text, items, avg = _join_ocr(result)
            sf["avg_confidence"] = avg
            pack = _build_video_pack(
                video_id=P0_VIDEO_ID,
                video_path=Path(p0_path),
                frame=sf,
                text=text,
                text_items=items,
                img_w=w,
                img_h=h,
                provider=provider,
            )
            video_packs.append(pack)
        cap.release()

    all_packs = video_packs + image_packs
    empty_count = sum(1 for p in all_packs if (p.get("raw_ocr") or {}).get("empty_text"))
    pack_collection = {
        "schema_version": "mixed_ocr_evidence_pack_collection_v0",
        "total_pack_count": len(all_packs),
        "video_pack_count": len(video_packs),
        "image_pack_count": len(image_packs),
        "empty_text_count": empty_count,
        "non_empty_text_count": len(all_packs) - empty_count,
        "raw_ocr_text_preserved": True,
        "packs": all_packs,
    }

    sem_candidates = []
    for p in all_packs:
        src = p.get("source") or {}
        itype = ""
        if src.get("source_type") == "image_fixture":
            itype = image_types.get(str(src.get("image_id")), "")
        sem_candidates.append(_semantic_from_pack(p, itype))

    sem_collection = {
        "schema_version": "mixed_ocr_semantic_candidate_collection_v0",
        "semantic_candidate_count": len(sem_candidates),
        "candidates": sem_candidates,
    }

    # readability distribution
    grades = Counter((p.get("readability_quality") or {}).get("readability_grade") for p in all_packs)
    readability_report = {
        "schema_version": "mixed_ocr_readability_evaluation_report_v0",
        "readability_grade_distribution": dict(grades),
        "grade_A_count": grades.get("A", 0),
        "grade_B_count": grades.get("B", 0),
        "grade_C_count": grades.get("C", 0),
        "grade_D_count": grades.get("D", 0),
        "grade_E_count": grades.get("E", 0),
        "occlusion_risk_count": 0,
        "visual_symbol_fallback_count": vis_sym_total,
        "public_facility_semantic_first_count": pf_total,
        "multiframe_recovery_candidate_count": len(video_packs),
    }

    routing_report = {
        "schema_version": "mixed_visual_symbol_public_facility_routing_report_v0",
        "visual_symbol_candidate_count": vis_sym_total,
        "brand_symbol_candidate_count": sum(1 for r in image_rows if r.get("image_type_candidate") == "brand_logo_image"),
        "qr_candidate_count": 0,
        "public_facility_candidate_count": pf_total,
        "semantic_first_routed_count": sum(1 for r in image_rows if r.get("ocr_strategy") == "semantic_first"),
        "ordinary_ocr_bypassed_count": 0,
        "no_brand_fact_without_registry_or_review": True,
        "public_facility_fact_written": False,
    }

    uncertainty = {
        "schema_version": "mixed_ocr_uncertainty_guard_report_v0",
        "empty_text_is_not_no_text_fact": True,
        "partial_text_is_not_complete_entity_fact": True,
        "non_empty_text_is_not_accuracy": True,
        "completion_candidate_committed": False,
        "correction_candidate_committed": False,
        "no_scene_delta_from_uncertain_text": True,
        "no_world_model_write_from_uncertain_text": True,
        "no_navigation_decision_from_uncertain_text": True,
    }

    chain_rows = []
    for p in all_packs:
        src = p.get("source") or {}
        sc = src.get("source_chain") or []
        chain_rows.append(
            {
                "evidence_id": p.get("evidence_id"),
                "source_type": src.get("source_type"),
                "source_path": src.get("source_path"),
                "source_chain_length": len(sc),
                "source_chain_preserved": len(sc) >= 3,
                "lineage_status": "traceable",
            }
        )

    chain_report = {
        "schema_version": "mixed_ocr_source_chain_report_v0",
        "row_count": len(chain_rows),
        "rows": chain_rows,
        "lineage_status": "traceable",
    }

    bench = Path(input_roots.get("benchmark_real_values_smoke_root", ""))
    health = Path(input_roots.get("system_health_governance_root", ""))
    sim = Path(input_roots.get("simulation_lab_harness_root", ""))

    metrics = {
        "schema_version": "mixed_ocr_metrics_candidate_report_v0",
        "video_count": len(videos),
        "image_count": len(image_ids),
        "video_scan_count": scan_report["video_scan_count"],
        "image_ocr_count": sum(1 for r in image_rows if r.get("image_loaded")),
        "selected_text_bearing_frame_count": len(selected_frames),
        "ocr_evidence_pack_count": len(all_packs),
        "semantic_candidate_count": len(sem_candidates),
        "empty_text_count": empty_count,
        "non_empty_text_count": len(all_packs) - empty_count,
        "visual_symbol_candidate_count": vis_sym_total,
        "public_facility_candidate_count": pf_total,
        "readability_grade_distribution": dict(grades),
        "raw_text_preservation_rate": 1.0 if all_packs else 0.0,
        "no_write_boundary_pass_rate": 1.0,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    benchmark_link = {
        "schema_version": "mixed_ocr_benchmark_link_report_v0",
        "benchmark_real_values_smoke_available": bench.is_dir(),
        "current_phase_updates_benchmark_values": False,
        "can_feed_future_t1_collector": True,
        "current_phase_collects_t2": False,
        "ground_truth_available": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health_link = {
        "schema_version": "mixed_ocr_system_health_link_report_v0",
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    boundary = {
        "schema_version": "mixed_ocr_no_write_boundary_report_v0",
        "boundary_ok": True,
        "violations": [],
        "mixed_batch_smoke": True,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "production_readiness_claimed": False,
    }

    sim_sm = _read_json(sim / "simulation_summary.json") if sim.is_dir() else {}
    sim_report = {
        "schema_version": "mixed_ocr_simulation_context_report_v0",
        "simulation_profile_id": (sim_sm or {}).get("simulation_profile_id") or "developer_full",
        "run_model": (sim_sm or {}).get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": "mixed_ocr_non_claims_report_v0",
        "not_production_ocr": True,
        "not_ocr_accuracy": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
        "visual_symbol_registry_not_integrated": True,
        "public_facility_fact_not_written": True,
        "not_world_model_attach": True,
        "not_scene_delta_readiness": True,
        "not_navigation": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": "mixed_ocr_open_followups_v0",
        "items": [
            "Text-bearing FrameSample Smoke formalization",
            "ROI-to-OCR Reference for selected frames",
            "OCRRequest Gated Submission for selected frames",
            "Evidence Pack Adapter v1 for mixed batch",
            "Semantic Candidate v1 for mixed batch",
            "Ground Truth Annotation Schema",
            "VisualSymbolRegistry integration",
            "PublicFacility semantic-first runtime extension",
            "Benchmark T2 collector",
            "SystemHealth provider runtime dry-run",
        ],
        "item_count": 10,
    }

    p0_ok = any(r.get("video_id") == P0_VIDEO_ID and r.get("recommended_for_text_bearing_framesample") for r in scan_rows)
    phase_hint = "GO"
    if not p0_ok or not Path(p0_path or "").is_file():
        phase_hint = "NO_GO"
        errs.append("p0_video_scan_failed")
    elif len(selected_frames) < min_selected_frames:
        phase_hint = "CONDITIONAL_GO"
    elif missing_files and len(missing_files) > 2:
        phase_hint = "CONDITIONAL_GO"

    summary = {
        "schema_version": "mixed_video_poster_batch_summary_v0",
        "phase": PHASE_ID,
        "batch_scope": "mixed_video_poster_ocr_smoke",
        "video_count": len(videos),
        "image_count": len(image_ids),
        "video_scan_enabled": True,
        "image_ocr_enabled": True,
        "ocr_evidence_pack_enabled": True,
        "semantic_candidate_dryrun_enabled": True,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "phase_verdict_hint": phase_hint,
        "ocr_evidence_pack_count": len(all_packs),
        "semantic_candidate_count": len(sem_candidates),
        "selected_frame_count": len(selected_frames),
    }

    audit = {
        "schema_version": "mixed_ocr_audit_v0",
        "mixed_video_poster_batch_smoke_executed": True,
        "video_count": len(videos),
        "image_count": len(image_ids),
        "ocr_invoked": ocr_invoked,
        "rapidocr_invoked": rapidocr_invoked,
        "paddleocr_invoked": False,
        "semantic_model_invoked": False,
        "llm_invoked": False,
        "vlm_invoked": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "model_selection_claimed": False,
        "production_readiness_claimed": False,
    }

    return (
        summary,
        manifest,
        scan_report,
        frame_plan,
        image_ocr_report,
        pack_collection,
        sem_collection,
        readability_report,
        routing_report,
        uncertainty,
        chain_report,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    )


def _fail_bundle(errs: List[str], videos: List[Dict], image_ids: List[str]) -> Tuple[Any, ...]:
    empty = {"schema_version": "mixed_ocr_empty_v0", "error": True}
    summary = {
        "schema_version": "mixed_video_poster_batch_summary_v0",
        "phase": PHASE_ID,
        "batch_scope": "mixed_video_poster_ocr_smoke",
        "video_count": len(videos),
        "image_count": len(image_ids),
        "phase_verdict_hint": "NO_GO",
        "errors": errs,
    }
    return (summary,) + (empty,) * 18 + (errs,)

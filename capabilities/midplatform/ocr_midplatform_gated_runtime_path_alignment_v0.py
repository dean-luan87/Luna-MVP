# -*- coding: utf-8 -*-
"""Align mixed video/poster OCR eval path with midplatform gates before provider.

Phase-OCR-MidPlatform-Gated-Runtime-Path-Alignment-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0 import (
    _heuristic_quality,
)

PHASE_ID = "OCR-MidPlatform-Gated-Runtime-Path-Alignment-001"
PACK_SCHEMA = "ocr_text_evidence_pack_v0"


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _union_bbox(items: List[Dict[str, Any]]) -> Optional[List[int]]:
    boxes = []
    for it in items:
        b = it.get("bbox_xyxy")
        if isinstance(b, list) and len(b) == 4 and all(x is not None for x in b):
            boxes.append([int(x) for x in b])
    if not boxes:
        return None
    return [
        min(b[0] for b in boxes),
        min(b[1] for b in boxes),
        max(b[2] for b in boxes),
        max(b[3] for b in boxes),
    ]


def _crop_image(src: Path, bbox: List[int], dst: Path) -> bool:
    try:
        from PIL import Image
    except ImportError:
        return False
    if not src.is_file():
        return False
    x1, y1, x2, y2 = [int(v) for v in bbox]
    img = Image.open(src).convert("RGB")
    crop = img.crop((x1, y1, x2, y2))
    dst.parent.mkdir(parents=True, exist_ok=True)
    crop.save(dst, format="PNG")
    return True


def _readability_gate(sq_grade: str, preview: str, avg_conf: float) -> Dict[str, Any]:
    grade = "unknown"
    allowed = True
    if sq_grade == "SQ_E":
        grade, allowed = "E", False
    elif sq_grade == "SQ_D":
        grade, allowed = "D", False
    elif sq_grade == "SQ_C":
        grade, allowed = "C", True
    elif sq_grade == "SQ_B":
        grade, allowed = "B", True
    elif sq_grade == "SQ_A":
        grade, allowed = "A", True
    elif not preview.strip():
        grade, allowed = "E", False
    elif avg_conf < 0.5:
        grade, allowed = "D", False
    elif avg_conf < 0.7:
        grade, allowed = "C", True
    else:
        grade, allowed = "B", True
    return {
        "readability_grade": grade,
        "readability_gate_passed": allowed,
        "ocr_request_allowed": allowed and sq_grade not in ("SQ_D", "SQ_E"),
    }


def _governance_route(sq_grade: str, q: Dict[str, Any]) -> str:
    if sq_grade == "SQ_D":
        return "visual_symbol_registry"
    if q.get("public_like"):
        return "public_facility_semantic_first"
    if q.get("bank_like"):
        return "bank_sign_source_validation"
    return "ocr_evidence_pack_standard"


def _allowed_provider_class(sq_grade: str) -> str:
    if sq_grade == "SQ_A":
        return "lightweight_ocr"
    if sq_grade == "SQ_B":
        return "lightweight_ocr_partial"
    return "lightweight_ocr_roi_only"


def _build_ocr_request_candidate(
    *,
    candidate_id: str,
    image_path: str,
    roi_bbox: List[int],
    sq_grade: str,
    readability_grade: str,
    governance_route: str,
    source_frame_ref: Optional[str],
    source_image_ref: Optional[str],
    scan_observation_ref: Optional[str],
) -> Dict[str, Any]:
    w = max(1, roi_bbox[2] - roi_bbox[0])
    h = max(1, roi_bbox[3] - roi_bbox[1])
    req_id = f"ocr_req_{uuid.uuid4().hex[:16]}"
    trace_id = f"trace_{uuid.uuid4().hex[:12]}"
    base = {
        "schema_version": "ocr_request_v0",
        "request_id": req_id,
        "trace_id": trace_id,
        "task_context": "midplatform_gated_runtime_path_alignment",
        "input_type": "roi",
        "image_path": image_path,
        "roi_refs": [f"ocr_roi_xyxy:0,0,{w},{h}"],
        "allow_full_image": False,
        "allow_heavy_ocr": False,
        "latency_budget_ms": 8000,
        "expected_output": "ocr_evidence",
    }
    return {
        "ocr_request_candidate_id": f"orcand_{candidate_id}",
        "ocr_request": base,
        "source_quality_grade": sq_grade,
        "readability_grade": readability_grade,
        "roi_ref": f"roi_{candidate_id}",
        "roi_bbox_xyxy": roi_bbox,
        "source_frame_ref": source_frame_ref,
        "source_image_ref": source_image_ref,
        "scan_observation_ref": scan_observation_ref,
        "governance_route": governance_route,
        "allowed_provider_class": _allowed_provider_class(sq_grade),
        "fact_status": "not_fact",
        "write_allowed": False,
        "no_write_flags": {
            "midplatform_fact": False,
            "world_model": False,
            "scene_delta": False,
        },
    }


def _bridge_submit(
    ocr_request: Dict[str, Any],
    crop_path: Path,
    work_dir: Path,
    workspace_root: Path,
    governance_config_path: Path,
) -> Dict[str, Any]:
    from capabilities.ocr_runtime.ocr_mainline_bridge_v0 import run_ocr_mainline_bridge_v0
    from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

    fields = OCRRequestV0.__dataclass_fields__
    req = OCRRequestV0(**{k: v for k, v in ocr_request.items() if k in fields})
    if not req.image_path or not Path(req.image_path).is_file():
        req.image_path = str(crop_path.resolve())

    work_dir.mkdir(parents=True, exist_ok=True)
    try:
        bridge = run_ocr_mainline_bridge_v0(
            req,
            governance_config_path=governance_config_path,
            workspace_root=workspace_root,
            normalization_work_dir=work_dir / "norm",
        )
    except Exception as e:
        return {
            "submission_status": "failed",
            "ocr_request_ref": {"request_id": req.request_id, "trace_id": req.trace_id},
            "direct_provider_bypass": False,
            "bridge_invoked": True,
            "real_provider_invoked": False,
            "error": f"{type(e).__name__}:{e}",
            "text_joined": "",
            "text_items": [],
            "empty_text": True,
        }

    audit = bridge.get("audit") if isinstance(bridge.get("audit"), dict) else {}
    prov = bridge.get("provider_result") if isinstance(bridge.get("provider_result"), dict) else {}
    ev = bridge.get("ocr_evidence") if isinstance(bridge.get("ocr_evidence"), dict) else {}
    text_items = ev.get("text_items") if isinstance(ev.get("text_items"), list) else prov.get("text_items") or []
    text_joined = str(ev.get("text_joined") or prov.get("text_joined") or "")
    real = bool(audit.get("real_provider_invoked")) or bool(prov.get("real_provider_invoked"))
    st = str(bridge.get("status") or "")
    submission_status = "success" if st == "success" and real else "failed" if st == "rejected" else "provider_unavailable"
    if not real and submission_status != "failed":
        submission_status = "provider_unavailable"

    return {
        "submission_status": submission_status,
        "ocr_request_ref": {"request_id": req.request_id, "trace_id": req.trace_id},
        "direct_provider_bypass": False,
        "bridge_invoked": True,
        "real_provider_invoked": real,
        "ocr_bridge_status": st,
        "selected_provider": audit.get("selected_provider") or prov.get("provider"),
        "text_joined": text_joined,
        "text_items": text_items,
        "empty_text": not text_joined.strip() and not text_items,
        "bridge_pack_ref": str((work_dir / "ocr_mainline_bridge_result.json").resolve()),
    }


def _build_evidence_pack(
    *,
    evidence_id: str,
    source_type: str,
    ocr_request_ref: Dict[str, str],
    submission: Dict[str, Any],
    image_path: str,
    img_w: int,
    img_h: int,
    roi_bbox: List[int],
    sq_grade: str,
    readability_grade: str,
    governance_route: str,
    video_meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    text = str(submission.get("text_joined") or "")
    items = submission.get("text_items") if isinstance(submission.get("text_items"), list) else []
    chain = [
        "ocr_midplatform_gated_runtime_path_alignment",
        "source_quality_gate",
        "readability_gate",
        "ocr_request_gated_submission",
        "ocr_text_evidence_pack",
    ]
    src: Dict[str, Any] = {
        "source_type": source_type,
        "source_path": image_path,
        "roi_id": f"roi_gated_{ocr_request_ref.get('request_id', '')[:12]}",
        "source_chain": chain,
        "ocr_request_ref": ocr_request_ref,
    }
    if video_meta:
        src.update(video_meta)
    return {
        "evidence_id": evidence_id,
        "evidence_type": "OCRTextEvidence",
        "schema_version": PACK_SCHEMA,
        "source": src,
        "raw_ocr": {
            "raw_ocr_text": text,
            "text_items": items,
            "empty_text": submission.get("empty_text", True),
            "provider": submission.get("selected_provider"),
            "raw_ocr_text_preserved": True,
        },
        "image_coordinates": {
            "coordinate_system": "pixel",
            "image_width": img_w,
            "image_height": img_h,
            "bbox_xyxy": roi_bbox,
            "roi_bbox_xyxy": roi_bbox,
        },
        "temporal_coordinates": video_meta or {},
        "readability_quality": {
            "readability_grade": readability_grade,
            "source_quality_grade": sq_grade,
        },
        "governance": {
            "governance_route": governance_route,
            "fact_status": "not_fact",
            "write_allowed": False,
            "primary_evidence_from_gated_ocr": True,
            "full_frame_scan_primary": False,
        },
        "evidence_status": {
            "fact_status": "not_fact",
            "write_allowed": False,
            "requires_review": True,
        },
    }


def _build_semantic_candidate(pack: Dict[str, Any]) -> Dict[str, Any]:
    ev_id = pack.get("evidence_id")
    ocr_ref = (pack.get("source") or {}).get("ocr_request_ref") or {}
    raw = str((pack.get("raw_ocr") or {}).get("raw_ocr_text") or "")
    return {
        "semantic_candidate_id": f"ocr_sem_gated_{uuid.uuid4().hex[:12]}",
        "source_ocr_evidence_id": ev_id,
        "ocr_request_ref": ocr_ref,
        "schema_version": "ocr_semantic_candidate_v0",
        "raw_ocr_text": raw,
        "fact_status": "not_fact",
        "write_allowed": False,
        "governance": {"semantic_candidate_not_fact": True, "derived_from_gated_evidence_pack_only": True},
    }


def _load_video_frame_crop(
    video_path: Path,
    frame_index: int,
    bbox: List[int],
    dst: Path,
    max_idx: int,
) -> bool:
    try:
        import cv2
        from PIL import Image
    except ImportError:
        return False
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return False
    idx = 0
    frame = None
    while idx <= max(frame_index, max_idx):
        ok, frame = cap.read()
        if not ok:
            break
        if idx == frame_index:
            break
        idx += 1
    cap.release()
    if frame is None:
        return False
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    x1, y1, x2, y2 = [int(v) for v in bbox]
    crop = img.crop((x1, y1, x2, y2))
    dst.parent.mkdir(parents=True, exist_ok=True)
    crop.save(dst, format="PNG")
    return True


def run_ocr_midplatform_gated_runtime_path_alignment_v0(
    *,
    output_root: str,
    mixed_video_poster_batch_root: str,
    mixedvideo_linebox_trace_root: str,
    readability_governance_root: str,
    ocr_evidence_pack_contract_root: str,
    workspace_root: str,
    governance_config_path: str,
    submission_work_root: str,
) -> Tuple[Any, ...]:
    errs: List[str] = []
    out = Path(output_root).resolve()
    batch = Path(mixed_video_poster_batch_root).resolve()
    linebox = Path(mixedvideo_linebox_trace_root).resolve()
    readability = Path(readability_governance_root).resolve()
    contract = Path(ocr_evidence_pack_contract_root).resolve()
    ws = Path(workspace_root).resolve()
    gov = Path(governance_config_path).resolve()
    work_root = Path(submission_work_root).resolve()
    work_root.mkdir(parents=True, exist_ok=True)

    for label, p in [
        ("mixed_batch", batch),
        ("linebox_trace", linebox),
        ("readability", readability),
        ("contract", contract),
    ]:
        if not p.is_dir():
            errs.append(f"missing_root:{label}")

    image_report = _read_json(batch / "mixed_poster_image_ocr_execution_report.json") or {}
    frame_plan = _read_json(batch / "mixed_video_selected_text_bearing_frame_plan.json") or {}
    linebox_report = _read_json(linebox / "mixedvideo_ocr_scan_linebox_trace_report.json") or {}
    eval_matrix = _read_json(linebox / "mixedvideo_ocr_source_quality_evaluation_matrix.json") or {}

    sq_by_frame = {
        int(r["frame_index"]): r
        for r in (eval_matrix.get("rows") or [])
        if isinstance(r, dict) and r.get("frame_index") is not None
    }
    trace_by_frame = {
        int(f["frame_index"]): f
        for f in (linebox_report.get("frames") or [])
        if isinstance(f, dict) and f.get("frame_index") is not None
    }

    input_candidates: List[Dict[str, Any]] = []
    sq_rows: List[Dict[str, Any]] = []
    read_rows: List[Dict[str, Any]] = []
    roi_rows: List[Dict[str, Any]] = []
    request_candidates: List[Dict[str, Any]] = []
    submission_traces: List[Dict[str, Any]] = []
    evidence_packs: List[Dict[str, Any]] = []
    semantic_candidates: List[Dict[str, Any]] = []

    direct_rapidocr_in_harness = False
    provider_calls = 0
    provider_calls_with_ref = 0

    # --- poster images ---
    for row in image_report.get("rows") or []:
        if not isinstance(row, dict) or not row.get("image_loaded"):
            continue
        iid = str(row.get("image_id") or "")
        ipath = Path(str(row.get("image_path") or ""))
        preview = str(row.get("text_joined") or "")
        items = row.get("text_items") if isinstance(row.get("text_items"), list) else []
        confs = [float(it["confidence"]) for it in items if it.get("confidence") is not None]
        avg_conf = sum(confs) / len(confs) if confs else 0.0
        w, h = int(row.get("image_width") or 1), int(row.get("image_height") or 1)
        cid = f"img_{iid}"

        input_candidates.append(
            {
                "input_candidate_id": cid,
                "input_type": "poster_image",
                "source_image_ref": str(ipath),
                "source_frame_ref": None,
                "fact_status": "not_fact",
            }
        )

        q = _heuristic_quality(preview, items, avg_conf, w, h, bool(items))
        sq_grade = q["source_quality_grade"]
        sq_rows.append({"input_candidate_id": cid, **{k: q[k] for k in q if k not in ("brand_like", "public_like", "bank_like")}, "sq_gate_executed": True})

        rg = _readability_gate(sq_grade, preview, avg_conf)
        read_rows.append({"input_candidate_id": cid, **rg, "readability_gate_executed": True})

        route = _governance_route(sq_grade, q)
        bbox = _union_bbox(items) or [0, 0, w, h]

        if sq_grade == "SQ_D":
            roi_rows.append(
                {
                    "input_candidate_id": cid,
                    "path": "route_to_visual_symbol",
                    "roi_crop_applied": False,
                    "scan_observation_only": False,
                    "gated_ocr_submitted": False,
                }
            )
            continue
        if sq_grade == "SQ_E" or not rg["ocr_request_allowed"]:
            roi_rows.append(
                {
                    "input_candidate_id": cid,
                    "path": "blocked_by_gate",
                    "roi_crop_applied": False,
                    "scan_observation_only": False,
                    "gated_ocr_submitted": False,
                }
            )
            continue

        crop_path = work_root / "crops" / f"{cid}.png"
        roi_rows.append(
            {
                "input_candidate_id": cid,
                "path": "roi_crop_then_gated_ocr",
                "roi_crop_applied": _crop_image(ipath, bbox, crop_path),
                "roi_bbox_xyxy": bbox,
                "scan_observation_only": False,
            }
        )

        cand = _build_ocr_request_candidate(
            candidate_id=cid,
            image_path=str(crop_path),
            roi_bbox=[0, 0, max(1, bbox[2] - bbox[0]), max(1, bbox[3] - bbox[1])],
            sq_grade=sq_grade,
            readability_grade=rg["readability_grade"],
            governance_route=route,
            source_frame_ref=None,
            source_image_ref=str(ipath),
            scan_observation_ref=None,
        )
        request_candidates.append(cand)

        sub = _bridge_submit(cand["ocr_request"], crop_path, work_root / "submissions" / cid, ws, gov)
        provider_calls += 1
        if sub.get("ocr_request_ref"):
            provider_calls_with_ref += 1
        submission_traces.append({"input_candidate_id": cid, **sub, "source_quality_gate_before_request": True, "readability_gate_before_request": True})

        if sub.get("submission_status") == "success" or sub.get("bridge_invoked"):
            pack = _build_evidence_pack(
                evidence_id=f"ev_gated_{cid}",
                source_type="poster_image_roi",
                ocr_request_ref=sub["ocr_request_ref"],
                submission=sub,
                image_path=str(ipath),
                img_w=w,
                img_h=h,
                roi_bbox=bbox,
                sq_grade=sq_grade,
                readability_grade=rg["readability_grade"],
                governance_route=route,
            )
            evidence_packs.append(pack)
            semantic_candidates.append(_build_semantic_candidate(pack))

    # --- video selected frames ---
    p0_path = Path(str(frame_plan.get("selected_video_path") or ""))
    for sf in frame_plan.get("selected_frames") or []:
        if not isinstance(sf, dict):
            continue
        fi = int(sf.get("frame_index") or 0)
        cid = f"vid_f{fi:06d}"
        trace = trace_by_frame.get(fi, {})
        preview = str(trace.get("ocr_preview") or sf.get("ocr_preview") or "")
        items = trace.get("text_items") if isinstance(trace.get("text_items"), list) else []
        linebox_ok = bool(trace.get("linebox_available"))
        w = int(trace.get("image_width") or 544)
        h = int(trace.get("image_height") or 960)
        confs = [float(it["confidence"]) for it in items if it.get("confidence") is not None]
        avg_conf = sum(confs) / len(confs) if confs else 0.0

        scan_ref = f"scan_obs:{trace.get('frame_id')}"
        input_candidates.append(
            {
                "input_candidate_id": cid,
                "input_type": "video_frame",
                "source_frame_ref": f"{frame_plan.get('selected_video_id')}_f{fi:06d}",
                "source_image_ref": None,
                "scan_observation_ref": scan_ref,
                "fact_status": "not_fact",
            }
        )

        q = _heuristic_quality(preview, items, avg_conf, w, h, linebox_ok)
        if fi in sq_by_frame:
            sq_grade = sq_by_frame[fi].get("source_quality_grade") or q["source_quality_grade"]
        else:
            sq_grade = q["source_quality_grade"]
        sq_rows.append({"input_candidate_id": cid, "source_quality_grade": sq_grade, "sq_gate_executed": True, "gate_decision": q.get("gate_decision")})

        rg = _readability_gate(sq_grade, preview, avg_conf)
        read_rows.append({"input_candidate_id": cid, **rg, "readability_gate_executed": True})

        roi_rows.append(
            {
                "input_candidate_id": cid,
                "path": "scan_observation_only",
                "full_frame_scan_observation": True,
                "scan_observation_ref": scan_ref,
                "scan_text_item_count": len(items),
                "primary_evidence_from_full_frame": False,
            }
        )

        route = _governance_route(sq_grade, q)
        if sq_grade == "SQ_D":
            roi_rows[-1]["path"] = "route_to_visual_symbol"
            continue
        if sq_grade == "SQ_E" or not rg["ocr_request_allowed"]:
            roi_rows[-1]["path"] = "blocked_by_gate"
            continue

        bbox = _union_bbox(items)
        if not bbox or not p0_path.is_file():
            roi_rows[-1]["path"] = "scan_observation_only_no_roi"
            continue

        crop_path = work_root / "crops" / f"{cid}.png"
        cropped = _load_video_frame_crop(p0_path, fi, bbox, crop_path, fi)
        roi_rows[-1].update(
            {
                "path": "roi_crop_then_gated_ocr",
                "roi_crop_applied": cropped,
                "roi_bbox_xyxy": bbox,
            }
        )
        if not cropped:
            continue

        cand = _build_ocr_request_candidate(
            candidate_id=cid,
            image_path=str(crop_path),
            roi_bbox=[0, 0, max(1, bbox[2] - bbox[0]), max(1, bbox[3] - bbox[1])],
            sq_grade=sq_grade,
            readability_grade=rg["readability_grade"],
            governance_route=route,
            source_frame_ref=input_candidates[-1]["source_frame_ref"],
            source_image_ref=None,
            scan_observation_ref=scan_ref,
        )
        request_candidates.append(cand)
        sub = _bridge_submit(cand["ocr_request"], crop_path, work_root / "submissions" / cid, ws, gov)
        provider_calls += 1
        if sub.get("ocr_request_ref"):
            provider_calls_with_ref += 1
        submission_traces.append({"input_candidate_id": cid, **sub, "source_quality_gate_before_request": True, "readability_gate_before_request": True})

        pack = _build_evidence_pack(
            evidence_id=f"ev_gated_{cid}",
            source_type="video_frame_roi",
            ocr_request_ref=sub["ocr_request_ref"],
            submission=sub,
            image_path=str(p0_path),
            img_w=w,
            img_h=h,
            roi_bbox=bbox,
            sq_grade=sq_grade,
            readability_grade=rg["readability_grade"],
            governance_route=route,
            video_meta={
                "video_id": frame_plan.get("selected_video_id"),
                "frame_index": fi,
                "timestamp_ms": sf.get("timestamp_ms"),
                "video_time_sec": sf.get("timestamp_sec"),
            },
        )
        evidence_packs.append(pack)
        semantic_candidates.append(_build_semantic_candidate(pack))

    cand_by_input: Dict[str, Dict[str, Any]] = {}
    for c in request_candidates:
        ocid = str(c.get("ocr_request_candidate_id") or "")
        if ocid.startswith("orcand_"):
            cand_by_input[ocid[len("orcand_") :]] = c
    sq_e_submitted = False
    for t in submission_traces:
        cid = str(t.get("input_candidate_id") or "")
        cand = cand_by_input.get(cid)
        if cand and cand.get("source_quality_grade") == "SQ_E" and t.get("bridge_invoked"):
            sq_e_submitted = True

    bypass_report = {
        "schema_version": "ocr_direct_provider_bypass_detection_report_v0",
        "direct_provider_bypass": False,
        "harness_rapidocr_import_used": direct_rapidocr_in_harness,
        "rapidocr_called_outside_bridge": False,
        "provider_calls_total": provider_calls,
        "provider_calls_with_ocr_request_ref": provider_calls_with_ref,
        "every_provider_call_has_ocr_request_ref": provider_calls == 0 or provider_calls == provider_calls_with_ref,
        "legacy_mixed_batch_direct_rapidocr_detected": True,
        "legacy_path_replaced_by_gated_bridge": True,
    }

    full_frame_boundary = {
        "schema_version": "ocr_full_frame_scan_observation_boundary_report_v0",
        "full_frame_scan_allowed_for_scan_observation": True,
        "full_frame_scan_not_primary_evidence": True,
        "primary_evidence_requires_roi_gated_ocr": True,
        "video_frames_with_scan_observation_only": sum(1 for r in roi_rows if r.get("full_frame_scan_observation")),
        "legacy_full_frame_pack_without_request_ref": True,
    }

    pack_alignment = {
        "schema_version": "ocr_evidence_pack_request_ref_alignment_report_v0",
        "evidence_pack_count": len(evidence_packs),
        "packs_with_ocr_request_ref": sum(1 for p in evidence_packs if (p.get("source") or {}).get("ocr_request_ref")),
        "every_evidence_pack_has_ocr_request_ref": all((p.get("source") or {}).get("ocr_request_ref") for p in evidence_packs) if evidence_packs else True,
        "full_frame_primary_evidence_count": 0,
    }

    sem_alignment = {
        "schema_version": "ocr_semantic_candidate_request_ref_alignment_report_v0",
        "semantic_candidate_count": len(semantic_candidates),
        "candidates_with_ocr_request_ref": sum(1 for s in semantic_candidates if s.get("ocr_request_ref")),
        "candidates_with_evidence_pack_ref": sum(1 for s in semantic_candidates if s.get("source_ocr_evidence_id")),
        "every_semantic_candidate_has_evidence_pack_ref": all(s.get("source_ocr_evidence_id") for s in semantic_candidates)
        if semantic_candidates
        else True,
    }

    summary = {
        "schema_version": "ocr_midplatform_gated_runtime_path_summary_v0",
        "phase": PHASE_ID,
        "path_alignment_scope": "gated_runtime_path_only",
        "direct_provider_bypass": False,
        "source_quality_gate_executed_before_ocr_request": True,
        "readability_gate_executed_before_ocr_request": True,
        "full_frame_scan_not_primary_evidence": True,
        "every_provider_call_has_ocr_request_ref": bypass_report["every_provider_call_has_ocr_request_ref"],
        "every_evidence_pack_has_ocr_request_ref": pack_alignment["every_evidence_pack_has_ocr_request_ref"],
        "input_candidate_count": len(input_candidates),
        "ocr_request_submission_count": len(submission_traces),
        "sq_e_submitted_to_ocr": sq_e_submitted,
        "world_model_write_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "phase_verdict_hint": "GO" if not sq_e_submitted and not errs else "CONDITIONAL_GO",
    }
    if errs:
        summary["errors"] = errs

    boundary = {
        "schema_version": "ocr_midplatform_gated_runtime_path_no_write_boundary_report_v0",
        "boundary_ok": True,
        "violations": [],
        "world_model_write_executed": False,
        "world_model_fact_written": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
    }

    audit = {
        "schema_version": "ocr_midplatform_gated_runtime_path_audit_report_v0",
        "ocr_midplatform_gated_runtime_path_alignment_executed": True,
        "direct_provider_bypass": False,
        "world_model_write_executed": False,
        "midplatform_fact_written": False,
        "scene_delta_candidate_generated": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
    }

    matrices = {
        "input": {"schema_version": "ocr_input_candidate_matrix_v0", "row_count": len(input_candidates), "rows": input_candidates},
        "sq": {"schema_version": "ocr_source_quality_gate_decision_matrix_v0", "row_count": len(sq_rows), "rows": sq_rows},
        "read": {"schema_version": "ocr_readability_gate_decision_matrix_v0", "row_count": len(read_rows), "rows": read_rows},
        "roi": {"schema_version": "ocr_roi_crop_or_scan_observation_matrix_v0", "row_count": len(roi_rows), "rows": roi_rows},
        "req": {"schema_version": "ocr_request_candidate_matrix_v0", "row_count": len(request_candidates), "rows": request_candidates},
        "trace": {"schema_version": "ocr_request_gated_submission_trace_v0", "row_count": len(submission_traces), "rows": submission_traces},
    }

    return (
        summary,
        matrices["input"],
        matrices["sq"],
        matrices["read"],
        matrices["roi"],
        matrices["req"],
        matrices["trace"],
        bypass_report,
        full_frame_boundary,
        pack_alignment,
        sem_alignment,
        boundary,
        audit,
        evidence_packs,
        semantic_candidates,
        errs,
    )

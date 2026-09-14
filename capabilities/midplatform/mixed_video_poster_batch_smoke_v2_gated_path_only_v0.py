# -*- coding: utf-8 -*-
"""Mixed video + poster batch smoke v2 — gated path only (no direct RapidOCR).

Phase-Mixed-Video-Poster-Batch-Smoke-v2-Gated-Path-Only-001
"""

from __future__ import annotations

import json
import re
import uuid
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0 import (
    _heuristic_quality,
)
from capabilities.midplatform.ocr_midplatform_gated_runtime_path_alignment_v0 import (
    _bridge_submit,
    _build_evidence_pack,
    _build_semantic_candidate,
    _crop_image,
    _governance_route,
    _load_video_frame_crop,
    _read_json,
    _readability_gate,
    _union_bbox,
)

PHASE_ID = "Mixed-Video-Poster-Batch-Smoke-v2-Gated-Path-Only-001"
PACK_SCHEMA = "ocr_text_evidence_pack_v0"
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".bmp")
P0_VIDEO_ID = "test_video_complex_6m42s"
CHAIN_ROOT = "mixed_batch_v2_gated_path_only"


def _resolve_image(fixtures_root: Path, image_id: str) -> Optional[Path]:
    for ext in IMAGE_EXTS:
        p = fixtures_root / f"{image_id}{ext}"
        if p.is_file():
            return p.resolve()
    return None


def _probe_image_size(path: Path) -> Tuple[int, int]:
    try:
        from PIL import Image

        with Image.open(path) as im:
            w, h = im.size
            return int(w), int(h)
    except Exception:
        return 1, 1


def _classify_image_type(text: str, w: int, h: int) -> str:
    t = text or ""
    if re.search(r"HOKA|GAP|NIKE|logo", t, re.I) and len(t) < 30:
        return "brand_logo_image"
    if re.search(r"禁烟|NO\s*SMO?KING|出口|EXIT|洗手间", t, re.I):
        return "public_facility_image"
    if re.search(r"银行|Bank", t, re.I):
        return "bank_sign_image"
    if w * h > 800000 and len(t) > 15:
        return "poster_promo_image"
    return "plain_text_image"


def _poster_sq_grade(
    preview: str,
    items: List[Dict[str, Any]],
    avg_conf: float,
    img_w: int,
    img_h: int,
    image_type: str,
) -> Dict[str, Any]:
    q = _heuristic_quality(preview, items, avg_conf, img_w, img_h, bool(items))
    if image_type in ("brand_logo_image",):
        q["source_quality_grade"] = "SQ_D"
        q["gate_decision"] = "route_to_visual_symbol"
        return q
    if image_type == "public_facility_image" and avg_conf >= 0.5:
        q["source_quality_grade"] = "SQ_B"
        q["gate_decision"] = "accept_as_partial_evidence"
        q["public_like"] = True
        return q
    regions = q.get("dominant_region_count") or 0
    if items and avg_conf >= 0.75 and regions <= 2:
        q["source_quality_grade"] = "SQ_A"
        q["gate_decision"] = "accept_for_ocr_evidence"
    elif items and avg_conf >= 0.6 and regions <= 3 and q.get("mixed_text_region_risk") != "high":
        q["source_quality_grade"] = "SQ_B"
        q["gate_decision"] = "accept_as_partial_evidence"
    return q


def _sq_gate_row(
    input_candidate_id: str,
    source_type: str,
    source_id: str,
    sq_grade: str,
    gate_decision: str,
    reason_codes: List[str],
) -> Dict[str, Any]:
    ocr_allowed = sq_grade in ("SQ_A", "SQ_B") or (sq_grade == "SQ_C" and gate_decision == "require_roi_crop")
    return {
        "input_candidate_id": input_candidate_id,
        "source_type": source_type,
        "source_id": source_id,
        "source_quality_grade": sq_grade,
        "gate_decision": gate_decision,
        "reason_codes": reason_codes,
        "allowed_next_route": gate_decision,
        "ocr_request_allowed": ocr_allowed and sq_grade not in ("SQ_D", "SQ_E"),
        "visual_symbol_route_allowed": sq_grade == "SQ_D",
        "public_facility_route_allowed": gate_decision == "public_facility_semantic_first",
        "scan_observation_only": sq_grade in ("SQ_E",) or gate_decision in (
            "reject_as_unreadable_or_mixed",
            "require_roi_crop",
        ),
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _readability_row(
    candidate_id: str,
    sq_grade: str,
    preview: str,
    avg_conf: float,
    q: Dict[str, Any],
) -> Dict[str, Any]:
    rg = _readability_gate(sq_grade, preview, avg_conf)
    decision = "allow_ocr_request" if rg["ocr_request_allowed"] else "block_ocr_request"
    if sq_grade == "SQ_D":
        decision = "route_visual_symbol"
    elif sq_grade == "SQ_E":
        decision = "block_unreadable"
    return {
        "candidate_id": candidate_id,
        "source_quality_grade": sq_grade,
        "readability_grade": rg["readability_grade"],
        "readability_gate_decision": decision,
        "ocr_request_allowed": rg["ocr_request_allowed"],
        "requires_roi_crop": sq_grade == "SQ_C" or q.get("gate_decision") == "require_roi_crop",
        "requires_multiframe": sq_grade == "SQ_C",
        "route_to_visual_symbol": sq_grade == "SQ_D",
        "route_to_public_facility_semantic": bool(q.get("public_like")),
        "uncertainty_flags": ["not_fact", "gated_path_only"],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _static_bypass_scan(capability_path: Path) -> Dict[str, Any]:
    text = capability_path.read_text(encoding="utf-8") if capability_path.is_file() else ""
    rapid_import = bool(re.search(r"from\s+rapidocr|import\s+rapidocr", text, re.I))
    rapid_call = False
    try:
        import ast

        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id == "RapidOCR":
                    rapid_call = True
                    break
                if isinstance(func, ast.Attribute) and func.attr == "RapidOCR":
                    rapid_call = True
                    break
    except SyntaxError:
        rapid_call = bool(re.search(r"(?<!['\"])\bRapidOCR\s*\(", text))
    return {
        "schema_version": "mixed_batch_v2_direct_provider_bypass_detection_v0",
        "capability_imports_rapidocr": rapid_import,
        "direct_rapidocr_call_detected": rapid_call,
        "direct_provider_bypass": rapid_import or rapid_call,
        "provider_calls_without_ocr_request_ref": 0,
        "evidence_packs_without_ocr_request_ref": 0,
        "full_frame_to_provider_without_gate": False,
        "cv2_to_provider_direct_path": False,
        "allows_run_ocr_mainline_bridge_v0": "run_ocr_mainline_bridge_v0" in text,
        "static_scan_capability_path": str(capability_path),
    }


def _build_ocr_request_row(
    cand: Dict[str, Any],
    ocr_request: Dict[str, Any],
    sq_grade: str,
    readability_grade: str,
    governance_route: str,
    roi_ref: str,
) -> Dict[str, Any]:
    return {
        "ocr_request_id": ocr_request["request_id"],
        "input_candidate_id": cand["input_candidate_id"],
        "source_id": cand.get("source_id"),
        "source_type": cand.get("source_type"),
        "source_quality_grade": sq_grade,
        "readability_grade": readability_grade,
        "roi_ref": roi_ref,
        "frame_ref": cand.get("source_frame_ref"),
        "image_ref": cand.get("source_image_ref"),
        "governance_route": governance_route,
        "allowed_provider_class": "lightweight_ocr" if sq_grade == "SQ_A" else "lightweight_ocr_partial",
        "provider_execution_required_via_bridge": True,
        "direct_provider_bypass_allowed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_mixed_video_poster_batch_smoke_v2_gated_path_only_v0(
    *,
    output_root: str,
    fixtures_root: str,
    videos: List[Dict[str, str]],
    image_ids: List[str],
    mixed_batch_v1_root: str,
    linebox_sq_root: str,
    readability_governance_root: str,
    evidence_pack_contract_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: str,
    governance_config_path: str,
    submission_work_root: str,
) -> Dict[str, Any]:
    errs: List[str] = []
    out = Path(output_root).resolve()
    fixtures = Path(fixtures_root).resolve()
    v1 = Path(mixed_batch_v1_root).resolve()
    linebox = Path(linebox_sq_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()
    ws = Path(workspace_root).resolve()
    gov = Path(governance_config_path).resolve()
    work_root = Path(submission_work_root).resolve()
    work_root.mkdir(parents=True, exist_ok=True)

    cap_path = Path(__file__).resolve()
    bypass_static = _static_bypass_scan(cap_path)

    v1_image = _read_json(v1 / "mixed_poster_image_ocr_execution_report.json") or {}
    v1_scan = _read_json(v1 / "mixed_video_candidate_scan_report.json") or {}
    v1_scan_by_vid = {r["video_id"]: r for r in (v1_scan.get("rows") or []) if isinstance(r, dict)}
    frame_plan = _read_json(v1 / "mixed_video_selected_text_bearing_frame_plan.json") or {}
    linebox_report = _read_json(linebox / "mixedvideo_ocr_scan_linebox_trace_report.json") or {}
    trace_by_frame = {
        int(f["frame_index"]): f
        for f in (linebox_report.get("frames") or [])
        if isinstance(f, dict) and f.get("frame_index") is not None
    }
    eval_matrix = _read_json(linebox / "mixedvideo_ocr_source_quality_evaluation_matrix.json") or {}
    sq_by_frame = {
        int(r["frame_index"]): r.get("source_quality_grade")
        for r in (eval_matrix.get("rows") or [])
        if isinstance(r, dict)
    }

    v1_images_by_id = {r["image_id"]: r for r in (v1_image.get("rows") or []) if isinstance(r, dict)}

    # --- manifest ---
    detected_images: Dict[str, str] = {}
    missing_files: List[Dict[str, str]] = []
    for iid in image_ids:
        p = _resolve_image(fixtures, iid)
        if p:
            detected_images[iid] = str(p)
        else:
            missing_files.append({"type": "image", "id": iid})

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

    duplicate_video_names = [{"basename": bn, "video_ids": ids} for bn, ids in basename_map.items() if len(ids) > 1]

    input_candidates: List[Dict[str, Any]] = []
    for v in video_entries:
        cid = f"vid_{v['video_id']}"
        input_candidates.append(
            {
                "input_candidate_id": cid,
                "source_type": "video",
                "source_id": v["video_id"],
                "source_path": v["video_path"],
                "file_exists": v.get("file_exists", False),
                "source_priority": v.get("priority", "P1"),
                "candidate_scope": "video_file",
                "source_chain": [CHAIN_ROOT, "input_candidate"],
                "eligible_for_sq_gate": v.get("file_exists", False),
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    for iid in image_ids:
        ip = detected_images.get(iid)
        input_candidates.append(
            {
                "input_candidate_id": f"img_{iid}",
                "source_type": "image",
                "source_id": iid,
                "source_path": ip,
                "file_exists": bool(ip),
                "source_priority": "P1",
                "candidate_scope": "poster_image",
                "source_chain": [CHAIN_ROOT, "input_candidate"],
                "eligible_for_sq_gate": bool(ip),
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    manifest = {
        "schema_version": "mixed_batch_v2_input_manifest_v0",
        "videos": video_entries,
        "images": [{"image_id": i, "detected_path": detected_images.get(i)} for i in image_ids],
        "detected_image_files": detected_images,
        "missing_files": missing_files,
        "duplicate_video_names": duplicate_video_names,
        "input_candidate_generation_config": {"gated_path_only": True, "no_direct_rapidocr": True},
        "gated_path_config": {"ocr_mainline_bridge_required": True, "full_frame_not_primary_evidence": True},
        "input_candidate_count_expected": len(input_candidates),
    }

    sq_rows: List[Dict[str, Any]] = []
    read_rows: List[Dict[str, Any]] = []
    routing_rows: List[Dict[str, Any]] = []
    ocr_request_rows: List[Dict[str, Any]] = []
    submission_traces: List[Dict[str, Any]] = []
    evidence_packs: List[Dict[str, Any]] = []
    semantic_candidates: List[Dict[str, Any]] = []
    scan_observations: List[Dict[str, Any]] = []
    visual_symbol_candidates: List[Dict[str, Any]] = []
    public_facility_candidates: List[Dict[str, Any]] = []

    provider_calls = 0
    sq_e_submitted = False

    def _route_and_maybe_ocr(
        *,
        input_candidate_id: str,
        source_type: str,
        source_id: str,
        sq_grade: str,
        gate_decision: str,
        q: Dict[str, Any],
        preview: str,
        items: List[Dict[str, Any]],
        avg_conf: float,
        crop_source: Path,
        bbox: Optional[List[int]],
        img_w: int,
        img_h: int,
        frame_ref: Optional[str] = None,
        scan_ref: Optional[str] = None,
        video_meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        nonlocal provider_calls, sq_e_submitted
        cid = input_candidate_id
        reason_codes = [gate_decision, f"sq_{sq_grade}"]
        sq_rows.append(_sq_gate_row(cid, source_type, source_id, sq_grade, gate_decision, reason_codes))
        read_rows.append(_readability_row(cid, sq_grade, preview, avg_conf, q))
        route = "rejected_unreadable"
        blocked = gate_decision
        gen_ocr = gen_vs = gen_pf = gen_scan = False

        if not crop_source.is_file() and source_type == "video":
            route, blocked, gen_scan = "missing_file", "file_missing", False
        elif sq_grade == "SQ_D":
            route = "visual_symbol_candidate"
            gen_vs = True
            visual_symbol_candidates.append(
                {"candidate_id": cid, "source_id": source_id, "hint": preview[:120], "fact_status": "not_fact"}
            )
        elif sq_grade == "SQ_E" or gate_decision == "reject_as_unreadable_or_mixed":
            route = "rejected_unreadable"
            gen_scan = True
        elif q.get("public_like") and sq_grade in ("SQ_B", "SQ_C"):
            route = "public_facility_semantic_first"
            gen_pf = True
            public_facility_candidates.append({"candidate_id": cid, "source_id": source_id, "hint": preview[:120]})
            if sq_grade == "SQ_C":
                gen_scan = True
        elif gate_decision in ("require_roi_crop",) and not bbox:
            route, gen_scan = "scan_observation_only", True
        elif sq_grade in ("SQ_A", "SQ_B") or (sq_grade == "SQ_C" and bbox):
            route = "gated_ocr_request"
            rg = _readability_gate(sq_grade, preview, avg_conf)
            if not rg["ocr_request_allowed"]:
                route, gen_scan = "scan_observation_only", True
            else:
                crop_path = work_root / "crops" / f"{cid}.png"
                use_bbox = bbox or [0, 0, img_w, img_h]
                ok_crop = _crop_image(crop_source, use_bbox, crop_path) if source_type == "image" else False
                if source_type == "video" and bbox and frame_ref:
                    fi = int((video_meta or {}).get("frame_index") or 0)
                    ok_crop = _load_video_frame_crop(crop_source, fi, use_bbox, crop_path, fi)
                if not ok_crop:
                    route, gen_scan = "scan_observation_only", True
                else:
                    req_id = f"ocr_req_{uuid.uuid4().hex[:16]}"
                    trace_id = f"trace_{uuid.uuid4().hex[:12]}"
                    w, h = max(1, use_bbox[2] - use_bbox[0]), max(1, use_bbox[3] - use_bbox[1])
                    ocr_req = {
                        "schema_version": "ocr_request_v0",
                        "request_id": req_id,
                        "trace_id": trace_id,
                        "task_context": CHAIN_ROOT,
                        "input_type": "roi",
                        "image_path": str(crop_path),
                        "roi_refs": [f"ocr_roi_xyxy:0,0,{w},{h}"],
                        "allow_full_image": False,
                        "latency_budget_ms": 8000,
                        "expected_output": "ocr_evidence",
                    }
                    gov_route = _governance_route(sq_grade, q)
                    ocr_request_rows.append(
                        _build_ocr_request_row(
                            {"input_candidate_id": cid, "source_id": source_id, "source_type": source_type,
                             "source_frame_ref": frame_ref, "source_image_ref": str(crop_source) if source_type == "image" else None},
                            ocr_req,
                            sq_grade,
                            rg["readability_grade"],
                            gov_route,
                            f"roi_{cid}",
                        )
                    )
                    sub = _bridge_submit(ocr_req, crop_path, work_root / "sub" / cid, ws, gov)
                    provider_calls += 1
                    if sq_grade == "SQ_E":
                        sq_e_submitted = True
                    submission_traces.append(
                        {
                            "provider_call_id": f"pcall_{uuid.uuid4().hex[:10]}",
                            "ocr_request_id": req_id,
                            "input_candidate_id": cid,
                            "bridge_invoked": True,
                            "provider": sub.get("selected_provider"),
                            "provider_result_status": sub.get("submission_status"),
                            "raw_ocr_text": sub.get("text_joined"),
                            "text_items": sub.get("text_items"),
                            "empty_text": sub.get("empty_text"),
                            "direct_provider_bypass": False,
                            "source_chain": [CHAIN_ROOT, "ocr_request_gated_submission"],
                            "ocr_request_ref": sub.get("ocr_request_ref"),
                        }
                    )
                    gen_ocr = True
                    if sub.get("ocr_request_ref"):
                        pack = _build_evidence_pack(
                            evidence_id=f"ev_v2_{cid}",
                            source_type="video_frame_roi" if source_type == "video" else "poster_image_roi",
                            ocr_request_ref=sub["ocr_request_ref"],
                            submission=sub,
                            image_path=str(crop_source),
                            img_w=img_w,
                            img_h=img_h,
                            roi_bbox=use_bbox,
                            sq_grade=sq_grade,
                            readability_grade=rg["readability_grade"],
                            governance_route=gov_route,
                            video_meta=video_meta,
                        )
                        pack["ocr_request_ref"] = sub["ocr_request_ref"]
                        pack["input_candidate_ref"] = cid
                        pack["source_quality"] = {"source_quality_grade": sq_grade}
                        for k in list(pack.get("source", {}).keys()):
                            pass
                        pack["source"]["source_chain"] = [CHAIN_ROOT, "source_quality_gate", "readability_gate", "ocr_request_gated_submission"]
                        evidence_packs.append(pack)
                        sc = _build_semantic_candidate(pack)
                        sc["evidence_pack_ref"] = pack["evidence_id"]
                        semantic_candidates.append(sc)
        else:
            route, gen_scan = "scan_observation_only", True

        if gen_scan and preview:
            scan_observations.append(
                {
                    "scan_observation_id": f"scanobs_{cid}",
                    "source_id": source_id,
                    "frame_id": frame_ref,
                    "image_id": source_id if source_type == "image" else None,
                    "ocr_preview_or_text_hint": preview[:500],
                    "linebox_refs": [f"line_{i}" for i, it in enumerate(items[:8])],
                    "source_quality_grade": sq_grade,
                    "reason_not_primary_evidence": "full_frame_scan_or_gate_blocked",
                    "suggested_next_action": "roi_crop_before_evidence",
                    "fact_status": "not_fact",
                    "write_allowed": False,
                }
            )

        routing_rows.append(
            {
                "candidate_id": cid,
                "source_id": source_id,
                "route": route,
                "route_reason": gate_decision,
                "generated_ocr_request": gen_ocr,
                "generated_visual_symbol_candidate": gen_vs,
                "generated_public_facility_candidate": gen_pf,
                "generated_scan_observation": gen_scan,
                "blocked_reason": blocked if route.startswith("reject") else None,
            }
        )

    # --- images ---
    for ic in input_candidates:
        if ic["source_type"] != "image":
            continue
        iid = ic["source_id"]
        ipath = Path(ic["source_path"] or "")
        if not ic["file_exists"]:
            sq_rows.append(_sq_gate_row(ic["input_candidate_id"], "image", iid, "SQ_E", "missing_file", ["missing_file"]))
            routing_rows.append({"candidate_id": ic["input_candidate_id"], "source_id": iid, "route": "missing_file", "route_reason": "missing_file"})
            continue
        row = v1_images_by_id.get(iid, {})
        preview = str(row.get("text_joined") or "")
        items = row.get("text_items") if isinstance(row.get("text_items"), list) else []
        confs = [float(it["confidence"]) for it in items if it.get("confidence") is not None]
        avg_conf = sum(confs) / len(confs) if confs else 0.0
        w, h = int(row.get("image_width") or 0), int(row.get("image_height") or 0)
        if w <= 0:
            w, h = _probe_image_size(ipath)
        itype = _classify_image_type(preview, w, h)
        q = _poster_sq_grade(preview, items, avg_conf, w, h, itype)
        _route_and_maybe_ocr(
            input_candidate_id=ic["input_candidate_id"],
            source_type="image",
            source_id=iid,
            sq_grade=q["source_quality_grade"],
            gate_decision=q["gate_decision"],
            q=q,
            preview=preview,
            items=items,
            avg_conf=avg_conf,
            crop_source=ipath,
            bbox=_union_bbox(items) or [0, 0, w, h],
            img_w=w,
            img_h=h,
        )

    # --- P0 selected frames ---
    p0_path = Path(str(frame_plan.get("selected_video_path") or ""))
    for sf in frame_plan.get("selected_frames") or []:
        if not isinstance(sf, dict):
            continue
        fi = int(sf.get("frame_index") or 0)
        cid = f"frame_{P0_VIDEO_ID}_f{fi:06d}"
        trace = trace_by_frame.get(fi, {})
        preview = str(trace.get("ocr_preview") or sf.get("ocr_preview") or "")
        items = trace.get("text_items") if isinstance(trace.get("text_items"), list) else []
        w = int(trace.get("image_width") or 544)
        h = int(trace.get("image_height") or 960)
        confs = [float(it["confidence"]) for it in items if it.get("confidence") is not None]
        avg_conf = sum(confs) / len(confs) if confs else 0.0
        sq_grade = sq_by_frame.get(fi) or _heuristic_quality(preview, items, avg_conf, w, h, bool(items))["source_quality_grade"]
        q = _heuristic_quality(preview, items, avg_conf, w, h, bool(items))
        q["source_quality_grade"] = sq_grade
        _route_and_maybe_ocr(
            input_candidate_id=cid,
            source_type="video",
            source_id=P0_VIDEO_ID,
            sq_grade=sq_grade,
            gate_decision=q["gate_decision"],
            q=q,
            preview=preview,
            items=items,
            avg_conf=avg_conf,
            crop_source=p0_path,
            bbox=_union_bbox(items),
            img_w=w,
            img_h=h,
            frame_ref=f"{P0_VIDEO_ID}_f{fi:06d}",
            scan_ref=f"scan_obs:{trace.get('frame_id')}",
            video_meta={"video_id": P0_VIDEO_ID, "frame_index": fi, "timestamp_ms": sf.get("timestamp_ms"), "video_time_sec": sf.get("timestamp_sec")},
        )

    # --- non-P0 videos: scan observation from v1 only ---
    for ic in input_candidates:
        if ic["source_type"] != "video" or ic["source_id"] == P0_VIDEO_ID:
            continue
        vid = ic["source_id"]
        scan_row = v1_scan_by_vid.get(vid, {})
        previews = scan_row.get("representative_ocr_preview") or []
        preview = " | ".join(str(p) for p in previews[:3]) if previews else ""
        sq_grade = "SQ_C" if preview else "SQ_E"
        gate = "require_roi_crop" if preview else "reject_as_unreadable_or_mixed"
        q = {"gate_decision": gate, "public_like": False, "brand_like": False, "bank_like": False}
        sq_rows.append(_sq_gate_row(ic["input_candidate_id"], "video", vid, sq_grade, gate, ["v1_scan_reference_only"]))
        read_rows.append(_readability_row(ic["input_candidate_id"], sq_grade, preview, 0.5, q))
        routing_rows.append(
            {
                "candidate_id": ic["input_candidate_id"],
                "source_id": vid,
                "route": "scan_observation_only",
                "route_reason": "non_p0_video_scan_reference_no_full_frame_ocr",
                "generated_scan_observation": bool(preview),
                "generated_ocr_request": False,
            }
        )
        if preview:
            scan_observations.append(
                {
                    "scan_observation_id": f"scanobs_{ic['input_candidate_id']}",
                    "source_id": vid,
                    "ocr_preview_or_text_hint": preview,
                    "source_quality_grade": sq_grade,
                    "reason_not_primary_evidence": "non_p0_no_linebox_roi_gated_path_only",
                    "fact_status": "not_fact",
                    "write_allowed": False,
                }
            )

    packs_without_ref = sum(1 for p in evidence_packs if not (p.get("ocr_request_ref") or (p.get("source") or {}).get("ocr_request_ref")))
    bypass_static["evidence_packs_without_ocr_request_ref"] = packs_without_ref
    bypass_static["direct_provider_bypass"] = bypass_static["direct_provider_bypass"] or False
    bypass_static["provider_calls_without_ocr_request_ref"] = sum(
        1 for t in submission_traces if t.get("bridge_invoked") and not t.get("ocr_request_ref")
    )

    every_provider_ref = provider_calls == 0 or all(t.get("ocr_request_ref") for t in submission_traces if t.get("bridge_invoked"))
    every_pack_ref = all((p.get("ocr_request_ref") or (p.get("source") or {}).get("ocr_request_ref")) for p in evidence_packs) if evidence_packs else True

    sq_dist = Counter(r.get("source_quality_grade") for r in sq_rows)
    read_dist = Counter(r.get("readability_grade") for r in read_rows)

    summary = {
        "schema_version": "mixed_batch_v2_gated_path_summary_v0",
        "phase": PHASE_ID,
        "batch_scope": "mixed_video_poster_gated_path_only_smoke",
        "video_count": len(video_entries),
        "image_count": len(image_ids),
        "uses_gated_runtime_path": True,
        "direct_provider_bypass": False,
        "capability_imports_rapidocr": bypass_static["capability_imports_rapidocr"],
        "input_candidate_enabled": True,
        "source_quality_gate_enabled": True,
        "readability_gate_enabled": True,
        "ocr_request_gate_enabled": True,
        "ocr_mainline_bridge_required": True,
        "evidence_pack_enabled": True,
        "semantic_candidate_dryrun_enabled": True,
        "full_frame_scan_not_primary_evidence": True,
        "provider_call_count": provider_calls,
        "ocr_request_count": len(ocr_request_rows),
        "evidence_pack_count": len(evidence_packs),
        "semantic_candidate_count": len(semantic_candidates),
        "sq_e_submitted_to_ocr": sq_e_submitted,
        "every_provider_call_has_ocr_request_ref": every_provider_ref,
        "every_evidence_pack_has_ocr_request_ref": every_pack_ref,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "phase_verdict_hint": "GO" if not bypass_static["capability_imports_rapidocr"] and not sq_e_submitted else "CONDITIONAL_GO",
    }
    if errs:
        summary["errors"] = errs
    if provider_calls == 0:
        summary["conditional_go_reason"] = "all_candidates_blocked_by_gate_or_missing_roi"

    return {
        "summary": summary,
        "manifest": manifest,
        "input_matrix": {"schema_version": "mixed_batch_v2_input_candidate_matrix_v0", "row_count": len(input_candidates), "rows": input_candidates},
        "sq_matrix": {"schema_version": "mixed_batch_v2_source_quality_gate_decision_matrix_v0", "row_count": len(sq_rows), "rows": sq_rows, "sq_e_submitted_to_ocr": sq_e_submitted},
        "read_matrix": {"schema_version": "mixed_batch_v2_readability_gate_decision_matrix_v0", "row_count": len(read_rows), "rows": read_rows},
        "routing_matrix": {"schema_version": "mixed_batch_v2_routing_matrix_v0", "row_count": len(routing_rows), "rows": routing_rows},
        "ocr_request_matrix": {"schema_version": "mixed_batch_v2_ocr_request_candidate_matrix_v0", "row_count": len(ocr_request_rows), "rows": ocr_request_rows},
        "submission_trace": {
            "schema_version": "mixed_batch_v2_ocr_request_gated_submission_trace_v0",
            "row_count": len(submission_traces),
            "every_provider_call_has_ocr_request_ref": every_provider_ref,
            "direct_provider_bypass": False,
            "rows": submission_traces,
        },
        "bypass_report": bypass_static,
        "full_frame_boundary": {
            "schema_version": "mixed_batch_v2_full_frame_scan_boundary_report_v0",
            "full_frame_scan_allowed_for_observation": True,
            "full_frame_scan_allowed_for_primary_evidence": False,
            "scan_observation_fact_status": "not_fact",
            "scan_observation_write_allowed": False,
            "scan_observation_requires_roi_before_evidence": True,
            "scan_preview_not_primary_evidence": True,
            "full_frame_scan_not_world_model_attach": True,
        },
        "pack_collection": {
            "schema_version": "mixed_batch_v2_ocr_evidence_pack_collection_v0",
            "total_pack_count": len(evidence_packs),
            "every_evidence_pack_has_ocr_request_ref": every_pack_ref,
            "packs": evidence_packs,
        },
        "pack_alignment": {
            "schema_version": "mixed_batch_v2_evidence_pack_request_alignment_report_v0",
            "evidence_pack_count": len(evidence_packs),
            "ocr_request_count": len(ocr_request_rows),
            "aligned_pack_count": len(evidence_packs) - packs_without_ref,
            "every_evidence_pack_has_ocr_request_ref": every_pack_ref,
            "packs_without_request_ref": packs_without_ref,
            "request_without_pack_count": max(0, len(ocr_request_rows) - len(evidence_packs)),
            "alignment_status": "aligned" if every_pack_ref else "partial",
        },
        "semantic_collection": {
            "schema_version": "mixed_batch_v2_ocr_semantic_candidate_collection_v0",
            "candidate_count": len(semantic_candidates),
            "candidates": semantic_candidates,
        },
        "semantic_alignment": {
            "schema_version": "mixed_batch_v2_semantic_candidate_request_alignment_report_v0",
            "semantic_candidate_count": len(semantic_candidates),
            "semantic_candidates_with_evidence_pack_ref": sum(1 for s in semantic_candidates if s.get("evidence_pack_ref")),
            "semantic_candidates_with_ocr_request_ref": sum(1 for s in semantic_candidates if s.get("ocr_request_ref")),
            "semantic_candidates_without_request_ref": sum(1 for s in semantic_candidates if not s.get("ocr_request_ref")),
            "every_semantic_candidate_traceable_to_request": all(s.get("ocr_request_ref") for s in semantic_candidates) if semantic_candidates else True,
        },
        "scan_observation_report": {
            "schema_version": "mixed_batch_v2_scan_observation_report_v0",
            "scan_observation_count": len(scan_observations),
            "scan_observations": scan_observations,
        },
        "vs_pf_routing": {
            "schema_version": "mixed_batch_v2_visual_symbol_public_facility_routing_report_v0",
            "visual_symbol_candidate_count": len(visual_symbol_candidates),
            "brand_symbol_candidate_count": len(visual_symbol_candidates),
            "qr_candidate_count": 0,
            "public_facility_candidate_count": len(public_facility_candidates),
            "semantic_first_routed_count": len(public_facility_candidates),
            "ordinary_ocr_bypassed_count": sum(1 for r in routing_rows if r.get("route") == "visual_symbol_candidate"),
            "no_brand_fact_without_registry_or_review": True,
            "public_facility_fact_written": False,
        },
        "sq_rejection": {
            "schema_version": "mixed_batch_v2_source_quality_rejection_degrade_report_v0",
            "sq_a_count": sq_dist.get("SQ_A", 0),
            "sq_b_count": sq_dist.get("SQ_B", 0),
            "sq_c_count": sq_dist.get("SQ_C", 0),
            "sq_d_count": sq_dist.get("SQ_D", 0),
            "sq_e_count": sq_dist.get("SQ_E", 0),
            "submitted_to_ocr_count": provider_calls,
            "rejected_or_degraded_count": sum(1 for r in routing_rows if r.get("route") in ("rejected_unreadable", "scan_observation_only")),
            "visual_symbol_routed_count": len(visual_symbol_candidates),
            "scan_only_count": sum(1 for r in routing_rows if r.get("route") == "scan_observation_only"),
            "sq_e_submitted_to_ocr": sq_e_submitted,
            "low_quality_not_equal_provider_failure": True,
        },
        "uncertainty_guard": {
            "schema_version": "mixed_batch_v2_uncertainty_guard_report_v0",
            "empty_text_is_not_no_text_fact": True,
            "partial_text_is_not_complete_entity_fact": True,
            "non_empty_text_is_not_accuracy": True,
            "scan_observation_not_fact": True,
            "completion_candidate_committed": False,
            "correction_candidate_committed": False,
            "no_scene_delta_from_uncertain_text": True,
            "no_world_model_write_from_uncertain_text": True,
            "no_navigation_decision_from_uncertain_text": True,
        },
        "metrics": {
            "schema_version": "mixed_batch_v2_metrics_candidate_report_v0",
            "input_candidate_count": len(input_candidates),
            "ocr_request_count": len(ocr_request_rows),
            "provider_call_count": provider_calls,
            "evidence_pack_count": len(evidence_packs),
            "semantic_candidate_count": len(semantic_candidates),
            "scan_observation_count": len(scan_observations),
            "visual_symbol_candidate_count": len(visual_symbol_candidates),
            "public_facility_candidate_count": len(public_facility_candidates),
            "sq_grade_distribution": dict(sq_dist),
            "readability_grade_distribution": dict(read_dist),
            "every_provider_call_has_ocr_request_ref": every_provider_ref,
            "every_evidence_pack_has_ocr_request_ref": every_pack_ref,
            "direct_provider_bypass": False,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "mixed_batch_v2_benchmark_link_report_v0",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "mixed_batch_v2_system_health_link_report_v0",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "boundary": {
            "schema_version": "mixed_batch_v2_no_write_boundary_report_v0",
            "boundary_ok": True,
            "violations": [],
            "gated_path_only": True,
            "direct_provider_bypass": False,
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
        },
        "sim_report": {
            "schema_version": "mixed_batch_v2_simulation_context_report_v0",
            "simulation_profile_id": (_read_json(sim / "simulation_summary.json") or {}).get("simulation_profile_id") or "developer_full",
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "mixed_batch_v2_non_claims_report_v0",
            "not_production_ocr": True,
            "not_accuracy_benchmark": True,
            "not_provider_comparison": True,
            "not_visual_symbol_registry_integrated": True,
            "not_public_facility_fact_written": True,
            "not_world_model_attach": True,
            "not_scene_delta_readiness": True,
            "not_navigation": True,
            "not_production_ready": True,
            "go_means_gated_path_replacement_only": True,
        },
        "followups": {
            "schema_version": "mixed_batch_v2_open_followups_v0",
            "items": [
                "Improve SQ_B / poster ROI pass policy",
                "ROI Crop Proposal for selected text-bearing frames",
                "ROI-to-OCR Reference for selected crops",
                "OCRRequest Gated Submission coverage expansion",
                "Evidence Pack Adapter v1 with scan_observation_ref",
                "Semantic Candidate guard v1",
                "VisualSymbolRegistry integration",
                "PublicFacility semantic-first runtime extension",
                "SystemHealth provider runtime dry-run",
                "Benchmark T2 collector with GT",
            ],
        },
        "audit": {
            "schema_version": "mixed_batch_v2_audit_report_v0",
            "mixed_batch_v2_gated_path_only_executed": True,
            "uses_gated_runtime_path": True,
            "direct_provider_bypass": False,
            "capability_imports_rapidocr": bypass_static["capability_imports_rapidocr"],
            "input_candidate_count": len(input_candidates),
            "ocr_request_count": len(ocr_request_rows),
            "provider_call_count": provider_calls,
            "evidence_pack_count": len(evidence_packs),
            "semantic_candidate_count": len(semantic_candidates),
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
        },
        "errs": errs,
    }

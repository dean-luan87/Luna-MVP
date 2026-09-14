# -*- coding: utf-8 -*-
"""Rule-based ROI proposal stub (no YOLO, no Supervision mainline, no real segmentation)."""

from __future__ import annotations

import re
import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple


def bbox_to_polygon_xy_v0(x1: int, y1: int, x2: int, y2: int) -> List[List[int]]:
    return [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]


def _clamp_box(x1: int, y1: int, x2: int, y2: int, w: int, h: int) -> Tuple[int, int, int, int]:
    x1 = max(0, min(x1, w - 1))
    y1 = max(0, min(y1, h - 1))
    x2 = max(x1 + 1, min(x2, w))
    y2 = max(y1 + 1, min(y2, h))
    return x1, y1, x2, y2


def build_rule_stub_rois_for_frame_v0(
    *,
    frame_id: str,
    source_image_ref: str,
    frame_w: int,
    frame_h: int,
) -> List[Dict[str, Any]]:
    """Five fixed layout ROIs in frame pixel space."""
    w, h = int(frame_w), int(frame_h)
    specs: List[Tuple[str, str, Tuple[int, int, int, int]]] = [
        (
            "center_roi",
            "navigation_nearfield",
            _clamp_box(int(w * 0.3), int(h * 0.3), int(w * 0.7), int(h * 0.7), w, h),
        ),
        (
            "ground_roi",
            "navigation_nearfield",
            _clamp_box(0, int(h * 0.55), w, h, w, h),
        ),
        (
            "upper_sign_roi",
            "sign_region",
            _clamp_box(int(w * 0.2), 0, int(w * 0.8), int(h * 0.25), w, h),
        ),
        (
            "left_roi",
            "general_context",
            _clamp_box(0, 0, int(w * 0.35), h, w, h),
        ),
        (
            "right_roi",
            "general_context",
            _clamp_box(int(w * 0.65), 0, w, h, w, h),
        ),
    ]
    safe_fid = re.sub(r"[^a-zA-Z0-9_]+", "_", frame_id).strip("_")
    out: List[Dict[str, Any]] = []
    for roi_type, task_hint, (x1, y1, x2, y2) in specs:
        rid = f"vision_roi_{safe_fid}_{roi_type}"
        poly = bbox_to_polygon_xy_v0(x1, y1, x2, y2)
        out.append(
            {
                "roi_id": rid,
                "source_frame_id": frame_id,
                "source_image_ref": source_image_ref,
                "roi_type": roi_type,
                "bbox_in_frame": [x1, y1, x2, y2],
                "polygon_in_frame": poly,
                "coordinate_space": "frame_pixel",
                "proposal_source": "rule_stub",
                "confidence": 1.0,
                "task_hint": task_hint,
                "segmentation_stub": {
                    "mask_available": False,
                    "mask_ref": None,
                    "polygon_source": "bbox_as_polygon_stub",
                },
            }
        )
    return out


def crop_roi_to_png_v0(
    *,
    source_image: Path,
    bbox: List[int],
    out_path: Path,
) -> None:
    from PIL import Image  # type: ignore

    x1, y1, x2, y2 = (int(v) for v in bbox)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source_image) as im:
        crop = im.crop((x1, y1, x2, y2))
        crop.save(out_path, format="PNG")


def run_vision_roi_proposal_stub_from_governance_v0(
    governance_root: Path,
    output_root: Path,
) -> Dict[str, Any]:
    """Build ROI stub, crops, packs, matrices, audit from governance artifacts."""
    from capabilities.vision_runtime.vision_provider_input_pack_v0 import build_pack_for_frame_v0

    gov = governance_root.resolve()
    out = output_root.resolve()
    out.mkdir(parents=True, exist_ok=True)
    crops_dir = out / "crops"

    cand_path = gov / "vision_provider_input_candidate.json"
    mx_path = gov / "vision_frame_input_governance_matrix.json"
    if not cand_path.is_file():
        raise FileNotFoundError(cand_path)
    if not mx_path.is_file():
        raise FileNotFoundError(mx_path)

    candidate = json.loads(cand_path.read_text(encoding="utf-8"))
    matrix = json.loads(mx_path.read_text(encoding="utf-8"))

    dims_by_frame: Dict[str, Tuple[int, int]] = {}
    for row in matrix.get("rows") or []:
        fid = str(row.get("frame_id") or "")
        if not fid:
            continue
        w = int(row.get("width") or 0)
        h = int(row.get("height") or 0)
        if w > 0 and h > 0:
            dims_by_frame[fid] = (w, h)

    frames_in = candidate.get("frames") or []
    accepted = [f for f in frames_in if str(f.get("input_status") or "") == "accepted"]

    roi_items: List[Dict[str, Any]] = []
    packs: List[Dict[str, Any]] = []
    proposal_rows: List[Dict[str, Any]] = []
    unit_rows: List[Dict[str, Any]] = []
    per_frame_chains: List[Dict[str, Any]] = []

    gov_ref = str(gov)

    for fr in accepted:
        frame_id = str(fr.get("frame_id") or "")
        image_ref = str(fr.get("image_ref") or "")
        src_img = Path(image_ref).expanduser().resolve()
        if not src_img.is_file():
            raise FileNotFoundError(src_img)

        wh = dims_by_frame.get(frame_id)
        if not wh:
            from PIL import Image  # type: ignore

            with Image.open(src_img) as im:
                wh = (int(im.width), int(im.height))
        fw, fh = wh

        rois = build_rule_stub_rois_for_frame_v0(
            frame_id=frame_id,
            source_image_ref=image_ref,
            frame_w=fw,
            frame_h=fh,
        )

        crop_refs_by_roi_id: Dict[str, str] = {}
        for roi in rois:
            rid = str(roi.get("roi_id") or "")
            roi_type = str(roi.get("roi_type") or "roi")
            safe_fid = re.sub(r"[^a-zA-Z0-9_]+", "_", frame_id).strip("_")
            rel_name = f"{safe_fid}__{roi_type}.png"
            crop_path = crops_dir / rel_name
            crop_roi_to_png_v0(source_image=src_img, bbox=list(roi["bbox_in_frame"]), out_path=crop_path)
            crop_refs_by_roi_id[rid] = str(crop_path.resolve())

        pack_id = f"pack_{uuid.uuid4().hex[:16]}"
        pack = build_pack_for_frame_v0(
            pack_id=pack_id,
            source_frame_id=frame_id,
            source_image_ref=image_ref,
            governance_root=gov_ref,
            rois=rois,
            crop_refs_by_roi_id=crop_refs_by_roi_id,
            frame_w=fw,
            frame_h=fh,
        )
        packs.append(pack)
        roi_items.extend(rois)
        per_frame_chains.append({"frame_id": frame_id, "source_chain": pack.get("source_chain") or []})

        for roi in rois:
            rid = str(roi.get("roi_id") or "")
            proposal_rows.append(
                {
                    "frame_id": frame_id,
                    "roi_id": rid,
                    "roi_type": str(roi.get("roi_type") or ""),
                    "bbox_in_frame": list(roi.get("bbox_in_frame") or []),
                    "crop_image_ref": crop_refs_by_roi_id.get(rid, ""),
                    "task_hint": str(roi.get("task_hint") or ""),
                    "proposal_source": str(roi.get("proposal_source") or ""),
                    "segmentation_stub_mask_available": bool(
                        (roi.get("segmentation_stub") or {}).get("mask_available")
                    ),
                }
            )

        for u in pack.get("input_units") or []:
            unit_rows.append(
                {
                    "pack_id": pack_id,
                    "source_frame_id": frame_id,
                    "unit_id": str(u.get("unit_id") or ""),
                    "roi_id": str(u.get("roi_id") or ""),
                    "unit_type": str(u.get("unit_type") or ""),
                    "crop_image_ref": str(u.get("image_ref") or ""),
                    "task_hint": str(u.get("task_hint") or ""),
                }
            )

    input_units_total = sum(len(p.get("input_units") or []) for p in packs)

    summary = {
        "phase": "Phase-Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001",
        "schema": "vision_roi_proposal_stub_summary_v0",
        "frame_input_governance_root": gov_ref,
        "source_frame_count": len(accepted),
        "roi_items_count": len(roi_items),
        "input_units_count": input_units_total,
        "pack_count": len(packs),
        "proposal_source": "rule_stub",
    }

    proposal_candidate = {
        "schema_version": "vision_roi_proposal_candidate_v0",
        "proposal_source": "rule_stub",
        "frame_input_governance_root_ref": gov_ref,
        "roi_items": roi_items,
    }

    pack_bundle = {
        "bundle_schema": "vision_provider_input_pack_bundle_v0",
        "packs": packs,
    }

    proposal_matrix = {
        "schema": "vision_roi_proposal_matrix_v0",
        "rows": proposal_rows,
    }

    unit_matrix = {
        "schema": "vision_provider_input_unit_matrix_v0",
        "rows": unit_rows,
    }

    source_chain_summary = {
        "schema": "vision_roi_source_chain_summary_v0",
        "frame_input_governance_root": gov_ref,
        "per_frame": per_frame_chains,
    }

    audit = {
        "schema": "vision_roi_proposal_audit_v0",
        "roi_proposal_stub_generated": True,
        "vision_provider_input_pack_generated": True,
        "yolo_invoked": False,
        "real_detector_invoked": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
    }

    return {
        "summary": summary,
        "proposal_candidate": proposal_candidate,
        "provider_input_pack_bundle": pack_bundle,
        "proposal_matrix": proposal_matrix,
        "unit_matrix": unit_matrix,
        "source_chain_summary": source_chain_summary,
        "audit": audit,
    }

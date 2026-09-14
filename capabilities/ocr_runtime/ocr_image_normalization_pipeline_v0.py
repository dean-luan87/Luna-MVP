# -*- coding: utf-8 -*-
"""
OCR Image Input Normalization Pipeline v0 — probe, decisions, optional safe normalize, provider input pack.

No real OCR. Does not call PaddleOCR / RapidOCR.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.ocr_runtime.ocr_provider_input_pack_v0 import SCHEMA_VERSION, new_pack_id


def _read_gov(p: Path) -> Dict[str, Any]:
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _sha256_file(path: Path, max_bytes: int = 16 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    n = 0
    with path.open("rb") as f:
        while n < max_bytes:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            take = min(len(chunk), max_bytes - n)
            h.update(chunk[:take])
            n += take
    return h.hexdigest()


def probe_image_metadata_v0(image_path: Path) -> Dict[str, Any]:
    row: Dict[str, Any] = {
        "image_path": str(image_path.resolve()),
        "file_exists": image_path.is_file(),
        "file_size_bytes": image_path.stat().st_size if image_path.is_file() else None,
        "width": None,
        "height": None,
        "megapixels": None,
        "format": None,
        "mode": None,
        "channels": None,
        "exif_orientation": None,
        "extreme_aspect_ratio": None,
        "image_fingerprint": None,
        "probe_error": None,
    }
    if not image_path.is_file():
        row["probe_error"] = "file_missing"
        return row
    try:
        from PIL import Image

        row["image_fingerprint"] = _sha256_file(image_path)
        with Image.open(image_path) as im:
            row["format"] = im.format
            row["mode"] = im.mode
            w, h = im.size
            row["width"] = int(w)
            row["height"] = int(h)
            row["megapixels"] = round((w * h) / 1_000_000.0, 6)
            if hasattr(im, "getbands"):
                row["channels"] = len(im.getbands())
            exif = im.getexif()
            if exif is not None:
                ori = exif.get(274)
                if ori is not None:
                    row["exif_orientation"] = int(ori)
            ar = float(max(w, h)) / float(min(w, h)) if min(w, h) > 0 else 0.0
            row["extreme_aspect_ratio"] = bool(ar > 6.0)
    except Exception as e:
        row["probe_error"] = f"{type(e).__name__}:{e}"
    return row


def build_input_decision_v0(probe: Dict[str, Any], gate: Dict[str, Any]) -> Dict[str, Any]:
    mode = str(probe.get("mode") or "")
    exif = probe.get("exif_orientation")
    gv = str(gate.get("gate_verdict") or "")
    rec = str(gate.get("recommended_input_strategy") or "")
    return {
        "schema_version": "ocr_image_input_decision_v0",
        "rgb_convert_required": "A" in mode,
        "exif_transpose_required": exif is not None and int(exif) != 1,
        "downscale_required": gv == "CONDITIONAL_ALLOW" and rec == "downscale",
        "tile_path": gv == "CONDITIONAL_ALLOW" and rec == "tile",
        "tile_required": rec == "tile_required",
        "roi_required": False,
        "reject_required": gv == "REJECT",
        "gate_verdict": gv,
        "recommended_input_strategy": rec,
    }


def _apply_safe_normalize(
    image_path: Path,
    work_dir: Path,
    decision: Dict[str, Any],
    gov: Dict[str, Any],
    probe: Dict[str, Any],
) -> Tuple[Path, Dict[str, Any], List[str]]:
    """Returns (output_image_path, coordinate_transform, source_chain_steps)."""
    from PIL import Image, ImageOps

    work_dir.mkdir(parents=True, exist_ok=True)
    chain: List[str] = ["read_source"]
    im = Image.open(image_path)
    im.load()
    ow, oh = im.size
    if decision.get("exif_transpose_required"):
        im = ImageOps.exif_transpose(im)
        chain.append("exif_transpose")
    if decision.get("rgb_convert_required") or im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
        chain.append("rgba_to_rgb_or_convert")
    tw, th = im.size
    if decision.get("downscale_required"):
        ds = gov.get("downscale_policy") if isinstance(gov.get("downscale_policy"), dict) else {}
        max_side = int(ds.get("preferred_max_side") or 1600)
        w, h = im.size
        m = max(w, h)
        if m > max_side:
            sc = max_side / float(m)
            tw = max(1, int(round(w * sc)))
            th = max(1, int(round(h * sc)))
            im = im.resize((tw, th), Image.Resampling.LANCZOS)
            chain.append(f"downscale_max_side_{max_side}")
    out_p = work_dir / "normalized_for_provider.png"
    im.save(out_p, format="PNG")
    chain.append("write_normalized_png")
    transform: Dict[str, Any] = {
        "original_width": int(ow),
        "original_height": int(oh),
        "transformed_width": int(tw),
        "transformed_height": int(th),
        "scale_x": round(float(tw) / float(ow), 8) if ow else 1.0,
        "scale_y": round(float(th) / float(oh), 8) if oh else 1.0,
    }
    return out_p.resolve(), transform, chain


def _clamp_bbox_xyxy_v0(bbox: List[int], ow: int, oh: int) -> List[int]:
    x0, y0, x1, y1 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    x0 = max(0, min(x0, max(0, ow - 1)))
    y0 = max(0, min(y0, max(0, oh - 1)))
    x1 = max(x0 + 1, min(x1, ow))
    y1 = max(y0 + 1, min(y1, oh))
    return [x0, y0, x1, y1]


def _build_roi_provider_branch_v0(
    *,
    image_path: Path,
    gate: Dict[str, Any],
    probe: Dict[str, Any],
    decision: Dict[str, Any],
    normalization_work_dir: Path,
    request_id: str,
    trace_id: str,
    roi_bbox_xyxy: List[int],
    norm_audit: Dict[str, Any],
) -> Dict[str, Any]:
    """Crop ROI from source (after EXIF/RGB same as full-image branch), optional inner downscale to lightweight max edge."""
    from PIL import Image, ImageOps

    from capabilities.ocr_runtime.ocr_lightweight_provider_adapter_v0 import lightweight_max_edge_px_v0

    normalization_work_dir.mkdir(parents=True, exist_ok=True)
    chain: List[str] = ["probe_complete", "read_source_for_roi"]

    im = Image.open(image_path)
    im.load()
    if decision.get("exif_transpose_required"):
        im = ImageOps.exif_transpose(im)
        chain.append("exif_transpose_roi_branch")
    if decision.get("rgb_convert_required") or im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
        chain.append("rgba_to_rgb_or_convert_roi_branch")

    ow, oh = im.size
    x0, y0, x1, y1 = _clamp_bbox_xyxy_v0(roi_bbox_xyxy, ow, oh)
    chain.append(f"roi_bbox_xyxy_clamped:{x0},{y0},{x1},{y1}")

    crop = im.crop((x0, y0, x1, y1))
    roi_w0, roi_h0 = x1 - x0, y1 - y0

    cap = lightweight_max_edge_px_v0()
    cw, ch = int(crop.width), int(crop.height)
    inner_down = False
    m = max(cw, ch)
    if m > cap:
        sc = cap / float(m)
        cw = max(1, int(round(cw * sc)))
        ch = max(1, int(round(ch * sc)))
        crop = crop.resize((cw, ch), Image.Resampling.LANCZOS)
        inner_down = True
        chain.append(f"roi_inner_downscale_max_edge_{cap}")

    out_p = (normalization_work_dir / "roi_crop_for_provider.png").resolve()
    crop.save(out_p, format="PNG")
    chain.append("write_roi_crop_png")
    chain.append(f"roi_crop_ref:{out_p}")
    chain.append("build_provider_input_pack")

    scale_x = float(cw) / float(roi_w0) if roi_w0 else 1.0
    scale_y = float(ch) / float(roi_h0) if roi_h0 else 1.0
    transform: Dict[str, Any] = {
        "mode": "roi_crop",
        "offset_x": int(x0),
        "offset_y": int(y0),
        "original_width": int(ow),
        "original_height": int(oh),
        "roi_source_width": int(roi_w0),
        "roi_source_height": int(roi_h0),
        "transformed_width": int(cw),
        "transformed_height": int(ch),
        "scale_x": round(scale_x, 8),
        "scale_y": round(scale_y, 8),
    }

    nmp = round((cw * ch) / 1_000_000.0, 6)
    unit: Dict[str, Any] = {
        "unit_id": "unit_001",
        "unit_type": "roi",
        "image_ref": str(out_p),
        "bbox_in_original": [x0, y0, x1, y1],
        "scale_ratio": max(scale_x, scale_y),
        "coordinate_transform": json.dumps(transform, sort_keys=True),
        "width": int(cw),
        "height": int(ch),
        "megapixels": nmp,
        "provider_level_hint": "level_1",
        "ocr_allowed": True,
    }

    norm_audit["original_image_used_directly"] = False
    norm_audit["normalized_image_generated"] = True
    norm_audit["downscale_applied"] = bool(inner_down)
    norm_audit["coordinate_transform_recorded"] = True
    norm_audit["tile_applied"] = False

    source_ref = str(image_path.resolve())
    stcm_hint = {
        "deadline_class": "ocr_mainline_minimal",
        "valid_until": "relative_to_request_latency_budget",
        "trace_id": trace_id,
        "request_id": request_id,
    }
    pack: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "pack_id": new_pack_id(),
        "source_image_ref": source_ref,
        "normalized_image_ref": str(out_p),
        "image_fingerprint": str(probe.get("image_fingerprint") or ""),
        "input_units": [unit],
        "processing_policy": {
            "strategy": "roi",
            "reason_codes": list(gate.get("reason_codes") or []) if isinstance(gate.get("reason_codes"), list) else [],
        },
        "source_chain": chain,
        "coordinate_transform": transform,
        "stcm_deadline_hint": stcm_hint,
        "audit": {
            "pack_builder": "ocr_image_normalization_pipeline_v0+roi_crop",
            "original_image_used_directly": bool(norm_audit.get("original_image_used_directly")),
            "normalized_image_generated": bool(norm_audit.get("normalized_image_generated")),
            "downscale_applied": bool(norm_audit.get("downscale_applied")),
            "tile_applied": bool(norm_audit.get("tile_applied")),
            "coordinate_transform_recorded": bool(norm_audit.get("coordinate_transform_recorded")),
            "real_provider_invoked": False,
            "paddleocr_invoked": False,
            "rapidocr_replaced": False,
            "ocr_routing_changed": False,
            "midplatform_invoked": False,
            "world_model_written": False,
        },
    }

    return {
        "metadata_probe": probe,
        "input_decision": decision,
        "coordinate_transform_matrix": {"units": [transform]},
        "provider_input_pack": pack,
        "normalization_audit": norm_audit,
        "source_chain": chain,
    }


def _build_multi_roi_provider_branch_v0(
    *,
    image_path: Path,
    gate: Dict[str, Any],
    probe: Dict[str, Any],
    decision: Dict[str, Any],
    normalization_work_dir: Path,
    request_id: str,
    trace_id: str,
    roi_bboxes_xyxy: List[List[int]],
    norm_audit: Dict[str, Any],
) -> Dict[str, Any]:
    """Multiple ROI crops on one source image; one input_unit per ROI (``strategy=roi_list``)."""
    from PIL import Image, ImageOps

    from capabilities.ocr_runtime.ocr_lightweight_provider_adapter_v0 import lightweight_max_edge_px_v0

    normalization_work_dir.mkdir(parents=True, exist_ok=True)
    chain: List[str] = ["probe_complete", "read_source_for_roi_multi"]

    im = Image.open(image_path)
    im.load()
    if decision.get("exif_transpose_required"):
        im = ImageOps.exif_transpose(im)
        chain.append("exif_transpose_roi_multi_branch")
    if decision.get("rgb_convert_required") or im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
        chain.append("rgba_to_rgb_or_convert_roi_multi_branch")

    ow, oh = im.size
    cap = lightweight_max_edge_px_v0()
    units: List[Dict[str, Any]] = []
    transforms: List[Dict[str, Any]] = []
    any_inner_down = False
    first_crop_path: Optional[Path] = None

    for idx, raw_bbox in enumerate(roi_bboxes_xyxy):
        if not isinstance(raw_bbox, list) or len(raw_bbox) != 4:
            continue
        x0, y0, x1, y1 = _clamp_bbox_xyxy_v0([int(raw_bbox[0]), int(raw_bbox[1]), int(raw_bbox[2]), int(raw_bbox[3])], ow, oh)
        roi_id = f"roi_{idx:03d}"
        unit_id = f"unit_{idx + 1:03d}"
        chain.append(f"roi_bbox_xyxy_clamped:{roi_id}:{x0},{y0},{x1},{y1}")

        crop = im.crop((x0, y0, x1, y1))
        roi_w0, roi_h0 = x1 - x0, y1 - y0

        cw, ch = int(crop.width), int(crop.height)
        inner_down = False
        m = max(cw, ch)
        if m > cap:
            sc = cap / float(m)
            cw = max(1, int(round(cw * sc)))
            ch = max(1, int(round(ch * sc)))
            crop = crop.resize((cw, ch), Image.Resampling.LANCZOS)
            inner_down = True
            any_inner_down = True
            chain.append(f"roi_inner_downscale_max_edge_{cap}:{roi_id}")

        out_p = (normalization_work_dir / f"roi_crop_{roi_id}.png").resolve()
        crop.save(out_p, format="PNG")
        chain.append(f"write_roi_crop_png:{roi_id}")
        chain.append(f"roi_crop_ref:{roi_id}:{out_p}")
        if first_crop_path is None:
            first_crop_path = out_p

        scale_x = float(cw) / float(roi_w0) if roi_w0 else 1.0
        scale_y = float(ch) / float(roi_h0) if roi_h0 else 1.0
        transform: Dict[str, Any] = {
            "mode": "roi_crop",
            "roi_id": roi_id,
            "unit_id": unit_id,
            "offset_x": int(x0),
            "offset_y": int(y0),
            "original_width": int(ow),
            "original_height": int(oh),
            "roi_source_width": int(roi_w0),
            "roi_source_height": int(roi_h0),
            "transformed_width": int(cw),
            "transformed_height": int(ch),
            "scale_x": round(scale_x, 8),
            "scale_y": round(scale_y, 8),
        }
        transforms.append(transform)

        nmp = round((cw * ch) / 1_000_000.0, 6)
        units.append(
            {
                "unit_id": unit_id,
                "roi_id": roi_id,
                "unit_type": "roi",
                "image_ref": str(out_p),
                "bbox_in_original": [x0, y0, x1, y1],
                "scale_ratio": max(scale_x, scale_y),
                "coordinate_transform": json.dumps(transform, sort_keys=True),
                "width": int(cw),
                "height": int(ch),
                "megapixels": nmp,
                "provider_level_hint": "level_1",
                "ocr_allowed": True,
            }
        )

    chain.append("build_provider_input_pack")
    norm_audit["original_image_used_directly"] = False
    norm_audit["normalized_image_generated"] = True
    norm_audit["downscale_applied"] = bool(any_inner_down)
    norm_audit["coordinate_transform_recorded"] = True
    norm_audit["tile_applied"] = False

    source_ref = str(image_path.resolve())
    stcm_hint = {
        "deadline_class": "ocr_mainline_minimal",
        "valid_until": "relative_to_request_latency_budget",
        "trace_id": trace_id,
        "request_id": request_id,
    }
    agg_ct: Dict[str, Any] = {
        "mode": "multi_roi_crop",
        "roi_unit_count": len(units),
        "per_unit_transform_in_matrix": True,
        "original_width": int(ow),
        "original_height": int(oh),
    }
    norm_ref = str(first_crop_path) if first_crop_path else source_ref
    pack: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "pack_id": new_pack_id(),
        "source_image_ref": source_ref,
        "normalized_image_ref": norm_ref,
        "image_fingerprint": str(probe.get("image_fingerprint") or ""),
        "input_units": units,
        "processing_policy": {
            "strategy": "roi_list",
            "reason_codes": list(gate.get("reason_codes") or []) if isinstance(gate.get("reason_codes"), list) else [],
        },
        "source_chain": chain,
        "coordinate_transform": agg_ct,
        "stcm_deadline_hint": stcm_hint,
        "audit": {
            "pack_builder": "ocr_image_normalization_pipeline_v0+multi_roi_crop",
            "original_image_used_directly": bool(norm_audit.get("original_image_used_directly")),
            "normalized_image_generated": bool(norm_audit.get("normalized_image_generated")),
            "downscale_applied": bool(norm_audit.get("downscale_applied")),
            "tile_applied": bool(norm_audit.get("tile_applied")),
            "coordinate_transform_recorded": bool(norm_audit.get("coordinate_transform_recorded")),
            "real_provider_invoked": False,
            "paddleocr_invoked": False,
            "rapidocr_replaced": False,
            "ocr_routing_changed": False,
            "midplatform_invoked": False,
            "world_model_written": False,
        },
    }

    return {
        "metadata_probe": probe,
        "input_decision": decision,
        "coordinate_transform_matrix": {"units": transforms},
        "provider_input_pack": pack,
        "normalization_audit": norm_audit,
        "source_chain": chain,
    }


def run_ocr_image_normalization_pipeline_v0(
    *,
    image_path: Path,
    gate: Dict[str, Any],
    governance_config_path: Path,
    normalization_work_dir: Path,
    request_id: str,
    trace_id: str,
    roi_bboxes_xyxy: Optional[List[List[int]]] = None,
) -> Dict[str, Any]:
    gov = _read_gov(governance_config_path)
    probe = probe_image_metadata_v0(image_path)
    decision = build_input_decision_v0(probe, gate)

    norm_audit = {
        "original_image_used_directly": False,
        "normalized_image_generated": False,
        "downscale_applied": False,
        "tile_applied": False,
        "coordinate_transform_recorded": False,
    }

    if decision.get("reject_required"):
        return {
            "metadata_probe": probe,
            "input_decision": decision,
            "coordinate_transform_matrix": {"units": []},
            "provider_input_pack": None,
            "normalization_audit": norm_audit,
            "source_chain": ["probe_only_reject"],
        }

    if roi_bboxes_xyxy is not None:
        clean: List[List[int]] = [b for b in roi_bboxes_xyxy if isinstance(b, list) and len(b) == 4]
        if len(clean) == 1:
            return _build_roi_provider_branch_v0(
                image_path=image_path,
                gate=gate,
                probe=probe,
                decision=decision,
                normalization_work_dir=normalization_work_dir,
                request_id=request_id,
                trace_id=trace_id,
                roi_bbox_xyxy=clean[0],
                norm_audit=norm_audit,
            )
        if len(clean) >= 2:
            return _build_multi_roi_provider_branch_v0(
                image_path=image_path,
                gate=gate,
                probe=probe,
                decision=decision,
                normalization_work_dir=normalization_work_dir,
                request_id=request_id,
                trace_id=trace_id,
                roi_bboxes_xyxy=clean,
                norm_audit=norm_audit,
            )

    if decision.get("tile_path"):
        from capabilities.ocr_runtime.ocr_tile_planner_v0 import plan_tiles_v0, prepare_image_for_tiling_v0

        normalization_work_dir.mkdir(parents=True, exist_ok=True)
        pre_path, tw, th, prep_chain = prepare_image_for_tiling_v0(image_path, normalization_work_dir, decision)
        tile_plan, units, transforms = plan_tiles_v0(
            source_image_path=pre_path,
            work_dir=normalization_work_dir,
            governance=gov,
            original_width=tw,
            original_height=th,
        )
        norm_audit["tile_applied"] = True
        norm_audit["tile_count"] = len(units)
        norm_audit["coordinate_transform_recorded"] = True
        norm_audit["original_image_used_directly"] = False
        norm_audit["normalized_image_generated"] = True
        norm_audit["downscale_applied"] = False

        cov_complete = bool(tile_plan.get("coverage_complete"))
        trunc_b = bool(tile_plan.get("truncated_to_budget"))
        norm_audit["tile_coverage_complete"] = cov_complete
        norm_audit["tile_truncated_to_budget"] = trunc_b
        norm_audit["full_image_claim_allowed"] = False
        norm_audit["partial_evidence_scope_recorded"] = True

        evidence_scope = "partial_image" if trunc_b or not cov_complete else "tile_set_complete"
        reading_order_confidence = "low" if evidence_scope == "partial_image" else "medium"
        async_avail = bool(tile_plan.get("async_completion_available"))

        tile_coverage: Dict[str, Any] = {
            "schema_version": "ocr_tile_coverage_summary_v0",
            "raw_tile_count": int(tile_plan.get("raw_tile_count") or 0),
            "materialized_tile_count": int(tile_plan.get("materialized_tile_count") or 0),
            "truncated_to_budget": trunc_b,
            "coverage_complete": cov_complete,
            "coverage_ratio_estimate": float(tile_plan.get("coverage_ratio_estimate") or 0.0),
            "coverage_ratio_method": str(tile_plan.get("coverage_ratio_method") or ""),
            "covered_regions": tile_plan.get("covered_regions") if isinstance(tile_plan.get("covered_regions"), list) else [],
            "uncovered_regions": tile_plan.get("uncovered_regions") if isinstance(tile_plan.get("uncovered_regions"), list) else [],
            "max_tile_count_applied": int(tile_plan.get("max_tile_count_applied") or 0),
            "tile_budget_type": str(tile_plan.get("tile_budget_type") or "sync"),
            "async_completion_available": async_avail,
        }

        source_ref = str(image_path.resolve())
        agg_ct: Dict[str, Any] = {
            "mode": "multi_tile",
            "original_width": tw,
            "original_height": th,
            "tile_count": len(units),
            "requires_per_unit_transform": True,
            "coverage_complete": cov_complete,
            "truncated_to_budget": trunc_b,
        }
        full_chain = (
            [f"original_image_ref:{source_ref}", "probe_complete"]
            + prep_chain
            + ["tile_plan_created", "tile_generated", "coordinate_transform_recorded"]
            + [
                f"tile_plan_raw_count:{int(tile_plan.get('raw_tile_count') or 0)}",
                f"tile_materialized_count:{int(tile_plan.get('materialized_tile_count') or 0)}",
                f"tile_truncated_to_budget:{str(bool(tile_plan.get('truncated_to_budget'))).lower()}",
                f"coverage_complete:{str(bool(tile_plan.get('coverage_complete'))).lower()}",
            ]
            + [f"tile_ref:{u.get('image_ref')}" for u in units if isinstance(u, dict)]
            + ["build_provider_input_pack"]
        )

        pack: Dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "pack_id": new_pack_id(),
            "source_image_ref": source_ref,
            "normalized_image_ref": str(pre_path),
            "image_fingerprint": str(probe.get("image_fingerprint") or ""),
            "input_units": units,
            "tile_coverage": tile_coverage,
            "processing_policy": {
                "strategy": "tile",
                "reason_codes": list(gate.get("reason_codes") or []) if isinstance(gate.get("reason_codes"), list) else [],
                "evidence_scope": evidence_scope,
                "full_image_claim_allowed": False,
                "reading_order_confidence": reading_order_confidence,
                "async_completion_available": async_avail,
            },
            "source_chain": full_chain,
            "coordinate_transform": agg_ct,
            "stcm_deadline_hint": {
                "deadline_class": "ocr_mainline_minimal",
                "valid_until": "relative_to_request_latency_budget",
                "trace_id": trace_id,
                "request_id": request_id,
            },
            "audit": {
                "pack_builder": "ocr_image_normalization_pipeline_v0+ocr_tile_planner_v0",
                "original_image_used_directly": bool(norm_audit.get("original_image_used_directly")),
                "normalized_image_generated": bool(norm_audit.get("normalized_image_generated")),
                "downscale_applied": bool(norm_audit.get("downscale_applied")),
                "tile_applied": bool(norm_audit.get("tile_applied")),
                "coordinate_transform_recorded": bool(norm_audit.get("coordinate_transform_recorded")),
                "tile_coverage_complete": cov_complete,
                "tile_truncated_to_budget": trunc_b,
                "full_image_claim_allowed": False,
                "partial_evidence_scope_recorded": True,
                "real_provider_invoked": False,
                "paddleocr_invoked": False,
                "rapidocr_replaced": False,
                "ocr_routing_changed": False,
                "midplatform_invoked": False,
                "world_model_written": False,
            },
        }
        return {
            "metadata_probe": probe,
            "input_decision": decision,
            "coordinate_transform_matrix": {"units": transforms, "tile_coverage": tile_coverage},
            "provider_input_pack": pack,
            "normalization_audit": norm_audit,
            "source_chain": full_chain,
            "tile_plan": tile_plan,
        }

    gv = gate.get("gate_verdict")
    need_pixel_pipeline = bool(
        decision.get("rgb_convert_required")
        or decision.get("exif_transpose_required")
        or decision.get("downscale_required")
        or gv == "CONDITIONAL_ALLOW"
    )

    source_ref = str(image_path.resolve())
    normalized_path: Optional[Path] = None
    transform: Dict[str, Any] = {}
    chain_steps: List[str] = ["probe_complete"]

    if need_pixel_pipeline:
        normalization_work_dir.mkdir(parents=True, exist_ok=True)
        normalized_path, transform, chain_steps = _apply_safe_normalize(
            image_path, normalization_work_dir, decision, gov, probe
        )
        norm_audit["normalized_image_generated"] = True
        norm_audit["downscale_applied"] = bool(decision.get("downscale_required"))
        norm_audit["coordinate_transform_recorded"] = True
        if not decision.get("downscale_required") and float(transform.get("scale_x") or 1) == 1.0 and float(transform.get("scale_y") or 1) == 1.0:
            norm_audit["original_image_used_directly"] = True
        else:
            norm_audit["original_image_used_directly"] = False
    else:
        normalized_path = image_path.resolve()
        ow = int(probe.get("width") or 0)
        oh = int(probe.get("height") or 0)
        transform = {
            "original_width": ow,
            "original_height": oh,
            "transformed_width": ow,
            "transformed_height": oh,
            "scale_x": 1.0,
            "scale_y": 1.0,
        }
        chain_steps.append("no_pixel_transform_use_source_as_normalized_ref")
        norm_audit["original_image_used_directly"] = True
        norm_audit["coordinate_transform_recorded"] = True

    assert normalized_path is not None
    nw = int(transform.get("transformed_width") or 0)
    nh = int(transform.get("transformed_height") or 0)
    nmp = round((nw * nh) / 1_000_000.0, 6) if nw and nh else 0.0

    unit_type = "downscaled_full_image" if decision.get("downscale_required") else "full_image"
    unit: Dict[str, Any] = {
        "unit_id": "unit_001",
        "unit_type": unit_type,
        "image_ref": str(normalized_path),
        "bbox_in_original": [0, 0, int(probe.get("width") or 0), int(probe.get("height") or 0)],
        "scale_ratio": float(transform.get("scale_x") or 1.0),
        "coordinate_transform": json.dumps(transform, sort_keys=True),
        "width": nw,
        "height": nh,
        "megapixels": nmp,
        "provider_level_hint": "level_1",
        "ocr_allowed": True,
    }

    strategy = "downscale" if decision.get("downscale_required") else "roi_only_stub"
    if gv == "ALLOW" and not decision.get("downscale_required"):
        strategy = "full_image_allowed"

    stcm_hint = {
        "deadline_class": "ocr_mainline_minimal",
        "valid_until": "relative_to_request_latency_budget",
        "trace_id": trace_id,
        "request_id": request_id,
    }

    full_chain = chain_steps + [
        f"normalized_ref:{normalized_path}",
        "build_provider_input_pack",
    ]

    pack: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "pack_id": new_pack_id(),
        "source_image_ref": source_ref,
        "normalized_image_ref": str(normalized_path),
        "image_fingerprint": str(probe.get("image_fingerprint") or ""),
        "input_units": [unit],
        "processing_policy": {
            "strategy": strategy,
            "reason_codes": list(gate.get("reason_codes") or []) if isinstance(gate.get("reason_codes"), list) else [],
        },
        "source_chain": full_chain,
        "coordinate_transform": transform,
        "stcm_deadline_hint": stcm_hint,
        "audit": {
            "pack_builder": "ocr_image_normalization_pipeline_v0",
            "original_image_used_directly": bool(norm_audit.get("original_image_used_directly")),
            "normalized_image_generated": bool(norm_audit.get("normalized_image_generated")),
            "downscale_applied": bool(norm_audit.get("downscale_applied")),
            "tile_applied": bool(norm_audit.get("tile_applied")),
            "coordinate_transform_recorded": bool(norm_audit.get("coordinate_transform_recorded")),
            "real_provider_invoked": False,
            "paddleocr_invoked": False,
            "rapidocr_replaced": False,
            "ocr_routing_changed": False,
            "midplatform_invoked": False,
            "world_model_written": False,
        },
    }

    return {
        "metadata_probe": probe,
        "input_decision": decision,
        "coordinate_transform_matrix": {"units": [transform]},
        "provider_input_pack": pack,
        "normalization_audit": norm_audit,
        "source_chain": full_chain,
    }

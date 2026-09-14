# -*- coding: utf-8 -*-
"""RapidOCR lightweight runtime adapter — optional dependency; never touches MidPlatform / WorldModel."""

from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Optional, Tuple, Type

from capabilities.ocr_runtime.ocr_lightweight_provider_adapter_v0 import (
    evaluate_lightweight_provider_input_pack_v0,
    lightweight_max_edge_px_v0,
)
from capabilities.ocr_runtime.ocr_roi_coordinate_lift_v0 import (
    local_bbox_xyxy_from_polygon_v0,
    normalize_local_polygon_v0,
)
from capabilities.ocr_runtime.ocr_provider_adapter_contract_v0 import OCRProviderAdapterV0
from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

_RapidOCRClass: Optional[Type[Any]] = None
_RapidImportError: Optional[str] = None
_ENGINE_INSTANCE: Any = None
_ENGINE_ERROR: Optional[str] = None


def _try_import_rapidocr_class() -> Tuple[Optional[Type[Any]], Optional[str]]:
    global _RapidOCRClass, _RapidImportError
    if _RapidOCRClass is not None:
        return _RapidOCRClass, _RapidImportError
    try:
        from rapidocr_onnxruntime import RapidOCR as _ROC  # type: ignore[import-not-found]

        _RapidOCRClass = _ROC
        _RapidImportError = None
        return _RapidOCRClass, None
    except Exception as e1:  # noqa: BLE001 — best-effort import
        try:
            from rapidocr import RapidOCR as _ROC2  # type: ignore[import-not-found]

            _RapidOCRClass = _ROC2
            _RapidImportError = None
            return _RapidOCRClass, None
        except Exception as e2:  # noqa: BLE001
            _RapidOCRClass = None
            _RapidImportError = f"rapidocr_import_failed:{e1!s}|{e2!s}"
            return None, _RapidImportError


def _get_engine() -> Tuple[Any, Optional[str]]:
    """Lazy singleton RapidOCR engine; returns (engine_or_none, error_message)."""
    global _ENGINE_INSTANCE, _ENGINE_ERROR
    if _ENGINE_ERROR is not None and _ENGINE_INSTANCE is None:
        return None, _ENGINE_ERROR
    if _ENGINE_INSTANCE is not None:
        return _ENGINE_INSTANCE, None
    cls, err = _try_import_rapidocr_class()
    if cls is None:
        _ENGINE_ERROR = err or "rapidocr_class_unavailable"
        return None, _ENGINE_ERROR
    try:
        _ENGINE_INSTANCE = cls()
        _ENGINE_ERROR = None
        return _ENGINE_INSTANCE, None
    except Exception as e:  # noqa: BLE001
        _ENGINE_ERROR = f"rapidocr_engine_init_failed:{e!s}"
        return None, _ENGINE_ERROR


def _parse_rapid_output(raw: Any) -> Tuple[List[Dict[str, Any]], str]:
    items: List[Dict[str, Any]] = []
    if not raw:
        return items, ""
    if not isinstance(raw, (list, tuple)):
        return items, ""
    for row in raw:
        if not row or not isinstance(row, (list, tuple)):
            continue
        box: Any = None
        text = ""
        score = 0.0
        if len(row) >= 2:
            box, payload = row[0], row[1]
        else:
            continue
        if isinstance(payload, (list, tuple)) and len(payload) >= 1:
            text = str(payload[0] or "")
            if len(payload) >= 2 and payload[1] is not None:
                try:
                    score = float(payload[1])
                except (TypeError, ValueError):
                    score = 0.0
        elif isinstance(payload, str):
            text = payload
        else:
            continue
        if text.strip():
            entry: Dict[str, Any] = {"text": text, "score": score, "polygon": box}
            pts = normalize_local_polygon_v0(box)
            if pts:
                entry["local_polygon"] = pts
                entry["local_bbox"] = local_bbox_xyxy_from_polygon_v0(pts)
            items.append(entry)
    joined = " | ".join(str(x.get("text") or "") for x in items)
    return items, joined


def _unpack_rapid_engine_output(raw: Any) -> Tuple[Any, Any]:
    raw_result: Any = None
    elapse: Any = None
    if isinstance(raw, tuple):
        if len(raw) >= 2:
            raw_result, elapse = raw[0], raw[1]
        elif len(raw) == 1:
            raw_result = raw[0]
    else:
        raw_result = raw
    return raw_result, elapse


class RapidOCRProviderAdapterV0(OCRProviderAdapterV0):
    """Lightweight OCR via RapidOCR (onnxruntime or rapidocr package)."""

    @property
    def provider_name(self) -> str:
        return "rapidocr_candidate"

    @property
    def provider_level(self) -> str:
        return "lightweight"

    def supports_input_pack(self) -> bool:
        return True

    def provider_input_pack_eligible(self, input_pack: Optional[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        return evaluate_lightweight_provider_input_pack_v0(input_pack)

    def health_check(self) -> Dict[str, Any]:
        if os.environ.get("LUNA_OCR_RAPIDOCR_FORCE_UNAVAILABLE_V0", "").strip().lower() in ("1", "true", "yes", "on"):
            return {
                "ok": False,
                "availability": "unavailable",
                "provider": self.provider_name,
                "level": self.provider_level,
                "reason": "forced_unavailable_smoke_flag",
            }
        cls, imp_err = _try_import_rapidocr_class()
        if cls is None:
            return {
                "ok": False,
                "availability": "unavailable",
                "provider": self.provider_name,
                "level": self.provider_level,
                "reason": imp_err or "import_failed",
            }
        eng, err = _get_engine()
        if eng is None:
            return {
                "ok": False,
                "availability": "unavailable",
                "provider": self.provider_name,
                "level": self.provider_level,
                "reason": err or "engine_init_failed",
            }
        return {"ok": True, "availability": "available", "provider": self.provider_name, "level": self.provider_level}

    def estimate_cost(self, input_pack: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        units = (input_pack or {}).get("input_units") if isinstance(input_pack, dict) else None
        n = len(units) if isinstance(units, list) else 0
        cap = lightweight_max_edge_px_v0()
        return {
            "latency_class": "lightweight_single_pass",
            "memory_class": "low_onnx_stub_or_similar",
            "input_unit_count": n,
            "lightweight_max_edge_px": cap,
        }

    def run(
        self,
        input_pack: Optional[Dict[str, Any]],
        request: OCRRequestV0,
        deadline: Dict[str, Any],
    ) -> Dict[str, Any]:
        _ = deadline
        t0 = time.perf_counter()
        ok, reasons = self.provider_input_pack_eligible(input_pack)
        if not ok:
            return {
                "provider": self.provider_name,
                "status": "error",
                "error": "lightweight_input_pack_rejected:" + ",".join(reasons),
                "text_items": [],
                "text_joined": "",
                "duration_ms": round((time.perf_counter() - t0) * 1000.0, 3),
                "provider_raw_ref": {"reject_reasons": reasons},
                "call_method": "lightweight_runtime",
                "real_provider_invoked": False,
            }
        hc = self.health_check()
        if hc.get("availability") != "available":
            return {
                "provider": self.provider_name,
                "status": "error",
                "error": "provider_runtime_unavailable:" + str(hc.get("reason") or "unknown"),
                "text_items": [],
                "text_joined": "",
                "duration_ms": round((time.perf_counter() - t0) * 1000.0, 3),
                "provider_raw_ref": {"health_check": hc},
                "call_method": "lightweight_runtime",
                "real_provider_invoked": False,
            }
        unit = (input_pack or {}).get("input_units", [{}])[0]  # type: ignore[union-attr]
        pol = (input_pack or {}).get("processing_policy") if isinstance((input_pack or {}).get("processing_policy"), dict) else {}
        strategy = str(pol.get("strategy") or "")
        units_all = (input_pack or {}).get("input_units") if isinstance((input_pack or {}).get("input_units"), list) else []
        multi_roi = strategy == "roi_list" and len(units_all) >= 2
        img_path = str((unit or {}).get("image_ref") or "")
        eng, err = _get_engine()
        if eng is None:
            return {
                "provider": self.provider_name,
                "status": "error",
                "error": err or "engine_unavailable",
                "text_items": [],
                "text_joined": "",
                "duration_ms": round((time.perf_counter() - t0) * 1000.0, 3),
                "provider_raw_ref": {},
                "call_method": "lightweight_runtime",
                "real_provider_invoked": False,
            }
        try:
            if multi_roi:
                all_items: List[Dict[str, Any]] = []
                per_roi: List[Dict[str, Any]] = []
                joined_parts: List[str] = []
                last_elapse: Any = None
                for u in units_all:
                    if not isinstance(u, dict):
                        continue
                    upath = str(u.get("image_ref") or "")
                    uid = str(u.get("unit_id") or "")
                    rid = str(u.get("roi_id") or "")
                    raw_u = eng(upath)
                    raw_result, elapse = _unpack_rapid_engine_output(raw_u)
                    last_elapse = elapse
                    items_u, joined_u = _parse_rapid_output(raw_result)
                    st_u = "success" if items_u else "empty"
                    for it in items_u:
                        it2 = dict(it)
                        it2["unit_id"] = uid
                        it2["roi_id"] = rid
                        it2["source_unit_ref"] = upath
                        all_items.append(it2)
                    joined_parts.append(joined_u)
                    per_roi.append(
                        {
                            "unit_id": uid,
                            "roi_id": rid,
                            "status": st_u,
                            "text_joined": joined_u,
                            "text_item_count": len(items_u),
                            "source_unit_ref": upath,
                        }
                    )
                merged = " | ".join(p for p in joined_parts if str(p).strip())
                dur = round((time.perf_counter() - t0) * 1000.0, 3)
                roc = {
                    "schema_version": "ocr_reading_order_candidate_v0",
                    "strategy": "roi_order_then_provider_order",
                    "confidence": "low_to_medium",
                    "reason_codes": ["no_layout_semantics_v0"],
                }
                return {
                    "provider": self.provider_name,
                    "status": "success" if all_items else "empty",
                    "text_items": all_items,
                    "text_joined": merged,
                    "duration_ms": dur,
                    "provider_raw_ref": {
                        "rapidocr_elapse_field": last_elapse,
                        "multi_roi": True,
                        "per_roi_provider_status": per_roi,
                    },
                    "call_method": "lightweight_runtime",
                    "real_provider_invoked": True,
                    "reading_order_candidate": roc,
                    "error": None,
                }

            raw = eng(img_path)
            raw_result, elapse = _unpack_rapid_engine_output(raw)
            items, joined = _parse_rapid_output(raw_result)
            dur = round((time.perf_counter() - t0) * 1000.0, 3)
            out: Dict[str, Any] = {
                "provider": self.provider_name,
                "status": "success" if items else "empty",
                "text_items": items,
                "text_joined": joined,
                "duration_ms": dur,
                "provider_raw_ref": {"rapidocr_elapse_field": elapse, "raw_result_type": type(raw_result).__name__},
                "call_method": "lightweight_runtime",
                "real_provider_invoked": True,
                "error": None,
            }
            return out
        except Exception as e:  # noqa: BLE001
            return {
                "provider": self.provider_name,
                "status": "error",
                "error": f"rapidocr_runtime_exception:{e!s}",
                "text_items": [],
                "text_joined": "",
                "duration_ms": round((time.perf_counter() - t0) * 1000.0, 3),
                "provider_raw_ref": {},
                "call_method": "lightweight_runtime",
                "real_provider_invoked": False,
            }

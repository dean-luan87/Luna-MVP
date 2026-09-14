# -*- coding: utf-8 -*-
"""Stub Vision provider: synthetic labels only, no real inference."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .vision_provider_adapter_contract_v0 import VisionProviderAdapterV0


class VisionStubAdapterV0(VisionProviderAdapterV0):
    provider_name = "vision_stub"
    provider_level = "stub"

    def supports_input_pack(self, input_pack: Dict[str, Any]) -> bool:
        units = input_pack.get("input_units")
        return isinstance(units, list) and len(units) > 0

    def health_check(self) -> Dict[str, Any]:
        return {"status": "ok", "provider": self.provider_name, "synthetic": True}

    def estimate_cost(self, input_pack: Dict[str, Any]) -> Dict[str, Any]:
        n = len(input_pack.get("input_units") or [])
        return {"estimated_units": n, "estimated_ms_hint": 1.0, "synthetic": True}

    def run(
        self,
        input_pack: Dict[str, Any],
        request: Dict[str, Any],
        deadline: Optional[float],
    ) -> Dict[str, Any]:
        _ = request, deadline
        pack_id = str(input_pack.get("pack_id") or "")
        items: List[Dict[str, Any]] = []
        for u in input_pack.get("input_units") or []:
            if not isinstance(u, dict):
                continue
            ct = u.get("coordinate_transform") or {}
            tw = int(ct.get("transformed_width") or 0)
            th = int(ct.get("transformed_height") or 0)
            if tw <= 0:
                tw = 1
            if th <= 0:
                th = 1
            uid = str(u.get("unit_id") or "")
            rid = str(u.get("roi_id") or "")
            bbox_frame = u.get("bbox_in_frame")
            if not isinstance(bbox_frame, list) or len(bbox_frame) != 4:
                bbox_frame = [0, 0, tw, th]
            items.append(
                {
                    "unit_id": uid,
                    "roi_id": rid,
                    "label": "stub_object",
                    "confidence": 0.5,
                    "bbox_in_unit": [0, 0, tw, th],
                    "bbox_in_frame": [int(x) for x in bbox_frame],
                    "source_unit_ref": uid or f"{pack_id}:unknown_unit",
                    "synthetic": True,
                    "stub_provider": True,
                }
            )
        return {
            "schema_version": "vision_provider_stub_result_v0",
            "provider": self.provider_name,
            "input_pack_id": pack_id,
            "synthetic": True,
            "items": items,
        }


def merge_stub_results_v0(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Flatten per-pack stub results into one evaluation artifact."""
    all_items: List[Dict[str, Any]] = []
    for r in results:
        if not isinstance(r, dict):
            continue
        pid = str(r.get("input_pack_id") or "")
        for it in r.get("items") or []:
            if isinstance(it, dict):
                row = dict(it)
                row.setdefault("pack_id", pid)
                all_items.append(row)
    return {
        "schema_version": "vision_provider_stub_result_v0",
        "provider": "vision_stub",
        "input_pack_id": "vision_eval_bundle_multi_pack_v0",
        "synthetic": True,
        "items": all_items,
    }

from __future__ import annotations

from typing import Dict, Any

from predictive_attention.engine import PalOutput


def snapshot_pal_debug(pal_out: PalOutput) -> Dict[str, Any]:
    return {
        "pal_debug": {
            "enabled": pal_out.debug.get("enabled", False),
            "hint_count": len(pal_out.hints),
            "hints": [
                {
                    "roi_kind": h.roi_kind.value,
                    "priority": int(h.priority),
                    "ttl_s": h.ttl_s,
                    "confidence": h.confidence,
                    "reason_codes": h.reason_codes,
                }
                for h in pal_out.hints
            ],
            "paths": {
                "main": {
                    "segment_id": pal_out.paths.main.segment_id,
                    "avg_heading_deg": pal_out.paths.main.avg_heading_deg,
                },
                "branch": (
                    None
                    if pal_out.paths.active_branch is None
                    else {
                        "segment_id": pal_out.paths.active_branch.segment_id,
                        "avg_heading_deg": pal_out.paths.active_branch.avg_heading_deg,
                    }
                ),
            },
        }
    }

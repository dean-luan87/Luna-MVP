from __future__ import annotations

from typing import Any, Dict, List, Optional

from dynamic_view.attention import AttentionWindow
from dynamic_view.roi import RoiHint


def snapshot_roi_debug(
    attention_windows: List[AttentionWindow],
    roi_hints: List[RoiHint],
    roi_hit_entity_ids: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Debug-only ROI 快照：
    - 不参与判断
    - 只用于回放/审计
    """
    return {
        "roi_debug": {
            "attention_windows": [
                {
                    "area_type": w.area_type,
                    "hint": w.hint,
                    "ttl_frames": w.ttl_frames,
                    "source": w.source,
                    "constraints": w.constraints,
                }
                for w in attention_windows
            ],
            "roi_hints": [
                {
                    "area_type": r.area_type,
                    "hint": r.hint,
                    "weight": r.weight,
                    "source": r.source,
                    "constraints": r.constraints,
                }
                for r in roi_hints
            ],
            "roi_hit": {
                "hit": bool(roi_hit_entity_ids),
                "entity_ids": roi_hit_entity_ids or [],
            },
        }
    }

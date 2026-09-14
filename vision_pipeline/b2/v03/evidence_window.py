# vision_pipeline/b2/v03/evidence_window.py
from __future__ import annotations
from typing import List, Dict, Any

from .evidence_types import EvidenceRecord


def build_evidence_window(
    records: List[EvidenceRecord],
) -> Dict[str, Any]:
    """
    将窗口内的 EvidenceRecord 组织为"完整证据窗口"
    不压缩，不裁剪
    """

    if not records:
        return {
            "count": 0,
            "records": [],
        }

    return {
        "count": len(records),
        "start_t": records[0].t_video,
        "end_t": records[-1].t_video,
        "records": [
            {
                "t_video": r.t_video,
                "frame_idx": r.frame_idx,
                "factors": r.factors.factors,
                "confidence": r.factors.confidence,
                "continuity": {
                    "visual_ok": r.continuity.visual_ok,
                    "spatial_ok": r.continuity.spatial_ok,
                    "direction_consistent": r.continuity.direction_consistent,
                    "gps_consistent": r.continuity.gps_consistent,
                    "gps_jump_m": r.continuity.gps_jump_m,
                },
            }
            for r in records
        ],
    }


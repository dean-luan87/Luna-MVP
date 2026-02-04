# vision_pipeline/b2/v03/evidence_window_export.py
from __future__ import annotations
from typing import List, Dict, Any
import json
import os

from .evidence_types import EvidenceRecord


def export_evidence_window(
    records: List[EvidenceRecord],
    out_path: str,
) -> str:
    """
    将完整证据窗口写入文件（JSON）
    返回文件路径
    """

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    payload: Dict[str, Any] = {
        "count": len(records),
        "start_t": records[0].t_video if records else None,
        "end_t": records[-1].t_video if records else None,
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

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return out_path


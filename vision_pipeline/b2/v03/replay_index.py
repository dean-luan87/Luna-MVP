# vision_pipeline/b2/v03/replay_index.py
from __future__ import annotations
from typing import Dict, Any
import json
import os


def build_replay_index(
    timeline_event: Dict[str, Any],
    evidence_path: str,
    snapshot_dir: str,
) -> Dict[str, Any]:
    """
    生成一个"可回放索引"
    用于 UI / Debug / 人工检查
    """

    keyframes = timeline_event.get("keyframes", {})
    return {
        "t_video": timeline_event.get("t_video"),
        "t_str": timeline_event.get("t_str"),
        "decision": timeline_event.get("decision"),
        "main_factor": timeline_event.get("main_factor"),
        "confidence": timeline_event.get("confidence"),

        "evidence_path": evidence_path,

        "snapshots": {
            "before": os.path.join(snapshot_dir, "before.jpg"),
            "at": os.path.join(snapshot_dir, "at.jpg"),
            "after": os.path.join(snapshot_dir, "after.jpg"),
        },

        "keyframes": keyframes,
    }


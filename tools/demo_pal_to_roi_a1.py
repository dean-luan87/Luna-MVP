import sys
import time
from pathlib import Path

# 确保仓库根在 path，便于直接运行
_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import pal_roi_bridge.config as cfg
from pal_roi_bridge.pipeline import run_pal_roi_pipeline
from pal_roi_bridge.schema import PalRoiHint
from observe.timeline.schema import TimelineFrame
from observe.timeline_pal_roi import snapshot_pal_roi_debug


def demo():
    cfg.PAL_ROI_ENABLED = True

    pal_hints = [
        PalRoiHint(
            roi_kind="traffic_signal",
            area=(120, 80, 220, 180),
            confidence=0.82,
            reason="approaching_crosswalk",
            ttl_s=5.0,
        )
    ]

    rois = run_pal_roi_pipeline(pal_hints)
    pal_roi_debug = snapshot_pal_roi_debug(
        enabled=True,
        pal_hint_count=len(pal_hints),
        roi_hints=rois,
    ).get("pal_roi_debug", {})

    frame = TimelineFrame(
        ts=time.time(),
        entities={},
        tasks=[],
        c_decision={},
        pal_roi_debug=pal_roi_debug,
    )

    print(frame.to_json())


if __name__ == "__main__":
    demo()

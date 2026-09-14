import sys
import time
from pathlib import Path

# 确保仓库根在 path，便于直接运行
_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from observe.timeline.recorder import TimelineRecorder
from observe.timeline_roi_perception import snapshot_roi_perception_debug
from observe.timeline_roi import snapshot_roi_debug
from tools.run_dynamic_full_demo import snapshot_timeline
from dynamic_view.attention import AttentionManager, AttentionWindow
from dynamic_view.roi_adapter import attention_to_roi
from vision_perception_b1.pipeline import run_roi_perception


class _EmptyTaskEngine:
    def __init__(self):
        self.active_task = None


class _EmptyObs:
    def __init__(self):
        self.entities = {}


def main():
    timeline_fp = open("runs/roi_perception_b1.timeline.jsonl", "w", encoding="utf-8")
    recorder = TimelineRecorder(timeline_fp)

    obs = _EmptyObs()
    task_engine = _EmptyTaskEngine()
    c_decision = {}

    frame = [[0, 1], [2, 3]]
    t0 = time.time()

    # Case A: no ROI -> should not run
    attention_manager = AttentionManager()
    attention_manager.tick()
    windows = attention_manager.get()
    rois = attention_to_roi(windows)
    references = run_roi_perception(frame, rois)

    roi_debug = snapshot_roi_debug(windows, rois, None).get("roi_debug", {})
    roi_perception_debug = snapshot_roi_perception_debug(rois, references).get(
        "roi_perception_debug", {}
    )
    frame_a = snapshot_timeline(
        obs,
        task_engine,
        c_decision,
        t0,
        roi_debug=roi_debug,
        roi_perception_debug=roi_perception_debug,
    )
    recorder.record(frame_a)

    # Case B: with ROI -> should run
    attention_manager.set(
        [AttentionWindow(area_type="exit_area", hint="demo", ttl_frames=10)]
    )
    attention_manager.tick()
    windows = attention_manager.get()
    rois = attention_to_roi(windows)
    references = run_roi_perception(frame, rois)

    roi_debug = snapshot_roi_debug(windows, rois, None).get("roi_debug", {})
    roi_perception_debug = snapshot_roi_perception_debug(rois, references).get(
        "roi_perception_debug", {}
    )
    frame_b = snapshot_timeline(
        obs,
        task_engine,
        c_decision,
        t0 + 0.1,
        roi_debug=roi_debug,
        roi_perception_debug=roi_perception_debug,
    )
    recorder.record(frame_b)

    timeline_fp.close()
    print("[OK] wrote runs/roi_perception_b1.timeline.jsonl")


if __name__ == "__main__":
    main()

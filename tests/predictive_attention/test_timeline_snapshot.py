import time

from predictive_attention.context import PalContext
from predictive_attention.schema import MotionSample
from predictive_attention.engine import PredictiveAttentionEngine
from predictive_attention.path.simple_path_manager import SimplePathManager
from predictive_attention.roi.simple_roi_predictor import SimpleRoiPredictor
from observe.timeline_pal import snapshot_pal_debug


def test_timeline_snapshot_structure():
    eng = PredictiveAttentionEngine(SimplePathManager(), SimpleRoiPredictor(), enabled=True)
    now = time.time()
    ctx = PalContext(
        now_ts=now,
        motion_window=[MotionSample(ts=now - 1, position_xy=(0, 0)), MotionSample(ts=now, position_xy=(1, 0))],
    )
    out = eng.run(ctx)
    snap = snapshot_pal_debug(out)
    assert "pal_debug" in snap
    assert "enabled" in snap["pal_debug"]
    assert "paths" in snap["pal_debug"]

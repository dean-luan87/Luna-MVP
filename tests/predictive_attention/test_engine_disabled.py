import time

from predictive_attention.context import PalContext
from predictive_attention.schema import MotionSample
from predictive_attention.engine import PredictiveAttentionEngine
from predictive_attention.path.simple_path_manager import SimplePathManager
from predictive_attention.roi.simple_roi_predictor import SimpleRoiPredictor


def test_disabled_outputs_no_hints():
    eng = PredictiveAttentionEngine(SimplePathManager(), SimpleRoiPredictor(), enabled=False)
    now = time.time()
    ctx = PalContext(
        now_ts=now,
        motion_window=[MotionSample(ts=now - 1, position_xy=(0, 0)), MotionSample(ts=now, position_xy=(1, 0))],
    )
    out = eng.run(ctx)
    assert out.hints == []
    assert out.debug.get("enabled") is False

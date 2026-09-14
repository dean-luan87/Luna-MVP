import time

from predictive_attention.context import PalContext
from predictive_attention.schema import MotionSample, NavigationGoal
from predictive_attention.engine import PredictiveAttentionEngine
from predictive_attention.path.simple_path_manager import SimplePathManager
from predictive_attention.roi.simple_roi_predictor import SimpleRoiPredictor, SimpleRoiConfig


def test_hints_have_positive_ttl():
    eng = PredictiveAttentionEngine(
        SimplePathManager(),
        SimpleRoiPredictor(SimpleRoiConfig(ttl_s=2.0)),
        enabled=True,
    )
    now = time.time()
    ctx = PalContext(
        now_ts=now,
        motion_window=[MotionSample(ts=now - 1, position_xy=(0, 0)), MotionSample(ts=now, position_xy=(2, 0))],
        goal=NavigationGoal(goal_id="g", goal_type="poi", target_xy=(10, 0)),
    )
    out = eng.run(ctx)
    assert len(out.hints) >= 1
    for h in out.hints:
        assert h.ttl_s > 0
        assert h.created_ts == now

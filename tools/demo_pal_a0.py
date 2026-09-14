import time

from predictive_attention.context import PalContext
from predictive_attention.schema import MotionSample, NavigationGoal
from predictive_attention.engine import PredictiveAttentionEngine
from predictive_attention.path.simple_path_manager import SimplePathManager
from predictive_attention.roi.simple_roi_predictor import SimpleRoiPredictor
from observe.timeline_pal import snapshot_pal_debug


def _ms(ts, x, y):
    return MotionSample(ts=ts, position_xy=(x, y), source="demo", confidence=1.0)


def main():
    pm = SimplePathManager()
    rp = SimpleRoiPredictor()
    eng = PredictiveAttentionEngine(pm, rp, enabled=False)

    now = time.time()
    goal = NavigationGoal(goal_id="g1", goal_type="poi", target_xy=(10.0, 0.0), semantic="go mall")

    ctx1 = PalContext(
        now_ts=now,
        motion_window=[_ms(now - 2, 0, 0), _ms(now, 2, 0)],
        goal=goal,
    )
    out1 = eng.run(ctx1)
    print("STEP1 enabled=False hints:", len(out1.hints), snapshot_pal_debug(out1))

    eng.set_enabled(True)

    out2 = eng.run(ctx1)
    print("STEP2 enabled=True hints:", len(out2.hints), snapshot_pal_debug(out2))

    ctx3 = PalContext(
        now_ts=now + 3,
        motion_window=[_ms(now + 1, 2, 0), _ms(now + 3, 2, 2)],
        goal=goal,
    )
    out3 = eng.run(ctx3)
    print("STEP3 branch hints:", len(out3.hints), snapshot_pal_debug(out3))

    ctx4 = PalContext(
        now_ts=now + 6,
        motion_window=[_ms(now + 4, 2, 2), _ms(now + 6, 4, 2)],
        goal=goal,
    )
    out4 = eng.run(ctx4)
    print("STEP4 return hints:", len(out4.hints), snapshot_pal_debug(out4))


if __name__ == "__main__":
    main()

import time

from predictive_attention.context import PalContext
from predictive_attention.schema import MotionSample
from predictive_attention.path.simple_path_manager import SimplePathManager, SimplePathConfig


def ms(ts, x, y):
    return MotionSample(ts=ts, position_xy=(x, y), source="t", confidence=1.0)


def test_branch_created_and_closed():
    pm = SimplePathManager(SimplePathConfig(branch_angle_deg=25, return_angle_deg=15, branch_timeout_s=100))
    now = time.time()

    s1 = pm.update(PalContext(now_ts=now, motion_window=[ms(now - 1, 0, 0), ms(now, 2, 0)]))
    assert s1.main.kind.value == "main"

    s2 = pm.update(PalContext(now_ts=now + 2, motion_window=[ms(now + 1, 2, 0), ms(now + 2, 2, 2)]))
    assert s2.active_branch is not None
    assert s2.active_branch.kind.value == "branch"

    s3 = pm.update(PalContext(now_ts=now + 4, motion_window=[ms(now + 3, 2, 2), ms(now + 4, 4, 2)]))
    assert s3.active_branch is None

from dynamic_view.perception_hook import apply_roi_if_supported
from dynamic_view.roi import RoiHint


class DummyDetector:
    pass


def test_apply_roi_ignorable():
    d = DummyDetector()
    apply_roi_if_supported(d, [RoiHint(area_type="x", hint="h")])

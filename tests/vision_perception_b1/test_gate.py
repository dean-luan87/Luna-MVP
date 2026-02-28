from dynamic_view.roi import RoiHint
from vision_perception_b1.gate import should_run


def test_should_run_requires_roi():
    assert should_run([]) is False
    assert should_run([RoiHint(area_type="x", hint="h")]) is True

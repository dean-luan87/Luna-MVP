from dynamic_view.roi import RoiHint

from vision_perception_b1.crop import crop_by_roi


def test_crop_by_roi_none_bbox_returns_frame():
    frame = [[1, 2], [3, 4]]
    roi = RoiHint(area_type="x", hint="h", bbox=None)
    out = crop_by_roi(frame, roi)
    assert out == frame

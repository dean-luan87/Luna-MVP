from dynamic_view.roi import RoiHint
from vision_ocr.types import ReferenceCard
from observe.timeline_roi_perception import snapshot_roi_perception_debug


def test_roi_perception_debug_schema():
    rois = [RoiHint(area_type="exit_area", hint="h")]
    refs = [ReferenceCard(kind="vision_reference", meaning="EXIT", confidence=0.5)]
    snap = snapshot_roi_perception_debug(rois, refs)

    assert "roi_perception_debug" in snap
    data = snap["roi_perception_debug"]
    assert data["ran"] is True
    assert data["roi_count"] == 1
    assert data["reference_count"] == 1

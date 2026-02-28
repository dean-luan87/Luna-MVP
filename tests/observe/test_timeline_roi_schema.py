from observe.timeline_roi import snapshot_roi_debug
from dynamic_view.attention import AttentionWindow
from dynamic_view.roi import RoiHint


def test_timeline_roi_schema():
    attn = [AttentionWindow(area_type="platform", hint="test", ttl_frames=10)]
    rois = [RoiHint(area_type="platform", hint="test", weight=1.1)]
    snap = snapshot_roi_debug(attn, rois, ["e1"])

    assert "roi_debug" in snap
    assert snap["roi_debug"]["roi_hit"]["hit"] is True
    assert snap["roi_debug"]["roi_hit"]["entity_ids"] == ["e1"]

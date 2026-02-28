from dynamic_view.roi_adapter import attention_to_roi
from dynamic_view.attention import AttentionWindow


def test_attention_to_roi():
    rois = attention_to_roi(
        [AttentionWindow(area_type="platform", hint="test", ttl_frames=10)]
    )
    assert len(rois) == 1
    assert rois[0].area_type == "platform"
    assert rois[0].weight > 1.0

import pal_roi_bridge.config as cfg
from pal_roi_bridge.adapter import pal_hint_to_roi
from pal_roi_bridge.schema import PalRoiHint


def test_pal_roi_ttl_in_constraints():
    cfg.PAL_ROI_TTL_S = 5.0
    hint = PalRoiHint(roi_kind="exit_area", area=None, confidence=0.5, reason="x", ttl_s=10.0)
    roi = pal_hint_to_roi(hint)
    assert roi.constraints.get("ttl_s") <= cfg.PAL_ROI_TTL_S

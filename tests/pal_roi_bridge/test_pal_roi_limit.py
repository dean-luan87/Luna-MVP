from pal_roi_bridge.pipeline import run_pal_roi_pipeline
from pal_roi_bridge.schema import PalRoiHint
from pal_roi_bridge import config


def test_max_hints(monkeypatch):
    monkeypatch.setattr(config, "PAL_ROI_ENABLED", True)
    monkeypatch.setattr(config, "PAL_ROI_MAX_HINTS", 1)
    hints = [
        PalRoiHint(roi_kind="a", area=None, confidence=0.5, reason="x", ttl_s=1.0),
        PalRoiHint(roi_kind="b", area=None, confidence=0.5, reason="x", ttl_s=1.0),
        PalRoiHint(roi_kind="c", area=None, confidence=0.5, reason="x", ttl_s=1.0),
        PalRoiHint(roi_kind="d", area=None, confidence=0.5, reason="x", ttl_s=1.0),
    ]
    out = run_pal_roi_pipeline(hints)
    assert len(out) == 1

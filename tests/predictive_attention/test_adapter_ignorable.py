from predictive_attention.adapter_to_dynamic_view import to_roi_hints
from predictive_attention.schema import AttentionHint, RoiKind, RoiPriority


def test_adapter_ignorable_area():
    hints = [
        AttentionHint(
            hint_id="h1",
            roi_kind=RoiKind.EXIT_AREA,
            priority=RoiPriority.ROUTE,
            ttl_s=1.0,
            created_ts=0.0,
        )
    ]
    out = to_roi_hints(hints)
    assert len(out) == 1
    assert out[0].bbox is None

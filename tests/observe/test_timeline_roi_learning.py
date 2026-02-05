from roi_learning_c1.schema import ROIPromotionProposal
from observe.timeline_roi_learning import snapshot_roi_learning_debug


def test_snapshot_empty_proposals_is_noop():
    out = snapshot_roi_learning_debug([])
    assert out == {}


def test_snapshot_writes_debug_fields():
    proposals = [
        ROIPromotionProposal(
            roi_kind="exit_area",
            evidence={
                "appear_count": 10,
                "hit_rate": 0.4,
                "avg_latency_s": None,
                "stability": 0.2,
                "value_hits": ["roi_hit_or_reference"],
            },
            score=0.52,
            suggestion="OBSERVE",
            confidence=0.66,
        )
    ]
    out = snapshot_roi_learning_debug(proposals)
    assert "roi_learning_debug" in out
    dbg = out["roi_learning_debug"]
    assert dbg["version"] == "c1-v0"
    assert len(dbg["proposals"]) == 1
    p = dbg["proposals"][0]
    assert p["roi_kind"] == "exit_area"
    assert p["suggestion"] == "OBSERVE"

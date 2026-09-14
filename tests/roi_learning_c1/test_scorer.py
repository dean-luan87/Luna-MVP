from roi_learning_c1.scorer import score_evidence


def test_score_increases_with_hits():
    low = {"appear_count": 10, "hit_rate": 0.1, "avg_latency_s": None, "stability": 0.0}
    high = {"appear_count": 10, "hit_rate": 0.8, "avg_latency_s": None, "stability": 0.0}
    assert score_evidence(high) > score_evidence(low)

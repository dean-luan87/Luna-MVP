from roi_learning_c1.metrics import compute_roi_metrics


def test_metrics_appear_and_hit():
    frames = [
        {"roi_debug": {"roi_hints": [{"area_type": "exit_area"}], "roi_hit": {"hit": True}}},
        {
            "roi_debug": {"roi_hints": [{"area_type": "exit_area"}], "roi_hit": {"hit": False}},
            "roi_perception_debug": {"reference_count": 2},
        },
    ]
    m = compute_roi_metrics(frames)
    e = m["exit_area"]
    assert e["appear_count"] == 2
    assert e["hit_rate"] > 0.0

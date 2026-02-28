from c1_v0.analyzer import analyze_timeline


def test_analyze_timeline_suggestion_ignore():
    frames = [
        {
            "ts": 1.0,
            "roi_perception_debug": {"roi_kinds": ["bus_arrival"]},
            "roi_debug": {"roi_hit": {"hit": False}},
            "tasks": [],
            "c_decision": {},
        }
    ]
    proposals = analyze_timeline(frames, appear_norm_cap=100)
    assert proposals[0].suggestion == "IGNORE"

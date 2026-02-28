from c1_v0.analyzer import analyze_timeline


def test_analyze_timeline_proposes_on_value_event():
    frames = [
        {
            "ts": 1.0,
            "roi_perception_debug": {"roi_kinds": ["exit_area"]},
            "roi_debug": {"roi_hit": {"hit": False}},
            "tasks": [{"task": "t1", "state": "waiting"}],
            "c_decision": {"safety": "hold"},
        },
        {
            "ts": 2.5,
            "roi_perception_debug": {"roi_kinds": ["exit_area"]},
            "roi_debug": {"roi_hit": {"hit": True}},
            "tasks": [{"task": "t1", "state": "completed"}],
            "c_decision": {"safety": "pass"},
        },
    ]
    proposals = analyze_timeline(frames, appear_norm_cap=2)
    assert len(proposals) == 1
    p = proposals[0]
    assert p.roi_kind == "exit_area"
    assert p.evidence.appear_count == 2
    assert p.evidence.hit_rate > 0
    assert p.suggestion in {"PROMOTE_TO_DEFAULT", "OBSERVE"}

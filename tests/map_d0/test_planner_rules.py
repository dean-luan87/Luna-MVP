from map_d0.planner import plan_download_from_roi_debug


def test_planner_priority_boost_on_hit():
    roi_debug = {
        "roi_hints": [
            {"area_type": "platform", "hint": "test", "constraints": {}}
        ],
        "roi_hit": {"hit": True, "entity_ids": ["e1"]},
    }
    plans = plan_download_from_roi_debug(roi_debug, city="shanghai")
    assert plans[0].priority > 0.3
    assert plans[0].granularity == "medium"

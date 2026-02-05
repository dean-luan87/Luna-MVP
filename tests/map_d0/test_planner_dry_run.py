from map_d0.planner import plan_download_from_roi_debug


def test_planner_dry_run_only():
    roi_debug = {"roi_hints": [], "roi_hit": {"hit": False}}
    plans = plan_download_from_roi_debug(roi_debug)
    assert plans == []

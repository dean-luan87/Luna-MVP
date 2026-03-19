from decision_monitor.spatiotemporal_continuity_reserve import build_spatiotemporal_continuity_reserve


def _frame(**kw):
    f = {
        "state": {"state_trend": kw.get("trend", "stable"), "prev_state_summary": kw.get("prev", "—")},
        "local_task_space_grid": {"recommended_search_cell_id": kw.get("rec_cell")},
        "confirmation_input_bridge": {
            "confirmation_input_raw_text": kw.get("raw_fb"),
            "confirmation_input_type": kw.get("fb_type"),
            "confirmation_bridge_next_effect": kw.get("next_effect"),
        },
        "reasoning_tree_metrics": {"possible_tree_issue_type": kw.get("issue")},
        "recheck_planner": {"recheck_blocked": kw.get("recheck_blocked", False)},
        "object_search_interaction": {"suggested_search_zone": kw.get("zone"), "search_terminal_status": kw.get("terminal", "none")},
    }
    return f


def test_path_preserved_marks_high_or_medium():
    f = _frame(rec_cell="center_front", zone="中前", trend="stable", raw_fb=None)
    out = build_spatiotemporal_continuity_reserve(f).to_dict()
    assert out["continuity_preserved"] is True
    assert out["continuity_support_level"] in ("high", "medium")


def test_user_feedback_breaks_continuity():
    f = _frame(raw_fb="我打开了，没有", fb_type="opened_container", next_effect="advance_to_recheck", rec_cell="center_front")
    out = build_spatiotemporal_continuity_reserve(f).to_dict()
    assert out["continuity_broken"] is True
    assert out["continuity_support_level"] == "broken"


def test_recheck_blocked_marks_low():
    f = _frame(recheck_blocked=True, trend="worsening", rec_cell=None, zone=None)
    out = build_spatiotemporal_continuity_reserve(f).to_dict()
    assert out["continuity_support_level"] == "low"


def test_unknown_when_insufficient_info():
    f = _frame(rec_cell=None, zone=None, trend="shifting", raw_fb=None)
    out = build_spatiotemporal_continuity_reserve(f).to_dict()
    assert out["continuity_support_level"] == "unknown"


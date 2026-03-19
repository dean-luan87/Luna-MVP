from decision_monitor.optimization_hint import build_optimization_hint


def _mk(metrics_issue_type=None, **kw):
    m = {
        "possible_tree_issue_type": metrics_issue_type,
        "possible_tree_issue_reason": kw.get("possible_tree_issue_reason"),
        "metrics_summary": kw.get("metrics_summary", "depth=5 branch=3 dead=2 ..."),
        "tree_depth": kw.get("tree_depth", 5),
        "branch_count": kw.get("branch_count", 3),
        "dead_branch_count": kw.get("dead_branch_count", 2),
        "prune_rate": kw.get("prune_rate", 0.67),
        "feedback_node_count": kw.get("feedback_node_count", 1),
        "effective_feedback_count": kw.get("effective_feedback_count", 0),
        "resolved": kw.get("resolved", False),
        "blocked": kw.get("blocked", False),
    }
    t = {"tree_summary": "root=药瓶 flow=container_check_flow active_path=4 pruned=2"}
    return m, t


def test_high_dead_branch_ratio_maps_to_reduce_dead_branches():
    m, t = _mk("high_dead_branch_ratio", prune_rate=0.67, branch_count=3, dead_branch_count=2)
    out = build_optimization_hint(reasoning_tree_metrics=m, reasoning_structure_tree=t, whiteboxes={}).to_dict()
    assert out["optimization_hint_applied"] is True
    assert out["optimization_hint_type"] == "reduce_dead_branches"
    assert out["suggested_optimization_module"] in ("hypothesis_layer", "grid_search_expansion")
    assert out["priority_level"] in ("medium", "high")


def test_feedback_not_effective_maps_to_improve_feedback_convergence():
    m, t = _mk("feedback_not_effective", feedback_node_count=1, effective_feedback_count=0)
    out = build_optimization_hint(reasoning_tree_metrics=m, reasoning_structure_tree=t, whiteboxes={}).to_dict()
    assert out["optimization_hint_type"] == "improve_feedback_convergence"
    assert out["suggested_optimization_module"] in ("confirmation_input_bridge", "action_hint_copy")
    assert out["priority_level"] == "high"


def test_tree_too_deep_maps_to_shorten_resolution_path():
    m, t = _mk("tree_too_deep", tree_depth=7)
    out = build_optimization_hint(reasoning_tree_metrics=m, reasoning_structure_tree=t, whiteboxes={}).to_dict()
    assert out["optimization_hint_type"] == "shorten_resolution_path"
    assert out["suggested_optimization_module"] in ("action_hint_copy", "confirmation_input_bridge", "recheck_planner")


def test_blocked_without_resolution_maps_to_resolve_blocked_state():
    m, t = _mk("blocked_without_resolution", blocked=True, resolved=False)
    out = build_optimization_hint(reasoning_tree_metrics=m, reasoning_structure_tree=t, whiteboxes={}).to_dict()
    assert out["optimization_hint_type"] == "resolve_blocked_state"
    assert out["suggested_optimization_module"] in ("recheck_planner", "task_arbitration")
    assert out["priority_level"] == "high"


def test_no_issue_returns_none_not_applied():
    m, t = _mk(None)
    out = build_optimization_hint(reasoning_tree_metrics=m, reasoning_structure_tree=t, whiteboxes={}).to_dict()
    assert out["optimization_hint_type"] == "none"
    assert out["optimization_hint_applied"] is False


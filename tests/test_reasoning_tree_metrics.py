from decision_monitor.reasoning_tree_metrics import build_reasoning_tree_metrics


def _node(node_id, parent_id, node_type="hypothesis", status="active", **kw):
    d = {
        "node_id": node_id,
        "parent_node_id": parent_id,
        "node_type": node_type,
        "node_title": node_id,
        "status": status,
        "is_user_feedback_driven": kw.get("is_user_feedback_driven", False),
        "next_effect": kw.get("next_effect"),
    }
    return d


def test_converged_tree_metrics_resolved():
    tree = {
        "root_node_id": "root",
        "resolved_node_id": "res",
        "nodes": [
            _node("root", None, node_type="resolution", status="active"),
            _node("ev", "root", node_type="evidence", status="active"),
            _node("hyp", "ev", node_type="hypothesis", status="active"),
            _node("res", "root", node_type="resolution", status="resolved"),
        ],
        "active_path_node_ids": ["root", "ev", "hyp"],
        "pruned_node_ids": [],
    }
    m = build_reasoning_tree_metrics(tree)
    assert m.metrics_applied is True
    assert m.tree_depth >= 2
    assert m.resolved is True
    assert m.resolution_path_length >= 1


def test_pruned_branch_increases_dead_and_prune_rate():
    tree = {
        "root_node_id": "root",
        "resolved_node_id": None,
        "nodes": [
            _node("root", None, node_type="resolution", status="active"),
            _node("ev", "root", node_type="evidence", status="active"),
            _node("hypA", "ev", node_type="hypothesis", status="active"),
            _node("hypB", "ev", node_type="hypothesis", status="pruned"),
            _node("exB", "hypB", node_type="exclusion", status="pruned"),
        ],
        "active_path_node_ids": ["root", "ev", "hypA"],
        "pruned_node_ids": ["hypB", "exB"],
    }
    m = build_reasoning_tree_metrics(tree)
    assert m.dead_branch_count > 0
    assert m.prune_rate >= 0.0


def test_effective_feedback_count_positive_when_next_effect_advances():
    tree = {
        "root_node_id": "root",
        "resolved_node_id": None,
        "nodes": [
            _node("root", None, node_type="resolution", status="active"),
            _node("hyp", "root", node_type="hypothesis", status="active"),
            _node(
                "fb",
                "hyp",
                node_type="confirmation_input",
                status="confirmed",
                is_user_feedback_driven=True,
                next_effect="advance_to_recheck",
            ),
        ],
        "active_path_node_ids": ["root", "hyp", "fb"],
        "pruned_node_ids": [],
    }
    m = build_reasoning_tree_metrics(tree)
    assert m.feedback_node_count > 0
    assert m.effective_feedback_count > 0


def test_feedback_not_effective_rule_triggers():
    tree = {
        "root_node_id": "root",
        "resolved_node_id": None,
        "nodes": [
            _node("root", None, node_type="resolution", status="active"),
            _node("hyp", "root", node_type="hypothesis", status="active"),
            _node(
                "fb",
                "hyp",
                node_type="confirmation_input",
                status="confirmed",
                is_user_feedback_driven=True,
                next_effect="none",
            ),
        ],
        "active_path_node_ids": ["root", "hyp"],
        "pruned_node_ids": [],
    }
    m = build_reasoning_tree_metrics(tree)
    assert m.feedback_node_count > 0
    assert m.effective_feedback_count == 0
    assert m.possible_tree_issue_type in ("feedback_not_effective", None)


def test_blocked_without_resolution_rule_triggers():
    tree = {
        "root_node_id": "root",
        "resolved_node_id": None,
        "nodes": [
            _node("root", None, node_type="resolution", status="active"),
            _node("blk", "root", node_type="recheck_decision", status="blocked"),
        ],
        "active_path_node_ids": ["root", "blk"],
        "pruned_node_ids": [],
    }
    m = build_reasoning_tree_metrics(tree)
    assert m.blocked is True
    assert m.resolved is False
    assert m.possible_tree_issue_type == "blocked_without_resolution"


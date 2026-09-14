# -*- coding: utf-8 -*-
from decision_monitor.reasoning_tree_quality_overlay import build_reasoning_tree_quality_overlay


def _tree(nodes=None, active=None, pruned=None, resolved_id=None, root_id="root:1"):
    return {
        "root_node_id": root_id,
        "nodes": nodes or [],
        "active_path_node_ids": active or [],
        "pruned_node_ids": pruned or [],
        "resolved_node_id": resolved_id,
    }


def _node(nid, status="active", is_feedback=False, confidence=None):
    n = {"node_id": nid, "status": status, "node_type": "hypothesis", "node_title": nid, "is_user_feedback_driven": is_feedback}
    if confidence is not None:
        n["confidence_score"] = confidence
    return n


def test_structure_good_convergence_good():
    metrics = {
        "tree_depth": 3,
        "branch_count": 1,
        "dead_branch_count": 0,
        "prune_rate": 0.2,
        "resolution_path_length": 2,
        "active_path_length": 3,
        "resolved": True,
        "blocked": False,
        "effective_feedback_count": 2,
        "possible_tree_issue_type": None,
    }
    tree = _tree(
        nodes=[_node("a"), _node("b"), _node("c")],
        active=["a", "b", "c"],
        resolved_id="c",
    )
    out = build_reasoning_tree_quality_overlay(tree, metrics).to_dict()
    assert out["quality_grade"] == "good"
    assert out["quality_overlay_applied"] is True
    assert out["structure_score"] >= 70
    assert out["convergence_score"] >= 70


def test_structure_acceptable_convergence_acceptable():
    metrics = {
        "tree_depth": 5,
        "branch_count": 2,
        "dead_branch_count": 1,
        "prune_rate": 0.5,
        "resolution_path_length": 0,
        "active_path_length": 4,
        "resolved": False,
        "blocked": False,
        "effective_feedback_count": 1,
        "possible_tree_issue_type": None,
    }
    tree = _tree(nodes=[_node("a"), _node("b"), _node("c", "pruned")], active=["a", "b"], pruned=["c"])
    out = build_reasoning_tree_quality_overlay(tree, metrics).to_dict()
    assert out["quality_grade"] in ("acceptable", "good")
    assert out["quality_overlay_applied"] is True
    assert out["score_reason_summary"]
    assert isinstance(out["score_penalty_sources"], list)
    assert isinstance(out["score_bonus_sources"], list)


def test_deep_tree_high_dead_blocked_poor():
    metrics = {
        "tree_depth": 7,
        "branch_count": 4,
        "dead_branch_count": 3,
        "prune_rate": 0.8,
        "resolution_path_length": 0,
        "active_path_length": 6,
        "resolved": False,
        "blocked": True,
        "effective_feedback_count": 0,
        "possible_tree_issue_type": "blocked_without_resolution",
    }
    tree = _tree(
        nodes=[_node("a"), _node("b"), _node("c", "blocked"), _node("d", "pruned"), _node("e", "pruned")],
        active=["a", "b", "c"],
        pruned=["d", "e"],
    )
    out = build_reasoning_tree_quality_overlay(tree, metrics).to_dict()
    assert out["quality_grade"] == "poor"
    assert "blocked" in str(out["score_penalty_sources"])
    assert out["quality_summary"]


def test_node_quality_annotations():
    tree = _tree(
        nodes=[
            _node("active_1"),
            _node("pruned_1", "pruned"),
            _node("blocked_1", "blocked"),
            _node("feedback_1", "active", is_feedback=True),
        ],
        active=["active_1", "feedback_1"],
        pruned=["pruned_1"],
    )
    metrics = {"effective_feedback_count": 1, "tree_depth": 4}
    out = build_reasoning_tree_quality_overlay(tree, metrics).to_dict()
    ann = out.get("node_quality_annotations") or {}
    assert "pruned_1" in ann
    assert ann["pruned_1"].get("quality_flag") == "pruned"
    assert "blocked_1" in ann
    assert ann["blocked_1"].get("quality_flag") == "blocked"
    assert "feedback_1" in ann
    assert ann["feedback_1"].get("quality_flag") in ("feedback_effective", "feedback_ineffective")


def test_score_reason_penalty_bonus_non_empty():
    metrics = {
        "tree_depth": 5,
        "dead_branch_count": 2,
        "branch_count": 2,
        "prune_rate": 0.6,
        "resolved": False,
        "blocked": False,
        "effective_feedback_count": 1,
    }
    tree = _tree(nodes=[_node("a"), _node("b")], active=["a", "b"])
    out = build_reasoning_tree_quality_overlay(tree, metrics).to_dict()
    assert out["score_reason_summary"]
    assert isinstance(out["score_penalty_sources"], list)
    assert isinstance(out["score_bonus_sources"], list)
    assert out["quality_grade"] in ("good", "acceptable", "poor")

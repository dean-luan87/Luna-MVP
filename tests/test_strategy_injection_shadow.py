from decision_monitor.strategy_injection_shadow import build_strategy_injection_shadow


def _slot(target="hypothesis_layer", mode="strategy_hint", reserved=True):
    return {
        "injection_target_module": target,
        "injection_mode": mode,
        "injection_slot_reserved": reserved,
    }


def test_hypothesis_layer_strategy_hint_low_risk():
    out = build_strategy_injection_shadow(
        injection_slot=_slot("hypothesis_layer", "strategy_hint"),
        optimization_hint={"trigger_issue_type": "high_dead_branch_ratio"},
        optimization_feedback_loop=None,
        reasoning_tree_metrics={"possible_tree_issue_type": "high_dead_branch_ratio"},
        reasoning_structure_tree={},
    ).to_dict()
    assert out["shadow_applied"] is True
    assert out["expected_risk_level"] == "low"
    assert out["expected_tree_change"]
    assert out["expected_metric_change"]


def test_optimization_hint_rule_patch_medium_risk():
    out = build_strategy_injection_shadow(
        injection_slot=_slot("optimization_hint", "rule_patch"),
        optimization_hint={"trigger_issue_type": "tree_too_deep"},
        optimization_feedback_loop=None,
        reasoning_tree_metrics={"possible_tree_issue_type": "tree_too_deep"},
        reasoning_structure_tree={},
    ).to_dict()
    assert out["expected_risk_level"] == "medium"
    assert out["recommended_next_step"] in ("keep_reserved_only", "validate_with_library_when_enabled")


def test_recheck_planner_rule_patch_expected_blocked_relief():
    out = build_strategy_injection_shadow(
        injection_slot=_slot("recheck_planner", "rule_patch"),
        optimization_hint={"trigger_issue_type": "blocked_without_resolution"},
        optimization_feedback_loop=None,
        reasoning_tree_metrics={"possible_tree_issue_type": "blocked_without_resolution"},
        reasoning_structure_tree={},
    ).to_dict()
    assert "blocked" in (out["expected_issue_relief"] or "") or out["expected_issue_relief"]


def test_weight_patch_high_risk():
    out = build_strategy_injection_shadow(
        injection_slot=_slot("hypothesis_layer", "weight_patch"),
        optimization_hint={"trigger_issue_type": "high_dead_branch_ratio"},
        optimization_feedback_loop=None,
        reasoning_tree_metrics={"possible_tree_issue_type": "high_dead_branch_ratio"},
        reasoning_structure_tree={},
    ).to_dict()
    assert out["expected_risk_level"] == "high"


def test_no_slot_shadow_not_applied():
    out = build_strategy_injection_shadow(
        injection_slot=None,
        optimization_hint=None,
        optimization_feedback_loop=None,
        reasoning_tree_metrics={"possible_tree_issue_type": None},
        reasoning_structure_tree={},
    ).to_dict()
    assert out["shadow_applied"] is False


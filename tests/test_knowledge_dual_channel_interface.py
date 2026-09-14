from decision_monitor.knowledge_dual_channel_interface import build_knowledge_dual_channel_interface


def test_worth_persisting_true_generates_persist_candidate():
    ofl = {"worth_persisting_to_library": True, "validation_result": "improved", "current_issue_type": None}
    oh = {"optimization_hint_type": "reduce_dead_branches", "optimization_hint_applied": True}
    m = {"possible_tree_issue_type": None, "metrics_summary": "depth=4 ..."}
    out = build_knowledge_dual_channel_interface(optimization_feedback_loop=ofl, optimization_hint=oh, reasoning_tree_metrics=m).to_dict()
    assert out["interface_applied"] is True
    assert out["persist_candidate"]["worth_persisting"] is True
    assert out["persist_candidate"]["persist_candidate_applied"] is True


def test_issue_persists_or_no_data_triggers_external_strategy_support():
    ofl = {"worth_persisting_to_library": False, "validation_result": "not_enough_data", "current_issue_type": "high_dead_branch_ratio"}
    oh = {"optimization_hint_type": "reduce_dead_branches", "optimization_hint_applied": True, "trigger_issue_type": "high_dead_branch_ratio"}
    m = {"possible_tree_issue_type": "high_dead_branch_ratio"}
    out = build_knowledge_dual_channel_interface(optimization_feedback_loop=ofl, optimization_hint=oh, reasoning_tree_metrics=m).to_dict()
    assert out["optimization_candidate"]["needs_external_strategy_support"] is True
    assert out["optimization_candidate"]["optimization_candidate_applied"] is True


def test_injection_slot_reserved_and_non_empty():
    ofl = {"validation_result": "unchanged", "current_issue_type": "too_many_branches"}
    oh = {"optimization_hint_type": "reduce_over_branching", "optimization_hint_applied": True}
    m = {"possible_tree_issue_type": "too_many_branches"}
    out = build_knowledge_dual_channel_interface(optimization_feedback_loop=ofl, optimization_hint=oh, reasoning_tree_metrics=m).to_dict()
    slot = out["injection_slot"]
    assert slot["injection_slot_reserved"] is True
    assert slot["injection_target_module"]
    assert slot["injection_mode"]


def test_no_obvious_candidates_still_returns_structure():
    out = build_knowledge_dual_channel_interface(optimization_feedback_loop=None, optimization_hint=None, reasoning_tree_metrics=None).to_dict()
    assert out["interface_applied"] is True
    assert out["persist_candidate"] is not None
    assert out["optimization_candidate"] is not None
    assert out["injection_slot"]["injection_slot_reserved"] is True


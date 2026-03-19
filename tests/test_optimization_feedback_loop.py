from decision_monitor.optimization_feedback_loop import build_optimization_feedback_loop


def _hint(applied=True, typ="reduce_dead_branches"):
    return {
        "optimization_hint_applied": applied,
        "optimization_hint_type": typ,
        "suggested_optimization_module": "hypothesis_layer",
        "suggested_optimization_action": "tighten weak-hypothesis entry threshold",
        "trigger_issue_type": "high_dead_branch_ratio",
    }


def _metrics(issue="high_dead_branch_ratio", depth=5, branch=3, dead=2, res_len=0, eff_fb=2, prune=0.67):
    return {
        "possible_tree_issue_type": issue,
        "tree_depth": depth,
        "branch_count": branch,
        "dead_branch_count": dead,
        "resolution_path_length": res_len,
        "effective_feedback_count": eff_fb,
        "prune_rate": prune,
        "metrics_summary": f"depth={depth} branch={branch} dead={dead} prune_rate={prune}",
    }


def test_improved_marks_library_candidate_when_issue_disappears():
    hint = _hint()
    baseline = {
        "tree_depth": 6,
        "branch_count": 3,
        "dead_branch_count": 3,
        "resolution_path_length": 0,
        "effective_feedback_count": 1,
        "prune_rate": 0.8,
        "issue_type": "high_dead_branch_ratio",
    }
    cur = _metrics(issue=None, depth=5, dead=1, eff_fb=2, prune=0.4)
    out = build_optimization_feedback_loop(optimization_hint=hint, reasoning_tree_metrics=cur, baseline=baseline).to_dict()
    assert out["validation_result"] == "improved"
    assert out["improvement_detected"] is True
    assert out["worth_persisting_to_library"] is True
    assert out["suggested_next_step"] in ("persist_to_library_candidate", "keep_observing")


def test_regressed_detected():
    hint = _hint()
    baseline = {"tree_depth": 5, "branch_count": 3, "dead_branch_count": 1, "resolution_path_length": 0, "effective_feedback_count": 2, "prune_rate": 0.3, "issue_type": None}
    cur = _metrics(issue="high_dead_branch_ratio", depth=6, dead=3, eff_fb=1, prune=0.8)
    out = build_optimization_feedback_loop(optimization_hint=hint, reasoning_tree_metrics=cur, baseline=baseline).to_dict()
    assert out["validation_result"] == "regressed"
    assert out["regression_detected"] is True
    assert out["worth_persisting_to_library"] is False


def test_unchanged_when_mixed_signals():
    hint = _hint()
    baseline = {"tree_depth": 5, "branch_count": 3, "dead_branch_count": 2, "resolution_path_length": 0, "effective_feedback_count": 2, "prune_rate": 0.67, "issue_type": "high_dead_branch_ratio"}
    cur = _metrics(issue="high_dead_branch_ratio", depth=4, dead=3, eff_fb=2, prune=0.67)
    out = build_optimization_feedback_loop(optimization_hint=hint, reasoning_tree_metrics=cur, baseline=baseline).to_dict()
    assert out["validation_result"] == "unchanged"


def test_not_enough_data_without_baseline():
    hint = _hint()
    cur = _metrics()
    out = build_optimization_feedback_loop(optimization_hint=hint, reasoning_tree_metrics=cur, baseline=None).to_dict()
    assert out["validation_result"] == "not_enough_data"
    assert out["suggested_next_step"] == "validate_with_more_samples"


def test_not_applicable_when_no_hint():
    out = build_optimization_feedback_loop(optimization_hint=None, reasoning_tree_metrics=_metrics(), baseline=None).to_dict()
    assert out["validation_result"] == "not_applicable"


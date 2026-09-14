# -*- coding: utf-8 -*-

from tools.benchmark_triage_board import build_triage_board


def test_case_ranking_poor_and_blocked_first():
    results = [
        {
            "case_id": "c_ok",
            "case_type": "general_search",
            "quality_grade": "acceptable",
            "issue_type": "high_dead_branch_ratio",
            "optimization_hint_module": "hypothesis_layer",
            "optimization_hint_type": "reduce_dead_branches",
            "blocked": False,
        },
        {
            "case_id": "c_blocked",
            "case_type": "blocked_or_fallback",
            "quality_grade": "poor",
            "issue_type": "blocked_without_resolution",
            "optimization_hint_module": "recheck_planner",
            "optimization_hint_type": "resolve_blocked_state",
            "blocked": True,
        },
    ]
    board = build_triage_board(results)
    assert board.ranked_cases[0].case_id == "c_blocked"
    assert board.ranked_cases[0].priority_level in ("high", "medium")


def test_module_ranking_aggregates_poor_cases():
    results = [
        {
            "case_id": "c1",
            "quality_grade": "poor",
            "issue_type": "feedback_not_effective",
            "optimization_hint_module": "confirmation_input_bridge",
        },
        {
            "case_id": "c2",
            "quality_grade": "poor",
            "issue_type": "blocked_without_resolution",
            "optimization_hint_module": "recheck_planner",
        },
        {
            "case_id": "c3",
            "quality_grade": "acceptable",
            "issue_type": "high_dead_branch_ratio",
            "optimization_hint_module": "hypothesis_layer",
        },
        {
            "case_id": "c4",
            "quality_grade": "poor",
            "issue_type": "feedback_not_effective",
            "optimization_hint_module": "confirmation_input_bridge",
        },
    ]
    board = build_triage_board(results)
    assert board.ranked_modules
    assert board.ranked_modules[0].module_name in ("confirmation_input_bridge", "recheck_planner")
    assert board.next_focus_modules


def test_issue_ranking_blocked_is_highest():
    results = [
        {"case_id": "a", "quality_grade": "poor", "issue_type": "high_dead_branch_ratio", "optimization_hint_module": "hypothesis_layer"},
        {"case_id": "b", "quality_grade": "poor", "issue_type": "blocked_without_resolution", "optimization_hint_module": "recheck_planner", "blocked": True},
        {"case_id": "c", "quality_grade": "acceptable", "issue_type": "high_dead_branch_ratio", "optimization_hint_module": "hypothesis_layer"},
    ]
    board = build_triage_board(results)
    assert board.ranked_issues
    assert board.ranked_issues[0].issue_type == "blocked_without_resolution"
    assert board.next_focus_issue_types


def test_next_focus_outputs_present():
    results = [
        {"case_id": "a", "quality_grade": "poor", "issue_type": "blocked_without_resolution", "optimization_hint_module": "recheck_planner", "blocked": True},
        {"case_id": "b", "quality_grade": "poor", "issue_type": "feedback_not_effective", "optimization_hint_module": "confirmation_input_bridge"},
        {"case_id": "c", "quality_grade": "acceptable", "issue_type": "high_dead_branch_ratio", "optimization_hint_module": "hypothesis_layer"},
    ]
    board = build_triage_board(results)
    assert board.next_focus_case_ids
    assert board.next_focus_modules
    assert board.next_focus_issue_types
    assert board.triage_summary


def test_summary_consistent_with_ranking():
    results = [
        {"case_id": "a", "quality_grade": "poor", "issue_type": "blocked_without_resolution", "optimization_hint_module": "recheck_planner", "blocked": True},
        {"case_id": "b", "quality_grade": "acceptable", "issue_type": "high_dead_branch_ratio", "optimization_hint_module": "hypothesis_layer"},
    ]
    board = build_triage_board(results)
    assert "a" in (board.triage_summary or "")


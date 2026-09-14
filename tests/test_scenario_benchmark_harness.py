# -*- coding: utf-8 -*-

from tools.scenario_benchmark_harness import (
    ScenarioBenchmarkCase,
    evaluate_case,
    run_cases,
    summarize_results,
)


def test_single_case_runs():
    c = ScenarioBenchmarkCase(
        case_id="T1",
        case_name="single",
        case_type="general_search",
        input_mode="synthetic",
        focus_text="keys",
        expected_quality_floor=None,
        expected_issue_type=None,
        ctx={"frame_seq": 1, "current_ts": 0.0, "trace_anchor_id": "t1", "focus_object_label": "keys"},
    )
    r = evaluate_case(c)
    assert r.case_id == "T1"
    assert r.quality_grade in ("good", "acceptable", "poor", None)
    assert isinstance(r.tree_depth, int)


def test_group_runs_and_summary():
    cases = [
        ScenarioBenchmarkCase(
            case_id="T2a",
            case_name="a",
            case_type="feedback_effective",
            input_mode="synthetic",
            focus_text="bottle",
            expected_quality_floor=None,
            expected_issue_type=None,
            ctx={
                "frame_seq": 1,
                "current_ts": 0.0,
                "trace_anchor_id": "t2a",
                "focus_object_label": "bottle",
                "confirmation_input_raw_text": "找到了",
                "confirmation_input_type": "target_found",
            },
        ),
        ScenarioBenchmarkCase(
            case_id="T2b",
            case_name="b",
            case_type="blocked_or_fallback",
            input_mode="synthetic",
            focus_text="bottle",
            expected_quality_floor=None,
            expected_issue_type=None,
            ctx={
                "frame_seq": 1,
                "current_ts": 0.0,
                "trace_anchor_id": "t2b",
                "focus_object_label": "bottle",
                "minimum_mode_active": True,
            },
        ),
    ]
    results, summary = run_cases(cases)
    assert len(results) == 2
    assert summary["total_cases"] == 2
    assert "quality_grade_distribution" in summary


def test_pass_rule_quality_floor():
    c = ScenarioBenchmarkCase(
        case_id="T3",
        case_name="floor",
        case_type="feedback_effective",
        input_mode="synthetic",
        expected_quality_floor="acceptable",
        expected_issue_type=None,
        ctx={
            "frame_seq": 1,
            "current_ts": 0.0,
            "trace_anchor_id": "t3",
            "focus_object_label": "bottle",
            "confirmation_input_raw_text": "找到了",
            "confirmation_input_type": "target_found",
        },
    )
    r = evaluate_case(c)
    assert r.scenario_passed is True


def test_pass_rule_expected_issue_type():
    c = ScenarioBenchmarkCase(
        case_id="T4",
        case_name="issue",
        case_type="blocked_or_fallback",
        input_mode="synthetic",
        expected_quality_floor=None,
        expected_issue_type="__impossible_issue__",
        ctx={
            "frame_seq": 1,
            "current_ts": 0.0,
            "trace_anchor_id": "t4",
            "focus_object_label": "bottle",
            "minimum_mode_active": True,
        },
    )
    r = evaluate_case(c)
    # expected_issue_type 存在时，pass 只看 issue 是否命中（不做复杂容错）
    assert r.scenario_passed is False


def test_summary_distributions():
    from tools.scenario_benchmark_harness import ScenarioBenchmarkResult

    results = [
        ScenarioBenchmarkResult(case_id="a", case_type="x", focus_text=None, quality_grade="good", issue_type=None, scenario_passed=True),
        ScenarioBenchmarkResult(case_id="b", case_type="x", focus_text=None, quality_grade="poor", issue_type="blocked_without_resolution", scenario_passed=False),
    ]
    s = summarize_results(results)
    assert s["total_cases"] == 2
    assert s["quality_grade_distribution"]["good"] == 1
    assert s["quality_grade_distribution"]["poor"] == 1
    assert s["issue_type_distribution"]["none"] == 1
    assert s["issue_type_distribution"]["blocked_without_resolution"] == 1


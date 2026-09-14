# -*- coding: utf-8 -*-
"""M0.7：多步反馈/背离/任务插入场景下的 recheck 收敛（R17/R18/R19）回归。"""

from __future__ import annotations

from tools.real_scenario_pack import run_real_cases


def test_r17_r18_r19_issue_removed() -> None:
    for case_id in (
        "R17_multi_step_feedback_repair_real",
        "R18_user_system_divergence_real",
        "R19_task_insertion_interrupt_real",
    ):
        results, _ = run_real_cases(case_id)
        assert len(results) == 1
        r = results[0]
        assert r.scenario_passed is True
        assert r.issue_type is None
        assert r.quality_grade == "acceptable"
        assert r.blocked is False


def test_regression_r11_r14_r16_and_r1_r2() -> None:
    # M0.6 + M0.5 边界：这些 case 不应回归为 blocked_without_resolution
    regress = (
        "R11_occlusion_plus_competition_real",
        "R14_task_chain_shift_complex_real",
        "R16_continuity_break_recovery_real",
        "R6_blocked_or_fallback_real",
        "R5_feedback_ineffective_real",
        "R1_container_real",
        "R2_occlusion_real",
    )
    for case_id in regress:
        results, _ = run_real_cases(case_id)
        assert len(results) == 1
        r = results[0]
        assert r.issue_type is None
        assert r.quality_grade == "acceptable"

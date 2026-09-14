# -*- coding: utf-8 -*-
"""M0.6：高失稳/中断场景下 recheck 收口回归。"""

from tools.real_scenario_pack import run_real_cases


def test_unstable_interrupt_cases_no_blocked_without_resolution() -> None:
    for case_id in (
        "R11_occlusion_plus_competition_real",
        "R14_task_chain_shift_complex_real",
        "R16_continuity_break_recovery_real",
    ):
        results, _ = run_real_cases(case_id)
        assert len(results) == 1
        r = results[0]
        assert r.issue_type is None
        assert r.quality_grade == "acceptable"
        assert r.blocked is False

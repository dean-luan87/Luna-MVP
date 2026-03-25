# -*- coding: utf-8 -*-
"""M0.7 第八批真实场景：最小可加载 / 可跑通校验（非大规模测试工程）。"""

from tools.real_scenario_pack import CTX_DIR, default_real_cases, run_real_cases

M07_CASE_IDS = (
    "R41_confirmed_but_long_term_diverged_real",
    "R42_task_subtask_fact_shift_real",
    "R43_success_condition_overwritten_real",
    "R44_false_multi_recovery_real",
    "R45_multi_feedback_source_conflict_real",
    "R46_delayed_exposure_mismatch_real",
)


def test_m07_cases_registered_in_pack():
    ids = {c.case_id for c, _ in default_real_cases()}
    for cid in M07_CASE_IDS:
        assert cid in ids


def test_m07_ctx_json_files_exist():
    for cid in M07_CASE_IDS:
        p = CTX_DIR / f"{cid}_ctx.json"
        assert p.is_file(), f"missing {p}"


def test_m07_sample_case_builds():
    results, summary = run_real_cases("R46_delayed_exposure_mismatch_real")
    assert len(results) == 1
    assert results[0].case_id == "R46_delayed_exposure_mismatch_real"
    assert summary["total_cases"] == 1

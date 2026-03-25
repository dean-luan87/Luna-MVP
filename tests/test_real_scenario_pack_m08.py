# -*- coding: utf-8 -*-
"""M0.8 第九批真实场景：最小可加载 / 可跑通校验。"""

from tools.real_scenario_pack import CTX_DIR, default_real_cases, run_real_cases

M08_CASE_IDS = (
    "R47_gradual_goal_drift_real",
    "R48_local_recovery_global_mismatch_real",
    "R49_multi_constraint_soft_shift_real",
    "R50_feedback_fact_consistent_but_wrong_real",
    "R51_task_semantic_crack_real",
    "R52_slow_poisoning_real",
)


def test_m08_cases_registered_in_pack():
    ids = {c.case_id for c, _ in default_real_cases()}
    for cid in M08_CASE_IDS:
        assert cid in ids


def test_m08_ctx_json_files_exist():
    for cid in M08_CASE_IDS:
        p = CTX_DIR / f"{cid}_ctx.json"
        assert p.is_file(), f"missing {p}"


def test_m08_sample_case_builds():
    results, summary = run_real_cases("R52_slow_poisoning_real")
    assert len(results) == 1
    assert results[0].case_id == "R52_slow_poisoning_real"
    assert summary["total_cases"] == 1

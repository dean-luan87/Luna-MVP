# -*- coding: utf-8 -*-
"""M0.5：hold_for_floor + fine_interaction 下 hypothesis 分支收敛（R8/R10 回归）。"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.real_scenario_pack import run_real_cases


CTX_DIR = Path(__file__).resolve().parent / "real_scenarios" / "ctx"


def _load_ctx(name: str) -> dict:
    return json.loads((CTX_DIR / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "case_id,ctx_file",
    [
        ("R8_multi_candidate_container_real", "R8_multi_candidate_container_real_ctx.json"),
        ("R10_partial_memory_vs_novel_real", "R10_partial_memory_vs_novel_real_ctx.json"),
    ],
)
def test_hold_floor_fine_collapses_high_dead_branch_ratio(case_id: str, ctx_file: str) -> None:
    ctx = _load_ctx(ctx_file)
    assert ctx.get("detector_floor_due") is True, "fixture must use hold_for_floor pressure"

    results, _ = run_real_cases(case_id)
    assert len(results) == 1
    r = results[0]
    assert r.scenario_passed is True
    assert r.issue_type is None
    assert r.prune_rate is not None and r.prune_rate <= 0.6
    assert (r.dead_branch_count or 0) <= 1

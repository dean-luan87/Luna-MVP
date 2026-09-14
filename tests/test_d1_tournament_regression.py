# -*- coding: utf-8 -*-
"""
Phase 2 回归：D1 Tournament 在固定 seed + 固定 suite 下 champion_id 一致；
rank_report.json 含关键字段；lexicographic_ranker 单元测试。
"""
import json
import tempfile
from pathlib import Path

import pytest

from simulation.d1.lexicographic_ranker import rank_candidates


def _mock_suite_report(
    overall: bool = True,
    early_gain_mean: float = 0.1,
    dwell_p95_delta: float = 0.0,
    volatility_mean: float = 0.05,
    guarded_ratio_delta_mean: float = 0.0,
) -> dict:
    """构造带 per_episode scorecard_path 的 mock suite_report（rank_candidates 会读 scorecard 聚合）。"""
    return {
        "overall": overall,
        "overall_fail_reasons": [] if overall else ["BUCKET_FAIL:low_light:ep1:[]"],
        "per_episode": {
            "ep1": {
                "scorecard_path": None,
                "gate_result_path": None,
                "passed": overall,
            },
        },
    }


def _mock_scorecard_path(tmp_path: Path, early_gain: float, dwell_p95_delta: float, vol: float, gr_delta: float) -> str:
    sc = {
        "early": {"early_gain_weighted": early_gain, "weighted_early_gain_available": True},
        "event_metrics": {"delta": {"dwell_p95_delta": dwell_p95_delta}},
        "volatility_index": vol,
        "efficiency": {"guarded_ratio_delta": gr_delta},
    }
    p = tmp_path / "scorecard.json"
    p.write_text(json.dumps(sc, ensure_ascii=False), encoding="utf-8")
    return str(p)


@pytest.fixture
def run_dir_with_mock_reports(tmp_path):
    """在 tmp_path 下建 baseline/aggressive/conservative 三个目录，各含 suite_report.json（含可读 scorecard_path）。"""
    # baseline: early=0.08, dwell_delta=0, vol=0.04, gr=0
    # aggressive: early=0.12, dwell_delta=2, vol=0.08, gr=0.02
    # conservative: early=0.10, dwell_delta=-1, vol=0.03, gr=-0.01
    base = tmp_path / "run"
    base.mkdir()
    for pid, early, dwell, vol, gr in [
        ("baseline", 0.08, 0.0, 0.04, 0.0),
        ("aggressive", 0.12, 2.0, 0.08, 0.02),
        ("conservative", 0.10, -1.0, 0.03, -0.01),
    ]:
        (base / pid).mkdir()
        sc_path = _mock_scorecard_path(base / pid, early, dwell, vol, gr)
        report = {
            "overall": True,
            "overall_fail_reasons": [],
            "per_episode": {"ep1": {"scorecard_path": sc_path, "gate_result_path": None, "passed": True}},
        }
        (base / pid / "suite_report.json").write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        (base / pid / "patch.json").write_text("{}", encoding="utf-8")
    return base


def test_lexicographic_ranker_discovers_and_ranks(run_dir_with_mock_reports):
    """rank_candidates(run_dir) 能发现 * /suite_report.json，按 L1(early↑) L2(dwell_p95_delta↓,vol↓) L3(gr_delta↓) 排序。"""
    run_dir = run_dir_with_mock_reports
    out = rank_candidates(run_dir, candidate_results=None)
    assert "champion_id" in out
    assert "ranked" in out
    assert "eliminated" in out
    # L1 最大化 early_gain → aggressive(0.12) 应排第一
    assert out["champion_id"] == "aggressive"
    ranked = out["ranked"]
    assert len(ranked) == 3
    ids = [r["patch_id"] for r in ranked]
    assert ids[0] == "aggressive"
    # L2/L3 次要：conservative 的 dwell_delta 最小(-1)，应第二
    assert ids[1] == "conservative"
    assert ids[2] == "baseline"

    json_path = run_dir / "rank_report.json"
    assert json_path.is_file()
    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["champion_id"] == "aggressive"
    assert "ranked" in data and len(data["ranked"]) == 3

    md_path = run_dir / "rank_report.md"
    assert md_path.is_file()
    assert "Champion" in md_path.read_text(encoding="utf-8")


def test_lexicographic_ranker_l0_eliminates_fail(tmp_path):
    """L0：overall=False 的候选被淘汰，不进入 ranked。"""
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "pass").mkdir()
    (run_dir / "fail").mkdir()
    sc_ok = _mock_scorecard_path(run_dir / "pass", 0.1, 0.0, 0.05, 0.0)
    report_ok = {"overall": True, "overall_fail_reasons": [], "per_episode": {"ep1": {"scorecard_path": sc_ok, "passed": True}}}
    (run_dir / "pass" / "suite_report.json").write_text(json.dumps(report_ok), encoding="utf-8")
    (run_dir / "pass" / "patch.json").write_text("{}")
    report_fail = {"overall": False, "overall_fail_reasons": ["BUCKET_FAIL:x:y:[]"], "per_episode": {}}
    (run_dir / "fail" / "suite_report.json").write_text(json.dumps(report_fail), encoding="utf-8")
    (run_dir / "fail" / "patch.json").write_text("{}")

    out = rank_candidates(run_dir, candidate_results=None)
    assert out["champion_id"] == "pass"
    assert len(out["ranked"]) == 1
    assert len(out["eliminated"]) == 1
    assert out["eliminated"][0]["patch_id"] == "fail"
    assert "gate_fail" in out["eliminated"][0]["reason"]


def test_rank_report_schema():
    """rank_report.json 必须包含 champion_id, ranked, eliminated；ranked 项含 aggregated 与 sort_reason。"""
    with tempfile.TemporaryDirectory() as d:
        run_dir = Path(d) / "r"
        run_dir.mkdir()
        (run_dir / "only").mkdir()
        sc_path = _mock_scorecard_path(run_dir / "only", 0.05, 0.0, 0.02, 0.0)
        report = {"overall": True, "overall_fail_reasons": [], "per_episode": {"ep1": {"scorecard_path": sc_path, "passed": True}}}
        (run_dir / "only" / "suite_report.json").write_text(json.dumps(report), encoding="utf-8")
        (run_dir / "only" / "patch.json").write_text("{}")

        out = rank_candidates(run_dir, candidate_results=None)
        assert "champion_id" in out
        assert "ranked" in out
        assert "eliminated" in out
        if out["ranked"]:
            r = out["ranked"][0]
            assert "aggregated" in r
            assert "sort_reason" in r
            assert "early_gain_weighted_mean" in r["aggregated"]
            assert "dwell_p95_delta_mean" in r["aggregated"]

import json
from pathlib import Path

from decision_monitor.builder import DecisionMonitorBuilder


ROOT = Path(__file__).resolve().parents[1]


def _load_ctx(name: str) -> dict:
    p = ROOT / "tests" / "real_scenarios" / "ctx" / name
    return json.loads(p.read_text(encoding="utf-8"))


def test_advisory_review_observation_positive_hits_sf1_prime() -> None:
    ctx = _load_ctx("R89_advisory_candidate_resume_fragility_global_stall_real_ctx.json")
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    adv = frame.get("advisory_review_observation") or {}
    assert adv.get("advisory_review_observation_applied") is True
    assert adv.get("soft_fail_candidate_observed") is True
    assert adv.get("soft_fail_candidate_clause_id") == "SF-1-prime"
    assert adv.get("review_gate_recommended") is True
    assert adv.get("advisory_only") is True


def test_advisory_review_observation_near_neighbor_not_misflagged() -> None:
    ctx = _load_ctx("R90_advisory_candidate_near_miss_pc_high_lg_medium_real_ctx.json")
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    adv = frame.get("advisory_review_observation") or {}
    assert adv.get("advisory_review_observation_applied") is True
    assert adv.get("soft_fail_candidate_observed") is False
    assert adv.get("review_gate_recommended") is False
    assert adv.get("advisory_only") is True


def test_advisory_review_observation_healthy_terminal_found_not_misflagged() -> None:
    ctx = _load_ctx("R91_complex_resume_chain_but_healthy_terminal_real_ctx.json")
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    adv = frame.get("advisory_review_observation") or {}
    assert adv.get("advisory_review_observation_applied") is True
    assert adv.get("soft_fail_candidate_observed") is False
    assert adv.get("review_gate_recommended") is False
    assert adv.get("advisory_only") is True


def test_advisory_observation_does_not_change_pass_fail_fields() -> None:
    ctx = _load_ctx("R89_advisory_candidate_resume_fragility_global_stall_real_ctx.json")
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    # 本接入不应引入 benchmark/hard-fail 字段或修改主链判定。
    assert isinstance(frame.get("decision"), dict)
    assert frame.get("decision", {}).get("decision_owner") is not None
    assert isinstance(frame.get("run_summary_reference"), dict)

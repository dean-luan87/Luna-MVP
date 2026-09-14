from luna_badge_v1_2.governance.output_controller.ability_matrix import AuthorityLevel
from luna_badge_v1_2.governance.output_controller.authority_hysteresis import apply_authority_hysteresis
from luna_badge_v1_2.governance.output_controller.controller import build_ability_mask
from luna_badge_v1_2.governance.output_controller.distortion_report import DistortionReport


def _distortion_ok():
    return DistortionReport(
        distorted=False,
        severity="LOW",
        reason_codes=[],
        recommended_action="NONE",
    )


def test_risk_blocks_recovery():
    history = [{"ts": 0.0, "raw": "A5", "effective": "A5", "since": 0.0}]
    result = apply_authority_hysteresis(
        raw_authority=AuthorityLevel.A4,
        authority_history=history,
        distortion_report=_distortion_ok(),
        now_ts=100.0,
        risk_context={"risk_present": True, "risk_level": "HIGH"},
    )
    assert result == AuthorityLevel.A5


def test_risk_does_not_prevent_downgrade():
    history = [{"ts": 0.0, "raw": "A3", "effective": "A3", "since": 0.0}]
    result = apply_authority_hysteresis(
        raw_authority=AuthorityLevel.A5,
        authority_history=history,
        distortion_report=_distortion_ok(),
        now_ts=10.0,
        risk_context={"risk_present": True, "risk_level": "HIGH"},
    )
    assert result == AuthorityLevel.A5


def test_risk_does_not_change_ability_directly():
    history = [{"ts": 0.0, "raw": "A2", "effective": "A2", "since": 0.0}]
    result = apply_authority_hysteresis(
        raw_authority=AuthorityLevel.A2,
        authority_history=history,
        distortion_report=_distortion_ok(),
        now_ts=10.0,
        risk_context={"risk_present": True, "risk_level": "HIGH"},
    )
    assert build_ability_mask(result) == build_ability_mask(AuthorityLevel.A2)

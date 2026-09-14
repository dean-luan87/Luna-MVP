from luna_badge_v1_2.governance.output_controller.debug_view import build_debug_view
from luna_badge_v1_2.governance.output_controller.ability_matrix import AbilityMask, AuthorityLevel
from luna_badge_v1_2.governance.risk_center.interfaces.signal import EnvelopeSignal


def test_risk_panel_level_none_when_not_present():
    view = build_debug_view(
        raw_authority=AuthorityLevel.A2,
        effective_authority=AuthorityLevel.A2,
        blocked_by=None,
        authority_since=0.0,
        risk_signal=EnvelopeSignal(False, "LOW", "VISION", "UNKNOWN", None, []),
        gate_blocked=False,
        abilities=AbilityMask(
            allow_b_input=True,
            allow_c_input=False,
            allow_arbitration=True,
            allow_shaping=False,
            allow_output=True,
            allow_voice=False,
        ),
        attempting_recovery=False,
        distortion_distorted=False,
        envelope_signal={},
        risk_vo={},
    )
    assert view["risk_panel"]["level"] == "NONE"

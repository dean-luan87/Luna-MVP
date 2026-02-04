from luna_badge_v1_2.governance.output_controller.debug_view import build_debug_view
from luna_badge_v1_2.governance.output_controller.ability_matrix import AbilityMask, AuthorityLevel
from luna_badge_v1_2.governance.risk_center.interfaces.signal import EnvelopeSignal


def test_envelope_panel_priority():
    view = build_debug_view(
        raw_authority=AuthorityLevel.A3,
        effective_authority=AuthorityLevel.A4,
        blocked_by="HYSTERESIS",
        authority_since=0.0,
        risk_signal=EnvelopeSignal(True, "MEDIUM", "VISION", "RELATIVE_MOTION", 1.0, []),
        gate_blocked=True,
        abilities=AbilityMask(
            allow_b_input=True,
            allow_c_input=False,
            allow_arbitration=True,
            allow_shaping=False,
            allow_output=False,
            allow_voice=False,
        ),
        attempting_recovery=True,
        distortion_distorted=True,
        envelope_signal={"status": "UNACCEPTABLE"},
        risk_vo={},
    )
    panel = view["envelope_panel"]
    assert panel["within_envelope"] is False
    assert panel["envelope_reason"] == "HARD_GATE"

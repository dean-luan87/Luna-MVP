from luna_badge_v1_2.governance.output_controller.debug_view import build_debug_view
from luna_badge_v1_2.governance.output_controller.ability_matrix import AbilityMask, AuthorityLevel
from luna_badge_v1_2.governance.risk_center.interfaces.signal import EnvelopeSignal


def test_debug_view_schema_version_from_dump():
    view = build_debug_view(
        raw_authority=AuthorityLevel.A3,
        effective_authority=AuthorityLevel.A4,
        blocked_by="RISK",
        authority_since=0.0,
        risk_signal=EnvelopeSignal(True, "MEDIUM", "VISION", "RELATIVE_MOTION", 1.0, ["CURVATURE_BREAKS_CPA"]),
        gate_blocked=False,
        abilities=AbilityMask(
            allow_b_input=True,
            allow_c_input=False,
            allow_arbitration=True,
            allow_shaping=False,
            allow_output=True,
            allow_voice=False,
        ),
        attempting_recovery=True,
        distortion_distorted=False,
        envelope_signal={"status": "WITHIN_ENVELOPE"},
        risk_vo={"level": "NONE"},
    )
    assert "authority_panel" in view
    assert "envelope" in view

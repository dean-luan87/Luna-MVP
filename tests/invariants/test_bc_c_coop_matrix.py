from luna_badge_v1_2.governance.output_controller.ability_matrix import AuthorityLevel
from luna_badge_v1_2.governance.output_controller.bc_c_coop import (
    can_execute_b_candidates,
    resolve_bc_action,
)


def test_c_stop_always_force_stop():
    for level in AuthorityLevel:
        assert resolve_bc_action(level, "STOP") == "FORCE_STOP"
        assert not can_execute_b_candidates(level, "STOP")


def test_c_request_takeover_always_blocks_execution():
    for level in AuthorityLevel:
        assert resolve_bc_action(level, "REQUEST_TAKEOVER") == "REQUEST_TAKEOVER"
        assert not can_execute_b_candidates(level, "REQUEST_TAKEOVER")


def test_c_hold_respects_authority():
    assert resolve_bc_action(AuthorityLevel.A1, "HOLD") == "HOLD"
    assert resolve_bc_action(AuthorityLevel.A2, "HOLD") == "HOLD"
    assert resolve_bc_action(AuthorityLevel.A3, "HOLD") == "HOLD"
    assert resolve_bc_action(AuthorityLevel.A4, "HOLD") == "FALLBACK"
    assert resolve_bc_action(AuthorityLevel.A5, "HOLD") == "FALLBACK"


def test_no_instinct_respects_authority():
    assert resolve_bc_action(AuthorityLevel.A1, "NONE") == "EXECUTE"
    assert resolve_bc_action(AuthorityLevel.A2, "NONE") == "EXECUTE"
    assert resolve_bc_action(AuthorityLevel.A3, "NONE") == "EXECUTE"
    assert resolve_bc_action(AuthorityLevel.A4, "NONE") == "FALLBACK"
    assert resolve_bc_action(AuthorityLevel.A5, "NONE") == "FALLBACK"

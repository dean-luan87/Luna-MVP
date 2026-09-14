import pytest

from luna_badge_v1_2.governance.output_controller.ability_matrix import AuthorityLevel
from luna_badge_v1_2.governance.output_controller.bc_c_coordinator import (
    BCAction,
    decide_bc_c_cooperation,
)


def test_stop_is_absolute():
    coop = decide_bc_c_cooperation(authority=AuthorityLevel.A1, c_decision={"decision": "STOP"})
    assert coop.bc_action == BCAction.FORCE_STOP
    assert coop.allow_execute_b is False
    assert coop.allow_output is False
    assert coop.can_recover is False


@pytest.mark.parametrize("auth", [AuthorityLevel.A1, AuthorityLevel.A2, AuthorityLevel.A3])
def test_hold_blocks_b_execution(auth):
    coop = decide_bc_c_cooperation(authority=auth, c_decision={"decision": "HOLD"})
    assert coop.bc_action == BCAction.HOLD
    assert coop.allow_execute_b is False
    assert coop.allow_output is False
    assert coop.can_recover is True


@pytest.mark.parametrize("auth", [AuthorityLevel.A4, AuthorityLevel.A5])
def test_hold_fallback_on_a4_a5(auth):
    coop = decide_bc_c_cooperation(authority=auth, c_decision={"decision": "HOLD"})
    assert coop.bc_action == BCAction.FALLBACK
    assert coop.allow_execute_b is False
    assert coop.allow_output is False
    assert coop.can_recover is False


@pytest.mark.parametrize("auth", [AuthorityLevel.A1, AuthorityLevel.A2, AuthorityLevel.A3])
def test_none_executes_on_a1_a3(auth):
    coop = decide_bc_c_cooperation(authority=auth, c_decision=None)
    assert coop.bc_action == BCAction.EXECUTE
    assert coop.allow_execute_b is True
    assert coop.allow_output is True
    assert coop.can_recover is True


@pytest.mark.parametrize("auth", [AuthorityLevel.A4, AuthorityLevel.A5])
def test_none_fallback_on_a4_a5(auth):
    coop = decide_bc_c_cooperation(authority=auth, c_decision=None)
    assert coop.bc_action == BCAction.FALLBACK
    assert coop.allow_execute_b is False
    assert coop.allow_output is False
    assert coop.can_recover is False

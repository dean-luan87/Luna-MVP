# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Non-Effect Wiring v0

Covers:
- Scenario A: all upstream ready + skeleton/stub identities conservative => wired_ready, side_effects_released=false
- Scenario B: missing activation dry-run ready => wired_not_ready
- Scenario C: stub identity scope mismatch => wired_blocked
- relevant-only: no core inputs => not applicable
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_v0 import (  # noqa: E402
        get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity,
    )
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_v0 import (  # noqa: E402
        get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity,
    )
    from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0,
    )

    adm_ok = {"admission_status": "first_live_minimal_real_effect_admitted"}
    lgate_ok = {"launch_admission_status": "first_live_minimal_real_effect_launch_admitted"}
    pc_ok = {"pre_commit_status": "first_live_minimal_real_effect_pre_commit_ready"}
    cg_ok = {"commit_admission_status": "first_live_minimal_real_effect_commit_admitted"}
    cdr_ok = {"commit_dry_run_status": "first_live_minimal_real_effect_commit_ready"}
    ag_ok = {"activation_admission_status": "first_live_minimal_real_effect_activation_admitted"}
    adr_ok = {"activation_dry_run_status": "first_live_minimal_real_effect_activation_ready"}
    xs = {"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}
    rs = {"release_control_result_scope": "navigation_governance_action_release_control_result_v0"}

    sk_ok = get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity()
    stub_ok = get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity()

    # A: all prerequisites ok => wired_ready
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=adm_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=lgate_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0=pc_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0=cg_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0=cdr_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0=ag_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0=adr_ok,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0=sk_ok,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0=stub_ok,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        side_effects_released=False,
    )
    assert applicable is True
    assert isinstance(payload, dict)
    assert payload.get("wiring_status") == "first_live_minimal_real_effect_live_wired_ready"
    assert payload.get("side_effects_released") is False

    # B: activation dry-run not ready => not_ready
    applicable2, payload2 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=adm_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=lgate_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0=pc_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0=cg_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0=cdr_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0=ag_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0={
            "activation_dry_run_status": "first_live_minimal_real_effect_activation_not_ready"
        },
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0=sk_ok,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0=stub_ok,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        side_effects_released=False,
    )
    assert applicable2 is True
    assert isinstance(payload2, dict)
    assert payload2.get("wiring_status") == "first_live_minimal_real_effect_live_wired_not_ready"

    # C: stub identity scope mismatch => blocked
    bad_stub = dict(stub_ok)
    bad_stub["release_control_first_live_guarded_minimal_real_effect_live_implementation_stub_scope"] = "WRONG_SCOPE"
    applicable3, payload3 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=adm_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=lgate_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0=pc_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0=cg_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0=cdr_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0=ag_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0=adr_ok,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0=sk_ok,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0=bad_stub,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        side_effects_released=False,
    )
    assert applicable3 is True
    assert isinstance(payload3, dict)
    assert payload3.get("wiring_status") == "first_live_minimal_real_effect_live_wired_blocked"
    assert payload3.get("side_effects_released") is False

    # relevant-only: no core inputs => not applicable
    applicable4, payload4 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0=None,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0=None,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0=None,
        navigation_governance_action_release_control_execution_state_v0=None,
        navigation_governance_action_release_control_result_v0=None,
        side_effects_released=None,
    )
    assert applicable4 is False
    assert payload4 is None

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


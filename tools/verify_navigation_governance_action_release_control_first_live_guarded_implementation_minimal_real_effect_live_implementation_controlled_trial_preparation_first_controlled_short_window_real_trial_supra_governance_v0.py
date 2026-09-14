"""
Phase-Next-180 verifier

Verifies the Phase-Next-180 supra-governance runtime v0 obeys Phase-Next-179 constitution:
- Non-default explicit entry.
- Requires legal meta-governance completion + closed-safe + default path disabled.
- Only allowlisted governance outcomes.
- Forbidden probes/outcomes blocked.
- Governance never opens any side-effect window and never enables next runtime now.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_supra_governance_v0 import (  # noqa: E501
    SupraGovernanceInputV0,
    run_supra_governance_v0,
)


def _base_bundle() -> Dict[str, Any]:
    # A "clean, legal, closed-safe" meta-governance bundle baseline.
    return {
        "governance_completed": True,
        "governance_legality_seen": True,
        "closed_safe_state_preserved": True,
        "evidence_complete": True,
        "audit_trace_intact": True,
        "meta_governance_go_no_go_pack_v0": "go",
        "boundary_violation_seen": False,
        "structural_risk_seen": False,
        "widening_needed": False,
        "forbidden_signals": [],
    }


def _run(bundle: Dict[str, Any], *, explicit: bool = True, default_path_enabled: bool = False) -> Dict[str, Any]:
    inp = SupraGovernanceInputV0(
        meta_governance_bundle=bundle,
        explicit_supra_governance_entry_intent_v0=explicit,
        default_path_enabled=default_path_enabled,
    )
    return run_supra_governance_v0(inp)


def _assert_common_invariants(out: Dict[str, Any]) -> None:
    required = [
        "explicit_supra_governance_entry_seen",
        "meta_governance_completed_seen",
        "meta_governance_legality_seen",
        "closed_safe_state_seen",
        "evidence_complete_seen",
        "boundary_violation_seen",
        "allowed_supra_governance_outcome_selected",
        "forbidden_supra_governance_outcome_blocked",
        "human_confirmation_required",
        "requires_new_governance_definition",
        "allows_next_runtime_now",
        "closed_safe_state_preserved",
        "illegal_state_detected",
        "governance_completed",
        "keeps_system_closed",
    ]
    for k in required:
        assert k in out, f"missing field: {k}"

    assert out["keeps_system_closed"] is True
    assert out["allows_next_runtime_now"] is False
    assert out["closed_safe_state_preserved"] is True


def test_A_no_legal_meta_completion() -> None:
    b = dict(_base_bundle())
    b["governance_completed"] = False
    out = _run(b)
    _assert_common_invariants(out)
    assert out["illegal_state_detected"] is True
    assert out["allowed_supra_governance_outcome_selected"] == "remain_closed_safe"


def test_B_closed_safe_not_preserved() -> None:
    b = dict(_base_bundle())
    b["closed_safe_state_preserved"] = False
    out = _run(b)
    _assert_common_invariants(out)
    assert out["illegal_state_detected"] is True
    assert out["allowed_supra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_C_evidence_incomplete() -> None:
    b = dict(_base_bundle())
    b["evidence_complete"] = False
    out = _run(b)
    _assert_common_invariants(out)
    assert out["allowed_supra_governance_outcome_selected"] in {
        "require_new_evidence_before_any_further_governance",
        "remain_closed_safe",
    }


def test_D_clean_supra_case() -> None:
    out = _run(_base_bundle())
    _assert_common_invariants(out)
    assert out["illegal_state_detected"] is False
    assert out["allowed_supra_governance_outcome_selected"] == "allow_next_governance_preparation_under_same_guardrails"


def test_E_governance_boundary_violation_case() -> None:
    b = dict(_base_bundle())
    b["boundary_violation_seen"] = True
    out = _run(b)
    _assert_common_invariants(out)
    assert out["allowed_supra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_F_widening_needed_case() -> None:
    b = dict(_base_bundle())
    b["widening_needed"] = True
    out = _run(b)
    _assert_common_invariants(out)
    assert out["allowed_supra_governance_outcome_selected"] == "escalate_for_new_governance_definition"
    assert out["requires_new_governance_definition"] is True


def test_G_forbidden_reopen_probe() -> None:
    b = dict(_base_bundle())
    b["forbidden_signals"] = ["implicit_reopen"]
    out = _run(b)
    _assert_common_invariants(out)
    assert out["forbidden_supra_governance_outcome_blocked"] is True
    assert out["allowed_supra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_H_forbidden_retry_runtime_probe() -> None:
    b = dict(_base_bundle())
    b["forbidden_signals"] = ["implicit_retry_runtime"]
    out = _run(b)
    _assert_common_invariants(out)
    assert out["forbidden_supra_governance_outcome_blocked"] is True
    assert out["allowed_supra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_I_forbidden_widen_probe() -> None:
    b = dict(_base_bundle())
    b["forbidden_signals"] = ["implicit_widening"]
    out = _run(b)
    _assert_common_invariants(out)
    assert out["forbidden_supra_governance_outcome_blocked"] is True
    assert out["allowed_supra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_J_forbidden_long_running_probe() -> None:
    b = dict(_base_bundle())
    b["forbidden_signals"] = ["implicit_long_running_enablement"]
    out = _run(b)
    _assert_common_invariants(out)
    assert out["forbidden_supra_governance_outcome_blocked"] is True
    assert out["allowed_supra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_K_default_path_probe() -> None:
    out = _run(_base_bundle(), explicit=False)
    _assert_common_invariants(out)
    assert out["illegal_state_detected"] is True
    assert out["allowed_supra_governance_outcome_selected"] == "remain_closed_safe"

    out2 = _run(_base_bundle(), explicit=True, default_path_enabled=True)
    _assert_common_invariants(out2)
    assert out2["illegal_state_detected"] is True
    assert out2["allowed_supra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_L_require_new_evidence_case() -> None:
    b = dict(_base_bundle())
    b["audit_trace_intact"] = False
    out = _run(b)
    _assert_common_invariants(out)
    assert out["allowed_supra_governance_outcome_selected"] == "require_new_evidence_before_any_further_governance"


def test_M_structural_block_case() -> None:
    b = dict(_base_bundle())
    b["structural_risk_seen"] = True
    out = _run(b)
    _assert_common_invariants(out)
    assert out["allowed_supra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def main() -> None:
    tests = [
        test_A_no_legal_meta_completion,
        test_B_closed_safe_not_preserved,
        test_C_evidence_incomplete,
        test_D_clean_supra_case,
        test_E_governance_boundary_violation_case,
        test_F_widening_needed_case,
        test_G_forbidden_reopen_probe,
        test_H_forbidden_retry_runtime_probe,
        test_I_forbidden_widen_probe,
        test_J_forbidden_long_running_probe,
        test_K_default_path_probe,
        test_L_require_new_evidence_case,
        test_M_structural_block_case,
    ]
    for t in tests:
        t()
    print("OK: Phase-Next-180 supra-governance verifier v0")


if __name__ == "__main__":
    main()


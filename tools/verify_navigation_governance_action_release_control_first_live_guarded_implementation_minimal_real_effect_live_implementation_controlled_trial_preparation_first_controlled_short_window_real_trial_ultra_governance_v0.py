"""
Phase-Next-184 verifier

Validates that Ultra-Governance Runtime v0 obeys Phase-Next-183 constitution.

This tool is intentionally lightweight and self-contained (pytest-like).
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_ultra_governance_v0 import (  # noqa: E501
    UltraGovernanceInputV0,
    run_ultra_governance_v0,
)


def _base_bundle() -> Dict[str, Any]:
    return {
        "governance_completed": True,
        "governance_legality_seen": True,
        "closed_safe_state_preserved": True,
        "evidence_complete": True,
        "audit_trace_intact": True,
        # Optional pack prerequisite (182) if present; keep permissive default.
        "supra_governance_go_no_go_pack_v0": "go",
        "boundary_violation_seen": False,
        "structural_risk_seen": False,
        "widening_needed": False,
        "forbidden_signals": [],
    }


def _run(bundle: Dict[str, Any], *, explicit: bool = True, default_path_enabled: bool = False) -> Dict[str, Any]:
    inp = UltraGovernanceInputV0(
        supra_governance_bundle=bundle,
        explicit_ultra_governance_entry_intent_v0=explicit,
        default_path_enabled=default_path_enabled,
    )
    return run_ultra_governance_v0(inp)


def _assert_common_invariants(out: Dict[str, Any]) -> None:
    # Required invariants: always closed-safe and never allow next runtime.
    assert out["keeps_system_closed"] is True
    assert out["allows_next_runtime_now"] is False
    assert out["closed_safe_state_preserved"] is True
    # Allowed outcome must be in allowlist (Phase-Next-183).
    assert out["allowed_ultra_governance_outcome_selected"] in {
        "remain_closed_safe",
        "require_new_evidence_before_any_further_governance",
        "escalate_for_new_governance_definition",
        "allow_next_governance_preparation_under_same_guardrails",
        "block_further_real_action_until_manual_override",
    }


def test_A_no_legal_supra_completion() -> None:
    b = dict(_base_bundle())
    b["governance_completed"] = False
    out = _run(b)
    _assert_common_invariants(out)
    assert out["illegal_state_detected"] is True
    assert out["allowed_ultra_governance_outcome_selected"] == "remain_closed_safe"


def test_B_closed_safe_not_preserved() -> None:
    b = dict(_base_bundle())
    b["closed_safe_state_preserved"] = False
    out = _run(b)
    _assert_common_invariants(out)
    assert out["illegal_state_detected"] is True
    assert out["allowed_ultra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_C_evidence_incomplete() -> None:
    b = dict(_base_bundle())
    b["evidence_complete"] = False
    out = _run(b)
    _assert_common_invariants(out)
    assert out["allowed_ultra_governance_outcome_selected"] == "require_new_evidence_before_any_further_governance"


def test_D_clean_ultra_case() -> None:
    out = _run(_base_bundle())
    _assert_common_invariants(out)
    assert out["illegal_state_detected"] is False
    assert out["allowed_ultra_governance_outcome_selected"] == "allow_next_governance_preparation_under_same_guardrails"


def test_E_governance_boundary_violation_case() -> None:
    b = dict(_base_bundle())
    b["boundary_violation_seen"] = True
    out = _run(b)
    _assert_common_invariants(out)
    assert out["allowed_ultra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_F_widening_needed_case() -> None:
    b = dict(_base_bundle())
    b["widening_needed"] = True
    out = _run(b)
    _assert_common_invariants(out)
    assert out["allowed_ultra_governance_outcome_selected"] == "escalate_for_new_governance_definition"


def test_G_forbidden_reopen_probe() -> None:
    b = dict(_base_bundle())
    b["forbidden_signals"] = ["implicit_reopen"]
    out = _run(b)
    _assert_common_invariants(out)
    assert out["forbidden_ultra_governance_outcome_blocked"] is True
    assert out["illegal_state_detected"] is True
    assert out["allowed_ultra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_H_forbidden_retry_runtime_probe() -> None:
    b = dict(_base_bundle())
    b["forbidden_signals"] = ["implicit_retry_runtime"]
    out = _run(b)
    _assert_common_invariants(out)
    assert out["forbidden_ultra_governance_outcome_blocked"] is True
    assert out["illegal_state_detected"] is True
    assert out["allowed_ultra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_I_forbidden_widen_probe() -> None:
    b = dict(_base_bundle())
    b["forbidden_signals"] = ["implicit_widening"]
    out = _run(b)
    _assert_common_invariants(out)
    assert out["forbidden_ultra_governance_outcome_blocked"] is True
    assert out["illegal_state_detected"] is True
    assert out["allowed_ultra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_J_forbidden_long_running_probe() -> None:
    b = dict(_base_bundle())
    b["forbidden_signals"] = ["implicit_long_running_enablement"]
    out = _run(b)
    _assert_common_invariants(out)
    assert out["forbidden_ultra_governance_outcome_blocked"] is True
    assert out["illegal_state_detected"] is True
    assert out["allowed_ultra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_K_default_path_probe_not_explicit_entry() -> None:
    out = _run(_base_bundle(), explicit=False)
    _assert_common_invariants(out)
    assert out["explicit_ultra_governance_entry_seen"] is False
    assert out["illegal_state_detected"] is True
    assert out["allowed_ultra_governance_outcome_selected"] == "remain_closed_safe"


def test_K_default_path_probe_default_path_enabled() -> None:
    out = _run(_base_bundle(), explicit=True, default_path_enabled=True)
    _assert_common_invariants(out)
    assert out["illegal_state_detected"] is True
    assert out["allowed_ultra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def test_L_require_new_evidence_case() -> None:
    b = dict(_base_bundle())
    b["audit_trace_intact"] = False
    out = _run(b)
    _assert_common_invariants(out)
    assert out["allowed_ultra_governance_outcome_selected"] == "require_new_evidence_before_any_further_governance"


def test_M_structural_block_case() -> None:
    b = dict(_base_bundle())
    b["structural_risk_seen"] = True
    out = _run(b)
    _assert_common_invariants(out)
    assert out["allowed_ultra_governance_outcome_selected"] == "block_further_real_action_until_manual_override"


def main() -> None:
    tests = [
        test_A_no_legal_supra_completion,
        test_B_closed_safe_not_preserved,
        test_C_evidence_incomplete,
        test_D_clean_ultra_case,
        test_E_governance_boundary_violation_case,
        test_F_widening_needed_case,
        test_G_forbidden_reopen_probe,
        test_H_forbidden_retry_runtime_probe,
        test_I_forbidden_widen_probe,
        test_J_forbidden_long_running_probe,
        test_K_default_path_probe_not_explicit_entry,
        test_K_default_path_probe_default_path_enabled,
        test_L_require_new_evidence_case,
        test_M_structural_block_case,
    ]
    for t in tests:
        t()
    print("OK: Phase-Next-184 ultra-governance verifier v0")


if __name__ == "__main__":
    main()


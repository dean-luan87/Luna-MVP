"""
Phase-Next-173 (short filename due to macOS filename length limits)

Functional equivalent of the requested long-name tool:
tools/validate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_higher_order_governance_shadowed_validation_evaluation_v0.py

Purpose:
- Shadowed / guarded / evaluation-first validation of Phase-Next-172 higher-order governance runtime
  against Phase-Next-171 constitution boundaries:
  entry / lower-order legality prerequisite / closed-safe prerequisite / allowed outcomes /
  forbidden blocking / no-next-runtime-now.

Non-goals:
- No new runtime capability, no default path enablement, no real side effects, no widening.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_higher_order_governance_v0 import (  # noqa: E501
    HigherOrderGovernanceInputV0,
    run_higher_order_governance_v0,
)


ALLOWED_OUTCOMES = {
    "remain_closed_safe",
    "require_new_evidence_before_any_further_governance",
    "escalate_for_new_governance_definition",
    "allow_next_governance_preparation_under_same_guardrails",
    "block_further_real_action_until_manual_override",
}


def _base_bundle() -> Dict[str, Any]:
    return {
        "governance_completed": True,
        "governance_legality_seen": True,
        "closed_safe_state_preserved": True,
        "evidence_complete": True,
        "audit_trace_intact": True,
        "post_decision_governance_go_no_go_pack_v0": "go",
        "boundary_violation_seen": False,
        "structural_risk_seen": False,
        "widening_needed": False,
        "forbidden_signals": [],
    }


def _run(bundle: Dict[str, Any], *, explicit: bool = True, default_path_enabled: bool = False) -> Dict[str, Any]:
    inp = HigherOrderGovernanceInputV0(
        lower_order_governance_bundle=bundle,
        explicit_higher_order_governance_entry_intent_v0=explicit,
        default_path_enabled=default_path_enabled,
    )
    return run_higher_order_governance_v0(inp)


@dataclass(frozen=True)
class Scenario:
    name: str
    expected_outcome: str
    bundle: Dict[str, Any]
    explicit: bool = True
    default_path_enabled: bool = False
    expected_forbidden_blocked: Optional[bool] = None
    require_illegal_state: Optional[bool] = None


def _reason_codes_for(out: Dict[str, Any]) -> List[str]:
    codes: List[str] = []
    if not out.get("explicit_higher_order_governance_entry_seen", False):
        codes.append("ENTRY_NOT_EXPLICIT")
    if not out.get("lower_order_governance_completed_seen", False):
        codes.append("LOWER_ORDER_NOT_COMPLETED")
    if not out.get("lower_order_governance_legality_seen", False):
        codes.append("LOWER_ORDER_NOT_LEGAL")
    if not out.get("closed_safe_state_seen", False):
        codes.append("CLOSED_SAFE_NOT_SEEN")
    if not out.get("audit_trace_intact_seen", True):
        codes.append("AUDIT_TRACE_NOT_INTACT")
    if not out.get("evidence_complete_seen", True):
        codes.append("EVIDENCE_INCOMPLETE")
    if out.get("boundary_violation_seen", False):
        codes.append("BOUNDARY_VIOLATION_OR_RISK")
    if out.get("forbidden_higher_order_governance_outcome_blocked", False):
        codes.append("FORBIDDEN_BLOCKED")
    if out.get("allows_next_runtime_now", False):
        codes.append("NEXT_RUNTIME_ALLOWED_VIOLATION")
    if not out.get("keeps_system_closed", True):
        codes.append("CLOSED_SAFE_BROKEN_VIOLATION")
    if out.get("allowed_higher_order_governance_outcome_selected") not in ALLOWED_OUTCOMES:
        codes.append("OUTCOME_NOT_IN_ALLOWLIST")
    return codes


def _scenario_set() -> List[Scenario]:
    scenarios: List[Scenario] = []

    # A. no_legal_lower_order_completion
    bA = dict(_base_bundle())
    bA["governance_completed"] = False
    scenarios.append(
        Scenario(
            name="A.no_legal_lower_order_completion",
            expected_outcome="remain_closed_safe",
            bundle=bA,
            require_illegal_state=True,
        )
    )

    # B. closed_safe_not_preserved
    bB = dict(_base_bundle())
    bB["closed_safe_state_preserved"] = False
    scenarios.append(
        Scenario(
            name="B.closed_safe_not_preserved",
            expected_outcome="block_further_real_action_until_manual_override",
            bundle=bB,
            require_illegal_state=True,
        )
    )

    # C. evidence_incomplete
    bC = dict(_base_bundle())
    bC["evidence_complete"] = False
    scenarios.append(
        Scenario(
            name="C.evidence_incomplete",
            expected_outcome="require_new_evidence_before_any_further_governance",
            bundle=bC,
        )
    )

    # D. clean_higher_order_case
    scenarios.append(
        Scenario(
            name="D.clean_higher_order_case",
            expected_outcome="allow_next_governance_preparation_under_same_guardrails",
            bundle=_base_bundle(),
            require_illegal_state=False,
        )
    )

    # E. governance_boundary_violation_case
    bE = dict(_base_bundle())
    bE["boundary_violation_seen"] = True
    scenarios.append(
        Scenario(
            name="E.governance_boundary_violation_case",
            expected_outcome="block_further_real_action_until_manual_override",
            bundle=bE,
        )
    )

    # F. widening_needed_case
    bF = dict(_base_bundle())
    bF["widening_needed"] = True
    scenarios.append(
        Scenario(
            name="F.widening_needed_case",
            expected_outcome="escalate_for_new_governance_definition",
            bundle=bF,
        )
    )

    # G. forbidden_reopen_probe
    bG = dict(_base_bundle())
    bG["forbidden_signals"] = ["implicit_reopen"]
    scenarios.append(
        Scenario(
            name="G.forbidden_reopen_probe",
            expected_outcome="block_further_real_action_until_manual_override",
            bundle=bG,
            expected_forbidden_blocked=True,
            require_illegal_state=True,
        )
    )

    # H. forbidden_retry_runtime_probe
    bH = dict(_base_bundle())
    bH["forbidden_signals"] = ["implicit_retry_runtime"]
    scenarios.append(
        Scenario(
            name="H.forbidden_retry_runtime_probe",
            expected_outcome="block_further_real_action_until_manual_override",
            bundle=bH,
            expected_forbidden_blocked=True,
            require_illegal_state=True,
        )
    )

    # I. forbidden_widen_probe
    bI = dict(_base_bundle())
    bI["forbidden_signals"] = ["implicit_widening"]
    scenarios.append(
        Scenario(
            name="I.forbidden_widen_probe",
            expected_outcome="block_further_real_action_until_manual_override",
            bundle=bI,
            expected_forbidden_blocked=True,
            require_illegal_state=True,
        )
    )

    # J. forbidden_long_running_probe
    bJ = dict(_base_bundle())
    bJ["forbidden_signals"] = ["implicit_long_running_enablement"]
    scenarios.append(
        Scenario(
            name="J.forbidden_long_running_probe",
            expected_outcome="block_further_real_action_until_manual_override",
            bundle=bJ,
            expected_forbidden_blocked=True,
            require_illegal_state=True,
        )
    )

    # K. default_path_probe (1) not explicit entry
    scenarios.append(
        Scenario(
            name="K.default_path_probe.not_explicit_entry",
            expected_outcome="remain_closed_safe",
            bundle=_base_bundle(),
            explicit=False,
            require_illegal_state=True,
        )
    )
    # K. default_path_probe (2) default path enabled
    scenarios.append(
        Scenario(
            name="K.default_path_probe.default_path_enabled",
            expected_outcome="block_further_real_action_until_manual_override",
            bundle=_base_bundle(),
            explicit=True,
            default_path_enabled=True,
            require_illegal_state=True,
        )
    )

    # L. require_new_evidence_case (audit trace not intact)
    bL = dict(_base_bundle())
    bL["audit_trace_intact"] = False
    scenarios.append(
        Scenario(
            name="L.require_new_evidence_case",
            expected_outcome="require_new_evidence_before_any_further_governance",
            bundle=bL,
        )
    )

    # M. structural_block_case
    bM = dict(_base_bundle())
    bM["structural_risk_seen"] = True
    scenarios.append(
        Scenario(
            name="M.structural_block_case",
            expected_outcome="block_further_real_action_until_manual_override",
            bundle=bM,
        )
    )

    return scenarios


def _evaluate_scenario(s: Scenario) -> Dict[str, Any]:
    out = _run(s.bundle, explicit=s.explicit, default_path_enabled=s.default_path_enabled)

    actual_outcome = out.get("allowed_higher_order_governance_outcome_selected")
    pass_fail = True
    reasons: List[str] = []

    # Required invariants (171/172).
    if out.get("keeps_system_closed") is not True:
        pass_fail = False
        reasons.append("VIOLATION_KEEPS_SYSTEM_CLOSED")
    if out.get("allows_next_runtime_now") is not False:
        pass_fail = False
        reasons.append("VIOLATION_ALLOWS_NEXT_RUNTIME_NOW")
    if out.get("closed_safe_state_preserved") is not True:
        pass_fail = False
        reasons.append("VIOLATION_CLOSED_SAFE_PRESERVED")
    if actual_outcome not in ALLOWED_OUTCOMES:
        pass_fail = False
        reasons.append("VIOLATION_OUTCOME_NOT_IN_ALLOWLIST")

    # Expected outcome.
    if actual_outcome != s.expected_outcome:
        pass_fail = False
        reasons.append("MISMATCH_EXPECTED_OUTCOME")

    # Forbidden blocking expectation (when specified).
    if s.expected_forbidden_blocked is not None and out.get("forbidden_higher_order_governance_outcome_blocked") != s.expected_forbidden_blocked:
        pass_fail = False
        reasons.append("MISMATCH_FORBIDDEN_BLOCKED_EXPECTATION")

    # Illegal state expectation (when specified).
    if s.require_illegal_state is not None and out.get("illegal_state_detected") != s.require_illegal_state:
        pass_fail = False
        reasons.append("MISMATCH_ILLEGAL_STATE_EXPECTATION")

    # Entry gating integrity check: if not explicit, must be illegal and remain_closed_safe.
    if not s.explicit:
        if out.get("illegal_state_detected") is not True or actual_outcome != "remain_closed_safe":
            pass_fail = False
            reasons.append("VIOLATION_NON_DEFAULT_ENTRY_GATE")

    return {
        "scenario_name": s.name,
        "expected_outcome": s.expected_outcome,
        "actual_outcome": actual_outcome,
        "explicit_higher_order_governance_entry_seen": out.get("explicit_higher_order_governance_entry_seen"),
        "lower_order_governance_completed_seen": out.get("lower_order_governance_completed_seen"),
        "lower_order_governance_legality_seen": out.get("lower_order_governance_legality_seen"),
        "closed_safe_state_seen": out.get("closed_safe_state_seen"),
        "evidence_complete_seen": out.get("evidence_complete_seen"),
        "boundary_violation_seen": out.get("boundary_violation_seen"),
        "allowed_higher_order_governance_outcome_selected": actual_outcome,
        "forbidden_higher_order_governance_outcome_blocked": out.get("forbidden_higher_order_governance_outcome_blocked"),
        "requires_new_governance_definition": out.get("requires_new_governance_definition"),
        "human_confirmation_required": out.get("human_confirmation_required"),
        "allows_next_runtime_now": out.get("allows_next_runtime_now"),
        "closed_safe_state_preserved": out.get("closed_safe_state_preserved"),
        "illegal_state_detected": out.get("illegal_state_detected"),
        "pass_or_fail": "pass" if pass_fail else "fail",
        "evaluation_reason_codes": sorted(set(reasons + _reason_codes_for(out))),
    }


def _integrity_flags(results: List[Dict[str, Any]]) -> Dict[str, str]:
    def ok(pred) -> bool:
        return all(pred(r) for r in results)

    return {
        "entry_gate_integrity": "pass"
        if ok(lambda r: not (r["scenario_name"].startswith("K.default_path_probe.not_explicit_entry") and r["pass_or_fail"] != "pass"))
        else "fail",
        "lower_order_prerequisite_integrity": "pass"
        if ok(lambda r: not (r["scenario_name"].startswith("A.") and r["actual_outcome"] != "remain_closed_safe"))
        else "fail",
        "allowed_higher_order_governance_outcome_integrity": "pass"
        if ok(lambda r: r["allowed_higher_order_governance_outcome_selected"] in ALLOWED_OUTCOMES)
        else "fail",
        "forbidden_higher_order_governance_block_integrity": "pass"
        if ok(lambda r: not (r["scenario_name"].startswith(("G.", "H.", "I.", "J.")) and r["forbidden_higher_order_governance_outcome_blocked"] is not True))
        else "fail",
        "closed_safe_state_integrity": "pass"
        if ok(lambda r: r["closed_safe_state_preserved"] is True)
        else "fail",
        "no_next_runtime_integrity": "pass"
        if ok(lambda r: r["allows_next_runtime_now"] is False)
        else "fail",
    }


def _overall_evaluation(passed: int, failed: int, integrities: Dict[str, str]) -> Tuple[str, str]:
    if failed == 0 and all(v == "pass" for v in integrities.values()):
        return "go", "Phase-Next-174：Higher-Order Governance Go/No-Go Pack v0"
    if failed == 0:
        return "conditional_go", "补强 trace/telemetry/readability 后进入 Phase-Next-174"
    return "no_go", "x Fix Sprint（修复边界违规后再跑 173）"


def main() -> None:
    scenarios = _scenario_set()
    results = [_evaluate_scenario(s) for s in scenarios]

    total = len(results)
    passed = sum(1 for r in results if r["pass_or_fail"] == "pass")
    failed = total - passed
    integrities = _integrity_flags(results)
    overall, next_step = _overall_evaluation(passed, failed, integrities)

    report = {
        "summary": {
            "total_scenarios": total,
            "passed_scenarios": passed,
            "failed_scenarios": failed,
            **integrities,
            "overall_evaluation": overall,
            "recommended_next_step": next_step,
            "notes": [
                "default_path_still_disabled=true (by contract; tool does not enable default path)",
                "no_full_controlled_trial=true (evaluation only)",
                "no_real_side_effects=true (runtime is read-only governance output)",
            ],
        },
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False))


if __name__ == "__main__":
    main()


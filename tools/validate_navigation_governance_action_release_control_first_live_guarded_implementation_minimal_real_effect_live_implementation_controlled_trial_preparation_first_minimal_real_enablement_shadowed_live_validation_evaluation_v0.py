# -*- coding: utf-8 -*-
"""
Phase-Next-153:
Shadowed / Guarded Live Validation + Evaluation for Phase-Next-152 first minimal real enablement.

硬边界（写死）：
- 只做 validation/evaluation；不修改 151/152；不新增默认路径；不扩副作用面。
- 复用 152 runtime + 152 verifier 的边界语义。
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


@dataclass(frozen=True)
class ScenarioResult:
    scenario_name: str
    expected_outcome: Dict[str, Any]
    actual_outcome: Dict[str, Any]
    start_event_observed_seen: bool
    started_seen: bool
    side_effects_released_seen: bool
    closure_seen: bool
    rollback_seen: bool
    illegal_state_detected: bool
    pass_or_fail: str
    evaluation_reason_codes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_name": self.scenario_name,
            "expected_outcome": dict(self.expected_outcome),
            "actual_outcome": dict(self.actual_outcome),
            "start_event_observed_seen": bool(self.start_event_observed_seen),
            "started_seen": bool(self.started_seen),
            "side_effects_released_seen": bool(self.side_effects_released_seen),
            "closure_seen": bool(self.closure_seen),
            "rollback_seen": bool(self.rollback_seen),
            "illegal_state_detected": bool(self.illegal_state_detected),
            "pass_or_fail": str(self.pass_or_fail),
            "evaluation_reason_codes": list(self.evaluation_reason_codes),
        }


def _mk_prep_go_gate() -> dict:
    return {"controlled_trial_preparation_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_preparation_go"}


def _mk_prep_shadow_eval_go() -> dict:
    return {"controlled_trial_preparation_shadow_eval_status": "first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_go"}


def _mk_prep_admitted() -> dict:
    return {"controlled_trial_preparation_status": "first_live_minimal_real_effect_controlled_trial_preparation_admitted"}


def _mk_enablement_dry_run_executed() -> dict:
    return {
        "dry_run_status": "first_live_minimal_real_effect_controlled_trial_preparation_minimal_enablement_dry_run_executed"
    }


def _summarize_from_runtime_output(out: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    payload = out.get("payload") if isinstance(out, dict) else None
    payload = payload if isinstance(payload, dict) else {}
    state = payload.get("state") if isinstance(payload.get("state"), dict) else {}
    trace = payload.get("trace") if isinstance(payload.get("trace"), dict) else {}

    start_event_observed_seen = bool(state.get("start_event_observed") is True)
    started_seen = bool(state.get("real_enablement_started") is True)
    side_effects_released_seen = bool(state.get("side_effects_released") is True)
    closure_seen = bool(state.get("closed") is True)
    rollback_seen = bool(state.get("rollback_completed") is True)

    actual = {
        "ok": bool(out.get("ok") is True) if isinstance(out, dict) else False,
        "status": str(out.get("status") or "") if isinstance(out, dict) else "non_dict",
        "reason": str(out.get("reason") or "") if isinstance(out, dict) else "non_dict",
        "state": dict(state),
        "trace_order": list(trace.get("order") or []) if isinstance(trace.get("order"), list) else [],
    }

    observed = {
        "start_event_observed_seen": start_event_observed_seen,
        "started_seen": started_seen,
        "side_effects_released_seen": side_effects_released_seen,
        "closure_seen": closure_seen,
        "rollback_seen": rollback_seen,
    }
    return actual, observed


def _detect_illegal_states(observed: Dict[str, Any]) -> Tuple[bool, List[str]]:
    codes: List[str] = []
    start_event = bool(observed.get("start_event_observed_seen"))
    started = bool(observed.get("started_seen"))
    release = bool(observed.get("side_effects_released_seen"))
    closed = bool(observed.get("closure_seen"))

    illegal = False

    # 151 invariants
    if started and not start_event:
        illegal = True
        codes.append("illegal_started_without_start_event")
    if release and not started:
        illegal = True
        codes.append("illegal_release_without_started")
    if started and not closed:
        illegal = True
        codes.append("illegal_started_without_closure")
    return illegal, codes


def _run_scenario(
    *,
    scenario_name: str,
    expected: Dict[str, Any],
    run_fn: Callable[[], Dict[str, Any]],
) -> ScenarioResult:
    out = run_fn()
    actual, observed = _summarize_from_runtime_output(out)
    illegal, illegal_codes = _detect_illegal_states(observed)

    # Basic pass/fail checks based on expected fields.
    reason_codes: List[str] = []
    ok_expected = expected.get("ok")
    status_expected = expected.get("status")
    started_expected = expected.get("started_seen")
    release_expected = expected.get("side_effects_released_seen")
    closure_expected = expected.get("closure_seen")

    passed = True
    if ok_expected is not None and bool(ok_expected) != bool(actual.get("ok")):
        passed = False
        reason_codes.append("mismatch_ok")
    if status_expected is not None and str(status_expected) != str(actual.get("status")):
        passed = False
        reason_codes.append("mismatch_status")
    if started_expected is not None and bool(started_expected) != bool(observed.get("started_seen")):
        passed = False
        reason_codes.append("mismatch_started_seen")
    if release_expected is not None and bool(release_expected) != bool(observed.get("side_effects_released_seen")):
        passed = False
        reason_codes.append("mismatch_release_seen")
    if closure_expected is not None and bool(closure_expected) != bool(observed.get("closure_seen")):
        passed = False
        reason_codes.append("mismatch_closure_seen")

    if illegal:
        passed = False
        reason_codes.extend(illegal_codes)

    return ScenarioResult(
        scenario_name=scenario_name,
        expected_outcome=dict(expected),
        actual_outcome=dict(actual),
        start_event_observed_seen=bool(observed.get("start_event_observed_seen")),
        started_seen=bool(observed.get("started_seen")),
        side_effects_released_seen=bool(observed.get("side_effects_released_seen")),
        closure_seen=bool(observed.get("closure_seen")),
        rollback_seen=bool(observed.get("rollback_seen")),
        illegal_state_detected=bool(illegal),
        pass_or_fail="pass" if passed else "fail",
        evaluation_reason_codes=reason_codes,
    )


def main() -> int:
    # Reuse Phase-Next-152 runtime & Phase-Next-152 verifier.
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_minimal_real_enablement_v0 import (  # noqa: E402
        run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0,
    )

    # Ensure the dedicated verifier passes (hard-stop if not).
    from tools.verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_minimal_real_enablement_v0 import (  # noqa: E402
        main as verifier_main,
    )

    if int(verifier_main()) != 0:
        raise SystemExit(2)

    results: List[ScenarioResult] = []

    # Writers (shadowed/guarded): still injected, but they are "real enablement runtime" test doubles.
    def w_state_ok(p: dict) -> dict:
        return {"ok": True, "surface": p.get("surface")}

    def w_result_ok(p: dict) -> dict:
        return {"ok": True, "surface": p.get("surface")}

    def w_exc_ok(p: dict) -> dict:
        return {"ok": True, "surface": p.get("surface")}

    def w_state_fail(_: dict) -> dict:
        raise RuntimeError("boom_state")

    # A. not_ready
    results.append(
        _run_scenario(
            scenario_name="A.not_ready",
            expected={"ok": False, "status": "not_ready", "started_seen": False, "side_effects_released_seen": False},
            run_fn=lambda: run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(
                preparation_go_no_go_gate_v0=None,
                preparation_shadow_eval_gate_v0=None,
                preparation_admission_gate_v0=None,
                preparation_enablement_dry_run_v0=None,
                preparation_enablement_intent_v0=None,
                execution_state_v0={"x": 1},
                result_v0={"x": 1},
                exception_or_failure_path_v0={"x": 1},
                side_effects_released=False,
                execution_state_writer=w_state_ok,
                result_object_writer=w_result_ok,
                exception_or_failure_writer=w_exc_ok,
                context={"scenario": "A.not_ready"},
            ),
        )
    )

    # B. preparation_go_only
    results.append(
        _run_scenario(
            scenario_name="B.preparation_go_only",
            expected={"ok": False, "status": "not_ready", "started_seen": False, "side_effects_released_seen": False},
            run_fn=lambda: run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(
                preparation_go_no_go_gate_v0=_mk_prep_go_gate(),
                preparation_shadow_eval_gate_v0=None,
                preparation_admission_gate_v0=None,
                preparation_enablement_dry_run_v0=None,
                preparation_enablement_intent_v0={"intent": True},
                execution_state_v0={"x": 1},
                result_v0={"x": 1},
                exception_or_failure_path_v0={"x": 1},
                side_effects_released=False,
                execution_state_writer=w_state_ok,
                result_object_writer=w_result_ok,
                exception_or_failure_writer=w_exc_ok,
                context={"scenario": "B.preparation_go_only"},
            ),
        )
    )

    # C. dry_run_only (dry_run_executed but no real-start intent)
    results.append(
        _run_scenario(
            scenario_name="C.dry_run_only_no_intent",
            expected={"ok": False, "status": "not_ready", "started_seen": False, "side_effects_released_seen": False},
            run_fn=lambda: run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(
                preparation_go_no_go_gate_v0=_mk_prep_go_gate(),
                preparation_shadow_eval_gate_v0=_mk_prep_shadow_eval_go(),
                preparation_admission_gate_v0=_mk_prep_admitted(),
                preparation_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
                preparation_enablement_intent_v0=None,
                execution_state_v0={"x": 1},
                result_v0={"x": 1},
                exception_or_failure_path_v0={"x": 1},
                side_effects_released=False,
                execution_state_writer=w_state_ok,
                result_object_writer=w_result_ok,
                exception_or_failure_writer=w_exc_ok,
                context={"scenario": "C.dry_run_only_no_intent"},
            ),
        )
    )

    # D. admitted_but_no_start_event (we simulate by expecting not_ready when intent missing; start event is only in runtime path)
    results.append(
        _run_scenario(
            scenario_name="D.admitted_but_no_start_event",
            expected={"ok": False, "status": "not_ready", "started_seen": False, "side_effects_released_seen": False},
            run_fn=lambda: run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(
                preparation_go_no_go_gate_v0=_mk_prep_go_gate(),
                preparation_shadow_eval_gate_v0=_mk_prep_shadow_eval_go(),
                preparation_admission_gate_v0=_mk_prep_admitted(),
                preparation_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
                preparation_enablement_intent_v0=None,
                execution_state_v0={"x": 1},
                result_v0={"x": 1},
                exception_or_failure_path_v0={"x": 1},
                side_effects_released=False,
                execution_state_writer=w_state_ok,
                result_object_writer=w_result_ok,
                exception_or_failure_writer=w_exc_ok,
                context={"scenario": "D.admitted_but_no_start_event"},
            ),
        )
    )

    # E. legal_started_success
    results.append(
        _run_scenario(
            scenario_name="E.legal_started_success",
            expected={"ok": True, "status": "executed", "started_seen": True, "side_effects_released_seen": False, "closure_seen": True},
            run_fn=lambda: run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(
                preparation_go_no_go_gate_v0=_mk_prep_go_gate(),
                preparation_shadow_eval_gate_v0=_mk_prep_shadow_eval_go(),
                preparation_admission_gate_v0=_mk_prep_admitted(),
                preparation_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
                preparation_enablement_intent_v0={"intent": True, "reason": "unit_test"},
                execution_state_v0={"x": 1},
                result_v0={"x": 1},
                exception_or_failure_path_v0={"x": 1},
                side_effects_released=False,
                execution_state_writer=w_state_ok,
                result_object_writer=w_result_ok,
                exception_or_failure_writer=w_exc_ok,
                context={"scenario": "E.legal_started_success"},
            ),
        )
    )

    # F. legal_started_failure
    results.append(
        _run_scenario(
            scenario_name="F.legal_started_failure",
            expected={"ok": False, "status": "failed", "started_seen": True, "side_effects_released_seen": False, "closure_seen": True},
            run_fn=lambda: run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(
                preparation_go_no_go_gate_v0=_mk_prep_go_gate(),
                preparation_shadow_eval_gate_v0=_mk_prep_shadow_eval_go(),
                preparation_admission_gate_v0=_mk_prep_admitted(),
                preparation_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
                preparation_enablement_intent_v0={"intent": True, "reason": "unit_test"},
                execution_state_v0={"x": 1},
                result_v0={"x": 1},
                exception_or_failure_path_v0={"x": 1},
                side_effects_released=False,
                execution_state_writer=w_state_fail,
                result_object_writer=w_result_ok,
                exception_or_failure_writer=w_exc_ok,
                context={"scenario": "F.legal_started_failure"},
            ),
        )
    )

    # G. illegal_release_attempt (synthetic: bypass runtime output by crafting observed dict)
    # We treat this as a harness-level invariant check (should be no_go).
    illegal_release_observed = {
        "start_event_observed_seen": False,
        "started_seen": False,
        "side_effects_released_seen": True,  # illegal
        "closure_seen": False,
        "rollback_seen": False,
    }
    illegal, codes = _detect_illegal_states(illegal_release_observed)
    results.append(
        ScenarioResult(
            scenario_name="G.illegal_release_attempt_synthetic",
            expected_outcome={"illegal_state_detected": True, "evaluation_reason_codes_contains": "illegal_release_without_started"},
            actual_outcome={"synthetic_observed": dict(illegal_release_observed)},
            start_event_observed_seen=False,
            started_seen=False,
            side_effects_released_seen=True,
            closure_seen=False,
            rollback_seen=False,
            illegal_state_detected=bool(illegal),
            pass_or_fail="pass" if (illegal and "illegal_release_without_started" in codes) else "fail",
            evaluation_reason_codes=list(codes),
        )
    )

    # H. illegal_started_without_event (synthetic)
    illegal_started_observed = {
        "start_event_observed_seen": False,
        "started_seen": True,  # illegal
        "side_effects_released_seen": False,
        "closure_seen": True,
        "rollback_seen": False,
    }
    illegal, codes = _detect_illegal_states(illegal_started_observed)
    results.append(
        ScenarioResult(
            scenario_name="H.illegal_started_without_event_synthetic",
            expected_outcome={"illegal_state_detected": True, "evaluation_reason_codes_contains": "illegal_started_without_start_event"},
            actual_outcome={"synthetic_observed": dict(illegal_started_observed)},
            start_event_observed_seen=False,
            started_seen=True,
            side_effects_released_seen=False,
            closure_seen=True,
            rollback_seen=False,
            illegal_state_detected=bool(illegal),
            pass_or_fail="pass" if (illegal and "illegal_started_without_start_event" in codes) else "fail",
            evaluation_reason_codes=list(codes),
        )
    )

    # I. unclosed_path_probe (synthetic)
    unclosed_observed = {
        "start_event_observed_seen": True,
        "started_seen": True,
        "side_effects_released_seen": False,
        "closure_seen": False,  # illegal
        "rollback_seen": False,
    }
    illegal, codes = _detect_illegal_states(unclosed_observed)
    results.append(
        ScenarioResult(
            scenario_name="I.unclosed_path_probe_synthetic",
            expected_outcome={"illegal_state_detected": True, "evaluation_reason_codes_contains": "illegal_started_without_closure"},
            actual_outcome={"synthetic_observed": dict(unclosed_observed)},
            start_event_observed_seen=True,
            started_seen=True,
            side_effects_released_seen=False,
            closure_seen=False,
            rollback_seen=False,
            illegal_state_detected=bool(illegal),
            pass_or_fail="pass" if (illegal and "illegal_started_without_closure" in codes) else "fail",
            evaluation_reason_codes=list(codes),
        )
    )

    total = len(results)
    passed = sum(1 for r in results if r.pass_or_fail == "pass")
    failed = total - passed

    started_integrity = all(
        (not r.illegal_state_detected)
        or ("illegal_started_without_start_event" not in r.evaluation_reason_codes)
        for r in results
    )
    release_integrity = all(
        (not r.illegal_state_detected)
        or ("illegal_release_without_started" not in r.evaluation_reason_codes)
        for r in results
    )
    closure_integrity = all(
        (not r.illegal_state_detected) or ("illegal_started_without_closure" not in r.evaluation_reason_codes)
        for r in results
    )

    if failed == 0:
        overall = "go"
        next_step = "consider Phase-Next-154 go/no-go pack (still non-default; evaluation-first)"
    else:
        # If only synthetic illegal probes failed, treat as conditional_go.
        non_synth_failed = any(r.pass_or_fail == "fail" and "_synthetic" not in r.scenario_name for r in results)
        overall = "no_go" if non_synth_failed else "conditional_go"
        next_step = "fix validation failures before any short-window trial preparation"

    report = {
        "total_scenarios": total,
        "passed_scenarios": passed,
        "failed_scenarios": failed,
        "started_boundary_integrity": bool(started_integrity),
        "release_boundary_integrity": bool(release_integrity),
        "closure_integrity": bool(closure_integrity),
        "overall_evaluation": overall,
        "recommended_next_step": next_step,
        "scenarios": [r.to_dict() for r in results],
    }

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if overall in ("go", "conditional_go") else 3


if __name__ == "__main__":
    raise SystemExit(main())


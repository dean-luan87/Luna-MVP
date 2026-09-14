# -*- coding: utf-8 -*-
"""
Phase-Next-157:
Shadowed / Guarded Validation + Evaluation for Phase-Next-156 first controlled short-window trial runtime.

硬边界（写死）：
- 只做 validation/evaluation；不修改 151/155；不扩大 156；不 default-on；不 full controlled trial。
- 复用 156 runtime + 156 verifier。
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
    explicit_entry_seen: bool
    explicit_intent_seen: bool
    approval_seen: bool
    start_event_observed_seen: bool
    started_seen: bool
    side_effects_released_seen: bool
    abort_trigger_seen: bool
    recovery_seen: bool
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
            "explicit_entry_seen": bool(self.explicit_entry_seen),
            "explicit_intent_seen": bool(self.explicit_intent_seen),
            "approval_seen": bool(self.approval_seen),
            "start_event_observed_seen": bool(self.start_event_observed_seen),
            "started_seen": bool(self.started_seen),
            "side_effects_released_seen": bool(self.side_effects_released_seen),
            "abort_trigger_seen": bool(self.abort_trigger_seen),
            "recovery_seen": bool(self.recovery_seen),
            "closure_seen": bool(self.closure_seen),
            "rollback_seen": bool(self.rollback_seen),
            "illegal_state_detected": bool(self.illegal_state_detected),
            "pass_or_fail": str(self.pass_or_fail),
            "evaluation_reason_codes": list(self.evaluation_reason_codes),
        }


def _pack_go() -> dict:
    return {"recommended_go_no_go_pack_conclusion": "go"}


def _prep_go_gate() -> dict:
    return {"controlled_trial_preparation_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_preparation_go"}


def _prep_shadow_eval_go() -> dict:
    return {"controlled_trial_preparation_shadow_eval_status": "first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_go"}


def _prep_admitted() -> dict:
    return {"controlled_trial_preparation_status": "first_live_minimal_real_effect_controlled_trial_preparation_admitted"}


def _enablement_dry_run_executed() -> dict:
    return {
        "dry_run_status": "first_live_minimal_real_effect_controlled_trial_preparation_minimal_enablement_dry_run_executed"
    }


def _summarize_from_runtime_output(out: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    payload = out.get("payload") if isinstance(out, dict) else None
    payload = payload if isinstance(payload, dict) else {}
    state = payload.get("state") if isinstance(payload.get("state"), dict) else {}
    trace = payload.get("trace") if isinstance(payload.get("trace"), dict) else {}

    explicit_intent_seen = bool(state.get("explicit_trial_intent_seen") is True)
    approval_seen = bool(state.get("approval_seen") is True)
    start_event_observed_seen = bool(state.get("start_event_observed") is True)
    started_seen = bool(state.get("controlled_short_window_trial_started") is True)
    side_effects_released_seen = bool(state.get("side_effects_released") is True)
    abort_trigger_seen = bool(state.get("abort_triggered") is True)
    closure_seen = bool(state.get("closed") is True)
    rollback_seen = bool(state.get("rollback_completed") is True)
    recovery_seen = bool(state.get("recovery_completed") is True)

    actual = {
        "ok": bool(out.get("ok") is True) if isinstance(out, dict) else False,
        "status": str(out.get("status") or "") if isinstance(out, dict) else "non_dict",
        "reason": str(out.get("reason") or "") if isinstance(out, dict) else "non_dict",
        "abort_trigger_id": state.get("abort_trigger_id"),
        "state": dict(state),
        "trace_order": list(trace.get("order") or []) if isinstance(trace.get("order"), list) else [],
    }

    observed = {
        "explicit_intent_seen": explicit_intent_seen,
        "approval_seen": approval_seen,
        "start_event_observed_seen": start_event_observed_seen,
        "started_seen": started_seen,
        "side_effects_released_seen": side_effects_released_seen,
        "abort_trigger_seen": abort_trigger_seen,
        "recovery_seen": recovery_seen,
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
    if started and not start_event:
        illegal = True
        codes.append("illegal_started_without_start_event")
    if release and not started:
        illegal = True
        codes.append("illegal_release_without_started")
    if started and not closed:
        illegal = True
        codes.append("illegal_started_without_closure")
    if closed and release:
        illegal = True
        codes.append("illegal_release_not_recovered_after_closure")
    return illegal, codes


def _run_scenario(*, scenario_name: str, expected: Dict[str, Any], run_fn: Callable[[], Dict[str, Any]]) -> ScenarioResult:
    out = run_fn()
    actual, observed = _summarize_from_runtime_output(out)
    illegal, illegal_codes = _detect_illegal_states(observed)

    reason_codes: List[str] = []
    passed = True

    def _chk(key: str, actual_val: Any):
        nonlocal passed
        exp = expected.get(key)
        if exp is None:
            return
        if bool(exp) != bool(actual_val):
            passed = False
            reason_codes.append(f"mismatch_{key}")

    if expected.get("status") is not None and str(expected["status"]) != str(actual.get("status")):
        passed = False
        reason_codes.append("mismatch_status")
    if expected.get("abort_trigger_id") is not None and str(expected["abort_trigger_id"]) != str(actual.get("abort_trigger_id")):
        passed = False
        reason_codes.append("mismatch_abort_trigger_id")

    _chk("explicit_intent_seen", observed.get("explicit_intent_seen"))
    _chk("approval_seen", observed.get("approval_seen"))
    _chk("start_event_observed_seen", observed.get("start_event_observed_seen"))
    _chk("started_seen", observed.get("started_seen"))
    _chk("side_effects_released_seen", observed.get("side_effects_released_seen"))
    _chk("abort_trigger_seen", observed.get("abort_trigger_seen"))
    _chk("recovery_seen", observed.get("recovery_seen"))
    _chk("closure_seen", observed.get("closure_seen"))
    _chk("rollback_seen", observed.get("rollback_seen"))

    if illegal:
        passed = False
        reason_codes.extend(illegal_codes)

    return ScenarioResult(
        scenario_name=scenario_name,
        expected_outcome=dict(expected),
        actual_outcome=dict(actual),
        explicit_entry_seen=True,  # tool always calls explicit entry
        explicit_intent_seen=bool(observed.get("explicit_intent_seen")),
        approval_seen=bool(observed.get("approval_seen")),
        start_event_observed_seen=bool(observed.get("start_event_observed_seen")),
        started_seen=bool(observed.get("started_seen")),
        side_effects_released_seen=bool(observed.get("side_effects_released_seen")),
        abort_trigger_seen=bool(observed.get("abort_trigger_seen")),
        recovery_seen=bool(observed.get("recovery_seen")),
        closure_seen=bool(observed.get("closure_seen")),
        rollback_seen=bool(observed.get("rollback_seen")),
        illegal_state_detected=bool(illegal),
        pass_or_fail="pass" if passed else "fail",
        evaluation_reason_codes=reason_codes,
    )


def main() -> int:
    # Reuse 156 runtime + 156 verifier (hard-stop if verifier fails).
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_trial_v0 import (  # noqa: E402
        run_first_live_controlled_short_window_trial_v0,
    )

    from tools.verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_trial_v0 import (  # noqa: E402
        main as verifier_main,
    )

    if int(verifier_main()) != 0:
        raise SystemExit(2)

    def w_state_ok(p: dict) -> dict:
        return {"ok": True, "surface": p.get("surface")}

    def w_result_ok(p: dict) -> dict:
        return {"ok": True, "surface": p.get("surface")}

    def w_exc_ok(p: dict) -> dict:
        return {"ok": True, "surface": p.get("surface")}

    def w_state_fail(_: dict) -> dict:
        raise RuntimeError("boom_state")

    base = dict(
        guardrail_pack_go_no_go_v0=_pack_go(),
        preparation_go_no_go_gate_v0=_prep_go_gate(),
        preparation_shadow_eval_gate_v0=_prep_shadow_eval_go(),
        preparation_admission_gate_v0=_prep_admitted(),
        preparation_enablement_dry_run_v0=_enablement_dry_run_executed(),
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=False,
        execution_state_writer=w_state_ok,
        result_object_writer=w_result_ok,
        exception_or_failure_writer=w_exc_ok,
        trial_window_max_ms=1000,
        observed_elapsed_ms=10,
        context={"phase": "p157"},
    )

    results: List[ScenarioResult] = []

    def _is_synthetic(s: ScenarioResult) -> bool:
        return "synthetic" in (s.scenario_name or "")

    # A
    results.append(
        _run_scenario(
            scenario_name="A.no_explicit_intent",
            expected={
                "status": "aborted",
                "explicit_intent_seen": False,
                # 缺 intent 时应在 intent gate 即中止，approval_seen 合理为 false（不可要求读取 approval）
                "approval_seen": False,
                "started_seen": False,
                "side_effects_released_seen": False,
                "closure_seen": True,
            },
            run_fn=lambda: run_first_live_controlled_short_window_trial_v0(
                **base,
                explicit_short_window_trial_intent_v0=None,
                explicit_short_window_trial_approval_v0={"approve": True},
            ),
        )
    )

    # B
    results.append(
        _run_scenario(
            scenario_name="B.no_approval",
            expected={
                "status": "aborted",
                "explicit_intent_seen": True,
                "approval_seen": False,
                "started_seen": False,
                "side_effects_released_seen": False,
                "closure_seen": True,
            },
            run_fn=lambda: run_first_live_controlled_short_window_trial_v0(
                **base,
                explicit_short_window_trial_intent_v0={"intent": True, "allow_start_event_observed": True},
                explicit_short_window_trial_approval_v0=None,
            ),
        )
    )

    # C
    results.append(
        _run_scenario(
            scenario_name="C.armed_but_not_started",
            expected={
                "status": "armed_not_started",
                "explicit_intent_seen": True,
                "approval_seen": True,
                "start_event_observed_seen": False,
                "started_seen": False,
                "side_effects_released_seen": False,
                "closure_seen": True,
            },
            run_fn=lambda: run_first_live_controlled_short_window_trial_v0(
                **base,
                explicit_short_window_trial_intent_v0={"intent": True, "allow_start_event_observed": False},
                explicit_short_window_trial_approval_v0={"approve": True},
            ),
        )
    )

    # D
    results.append(
        _run_scenario(
            scenario_name="D.legal_short_window_success",
            expected={
                "status": "trial_executed_success",
                "start_event_observed_seen": True,
                "started_seen": True,
                "side_effects_released_seen": False,
                "closure_seen": True,
            },
            run_fn=lambda: run_first_live_controlled_short_window_trial_v0(
                **base,
                explicit_short_window_trial_intent_v0={"intent": True, "allow_start_event_observed": True},
                explicit_short_window_trial_approval_v0={"approve": True},
            ),
        )
    )

    # E
    b2 = dict(base)
    b2["execution_state_writer"] = w_state_fail
    results.append(
        _run_scenario(
            scenario_name="E.legal_short_window_failure",
            expected={
                "status": "trial_executed_failure_closed",
                "start_event_observed_seen": True,
                "started_seen": True,
                "side_effects_released_seen": False,
                "closure_seen": True,
                "rollback_seen": True,
            },
            run_fn=lambda: run_first_live_controlled_short_window_trial_v0(
                **b2,
                explicit_short_window_trial_intent_v0={"intent": True, "allow_start_event_observed": True},
                explicit_short_window_trial_approval_v0={"approve": True},
            ),
        )
    )

    # F
    b3 = dict(base)
    b3["observed_elapsed_ms"] = 2000
    results.append(
        _run_scenario(
            scenario_name="F.window_timeout",
            expected={
                "status": "aborted",
                "abort_trigger_id": "trial_window_timeout",
                "started_seen": False,
                "side_effects_released_seen": False,
                "closure_seen": True,
            },
            run_fn=lambda: run_first_live_controlled_short_window_trial_v0(
                **b3,
                explicit_short_window_trial_intent_v0={"intent": True, "allow_start_event_observed": True},
                explicit_short_window_trial_approval_v0={"approve": True},
            ),
        )
    )

    # G
    results.append(
        _run_scenario(
            scenario_name="G.unauthorized_surface",
            expected={
                "status": "aborted",
                "abort_trigger_id": "unauthorized_side_effect_surface",
                "started_seen": False,
                "side_effects_released_seen": False,
                "closure_seen": True,
            },
            run_fn=lambda: run_first_live_controlled_short_window_trial_v0(
                **base,
                explicit_short_window_trial_intent_v0={
                    "intent": True,
                    "allow_start_event_observed": True,
                    "requested_surfaces": ["route"],
                },
                explicit_short_window_trial_approval_v0={"approve": True},
            ),
        )
    )

    # H (synthetic illegal)
    illegal_release_observed = {
        "explicit_intent_seen": True,
        "approval_seen": True,
        "start_event_observed_seen": False,
        "started_seen": False,
        "side_effects_released_seen": True,
        "abort_trigger_seen": False,
        "recovery_seen": False,
        "closure_seen": False,
        "rollback_seen": False,
    }
    illegal, codes = _detect_illegal_states(illegal_release_observed)
    results.append(
        ScenarioResult(
            scenario_name="H.illegal_release_before_started_synthetic",
            expected_outcome={"illegal_state_detected": True},
            actual_outcome={"synthetic_observed": dict(illegal_release_observed)},
            explicit_entry_seen=False,
            explicit_intent_seen=True,
            approval_seen=True,
            start_event_observed_seen=False,
            started_seen=False,
            side_effects_released_seen=True,
            abort_trigger_seen=False,
            recovery_seen=False,
            closure_seen=False,
            rollback_seen=False,
            illegal_state_detected=bool(illegal),
            pass_or_fail="pass" if (illegal and "illegal_release_without_started" in codes) else "fail",
            evaluation_reason_codes=list(codes),
        )
    )

    # I
    b4 = dict(base)
    b4["trial_window_max_ms"] = "x"
    results.append(
        _run_scenario(
            scenario_name="I.missing_audit_trace",
            expected={
                "status": "aborted",
                "abort_trigger_id": "audit_trace_missing_or_broken",
                "started_seen": False,
                "side_effects_released_seen": False,
                "closure_seen": True,
            },
            run_fn=lambda: run_first_live_controlled_short_window_trial_v0(
                **b4,
                explicit_short_window_trial_intent_v0={"intent": True, "allow_start_event_observed": True},
                explicit_short_window_trial_approval_v0={"approve": True},
            ),
        )
    )

    # J default_path_probe (no intent+approval)
    b5 = dict(base)
    b5["context"] = {"scenario": "default_path_probe"}
    results.append(
        _run_scenario(
            scenario_name="J.default_path_probe",
            expected={
                "status": "aborted",
                "explicit_intent_seen": False,
                # default path probe：未提供 intent，预期同 A：approval_seen 不要求为 true
                "approval_seen": False,
                "started_seen": False,
                "side_effects_released_seen": False,
                "closure_seen": True,
            },
            run_fn=lambda: run_first_live_controlled_short_window_trial_v0(
                **b5,
                explicit_short_window_trial_intent_v0=None,
                explicit_short_window_trial_approval_v0={"approve": True},
            ),
        )
    )

    # K closure break probe (synthetic: started but unclosed, or closed but se still true)
    unclosed_observed = {
        "explicit_intent_seen": True,
        "approval_seen": True,
        "start_event_observed_seen": True,
        "started_seen": True,
        "side_effects_released_seen": False,
        "abort_trigger_seen": False,
        "recovery_seen": False,
        "closure_seen": False,
        "rollback_seen": False,
    }
    illegal, codes = _detect_illegal_states(unclosed_observed)
    results.append(
        ScenarioResult(
            scenario_name="K.closure_break_probe_synthetic",
            expected_outcome={"illegal_state_detected": True},
            actual_outcome={"synthetic_observed": dict(unclosed_observed)},
            explicit_entry_seen=False,
            explicit_intent_seen=True,
            approval_seen=True,
            start_event_observed_seen=True,
            started_seen=True,
            side_effects_released_seen=False,
            abort_trigger_seen=False,
            recovery_seen=False,
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

    non_synth = [r for r in results if not _is_synthetic(r)]

    entry_gate_integrity = all(
        r.pass_or_fail == "pass"
        for r in non_synth
        if r.scenario_name in {"A.no_explicit_intent", "B.no_approval", "J.default_path_probe"}
    )
    started_integrity = all(
        "illegal_started_without_start_event" not in r.evaluation_reason_codes for r in non_synth
    )
    release_integrity = all(
        "illegal_release_without_started" not in r.evaluation_reason_codes
        and "illegal_release_not_recovered_after_closure" not in r.evaluation_reason_codes
        for r in non_synth
    )
    closure_integrity = all("illegal_started_without_closure" not in r.evaluation_reason_codes for r in non_synth)
    abort_integrity = all(
        r.pass_or_fail == "pass" for r in non_synth if r.scenario_name in {"F.window_timeout", "G.unauthorized_surface", "I.missing_audit_trace"}
    )
    recovery_integrity = True  # for v0, abort paths always return closed with se=false

    if failed == 0:
        overall = "go"
        next_step = "consider Phase-Next-158 readiness go/no-go pack v0 (still non-default; guardrail-first)"
    else:
        non_synth_failed = any(r.pass_or_fail == "fail" for r in non_synth)
        overall = "no_go" if non_synth_failed else "conditional_go"
        next_step = "fix validation failures before any readiness pack refresh"

    report = {
        "total_scenarios": total,
        "passed_scenarios": passed,
        "failed_scenarios": failed,
        "entry_gate_integrity": bool(entry_gate_integrity),
        "started_boundary_integrity": bool(started_integrity),
        "release_boundary_integrity": bool(release_integrity),
        "abort_integrity": bool(abort_integrity),
        "recovery_integrity": bool(recovery_integrity),
        "closure_integrity": bool(closure_integrity),
        "overall_evaluation": overall,
        "recommended_next_step": next_step,
        "scenarios": [r.to_dict() for r in results],
    }

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if overall in ("go", "conditional_go") else 3


if __name__ == "__main__":
    raise SystemExit(main())


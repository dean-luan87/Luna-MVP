# -*- coding: utf-8 -*-
"""
Self-test: Controlled Trial First Minimal Real Enablement Code v0 (REAL, minimal; using in-memory writers).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _mk_trial_go() -> dict:
    return {"controlled_trial_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_go"}


def _mk_enablement_dry_run_executed() -> dict:
    return {"dry_run_status": "first_live_minimal_real_effect_controlled_trial_enablement_dry_run_executed"}


def _mk_real_enablement_ready() -> dict:
    return {"real_enablement_status": "first_live_minimal_real_effect_controlled_trial_real_enablement_ready"}


def _mk_xs() -> dict:
    return {"execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}


def _mk_rs() -> dict:
    return {"result_scope": "navigation_governance_action_release_control_result_v0"}


def _mk_ex() -> dict:
    return {"exception_or_failure_path_scope": "exception_or_failure_path_v0"}


def main() -> int:
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_real_enablement_v0 import (  # noqa: E402
        run_first_live_controlled_trial_first_minimal_real_enablement_v0,
    )

    writes = {"state": [], "result": [], "ex": []}

    def _state_writer(payload: dict) -> dict:
        writes["state"].append(dict(payload))
        return {"ok": True}

    def _result_writer(payload: dict) -> dict:
        writes["result"].append(dict(payload))
        return {"ok": True}

    def _ex_writer(payload: dict) -> dict:
        writes["ex"].append(dict(payload))
        return {"ok": True}

    # 1) normal executed
    res = run_first_live_controlled_trial_first_minimal_real_enablement_v0(
        controlled_trial_go_no_go_gate_v0=_mk_trial_go(),
        controlled_trial_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_real_enablement_ready(),
        real_enablement_approval_or_signal_v0={"enable": True},
        execution_state_v0=_mk_xs(),
        result_v0=_mk_rs(),
        exception_or_failure_path_v0=_mk_ex(),
        side_effects_released=False,
        execution_state_writer=_state_writer,
        result_object_writer=_result_writer,
        exception_or_failure_writer=_ex_writer,
        context={"test": "normal"},
    )
    assert res.get("ok") is True and res.get("status") == "executed"
    assert len(writes["state"]) == 1 and len(writes["result"]) == 1 and len(writes["ex"]) == 0

    # 2) missing signal -> not_ready, no writes
    writes2 = {"state": [], "result": [], "ex": []}

    def _s2(p: dict) -> dict:
        writes2["state"].append(dict(p))
        return {"ok": True}

    def _r2(p: dict) -> dict:
        writes2["result"].append(dict(p))
        return {"ok": True}

    def _e2(p: dict) -> dict:
        writes2["ex"].append(dict(p))
        return {"ok": True}

    res2 = run_first_live_controlled_trial_first_minimal_real_enablement_v0(
        controlled_trial_go_no_go_gate_v0=_mk_trial_go(),
        controlled_trial_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_real_enablement_ready(),
        real_enablement_approval_or_signal_v0=None,
        execution_state_v0=_mk_xs(),
        result_v0=_mk_rs(),
        exception_or_failure_path_v0=_mk_ex(),
        side_effects_released=False,
        execution_state_writer=_s2,
        result_object_writer=_r2,
        exception_or_failure_writer=_e2,
        context={"test": "missing_signal"},
    )
    assert res2.get("ok") is False and res2.get("status") == "not_ready"
    assert len(writes2["state"]) == 0 and len(writes2["result"]) == 0 and len(writes2["ex"]) == 0

    # 3) side_effects_released != False -> blocked, no writes
    writes3 = {"state": [], "result": [], "ex": []}

    def _s3(p: dict) -> dict:
        writes3["state"].append(dict(p))
        return {"ok": True}

    def _r3(p: dict) -> dict:
        writes3["result"].append(dict(p))
        return {"ok": True}

    def _e3(p: dict) -> dict:
        writes3["ex"].append(dict(p))
        return {"ok": True}

    res3 = run_first_live_controlled_trial_first_minimal_real_enablement_v0(
        controlled_trial_go_no_go_gate_v0=_mk_trial_go(),
        controlled_trial_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_real_enablement_ready(),
        real_enablement_approval_or_signal_v0={"enable": True},
        execution_state_v0=_mk_xs(),
        result_v0=_mk_rs(),
        exception_or_failure_path_v0=_mk_ex(),
        side_effects_released=True,
        execution_state_writer=_s3,
        result_object_writer=_r3,
        exception_or_failure_writer=_e3,
        context={"test": "blocked"},
    )
    assert res3.get("ok") is False and res3.get("status") == "blocked"
    assert len(writes3["state"]) == 0 and len(writes3["result"]) == 0 and len(writes3["ex"]) == 0

    # 4) state write failure -> failed + failure writes attempted + exception write attempted
    writes4 = {"state": [], "result": [], "ex": []}
    fail_once = {"done": False}

    def _s4(p: dict) -> dict:
        if not fail_once["done"]:
            fail_once["done"] = True
            raise RuntimeError("boom")
        writes4["state"].append(dict(p))
        return {"ok": True}

    def _r4(p: dict) -> dict:
        writes4["result"].append(dict(p))
        return {"ok": True}

    def _e4(p: dict) -> dict:
        writes4["ex"].append(dict(p))
        return {"ok": True}

    res4 = run_first_live_controlled_trial_first_minimal_real_enablement_v0(
        controlled_trial_go_no_go_gate_v0=_mk_trial_go(),
        controlled_trial_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_real_enablement_ready(),
        real_enablement_approval_or_signal_v0={"enable": True},
        execution_state_v0=_mk_xs(),
        result_v0=_mk_rs(),
        exception_or_failure_path_v0=_mk_ex(),
        side_effects_released=False,
        execution_state_writer=_s4,
        result_object_writer=_r4,
        exception_or_failure_writer=_e4,
        context={"test": "state_fail"},
    )
    assert res4.get("ok") is False and res4.get("status") == "failed"
    assert len(writes4["ex"]) == 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


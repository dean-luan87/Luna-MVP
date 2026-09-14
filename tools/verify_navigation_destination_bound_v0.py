#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify destination_bound_v0 materialization (minimal, metadata-only).

Scenarios:
- A: all hard conditions met -> writes destination_bound_v0 with binding_key/value
- B: missing confirmation -> not written
- C: missing binding evidence -> not written
- D: blocker (needs_confirmation=true) -> not written
- E: ordinary input via mainline -> not written
- F: V1 minimal flow remains OK (run separately)
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _stub_res(
    *,
    has_confirmation: bool,
    has_binding: bool,
    upgrade_eligible: bool,
    materialize_ready: bool,
    needs_confirmation: bool,
) -> Any:
    from capabilities.voice.bridge.route_types import BridgeRouteType

    proposal = SimpleNamespace(task_action="start_navigation")
    if has_binding:
        setattr(proposal, "destination_id", "dest_123")
    bd = SimpleNamespace(route=BridgeRouteType.TASK_LIFECYCLE, proposal=proposal)

    md: Dict[str, Any] = {
        "destination_candidate_v0": {"candidate_present": True, "candidate_text": "人民广场"},
        "destination_bound_check_v0": (
            {
                "bound_ready": True,
                "check_scope": "navigation_destination_bound_check_v0",
                "binding_key_seen": "destination_id",
                "needs_confirmation": False,
            }
            if has_binding
            else {
                "bound_ready": False,
                "check_scope": "navigation_destination_bound_check_v0",
                "reason": "missing_binding_evidence",
            }
        ),
        "destination_bound_upgrade_eval_v0": (
            {
                "eligible": True,
                "eval_scope": "navigation_destination_bound_upgrade_v0",
                "upgrade_scope": "future_bound_candidate_only",
                **({"needs_confirmation": True} if needs_confirmation else {}),
            }
            if upgrade_eligible
            else {
                "eligible": False,
                "eval_scope": "navigation_destination_bound_upgrade_v0",
                "reason": "missing",
            }
        ),
        "destination_bound_materialization_eval_v0": (
            {
                "materialize_ready": True,
                "eval_scope": "navigation_destination_bound_materialization_v0",
                "materialization_scope": "future_bound_materialization_candidate_only",
            }
            if materialize_ready
            else {
                "materialize_ready": False,
                "eval_scope": "navigation_destination_bound_materialization_v0",
                "reason": "blocked",
            }
        ),
    }

    if has_confirmation:
        md["destination_confirmation_fact_v0"] = {
            "confirmation_ready": True,
            "check_scope": "navigation_destination_confirmation_fact_v0",
            "confirmation_target": "current_destination_candidate",
            **({"needs_confirmation": True} if needs_confirmation else {}),
        }

    return SimpleNamespace(dispatch_type="short_controlled_input", bridge_decision=bd, metadata=md)


def main() -> int:
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "0"

    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402
    from capabilities.voice.runtime.voice_navigation_destination_bound_v0 import (  # noqa: E402
        materialize_destination_bound_v0_if_allowed,
    )

    # A
    res_a = _stub_res(
        has_confirmation=True,
        has_binding=True,
        upgrade_eligible=True,
        materialize_ready=True,
        needs_confirmation=False,
    )
    ok_a, bnd_a = materialize_destination_bound_v0_if_allowed(res=res_a)
    assert ok_a is True
    assert isinstance(bnd_a, dict)
    assert bnd_a.get("destination_bound") is True
    assert bnd_a.get("binding_key") == "destination_id"
    assert bnd_a.get("binding_value") == "dest_123"

    # B
    res_b = _stub_res(
        has_confirmation=False,
        has_binding=True,
        upgrade_eligible=True,
        materialize_ready=True,
        needs_confirmation=False,
    )
    ok_b, bnd_b = materialize_destination_bound_v0_if_allowed(res=res_b)
    assert ok_b is False and bnd_b is None

    # C
    res_c = _stub_res(
        has_confirmation=True,
        has_binding=False,
        upgrade_eligible=False,
        materialize_ready=False,
        needs_confirmation=False,
    )
    ok_c, bnd_c = materialize_destination_bound_v0_if_allowed(res=res_c)
    assert ok_c is False and bnd_c is None

    # D (blocker)
    res_d = _stub_res(
        has_confirmation=True,
        has_binding=True,
        upgrade_eligible=True,
        materialize_ready=False,
        needs_confirmation=True,
    )
    ok_d, bnd_d = materialize_destination_bound_v0_if_allowed(res=res_d)
    assert ok_d is False and bnd_d is None

    # E (ordinary input via mainline should not write destination_bound_v0)
    mgr = VoiceInputSessionManager()
    res_e = mgr.process_final_text_with_dispatch(
        "你好",
        now=time.time(),
        is_task_mode=False,
        session_id="dest_bound_v0_e",
        source_type="simulated",
    )
    md_e: Dict[str, Any] = dict(getattr(res_e, "metadata", {}) or {})
    assert md_e.get("destination_bound_v0") is None

    print("VERIFY_NAVIGATION_DESTINATION_BOUND_V0: ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


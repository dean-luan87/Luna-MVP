#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify destination_bound_check_v0 (read-only evaluator).

Scenarios:
- A: start_navigation + destination_candidate_v0 present but no explicit binding fields -> bound_ready=false, reason=missing_binding_evidence
- B: stub with destination_candidate_v0 + destination_id -> bound_ready=true, binding_key_seen=destination_id, does NOT write destination_bound
- C: ordinary input -> not written by dispatcher
- D: V1 minimal flow remains OK (run separately)
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


def _stub_res(*, has_binding: bool) -> tuple[Any, Any]:
    from capabilities.voice.bridge.route_types import BridgeRouteType

    event = SimpleNamespace(metadata={})
    proposal = SimpleNamespace(task_action="start_navigation")
    if has_binding:
        proposal.destination_id = "dest_123"
    bd = SimpleNamespace(route=BridgeRouteType.TASK_LIFECYCLE, proposal=proposal)
    res = SimpleNamespace(
        dispatch_type="short_controlled_input",
        bridge_decision=bd,
        metadata={
            "destination_candidate_v0": {
                "candidate_present": True,
                "candidate_text": "人民广场",
                "candidate_scope": "navigation_destination_candidate_v0",
                "requires_confirmation": True,
                "binding_reason": "candidate_captured_but_not_bound",
            }
        },
    )
    return res, event


def main() -> int:
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "0"

    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402
    from capabilities.voice.runtime.voice_navigation_destination_bound_check_v0 import (  # noqa: E402
        evaluate_destination_bound_check_v0,
    )

    # A: candidate present, no binding fields
    res_a, ev_a = _stub_res(has_binding=False)
    app_a, out_a = evaluate_destination_bound_check_v0(res=res_a, event=ev_a)
    assert app_a is True
    assert isinstance(out_a, dict)
    assert out_a.get("bound_ready") is False
    assert out_a.get("reason") == "missing_binding_evidence"

    # B: candidate present + destination_id
    res_b, ev_b = _stub_res(has_binding=True)
    app_b, out_b = evaluate_destination_bound_check_v0(res=res_b, event=ev_b)
    assert app_b is True
    assert isinstance(out_b, dict)
    assert out_b.get("bound_ready") is True
    assert out_b.get("binding_key_seen") == "destination_id"
    # sanity: evaluator must not output destination_bound
    assert "destination_bound" not in out_b

    # C: ordinary input through mainline should not write destination_bound_check_v0
    mgr = VoiceInputSessionManager()
    res_c = mgr.process_final_text_with_dispatch(
        "你好",
        now=time.time(),
        is_task_mode=False,
        session_id="dest_bound_check_c",
        source_type="simulated",
    )
    md_c: Dict[str, Any] = dict(getattr(res_c, "metadata", {}) or {})
    assert md_c.get("destination_bound_check_v0") is None

    print("VERIFY_NAVIGATION_DESTINATION_BOUND_CHECK_V0: ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


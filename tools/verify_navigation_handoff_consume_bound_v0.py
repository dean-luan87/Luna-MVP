#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify navigation_handoff_consume_bound_v0 (minimal, read-only consume).

Scenarios:
- A: start_navigation + destination_bound_v0 present -> produces consume dict with binding_key/value
- B: only candidate/confirmation but no bound -> no consume dict
- C: ordinary input via mainline -> field not written
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


def _stub_decision_start_nav() -> Any:
    from capabilities.voice.bridge.route_types import BridgeRouteType

    proposal = SimpleNamespace(task_action="start_navigation")
    return SimpleNamespace(route=BridgeRouteType.TASK_LIFECYCLE, proposal=proposal)


def main() -> int:
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "0"

    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402
    from capabilities.voice.runtime.voice_navigation_handoff_v0 import (  # noqa: E402
        consume_destination_bound_v0_in_handoff_v0,
    )

    # A
    bd = _stub_decision_start_nav()
    bound = {
        "destination_bound": True,
        "binding_key": "destination_id",
        "binding_value": "dest_123",
        "binding_reason": "candidate_confirmed_and_materialization_ready",
        "bound_scope": "navigation_start_v0",
    }
    out_a = consume_destination_bound_v0_in_handoff_v0(bd, destination_bound_v0=bound)
    assert isinstance(out_a, dict)
    assert out_a.get("bound_consumed") is True
    assert out_a.get("binding_key") == "destination_id"
    assert out_a.get("binding_value") == "dest_123"
    assert out_a.get("executor") == "voice_navigation_handoff_v0"

    # B
    out_b = consume_destination_bound_v0_in_handoff_v0(bd, destination_bound_v0=None)
    assert out_b is None

    # C: ordinary input via mainline should not write the field
    mgr = VoiceInputSessionManager()
    res_c = mgr.process_final_text_with_dispatch(
        "你好",
        now=time.time(),
        is_task_mode=False,
        session_id="handoff_consume_bound_c",
        source_type="simulated",
    )
    md_c: Dict[str, Any] = dict(getattr(res_c, "metadata", {}) or {})
    assert md_c.get("navigation_handoff_consume_bound_v0") is None

    print("VERIFY_NAVIGATION_HANDOFF_CONSUME_BOUND_V0: ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify navigation mainline thread wiring v0 (observable boundary only).

Goal:
- Ensure navigation-related shortcut produces TASK_LIFECYCLE proposal
- Ensure BridgeDecision is handed to core boundary placeholder trace (metadata["core_placeholder_v1"])
- Ensure no submit behavior expansion is required for this wiring check
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def main() -> None:
    # keep submit off: this test is about wiring/trace, not speaking.
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "0"

    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402

    mgr = VoiceInputSessionManager()
    # task mode to allow shortcut without wake word; "开始导航" is whitelisted task_start_nav.
    res = mgr.process_final_text_with_dispatch(
        "开始导航",
        now=1.0,
        is_task_mode=True,
        session_id="nav_wiring_v0",
        source_type="simulated",
    )
    assert getattr(res, "dispatch_type", "") == "short_controlled_input"
    bd = getattr(res, "bridge_decision", None)
    assert bd is not None, "bridge_decision_missing"
    r = getattr(bd, "route", None)
    route_s = str(getattr(r, "value", "") or r or "")
    assert route_s == "task_lifecycle", f"route_not_task_lifecycle:{r!r}"

    prop = getattr(bd, "proposal", None)
    assert prop is not None, "proposal_missing"
    # TaskActionProposal has task_action, and "task_start_nav" maps to "start_navigation".
    task_action = getattr(prop, "task_action", None)
    assert task_action == "start_navigation", f"task_action_unexpected:{task_action!r}"

    md: Dict[str, Any] = dict(getattr(res, "metadata", {}) or {})
    core = md.get("core_placeholder_v1")
    assert isinstance(core, dict) and core.get("received") is True, f"core_placeholder_trace_missing:{core!r}"
    tr = core.get("trace") if isinstance(core.get("trace"), dict) else {}
    assert str(tr.get("route") or "") == "task_lifecycle", f"core_trace_route_unexpected:{tr!r}"

    print("VERIFY_NAVIGATION_MAINLINE_THREAD_WIRING_V0: ALL_OK")


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify destination_candidate_v0 carrier + minimal evaluator (v0).

Scenarios:
- A: nav context established (start_navigation + missing_destination) then user supplies a place-like text -> captured
- B: same nav context but user says "继续" -> not captured
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


def _stub_nav_context_result(*, candidate_text: str) -> tuple[Any, Any]:
    """
    Build:
    - event: supplies candidate_text
    - res: mimics dispatcher output with strict nav missing-destination context
    """
    from capabilities.voice.bridge.route_types import BridgeRouteType

    event = SimpleNamespace(wake_word_stripped=candidate_text, normalized_text=candidate_text)
    proposal = SimpleNamespace(task_action="start_navigation")
    bd = SimpleNamespace(route=BridgeRouteType.TASK_LIFECYCLE, proposal=proposal)
    res = SimpleNamespace(
        dispatch_type="short_controlled_input",
        bridge_decision=bd,
        metadata={
            "destination_sufficiency_eval_v0": {
                "destination_sufficient": False,
                "eval_scope": "navigation_destination_sufficiency_v0",
                "reason": "missing_destination",
            }
        },
    )
    return event, res


def main() -> int:
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "0"

    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402
    from capabilities.voice.runtime.voice_navigation_destination_candidate_v0 import (  # noqa: E402
        capture_destination_candidate_v0,
    )

    # A: nav context + "人民广场"
    ev_a, res_a = _stub_nav_context_result(candidate_text="人民广场")
    out_a = capture_destination_candidate_v0(event=ev_a, navigation_context_result=res_a)
    assert isinstance(out_a, dict), f"candidate_missing:{out_a!r}"
    assert out_a.get("candidate_present") is True
    assert out_a.get("candidate_text") == "人民广场"
    assert out_a.get("requires_confirmation") is True

    # B: nav context + "继续"
    ev_b, res_b = _stub_nav_context_result(candidate_text="继续")
    out_b = capture_destination_candidate_v0(event=ev_b, navigation_context_result=res_b)
    assert out_b is None, f"unexpected_candidate_for_continue:{out_b!r}"

    # C: ordinary input through mainline should not write destination_candidate_v0
    mgr = VoiceInputSessionManager()
    res_c = mgr.process_final_text_with_dispatch(
        "你好",
        now=time.time(),
        is_task_mode=False,
        session_id="dest_candidate_c",
        source_type="simulated",
    )
    md_c: Dict[str, Any] = dict(getattr(res_c, "metadata", {}) or {})
    assert md_c.get("destination_candidate_v0") is None

    print("VERIFY_NAVIGATION_DESTINATION_CANDIDATE_V0: ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


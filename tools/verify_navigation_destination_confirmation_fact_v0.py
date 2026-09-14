#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify destination_confirmation_fact_check_v0 (read-only evaluator).

Scenarios:
- A: start_navigation + candidate present + input "对" -> confirmation_ready=true, target=current_destination_candidate
- B: start_navigation + candidate present + input "不是" -> confirmation_ready=false, reason=negative_or_rejection_signal
- C: start_navigation + candidate present + input "人民广场" -> confirmation_ready=false, reason=no_confirmation_signal
- D: ordinary input -> not written by dispatcher
- E: V1 minimal flow remains OK (run separately)
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


def _stub_res_with_candidate() -> Any:
    from capabilities.voice.bridge.route_types import BridgeRouteType

    proposal = SimpleNamespace(task_action="start_navigation")
    bd = SimpleNamespace(route=BridgeRouteType.TASK_LIFECYCLE, proposal=proposal)
    return SimpleNamespace(
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


def _stub_event(text: str) -> Any:
    return SimpleNamespace(wake_word_stripped=text, normalized_text=text, raw_text=text, metadata={})


def main() -> int:
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "0"

    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402
    from capabilities.voice.runtime.voice_navigation_destination_confirmation_fact_v0 import (  # noqa: E402
        evaluate_destination_confirmation_fact_check_v0,
    )

    res = _stub_res_with_candidate()

    # A
    app_a, out_a = evaluate_destination_confirmation_fact_check_v0(res=res, event=_stub_event("对"))
    assert app_a is True
    assert isinstance(out_a, dict)
    assert out_a.get("confirmation_ready") is True
    assert out_a.get("confirmation_target") == "current_destination_candidate"

    # B
    app_b, out_b = evaluate_destination_confirmation_fact_check_v0(res=res, event=_stub_event("不是"))
    assert app_b is True
    assert isinstance(out_b, dict)
    assert out_b.get("confirmation_ready") is False
    assert out_b.get("reason") == "negative_or_rejection_signal"

    # C
    app_c, out_c = evaluate_destination_confirmation_fact_check_v0(res=res, event=_stub_event("人民广场"))
    assert app_c is True
    assert isinstance(out_c, dict)
    assert out_c.get("confirmation_ready") is False
    assert out_c.get("reason") in ("no_confirmation_signal",)

    # D: ordinary input via mainline should not write destination_confirmation_fact_v0
    mgr = VoiceInputSessionManager()
    res_d = mgr.process_final_text_with_dispatch(
        "你好",
        now=time.time(),
        is_task_mode=False,
        session_id="dest_confirm_fact_d",
        source_type="simulated",
    )
    md_d: Dict[str, Any] = dict(getattr(res_d, "metadata", {}) or {})
    assert md_d.get("destination_confirmation_fact_v0") is None

    print("VERIFY_NAVIGATION_DESTINATION_CONFIRMATION_FACT_V0: ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


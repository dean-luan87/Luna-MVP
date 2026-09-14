#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify navigation_missing_destination_confirm_v0 response template (v0).

Scenarios:
- A: start_navigation with missing destination -> triggers fixed response template (response-only submit)
- B: ordinary input -> does not trigger
- C: predicate check: sufficient destination should not trigger (stub object)
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


def main() -> int:
    # Enable response-kind submit path.
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "1"

    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402
    from capabilities.voice.runtime.voice_navigation_response_template_v0 import (  # noqa: E402
        should_trigger_navigation_missing_destination_confirm_v0,
    )

    mgr = VoiceInputSessionManager()
    now = time.time()

    # A: start navigation, no destination binding fields -> should trigger response template
    res_a = mgr.process_final_text_with_dispatch(
        "开始导航",
        now=now,
        is_task_mode=True,
        session_id="nav_missing_dest_a",
        source_type="simulated",
    )
    md_a: Dict[str, Any] = dict(getattr(res_a, "metadata", {}) or {})
    assert should_trigger_navigation_missing_destination_confirm_v0(res_a) is True
    ev = md_a.get("destination_sufficiency_eval_v0")
    assert isinstance(ev, dict), f"dest_eval_missing:{ev!r}"
    assert ev.get("destination_sufficient") is False
    assert ev.get("reason") == "missing_destination"

    nh = md_a.get("navigation_handoff_v0") or {}
    assert isinstance(nh, dict) and nh.get("handoff_status") == "not_ready"

    rst = md_a.get("response_submit_template_v0")
    if not isinstance(rst, dict):
        print("DEBUG_MD_KEYS_A:", sorted(list(md_a.keys()))[:50])
        print("DEBUG_DEST_EVAL_A:", md_a.get("destination_sufficiency_eval_v0"))
        print("DEBUG_NAV_HANDOFF_A:", md_a.get("navigation_handoff_v0"))
        print("DEBUG_RESP_TEMPLATE_A:", md_a.get("response_submit_template_v0"))
    assert isinstance(rst, dict), f"response_submit_template_missing:{rst!r}"
    assert rst.get("template_id") == "navigation_missing_destination_confirm_v0"
    assert rst.get("submit_kind") == "response_only"

    # B: ordinary input -> should not trigger this template
    res_b = mgr.process_final_text_with_dispatch(
        "你好",
        now=now,
        is_task_mode=False,
        session_id="nav_missing_dest_b",
        source_type="simulated",
    )
    md_b: Dict[str, Any] = dict(getattr(res_b, "metadata", {}) or {})
    rst_b = md_b.get("response_submit_template_v0")
    if isinstance(rst_b, dict):
        assert (
            rst_b.get("template_id") != "navigation_missing_destination_confirm_v0"
        ), f"unexpected_template:{rst_b!r}"

    # C: predicate should be false when destination is sufficient (stub)
    bd = SimpleNamespace(route="task_lifecycle", proposal=SimpleNamespace(task_action="start_navigation"))
    res_c = SimpleNamespace(
        dispatch_type="short_controlled_input",
        bridge_decision=bd,
        metadata={
            "destination_sufficiency_eval_v0": {
                "destination_sufficient": True,
                "eval_scope": "navigation_destination_sufficiency_v0",
                "binding_key_seen": "destination_id",
            }
        },
    )
    assert should_trigger_navigation_missing_destination_confirm_v0(res_c) is False

    print("VERIFY_NAVIGATION_MISSING_DESTINATION_RESPONSE_V0: ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


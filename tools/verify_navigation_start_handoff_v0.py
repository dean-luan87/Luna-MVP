#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Start Navigation Handoff v0.

Asserts:
- "开始导航" in task mode yields TASK_LIFECYCLE + task_action=start_navigation
- result.metadata["navigation_handoff_v0"] exists with handoff_attempted=true
- handoff_status is explicit and non-empty
- non-navigation input does not write navigation_handoff_v0
- V1 minimal flow remains OK (run separately)
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Tuple

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _digest(res: Any) -> Tuple[str, str]:
    dt = str(getattr(res, "dispatch_type", "") or "")
    route = ""
    bd = getattr(res, "bridge_decision", None)
    if bd is not None:
        r = getattr(bd, "route", None)
        route = str(getattr(r, "value", "") or r or "")
    return dt, route


def main() -> int:
    # This verification is about handoff metadata, not speaking.
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "0"

    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402

    mgr = VoiceInputSessionManager()
    now = time.time()

    # A: start navigation
    res_a = mgr.process_final_text_with_dispatch(
        "开始导航",
        now=now,
        is_task_mode=True,
        session_id="nav_handoff_a",
        source_type="simulated",
    )
    assert _digest(res_a)[0] == "short_controlled_input"
    assert _digest(res_a)[1] == "task_lifecycle"
    bd = getattr(res_a, "bridge_decision", None)
    prop = getattr(bd, "proposal", None) if bd is not None else None
    assert getattr(prop, "task_action", None) == "start_navigation"

    md_a: Dict[str, Any] = dict(getattr(res_a, "metadata", {}) or {})
    nh = md_a.get("navigation_handoff_v0")
    assert isinstance(nh, dict), f"navigation_handoff_missing:{nh!r}"
    assert nh.get("handoff_attempted") is True
    assert nh.get("task_action") == "start_navigation"
    hs = str(nh.get("handoff_status") or "").strip()
    assert hs in ("started", "rejected", "not_ready", "not_implemented"), f"handoff_status_invalid:{nh!r}"

    # B: ordinary input should not write
    res_b = mgr.process_final_text_with_dispatch(
        "你好",
        now=now,
        is_task_mode=False,
        session_id="nav_handoff_b",
        source_type="simulated",
    )
    md_b: Dict[str, Any] = dict(getattr(res_b, "metadata", {}) or {})
    assert md_b.get("navigation_handoff_v0") is None, f"unexpected_nav_handoff:{md_b.get('navigation_handoff_v0')!r}"

    print("VERIFY_NAVIGATION_START_HANDOFF_V0: ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


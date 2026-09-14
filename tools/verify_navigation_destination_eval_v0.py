#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify destination_sufficiency_eval_v0 (read-only).

Scenarios:
- A: start_navigation via shortcut, no binding fields -> sufficient=false, reason=missing_destination; handoff remains not_ready
- B: ordinary input -> eval not written (or not_applicable); this implementation expects not written
- C: stub proposal with destination_id -> sufficient=true
- D: V1 minimal flow remains OK (run separately)
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def main() -> int:
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "0"

    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402
    from capabilities.voice.runtime.voice_navigation_destination_eval_v0 import (  # noqa: E402
        evaluate_destination_sufficiency_v0,
    )

    mgr = VoiceInputSessionManager()
    now = time.time()

    # A: start nav, no binding fields in proposal
    res_a = mgr.process_final_text_with_dispatch(
        "开始导航",
        now=now,
        is_task_mode=True,
        session_id="dest_eval_a",
        source_type="simulated",
    )
    md_a: Dict[str, Any] = dict(getattr(res_a, "metadata", {}) or {})
    ev = md_a.get("destination_sufficiency_eval_v0")
    assert isinstance(ev, dict), f"eval_missing:{ev!r}"
    assert ev.get("destination_sufficient") is False
    assert ev.get("reason") == "missing_destination"
    nh = md_a.get("navigation_handoff_v0") or {}
    assert isinstance(nh, dict) and nh.get("handoff_status") == "not_ready"

    # B: ordinary input should not write eval
    res_b = mgr.process_final_text_with_dispatch(
        "你好",
        now=now,
        is_task_mode=False,
        session_id="dest_eval_b",
        source_type="simulated",
    )
    md_b: Dict[str, Any] = dict(getattr(res_b, "metadata", {}) or {})
    assert md_b.get("destination_sufficiency_eval_v0") is None

    # C: stub proposal with explicit binding
    class _StubProposal:
        task_action = "start_navigation"
        destination_id = "dest_123"

    applicable, out = evaluate_destination_sufficiency_v0(_StubProposal())
    assert applicable is True
    assert isinstance(out, dict) and out.get("destination_sufficient") is True
    assert out.get("binding_key_seen") == "destination_id"

    print("VERIFY_NAVIGATION_DESTINATION_EVAL_V0: ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


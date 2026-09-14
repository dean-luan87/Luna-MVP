# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


def _assert_decision(md: Dict[str, Any], expected: str) -> None:
    r = md.get("need_navigation_routing_v0")
    assert isinstance(r, dict), f"missing_need_navigation_routing_v0:{type(r)}"
    assert r.get("routing_scope") == "need_navigation_routing_v0", f"bad_scope:{r}"
    assert r.get("routing_decision") == expected, f"bad_decision:{r}"


def main() -> None:
    from capabilities.mid_platform.runtime.need_navigation_routing_v0 import (
        evaluate_need_navigation_routing_v0,
    )
    from capabilities.voice.schemas.task_action_proposal import TaskActionProposal

    now = time.time()

    # 场景 A：显式导航任务（start_navigation）
    prop_a = TaskActionProposal(
        proposal_id="p_a",
        source_event_id="e_a",
        task_action="start_navigation",
        confidence=1.0,
        needs_confirmation=False,
    )
    r_a = evaluate_need_navigation_routing_v0(
        proposal=prop_a,
        route=None,
        raw_text="开始导航",
        runtime_context_metadata={},
    )
    _assert_decision({"need_navigation_routing_v0": r_a}, "navigation_required")

    # 场景 B：明显非导航型任务（任务生命周期控制）
    prop_b = TaskActionProposal(
        proposal_id="p_b",
        source_event_id="e_b",
        task_action="pause_task",
        confidence=1.0,
        needs_confirmation=True,
    )
    r_b = evaluate_need_navigation_routing_v0(
        proposal=prop_b,
        route=None,
        raw_text="暂停任务",
        runtime_context_metadata={},
    )
    _assert_decision({"need_navigation_routing_v0": r_b}, "navigation_not_required")

    # 场景 C：信息不足或边界不清
    r_c = evaluate_need_navigation_routing_v0(
        proposal=None,
        route=None,
        raw_text="你好",
        runtime_context_metadata={},
    )
    _assert_decision({"need_navigation_routing_v0": r_c}, "navigation_uncertain")

    print("VERIFY_NEED_NAVIGATION_ROUTING_V0: ALL_OK")


if __name__ == "__main__":
    main()


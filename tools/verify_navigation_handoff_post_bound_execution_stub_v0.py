# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


def _assert_payload(p: Dict[str, Any]) -> None:
    assert p.get("execution_stub_attempted") is True, f"attempted_not_true:{p}"
    assert p.get("execution_scope") == "navigation_handoff_post_bound_execution_stub_v0", f"bad_scope:{p}"
    assert p.get("execution_state") == "execution_pending", f"bad_state:{p}"
    assert p.get("reason") == "missing_formal_mid_platform_dispatch", f"bad_reason:{p}"


def main() -> None:
    from capabilities.voice.runtime.navigation_handoff_post_bound_execution_stub_v0 import (
        evaluate_navigation_handoff_post_bound_execution_stub_v0,
    )

    # 场景 A：存在 destination_bound_v0 + navigation_handoff_consume_bound_v0
    applicable_a, p_a = evaluate_navigation_handoff_post_bound_execution_stub_v0(
        destination_bound_v0={"destination_bound": True, "binding_key": "destination_id", "binding_value": "d1"},
        navigation_handoff_consume_bound_v0={"bound_consumed": True, "consume_scope": "x"},
    )
    assert applicable_a is True and isinstance(p_a, dict)
    _assert_payload(p_a)

    # 场景 B：缺少 destination_bound_v0
    applicable_b, p_b = evaluate_navigation_handoff_post_bound_execution_stub_v0(
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0={"bound_consumed": True},
    )
    assert applicable_b is False and p_b is None

    # 场景 C：缺少 navigation_handoff_consume_bound_v0
    applicable_c, p_c = evaluate_navigation_handoff_post_bound_execution_stub_v0(
        destination_bound_v0={"destination_bound": True},
        navigation_handoff_consume_bound_v0=None,
    )
    assert applicable_c is False and p_c is None

    print("VERIFY_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_V0: ALL_OK")


if __name__ == "__main__":
    main()


# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


def _assert_stub(md: Dict[str, Any], expected: str) -> None:
    stub = md.get("mid_platform_dispatch_consumption_stub_v0")
    assert isinstance(stub, dict), f"missing_stub:{type(stub)}"
    assert stub.get("consume_attempted") is True, f"consume_attempted_not_true:{stub}"
    assert stub.get("consume_scope") == "mid_platform_dispatch_consumption_stub_v0", f"bad_scope:{stub}"
    assert stub.get("consume_mode") == "read_only", f"bad_mode:{stub}"
    assert stub.get("routing_decision_seen") == expected, f"bad_routing_seen:{stub}"


def main() -> None:
    from capabilities.mid_platform.runtime.mid_platform_dispatch_consumption_stub_v0 import (
        consume_mid_platform_dispatch_consumption_stub_v0,
    )

    # 场景 A：navigation_required
    applicable_a, obs_a = consume_mid_platform_dispatch_consumption_stub_v0(
        need_navigation_routing_v0={
            "routing_decision": "navigation_required",
            "routing_scope": "need_navigation_routing_v0",
            "reason": "test",
        }
    )
    assert applicable_a is True and isinstance(obs_a, dict)
    _assert_stub({"mid_platform_dispatch_consumption_stub_v0": obs_a}, "navigation_required")

    # 场景 B：navigation_not_required
    applicable_b, obs_b = consume_mid_platform_dispatch_consumption_stub_v0(
        need_navigation_routing_v0={
            "routing_decision": "navigation_not_required",
            "routing_scope": "need_navigation_routing_v0",
            "reason": "test",
        }
    )
    assert applicable_b is True and isinstance(obs_b, dict)
    _assert_stub({"mid_platform_dispatch_consumption_stub_v0": obs_b}, "navigation_not_required")

    # 场景 C：无 need_navigation_routing_v0（relevant-only）
    applicable_c, obs_c = consume_mid_platform_dispatch_consumption_stub_v0(need_navigation_routing_v0=None)
    assert applicable_c is False and obs_c is None

    print("VERIFY_MID_PLATFORM_DISPATCH_CONSUMPTION_STUB_V0: ALL_OK")


if __name__ == "__main__":
    main()


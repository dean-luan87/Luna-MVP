#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sidewalk_env_summary_v1 最小构建器验证。"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.cross_domain.context.sidewalk_env_summary_v1 import (  # noqa: E402
    build_sidewalk_env_summary_v1,
    default_ttl_ms_v1,
)


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def main() -> None:
    now = 1_000_000.0
    ttl = 5000

    # 1) 新鲜 summary
    s1 = build_sidewalk_env_summary_v1(
        scene_candidate="outdoor_walkway",
        path_confidence=0.85,
        is_outdoor=True,
        event_timestamp=now - 0.5,
        now=now,
        ttl_ms=ttl,
    )
    _assert("fresh_freshness", s1["summary_freshness"] == "fresh")
    _assert("fresh_weight_positive", s1["confidence_weight"] > 0.4)
    _assert("has_core_keys", all(k in s1 for k in ("scene_candidate", "path_confidence", "is_outdoor", "ttl_ms", "event_timestamp")))

    # 2) 超过 TTL → stale
    s2 = build_sidewalk_env_summary_v1(
        scene_candidate="outdoor_walkway",
        path_confidence=0.9,
        is_outdoor=True,
        event_timestamp=now - 8.0,
        now=now,
        ttl_ms=ttl,
    )
    _assert("stale", s2["summary_freshness"] == "stale")
    _assert("stale_weight_zero", s2["confidence_weight"] == 0.0)
    _assert("stale_notes", "ttl_expired" in s2.get("inference_notes", []))

    # 3) 低置信 / 输入不足 → ambiguous
    s3 = build_sidewalk_env_summary_v1(
        scene_candidate="unknown",
        path_confidence=0.3,
        is_outdoor=False,
        event_timestamp=now - 0.2,
        now=now,
        ttl_ms=ttl,
    )
    _assert("ambiguous", s3["summary_freshness"] == "ambiguous")

    s3b = build_sidewalk_env_summary_v1(
        scene_candidate="unknown",
        path_confidence=0.5,
        is_outdoor=False,
        event_timestamp=now - 0.2,
        now=now,
        ttl_ms=ttl,
    )
    _assert("ambiguous_unknown_not_outdoor", s3b["summary_freshness"] == "ambiguous")

    # 4) 不因 risk 存在而污染：builder 不接收 risk；输出中不得出现 risk 键
    risk_side = {"risk_level": "high", "risk_type": "obstacle"}
    _assert("risk_unused", isinstance(risk_side, dict))
    s4 = build_sidewalk_env_summary_v1(
        scene_candidate="outdoor_walkway",
        path_confidence=0.8,
        is_outdoor=True,
        event_timestamp=now - 0.1,
        now=now,
        ttl_ms=ttl,
    )
    for k in ("risk_level", "risk_type", "risk_summary_v1"):
        _assert(f"no_risk_key_{k}", k not in s4, f"unexpected key {k}")

    # env TTL 默认值可读
    os.environ.pop("LUNA_SIDEWALK_ENV_SUMMARY_TTL_MS", None)
    _assert("default_ttl", default_ttl_ms_v1() == 5000)

    print("All sidewalk_env_summary_v1 builder checks passed.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""retail_env_summary_v1 最小构建器验证。"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.cross_domain.context.retail_env_summary_v1 import (  # noqa: E402
    build_retail_env_summary_v1,
    default_retail_ttl_ms_v1,
)


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def main() -> None:
    now = 2_000_000.0
    ttl = 8000

    # 1) 新鲜
    s1 = build_retail_env_summary_v1(
        scene_type_candidate="retail_shelf",
        retail_context_confidence=0.78,
        shelf_visible=True,
        gating_passed=None,
        event_timestamp=now - 0.5,
        now=now,
        ttl_ms=ttl,
    )
    _assert("fresh", s1["summary_freshness"] == "fresh")
    _assert("schema", str(s1.get("summary_schema_version") or "").startswith("retail_env_summary_v1/"))
    _assert("weight", s1["confidence_weight"] > 0.35)
    _assert("scene", s1["scene_type"] == "retail_shelf")

    forbidden = (
        "risk_level",
        "risk_summary_v1",
        "query",
        "active",
        "find_item_intent",
        "text_digest",
        "ocr_summary",
    )
    for k in forbidden:
        _assert(f"no_{k}", k not in s1, f"unexpected {k}")

    # 2) stale
    s2 = build_retail_env_summary_v1(
        scene_type="retail_aisle",
        retail_context_confidence=0.9,
        shelf_visible=True,
        event_timestamp=now - 20.0,
        now=now,
        ttl_ms=ttl,
    )
    _assert("stale", s2["summary_freshness"] == "stale")
    _assert("stale_w", s2["confidence_weight"] == 0.0)

    # 3) ambiguous — 低置信
    s3 = build_retail_env_summary_v1(
        scene_type_candidate="retail_shelf",
        retail_context_confidence=0.15,
        shelf_visible=True,
        event_timestamp=now - 0.2,
        now=now,
        ttl_ms=ttl,
    )
    _assert("ambig_low", s3["summary_freshness"] == "ambiguous")

    # 3b) ambiguous — 宣称 gating 但 scene 仍 unknown
    s3b = build_retail_env_summary_v1(
        scene_type="unknown",
        retail_context_confidence=0.5,
        shelf_visible=False,
        gating_passed=True,
        event_timestamp=now - 0.1,
        now=now,
        ttl_ms=ttl,
    )
    _assert("ambig_gating", s3b["summary_freshness"] == "ambiguous")

    # 默认 TTL
    os.environ.pop("LUNA_RETAIL_ENV_SUMMARY_TTL_MS", None)
    _assert("default_ttl", default_retail_ttl_ms_v1() == 8000)

    print("All retail_env_summary_v1 builder checks passed.")


if __name__ == "__main__":
    main()

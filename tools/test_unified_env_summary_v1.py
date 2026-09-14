#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""unified_env_summary_v1 最小构建器验证。"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.cross_domain.context.unified_env_summary_v1 import (  # noqa: E402
    build_unified_env_summary_v1,
    default_unified_ttl_ms_v1,
)


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def _no_risk_intent_ocr_keys(d: dict) -> None:
    """输出 dict 的键不得携带 risk / intent / OCR 语义（本 builder 不产出这些域）。"""
    for k in d.keys():
        lk = str(k).lower()
        _assert(f"key_not_risk_prefix_{k}", not lk.startswith("risk"), f"unexpected {k}")
        _assert(f"key_not_intent_{k}", "intent" not in lk, f"unexpected {k}")
        _assert(f"key_not_ocr_{k}", "ocr" not in lk, f"unexpected {k}")


def main() -> None:
    now = 2_000_000.0
    ttl = 6000

    # 1) walkway 输入 → walkway
    w1 = build_unified_env_summary_v1(
        raw_scene_candidate="outdoor_walkway",
        raw_environment_confidence=0.82,
        event_timestamp=now - 0.5,
        now=now,
        ttl_override_ms=ttl,
        source="test_v1",
    )
    _assert("walkway_family", w1["scene_family"] == "walkway")
    _assert("walkway_fresh", w1["summary_freshness"] == "fresh")
    _no_risk_intent_ocr_keys(w1)

    # 2) retail 输入 → retail
    r1 = build_unified_env_summary_v1(
        raw_scene_candidate="retail_shelf",
        raw_environment_confidence=0.75,
        event_timestamp=now - 0.4,
        now=now,
        ttl_override_ms=ttl,
    )
    _assert("retail_family", r1["scene_family"] == "retail")
    _assert("retail_schema", r1["summary_schema_version"] == "unified_env_summary_v1/1")
    _no_risk_intent_ocr_keys(r1)

    # 3) 无法识别 → unknown（无 hint）
    u1 = build_unified_env_summary_v1(
        raw_scene_candidate="hotel_lobby",
        raw_environment_confidence=0.6,
        event_timestamp=now - 0.3,
        now=now,
        ttl_override_ms=ttl,
    )
    _assert("unknown_family", u1["scene_family"] == "unknown")
    _no_risk_intent_ocr_keys(u1)

    # 3b) 跨域字符串护栏：retail-like candidate + walkway hint → 不允许硬落 retail
    g1 = build_unified_env_summary_v1(
        raw_scene_candidate="retail_shelf",
        raw_environment_confidence=0.8,
        raw_family_hint="walkway",
        event_timestamp=now - 0.3,
        now=now,
        ttl_override_ms=ttl,
    )
    _assert("guardrail_conflict_to_unknown", g1["scene_family"] == "unknown")

    # 4) 超 TTL → stale
    s_old = build_unified_env_summary_v1(
        raw_scene_candidate="outdoor_walkway",
        raw_environment_confidence=0.9,
        event_timestamp=now - 20.0,
        now=now,
        ttl_override_ms=ttl,
    )
    _assert("stale", s_old["summary_freshness"] == "stale")
    _assert("stale_weight", s_old["confidence_weight"] == 0.0)
    _assert("stale_notes", "ttl_expired" in s_old.get("inference_notes", []))
    _no_risk_intent_ocr_keys(s_old)

    # 5) 低置信 → ambiguous
    low = build_unified_env_summary_v1(
        raw_scene_candidate="outdoor_walkway",
        raw_environment_confidence=0.1,
        event_timestamp=now - 0.2,
        now=now,
        ttl_override_ms=ttl,
    )
    _assert("ambiguous_low_conf", low["summary_freshness"] == "ambiguous")
    _assert("amb_notes", "low_environment_confidence" in low.get("inference_notes", []))
    _no_risk_intent_ocr_keys(low)

    # unknown + 偏低置信 → ambiguous
    u2 = build_unified_env_summary_v1(
        raw_scene_candidate="unknown",
        raw_environment_confidence=0.35,
        event_timestamp=now - 0.2,
        now=now,
        ttl_override_ms=ttl,
    )
    _assert("ambiguous_unknown", u2["summary_freshness"] == "ambiguous")

    # 6) 输出键不含 risk / intent / OCR 语义
    sample = build_unified_env_summary_v1(
        raw_scene_candidate="retail_aisle",
        raw_environment_confidence=0.7,
        event_timestamp=now - 0.1,
        now=now,
        ttl_override_ms=ttl,
    )
    _no_risk_intent_ocr_keys(sample)

    os.environ.pop("LUNA_UNIFIED_ENV_SUMMARY_TTL_MS", None)
    _assert("default_ttl", default_unified_ttl_ms_v1() == 6000)

    print("All unified_env_summary_v1 builder checks passed.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""unified env shadow V1：开关、独立 key、不污染垂直 summary / risk / intent / OCR。"""

from __future__ import annotations

import copy
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.voice.runtime.voice_final_text_dispatcher import (  # noqa: E402
    _maybe_attach_unified_env_shadow_v1,
)
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent  # noqa: E402
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext  # noqa: E402


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def main() -> None:
    now = time.time()
    ev = VoiceInputEvent(
        request_id="r_shadow",
        session_id="s_shadow",
        timestamp=now,
        raw_text="t",
        normalized_text="t",
        is_task_mode=True,
    )

    base_md = {
        "sidewalk_env_summary_v1": {
            "scene_candidate": "outdoor_walkway",
            "path_confidence": 0.8,
            "is_outdoor": True,
            "summary_schema_version": "sidewalk_env_summary_v1/1",
            "summary_freshness": "fresh",
        },
        "retail_env_summary_v1": {
            "scene_type": "retail_shelf",
            "scene_type_candidate": "retail_shelf",
            "retail_context_confidence": 0.7,
            "shelf_visible": True,
            "summary_schema_version": "retail_env_summary_v1/1",
        },
        "risk_summary_v1": {"risk_level": "low", "risk_type": "none"},
        "find_item_intent_summary_v1": {"intent": "find_sku"},
        "ocr_summary_v1": {"text": "dummy"},
    }
    ctx = VoiceRuntimeContext(metadata=copy.deepcopy(base_md))

    # 1) 默认关闭（未设或 0）→ 不写 shadow key
    os.environ.pop("LUNA_ENABLE_UNIFIED_ENV_SHADOW_V1", None)
    out_off = _maybe_attach_unified_env_shadow_v1(ev, ctx)
    _assert("off_no_key", "unified_env_summary_shadow_v1" not in (out_off.metadata or {}))

    os.environ["LUNA_ENABLE_UNIFIED_ENV_SHADOW_V1"] = "0"
    out_off2 = _maybe_attach_unified_env_shadow_v1(ev, ctx)
    _assert("zero_no_key", "unified_env_summary_shadow_v1" not in (out_off2.metadata or {}))

    # 2) 开启后生成 shadow
    os.environ["LUNA_ENABLE_UNIFIED_ENV_SHADOW_V1"] = "1"
    out_on = _maybe_attach_unified_env_shadow_v1(ev, ctx)
    sh = (out_on.metadata or {}).get("unified_env_summary_shadow_v1")
    _assert("shadow_present", isinstance(sh, dict) and bool(sh))
    _assert(
        "shadow_schema",
        str(sh.get("summary_schema_version") or "").startswith("unified_env_summary_v1/"),
    )

    # 3) 不改写 sidewalk / retail（对象或内容一致）
    _assert(
        "sidewalk_preserved",
        (out_on.metadata or {}).get("sidewalk_env_summary_v1") == base_md["sidewalk_env_summary_v1"],
    )
    _assert(
        "retail_preserved",
        (out_on.metadata or {}).get("retail_env_summary_v1") == base_md["retail_env_summary_v1"],
    )

    # 4) risk / intent / OCR 不变
    _assert("risk_ok", (out_on.metadata or {}).get("risk_summary_v1") == base_md["risk_summary_v1"])
    _assert(
        "intent_ok",
        (out_on.metadata or {}).get("find_item_intent_summary_v1") == base_md["find_item_intent_summary_v1"],
    )
    _assert("ocr_ok", (out_on.metadata or {}).get("ocr_summary_v1") == base_md["ocr_summary_v1"])

    # 5) retail_like 优先时 shadow 应对齐 retail 场景（与派生优先级一致）
    _assert("retail_family", sh.get("scene_family") == "retail")
    _assert("retail_candidate", "retail" in str(sh.get("scene_candidate") or "").lower())

    os.environ.pop("LUNA_ENABLE_UNIFIED_ENV_SHADOW_V1", None)
    print("All unified_env_shadow_v1 checks passed.")


if __name__ == "__main__":
    main()

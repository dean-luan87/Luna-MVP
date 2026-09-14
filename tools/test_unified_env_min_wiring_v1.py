#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""unified env 最小接线实验 V1：只读补缺 + 独立留痕，不覆盖，不决策。"""

from __future__ import annotations

import copy
import os
import sys
import time
from pathlib import Path

# tools 可能是外链；import 需要外链 root + cwd
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path.cwd()))

from capabilities.voice.runtime.voice_final_text_dispatcher import (  # noqa: E402
    _maybe_attach_unified_env_fill_shadow_v1,
    _maybe_attach_unified_env_shadow_v1,
    _maybe_stabilize_runtime_context_retail_env_v1,
    _maybe_stabilize_runtime_context_sidewalk_env_v1,
)
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent  # noqa: E402
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext  # noqa: E402


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def main() -> None:
    now = time.time()
    ev = VoiceInputEvent(
        request_id="rid_min_wiring",
        session_id="sid_min_wiring",
        timestamp=now,
        raw_text="t",
        normalized_text="t",
        is_task_mode=True,
    )

    base_md = {
        # 垂直摘要（原始 dict，将被 stabilizer 转为带 freshness 等字段）
        "sidewalk_env_summary_v1": {"scene_candidate": "outdoor_walkway", "path_confidence": 0.82, "is_outdoor": True},
        "retail_env_summary_v1": {"scene_type_candidate": "retail_shelf", "retail_context_confidence": 0.76, "shelf_visible": True},
        "risk_summary_v1": {"risk_level": "low", "risk_type": "none"},
        "find_item_intent_summary_v1": {"intent": "find_item"},
        "ocr_summary_v1": {"text": "dummy"},
    }
    ctx0 = VoiceRuntimeContext(metadata=copy.deepcopy(base_md))

    # 先稳定化 + shadow（与主线路径一致）
    os.environ["LUNA_ENABLE_SIDEWALK_ENV_SUMMARY_STABILIZER_V1"] = "1"
    os.environ["LUNA_ENABLE_RETAIL_ENV_SUMMARY_STABILIZER_V1"] = "1"
    os.environ["LUNA_ENABLE_UNIFIED_ENV_SHADOW_V1"] = "1"

    st = _maybe_stabilize_runtime_context_sidewalk_env_v1(ev, ctx0)
    st = _maybe_stabilize_runtime_context_retail_env_v1(ev, st)
    st = _maybe_attach_unified_env_shadow_v1(ev, st)
    st_md_before = copy.deepcopy(st.metadata)

    # 1) 开关关闭：不写 fill shadow
    os.environ.pop("LUNA_ENABLE_UNIFIED_ENV_MIN_WIRING_V1", None)
    off = _maybe_attach_unified_env_fill_shadow_v1(event=ev, runtime_context=st)
    _assert("off_no_fill", "unified_env_fill_shadow_v1" not in (off.metadata or {}))

    # 2) 开启：但目标字段已存在（stabilizer 已写 freshness/ttl/...），应阻断，不补
    os.environ["LUNA_ENABLE_UNIFIED_ENV_MIN_WIRING_V1"] = "1"
    on = _maybe_attach_unified_env_fill_shadow_v1(event=ev, runtime_context=st)
    fill = (on.metadata or {}).get("unified_env_fill_shadow_v1") or {}
    _assert("fill_present", isinstance(fill, dict) and bool(fill))
    _assert("fill_applied_false", fill.get("fill_applied") is False)
    _assert("blocked_has_target_value", any(str(x).startswith("target_has_value:") for x in (fill.get("fill_blocked_reason") or [])))

    # 3) family/candidate 不一致时必须阻断：
    #    为避免依赖“自然产生错配”的偶然性，这里手动篡改 unified shadow 以模拟不一致输入。
    bad_ctx = VoiceRuntimeContext(
        metadata={
            "sidewalk_env_summary_v1": {"scene_candidate": "outdoor_walkway", "path_confidence": 0.9, "is_outdoor": True},
        }
    )
    bad = _maybe_stabilize_runtime_context_sidewalk_env_v1(ev, bad_ctx)
    bad = _maybe_attach_unified_env_shadow_v1(ev, bad)
    md_bad = dict(bad.metadata)
    uni_bad = dict(md_bad.get("unified_env_summary_shadow_v1") or {})
    uni_bad["scene_candidate"] = "retail_shelf"  # 强制 candidate 不一致
    uni_bad["scene_family"] = "retail"
    md_bad["unified_env_summary_shadow_v1"] = uni_bad
    bad = VoiceRuntimeContext(metadata=md_bad)
    bad2 = _maybe_attach_unified_env_fill_shadow_v1(event=ev, runtime_context=bad)
    f2 = (bad2.metadata or {}).get("unified_env_fill_shadow_v1") or {}
    _assert("mismatch_blocked", "family_candidate_mismatch" in (f2.get("fill_blocked_reason") or []))
    _assert("mismatch_no_apply", f2.get("fill_applied") is False)

    # 4) 不改写垂直 summary / risk / intent / OCR（只新增独立键）
    _assert("no_mutate_vertical", (st.metadata or {}).get("sidewalk_env_summary_v1") == st_md_before.get("sidewalk_env_summary_v1"))
    _assert("no_mutate_risk", (st.metadata or {}).get("risk_summary_v1") == st_md_before.get("risk_summary_v1"))
    _assert("no_mutate_intent", (st.metadata or {}).get("find_item_intent_summary_v1") == st_md_before.get("find_item_intent_summary_v1"))
    _assert("no_mutate_ocr", (st.metadata or {}).get("ocr_summary_v1") == st_md_before.get("ocr_summary_v1"))

    print("All unified_env_min_wiring_v1 checks passed.")


if __name__ == "__main__":
    main()


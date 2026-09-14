# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


def _slice_risk_min() -> Dict[str, Any]:
    return {
        "slice_id": "slice_risk_001",
        "slice_type": "risk_slice",
        "source_modules": ["vision.front_perception_v0"],
        "task_relevance": "unknown",
        "stability": "unstable",
        "confidence": 0.6,
        "needs_rerecognition": False,
        "needs_confirmation": False,
        "network_allowed": False,
        "memory_worthy": False,
        "consume_priority": "normal",
        "lane": "fast",
        "can_enter_mainline": False,
        "payload": {"risk_level_candidate": "unknown"},
    }


def _slice_ocr_min() -> Dict[str, Any]:
    return {
        "slice_id": "slice_ocr_001",
        "slice_type": "ocr_related_slice",
        "source_modules": ["vision.front_perception_v0"],
        "task_relevance": "unknown",
        "stability": "unstable",
        "confidence": 0.55,
        "needs_rerecognition": False,
        "needs_confirmation": False,
        "network_allowed": False,
        "memory_worthy": False,
        "consume_priority": "low",
        "lane": "fast",
        "can_enter_mainline": False,
        "payload": {"text_candidate": "TEST"},
    }


def _assert_mid_platform_obs(
    md: Dict[str, Any],
    *,
    expected_count: int,
    expected_types: List[str],
) -> None:
    obs = md.get("vision_mid_platform_consume_stub_v0")
    assert isinstance(obs, dict), f"missing_mid_platform_obs:{type(obs)}"
    assert obs.get("consume_attempted") is True, f"consume_attempted_not_true:{obs}"
    assert obs.get("consume_scope") == "vision_mid_platform_consume_stub_v0", f"bad_scope:{obs}"
    assert obs.get("consume_mode") == "read_only", f"bad_mode:{obs}"
    assert obs.get("slice_count") == expected_count, f"bad_count:{obs}"
    st = obs.get("slice_types")
    assert isinstance(st, list), f"slice_types_not_list:{obs}"
    for t in expected_types:
        assert t in st, f"missing_slice_type:{t}; got={st}"


def main() -> None:
    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager
    from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext

    mgr = VoiceInputSessionManager()
    now = time.time()

    # 场景 A：输入一个最小有效 risk_slice
    ctx_a = VoiceRuntimeContext(metadata={"vision_consumable_slices_v0": _slice_risk_min()})
    out_a = mgr.process_final_text_with_dispatch(
        "你好",
        now=now,
        is_task_mode=False,
        session_id="s_a",
        runtime_context=ctx_a,
    )
    md_a = out_a.metadata or {}
    _assert_mid_platform_obs(md_a, expected_count=1, expected_types=["risk_slice"])

    # 场景 B：输入一个包含多个类型的 slice 集合
    ctx_b = VoiceRuntimeContext(metadata={"vision_consumable_slices_v0": [_slice_risk_min(), _slice_ocr_min()]})
    out_b = mgr.process_final_text_with_dispatch(
        "你好",
        now=now + 1.0,
        is_task_mode=False,
        session_id="s_b",
        runtime_context=ctx_b,
    )
    md_b = out_b.metadata or {}
    _assert_mid_platform_obs(md_b, expected_count=2, expected_types=["risk_slice", "ocr_related_slice"])

    # 场景 C：普通主链输入，无视角 slice
    ctx_c = VoiceRuntimeContext(metadata={})
    out_c = mgr.process_final_text_with_dispatch(
        "你好",
        now=now + 2.0,
        is_task_mode=False,
        session_id="s_c",
        runtime_context=ctx_c,
    )
    md_c = out_c.metadata or {}
    assert "vision_mid_platform_consume_stub_v0" not in md_c, "should_not_write_when_no_slices"

    print("VERIFY_VISION_MID_PLATFORM_CONSUME_STUB_V0: ALL_OK")


if __name__ == "__main__":
    main()


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


def _risk_summary_v1_min() -> Dict[str, Any]:
    return {
        "risk_level": "warning",
        "risk_type": "obstacle_candidate",
        "risk_reason": "test_stub_risk_summary_v1",
        "confidence": 0.7,
        "source": "vision_stub_input",
        "is_gate_ready": True,
    }


def main() -> None:
    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager
    from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext

    mgr = VoiceInputSessionManager()
    now = time.time()

    # 场景 A：存在可转换的视角摘要输入（risk_summary_v1）
    ctx_a = VoiceRuntimeContext(metadata={"risk_summary_v1": _risk_summary_v1_min()})
    out_a = mgr.process_final_text_with_dispatch(
        "你好",
        now=now,
        is_task_mode=False,
        session_id="s_a",
        runtime_context=ctx_a,
    )
    md_a = out_a.metadata or {}
    obs_a = md_a.get("vision_mid_platform_consume_stub_v0")
    assert isinstance(obs_a, dict), f"missing_consume_obs_a:{type(obs_a)}"
    assert obs_a.get("consume_attempted") is True, f"consume_attempted_not_true:{obs_a}"
    assert obs_a.get("slice_count") == 1, f"slice_count_not_1:{obs_a}"
    st = obs_a.get("slice_types")
    assert isinstance(st, list) and "risk_slice" in st, f"missing_risk_slice:{obs_a}"

    # 场景 B：无有效视角摘要输入
    ctx_b = VoiceRuntimeContext(metadata={})
    out_b = mgr.process_final_text_with_dispatch(
        "你好",
        now=now + 1.0,
        is_task_mode=False,
        session_id="s_b",
        runtime_context=ctx_b,
    )
    md_b = out_b.metadata or {}
    assert "vision_mid_platform_consume_stub_v0" not in md_b, "should_not_write_when_no_valid_summary"

    print("VERIFY_VISION_MAINLINE_MINIMAL_WIRING_V0: ALL_OK")


if __name__ == "__main__":
    main()


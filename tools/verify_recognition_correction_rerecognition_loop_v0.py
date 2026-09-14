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


def _risk_summary_v1_triggering() -> Dict[str, Any]:
    # Must lead to a risk_slice with confidence < 0.75 and risk_level warning/high.
    return {
        "risk_level": "warning",
        "risk_type": "obstacle_candidate",
        "risk_reason": "test_stub_trigger_rerec",
        "confidence": 0.6,
        "source": "vision_stub_input",
        "is_gate_ready": True,
    }


def main() -> None:
    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager
    from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext

    mgr = VoiceInputSessionManager()
    now = time.time()

    # 场景 A：存在可触发的上游输入（risk_summary_v1 -> risk_slice -> needs_rerecognition_candidate）
    ctx_a = VoiceRuntimeContext(metadata={"risk_summary_v1": _risk_summary_v1_triggering()})
    out_a = mgr.process_final_text_with_dispatch(
        "你好",
        now=now,
        is_task_mode=False,
        session_id="s_a",
        runtime_context=ctx_a,
    )
    md_a = out_a.metadata or {}
    obs_a = md_a.get("vision_mid_platform_consume_stub_v0")
    assert isinstance(obs_a, dict), f"missing_mid_platform_obs:{type(obs_a)}"
    assert obs_a.get("consume_attempted") is True, f"consume_attempted_not_true:{obs_a}"
    assert obs_a.get("consume_mode") == "read_only", f"bad_mode:{obs_a}"
    assert obs_a.get("candidate_count") == 1, f"candidate_count_not_1:{obs_a}"
    cts = obs_a.get("candidate_types")
    assert isinstance(cts, list) and "needs_rerecognition_candidate" in cts, f"bad_candidate_types:{obs_a}"

    # 场景 B：无有效上游输入
    ctx_b = VoiceRuntimeContext(metadata={})
    out_b = mgr.process_final_text_with_dispatch(
        "你好",
        now=now + 1.0,
        is_task_mode=False,
        session_id="s_b",
        runtime_context=ctx_b,
    )
    md_b = out_b.metadata or {}
    assert "vision_mid_platform_consume_stub_v0" not in md_b, "should_not_write_when_no_inputs"

    print("VERIFY_RECOGNITION_CORRECTION_RERECOGNITION_LOOP_V0: ALL_OK")


if __name__ == "__main__":
    main()


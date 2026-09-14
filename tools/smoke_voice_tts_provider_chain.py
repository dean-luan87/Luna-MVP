#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smoke: Voice Stage-2 TTS provider chain (Fish primary, Piper fallback).

注意：本脚本不接入主链，不播放音频，仅验证：
- 配置可加载
- preset 可加载
- selector/fallback 可返回结构化结果（即便本机没有 piper 二进制）
"""

from __future__ import annotations

import sys
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities.voice.output.tts_request_executor import execute_tts_request
from capabilities.voice.schemas.speech_request import SpeechRequest


def main() -> None:
    req = SpeechRequest(
        request_id=f"smoke_{int(time.time())}",
        source_module="smoke",
        output_category="device_status",
        text_candidate="测试语音输出链：如果 Fish 不可用，将回退到 Piper。",
        priority=1,
        interruptible=True,
        dedup_allowed=True,
        cooldown_key="smoke_voice_tts",
        metadata={"preset": "calm_female_v1"},
    )
    outcome = execute_tts_request(request=req)
    chain = outcome.chain
    print("ok:", outcome.ok)
    print("chosen_provider:", chain.selection_observation.chosen_provider)
    if chain.final_result is None:
        print("final_result: None")
        return
    r = chain.final_result
    print("final_provider:", r.provider_name, "provider_ok:", r.ok, "latency_ms:", r.latency_ms)
    if r.failure:
        print("failure:", r.failure.failure_type, r.failure.reason)
    if chain.fallback_observation:
        fb = chain.fallback_observation
        print("fallback:", fb.primary_provider, "->", fb.final_provider_used, "reason:", fb.fallback_reason, "type:", fb.failure_type)


if __name__ == "__main__":
    main()


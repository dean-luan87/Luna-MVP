#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-shot trigger for unified env shadow snapshot.

- Does NOT set env vars (caller should export).
- Calls VoiceInputSessionManager.process_final_text_with_dispatch twice:
  - sidewalk-like context
  - retail-like context
"""

from __future__ import annotations

import sys
import time
from pathlib import Path


def _bootstrap_pythonpath() -> None:
    # Ensure repo root is on sys.path when executed from anywhere.
    root = Path(__file__).resolve().parent.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


def _ctx_sidewalk(now: float):
    from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext

    return VoiceRuntimeContext(
        metadata={
            "sidewalk_env_summary_v1": {
                "scene_candidate": "outdoor_walkway",
                "path_confidence": 0.82,
                "is_outdoor": True,
                "summary_freshness": "fresh",
                "event_timestamp": now,
                "ttl_ms": 5000,
                "confidence_weight": 0.82,
                "summary_schema_version": "sidewalk_env_summary_v1/1",
                "source": "sidewalk_env_summary_builder_v1",
                "age_ms": 0.0,
                "inference_notes": [],
            }
        }
    )


def _ctx_retail(now: float):
    from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext

    return VoiceRuntimeContext(
        metadata={
            "retail_env_summary_v1": {
                "scene_type": "retail_shelf",
                "scene_type_candidate": "retail_shelf",
                "retail_context_confidence": 0.76,
                "shelf_visible": True,
                "gating_passed": True,
                "summary_freshness": "fresh",
                "event_timestamp": now,
                "ttl_ms": 8000,
                "confidence_weight": 0.76,
                "summary_schema_version": "retail_env_summary_v1/1",
                "source": "retail_env_summary_builder_v1",
                "age_ms": 0.0,
                "inference_notes": [],
            }
        }
    )


def main() -> None:
    _bootstrap_pythonpath()
    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager

    mgr = VoiceInputSessionManager()
    now = time.time()

    r1 = mgr.process_final_text_with_dispatch(
        "向前走",
        now=now,
        is_task_mode=True,
        session_id="sid_unified_env_round02_sw",
        runtime_context=_ctx_sidewalk(now),
    )

    r2 = mgr.process_final_text_with_dispatch(
        "我在货架前",
        now=now + 0.01,
        is_task_mode=True,
        session_id="sid_unified_env_round02_rt",
        runtime_context=_ctx_retail(now + 0.01),
    )

    print("done")
    print("r1 dispatch_type:", getattr(r1, "dispatch_type", ""))
    print("r2 dispatch_type:", getattr(r2, "dispatch_type", ""))


if __name__ == "__main__":
    main()


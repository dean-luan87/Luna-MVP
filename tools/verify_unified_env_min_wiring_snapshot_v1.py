#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小验证：开启 LUNA_ENABLE_UNIFIED_ENV_MIN_WIRING_SNAPSHOT_V1 后，
_maybe_emit_unified_env_min_wiring_snapshot_v1 能写出 JSONL，且 metadata 含 unified_env_fill_shadow_v1。
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    os.chdir(repo)
    rp = str(repo)
    if rp not in sys.path:
        sys.path.insert(0, rp)

    fd, tmppath = tempfile.mkstemp(suffix=".jsonl")
    os.close(fd)
    p = Path(tmppath)
    try:
        os.environ["LUNA_ENABLE_UNIFIED_ENV_MIN_WIRING_SNAPSHOT_V1"] = "1"
        os.environ["LUNA_UNIFIED_ENV_MIN_WIRING_SNAPSHOT_V1_JSONL"] = str(p)

        from capabilities.voice.runtime.voice_final_text_dispatcher import (
            _maybe_emit_unified_env_min_wiring_snapshot_v1,
        )
        from capabilities.voice.schemas.voice_input_event import VoiceInputEvent
        from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext

        md = {
            "sidewalk_env_summary_v1": {"summary_schema_version": "sidewalk_env_summary_v1/0.1", "x": 1},
            "unified_env_summary_shadow_v1": {"scene_family": "walkway", "scene_candidate": "outdoor"},
            "unified_env_fill_shadow_v1": {
                "fill_applied": False,
                "filled_fields": [],
                "fill_blocked_reason": ["missing_unified_shadow"],
            },
        }
        ev = VoiceInputEvent(request_id="req-verify-min-wiring", event_id="e1", timestamp=1700000000.0)
        ctx = VoiceRuntimeContext(metadata=md)
        _maybe_emit_unified_env_min_wiring_snapshot_v1(event=ev, runtime_context=ctx)

        line = p.read_text(encoding="utf-8").strip()
        if not line:
            print("FAIL: empty jsonl")
            return 1
        obj = json.loads(line)
        if obj.get("type") != "unified_env_min_wiring_snapshot":
            print("FAIL: wrong type", obj)
            return 1
        fill = (obj.get("data") or {}).get("metadata", {}).get("unified_env_fill_shadow_v1")
        if not isinstance(fill, dict) or "fill_applied" not in fill:
            print("FAIL: missing unified_env_fill_shadow_v1 in metadata", obj)
            return 1
        print("OK: wrote line with unified_env_fill_shadow_v1")
        return 0
    finally:
        try:
            p.unlink(missing_ok=True)
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())

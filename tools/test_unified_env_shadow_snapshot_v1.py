#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""unified env shadow snapshot V1：开关、最小字段、白名单 metadata、失败吞掉。"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

# 注意：tools/ 在本工作区可能是指向外部仓库的符号链接。
# - import 需要把外部仓库 root 加入 sys.path（包含 shared 等依赖）
# - 输出落盘必须使用当前工作区 cwd（可写）
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path.cwd()))

from capabilities.voice.runtime.voice_final_text_dispatcher import (  # noqa: E402
    _maybe_emit_unified_env_shadow_snapshot_v1,
)
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent  # noqa: E402
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext  # noqa: E402


def _assert(name: str, cond: bool, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"[{name}] {msg}")


def main() -> None:
    out_dir = Path.cwd() / "analyze_unified_env_shadow_out"
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / "unified_env_shadow_snapshot_v1_test.jsonl"
    if p.exists():
        p.unlink()

    now = time.time()
    ev = VoiceInputEvent(
        request_id="rid_snap",
        session_id="sid_snap",
        timestamp=now,
        raw_text="t",
        normalized_text="t",
        is_task_mode=True,
    )
    ctx = VoiceRuntimeContext(
        metadata={
            "sidewalk_env_summary_v1": {
                "scene_candidate": "outdoor_walkway",
                "path_confidence": 0.8,
                "is_outdoor": True,
                "summary_schema_version": "sidewalk_env_summary_v1/1",
                "summary_freshness": "fresh",
                "event_timestamp": now,
            },
            "retail_env_summary_v1": {
                "scene_type_candidate": "retail_shelf",
                "retail_context_confidence": 0.7,
                "shelf_visible": True,
                "summary_schema_version": "retail_env_summary_v1/1",
                "summary_freshness": "fresh",
                "event_timestamp": now,
            },
            "risk_summary_v1": {"risk_level": "low", "risk_type": "none"},
        }
    )
    md_before = dict(ctx.metadata)

    # 1) 默认关闭：不写
    os.environ.pop("LUNA_ENABLE_UNIFIED_ENV_SHADOW_SNAPSHOT_V1", None)
    os.environ["LUNA_UNIFIED_ENV_SHADOW_SNAPSHOT_V1_JSONL"] = str(p)
    _maybe_emit_unified_env_shadow_snapshot_v1(event=ev, runtime_context=ctx)
    _assert("off_no_file", not p.exists())

    # 2) 开启：写一条
    os.environ["LUNA_ENABLE_UNIFIED_ENV_SHADOW_SNAPSHOT_V1"] = "1"
    _maybe_emit_unified_env_shadow_snapshot_v1(event=ev, runtime_context=ctx)
    _assert("on_file_exists", p.exists())
    lines = p.read_text(encoding="utf-8").splitlines()
    _assert("one_line", len(lines) >= 1)
    obj = json.loads(lines[-1])
    _assert("type", obj.get("type") == "unified_env_shadow_snapshot")
    data = obj.get("data") or {}
    _assert("has_timestamp", isinstance(data.get("timestamp"), (int, float)))
    _assert("has_event_timestamp", isinstance(data.get("event_timestamp"), (int, float)))
    _assert("has_related_request_id", data.get("related_request_id") == "rid_snap")
    _assert("has_source", bool(data.get("source")))
    md = data.get("metadata") or {}
    _assert("md_is_dict", isinstance(md, dict))
    _assert("has_sidewalk", "sidewalk_env_summary_v1" in md)
    _assert("has_retail", "retail_env_summary_v1" in md)
    _assert("has_unified_shadow", "unified_env_summary_shadow_v1" in md)
    _assert(
        "unified_schema",
        str((md.get("unified_env_summary_shadow_v1") or {}).get("summary_schema_version") or "").startswith(
            "unified_env_summary_v1/"
        ),
    )
    _assert("no_risk_key_in_snapshot_md", "risk_summary_v1" not in md)

    # 3) 不污染 runtime_context
    _assert("ctx_not_modified", ctx.metadata == md_before)

    # 4) 写入失败吞掉：把路径设成目录
    bad_dir = out_dir / "snap_dir"
    bad_dir.mkdir(parents=True, exist_ok=True)
    os.environ["LUNA_UNIFIED_ENV_SHADOW_SNAPSHOT_V1_JSONL"] = str(bad_dir)
    _maybe_emit_unified_env_shadow_snapshot_v1(event=ev, runtime_context=ctx)

    # cleanup
    os.environ.pop("LUNA_ENABLE_UNIFIED_ENV_SHADOW_SNAPSHOT_V1", None)
    os.environ.pop("LUNA_UNIFIED_ENV_SHADOW_SNAPSHOT_V1_JSONL", None)
    print("All unified_env_shadow_snapshot_v1 checks passed.")


if __name__ == "__main__":
    main()


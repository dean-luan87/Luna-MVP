#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Piper 工程包验证（基于正式配置）。"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.voice.runtime.tts_unified_entry import run_tts_unified_entry
from capabilities.voice.schemas.speech_request import SpeechRequest
from modules.voice import Voice


OUT_DIR = ROOT / "logs" / "piper_engineering_pack"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_JSON = ROOT / "logs" / "piper_engineering_pack.json"


def _legacy_submit(text: str) -> bool:
    return Voice().speak(text)


def _mk_request(scene: str, text: str, preset: str) -> SpeechRequest:
    return SpeechRequest(
        request_id=f"piper_eng_{scene}_{int(time.time() * 1000)}",
        source_module="run_piper_engineering_pack",
        output_category="interaction_result",
        text_candidate=text,
        priority=1,
        interruptible=True,
        dedup_allowed=True,
        cooldown_key=f"piper_eng_{scene}",
        metadata={"preset": preset, "scene": scene},
    )


def main() -> None:
    cases: List[Tuple[str, str, str]] = [
        ("navigation", "前方十米右转。", "navigation_clear_v1"),
        ("navigation", "请沿当前方向继续前进。", "navigation_clear_v1"),
        ("warning", "前方靠近水边，请停一下。", "warning_strong_v1"),
        ("warning", "前面人多，请减速靠右。", "warning_strong_v1"),
        ("feedback", "已开始导航。", "calm_female_v1"),
        ("feedback", "我没听清，请再说一次。", "gentle_companion_v1"),
        ("feedback", "已暂停当前任务。", "calm_female_v1"),
    ]
    rows: List[Dict[str, Any]] = []
    for scene, text, preset in cases:
        req = _mk_request(scene, text, preset)
        res = run_tts_unified_entry(request=req, legacy_submit=_legacy_submit)
        row: Dict[str, Any] = {
            "request_id": req.request_id,
            "scene": scene,
            "text": text,
            "preset": preset,
            "ok": res.ok,
            "final_execution_mode": res.final_execution_mode,
            "provider_name": res.provider_result.provider_name if res.provider_result else None,
            "provider_latency_ms": res.provider_result.latency_ms if res.provider_result else None,
            "selection": (res.selection_observation.__dict__ if res.selection_observation else None),
            "fallback": (res.fallback_observation.__dict__ if res.fallback_observation else None),
            "cutover": res.cutover_observation.__dict__,
            "rollback": (res.rollback_observation.__dict__ if res.rollback_observation else None),
        }
        if res.provider_result and res.provider_result.ok and res.provider_result.audio_bytes:
            wav = OUT_DIR / f"{req.request_id}_{preset}.wav"
            wav.write_bytes(res.provider_result.audio_bytes)
            row["audio_path"] = str(wav)
            row["audio_bytes"] = len(res.provider_result.audio_bytes)
        rows.append(row)

    out = {
        "generated_at": int(time.time()),
        "total": len(rows),
        "success": sum(1 for r in rows if r["ok"]),
        "provider_chain": sum(1 for r in rows if r["final_execution_mode"] == "provider_chain"),
        "legacy_fallback": sum(1 for r in rows if r["final_execution_mode"] == "legacy_fallback"),
        "rows": rows,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"saved: {OUT_JSON}")


if __name__ == "__main__":
    main()


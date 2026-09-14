#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3.5 显式开关灰度抽测（本地 smoke / 跑批脚本）

目标：
- 默认不改主链；仅在本脚本进程内设置 LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1 时走 prefilter 路由
- 统计 json/val/fallback（以 model_chain_* notes + validator wrap 为口径）
- 统计 mixed_preserve_rate（按 case mixed_keywords 与 non_task_payload 片段匹配）
- 统计 avg/p95 ms（e2e 以 dispatch 计时）
- 输出 route_to_* 路由分布

注意：本脚本不修改 schema / validator / builder / fallback 定义。
"""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
import sys

sys.path.insert(0, str(ROOT))


def _p95(xs: List[float]) -> float:
    if not xs:
        return 0.0
    s = sorted(xs)
    return float(s[int((len(s) - 1) * 0.95)])


def _non_task_blob(res: Any) -> str:
    p = getattr(res, "non_task_payload", None)
    if not p or not getattr(p, "exists", False):
        return ""
    segs = getattr(p, "segments", None) or []
    return " ".join((getattr(s, "content", "") or "") for s in segs)


@dataclass
class Row:
    case_id: str
    routing_suggestion: str
    selected_provider_model_id: str
    used_model_chain: bool
    validator_ok: Optional[bool]
    fallback: bool
    mixed_preserved: Optional[bool]
    e2e_ms: float


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--cases-json",
        type=Path,
        default=ROOT / "configs" / "voice" / "voice_prefilter_routing_real_cases_m3_5.json",
    )
    ap.add_argument("--rounds", type=int, default=20, help="抽测轮数（每轮跑一遍 cases）")
    ap.add_argument(
        "--enable-prefilter-routing",
        action="store_true",
        help="在本进程内设置 LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1（默认不设置，保持主链行为）",
    )
    args = ap.parse_args()

    if args.enable_prefilter_routing:
        os.environ["LUNA_VOICE_ENABLE_PREFILTER_ROUTING"] = "1"

    from capabilities.voice.runtime.voice_final_text_dispatcher import dispatch_voice_final_text
    from capabilities.voice.schemas.voice_input_event import VoiceInputEvent

    # wrap validator：捕获最近一次 validate_model_structured_output 结果（若本条走规则链，则为 None）
    import capabilities.voice.bridge.voice_long_input_model_output_validator as vmod

    _last_vr: Dict[str, Any] = {"vr": None}
    _orig_val = vmod.validate_model_structured_output

    def _val_wrap(s: Any, *, cfg: Any):
        r = _orig_val(s, cfg=cfg)
        _last_vr["vr"] = r
        return r

    vmod.validate_model_structured_output = _val_wrap  # type: ignore[assignment]

    data = json.loads(args.cases_json.read_text(encoding="utf-8"))
    cases: List[Dict[str, Any]] = list(data.get("cases") or [])
    if not cases:
        raise SystemExit(f"no cases in {args.cases_json}")

    rows: List[Row] = []
    route_counts: Dict[str, int] = {"route_to_turbo": 0, "route_to_plus": 0, "route_to_rule_or_reject": 0}
    e2e_all: List[float] = []

    for r in range(1, max(1, int(args.rounds)) + 1):
        for c in cases:
            cid = str(c.get("id") or "")
            text = str(c.get("text") or "")
            kws = list(c.get("mixed_keywords") or [])
            _last_vr["vr"] = None

            ev = VoiceInputEvent(
                event_id=f"m35_{r}_{cid}",
                request_id=f"m35_{r}_{cid}",
                session_id="m35",
                router_decision="accept",
                raw_text=text,
                normalized_text=text,
                wake_word_stripped=text,
                is_task_mode=False,
                shortcut_id=None,
                wake_word_detected=False,
            )
            t0 = time.perf_counter()
            out = dispatch_voice_final_text(ev)
            e2e_ms = (time.perf_counter() - t0) * 1000.0
            e2e_all.append(e2e_ms)

            meta = out.metadata or {}
            sug = str(meta.get("prefilter_routing_suggestion") or "")
            sel = str(meta.get("selected_provider_model_id") or "")
            if sug in route_counts:
                route_counts[sug] += 1

            res = out.long_input_parse_result
            notes = (getattr(res, "notes", "") or "") if res is not None else ""
            used_model = notes.startswith("model_chain")
            vr = _last_vr["vr"]
            vok = bool(vr.ok) if (vr is not None) else None

            # fallback 口径：
            # - 若路由建议走模型（turbo/plus），但没走 model_chain，则视为 fallback
            # - 若建议 rule_or_reject，则不把规则链当作 fallback
            fallback = False
            if sug in ("route_to_turbo", "route_to_plus"):
                fallback = not (used_model and vok is True)

            mixed_preserved: Optional[bool] = None
            if kws and res is not None:
                blob = _non_task_blob(res)
                mixed_preserved = any(k in blob for k in kws)

            rows.append(
                Row(
                    case_id=cid,
                    routing_suggestion=sug,
                    selected_provider_model_id=sel,
                    used_model_chain=used_model,
                    validator_ok=vok,
                    fallback=fallback,
                    mixed_preserved=mixed_preserved,
                    e2e_ms=e2e_ms,
                )
            )

    # restore
    vmod.validate_model_structured_output = _orig_val  # type: ignore[assignment]

    n = len(rows)
    model_rows = [x for x in rows if x.routing_suggestion in ("route_to_turbo", "route_to_plus")]
    n_m = len(model_rows)
    json_rate = sum(1 for x in model_rows if x.used_model_chain) / n_m if n_m else 0.0
    val_rate = sum(1 for x in model_rows if x.validator_ok is True) / n_m if n_m else 0.0
    fallback_rate = sum(1 for x in model_rows if x.fallback) / n_m if n_m else 0.0

    mixed_rows = [x for x in rows if x.mixed_preserved is not None]
    mixed_preserve_rate = (
        (sum(1 for x in mixed_rows if x.mixed_preserved is True) / len(mixed_rows)) if mixed_rows else None
    )

    print("M3.5 prefilter smoke")
    print("  cases_json:", args.cases_json)
    print("  rounds:", args.rounds)
    print("  prefilter_enabled:", bool(os.getenv("LUNA_VOICE_ENABLE_PREFILTER_ROUTING")))
    print("  n:", n)
    print("  model_routed_n:", n_m)
    print("  json_rate(model_routes):", round(json_rate, 4))
    print("  val_rate(model_routes):", round(val_rate, 4))
    print("  fallback_rate(model_routes):", round(fallback_rate, 4))
    print("  mixed_preserve_rate:", None if mixed_preserve_rate is None else round(mixed_preserve_rate, 4))
    print("  avg_ms:", round(sum(e2e_all) / len(e2e_all), 2) if e2e_all else 0.0)
    print("  p95_ms:", round(_p95(e2e_all), 2) if e2e_all else 0.0)
    print("  route_counts:", route_counts)


if __name__ == "__main__":
    main()


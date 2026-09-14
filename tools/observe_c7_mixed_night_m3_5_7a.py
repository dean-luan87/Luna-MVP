#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3.5.7a：C7/night 定点观察（mixed 波动）+ 最小证据落盘

目标：
- 只跑 case：C7_mixed_sleep_park_nav
- day / night 对照
- 多轮重复（建议 20～30 轮）
- 输出：mixed_preserved、missing_keywords、selected_provider_model_id、routing_suggestion、cleaned_text、non_task_payload 摘要、e2e_ms

原则：
- 不扩灰、不改骨架、不改 prefilter/prompt/schema/validator/builder/fallback
- 本脚本只做观察与记录，不做修复

用法：
  export LUNA_EXTERNAL_LLM_PROVIDER=qwen
  export DASHSCOPE_API_KEY=...
  export LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1
  export LUNA_QWEN_MODEL_TIMEOUT_MS=120000
  python3 tools/observe_c7_mixed_night_m3_5_7a.py --rounds 25 --time-slot all
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _git_head() -> str:
    try:
        return (
            subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except Exception:
        return ""


def _non_task_blob(res: Any) -> str:
    p = getattr(res, "non_task_payload", None)
    if not p or not getattr(p, "exists", False):
        return ""
    segs = getattr(p, "segments", None) or []
    return " ".join((getattr(s, "content", "") or "") for s in segs)


def _non_task_segments(res: Any) -> List[Dict[str, str]]:
    p = getattr(res, "non_task_payload", None)
    if not p or not getattr(p, "exists", False):
        return []
    segs = getattr(p, "segments", None) or []
    out: List[Dict[str, str]] = []
    for s in segs:
        out.append(
            {
                "segment_type": str(getattr(s, "segment_type", "") or ""),
                "content": str(getattr(s, "content", "") or ""),
            }
        )
    return out


@dataclass
class Row:
    time_slot: str
    round: int
    case_id: str
    routing_suggestion: str
    selected_provider_model_id: str
    bucket: str
    raw_text: str
    cleaned_text: str
    mixed_keywords: List[str]
    mixed_preserved: Optional[bool]
    missing_keywords: List[str]
    non_task_payload_exists: Optional[bool]
    non_task_payload_summary: str
    non_task_segments: List[Dict[str, str]]
    used_model_chain: bool
    validator_ok: Optional[bool]
    fallback: bool
    e2e_ms: float


def main() -> None:
    ap = argparse.ArgumentParser(description="M3.5.7a observe C7 mixed fluctuation (day/night)")
    ap.add_argument(
        "--cases-json",
        type=Path,
        default=ROOT / "configs" / "voice" / "voice_prefilter_routing_real_cases_m3_5_3.json",
        help="case 集（默认 m3_5_3）",
    )
    ap.add_argument("--rounds", type=int, default=25, help="每时段轮数（建议 20～30；默认 25）")
    ap.add_argument("--time-slot", choices=("day", "night", "all"), default="all", help="day/night 单段；all 顺序跑两段")
    ap.add_argument("--out-json", type=Path, default=None, help="落盘路径（默认 logs/observe_c7_mixed_night_m3_5_7a_<UTC>.json）")
    ap.add_argument("--out-dir", type=Path, default=Path.cwd() / "logs", help="输出目录（默认当前工作目录的 logs/）")
    ap.add_argument("--model-timeout-ms", type=int, default=120_000)
    args = ap.parse_args()

    # 与主线一致：显式开关；默认行为不变
    os.environ["LUNA_VOICE_ENABLE_PREFILTER_ROUTING"] = "1"
    if not (os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS") or "").strip():
        os.environ["LUNA_QWEN_MODEL_TIMEOUT_MS"] = str(int(args.model_timeout_ms))

    data = json.loads(args.cases_json.read_text(encoding="utf-8"))
    cases = list(data.get("cases") or [])
    c7 = None
    for c in cases:
        if str(c.get("id") or "") == "C7_mixed_sleep_park_nav":
            c7 = c
            break
    if not c7:
        raise SystemExit("C7_mixed_sleep_park_nav not found in cases json")

    raw_text = str(c7.get("text") or "")
    bucket = str(c7.get("bucket") or "")
    mixed_keywords = list(c7.get("mixed_keywords") or [])

    from capabilities.voice.runtime.voice_final_text_dispatcher import dispatch_voice_final_text
    from capabilities.voice.schemas.voice_input_event import VoiceInputEvent
    from capabilities.voice.bridge.voice_long_input_prefilter_v0 import prefilter_long_voice_text_v0

    import capabilities.voice.bridge.voice_long_input_model_output_validator as vmod

    _last_vr: Dict[str, Any] = {"vr": None}
    _orig_val = vmod.validate_model_structured_output

    def _val_wrap(s: Any, *, cfg: Any):
        r = _orig_val(s, cfg=cfg)
        _last_vr["vr"] = r
        return r

    vmod.validate_model_structured_output = _val_wrap  # type: ignore[assignment]

    slots = ["day", "night"] if args.time_slot == "all" else [args.time_slot]
    rows: List[Row] = []

    print("M3.5.7a observe starting…", flush=True)
    print("  case_id: C7_mixed_sleep_park_nav", "rounds/slot:", args.rounds, "time_slot:", args.time_slot, flush=True)

    for slot in slots:
        for r in range(1, max(1, int(args.rounds)) + 1):
            _last_vr["vr"] = None

            ev = VoiceInputEvent(
                event_id=f"m357a_{slot}_{r}_C7",
                request_id=f"m357a_{slot}_{r}_C7",
                session_id=f"m357a_{slot}",
                router_decision="accept",
                raw_text=raw_text,
                normalized_text=raw_text,
                wake_word_stripped=raw_text,
                is_task_mode=False,
                shortcut_id=None,
                wake_word_detected=False,
            )
            t0 = time.perf_counter()
            out = dispatch_voice_final_text(ev)
            e2e_ms = (time.perf_counter() - t0) * 1000.0

            meta = out.metadata or {}
            sug = str(meta.get("prefilter_routing_suggestion") or "")
            sel = str(meta.get("selected_provider_model_id") or "")

            # cleaned_text：以 prefilter 纯函数复算（dispatcher 内同口径）
            pf = prefilter_long_voice_text_v0(raw_text, session_hint=ev.context_resume_hint or "")
            cleaned = str(getattr(pf, "cleaned_text", "") or "")

            res = out.long_input_parse_result
            notes = (getattr(res, "notes", "") or "") if res is not None else ""
            used_model_chain = notes.startswith("model_chain")
            vr = _last_vr["vr"]
            vok = bool(vr.ok) if (vr is not None) else None

            fallback = False
            if sug in ("route_to_turbo", "route_to_plus"):
                fallback = not (used_model_chain and vok is True)

            nt_exists: Optional[bool] = None
            if res is not None:
                ntp = getattr(res, "non_task_payload", None)
                if ntp is not None:
                    nt_exists = bool(getattr(ntp, "exists", False))

            blob = _non_task_blob(res) if res is not None else ""
            mixed_preserved: Optional[bool] = None
            missing: List[str] = []
            if mixed_keywords and res is not None:
                missing = [k for k in mixed_keywords if (k not in blob)]
                mixed_preserved = (len(missing) == 0)

            segs = _non_task_segments(res) if res is not None else []
            summary = (blob[:160] + "…") if len(blob) > 160 else blob

            rows.append(
                Row(
                    time_slot=slot,
                    round=r,
                    case_id="C7_mixed_sleep_park_nav",
                    routing_suggestion=sug,
                    selected_provider_model_id=sel,
                    bucket=bucket,
                    raw_text=raw_text,
                    cleaned_text=cleaned,
                    mixed_keywords=mixed_keywords,
                    mixed_preserved=mixed_preserved,
                    missing_keywords=missing,
                    non_task_payload_exists=nt_exists,
                    non_task_payload_summary=summary,
                    non_task_segments=segs,
                    used_model_chain=used_model_chain,
                    validator_ok=vok,
                    fallback=fallback,
                    e2e_ms=e2e_ms,
                )
            )

            print(f"  [{slot}] [{r}/{args.rounds}] mixed_preserved={mixed_preserved} missing={missing} e2e_ms={e2e_ms:.1f}", flush=True)

    vmod.validate_model_structured_output = _orig_val  # type: ignore[assignment]

    payload: Dict[str, Any] = {
        "schema": "luna.voice.observe_m3_5_7a_c7_night.v1",
        "git_head": _git_head(),
        "cases_path": str(args.cases_json),
        "rounds_per_time_slot": int(args.rounds),
        "time_slots_executed": slots,
        "env": {
            "LUNA_VOICE_ENABLE_PREFILTER_ROUTING": os.getenv("LUNA_VOICE_ENABLE_PREFILTER_ROUTING"),
            "LUNA_QWEN_MODEL_TIMEOUT_MS": os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS"),
            "LUNA_EXTERNAL_LLM_PROVIDER": os.getenv("LUNA_EXTERNAL_LLM_PROVIDER"),
        },
        "rows": [asdict(x) for x in rows],
    }

    out_path = args.out_json
    if out_path is None:
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"observe_c7_mixed_night_m3_5_7a_{_utc_stamp()}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # Markdown table
    md_path = out_path.with_suffix(".md")
    lines: List[str] = []
    lines.append("# M3.5.7a C7/night mixed 定点观察")
    lines.append("")
    lines.append(f"- out_json: `{out_path}`")
    lines.append(f"- git_head: `{payload['git_head']}`")
    lines.append(f"- rounds/slot: **{args.rounds}** | slots: `{','.join(slots)}`")
    lines.append(f"- mixed_keywords: `{mixed_keywords}`")
    lines.append("")
    lines.append("| # | slot | round | mixed_preserved | missing_keywords | used_model_chain | validator_ok | fallback | suggestion | selected_model | non_task_exists | non_task_summary | e2e_ms |")
    lines.append("|---:|------|------:|----------------|------------------|-----------------|-------------|----------|------------|----------------|--------------|----------------|------:|")
    for i, r in enumerate(rows, 1):
        lines.append(
            "| {i} | {slot} | {rd} | {mp} | {miss} | {um} | {vok} | {fb} | {sug} | {m} | {nte} | {sum} | {ms:.1f} |".format(
                i=i,
                slot=r.time_slot,
                rd=r.round,
                mp=str(r.mixed_preserved),
                miss=str(r.missing_keywords),
                um=str(r.used_model_chain),
                vok=str(r.validator_ok),
                fb=str(r.fallback),
                sug=r.routing_suggestion or "—",
                m=r.selected_provider_model_id or "—",
                nte=str(r.non_task_payload_exists),
                sum=(r.non_task_payload_summary or "—").replace("\n", " ")[:80],
                ms=float(r.e2e_ms or 0.0),
            )
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("M3.5.7a observe OK")
    print("  out_json:", str(out_path))
    print("  out_md  :", str(md_path))


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3.5.1 小范围灰度验证（固定口径）

写死原则（避免灰度发散）：
- 仅在本进程内开启 LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1
- 固定 case 集、固定轮数；不混入新 prompt / 新模型 / 新规则
- 结果落盘 JSON（含硬指标、运营指标、暂停条件检查）

模型超时：
- **若未设置**环境变量 `LUNA_QWEN_MODEL_TIMEOUT_MS`，本脚本会在进程内默认写入 **120000**（与 benchmark 对齐，避免 YAML 默认 2000ms 导致全量超时）。
- 若已 `export LUNA_QWEN_MODEL_TIMEOUT_MS=...`，则以环境变量为准。

用法：
  export LUNA_EXTERNAL_LLM_PROVIDER=qwen
  export DASHSCOPE_API_KEY=...
  python3 tools/run_prefilter_routing_gray_m3_5_1.py --rounds 3 --out-json logs/gray_m3_5_1.json
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
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
    bucket: str
    routing_suggestion: str
    selected_provider_model_id: str
    used_model_chain: bool
    validator_ok: Optional[bool]
    fallback: bool
    mixed_preserved: Optional[bool]
    e2e_ms: float


def _git_head() -> str:
    try:
        return (
            subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except Exception:
        return ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--cases-json",
        type=Path,
        default=ROOT / "configs" / "voice" / "voice_prefilter_routing_real_cases_m3_5.json",
        help="固定 case 集（默认 M3.5 真实场景 12 条）",
    )
    ap.add_argument("--rounds", type=int, default=3, help="固定轮数（每轮跑一遍 cases）")
    ap.add_argument(
        "--out-json",
        type=Path,
        default=None,
        help="结果落盘路径（默认 logs/gray_m3_5_1_<UTC时间>.json）",
    )
    ap.add_argument(
        "--mixed-preserve-min",
        type=float,
        default=0.95,
        help="mixed_preserve_rate 低于该阈值则触发暂停检查（默认 0.95）",
    )
    ap.add_argument(
        "--rule-reject-max-ratio",
        type=float,
        default=0.35,
        help="rule_or_reject 占比高于该阈值则触发暂停检查（默认 0.35）",
    )
    ap.add_argument(
        "--model-timeout-ms",
        type=int,
        default=120_000,
        help="未设置 LUNA_QWEN_MODEL_TIMEOUT_MS 时使用的模型超时（ms）；默认 120000",
    )
    args = ap.parse_args()

    # 固定口径：显式开关开启（仅本进程）
    os.environ["LUNA_VOICE_ENABLE_PREFILTER_ROUTING"] = "1"
    if not (os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS") or "").strip():
        os.environ["LUNA_QWEN_MODEL_TIMEOUT_MS"] = str(int(args.model_timeout_ms))

    from capabilities.voice.runtime.voice_final_text_dispatcher import dispatch_voice_final_text
    from capabilities.voice.schemas.voice_input_event import VoiceInputEvent

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

    t_started = time.perf_counter()
    started_iso = datetime.now(timezone.utc).isoformat()

    print("M3.5.1 gray run starting…", flush=True)
    print(
        "  cases:",
        args.cases_json,
        "rounds:",
        args.rounds,
        "cases_n:",
        len(cases),
        "LUNA_QWEN_MODEL_TIMEOUT_MS:",
        os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS"),
        flush=True,
    )

    rows: List[Row] = []
    route_counts: Dict[str, int] = {"route_to_turbo": 0, "route_to_plus": 0, "route_to_rule_or_reject": 0}
    e2e_all: List[float] = []
    sel_counter: Counter[str] = Counter()

    complex_turbo: List[Dict[str, Any]] = []

    for r in range(1, max(1, int(args.rounds)) + 1):
        for c in cases:
            cid = str(c.get("id") or "")
            bucket = str(c.get("bucket") or "")
            text = str(c.get("text") or "")
            kws = list(c.get("mixed_keywords") or [])
            _last_vr["vr"] = None

            print(f"  [{r}/{args.rounds}] {cid} …", flush=True)

            ev = VoiceInputEvent(
                event_id=f"m351_{r}_{cid}",
                request_id=f"m351_{r}_{cid}",
                session_id="m351_gray",
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
            if sel:
                sel_counter[sel] += 1

            res = out.long_input_parse_result
            notes = (getattr(res, "notes", "") or "") if res is not None else ""
            used_model = notes.startswith("model_chain")
            vr = _last_vr["vr"]
            vok = bool(vr.ok) if (vr is not None) else None

            fallback = False
            if sug in ("route_to_turbo", "route_to_plus"):
                fallback = not (used_model and vok is True)

            mixed_preserved: Optional[bool] = None
            if kws and res is not None:
                blob = _non_task_blob(res)
                mixed_preserved = any(k in blob for k in kws)

            if bucket == "complex" and sug == "route_to_turbo":
                complex_turbo.append({"case_id": cid, "bucket": bucket, "routing_suggestion": sug})

            rows.append(
                Row(
                    case_id=cid,
                    bucket=bucket,
                    routing_suggestion=sug,
                    selected_provider_model_id=sel,
                    used_model_chain=used_model,
                    validator_ok=vok,
                    fallback=fallback,
                    mixed_preserved=mixed_preserved,
                    e2e_ms=e2e_ms,
                )
            )

    vmod.validate_model_structured_output = _orig_val  # type: ignore[assignment]

    ended_iso = datetime.now(timezone.utc).isoformat()
    duration_s = time.perf_counter() - t_started

    n = len(rows)
    model_rows = [x for x in rows if x.routing_suggestion in ("route_to_turbo", "route_to_plus")]
    n_m = len(model_rows)
    json_rate = sum(1 for x in model_rows if x.used_model_chain) / n_m if n_m else 0.0
    val_rate = sum(1 for x in model_rows if x.validator_ok is True) / n_m if n_m else 0.0
    fallback_rate = sum(1 for x in model_rows if x.fallback) / n_m if n_m else 0.0

    mixed_rows = [x for x in rows if x.mixed_preserved is not None]
    mixed_preserve_rate: Optional[float] = (
        (sum(1 for x in mixed_rows if x.mixed_preserved is True) / len(mixed_rows)) if mixed_rows else None
    )

    rule_n = route_counts.get("route_to_rule_or_reject", 0)
    rule_ratio = float(rule_n) / float(n) if n else 0.0

    pause_checks = {
        "val_rate_lt_1": val_rate < 1.0,
        "fallback_rate_gt_0": fallback_rate > 0.0,
        "mixed_preserve_below_min": (
            mixed_preserve_rate is not None and mixed_preserve_rate < float(args.mixed_preserve_min)
        ),
        "rule_or_reject_ratio_high": rule_ratio > float(args.rule_reject_max_ratio),
        "complex_bucket_routed_turbo_nonzero": len(complex_turbo) > 0,
    }
    pause_stop = any(
        [
            pause_checks["val_rate_lt_1"],
            pause_checks["fallback_rate_gt_0"],
            pause_checks["mixed_preserve_below_min"],
            pause_checks["rule_or_reject_ratio_high"],
        ]
    )

    payload: Dict[str, Any] = {
        "schema": "luna.voice.gray_m3_5_1.v1",
        "started_at_utc": started_iso,
        "ended_at_utc": ended_iso,
        "duration_sec": round(duration_s, 3),
        "git_head": _git_head(),
        "cases_path": str(args.cases_json),
        "rounds": int(args.rounds),
        "env": {
            "LUNA_VOICE_ENABLE_PREFILTER_ROUTING": os.getenv("LUNA_VOICE_ENABLE_PREFILTER_ROUTING"),
            "LUNA_QWEN_MODEL_TIMEOUT_MS": os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS"),
            "LUNA_EXTERNAL_LLM_PROVIDER": os.getenv("LUNA_EXTERNAL_LLM_PROVIDER"),
        },
        "hard_metrics": {
            "n_total": n,
            "n_model_routes": n_m,
            "json_rate_model_routes": json_rate,
            "val_rate_model_routes": val_rate,
            "fallback_rate_model_routes": fallback_rate,
            "mixed_preserve_rate": mixed_preserve_rate,
        },
        "ops_metrics": {
            "avg_e2e_ms": round(sum(e2e_all) / len(e2e_all), 4) if e2e_all else 0.0,
            "p95_e2e_ms": round(_p95(e2e_all), 4) if e2e_all else 0.0,
            "route_counts": route_counts,
            "rule_or_reject_ratio": round(rule_ratio, 4),
            "selected_provider_model_id_counts": dict(sel_counter),
        },
        "pause_checks": pause_checks,
        "pause_stop_expand_gray": bool(pause_stop),
        "review": {
            "complex_bucket_routed_turbo": complex_turbo,
        },
        "rows": [asdict(x) for x in rows],
    }

    out_path = args.out_json
    if out_path is None:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_dir = ROOT / "logs"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"gray_prefilter_routing_m3_5_1_{ts}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("M3.5.1 gray run OK")
    print("  out_json:", str(out_path))
    print("  hard:", payload["hard_metrics"])
    print("  ops:", payload["ops_metrics"])
    print("  pause_stop_expand_gray:", payload["pause_stop_expand_gray"])
    print("  pause_checks:", payload["pause_checks"])


if __name__ == "__main__":
    main()

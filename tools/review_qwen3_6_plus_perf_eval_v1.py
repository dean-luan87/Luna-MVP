#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
评审补项（V1｜旁路｜不上线）：
对 qwen-plus vs qwen3.6-plus 做三件事：
1) P95（多轮 e2e_ms 分布）
2) 超时边界（timeout_ms sweep：观察 fallback/超时路径）
3) tokens / 成本代理指标（usage input/output/total 的分布与均值）

用法（需已配置百炼）：
  export LUNA_EXTERNAL_LLM_PROVIDER=qwen
  export DASHSCOPE_API_KEY=...
  python3 tools/review_qwen3_6_plus_perf_eval_v1.py

可选：
  --models qwen-plus,qwen3.6-plus
  --iters 20
  --timeout-sweep "30000,60000,120000"
  --out-dir logs

说明：
- 不改 schema / validator / builder / fallback 语义
- 仅做旁路评估与产物落盘（JSON + Markdown）
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PROMPT_PLUS = ROOT / "capabilities" / "voice" / "config" / "prompts" / "voice_long_input_parse_v1_1_prompt_qwen_plus.md"
PROMPT_TURBO = ROOT / "capabilities" / "voice" / "config" / "prompts" / "voice_long_input_parse_v1_1_prompt_qwen_turbo.md"

SMOKES: Tuple[Tuple[str, str], ...] = (
    ("task_two_steps", "先去商场，再找便利店买点吃的"),
    ("mixed_hospital", "我今天有点不舒服，先带我去最近的医院吧"),
    ("unsupported_register", "帮我自动挂号"),
    ("hospital_short", "带我去医院"),
)


def _utc_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _p95(xs: Sequence[float]) -> float:
    if not xs:
        return 0.0
    xs2 = sorted(float(x) for x in xs)
    k = int((len(xs2) - 1) * 0.95)
    return float(xs2[k])


def _p50(xs: Sequence[float]) -> float:
    if not xs:
        return 0.0
    xs2 = sorted(float(x) for x in xs)
    k = int((len(xs2) - 1) * 0.50)
    return float(xs2[k])


def _usage_digest(u: Any) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    if not isinstance(u, dict):
        return None, None, None
    it = u.get("input_tokens")
    ot = u.get("output_tokens")
    tt = u.get("total_tokens")
    return (
        int(it) if isinstance(it, (int, float)) else None,
        int(ot) if isinstance(ot, (int, float)) else None,
        int(tt) if isinstance(tt, (int, float)) else None,
    )


def _cfg(timeout_ms: int):
    from capabilities.voice.config.voice_long_input_parse_config import VoiceLongInputParseConfig

    return VoiceLongInputParseConfig(
        parse_mode="model_preferred_with_rule_fallback",
        enable_model_adapter=True,
        model_timeout_ms=timeout_ms,
        fallback_to_rule_on_timeout=True,
        fallback_to_rule_on_validation_error=True,
        max_task_candidates=3,
        allow_non_task_payload=True,
    )


@dataclass
class Stat:
    iter_idx: int
    case_name: str
    model: str
    timeout_ms: int
    e2e_ms: float
    provider_ms: float
    json_ok: bool
    validator_ok: Optional[bool]
    fallback: bool
    api_route: str
    usage_input_tokens: Optional[int]
    usage_output_tokens: Optional[int]
    usage_total_tokens: Optional[int]
    notes: str


def _run_eval(*, model: str, timeout_ms: int, iters: int) -> List[Stat]:
    import capabilities.voice.bridge.voice_long_input_model_output_validator as vmod
    from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1
    from capabilities.voice.providers.qwen_external_long_input_model_provider import (
        QwenExternalLongInputModelProvider,
        create_qwen_external_long_input_provider_from_env,
        is_qwen_external_llm_configured,
    )

    if not is_qwen_external_llm_configured():
        raise RuntimeError("未配置百炼：请设置 LUNA_EXTERNAL_LLM_PROVIDER=qwen 且配置 DASHSCOPE_API_KEY")

    cfg = _cfg(timeout_ms)
    base = create_qwen_external_long_input_provider_from_env(timeout_ms=cfg.model_timeout_ms)
    if base is None:
        raise RuntimeError("无法构造 Provider（create_qwen_external_long_input_provider_from_env 返回 None）")

    _last_vr: Dict[str, Any] = {"vr": None}
    _orig_val: Callable[..., Any] = vmod.validate_model_structured_output

    def _val_wrap(s: Any, *, cfg: Any):
        r = _orig_val(s, cfg=cfg)
        _last_vr["vr"] = r
        return r

    vmod.validate_model_structured_output = _val_wrap  # type: ignore[assignment]

    class _Instrumented(QwenExternalLongInputModelProvider):
        last_ms: float = 0.0
        last_json_ok: bool = False

        def parse_long_input(self, text: str, *, session_hint: str = "", request_id: str = ""):
            t0 = time.perf_counter()
            r = super().parse_long_input(text, session_hint=session_hint, request_id=request_id)
            _Instrumented.last_ms = (time.perf_counter() - t0) * 1000.0
            _Instrumented.last_json_ok = r is not None
            return r

    provider = _Instrumented(
        api_key=base.api_key,
        model=model,
        responses_url=base.responses_url,
        chat_base_url=base.chat_base_url,
        prompt_path=(
            PROMPT_PLUS
            if model in ("qwen-plus", "qwen3.6-plus")
            else (PROMPT_TURBO if model == "qwen-turbo" else base.prompt_path)
        ),
        timeout_ms=base.timeout_ms,
        max_output_tokens=base.max_output_tokens,
        schema_strict=base.schema_strict,
        prefer_responses_api=base.prefer_responses_api,
        responses_http_timeout_sec=getattr(base, "responses_http_timeout_sec", None),
        chat_http_timeout_sec=getattr(base, "chat_http_timeout_sec", None),
    )

    out: List[Stat] = []
    for i in range(iters):
        for case_name, text in SMOKES:
            _last_vr["vr"] = None
            _Instrumented.last_ms = 0.0
            _Instrumented.last_json_ok = False

            t0 = time.perf_counter()
            res = run_long_input_task_planning_v1(text, parse_config=cfg, model_provider=provider)
            e2e_ms = (time.perf_counter() - t0) * 1000.0

            vr = _last_vr["vr"]
            validator_ok: Optional[bool] = None
            if vr is not None:
                validator_ok = bool(vr.ok)

            json_ok = _Instrumented.last_json_ok
            fallback = not (json_ok and validator_ok is True)
            uit, uot, utt = _usage_digest(getattr(provider, "last_usage", None))

            out.append(
                Stat(
                    iter_idx=i,
                    case_name=case_name,
                    model=model,
                    timeout_ms=timeout_ms,
                    e2e_ms=e2e_ms,
                    provider_ms=_Instrumented.last_ms,
                    json_ok=json_ok,
                    validator_ok=validator_ok,
                    fallback=fallback,
                    api_route=getattr(provider, "last_api_route", "") or "",
                    usage_input_tokens=uit,
                    usage_output_tokens=uot,
                    usage_total_tokens=utt,
                    notes=(getattr(res, "notes", "") or "")[:200],
                )
            )

        # 轻量进度（每轮打印一次）
        print(f"progress model={model} timeout_ms={timeout_ms}: {i+1}/{iters}")
        sys.stdout.flush()

    return out


def _agg(stats: List[Stat]) -> Dict[str, Any]:
    n = len(stats) or 1
    e2e = [s.e2e_ms for s in stats]
    prov = [s.provider_ms for s in stats]
    json_rate = sum(1 for s in stats if s.json_ok) / n
    val_rate = sum(1 for s in stats if s.validator_ok is True) / n
    fb_rate = sum(1 for s in stats if s.fallback) / n

    def _avg_int(xs: List[Optional[int]]) -> Optional[float]:
        ys = [x for x in xs if isinstance(x, int)]
        return (sum(ys) / len(ys)) if ys else None

    uit_avg = _avg_int([s.usage_input_tokens for s in stats])
    uot_avg = _avg_int([s.usage_output_tokens for s in stats])
    utt_avg = _avg_int([s.usage_total_tokens for s in stats])

    routes: Dict[str, int] = {}
    for s in stats:
        if s.api_route:
            routes[s.api_route] = routes.get(s.api_route, 0) + 1

    return {
        "n": len(stats),
        "json_rate": round(json_rate, 4),
        "val_rate": round(val_rate, 4),
        "fallback_rate": round(fb_rate, 4),
        "e2e_ms": {
            "avg": round(statistics.mean(e2e), 1) if e2e else 0.0,
            "p50": round(_p50(e2e), 1),
            "p95": round(_p95(e2e), 1),
            "max": round(max(e2e), 1) if e2e else 0.0,
        },
        "provider_ms": {
            "avg": round(statistics.mean(prov), 1) if prov else 0.0,
            "p50": round(_p50(prov), 1),
            "p95": round(_p95(prov), 1),
            "max": round(max(prov), 1) if prov else 0.0,
        },
        "usage_tokens_avg": {
            "input": round(uit_avg, 1) if isinstance(uit_avg, float) else uit_avg,
            "output": round(uot_avg, 1) if isinstance(uot_avg, float) else uot_avg,
            "total": round(utt_avg, 1) if isinstance(utt_avg, float) else utt_avg,
        },
        "api_routes": routes,
    }


def _md_report(*, meta: Dict[str, Any], buckets: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("## qwen3.6-plus 评审补项（V1｜旁路）")
    lines.append("")
    lines.append("### 0. 两句话结论（占位，跑完后手填）")
    lines.append("- qwen3.6-plus 已完成评审补项旁路评测。")
    lines.append("- 基于 P95 / 超时边界 / tokens 成本结果，决定是否进入灰度替换评审。")
    lines.append("")
    lines.append("### 1. 元信息")
    lines.append("```json")
    lines.append(json.dumps(meta, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("### 2. 汇总（按 model × timeout_ms）")
    lines.append("")
    lines.append("| model | timeout_ms | n | json_rate | val_rate | fallback_rate | e2e_avg | e2e_p95 | provider_p95 | tok_in_avg | tok_out_avg | tok_total_avg |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for b in buckets:
        a = b["agg"]
        e = a["e2e_ms"]
        p = a["provider_ms"]
        u = a["usage_tokens_avg"]
        lines.append(
            f"| {b['model']} | {b['timeout_ms']} | {a['n']} | {a['json_rate']} | {a['val_rate']} | {a['fallback_rate']} | "
            f"{e['avg']} | {e['p95']} | {p['p95']} | {u.get('input')} | {u.get('output')} | {u.get('total')} |"
        )
    lines.append("")
    lines.append("### 3. 超时边界观察（快速读法）")
    lines.append("- 看同一 model 下，timeout_ms 下探时，fallback_rate 是否抬升，以及 e2e_p95 是否逼近 timeout_ms。")
    lines.append("- 若出现大量 fallback 且 notes/错误提示指向 timeout，再结合 provider_p95 判断是否为“超时边界过紧”。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="qwen-plus,qwen3.6-plus", help="逗号分隔的模型名")
    ap.add_argument("--iters", type=int, default=int(os.getenv("LUNA_BENCH_ITERS", "20")))
    ap.add_argument("--timeout-sweep", default="30000,60000,120000", help="逗号分隔 timeout_ms 列表")
    ap.add_argument("--out-dir", default="logs", help="输出目录（相对当前工作目录）")
    args = ap.parse_args()

    from capabilities.voice.providers.qwen_external_long_input_model_provider import qwen_external_ab_profile_label

    models = [m.strip() for m in str(args.models).split(",") if m.strip()]
    timeouts = [int(x.strip()) for x in str(args.timeout_sweep).split(",") if x.strip()]
    iters = int(args.iters)

    # 注意：避免因不同运行环境/软链导致 ROOT 解析到不可写目录；统一写到当前工作目录下
    out_dir = (Path.cwd() / str(args.out_dir)).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    run_ts = _utc_ts()
    meta = {
        "schema": "luna.voice.qwen3_6_plus_review_perf_eval.v1",
        "utc_ts": run_ts,
        "models": models,
        "iters": iters,
        "timeout_sweep_ms": timeouts,
        "provider_ab_profile": qwen_external_ab_profile_label(),
    }

    all_stats: List[Stat] = []
    buckets: List[Dict[str, Any]] = []
    for model in models:
        for timeout_ms in timeouts:
            stats = _run_eval(model=model, timeout_ms=timeout_ms, iters=iters)
            all_stats.extend(stats)
            buckets.append(
                {
                    "model": model,
                    "timeout_ms": timeout_ms,
                    "agg": _agg(stats),
                }
            )

    payload = {
        "meta": meta,
        "buckets": buckets,
        "stats": [asdict(s) for s in all_stats],
    }

    out_json = out_dir / f"review_qwen3_6_plus_perf_eval_v1_{run_ts}.json"
    out_md = out_dir / f"review_qwen3_6_plus_perf_eval_v1_{run_ts}.md"

    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(_md_report(meta=meta, buckets=buckets), encoding="utf-8")

    print("wrote:", out_json)
    print("wrote:", out_md)


if __name__ == "__main__":
    main()


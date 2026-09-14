#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轻量多轮压测：qwen-plus 长语音任务拆解（avg / P95 / 稳定性）。

范围写死：
- 不改 schema / validator / builder / fallback
- 使用现有 QwenExternalLongInputModelProvider

使用：
export LUNA_EXTERNAL_LLM_PROVIDER=qwen
export DASHSCOPE_API_KEY=...
export LUNA_SMOKE_QWEN_MODELS="qwen-plus"
export LUNA_BENCH_ITERS=20
python3 tools/benchmark_qwen_plus_long_input_p95.py
"""

from __future__ import annotations

import os
import statistics
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PROMPT_PLUS = ROOT / "capabilities" / "voice" / "config" / "prompts" / "voice_long_input_parse_v1_1_prompt_qwen_plus.md"


SMOKES: Tuple[Tuple[str, str], ...] = (
    ("task_two_steps", "先去商场，再找便利店买点吃的"),
    ("mixed_hospital", "我今天有点不舒服，先带我去最近的医院吧"),
    ("unsupported_register", "帮我自动挂号"),
    ("hospital_short", "带我去医院"),
)


def _cfg():
    from capabilities.voice.config.voice_long_input_parse_config import VoiceLongInputParseConfig

    return VoiceLongInputParseConfig(
        parse_mode="model_preferred_with_rule_fallback",
        enable_model_adapter=True,
        model_timeout_ms=120_000,
        fallback_to_rule_on_timeout=True,
        fallback_to_rule_on_validation_error=True,
        max_task_candidates=3,
        allow_non_task_payload=True,
    )


def _p95(xs: List[float]) -> float:
    if not xs:
        return 0.0
    xs2 = sorted(xs)
    k = int((len(xs2) - 1) * 0.95)
    return float(xs2[k])


@dataclass
class Stat:
    e2e_ms: float
    json_ok: bool
    validator_ok: Optional[bool]
    fallback: bool
    mixed_preserved: Optional[bool]
    api_route: str


def main() -> None:
    import capabilities.voice.bridge.voice_long_input_model_output_validator as vmod
    from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1
    from capabilities.voice.providers.qwen_external_long_input_model_provider import (
        QwenExternalLongInputModelProvider,
        create_qwen_external_long_input_provider_from_env,
        is_qwen_external_llm_configured,
        qwen_external_ab_profile_label,
    )

    if not is_qwen_external_llm_configured():
        print("跳过：请设置 LUNA_EXTERNAL_LLM_PROVIDER=qwen 且配置 DASHSCOPE_API_KEY。", file=sys.stderr)
        sys.exit(2)

    iters = int(os.getenv("LUNA_BENCH_ITERS", "20"))
    model = (os.getenv("LUNA_BENCH_MODEL") or "qwen-plus").strip()
    cfg = _cfg()

    base = create_qwen_external_long_input_provider_from_env(timeout_ms=cfg.model_timeout_ms)
    if base is None:
        print("无法构造 Provider。", file=sys.stderr)
        sys.exit(2)

    _last_vr: Dict[str, Any] = {"vr": None}
    _orig_val: Callable[..., Any] = vmod.validate_model_structured_output

    def _val_wrap(s: Any, *, cfg: Any):
        r = _orig_val(s, cfg=cfg)
        _last_vr["vr"] = r
        return r

    vmod.validate_model_structured_output = _val_wrap  # type: ignore[assignment]

    class _Instrumented(QwenExternalLongInputModelProvider):
        last_json_ok: bool = False

        def parse_long_input(self, text: str, *, session_hint: str = "", request_id: str = ""):
            r = super().parse_long_input(text, session_hint=session_hint, request_id=request_id)
            _Instrumented.last_json_ok = r is not None
            return r

    provider = _Instrumented(
        api_key=base.api_key,
        model=model,
        responses_url=base.responses_url,
        chat_base_url=base.chat_base_url,
        # 与主链 smoke 对齐：qwen-plus 使用专用瘦输出 prompt
        prompt_path=PROMPT_PLUS if model == "qwen-plus" else base.prompt_path,
        timeout_ms=base.timeout_ms,
        max_output_tokens=base.max_output_tokens,
        schema_strict=base.schema_strict,
        prefer_responses_api=base.prefer_responses_api,
    )

    per_case: Dict[str, List[Stat]] = {k: [] for k, _ in SMOKES}

    print("model:", model)
    print("provider_ab_profile:", qwen_external_ab_profile_label())
    print("iters:", iters)
    print("responses_url:", provider.responses_url)
    print("chat_base_url:", provider.chat_base_url)
    print("---")
    sys.stdout.flush()

    for i in range(iters):
        for name, text in SMOKES:
            _last_vr["vr"] = None
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

            mixed_ok: Optional[bool] = None
            if name == "mixed_hospital":
                mixed_ok = bool(
                    res.non_task_payload
                    and res.non_task_payload.exists
                    and any("不舒服" in (s.content or "") for s in (res.non_task_payload.segments or []))
                )

            per_case[name].append(
                Stat(
                    e2e_ms=e2e_ms,
                    json_ok=json_ok,
                    validator_ok=validator_ok,
                    fallback=fallback,
                    mixed_preserved=mixed_ok,
                    api_route=getattr(provider, "last_api_route", "") or "",
                )
            )

        # 轻量进度：每轮结束打印一次，避免“无反应”错觉
        print(f"progress: {i+1}/{iters}")
        sys.stdout.flush()

    print("")
    print("结果（每条 case）")
    for name, _ in SMOKES:
        xs = [s.e2e_ms for s in per_case[name]]
        json_rate = sum(1 for s in per_case[name] if s.json_ok) / len(xs)
        val_rate = sum(1 for s in per_case[name] if s.validator_ok is True) / len(xs)
        fb_rate = sum(1 for s in per_case[name] if s.fallback) / len(xs)
        avg = statistics.mean(xs)
        p95 = _p95(xs)
        routes: Dict[str, int] = {}
        for s in per_case[name]:
            if s.api_route:
                routes[s.api_route] = routes.get(s.api_route, 0) + 1
        mixed = None
        if name == "mixed_hospital":
            mixed = sum(1 for s in per_case[name] if s.mixed_preserved is True) / len(xs)
        print(
            f"- {name}: avg_ms={avg:.1f} p95_ms={p95:.1f} "
            f"json={json_rate:.2f} val={val_rate:.2f} fallback={fb_rate:.2f} "
            f"mixed_preserve_rate={mixed if mixed is not None else 'N/A'} routes={routes}"
        )

    print("")
    print("总汇总（全样本）")
    all_stats = [s for xs in per_case.values() for s in xs]
    xs_all = [s.e2e_ms for s in all_stats]
    print("avg_ms:", round(statistics.mean(xs_all), 1))
    print("p95_ms:", round(_p95(xs_all), 1))
    print("json_rate:", round(sum(1 for s in all_stats if s.json_ok) / len(all_stats), 3))
    print("val_rate:", round(sum(1 for s in all_stats if s.validator_ok is True) / len(all_stats), 3))
    print("fallback_rate:", round(sum(1 for s in all_stats if s.fallback) / len(all_stats), 3))
    mixed_stats = per_case.get("mixed_hospital") or []
    if mixed_stats:
        mpr = sum(1 for s in mixed_stats if s.mixed_preserved is True) / len(mixed_stats)
        print("mixed_preserve_rate:", round(mpr, 3))

    jr_all = sum(1 for s in all_stats if s.json_ok) / len(all_stats) if all_stats else 0.0
    if jr_all < 1.0:
        print("")
        print("【警告】存在 json_ok=False。若日志中出现 status=401 / InvalidApiKey，说明 DASHSCOPE_API_KEY 无效或未生效，")
        print("        此时 avg_ms 仅为失败路径耗时，不可用于 provider A/B 或性能基线对比。")
    if jr_all == 0.0 and all_stats:
        print("【无效】json_rate=0：本次压测对 A/B 无意义，请修复 Key 后重跑。")


if __name__ == "__main__":
    main()


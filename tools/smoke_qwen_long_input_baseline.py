#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云百炼 Qwen 长语音任务拆解基线（真实 API）。

前置：
- `export LUNA_EXTERNAL_LLM_PROVIDER=qwen`
- `export DASHSCOPE_API_KEY='...'`
- `export LUNA_QWEN_EXTERNAL_MODEL=...` 或 `export LUNA_EXTERNAL_LLM_MODEL=...`（可选，默认 qwen3.5-flash）
- 可选：`export LUNA_QWEN_REGION=intl`（新加坡兼容 endpoint）

四条输入与统计口径与先前 OpenAI smoke 对齐；不改 validator / builder / fallback 语义。
"""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PROMPT_PLUS = ROOT / "capabilities" / "voice" / "config" / "prompts" / "voice_long_input_parse_v1_1_prompt_qwen_plus.md"
PROMPT_TURBO = ROOT / "capabilities" / "voice" / "config" / "prompts" / "voice_long_input_parse_v1_1_prompt_qwen_turbo.md"


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


SMOKES: Tuple[Tuple[str, str], ...] = (
    ("task_two_steps", "先去商场，再找便利店买点吃的"),
    ("mixed_hospital", "我今天有点不舒服，先带我去最近的医院吧"),
    ("unsupported_register", "帮我自动挂号"),
    ("hospital_short", "带我去医院"),
)

MODEL_CANDIDATES: Tuple[str, ...] = ("qwen3.5-flash", "qwen-plus", "qwen-turbo")
"""默认对比的模型列表。可用环境变量 `LUNA_SMOKE_QWEN_MODELS` 覆盖，例如：
`export LUNA_SMOKE_QWEN_MODELS="qwen-plus,qwen-turbo"`"""


def _selected_models() -> List[str]:
    raw = (os.getenv("LUNA_SMOKE_QWEN_MODELS") or "").strip()
    if not raw:
        return list(MODEL_CANDIDATES)
    ms = [x.strip() for x in raw.split(",") if x.strip()]
    return ms if ms else list(MODEL_CANDIDATES)


@dataclass
class Row:
    name: str
    text: str
    json_ok: bool = False
    api_route: str = ""
    usage_input_tokens: Optional[int] = None
    usage_output_tokens: Optional[int] = None
    usage_total_tokens: Optional[int] = None
    provider_ms: float = 0.0
    validator_ok: Optional[bool] = None
    validator_errors: List[str] = field(default_factory=list)
    fallback: bool = False
    e2e_ms: float = 0.0
    task_plan_v1_ok: bool = False
    task_plan_steps: int = 0
    task_plan_summary: str = ""
    mixed_non_task_preserved: Optional[bool] = None
    primary_domain: str = ""
    notes: str = ""


def _task_plan_digest(plan: Any) -> Tuple[int, str]:
    if plan is None:
        return 0, "null"
    try:
        eo = getattr(plan, "execution_order", None) or []
        n = len(eo)
        titles = []
        for x in eo[:5]:
            if hasattr(x, "instruction_text"):
                titles.append(getattr(x, "instruction_text", "") or "")
            elif isinstance(x, dict):
                titles.append(str(x.get("instruction_text", "")))
        tail = "..." if n > 5 else ""
        return n, json.dumps(titles, ensure_ascii=False) + tail
    except Exception:
        return -1, "error"

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

def _run_one_model(*, base_provider: Any, model: str) -> Dict[str, Any]:
    import capabilities.voice.bridge.voice_long_input_model_output_validator as vmod
    from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1
    from capabilities.voice.providers.qwen_external_long_input_model_provider import QwenExternalLongInputModelProvider

    cfg = _cfg()
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
        api_key=base_provider.api_key,
        model=model,
        responses_url=base_provider.responses_url,
        chat_base_url=base_provider.chat_base_url,
        prompt_path=(PROMPT_PLUS if model == "qwen-plus" else (PROMPT_TURBO if model == "qwen-turbo" else base_provider.prompt_path)),
        timeout_ms=base_provider.timeout_ms,
        max_output_tokens=base_provider.max_output_tokens,
        schema_strict=base_provider.schema_strict,
        prefer_responses_api=base_provider.prefer_responses_api,
    )

    rows: List[Row] = []
    for name, text in SMOKES:
        _last_vr["vr"] = None
        _Instrumented.last_ms = 0.0
        _Instrumented.last_json_ok = False

        t0 = time.perf_counter()
        res = run_long_input_task_planning_v1(text, parse_config=cfg, model_provider=provider)
        e2e_ms = (time.perf_counter() - t0) * 1000.0

        vr = _last_vr["vr"]
        validator_ok: Optional[bool] = None
        verrs: List[str] = []
        if vr is not None:
            validator_ok = bool(vr.ok)
            verrs = list(vr.errors or [])

        json_ok = _Instrumented.last_json_ok
        fallback = not (json_ok and validator_ok is True)
        steps, digest = _task_plan_digest(res.task_plan_v1)
        plan_ok = res.task_plan_v1 is not None

        mixed_ok: Optional[bool] = None
        if name == "mixed_hospital":
            mixed_ok = bool(
                res.non_task_payload
                and res.non_task_payload.exists
                and any("不舒服" in (s.content or "") for s in (res.non_task_payload.segments or []))
            )

        uit, uot, utt = _usage_digest(getattr(provider, "last_usage", None))

        row = Row(
            name=name,
            text=text,
            json_ok=json_ok,
            api_route=getattr(provider, "last_api_route", "") or "",
            usage_input_tokens=uit,
            usage_output_tokens=uot,
            usage_total_tokens=utt,
            provider_ms=_Instrumented.last_ms,
            validator_ok=validator_ok,
            validator_errors=verrs,
            fallback=fallback,
            e2e_ms=e2e_ms,
            task_plan_v1_ok=plan_ok,
            task_plan_steps=steps,
            task_plan_summary=digest,
            mixed_non_task_preserved=mixed_ok,
            primary_domain=getattr(res.domain_result, "primary_domain", "") or "",
            notes=(res.notes or "")[:200],
        )
        rows.append(row)

    # 汇总
    n = len(rows)
    json_rate = sum(1 for r in rows if r.json_ok) / n
    val_rate = sum(1 for r in rows if r.validator_ok is True) / n
    fb_rate = sum(1 for r in rows if r.fallback) / n
    avg_e2e = sum(r.e2e_ms for r in rows) / n
    mixed_row = next((r for r in rows if r.name == "mixed_hospital"), None)
    mixed_metric = mixed_row.mixed_non_task_preserved if mixed_row else None

    return {
        "model": model,
        "rows": rows,
        "json_rate": json_rate,
        "val_rate": val_rate,
        "fb_rate": fb_rate,
        "avg_e2e": avg_e2e,
        "mixed_metric": mixed_metric,
        "responses_url": provider.responses_url,
        "chat_base_url": provider.chat_base_url,
    }


def main() -> None:
    import capabilities.voice.bridge.voice_long_input_model_output_validator as vmod
    from capabilities.voice.providers.qwen_external_long_input_model_provider import (
        create_qwen_external_long_input_provider_from_env,
        is_qwen_external_llm_configured,
    )

    if not is_qwen_external_llm_configured():
        print(
            "跳过：请设置 LUNA_EXTERNAL_LLM_PROVIDER=qwen 且配置 DASHSCOPE_API_KEY。",
            file=sys.stderr,
        )
        sys.exit(2)

    cfg = _cfg()
    base = create_qwen_external_long_input_provider_from_env(timeout_ms=cfg.model_timeout_ms)
    if base is None:
        print("无法构造 Qwen 外部 Provider。", file=sys.stderr)
        sys.exit(2)

    print("第一部分：速度诊断（同一套 smoke，对比模型）")
    print("")

    outcomes: List[Dict[str, Any]] = []
    for m in _selected_models():
        out = _run_one_model(base_provider=base, model=m)
        outcomes.append(out)

        print("A. 环境确认")
        print("  provider: QwenExternalLongInputModelProvider（阿里云百炼 OpenAI 兼容）")
        print("  model:", out["model"])
        print("  responses_url:", out["responses_url"])
        print("  chat_base_url:", out["chat_base_url"])
        print("")
        print("B. 四条输入逐条结果")
        print("---")

        rows: List[Row] = out["rows"]
        route_counts: Dict[str, int] = {}
        for r in rows:
            if r.json_ok and r.api_route:
                route_counts[r.api_route] = route_counts.get(r.api_route, 0) + 1

            print(f"[{r.name}]")
            print("  1) JSON 成功/失败:", "成功" if r.json_ok else "失败", f"(通道: {r.api_route or '—'})")
            print(
                "  2) validator 通过/失败:",
                "通过" if r.validator_ok is True else ("未执行" if r.validator_ok is None else "失败"),
            )
            if r.validator_errors:
                print("      errors:", r.validator_errors)
            print("  3) fallback 是/否:", "是" if r.fallback else "否")
            print("  4) task_plan_v1 有/无:", "有" if r.task_plan_v1_ok else "无", f"steps={r.task_plan_steps}")
            print("  5) 耗时 ms — provider:", round(r.provider_ms, 1), "e2e:", round(r.e2e_ms, 1))
            print(
                "  usage tokens:",
                {"input": r.usage_input_tokens, "output": r.usage_output_tokens, "total": r.usage_total_tokens},
            )
            if r.mixed_non_task_preserved is not None:
                print("  mixed non_task_payload 保留(不舒服):", r.mixed_non_task_preserved)
            print("  primary_domain:", r.primary_domain)
            print("  task_plan digest:", r.task_plan_summary)
            print("  notes:", r.notes)
            print("---")

        print("")
        print("C. 总汇总")
        print("  纯 JSON 成功率:", round(out["json_rate"] * 100, 1), "%")
        print("  validator 通过率（分母=4，未校验视为未过）:", round(out["val_rate"] * 100, 1), "%")
        print("  fallback 触发率:", round(out["fb_rate"] * 100, 1), "%")
        print("  平均耗时 ms (e2e):", round(out["avg_e2e"], 1))
        print("  mixed 下 non_task_payload 是否保留:", out["mixed_metric"])
        print("  JSON 成功样本的 API 通道计数:", route_counts or "—")

        ok_rows = sum(1 for r in rows if not r.fallback)
        all_val = all(r.validator_ok is True for r in rows)
        mixed_failed = out["mixed_metric"] is False
        # 验收阈值（写死）：avg_e2e_ms > 15000 则不适合前台主链
        slow = float(out["avg_e2e"]) > 15_000.0
        if ok_rows >= 3 and all_val and not mixed_failed and not slow:
            verdict = "1）可作为当前主选方案继续推进"
        elif ok_rows >= 2:
            verdict = "2）可用但仍需诊断优化"
        else:
            verdict = "3）当前仍不可用"

        print("")
        print("D. 一句话结论")
        print(" ", verdict)
        print("")
        print("========================================")
        print("")

    # 对比总表（速度诊断）
    print("对比汇总（速度诊断）")
    for out in outcomes:
        print(
            f"- model={out['model']} avg_e2e_ms={round(out['avg_e2e'],1)} "
            f"json={round(out['json_rate']*100,1)}% val={round(out['val_rate']*100,1)}% "
            f"fallback={round(out['fb_rate']*100,1)}% mixed_preserve={out['mixed_metric']}"
        )


if __name__ == "__main__":
    main()

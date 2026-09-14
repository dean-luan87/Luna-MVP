#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M2：长语音任务拆解真实场景验证（主备 bundle：qwen-plus → qwen-turbo）。

前置（与主链一致）：
- export LUNA_EXTERNAL_LLM_PROVIDER=qwen
- export DASHSCOPE_API_KEY=...
- 建议：export LUNA_QWEN_USE_PRIMARY_BACKUP=1（与运行时习惯对齐；本脚本仍直接构造主备 bundle，不绕过 M1）

不改 schema / validator / builder / fallback 定义；仅观测与落盘。
"""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _cfg():
    from capabilities.voice.config.voice_long_input_parse_config import VoiceLongInputParseConfig

    return VoiceLongInputParseConfig(
        parse_mode="model_preferred_with_rule_fallback",
        enable_model_adapter=True,
        model_timeout_ms=int(os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS", "120000")),
        fallback_to_rule_on_timeout=True,
        fallback_to_rule_on_validation_error=True,
        max_task_candidates=3,
        allow_non_task_payload=True,
    )


@dataclass(frozen=True)
class M2Case:
    scenario: str
    case_id: str
    text: str
    session_hint: str = ""
    mixed_keywords: Tuple[str, ...] = ()
    min_plan_steps: int = 0
    expect_unsupported: bool = False


# 三类场景 × 各 4 条 = 12 条固定 case
M2_CASES: Tuple[M2Case, ...] = (
    # --- 场景 1：长句 + mixed + 情绪/身体背景 ---
    M2Case(
        scenario="A_mixed_emotion",
        case_id="A1_nav_body_mood",
        text=(
            "我今天从早上开始就有点头晕，心情也不太好，但还是得出门。"
            "先帮我导航到最近的综合医院，我想挂个内科，路上如果堵车就提醒我换条路。"
        ),
        mixed_keywords=("头晕",),
    ),
    M2Case(
        scenario="A_mixed_emotion",
        case_id="A2_nav_stress_gym",
        text=(
            "这周工作压力特别大，晚上想去健身房放松一下。"
            "先导航到万象城那家带泳池的健身房，最好走地面路线，我晕车不想走高架。"
        ),
        mixed_keywords=("压力",),
    ),
    M2Case(
        scenario="A_mixed_emotion",
        case_id="A3_airport_sleepy",
        text=(
            "昨晚只睡了四个小时，现在有点犯困，但下午有航班。"
            "帮我导航到首都机场T3，走机场高速，顺便提醒我哪里有服务区可以喝咖啡。"
        ),
        mixed_keywords=("困",),
    ),
    M2Case(
        scenario="A_mixed_emotion",
        case_id="A4_restaurant_social",
        text=(
            "我有点社交紧张，不太想排队太久。"
            "帮我找一家安静一点的日料店并导航过去，最好有包厢，不要商场里太吵的那种。"
        ),
        mixed_keywords=("紧张",),
    ),
    # --- 场景 2：强切后续接（hint 模拟前段收口）---
    M2Case(
        scenario="B_continuation",
        case_id="B1_airport_resume",
        session_hint="【前一段 ASR 超时收口】用户之前说：想去首都机场 T3。",
        text="刚才话没说完，请帮我走机场高速，避开拥堵路段，到航站楼出发层下车。",
    ),
    M2Case(
        scenario="B_continuation",
        case_id="B2_mall_resume",
        session_hint="【前一段已收口】用户上一轮已确认：导航到朝阳大悦城。",
        text="补充一下，我要停地下停车场 B2 区，入口靠近主路那边。",
    ),
    M2Case(
        scenario="B_continuation",
        case_id="B3_two_step_resume",
        session_hint="【前一段收口】用户之前说：先去商场吃饭。",
        text="接着刚才的，吃完饭再去旁边的电影院，帮我按这个顺序导航。",
    ),
    M2Case(
        scenario="B_continuation",
        case_id="B4_hospital_resume",
        session_hint="【前一段收口】用户说过身体不舒服，要去医院。",
        text="继续说：改成去三甲急诊，我现在胸口有点闷，尽量选最快的路线。",
        mixed_keywords=("闷",),
    ),
    # --- 场景 3：连续多轮承接（单轮一条 + hint 携带上轮语义）---
    M2Case(
        scenario="C_multi_round",
        case_id="C1_round1_base",
        text="先帮我导航到最近的加油站，我要加满油。",
        min_plan_steps=1,
    ),
    M2Case(
        scenario="C_multi_round",
        case_id="C2_round2_add_condition",
        session_hint="【上一轮】用户已请求：导航到最近的加油站。",
        text="对了，要支持扫码支付的那种，顺便看看顺路有没有便利店。",
        min_plan_steps=1,
    ),
    M2Case(
        scenario="C_multi_round",
        case_id="C3_round3_correct",
        session_hint="【上一轮】用户在补充加油站与便利店需求。",
        text="算了，改成先去便利店买水，再去加油站，顺序换一下。",
        min_plan_steps=1,
    ),
    M2Case(
        scenario="C_multi_round",
        case_id="C4_round4_clarify_style",
        session_hint="【上一轮】用户调整了任务顺序。",
        text="如果便利店和加油站不在一个方向，就只做导航到加油站，别的先不管。",
        min_plan_steps=1,
    ),
)


@dataclass
class Row:
    scenario: str
    case_id: str
    text: str
    session_hint: str
    json_ok: bool = False
    validator_ok: Optional[bool] = None
    validator_errors: List[str] = field(default_factory=list)
    fallback: bool = False
    mixed_preserved: Optional[bool] = None
    mixed_note: str = ""
    primary_domain: str = ""
    clarification_needed: bool = False
    rejection_needed: bool = False
    task_plan_steps: int = 0
    selected_provider_model_id: str = ""
    backup_provider_used: bool = False
    provider_switch_reason: str = ""
    api_route: str = ""
    e2e_ms: float = 0.0
    notes: str = ""


def _task_plan_steps(plan: Any) -> int:
    if plan is None:
        return 0
    try:
        eo = getattr(plan, "execution_order", None) or []
        return len(eo)
    except Exception:
        return -1


def _non_task_text(res: Any) -> str:
    p = getattr(res, "non_task_payload", None)
    if not p or not getattr(p, "exists", False):
        return ""
    segs = getattr(p, "segments", None) or []
    return " ".join((getattr(s, "content", "") or "") for s in segs)


def _bundle_json_trace(provider: Any) -> Any:
    """包装 bundle，记录 model 层是否返回结构化 JSON（非 None）。"""

    class _W:
        def __init__(self, inner: Any) -> None:
            self._inner = inner
            self.last_json_ok = False

        def parse_long_input(self, text: str, *, session_hint: str = "", request_id: str = ""):
            r = self._inner.parse_long_input(text, session_hint=session_hint, request_id=request_id)
            self.last_json_ok = r is not None
            return r

        def __getattr__(self, name: str) -> Any:
            return getattr(self._inner, name)

    return _W(provider)


def _run_all() -> Tuple[List[Row], Dict[str, Any]]:
    import capabilities.voice.bridge.voice_long_input_model_output_validator as vmod
    from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1
    from capabilities.voice.providers.qwen_long_voice_primary_backup_provider import (
        create_qwen_long_voice_task_parse_provider_bundle_from_env,
    )
    from capabilities.voice.providers.qwen_external_long_input_model_provider import is_qwen_external_llm_configured

    if not is_qwen_external_llm_configured():
        print("跳过：请设置 LUNA_EXTERNAL_LLM_PROVIDER=qwen 且配置 DASHSCOPE_API_KEY。", file=sys.stderr)
        sys.exit(2)

    cfg = _cfg()
    raw_bundle = create_qwen_long_voice_task_parse_provider_bundle_from_env(timeout_ms=cfg.model_timeout_ms)
    if raw_bundle is None:
        print("无法构造主备 Provider bundle。", file=sys.stderr)
        sys.exit(2)

    provider = _bundle_json_trace(raw_bundle)

    _last_vr: Dict[str, Any] = {"vr": None}
    _orig_val: Callable[..., Any] = vmod.validate_model_structured_output

    def _val_wrap(s: Any, *, cfg: Any):
        r = _orig_val(s, cfg=cfg)
        _last_vr["vr"] = r
        return r

    vmod.validate_model_structured_output = _val_wrap  # type: ignore[assignment]

    rows: List[Row] = []

    for c in M2_CASES:
        _last_vr["vr"] = None
        provider.last_json_ok = False  # type: ignore[attr-defined]

        t0 = time.perf_counter()
        res = run_long_input_task_planning_v1(
            c.text,
            session_hint=c.session_hint,
            parse_config=cfg,
            model_provider=provider,
        )
        e2e_ms = (time.perf_counter() - t0) * 1000.0

        vr = _last_vr["vr"]
        validator_ok: Optional[bool] = None
        verrs: List[str] = []
        if vr is not None:
            validator_ok = bool(vr.ok)
            verrs = list(vr.errors or [])

        json_ok = bool(getattr(provider, "last_json_ok", False))
        fallback = not (json_ok and validator_ok is True)
        steps = _task_plan_steps(res.task_plan_v1)

        mixed_ok: Optional[bool] = None
        mixed_note = ""
        if c.mixed_keywords:
            blob = _non_task_text(res)
            ok = any(k in blob for k in c.mixed_keywords)
            mixed_ok = ok
            mixed_note = f"keywords={c.mixed_keywords} hit={ok} non_task_blob_len={len(blob)}"

        sw_reason = str(getattr(raw_bundle, "provider_switch_reason", "") or "")

        rows.append(
            Row(
                scenario=c.scenario,
                case_id=c.case_id,
                text=c.text,
                session_hint=c.session_hint,
                json_ok=json_ok,
                validator_ok=validator_ok,
                validator_errors=verrs,
                fallback=fallback,
                mixed_preserved=mixed_ok,
                mixed_note=mixed_note,
                primary_domain=getattr(res.domain_result, "primary_domain", "") or "",
                clarification_needed=bool(res.clarification_needed),
                rejection_needed=bool(res.rejection_needed),
                task_plan_steps=steps,
                selected_provider_model_id=str(getattr(raw_bundle, "selected_provider_model_id", "") or ""),
                backup_provider_used=bool(getattr(raw_bundle, "backup_provider_used", False)),
                provider_switch_reason=sw_reason,
                api_route=str(getattr(raw_bundle, "last_api_route", "") or ""),
                e2e_ms=e2e_ms,
                notes=(res.notes or "")[:240],
            )
        )

    n = len(rows)
    json_rate = sum(1 for r in rows if r.json_ok) / n
    val_rate = sum(1 for r in rows if r.validator_ok is True) / n
    fb_rate = sum(1 for r in rows if r.fallback) / n
    mixed_rows = [r for r in rows if r.mixed_preserved is not None]
    mixed_preserve_rate = (
        sum(1 for r in mixed_rows if r.mixed_preserved is True) / len(mixed_rows) if mixed_rows else None
    )
    primary_used = sum(1 for r in rows if not r.backup_provider_used)
    backup_used = sum(1 for r in rows if r.backup_provider_used)
    switch_rate = backup_used / n if n else 0.0
    reason_counts: Dict[str, int] = {}
    for r in rows:
        if r.backup_provider_used:
            key = (r.provider_switch_reason or "unknown").split(";")[0].strip() or "unknown"
            reason_counts[key] = reason_counts.get(key, 0) + 1

    summary = {
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "LUNA_QWEN_USE_PRIMARY_BACKUP": os.getenv("LUNA_QWEN_USE_PRIMARY_BACKUP", ""),
        "primary_model": "qwen-plus",
        "backup_model": "qwen-turbo",
        "bundle": "create_qwen_long_voice_task_parse_provider_bundle_from_env",
        "n_cases": n,
        "json_rate": json_rate,
        "val_rate": val_rate,
        "fallback_rate": fb_rate,
        "mixed_preserve_rate": mixed_preserve_rate,
        "primary_used_count": primary_used,
        "backup_used_count": backup_used,
        "provider_switch_rate": switch_rate,
        "provider_switch_reason_breakdown": reason_counts,
        "avg_ms": sum(r.e2e_ms for r in rows) / n,
    }
    return rows, summary


def _print_report(rows: List[Row], summary: Dict[str, Any]) -> None:
    print("")
    print("========== M2 真实场景 smoke 报告 ==========")
    print("")
    print("A. 环境确认")
    print("  LUNA_QWEN_USE_PRIMARY_BACKUP:", os.getenv("LUNA_QWEN_USE_PRIMARY_BACKUP", "(未设置)"))
    print("  主模型:", summary["primary_model"], "| 备模型:", summary["backup_model"])
    print("  bundle:", summary["bundle"])
    print("  ts_utc:", summary["ts_utc"])
    print("")
    print("B. 逐 case 结果")
    for r in rows:
        print(f"  [{r.scenario} / {r.case_id}]")
        print("    JSON:", "ok" if r.json_ok else "fail", "| validator:", r.validator_ok, "| fallback:", r.fallback)
        if r.validator_errors:
            print("    validator_errors:", r.validator_errors[:3])
        print("    mixed:", r.mixed_preserved, r.mixed_note or "")
        print(
            "    provider:",
            r.selected_provider_model_id,
            "backup_used=",
            r.backup_provider_used,
            "reason=",
            r.provider_switch_reason or "—",
        )
        print("    primary_domain:", r.primary_domain, "steps:", r.task_plan_steps, "e2e_ms:", round(r.e2e_ms, 1))
        print("    api_route:", r.api_route or "—")
        print("---")
    print("")
    print("C. 汇总")
    print("  json_rate:", round(summary["json_rate"] * 100, 2), "%")
    print("  val_rate:", round(summary["val_rate"] * 100, 2), "%")
    print("  fallback_rate:", round(summary["fallback_rate"] * 100, 2), "%")
    if summary["mixed_preserve_rate"] is not None:
        print("  mixed_preserve_rate (有 keyword 的 case):", round(summary["mixed_preserve_rate"] * 100, 2), "%")
    print("  avg_ms:", round(summary["avg_ms"], 1))
    print("  primary_used_count:", summary["primary_used_count"], "backup_used_count:", summary["backup_used_count"])
    print("  provider_switch_rate:", round(summary["provider_switch_rate"] * 100, 2), "%")
    print("  provider_switch_reason_breakdown:", summary["provider_switch_reason_breakdown"])
    print("")
    print("D. 说明：语义误判需人工扫 notes/domain；本脚本只做 keyword 级 mixed 抽检。")
    print("E. 结论占位：请结合分时段 benchmark 与业务阈值在评审会勾选「可默认 / 显式开关 / 不适合」。")
    print("")


def main() -> None:
    out_dir = ROOT / "logs"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = out_dir / f"smoke_qwen_long_voice_realworld_m2_{ts}.json"

    rows, summary = _run_all()
    payload = {
        "summary": summary,
        "rows": [asdict(r) for r in rows],
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("结果已写入:", json_path)
    _print_report(rows, summary)


if __name__ == "__main__":
    main()

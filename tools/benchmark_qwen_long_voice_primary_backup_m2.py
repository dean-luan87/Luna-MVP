#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M2：主备 bundle 分时段稳定性抽测（20～50 轮可配）。

使用与 smoke M2 相同的主备 Provider（不得单独直测 plus/turbo 作为本轮主结论）。

环境：
- export LUNA_EXTERNAL_LLM_PROVIDER=qwen
- export DASHSCOPE_API_KEY=...
- 建议：export LUNA_QWEN_USE_PRIMARY_BACKUP=1
- 分时段标签：export LUNA_BENCH_TIME_SLOT=day 或 night（仅写入结果 JSON，便于两轮对比）

- export LUNA_BENCH_ITERS=30  （默认 20，约 20×4=80 次 API，可按配额调低）
"""

from __future__ import annotations

import json
import os
import statistics
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# 与 smoke M2 对齐：4 条代表性输入循环，覆盖 mixed / unsupported / task / short
BENCH_SMOKES: Tuple[Tuple[str, str], ...] = (
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
        model_timeout_ms=int(os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS", "120000")),
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


def _bundle_json_trace(inner: Any) -> Any:
    class _W:
        def __init__(self, i: Any) -> None:
            self._inner = i
            self.last_json_ok = False

        def parse_long_input(self, text: str, *, session_hint: str = "", request_id: str = ""):
            r = self._inner.parse_long_input(text, session_hint=session_hint, request_id=request_id)
            self.last_json_ok = r is not None
            return r

        def __getattr__(self, name: str) -> Any:
            return getattr(self._inner, name)

    return _W(inner)


@dataclass
class Sample:
    name: str
    iter_idx: int
    e2e_ms: float
    json_ok: bool
    validator_ok: Optional[bool]
    fallback: bool
    mixed_preserved: Optional[bool]
    backup_provider_used: bool
    provider_switch_reason: str
    selected_provider_model_id: str


def main() -> None:
    import capabilities.voice.bridge.voice_long_input_model_output_validator as vmod
    from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1
    from capabilities.voice.providers.qwen_long_voice_primary_backup_provider import (
        create_qwen_long_voice_task_parse_provider_bundle_from_env,
    )
    from capabilities.voice.providers.qwen_external_long_input_model_provider import (
        is_qwen_external_llm_configured,
        qwen_external_ab_profile_label,
    )

    if not is_qwen_external_llm_configured():
        print("跳过：请设置 LUNA_EXTERNAL_LLM_PROVIDER=qwen 且配置 DASHSCOPE_API_KEY。", file=sys.stderr)
        sys.exit(2)

    iters = int(os.getenv("LUNA_BENCH_ITERS", "20"))
    time_slot = (os.getenv("LUNA_BENCH_TIME_SLOT") or "").strip() or "unspecified"
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

    samples: List[Sample] = []
    reason_breakdown: Dict[str, int] = {}

    print("benchmark_qwen_long_voice_primary_backup_m2")
    print("  time_slot:", time_slot)
    print("  iters:", iters, "x", len(BENCH_SMOKES), "cases")
    print("  provider_ab_profile:", qwen_external_ab_profile_label())
    print("  LUNA_QWEN_USE_PRIMARY_BACKUP:", os.getenv("LUNA_QWEN_USE_PRIMARY_BACKUP", "(未设置)"))
    print("---")
    sys.stdout.flush()

    for i in range(iters):
        for name, text in BENCH_SMOKES:
            _last_vr["vr"] = None
            provider.last_json_ok = False  # type: ignore[attr-defined]

            t0 = time.perf_counter()
            res = run_long_input_task_planning_v1(text, parse_config=cfg, model_provider=provider)
            e2e_ms = (time.perf_counter() - t0) * 1000.0

            vr = _last_vr["vr"]
            validator_ok: Optional[bool] = None
            if vr is not None:
                validator_ok = bool(vr.ok)

            json_ok = bool(getattr(provider, "last_json_ok", False))
            fallback = not (json_ok and validator_ok is True)

            mixed_ok: Optional[bool] = None
            if name == "mixed_hospital":
                mixed_ok = bool(
                    res.non_task_payload
                    and res.non_task_payload.exists
                    and any("不舒服" in (s.content or "") for s in (res.non_task_payload.segments or []))
                )

            bu = bool(getattr(raw_bundle, "backup_provider_used", False))
            pr = str(getattr(raw_bundle, "provider_switch_reason", "") or "")
            mid = str(getattr(raw_bundle, "selected_provider_model_id", "") or "")
            if bu:
                rk = pr.split(";")[0] if pr else "unknown"
                reason_breakdown[rk] = reason_breakdown.get(rk, 0) + 1

            samples.append(
                Sample(
                    name=name,
                    iter_idx=i,
                    e2e_ms=e2e_ms,
                    json_ok=json_ok,
                    validator_ok=validator_ok,
                    fallback=fallback,
                    mixed_preserved=mixed_ok,
                    backup_provider_used=bu,
                    provider_switch_reason=pr,
                    selected_provider_model_id=mid,
                )
            )

        print(f"progress: {i + 1}/{iters}")
        sys.stdout.flush()

    xs = [s.e2e_ms for s in samples]
    n = len(samples)
    json_rate = sum(1 for s in samples if s.json_ok) / n
    val_rate = sum(1 for s in samples if s.validator_ok is True) / n
    fb_rate = sum(1 for s in samples if s.fallback) / n
    primary_used = sum(1 for s in samples if not s.backup_provider_used)
    backup_used = sum(1 for s in samples if s.backup_provider_used)
    switch_rate = backup_used / n if n else 0.0

    mixed_samples = [s for s in samples if s.name == "mixed_hospital"]
    mpr = (
        sum(1 for s in mixed_samples if s.mixed_preserved is True) / len(mixed_samples) if mixed_samples else None
    )

    per_case: Dict[str, Dict[str, float]] = {}
    for name, _ in BENCH_SMOKES:
        sub = [s.e2e_ms for s in samples if s.name == name]
        if not sub:
            continue
        per_case[name] = {
            "avg_ms": statistics.mean(sub),
            "p95_ms": _p95(sub),
            "n": float(len(sub)),
        }

    summary = {
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "time_slot": time_slot,
        "LUNA_QWEN_USE_PRIMARY_BACKUP": os.getenv("LUNA_QWEN_USE_PRIMARY_BACKUP", ""),
        "iters": iters,
        "total_samples": n,
        "primary_model": "qwen-plus",
        "backup_model": "qwen-turbo",
        "avg_ms": statistics.mean(xs),
        "p95_ms": _p95(xs),
        "json_rate": json_rate,
        "val_rate": val_rate,
        "fallback_rate": fb_rate,
        "mixed_preserve_rate": mpr,
        "primary_used_count": primary_used,
        "backup_used_count": backup_used,
        "provider_switch_rate": switch_rate,
        "provider_switch_reason_breakdown": reason_breakdown,
        "per_case_ms": per_case,
    }

    out_dir = ROOT / "logs"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = out_dir / f"benchmark_qwen_long_voice_primary_backup_m2_{time_slot}_{ts}.json"
    json_path.write_text(
        json.dumps({"summary": summary, "samples": [asdict(s) for s in samples]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("")
    print("========== M2 分时段抽测汇总 ==========")
    print("结果已写入:", json_path)
    print("")
    print("A. 环境")
    print("  time_slot:", time_slot, "| ts_utc:", summary["ts_utc"])
    print("  primary:", summary["primary_model"], "| backup:", summary["backup_model"])
    print("")
    print("B. 全局")
    print("  avg_ms:", round(summary["avg_ms"], 1), "p95_ms:", round(summary["p95_ms"], 1))
    print("  json_rate:", round(json_rate, 4), "val_rate:", round(val_rate, 4), "fallback_rate:", round(fb_rate, 4))
    if mpr is not None:
        print("  mixed_preserve_rate (mixed_hospital):", round(mpr, 4))
    print("  primary_used_count:", primary_used, "backup_used_count:", backup_used)
    print("  provider_switch_rate:", round(switch_rate, 4))
    print("  provider_switch_reason_breakdown:", reason_breakdown)
    print("")
    print("C. 各 case avg/p95")
    for name, d in per_case.items():
        print(f"  {name}: avg_ms={d['avg_ms']:.1f} p95_ms={d['p95_ms']:.1f} n={int(d['n'])}")
    print("")
    if json_rate < 1.0:
        print("【警告】json_rate < 1.0：请检查 Key / 网络 / 配额后再做默认化决策。")


if __name__ == "__main__":
    main()

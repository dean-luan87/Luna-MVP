#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qwen-plus 默认态产品化：默认态回归脚本（V1）

目标：
- 只跑“当前默认态”（不改主链逻辑，不强行打开任何开关）
- 通过主入口 dispatch，输出固定 KPI，并落盘 logs/

说明：
- 默认态是否走模型链，取决于部署环境是否显式开启：
  - LUNA_QWEN_USE_PRIMARY_BACKUP=1（不开 prefilter）
  - 或 LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1（灰度态；本脚本不建议作为默认态回归使用）
- 因此本脚本会在产物里记录“实际生效的运行态观测”（selected_provider_model_id / prefilter_enabled / bundle_enabled）。
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
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _utc_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _p95(xs: List[float]) -> float:
    if not xs:
        return 0.0
    xs2 = sorted(xs)
    k = int((len(xs2) - 1) * 0.95)
    return float(xs2[k])


def _env_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in ("1", "true", "yes")


CASES: Tuple[Tuple[str, str], ...] = (
    ("task_two_steps", "先去商场，再找便利店买点吃的"),
    ("mixed_hospital", "我今天有点不舒服，先带我去最近的医院吧"),
    ("unsupported_register", "帮我自动挂号"),
    ("hospital_short", "带我去医院"),
)


@dataclass
class Row:
    iter_idx: int
    case_name: str
    text: str
    e2e_ms: float
    dispatch_type: str
    rejected_input: bool
    short_controlled_input: bool
    long_task_planning_input: bool
    selected_provider_model_id: str
    prefilter_enabled: bool
    bundle_enabled: bool
    parse_mode: str
    enable_model_adapter: bool
    used_model_chain: Optional[bool]
    fallback: Optional[bool]
    validator_ok: Optional[bool]
    rule_or_reject: Optional[bool]
    notes: str


def _make_event(*, text: str, request_id: str) -> Any:
    # 只构造 dispatcher 所需字段（本 repo 的 VoiceInputEvent 是 dataclass）
    from capabilities.voice.schemas.voice_input_event import VoiceInputEvent

    return VoiceInputEvent(
        event_id=request_id,
        request_id=request_id,
        session_id="default_regression",
        raw_text=text,
        normalized_text=text,
        wake_word_stripped=text,
        is_task_mode=True,
        source_type="regression",
        context_resume_hint="",
        router_decision="accept",
        metadata={},
    )


def _extract_kpis(res: Any) -> Tuple[Optional[bool], Optional[bool], Optional[bool]]:
    """
    best-effort：从 dispatch result / metadata 中提取 used_model_chain / fallback / validator_ok。
    不强依赖字段存在，缺失则 None。
    """
    md = getattr(res, "metadata", None) or {}
    used_model_chain = md.get("used_model_chain")
    fallback = md.get("fallback")
    validator_ok = md.get("validator_ok")

    def _b(x: Any) -> Optional[bool]:
        return bool(x) if isinstance(x, bool) else None

    return _b(used_model_chain), _b(fallback), _b(validator_ok)


def main() -> None:
    ap = argparse.ArgumentParser(description="qwen-plus 默认态回归脚本 V1（只跑当前默认态）")
    ap.add_argument("--iters", type=int, default=int(os.getenv("LUNA_DEFAULT_REGRESSION_ITERS", "3")))
    ap.add_argument("--out-dir", default=str(Path.cwd() / "logs"))
    args = ap.parse_args()

    from capabilities.voice.config.voice_long_input_parse_config import get_default_voice_long_input_parse_config
    from capabilities.voice.runtime.voice_final_text_dispatcher import dispatch_voice_final_text

    iters = int(args.iters)
    out_dir = Path(str(args.out_dir)).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = _utc_ts()
    parse_cfg = get_default_voice_long_input_parse_config()

    env_obs = {
        "LUNA_VOICE_ENABLE_PREFILTER_ROUTING": os.getenv("LUNA_VOICE_ENABLE_PREFILTER_ROUTING", ""),
        "LUNA_QWEN_USE_PRIMARY_BACKUP": os.getenv("LUNA_QWEN_USE_PRIMARY_BACKUP", ""),
        "LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG": os.getenv("LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG", ""),
        "LUNA_QWEN_MODEL_TIMEOUT_MS": os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS", ""),
    }

    rows: List[Row] = []
    for i in range(iters):
        for name, text in CASES:
            rid = f"default_reg_v1_{ts}_{i}_{name}"
            ev = _make_event(text=text, request_id=rid)

            t0 = time.perf_counter()
            res = dispatch_voice_final_text(ev)
            e2e = (time.perf_counter() - t0) * 1000.0

            md = getattr(res, "metadata", None) or {}
            routing = md.get("routing_observation") or {}
            selected = str(routing.get("selected_provider_model_id") or "")

            used_model_chain, fallback, validator_ok = _extract_kpis(res)

            # rule_or_reject_ratio 的分子：rule_only 或 reject
            dispatch_type = getattr(res, "dispatch_type", "") or ""
            rejected = bool(getattr(res, "rejected_input", False))
            short_in = bool(getattr(res, "short_controlled_input", False))
            long_in = bool(getattr(res, "long_task_planning_input", False))
            rule_or_reject = None
            if rejected:
                rule_or_reject = True
            elif long_in and ("rule_chain_only" in selected or selected.startswith("legacy_default")):
                rule_or_reject = True
            elif long_in:
                rule_or_reject = False

            rows.append(
                Row(
                    iter_idx=i,
                    case_name=name,
                    text=text,
                    e2e_ms=e2e,
                    dispatch_type=dispatch_type,
                    rejected_input=rejected,
                    short_controlled_input=short_in,
                    long_task_planning_input=long_in,
                    selected_provider_model_id=selected,
                    prefilter_enabled=_env_truthy("LUNA_VOICE_ENABLE_PREFILTER_ROUTING"),
                    bundle_enabled=_env_truthy("LUNA_QWEN_USE_PRIMARY_BACKUP"),
                    parse_mode=parse_cfg.parse_mode,
                    enable_model_adapter=bool(parse_cfg.enable_model_adapter),
                    used_model_chain=used_model_chain,
                    fallback=fallback,
                    validator_ok=validator_ok,
                    rule_or_reject=rule_or_reject,
                    notes=str(getattr(res, "notes", "") or "")[:160],
                )
            )

    xs = [r.e2e_ms for r in rows] if rows else []
    json_rate = None
    val_rate = None
    fb_rate = None

    # 如果 metadata 里有 used_model_chain / validator_ok / fallback，则按布尔统计；否则留空
    if any(r.used_model_chain is not None for r in rows):
        json_rate = sum(1 for r in rows if r.used_model_chain is True) / len(rows)
    if any(r.validator_ok is not None for r in rows):
        val_rate = sum(1 for r in rows if r.validator_ok is True) / len(rows)
    if any(r.fallback is not None for r in rows):
        fb_rate = sum(1 for r in rows if r.fallback is True) / len(rows)

    rule_or_reject_ratio = None
    rr_vals = [r.rule_or_reject for r in rows if isinstance(r.rule_or_reject, bool)]
    if rr_vals:
        rule_or_reject_ratio = sum(1 for x in rr_vals if x) / len(rr_vals)

    payload: Dict[str, Any] = {
        "schema": "luna.voice.runtime_default_regression.v1",
        "utc_ts": ts,
        "env_observation": env_obs,
        "default_parse_config": {
            "parse_mode": parse_cfg.parse_mode,
            "enable_model_adapter": bool(parse_cfg.enable_model_adapter),
            "model_timeout_ms": int(parse_cfg.model_timeout_ms),
        },
        "kpi": {
            "json_rate": json_rate,
            "val_rate": val_rate,
            "fallback_rate": fb_rate,
            "avg_ms": round(statistics.mean(xs), 1) if xs else 0.0,
            "p95_ms": round(_p95(xs), 1),
            "rule_or_reject_ratio": rule_or_reject_ratio,
        },
        "rows": [asdict(r) for r in rows],
    }

    out_json = out_dir / f"runtime_default_regression_v1_{ts}.json"
    out_md = out_dir / f"runtime_default_regression_v1_{ts}.md"

    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines: List[str] = []
    md_lines.append("## qwen-plus 默认态回归（V1）")
    md_lines.append("")
    md_lines.append("### 1) KPI（best-effort；缺失则为 null）")
    md_lines.append("```json")
    md_lines.append(json.dumps(payload["kpi"], ensure_ascii=False, indent=2))
    md_lines.append("```")
    md_lines.append("")
    md_lines.append("### 2) 默认态观测（环境与选路）")
    md_lines.append("```json")
    md_lines.append(json.dumps(payload["env_observation"], ensure_ascii=False, indent=2))
    md_lines.append("```")
    md_lines.append("")
    md_lines.append("### 3) 说明")
    md_lines.append("- 本脚本不改任何开关；KPI 反映当前环境下的“真实默认态”。")
    md_lines.append("- 若 `json_rate/val_rate/fallback_rate` 为 null，说明当前默认态未输出相应观测字段（或走 rule_only），属于正常现象。")
    out_md.write_text("\n".join(md_lines), encoding="utf-8")

    print("wrote:", out_json)
    print("wrote:", out_md)


if __name__ == "__main__":
    main()


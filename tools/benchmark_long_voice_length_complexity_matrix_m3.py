#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3：长短语音「时长 × 复杂度」矩阵 benchmark — qwen-plus 与 qwen-turbo 单模型对比（不使用主备 bundle）。

前置：
  export LUNA_EXTERNAL_LLM_PROVIDER=qwen
  export DASHSCOPE_API_KEY=...

可选：
  export LUNA_M3_CASES_JSON=/path/to/voice_long_voice_length_complexity_cases_m3.json
  export LUNA_M3_MODEL_PLUS=qwen-plus          # 默认；可改为 qwen3.6-plus 等与百炼一致的模型名
  export LUNA_M3_MODEL_TURBO=qwen-turbo        # 默认；快档亦可试 qwen-flash / qwen3.5-flash 等
  python3 tools/benchmark_long_voice_length_complexity_matrix_m3.py --dry-run   # 只校验 case 与矩阵，不调 API

不改 schema / validator / builder / fallback；仅观测与落盘。
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DEFAULT_CASES = ROOT / "configs" / "voice" / "voice_long_voice_length_complexity_cases_m3.json"
PROMPT_PLUS = ROOT / "capabilities" / "voice" / "config" / "prompts" / "voice_long_input_parse_v1_1_prompt_qwen_plus.md"
PROMPT_TURBO = ROOT / "capabilities" / "voice" / "config" / "prompts" / "voice_long_input_parse_v1_1_prompt_qwen_turbo.md"


def _prompt_path_for_model(model: str) -> Path:
    """与模型名对齐分层提示：turbo / flash 走 turbo 稿；其余（含 qwen-plus、qwen3.6-plus）走 plus 稿。"""
    m = (model or "").lower()
    if "turbo" in m or "flash" in m:
        return PROMPT_TURBO
    return PROMPT_PLUS

from shared.schemas.task_domain_v1 import UNSUPPORTED_OR_REJECT  # noqa: E402


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


def _task_plan_steps(plan: Any) -> int:
    if plan is None:
        return 0
    try:
        return len(getattr(plan, "execution_order", None) or [])
    except Exception:
        return -1


def _non_task_blob(res: Any) -> str:
    p = getattr(res, "non_task_payload", None)
    if not p or not getattr(p, "exists", False):
        return ""
    segs = getattr(p, "segments", None) or []
    return " ".join((getattr(s, "content", "") or "") for s in segs)


def _usage_digest(u: Any) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    if not isinstance(u, dict):
        return None, None, None
    it, ot, tt = u.get("input_tokens"), u.get("output_tokens"), u.get("total_tokens")
    return (
        int(it) if isinstance(it, (int, float)) else None,
        int(ot) if isinstance(ot, (int, float)) else None,
        int(tt) if isinstance(tt, (int, float)) else None,
    )


@dataclass
class CaseRow:
    case_id: str
    length_tier: str
    complexity: str
    text_len: int
    model: str
    json_ok: bool = False
    validator_ok: Optional[bool] = None
    fallback: bool = False
    mixed_preserved: Optional[bool] = None
    primary_domain: str = ""
    task_plan_v1_ok: bool = False
    task_plan_steps: int = 0
    clarification_needed: bool = False
    rejection_needed: bool = False
    provider_ms: float = 0.0
    e2e_ms: float = 0.0
    usage_in: Optional[int] = None
    usage_out: Optional[int] = None
    usage_total: Optional[int] = None
    api_route: str = ""
    notes: str = ""
    heuristic_unsupported_misexecute: bool = False
    heuristic_mixed_lost: bool = False
    heuristic_multistep_flattened: bool = False


def _eval_heuristics(case: Dict[str, Any], res: Any, row: CaseRow) -> None:
    """仅在模型返回结构化 JSON 时计算；否则为规则链兜底，启发式不能代表 plus/turbo。"""
    if not row.json_ok:
        return
    h = case.get("heuristic") or {}
    kws = case.get("mixed_keywords") or []
    blob = _non_task_blob(res)
    if kws:
        row.mixed_preserved = any(k in blob for k in kws)
        row.heuristic_mixed_lost = not row.mixed_preserved
    min_steps = h.get("expect_min_plan_steps")
    if min_steps is not None and int(min_steps) >= 2:
        row.heuristic_multistep_flattened = row.task_plan_steps < int(min_steps)
    if h.get("unsupported_risk"):
        dom = row.primary_domain
        bad_exec = row.task_plan_v1_ok and row.task_plan_steps > 0 and dom not in (UNSUPPORTED_OR_REJECT, "")
        if dom and dom != UNSUPPORTED_OR_REJECT and bad_exec:
            row.heuristic_unsupported_misexecute = True


def _run_matrix(*, cases: List[Dict[str, Any]], model: str, base: Any) -> List[CaseRow]:
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

    class _Ins(QwenExternalLongInputModelProvider):
        last_ms: float = 0.0
        last_json_ok: bool = False

        def parse_long_input(self, text: str, *, session_hint: str = "", request_id: str = ""):
            t0 = time.perf_counter()
            r = super().parse_long_input(text, session_hint=session_hint, request_id=request_id)
            self.last_ms = (time.perf_counter() - t0) * 1000.0
            self.last_json_ok = r is not None
            return r

    provider = _Ins(
        api_key=base.api_key,
        model=model,
        responses_url=base.responses_url,
        chat_base_url=base.chat_base_url,
        prompt_path=_prompt_path_for_model(model),
        timeout_ms=base.timeout_ms,
        max_output_tokens=base.max_output_tokens,
        schema_strict=base.schema_strict,
        prefer_responses_api=base.prefer_responses_api,
        responses_http_timeout_sec=base.responses_http_timeout_sec,
        chat_http_timeout_sec=base.chat_http_timeout_sec,
    )

    rows: List[CaseRow] = []
    n_cases = len(cases)
    for idx, c in enumerate(cases, start=1):
        cid = str(c["id"])
        text = str(c["text"])
        _last_vr["vr"] = None
        provider.last_ms = 0.0  # type: ignore[attr-defined]
        provider.last_json_ok = False  # type: ignore[attr-defined]

        print(f"  [{model}] {idx}/{n_cases} {cid} …", flush=True)
        t0 = time.perf_counter()
        res = run_long_input_task_planning_v1(text, parse_config=cfg, model_provider=provider, request_id=f"m3_{model}_{cid}")
        e2e = (time.perf_counter() - t0) * 1000.0

        vr = _last_vr["vr"]
        vok = bool(vr.ok) if vr is not None else None
        json_ok = bool(getattr(provider, "last_json_ok", False))
        fallback = not (json_ok and vok is True)
        steps = _task_plan_steps(res.task_plan_v1)
        uit, uot, utt = _usage_digest(getattr(provider, "last_usage", None))

        row = CaseRow(
            case_id=cid,
            length_tier=str(c["length_tier"]),
            complexity=str(c["complexity"]),
            text_len=len(text),
            model=model,
            json_ok=json_ok,
            validator_ok=vok,
            fallback=fallback,
            mixed_preserved=None,
            primary_domain=getattr(res.domain_result, "primary_domain", "") or "",
            task_plan_v1_ok=res.task_plan_v1 is not None,
            task_plan_steps=steps,
            clarification_needed=bool(res.clarification_needed),
            rejection_needed=bool(res.rejection_needed),
            provider_ms=float(getattr(provider, "last_ms", 0.0)),
            e2e_ms=e2e,
            usage_in=uit,
            usage_out=uot,
            usage_total=utt,
            api_route=str(getattr(provider, "last_api_route", "") or ""),
            notes=(res.notes or "")[:180],
        )
        _eval_heuristics(c, res, row)
        rows.append(row)

    vmod.validate_model_structured_output = _orig_val  # type: ignore[assignment]
    return rows


def _agg(rows: List[CaseRow], key_fn: Callable[[CaseRow], str]) -> Dict[str, Dict[str, Any]]:
    buckets: Dict[str, List[CaseRow]] = defaultdict(list)
    for r in rows:
        buckets[key_fn(r)].append(r)
    out: Dict[str, Dict[str, Any]] = {}
    for k, xs in sorted(buckets.items()):
        n = len(xs)
        ok_json = [x for x in xs if x.json_ok]
        n_m = len(ok_json)
        out[k] = {
            "n": n,
            "json_rate": sum(1 for x in xs if x.json_ok) / n,
            "val_rate": sum(1 for x in xs if x.validator_ok is True) / n,
            "fallback_rate": sum(1 for x in xs if x.fallback) / n,
            "avg_e2e_ms": statistics.mean([x.e2e_ms for x in xs]),
            "avg_provider_ms": statistics.mean([x.provider_ms for x in xs]),
            "mixed_hit_rate": (
                (
                    sum(1 for x in mixed_xs if x.mixed_preserved is True) / len(mixed_xs)
                    if (mixed_xs := [x for x in ok_json if x.mixed_preserved is not None])
                    else None
                )
            ),
            # 仅统计「模型曾返回 JSON」的样本，避免 401 全程走规则链时误报
            "unsupported_misexec_rate": (
                sum(1 for x in ok_json if x.heuristic_unsupported_misexecute) / n_m if n_m else None
            ),
            "multistep_flatten_rate": (
                sum(1 for x in ok_json if x.heuristic_multistep_flattened) / n_m if n_m else None
            ),
        }
    return out


def _p95(xs: List[float]) -> float:
    if not xs:
        return 0.0
    s = sorted(xs)
    return float(s[int((len(s) - 1) * 0.95)])


def _fmt_h(v: Any) -> str:
    return f"{v:.2f}" if isinstance(v, (int, float)) and v is not None else "—"


def _print_summary(plus_rows: List[CaseRow], turbo_rows: List[CaseRow]) -> None:
    def by_len(r: CaseRow) -> str:
        return r.length_tier

    def by_cpx(r: CaseRow) -> str:
        return r.complexity

    for label, fn in [("按时长档 L1-L5", by_len), ("按复杂度档 C1-C5", by_cpx)]:
        print(f"\n### 汇总：{label}")
        ap = _agg(plus_rows, fn)
        at = _agg(turbo_rows, fn)
        keys = sorted(set(ap.keys()) | set(at.keys()))
        for k in keys:
            p, t = ap.get(k), at.get(k)
            print(f"  [{k}]")
            if p:
                print(
                    f"    plus:  json={p['json_rate']:.2f} val={p['val_rate']:.2f} fb={p['fallback_rate']:.2f} "
                    f"avg_e2e={p['avg_e2e_ms']:.0f}ms mis_unsup={_fmt_h(p['unsupported_misexec_rate'])} "
                    f"flat={_fmt_h(p['multistep_flatten_rate'])}"
                )
            if t:
                print(
                    f"    turbo: json={t['json_rate']:.2f} val={t['val_rate']:.2f} fb={t['fallback_rate']:.2f} "
                    f"avg_e2e={t['avg_e2e_ms']:.0f}ms mis_unsup={_fmt_h(t['unsupported_misexec_rate'])} "
                    f"flat={_fmt_h(t['multistep_flatten_rate'])}"
                )


def _verdict_hint(plus_rows: List[CaseRow], turbo_rows: List[CaseRow]) -> str:
    """控制台提示：最终结论须人工写入附录（三类之一）。"""
    def ok(rs: List[CaseRow]) -> Tuple[float, float, float]:
        n = len(rs)
        if not n:
            return 0.0, 0.0, 0.0
        return (
            sum(1 for r in rs if r.json_ok) / n,
            sum(1 for r in rs if r.validator_ok is True) / n,
            sum(1 for r in rs if r.fallback) / n,
        )

    pj, pv, pf = ok(plus_rows)
    tj, tv, tf = ok(turbo_rows)
    if pj == 0.0 and tj == 0.0:
        return (
            "【无效跑批】全程 json_rate=0：模型未形成「Provider 返回非空结构化对象」的命中统计，"
            "或存在超时/解析失败/校验失败后全程规则链兜底；请对照 stderr 中 validation_failed、timeout 等再跑。"
            "在排障完成前，本次汇总不宜直接用于 plus/turbo 分档结论。"
        )
    if pj < 0.95 or pv < 0.95:
        return "3）当前还不适合进入分档设计阶段（plus 基线未稳，先排障）"
    if tj >= 0.95 and tv >= 0.95 and tf == 0.0 and pj == pv == 1.0:
        return "1）已足够支撑进入「简单走 turbo、复杂走 plus」的分档设计阶段（请结合 heuristic 误判率人工确认）"
    if tj < 0.92 or tv < 0.92:
        return "2）结论仍不够清晰，需要补更多矩阵 case 或加长 L4/L5 覆盖"
    return "2）结论仍不够清晰，需对照各档 mixed/unsupported heuristic 人工裁定"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只加载 case，不调 API")
    ap.add_argument("--cases-json", type=Path, default=None, help="覆盖默认 case JSON 路径")
    ap.add_argument(
        "--model-plus",
        default=None,
        help="Plus 档模型名（默认 env LUNA_M3_MODEL_PLUS 或 qwen-plus）",
    )
    ap.add_argument(
        "--model-turbo",
        default=None,
        help="Turbo/快档模型名（默认 env LUNA_M3_MODEL_TURBO 或 qwen-turbo）",
    )
    args = ap.parse_args()

    model_plus = (args.model_plus or os.getenv("LUNA_M3_MODEL_PLUS") or "qwen-plus").strip()
    model_turbo = (args.model_turbo or os.getenv("LUNA_M3_MODEL_TURBO") or "qwen-turbo").strip()

    path = Path(args.cases_json or os.getenv("LUNA_M3_CASES_JSON") or DEFAULT_CASES)
    data = json.loads(path.read_text(encoding="utf-8"))
    cases: List[Dict[str, Any]] = data["cases"]
    if len(cases) != 25:
        print(f"警告：期望 25 条 case，实际 {len(cases)}", file=sys.stderr)

    if args.dry_run:
        print("dry-run OK:", path)
        print("cases:", len(cases))
        for L in ["L1", "L2", "L3", "L4", "L5"]:
            for C in ["C1", "C2", "C3", "C4", "C5"]:
                assert any(c["id"] == f"{L}_{C}" for c in cases), f"missing {L}_{C}"
        print("matrix 5x5 完整")
        sys.exit(0)

    from capabilities.voice.providers.qwen_external_long_input_model_provider import (
        create_qwen_external_long_input_provider_from_env,
        is_qwen_external_llm_configured,
        qwen_external_ab_profile_label,
    )

    if not is_qwen_external_llm_configured():
        print("跳过：请设置 LUNA_EXTERNAL_LLM_PROVIDER=qwen 且 DASHSCOPE_API_KEY。", file=sys.stderr)
        sys.exit(2)

    base = create_qwen_external_long_input_provider_from_env(timeout_ms=_cfg().model_timeout_ms)
    if base is None:
        print("无法构造 Provider。", file=sys.stderr)
        sys.exit(2)

    print("M3 matrix benchmark | cases=", len(cases), "| profile=", qwen_external_ab_profile_label())
    print("models（无主备 bundle）: plus=", model_plus, "| turbo=", model_turbo)
    sys.stdout.flush()

    plus_rows = _run_matrix(cases=cases, model=model_plus, base=base)
    pj0 = sum(1 for r in plus_rows if r.json_ok) / len(plus_rows) if plus_rows else 0.0
    if pj0 == 0.0:
        print(
            f"\n【警告】{model_plus} 本轮 json_rate=0：多为模型链未返回可解析结构化对象，或超时/解析失败后走规则链；"
            "请对照本终端与日志中的 timeout、model_output_validation_failed。",
            file=sys.stderr,
        )
    print("plus 完成，开始 turbo…")
    sys.stdout.flush()
    turbo_rows = _run_matrix(cases=cases, model=model_turbo, base=base)
    tj0 = sum(1 for r in turbo_rows if r.json_ok) / len(turbo_rows) if turbo_rows else 0.0
    if tj0 == 0.0:
        print(
            f"\n【警告】{model_turbo} 本轮 json_rate=0：若 stderr 出现 illegal_secondary_domain 等，"
            "多为模型输出的 secondary_domains 与 PRIMARY_DOMAIN_V1 枚举不一致导致校验失败并回退规则链。",
            file=sys.stderr,
        )

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = ROOT / "logs"
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_plus = model_plus.replace("/", "_").replace(".", "_")
    safe_turbo = model_turbo.replace("/", "_").replace(".", "_")
    out_path = out_dir / f"benchmark_long_voice_length_complexity_matrix_m3_{safe_plus}_{safe_turbo}_{ts}.json"
    payload = {
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "cases_path": str(path),
        "model_plus": model_plus,
        "model_turbo": model_turbo,
        "plus_rows": [asdict(r) for r in plus_rows],
        "turbo_rows": [asdict(r) for r in turbo_rows],
        "agg_by_length_plus": _agg(plus_rows, lambda r: r.length_tier),
        "agg_by_length_turbo": _agg(turbo_rows, lambda r: r.length_tier),
        "agg_by_complexity_plus": _agg(plus_rows, lambda r: r.complexity),
        "agg_by_complexity_turbo": _agg(turbo_rows, lambda r: r.complexity),
        "global_plus": {
            "json_rate": sum(1 for r in plus_rows if r.json_ok) / len(plus_rows),
            "val_rate": sum(1 for r in plus_rows if r.validator_ok is True) / len(plus_rows),
            "fallback_rate": sum(1 for r in plus_rows if r.fallback) / len(plus_rows),
            "avg_e2e_ms": statistics.mean([r.e2e_ms for r in plus_rows]),
            "p95_e2e_ms": _p95([r.e2e_ms for r in plus_rows]),
        },
        "global_turbo": {
            "json_rate": sum(1 for r in turbo_rows if r.json_ok) / len(turbo_rows),
            "val_rate": sum(1 for r in turbo_rows if r.validator_ok is True) / len(turbo_rows),
            "fallback_rate": sum(1 for r in turbo_rows if r.fallback) / len(turbo_rows),
            "avg_e2e_ms": statistics.mean([r.e2e_ms for r in turbo_rows]),
            "p95_e2e_ms": _p95([r.e2e_ms for r in turbo_rows]),
        },
        "verdict_hint": _verdict_hint(plus_rows, turbo_rows),
        "model_json_effective": pj0 > 0.0 and tj0 > 0.0,
        "plus_json_rate": pj0,
        "turbo_json_rate": tj0,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n结果已写入:", out_path)
    _print_summary(plus_rows, turbo_rows)
    print("\n【附录用】机器提示（非最终决策）:", payload["verdict_hint"])
    print("请将 logs JSON 汇总填入 docs/.../LUNA_VOICE_LONG_VOICE_LENGTH_COMPLEXITY_BENCHMARK_APPENDIX_M3.md")


if __name__ == "__main__":
    main()

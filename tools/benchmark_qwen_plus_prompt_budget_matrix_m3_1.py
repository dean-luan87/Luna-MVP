#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen Prompt Budget 实验 v1（M3.1）：仅替换 qwen-plus 的 instructions 文件，不改 schema / validator / builder / fallback / provider 实现。

前置：
  export LUNA_EXTERNAL_LLM_PROVIDER=qwen
  export DASHSCOPE_API_KEY=...

可选：
  export LUNA_PROMPT_BUDGET_QWEN_MODEL=qwen-plus   # 默认 qwen-plus
  export LUNA_PROMPT_BUDGET_CASES_JSON=/path/to/qwen_prompt_budget_cases_m3_1.json
  python3 tools/benchmark_qwen_plus_prompt_budget_matrix_m3_1.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DEFAULT_CASES = ROOT / "configs" / "voice" / "qwen_prompt_budget_cases_m3_1.json"
PROMPT_P2_STANDARD = ROOT / "capabilities" / "voice" / "config" / "prompts" / "voice_long_input_parse_v1_1_prompt_qwen_plus.md"
PROMPT_P1 = ROOT / "capabilities" / "voice" / "config" / "prompts" / "prompt_budget_m3_1" / "voice_long_input_parse_v1_1_prompt_qwen_plus_p1_minimal.md"
PROMPT_P3 = ROOT / "capabilities" / "voice" / "config" / "prompts" / "prompt_budget_m3_1" / "voice_long_input_parse_v1_1_prompt_qwen_plus_p3_enhanced.md"
PROMPT_P4 = ROOT / "capabilities" / "voice" / "config" / "prompts" / "prompt_budget_m3_1" / "voice_long_input_parse_v1_1_prompt_qwen_plus_p4_heavy.md"

BUDGET_PROMPT_PATH: Dict[str, Path] = {
    "P1": PROMPT_P1,
    "P2": PROMPT_P2_STANDARD,
    "P3": PROMPT_P3,
    "P4": PROMPT_P4,
}

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


def _p95(xs: List[float]) -> float:
    if not xs:
        return 0.0
    s = sorted(xs)
    return float(s[int((len(s) - 1) * 0.95)])


@dataclass
class CaseRow:
    case_id: str
    budget: str
    complexity_tier: str
    text_len: int
    mixed_case: bool
    unsupported_risk: bool
    json_ok: bool = False
    validator_ok: Optional[bool] = None
    fallback: bool = False
    mixed_preserved: Optional[bool] = None
    primary_domain: str = ""
    task_plan_v1_ok: bool = False
    task_plan_steps: int = 0
    provider_ms: float = 0.0
    e2e_ms: float = 0.0
    usage_in: Optional[int] = None
    usage_out: Optional[int] = None
    usage_total: Optional[int] = None
    api_route: str = ""
    notes: str = ""
    heuristic_mixed_lost: bool = False
    heuristic_multistep_flattened: bool = False
    heuristic_unsupported_misexecute: bool = False


def _eval_heuristics(case: Dict[str, Any], res: Any, row: CaseRow) -> None:
    if not row.json_ok:
        return
    h = case.get("heuristic") or {}
    kws = h.get("mixed_keywords") or []
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


def _run_cases(
    *,
    cases: List[Dict[str, Any]],
    base: Any,
    model: str,
) -> List[CaseRow]:
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
        def parse_long_input(self, text: str, *, session_hint: str = "", request_id: str = ""):
            t0 = time.perf_counter()
            r = super().parse_long_input(text, session_hint=session_hint, request_id=request_id)
            self.last_ms = (time.perf_counter() - t0) * 1000.0  # type: ignore[attr-defined]
            self.last_json_ok = r is not None  # type: ignore[attr-defined]
            return r

    rows: List[CaseRow] = []
    provider: Optional[_Ins] = None
    last_budget: Optional[str] = None
    n = len(cases)

    for idx, c in enumerate(cases, start=1):
        budget = str(c["budget"])
        if budget not in BUDGET_PROMPT_PATH:
            raise ValueError(f"unknown budget: {budget}")
        pp = BUDGET_PROMPT_PATH[budget]
        if not pp.is_file():
            raise FileNotFoundError(f"prompt file missing: {pp}")

        if budget != last_budget:
            provider = _Ins(
                api_key=base.api_key,
                model=model,
                responses_url=base.responses_url,
                chat_base_url=base.chat_base_url,
                prompt_path=pp,
                timeout_ms=base.timeout_ms,
                max_output_tokens=base.max_output_tokens,
                schema_strict=base.schema_strict,
                prefer_responses_api=base.prefer_responses_api,
                responses_http_timeout_sec=base.responses_http_timeout_sec,
                chat_http_timeout_sec=base.chat_http_timeout_sec,
            )
            last_budget = budget

        assert provider is not None
        cid = str(c["id"])
        text = str(c["text"])
        _last_vr["vr"] = None
        provider.last_ms = 0.0  # type: ignore[attr-defined]
        provider.last_json_ok = False  # type: ignore[attr-defined]

        print(f"  [{budget}] {idx}/{n} {cid} …", flush=True)
        t0 = time.perf_counter()
        res = run_long_input_task_planning_v1(
            text, parse_config=cfg, model_provider=provider, request_id=f"pb_{cid}"
        )
        e2e = (time.perf_counter() - t0) * 1000.0

        vr = _last_vr["vr"]
        vok = bool(vr.ok) if vr is not None else None
        json_ok = bool(getattr(provider, "last_json_ok", False))
        fallback = not (json_ok and vok is True)
        steps = _task_plan_steps(res.task_plan_v1)
        uit, uot, utt = _usage_digest(getattr(provider, "last_usage", None))

        row = CaseRow(
            case_id=cid,
            budget=budget,
            complexity_tier=str(c["complexity_tier"]),
            text_len=len(text),
            mixed_case=bool(c.get("mixed")),
            unsupported_risk=bool(c.get("unsupported_risk")),
            json_ok=json_ok,
            validator_ok=vok,
            fallback=fallback,
            mixed_preserved=None,
            primary_domain=getattr(res.domain_result, "primary_domain", "") or "",
            task_plan_v1_ok=res.task_plan_v1 is not None,
            task_plan_steps=steps,
            provider_ms=float(getattr(provider, "last_ms", 0.0)),
            e2e_ms=e2e,
            usage_in=uit,
            usage_out=uot,
            usage_total=utt,
            api_route=str(getattr(provider, "last_api_route", "") or ""),
            notes=(res.notes or "")[:120],
        )
        _eval_heuristics(c, res, row)
        rows.append(row)

    vmod.validate_model_structured_output = _orig_val  # type: ignore[assignment]
    return rows


def _cell_stats(xs: List[CaseRow]) -> Dict[str, Any]:
    n = len(xs)
    if not n:
        return {}
    e2e = [r.e2e_ms for r in xs]
    mixed_json = [r for r in xs if r.mixed_case and r.json_ok]
    mixed_ok = [r for r in mixed_json if r.mixed_preserved is True]
    mixed_lost = [r for r in mixed_json if r.heuristic_mixed_lost]
    flat_rows = [r for r in xs if r.json_ok and r.heuristic_multistep_flattened]

    def _mean_usage(key: str) -> Optional[float]:
        vals = [getattr(r, key) for r in xs]
        nums = [v for v in vals if isinstance(v, (int, float))]
        return statistics.mean(nums) if nums else None

    return {
        "n": n,
        "json_rate": sum(1 for r in xs if r.json_ok) / n,
        "val_rate": sum(1 for r in xs if r.validator_ok is True) / n,
        "fallback_rate": sum(1 for r in xs if r.fallback) / n,
        "avg_e2e_ms": statistics.mean(e2e),
        "p95_e2e_ms": _p95(e2e),
        "avg_usage_in": _mean_usage("usage_in"),
        "avg_usage_out": _mean_usage("usage_out"),
        "avg_usage_total": _mean_usage("usage_total"),
        "mixed_preserve_rate": (len(mixed_ok) / len(mixed_json)) if mixed_json else None,
        "mixed_lost_count": len(mixed_lost),
        "multistep_flatten_count": len(flat_rows),
        "unsupported_misexec_count": sum(1 for r in xs if r.heuristic_unsupported_misexecute),
    }


def _print_matrix(rows: List[CaseRow]) -> None:
    budgets = ["P1", "P2", "P3", "P4"]
    tiers = ["C1", "C2", "C3"]
    print("\n### 矩阵：复杂度(行) × Prompt Budget(列)")
    print("  单元格：json / val / fb | avg_ms p95_ms | mixed保留(仅 mixed case) | flat数")
    for tier in tiers:
        print(f"\n  [{tier}]")
        parts = []
        for b in budgets:
            xs = [r for r in rows if r.budget == b and r.complexity_tier == tier]
            st = _cell_stats(xs)
            mp = st.get("mixed_preserve_rate")
            mps = f"{mp:.2f}" if isinstance(mp, (int, float)) else "—"
            parts.append(
                f"{b}: j={st['json_rate']:.2f} v={st['val_rate']:.2f} fb={st['fallback_rate']:.2f} | "
                f"avg={st['avg_e2e_ms']:.0f} p95={st['p95_e2e_ms']:.0f} | mix={mps} | flat={st['multistep_flatten_count']}"
            )
        for p in parts:
            print("    ", p)

    print("\n### 按 Budget 汇总（9 条/档）")
    for b in budgets:
        xs = [r for r in rows if r.budget == b]
        st = _cell_stats(xs)
        mp = st.get("mixed_preserve_rate")
        mps = f"{mp:.2f}" if isinstance(mp, (int, float)) else "—"
        print(
            f"  {b}: j={st['json_rate']:.2f} v={st['val_rate']:.2f} fb={st['fallback_rate']:.2f} | "
            f"avg={st['avg_e2e_ms']:.0f} p95={st['p95_e2e_ms']:.0f} | mix={mps} | "
            f"flat={st['multistep_flatten_count']} unsup_bad={st['unsupported_misexec_count']}"
        )

    _print_red_flags(rows)


def _print_red_flags(rows: List[CaseRow]) -> None:
    """结构稳定性优先：明显劣化打印警告。"""
    baseline = [r for r in rows if r.budget == "P2"]
    if len(baseline) < 9:
        return
    b_st = _cell_stats(baseline)
    print("\n### 相对 P2 标准档的劣化提示（结构优先）")
    for b in ["P1", "P3", "P4"]:
        xs = [r for r in rows if r.budget == b]
        st = _cell_stats(xs)
        msgs = []
        if st["json_rate"] < b_st["json_rate"] - 0.05:
            msgs.append(f"json_rate 低于 P2 超 5pt ({st['json_rate']:.2f} vs {b_st['json_rate']:.2f})")
        if st["val_rate"] < b_st["val_rate"] - 0.05:
            msgs.append(f"val_rate 低于 P2 超 5pt ({st['val_rate']:.2f} vs {b_st['val_rate']:.2f})")
        if st["fallback_rate"] > b_st["fallback_rate"] + 0.05:
            msgs.append(f"fallback_rate 高于 P2 超 5pt ({st['fallback_rate']:.2f} vs {b_st['fallback_rate']:.2f})")
        if st["mixed_lost_count"] > b_st["mixed_lost_count"]:
            msgs.append(f"mixed 丢失条数多于 P2 ({st['mixed_lost_count']} vs {b_st['mixed_lost_count']})")
        if msgs:
            print(f"  【{b}】", "; ".join(msgs))
        else:
            print(f"  【{b}】相对 P2 未发现上述阈值级劣化")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只校验 case 与 prompt 文件存在")
    ap.add_argument("--cases-json", type=Path, default=None)
    args = ap.parse_args()

    path = Path(args.cases_json or os.getenv("LUNA_PROMPT_BUDGET_CASES_JSON") or DEFAULT_CASES)
    data = json.loads(path.read_text(encoding="utf-8"))
    cases: List[Dict[str, Any]] = data["cases"]
    budgets = data.get("budgets") or ["P1", "P2", "P3", "P4"]
    tiers = data.get("complexity_tiers") or ["C1", "C2", "C3"]

    for b, p in BUDGET_PROMPT_PATH.items():
        if not p.is_file():
            print(f"错误：缺少 prompt 文件 {p}", file=sys.stderr)
            sys.exit(2)

    if args.dry_run:
        if len(cases) != 36:
            print(f"警告：期望 36 条 case，实际 {len(cases)}", file=sys.stderr)
        by_b: Dict[str, int] = defaultdict(int)
        by_t: Dict[str, int] = defaultdict(int)
        for c in cases:
            by_b[str(c["budget"])] += 1
            by_t[str(c["complexity_tier"])] += 1
        print("dry-run OK:", path)
        print("cases:", len(cases), "| per budget:", dict(by_b), "| per tier:", dict(by_t))
        print("P2 →", PROMPT_P2_STANDARD)
        print("P1/P3/P4 → prompt_budget_m3_1/")
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

    model = (os.getenv("LUNA_PROMPT_BUDGET_QWEN_MODEL") or "qwen-plus").strip()

    print("Qwen Prompt Budget matrix M3.1 | model=", model, "| profile=", qwen_external_ab_profile_label())
    print("cases=", len(cases), "| budgets=", ",".join(budgets))
    sys.stdout.flush()

    rows = _run_cases(cases=cases, base=base, model=model)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = ROOT / "logs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"benchmark_qwen_plus_prompt_budget_m3_1_{ts}.json"

    matrix: Dict[str, Any] = {}
    for b in budgets:
        matrix[b] = {}
        for t in tiers:
            xs = [r for r in rows if r.budget == b and r.complexity_tier == t]
            matrix[b][t] = _cell_stats(xs)

    payload = {
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "cases_path": str(path),
        "model": model,
        "ab_profile": qwen_external_ab_profile_label(),
        "rows": [asdict(r) for r in rows],
        "matrix_budget_x_complexity": matrix,
        "budget_totals": {b: _cell_stats([r for r in rows if r.budget == b]) for b in budgets},
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n结果已写入:", out_path)
    _print_matrix(rows)
    print("\n请将汇总填入 docs/architecture/voice/LUNA_VOICE_QWEN_PROMPT_BUDGET_APPENDIX_M3_1.md")


if __name__ == "__main__":
    main()

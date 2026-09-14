#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
risk_interrupt_v1 试点观测聚合工具（V1）

输入：一到多个 JSONL trace 文件（每行一个 JSON 对象，形如 {"type": "...", "data": {...}}）
输出：
- logs/analyze_risk_interrupt_v1_pilot_<UTC>.json
- logs/analyze_risk_interrupt_v1_pilot_<UTC>.md

聚合维度（必须）：
- 按 request_id
- 按 pilot path（Level2A preempt-before-submit / Level2B cancel+replace pending-only）
- 按 reason
- 按 terminal state（尽量从 request_runtime/playback_runtime 终态推断）
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


PREEMPT_REASON = "risk_interrupt_v1_level2_pilot_preempt_before_submit"
CANCEL_REPLACE_EVAL_REASON = "risk_interrupt_v1_cancel_replace_pilot_evaluated"
PILOT_STATE_TRANSITION_TYPE = "pilot_state_transition"


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _read_jsonl(path: Path) -> Iterable[Tuple[int, Dict[str, Any]]]:
    try:
        txt = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    out: List[Tuple[int, Dict[str, Any]]] = []
    for idx, ln in enumerate(txt.splitlines(), start=1):
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append((idx, json.loads(ln)))
        except Exception:
            # 忽略坏行，但保持可运行
            continue
    return out


@dataclass
class RequestAggregate:
    request_id: str
    # pilot path facts
    preempt: Optional[Dict[str, Any]] = None
    cancel_replace_eval: Optional[Dict[str, Any]] = None
    # request/playback terminal hints
    request_terminal_event: Optional[str] = None
    request_terminal_reason: Optional[str] = None
    playback_terminal_event: Optional[str] = None
    # bookkeeping
    events_seen: int = 0
    sources: List[Dict[str, Any]] = field(default_factory=list)  # {file, line, type, reason}

    def pilot_path(self) -> str:
        # 注意：一个 request_id 可能同时出现 preempt 与 cancel_replace_eval（因为实现里会无条件写 eval 观测）
        if self.cancel_replace_eval and bool((self.cancel_replace_eval.get("metadata") or {}).get("cancel_replace_on")):
            return "level2b_cancel_replace_pending_only"
        if self.preempt:
            return "level2a_preempt_before_submit"
        return "none_or_level1"

    def cancel_replace_chain_closed(self) -> bool:
        md = (self.cancel_replace_eval or {}).get("metadata") or {}
        return bool(md.get("cancel_replace_chain_closed"))

    def fallback_to_preempt(self) -> bool:
        md = (self.cancel_replace_eval or {}).get("metadata") or {}
        return bool(md.get("fallback_to_preempt_before_submit"))

    def replacement_request_id(self) -> str:
        md = (self.cancel_replace_eval or {}).get("metadata") or {}
        return str(md.get("replacement_request_id") or "")


def _upsert_agg(m: Dict[str, RequestAggregate], rid: str) -> RequestAggregate:
    if rid not in m:
        m[rid] = RequestAggregate(request_id=rid)
    return m[rid]


def analyze(paths: List[Path]) -> Dict[str, Any]:
    by_request: Dict[str, RequestAggregate] = {}
    total_events = 0
    state_transitions: List[Dict[str, Any]] = []

    for p in paths:
        for line_no, row in _read_jsonl(p):
            total_events += 1
            typ = row.get("type")
            data = row.get("data") if isinstance(row.get("data"), dict) else {}
            if typ == PILOT_STATE_TRANSITION_TYPE:
                state_transitions.append(
                    {
                        "file": str(p),
                        "line": line_no,
                        "timestamp": data.get("timestamp"),
                        "transition": data.get("transition"),
                        "reason": data.get("reason"),
                        "related_request_id": data.get("related_request_id"),
                        "metadata": data.get("metadata") or {},
                    }
                )
                continue

            rid = str(data.get("request_id") or "").strip()
            if not rid:
                continue

            agg = _upsert_agg(by_request, rid)
            agg.events_seen += 1

            reason = str(data.get("reason") or "")
            agg.sources.append({"file": str(p), "line": line_no, "type": typ, "reason": reason})

            if typ == "output_decision":
                if reason == PREEMPT_REASON:
                    agg.preempt = data
                elif reason == CANCEL_REPLACE_EVAL_REASON:
                    agg.cancel_replace_eval = data
            elif typ == "request_runtime":
                ev = str(data.get("event") or "")
                if ev == "request_terminal_observed":
                    agg.request_terminal_event = ev
                    agg.request_terminal_reason = str(data.get("reason") or "")
            elif typ == "playback_runtime":
                ev = str(data.get("event") or "")
                if ev in ("playback_finished", "playback_failed", "playback_cancelled"):
                    agg.playback_terminal_event = ev

    # ---- metrics (按 request_id 聚合，而非按事件条数) ----
    reqs = list(by_request.values())

    preempt_before_submit_count = sum(1 for a in reqs if a.preempt is not None)

    cancel_replace_attempt_reqs = [
        a for a in reqs if a.cancel_replace_eval and bool((a.cancel_replace_eval.get("metadata") or {}).get("cancel_replace_on"))
    ]
    cancel_replace_attempt_count = len(cancel_replace_attempt_reqs)
    cancel_replace_chain_closed_count = sum(1 for a in cancel_replace_attempt_reqs if a.cancel_replace_chain_closed())
    fallback_to_preempt_before_submit_count = sum(1 for a in cancel_replace_attempt_reqs if a.fallback_to_preempt())

    # 由 pilot_state_transition 显式事件统计（按“事件条数”，因为它本身就是“回退动作发生过”的事实）
    fallback_to_level1_count = sum(1 for t in state_transitions if str(t.get("transition")) == "level2a_to_level1")
    fallback_to_level0_count = sum(1 for t in state_transitions if str(t.get("transition")) == "any_to_level0")

    # high/critical 与 prompt/confirmation 目标数：基于 preempt metadata（当前 cancel+replace eval 没带这些字段）
    high_critical_trigger_count = 0
    prompt_confirmation_target_count = 0
    for a in reqs:
        if a.preempt:
            md = a.preempt.get("metadata") or {}
            lv = str(md.get("risk_level") or "").lower()
            cat = str(md.get("preempted_output_category") or "")
            if lv in ("high", "critical"):
                high_critical_trigger_count += 1
            if cat in ("prompt", "confirmation"):
                prompt_confirmation_target_count += 1
        if a.cancel_replace_eval and bool((a.cancel_replace_eval.get("metadata") or {}).get("cancel_replace_on")):
            md2 = a.cancel_replace_eval.get("metadata") or {}
            lv2 = str(md2.get("risk_level") or "").lower()
            cat2 = str(md2.get("target_output_category") or "")
            if lv2 in ("high", "critical"):
                high_critical_trigger_count += 1
            if cat2 in ("prompt", "confirmation"):
                prompt_confirmation_target_count += 1

    # ---- sample export ----
    success_samples: List[Dict[str, Any]] = []
    fallback_samples: List[Dict[str, Any]] = []
    suspicious_samples: List[Dict[str, Any]] = []

    # success: preempt hit OR cancel+replace chain closed
    for a in reqs:
        if a.preempt is not None:
            md = a.preempt.get("metadata") or {}
            success_samples.append(
                {
                    "request_id": a.request_id,
                    "pilot_path": "level2a_preempt_before_submit",
                    "risk_level": md.get("risk_level"),
                    "preempted_output_category": md.get("preempted_output_category"),
                }
            )
        elif a.cancel_replace_eval and bool((a.cancel_replace_eval.get("metadata") or {}).get("cancel_replace_on")) and a.cancel_replace_chain_closed():
            md = a.cancel_replace_eval.get("metadata") or {}
            success_samples.append(
                {
                    "request_id": a.request_id,
                    "pilot_path": "level2b_cancel_replace_pending_only",
                    "replacement_request_id": md.get("replacement_request_id"),
                }
            )

    # fallback: cancel+replace attempt but chain not closed OR explicit fallback_to_preempt
    for a in cancel_replace_attempt_reqs:
        md = a.cancel_replace_eval.get("metadata") or {}
        if (not a.cancel_replace_chain_closed()) or a.fallback_to_preempt():
            fallback_samples.append(
                {
                    "request_id": a.request_id,
                    "pilot_path": "level2b_cancel_replace_pending_only",
                    "cancel_replace_chain_closed": md.get("cancel_replace_chain_closed"),
                    "fallback_to_preempt_before_submit": md.get("fallback_to_preempt_before_submit"),
                    "failure_reason": md.get("failure_reason"),
                }
            )

    # suspicious: 越界/缺字段/链不一致
    for a in reqs:
        if a.preempt is not None:
            md = a.preempt.get("metadata") or {}
            lv = str(md.get("risk_level") or "").lower()
            cat = str(md.get("preempted_output_category") or "")
            if lv not in ("high", "critical") or cat not in ("prompt", "confirmation"):
                suspicious_samples.append(
                    {
                        "request_id": a.request_id,
                        "pilot_path": "level2a_preempt_before_submit",
                        "problem": "preempt_out_of_bounds",
                        "risk_level": md.get("risk_level"),
                        "preempted_output_category": md.get("preempted_output_category"),
                    }
                )

        if a.cancel_replace_eval and bool((a.cancel_replace_eval.get("metadata") or {}).get("cancel_replace_on")):
            md = a.cancel_replace_eval.get("metadata") or {}
            # 试点 attempt 但 failure_reason 为空且链不闭合：优先人工复核（说明观测不足或实现异常）
            if (not a.cancel_replace_chain_closed()) and (not str(md.get("failure_reason") or "").strip()):
                suspicious_samples.append(
                    {
                        "request_id": a.request_id,
                        "pilot_path": "level2b_cancel_replace_pending_only",
                        "problem": "cancel_replace_unclosed_without_reason",
                    }
                )
            # 越界检查（与 preempt 同口径）
            lv = str(md.get("risk_level") or "").lower()
            cat = str(md.get("target_output_category") or "")
            if lv and lv not in ("high", "critical"):
                suspicious_samples.append(
                    {
                        "request_id": a.request_id,
                        "pilot_path": "level2b_cancel_replace_pending_only",
                        "problem": "cancel_replace_out_of_bounds_risk_level",
                        "risk_level": md.get("risk_level"),
                    }
                )
            if cat and cat not in ("prompt", "confirmation"):
                suspicious_samples.append(
                    {
                        "request_id": a.request_id,
                        "pilot_path": "level2b_cancel_replace_pending_only",
                        "problem": "cancel_replace_out_of_bounds_output_category",
                        "target_output_category": md.get("target_output_category"),
                    }
                )
            # replacement_request_id 赋值但 replacement 没看到 request_created（跨 request_id 链断）
            rep = a.replacement_request_id()
            if rep and rep not in by_request:
                suspicious_samples.append(
                    {
                        "request_id": a.request_id,
                        "pilot_path": "level2b_cancel_replace_pending_only",
                        "problem": "replacement_request_missing_in_trace",
                        "replacement_request_id": rep,
                    }
                )

    result: Dict[str, Any] = {
        "version": "v1",
        "generated_at_utc": _utc_stamp(),
        "inputs": [str(p) for p in paths],
        "stats": {
            "total_events_parsed": total_events,
            "distinct_request_ids": len(by_request),
        },
        "pilot_state_transitions": state_transitions[-200:],
        "metrics_by_request_id": {
            "preempt_before_submit_count": preempt_before_submit_count,
            "cancel_replace_attempt_count": cancel_replace_attempt_count,
            "cancel_replace_chain_closed_count": cancel_replace_chain_closed_count,
            "cancel_replace_chain_closed_rate": (
                (cancel_replace_chain_closed_count / cancel_replace_attempt_count) if cancel_replace_attempt_count else None
            ),
            "fallback_to_preempt_before_submit_count": fallback_to_preempt_before_submit_count,
            "fallback_to_level1_count": fallback_to_level1_count,
            "fallback_to_level0_count": fallback_to_level0_count,
            "high_critical_trigger_count": high_critical_trigger_count,
            "prompt_confirmation_target_count": prompt_confirmation_target_count,
        },
        "samples": {
            "success": success_samples[:50],
            "fallback": fallback_samples[:50],
            "suspicious": suspicious_samples[:50],
        },
        "notes": {
            "fallback_to_level1_level0": "fallback_to_level1/0 由 pilot_state_transition 显式事件统计（不猜、不推断）。",
            "cancel_replace_high_critical_prompt_confirmation": "cancel+replace eval 已携带 risk_level/target_output_category，可用于与 preempt 同口径越界检查与统计。",
        },
    }
    return result


def render_md(res: Dict[str, Any]) -> str:
    m = res["metrics_by_request_id"]
    lines: List[str] = []
    lines.append("# risk_interrupt_v1 试点观测聚合（V1）")
    lines.append("")
    lines.append(f"- generated_at_utc: `{res['generated_at_utc']}`")
    lines.append(f"- inputs: {', '.join(f'`{p}`' for p in res['inputs'])}")
    lines.append("")
    lines.append("## 指标（按 request_id 聚合）")
    lines.append("")
    for k in [
        "preempt_before_submit_count",
        "cancel_replace_attempt_count",
        "cancel_replace_chain_closed_count",
        "cancel_replace_chain_closed_rate",
        "fallback_to_preempt_before_submit_count",
        "fallback_to_level1_count",
        "fallback_to_level0_count",
        "high_critical_trigger_count",
        "prompt_confirmation_target_count",
    ]:
        lines.append(f"- **{k}**: `{m.get(k)}`")
    lines.append("")
    lines.append("## 样本导出（最多 50 条/类）")
    lines.append("")
    for key in ("success", "fallback", "suspicious"):
        lines.append(f"### {key}")
        lines.append("")
        arr = res["samples"].get(key, [])
        if not arr:
            lines.append("- (empty)")
            lines.append("")
            continue
        for it in arr:
            rid = it.get("request_id")
            path = it.get("pilot_path")
            extra = {k: v for k, v in it.items() if k not in ("request_id", "pilot_path")}
            lines.append(f"- `request_id={rid}` `pilot_path={path}` {json.dumps(extra, ensure_ascii=False)}")
        lines.append("")
    lines.append("## 备注")
    lines.append("")
    for k, v in (res.get("notes") or {}).items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        action="append",
        default=[],
        help="JSONL trace path; can be repeated. If omitted, use $LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL or logs/*.jsonl",
    )
    ap.add_argument("--out_dir", default="logs", help="output directory (default: logs)")
    args = ap.parse_args()

    paths: List[Path] = []
    for s in args.input:
        paths.append(Path(s))
    if not paths:
        envp = os.getenv("LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL", "").strip()
        if envp:
            paths = [Path(envp)]
        else:
            paths = sorted(Path("logs").glob("*.jsonl"))

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = _utc_stamp()
    out_json = out_dir / f"analyze_risk_interrupt_v1_pilot_{stamp}.json"
    out_md = out_dir / f"analyze_risk_interrupt_v1_pilot_{stamp}.md"

    res = analyze(paths)
    out_json.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out_md.write_text(render_md(res), encoding="utf-8")

    print(str(out_md))


if __name__ == "__main__":
    main()


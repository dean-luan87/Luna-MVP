#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3.5.4b mixed 边界专项验证：只跑 C1_mixed_nav / C7_mixed_sleep_park_nav

目标：坐实 day/night 与 mixed 边界是否可复现，并回答：
1) 掉档是否可复现
2) 是否主要发生在 day
3) non_task_payload 是否缺失
4) mixed 关键词是否未完整落槽（all keywords 是否都命中）
5) 是否与路由模型（turbo / plus）强相关

不改语音骨架、不改 prefilter/prompt；仅增强 benchmark 观测字段。
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
from typing import Any, Dict, List, Optional, Tuple

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


def _non_task_payload_exists(res: Any) -> bool:
    p = getattr(res, "non_task_payload", None)
    if not p:
        return False
    return bool(getattr(p, "exists", False))


def _mixed_keyword_hit_report(expected: List[str], blob: str) -> Tuple[List[str], List[str]]:
    """
    返回：
    - found：blob 内命中的关键词列表
    - missing：blob 内未命中的关键词列表
    """
    if not expected:
        return [], []
    found = [k for k in expected if k in blob]
    missing = [k for k in expected if k not in blob]
    return found, missing


def _timeout_hint(dispatch_notes: str, long_notes: str) -> bool:
    blob = f"{dispatch_notes or ''} {long_notes or ''}".lower()
    return "timeout" in blob or "timed out" in blob


@dataclass
class Row:
    time_slot: str
    round_idx: int
    case_id: str
    bucket: str
    routing_suggestion: str
    selected_provider_model_id: str
    used_model_chain: bool
    validator_ok: Optional[bool]
    fallback: bool
    mixed_preserved: Optional[bool]
    mixed_preserved_all: Optional[bool]
    expected_mixed_keywords: List[str]
    non_task_payload_exists: bool
    mixed_keywords_found: List[str]
    mixed_keywords_missing: List[str]
    e2e_ms: float
    backup_provider_used: bool
    provider_switch_reason: str
    timeout_hint: bool


def _git_head() -> str:
    try:
        return (
            subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except Exception:
        return ""


def _pause_stop(
    *,
    val_rate: float,
    fallback_rate: float,
    mixed_preserve_rate: Optional[float],
    rule_ratio: float,
    mixed_preserve_min: float,
    rule_reject_max_ratio: float,
) -> Tuple[Dict[str, bool], bool]:
    pause_checks = {
        "val_rate_lt_1": val_rate < 1.0,
        "fallback_rate_gt_0": fallback_rate > 0.0,
        "mixed_preserve_below_min": (
            mixed_preserve_rate is not None and mixed_preserve_rate < float(mixed_preserve_min)
        ),
        "rule_or_reject_ratio_high": rule_ratio > float(rule_reject_max_ratio),
    }
    pause_stop = any(pause_checks.values())
    return pause_checks, pause_stop


def _metrics_from_rows(
    rows: List[Row],
    *,
    mixed_preserve_min: float,
    rule_reject_max_ratio: float,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, bool], bool, List[Dict[str, Any]]]:
    n = len(rows)
    route_counts: Dict[str, int] = {"route_to_turbo": 0, "route_to_plus": 0, "route_to_rule_or_reject": 0}
    e2e_all = [r.e2e_ms for r in rows]
    sel_counter: Counter[str] = Counter()
    complex_turbo: List[Dict[str, Any]] = []

    for r in rows:
        sug = r.routing_suggestion
        if sug in route_counts:
            route_counts[sug] += 1
        if r.selected_provider_model_id:
            sel_counter[r.selected_provider_model_id] += 1
        if r.bucket == "complex" and sug == "route_to_turbo":
            complex_turbo.append(
                {"case_id": r.case_id, "bucket": r.bucket, "routing_suggestion": sug, "time_slot": r.time_slot}
            )

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

    pause_checks, pause_stop = _pause_stop(
        val_rate=val_rate,
        fallback_rate=fallback_rate,
        mixed_preserve_rate=mixed_preserve_rate,
        rule_ratio=rule_ratio,
        mixed_preserve_min=mixed_preserve_min,
        rule_reject_max_ratio=rule_reject_max_ratio,
    )

    backup_n = sum(1 for x in rows if x.backup_provider_used)
    reason_ct = Counter((x.provider_switch_reason or "").strip() for x in rows if (x.provider_switch_reason or "").strip())
    timeout_n = sum(1 for x in rows if x.timeout_hint)

    hard_metrics = {
        "n_total": n,
        "n_model_routes": n_m,
        "json_rate_model_routes": json_rate,
        "val_rate_model_routes": val_rate,
        "fallback_rate_model_routes": fallback_rate,
        "mixed_preserve_rate": mixed_preserve_rate,
    }
    ops_metrics = {
        "avg_e2e_ms": round(sum(e2e_all) / len(e2e_all), 4) if e2e_all else 0.0,
        "p95_e2e_ms": round(_p95(e2e_all), 4) if e2e_all else 0.0,
        "route_counts": route_counts,
        "rule_or_reject_ratio": round(rule_ratio, 4),
        "rule_or_reject_count": int(rule_n),
        "selected_provider_model_id_counts": dict(sel_counter),
        "backup_provider_used_count": int(backup_n),
        "backup_provider_used_rate": round(float(backup_n) / float(n), 6) if n else 0.0,
        "provider_switch_reason_counts": dict(reason_ct),
        "timeout_hint_count": int(timeout_n),
    }
    routing_observation = {
        "complex_bucket_routed_turbo_count": len(complex_turbo),
        "rule_or_reject_count": int(rule_n),
        "pause_stop_expand_gray": bool(pause_stop),
    }
    return hard_metrics, ops_metrics, routing_observation, pause_checks, pause_stop, complex_turbo


def _mixed_boundary_summary(rows: List[Row]) -> Dict[str, Any]:
    """
    专项汇总：回答 day/night 是否主要掉档、是否可复现、非任务载荷是否缺失、以及 mixed all 命中率。
    """
    # case -> slot -> stats
    stats: Dict[str, Dict[str, Any]] = {}
    # routing model 侧
    model_fail: Dict[str, Dict[str, Any]] = {}

    for r in rows:
        if not r.case_id:
            continue
        if r.case_id not in stats:
            stats[r.case_id] = {}
        if r.time_slot not in stats[r.case_id]:
            stats[r.case_id][r.time_slot] = {
                "n": 0,
                "n_any_preserved": 0,
                "n_any_missed": 0,
                "n_all_preserved": 0,
                "n_all_missed": 0,
                "n_non_task_payload_missing": 0,
                "missing_keywords_all": Counter(),
                "missing_round_indices_any": set(),
                "missing_round_indices_all": set(),
            }

        slot_bucket = stats[r.case_id][r.time_slot]
        if r.mixed_preserved is None:
            continue

        slot_bucket["n"] += 1
        if r.non_task_payload_exists is False:
            slot_bucket["n_non_task_payload_missing"] += 1

        if r.mixed_preserved is True:
            slot_bucket["n_any_preserved"] += 1
        else:
            slot_bucket["n_any_missed"] += 1
            slot_bucket["missing_round_indices_any"].add(r.round_idx)

        if r.mixed_preserved_all is True:
            slot_bucket["n_all_preserved"] += 1
        else:
            # mixed_preserved_all 只有在 expected 非空时才会有值；因此可直接认为 all 未命中
            if r.mixed_preserved_all is False:
                slot_bucket["n_all_missed"] += 1
                slot_bucket["missing_round_indices_all"].add(r.round_idx)
                # 统计 missing keywords
                slot_bucket["missing_keywords_all"].update(r.mixed_keywords_missing)

        model_key = f"{r.routing_suggestion}|{r.selected_provider_model_id}".strip("|")
        if model_key not in model_fail:
            model_fail[model_key] = {"n": 0, "n_any_missed": 0, "n_all_missed": 0}
        model_fail[model_key]["n"] += 1
        if r.mixed_preserved is False:
            model_fail[model_key]["n_any_missed"] += 1
        if r.mixed_preserved_all is False:
            model_fail[model_key]["n_all_missed"] += 1

    # 把 set / Counter 转成可 JSON 序列化
    for case_id, per_slot in stats.items():
        for slot, sc in per_slot.items():
            sc["missing_round_indices_any"] = sorted(list(sc["missing_round_indices_any"]))
            sc["missing_round_indices_all"] = sorted(list(sc["missing_round_indices_all"]))
            sc["missing_keywords_all"] = dict(sc["missing_keywords_all"])

    return {
        "per_case_per_slot": stats,
        "fail_by_routing_model": model_fail,
    }


def _run_slot(
    *,
    time_slot: str,
    cases: List[Dict[str, Any]],
    rounds: int,
    mixed_preserve_min: float,
    rule_reject_max_ratio: float,
) -> Tuple[List[Row], Dict[str, Any]]:
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

    rows: List[Row] = []
    t_started = time.perf_counter()
    started_iso = datetime.now(timezone.utc).isoformat()

    for r in range(1, max(1, int(rounds)) + 1):
        for c in cases:
            cid = str(c.get("id") or "")
            bucket = str(c.get("bucket") or "")
            text = str(c.get("text") or "")
            kws = list(c.get("mixed_keywords") or [])
            _last_vr["vr"] = None

            print(f"  [{time_slot}] [{r}/{rounds}] {cid} …", flush=True)

            ev = VoiceInputEvent(
                event_id=f"m354b_{time_slot}_{r}_{cid}",
                request_id=f"m354b_{time_slot}_{r}_{cid}",
                session_id=f"m354b_gray_{time_slot}",
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

            meta = out.metadata or {}
            sug = str(meta.get("prefilter_routing_suggestion") or "")
            sel = str(meta.get("selected_provider_model_id") or "")
            backup_used = bool(meta.get("backup_provider_used", False))
            switch_rs = str(meta.get("provider_switch_reason") or "")

            res = out.long_input_parse_result
            notes = (getattr(res, "notes", "") or "") if res is not None else ""
            used_model = notes.startswith("model_chain")
            vr = _last_vr["vr"]
            vok = bool(vr.ok) if (vr is not None) else None

            fallback = False
            if sug in ("route_to_turbo", "route_to_plus"):
                fallback = not (used_model and vok is True)

            expected_kws = list(kws or [])
            non_task_exists = bool(res is not None and _non_task_payload_exists(res))
            mixed_keywords_found: List[str] = []
            mixed_keywords_missing: List[str] = []
            mixed_preserved: Optional[bool] = None
            mixed_preserved_all: Optional[bool] = None
            if expected_kws and res is not None:
                blob = _non_task_blob(res)
                mixed_keywords_found, mixed_keywords_missing = _mixed_keyword_hit_report(expected_kws, blob)
                mixed_preserved = len(mixed_keywords_found) > 0
                mixed_preserved_all = len(mixed_keywords_missing) == 0

            th = _timeout_hint(str(out.notes or ""), str(notes or ""))

            rows.append(
                Row(
                    time_slot=time_slot,
                    round_idx=r,
                    case_id=cid,
                    bucket=bucket,
                    routing_suggestion=sug,
                    selected_provider_model_id=sel,
                    used_model_chain=used_model,
                    validator_ok=vok,
                    fallback=fallback,
                    mixed_preserved=mixed_preserved,
                    mixed_preserved_all=mixed_preserved_all,
                    expected_mixed_keywords=expected_kws,
                    non_task_payload_exists=non_task_exists,
                    mixed_keywords_found=mixed_keywords_found,
                    mixed_keywords_missing=mixed_keywords_missing,
                    e2e_ms=e2e_ms,
                    backup_provider_used=backup_used,
                    provider_switch_reason=switch_rs,
                    timeout_hint=th,
                )
            )

    vmod.validate_model_structured_output = _orig_val  # type: ignore[assignment]

    ended_iso = datetime.now(timezone.utc).isoformat()
    duration_s = time.perf_counter() - t_started

    hm, om, ro, pchecks, pstop, cxt = _metrics_from_rows(
        rows, mixed_preserve_min=mixed_preserve_min, rule_reject_max_ratio=rule_reject_max_ratio
    )

    block = {
        "started_at_utc": started_iso,
        "ended_at_utc": ended_iso,
        "duration_sec": round(duration_s, 3),
        "hard_metrics": hm,
        "ops_metrics": om,
        "routing_observation": ro,
        "pause_checks": {**pchecks, "complex_bucket_routed_turbo_nonzero": len(cxt) > 0},
        "pause_stop_expand_gray": bool(pstop),
        "review": {"complex_bucket_routed_turbo": cxt},
        "rows": [asdict(x) for x in rows],
    }
    return rows, block


def main() -> None:
    ap = argparse.ArgumentParser(description="M3.5.4b mixed boundary专项验证 benchmark")
    ap.add_argument(
        "--cases-json",
        type=Path,
        default=ROOT / "configs" / "voice" / "voice_prefilter_routing_real_cases_m3_5_4a.json",
        help="专项 case 集（默认仅 C1/C7，2 条）",
    )
    ap.add_argument("--rounds", type=int, default=20, help="每时段轮数（建议 15～30；默认 20）")
    ap.add_argument(
        "--time-slot",
        choices=("day", "night", "all"),
        default="all",
        help="分时段标签：day / night 只跑单段；all 顺序跑 day 与 night（默认）",
    )
    ap.add_argument("--out-json", type=Path, default=None, help="落盘路径（默认 logs/benchmark_prefilter_routing_m3_5_4b_<UTC>.json）")
    ap.add_argument("--mixed-preserve-min", type=float, default=0.95)
    ap.add_argument("--rule-reject-max-ratio", type=float, default=0.35)
    ap.add_argument("--model-timeout-ms", type=int, default=120_000)
    args = ap.parse_args()

    os.environ["LUNA_VOICE_ENABLE_PREFILTER_ROUTING"] = "1"
    if not (os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS") or "").strip():
        os.environ["LUNA_QWEN_MODEL_TIMEOUT_MS"] = str(int(args.model_timeout_ms))

    data = json.loads(args.cases_json.read_text(encoding="utf-8"))
    cases: List[Dict[str, Any]] = list(data.get("cases") or [])
    if not cases:
        raise SystemExit(f"no cases in {args.cases_json}")

    slots: List[str]
    if args.time_slot == "all":
        slots = ["day", "night"]
    else:
        slots = [args.time_slot]

    t0_all = time.perf_counter()
    started_all = datetime.now(timezone.utc).isoformat()

    print("M3.5.4b benchmark starting…", flush=True)
    print(
        "  cases:",
        args.cases_json,
        "cases_n:",
        len(cases),
        "rounds/slot:",
        args.rounds,
        "time_slot:",
        args.time_slot,
        "LUNA_QWEN_MODEL_TIMEOUT_MS:",
        os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS"),
        flush=True,
    )

    per_slot: Dict[str, Any] = {}
    all_rows: List[Row] = []

    for slot in slots:
        rows, block = _run_slot(
            time_slot=slot,
            cases=cases,
            rounds=int(args.rounds),
            mixed_preserve_min=float(args.mixed_preserve_min),
            rule_reject_max_ratio=float(args.rule_reject_max_ratio),
        )
        per_slot[slot] = block
        all_rows.extend(rows)

    hm, om, ro, pchecks, pstop, cxt = _metrics_from_rows(
        all_rows, mixed_preserve_min=float(args.mixed_preserve_min), rule_reject_max_ratio=float(args.rule_reject_max_ratio)
    )
    aggregate = {
        "started_at_utc": started_all,
        "ended_at_utc": datetime.now(timezone.utc).isoformat(),
        "duration_sec": round(time.perf_counter() - t0_all, 3),
        "hard_metrics": hm,
        "ops_metrics": om,
        "routing_observation": ro,
        "pause_checks": {**pchecks, "complex_bucket_routed_turbo_nonzero": len(cxt) > 0},
        "pause_stop_expand_gray": bool(pstop),
        "review": {"complex_bucket_routed_turbo": cxt},
    }

    mixed_summary = _mixed_boundary_summary(all_rows)

    payload: Dict[str, Any] = {
            "schema": "luna.voice.gray_m3_5_4b.v1",
        "git_head": _git_head(),
        "cases_path": str(args.cases_json),
        "cases_n": len(cases),
        "rounds_per_time_slot": int(args.rounds),
        "time_slots_executed": slots,
        "env": {
            "LUNA_VOICE_ENABLE_PREFILTER_ROUTING": os.getenv("LUNA_VOICE_ENABLE_PREFILTER_ROUTING"),
            "LUNA_QWEN_MODEL_TIMEOUT_MS": os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS"),
            "LUNA_EXTERNAL_LLM_PROVIDER": os.getenv("LUNA_EXTERNAL_LLM_PROVIDER"),
        },
        "per_time_slot": per_slot,
        "mixed_boundary_summary": mixed_summary,
        "aggregate": aggregate,
    }

    out_path = args.out_json
    if out_path is None:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_dir = ROOT / "logs"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"benchmark_prefilter_routing_m3_5_4b_{ts}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("M3.5.4b benchmark OK")
    print("  out_json:", str(out_path))
    print("  aggregate hard:", aggregate["hard_metrics"])
    print("  aggregate ops (excerpt): avg_e2e_ms=", aggregate["ops_metrics"]["avg_e2e_ms"], "p95=", aggregate["ops_metrics"]["p95_e2e_ms"])
    print("  aggregate pause_stop_expand_gray:", aggregate["pause_stop_expand_gray"])
    if len(slots) > 1:
        print("  per_slot pause_stop:", {k: v["pause_stop_expand_gray"] for k, v in per_slot.items()})


if __name__ == "__main__":
    main()

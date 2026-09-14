#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3.5.6a model_chain 识别链归因（只做审计/对照/最小定位，不做修复）

固定输入：
  logs/benchmark_prefilter_routing_m3_5_6_20260407T025835Z.json

失败集合口径（必须收紧，避免把 rule/reject 正常样本吸进来）：
  - routing_suggestion in {route_to_turbo, route_to_plus}
  - 且满足任一：used_model_chain == false / validator_ok != true / fallback == true

输出：
  - logs/audit_model_chain_failures_m3_5_6a_<UTC>.json
  - logs/audit_model_chain_failures_m3_5_6a_<UTC>.md

注意：
  该脚本只基于 M3.5.6 日志中现有字段做“定点归因标签”。
  若需要回答“原始模型返回体/原始 JSON 是否存在”等问题，而日志字段不足，
  请按指令允许的最小 instrumentation 另行补充观测字段（本脚本会在输出中显式标注缺失）。
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


FAILURE_TAGS = (
    "no_model_payload",
    "model_payload_non_json",
    "json_present_but_not_tagged_as_model_chain",
    "json_present_but_parse_failed",
    "json_present_but_validator_not_reached",
    "unknown",
)


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _is_model_route(r: Dict[str, Any]) -> bool:
    return str(r.get("routing_suggestion") or "") in ("route_to_turbo", "route_to_plus")


def _is_failure_row(r: Dict[str, Any]) -> bool:
    # Strict per spec: any of the three signals.
    used = r.get("used_model_chain")
    vok = r.get("validator_ok")
    fb = r.get("fallback")
    return (used is False) or (vok is not True) or (fb is True)


def _pick_rows(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    per = obj.get("per_time_slot") or {}
    rows: List[Dict[str, Any]] = []
    for _slot, block in per.items():
        rows.extend(list(block.get("rows") or []))
    return rows


def _summarize_row(r: Dict[str, Any]) -> Dict[str, Any]:
    # Only include fields needed for audit; keep stable keys for diffing.
    return {
        "time_slot": r.get("time_slot"),
        "case_id": r.get("case_id"),
        "bucket": r.get("bucket"),
        "routing_suggestion": r.get("routing_suggestion"),
        "selected_provider_model_id": r.get("selected_provider_model_id"),
        "e2e_ms": r.get("e2e_ms"),
        "used_model_chain": r.get("used_model_chain"),
        "validator_ok": r.get("validator_ok"),
        "fallback": r.get("fallback"),
        "backup_provider_used": r.get("backup_provider_used"),
        "provider_switch_reason": r.get("provider_switch_reason"),
        # The following are desired-by-spec but NOT present in M3.5.6 log rows.
        "notes": None,
        "raw_model_payload_summary": None,
        "raw_model_payload_present": None,
        "raw_json_present": None,
        "raw_json_top_level_keys": None,
        "model_chain_detection_reason": None,
        "model_chain_detection_failed_reason": None,
    }


def _attribution_tag(r: Dict[str, Any]) -> Tuple[str, str]:
    """
    Return (failure_tag, rationale).
    With current M3.5.6 row schema we cannot truly know whether raw JSON existed.
    We therefore tag conservatively and explain what is missing.
    """
    used = r.get("used_model_chain")
    vok = r.get("validator_ok")
    fb = r.get("fallback")

    if not _is_model_route(r):
        return ("unknown", "non-model-route row should not be audited")

    # In M3.5.6 failures observed: used_model_chain=False, validator_ok=None, fallback=True
    # That pattern implies validator likely not reached, but we can't confirm raw JSON presence.
    if used is False and vok is None and fb is True:
        return (
            "unknown",
            "used_model_chain=false & validator_ok=None & fallback=true; raw model payload/json not present in log rows",
        )
    if used is False and fb is True:
        return ("unknown", "used_model_chain=false & fallback=true; need raw payload/json to distinguish A vs B")
    if vok is not True:
        return ("unknown", "validator_ok!=true; need validator error/raw json to attribute")
    return ("unknown", "unclassified by current evidence")


def _select_success_controls(
    rows: Sequence[Dict[str, Any]],
    *,
    preferred_case_ids: Sequence[str],
    k: int,
) -> List[Dict[str, Any]]:
    """
    Select 3-5 success rows as controls:
      - model routes only
      - success means: used_model_chain==True AND validator_ok==True AND fallback==False
      - prefer cases in preferred_case_ids (same type as failures)
    """
    def is_success(r: Dict[str, Any]) -> bool:
        if not _is_model_route(r):
            return False
        return (r.get("used_model_chain") is True) and (r.get("validator_ok") is True) and (r.get("fallback") is False)

    preferred = []
    fallback = []
    pref_set = {str(x) for x in preferred_case_ids if str(x)}
    for r in rows:
        if not is_success(r):
            continue
        if str(r.get("case_id") or "") in pref_set:
            preferred.append(r)
        else:
            fallback.append(r)

    chosen: List[Dict[str, Any]] = []
    for pool in (preferred, fallback):
        for r in pool:
            if len(chosen) >= int(k):
                break
            chosen.append(r)
        if len(chosen) >= int(k):
            break
    return chosen


def _write_markdown(
    *,
    out_path: Path,
    source_log: Path,
    git_head: str,
    failures: List[Dict[str, Any]],
    controls: List[Dict[str, Any]],
    conclusion_hint: str,
) -> None:
    def row_table(rs: List[Dict[str, Any]]) -> List[str]:
        lines: List[str] = []
        lines.append("| # | slot | case_id | bucket | suggestion | selected_model | used_model_chain | validator_ok | fallback | e2e_ms | tag | rationale |")
        lines.append("|---:|------|---------|--------|------------|----------------|-----------------|-------------|----------|--------:|-----|-----------|")
        for i, r in enumerate(rs, 1):
            tag = str(r.get("failure_tag") or "—")
            rat = str(r.get("failure_rationale") or "—").replace("\n", " ").strip()
            lines.append(
                "| {i} | {slot} | `{cid}` | {bucket} | {sug} | {model} | {used} | {vok} | {fb} | {ms:.3f} | {tag} | {rat} |".format(
                    i=i,
                    slot=str(r.get("time_slot") or ""),
                    cid=str(r.get("case_id") or ""),
                    bucket=str(r.get("bucket") or ""),
                    sug=str(r.get("routing_suggestion") or ""),
                    model=str(r.get("selected_provider_model_id") or ""),
                    used=str(r.get("used_model_chain")),
                    vok=str(r.get("validator_ok")),
                    fb=str(r.get("fallback")),
                    ms=float(r.get("e2e_ms") or 0.0),
                    tag=tag,
                    rat=(rat[:180] + "…") if len(rat) > 180 else rat,
                )
            )
        return lines

    lines: List[str] = []
    lines.append("# M3.5.6a model_chain 识别链归因（审计产物）")
    lines.append("")
    lines.append(f"- source_log: `{source_log}`")
    lines.append(f"- git_head: `{git_head}`")
    lines.append(f"- extracted_at_utc: `{datetime.now(timezone.utc).isoformat()}`")
    lines.append("")
    lines.append("## 失败集合口径（固定）")
    lines.append("")
    lines.append("- 仅审计 `route_to_turbo/route_to_plus` 的 model routes")
    lines.append("- failure 条件：`used_model_chain=false` 或 `validator_ok!=true` 或 `fallback=true`")
    lines.append("- 明确剔除：`route_to_rule_or_reject`（正常样本）")
    lines.append("")
    lines.append("## 失败样本（12 条）")
    lines.append("")
    lines.extend(row_table(failures))
    lines.append("")
    lines.append("## 成功对照样本（3–5 条）")
    lines.append("")
    lines.extend(row_table(controls))
    lines.append("")
    lines.append("## 字段缺口（本轮仅定位，不做修复）")
    lines.append("")
    lines.append("- 本次 M3.5.6 `rows` 未包含 `notes` / `raw_model_payload` / `raw_json` 等证据字段。")
    lines.append("- 因此当前 failure_tag 只能给出 **保守归因**（多为 `unknown`），要区分「模型真失败」 vs 「识别/打标漏识别」，需要最小 instrumentation 补充观测字段。")
    lines.append("")
    lines.append("## 结论模板（跑完补观测后填写）")
    lines.append("")
    lines.append("- 结论：A / B / C（只选一个）")
    lines.append(f"- 当前提示：{conclusion_hint}")
    lines.append("")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="M3.5.6a audit: model_chain detection/tagging failures (no fixes)")
    ap.add_argument(
        "--src-log",
        type=Path,
        default=Path("logs/benchmark_prefilter_routing_m3_5_6_20260407T025835Z.json"),
        help="M3.5.6 源日志（固定口径默认值）",
    )
    ap.add_argument("--out-dir", type=Path, default=Path.cwd() / "logs", help="输出目录（默认当前工作目录的 logs/）")
    ap.add_argument("--controls", type=int, default=5, help="成功对照样本数（默认 5；建议 3～5）")
    ap.add_argument(
        "--prefer-cases",
        type=str,
        default="C1_mixed_nav,C2_mixed_health_nav,C3_ordered_itinerary_multistep,S4_simple_nav_longer,S5_simple_poi_longer",
        help="优先抽取成功对照的 case_id（逗号分隔）",
    )
    args = ap.parse_args()

    src = args.src_log
    if not src.exists():
        raise SystemExit(f"src log not found: {src}")

    obj = _read_json(src)
    git_head = str(obj.get("git_head") or "")
    rows = _pick_rows(obj)

    model_rows = [r for r in rows if _is_model_route(r)]
    failures_raw = [r for r in model_rows if _is_failure_row(r)]

    failures: List[Dict[str, Any]] = []
    for r in failures_raw:
        s = _summarize_row(r)
        tag, rat = _attribution_tag(r)
        s["failure_tag"] = tag
        s["failure_rationale"] = rat
        failures.append(s)

    # Deterministic ordering for review.
    failures = sorted(failures, key=lambda x: (str(x.get("time_slot") or ""), str(x.get("case_id") or ""), str(x.get("routing_suggestion") or "")))

    preferred_cases = [x.strip() for x in str(args.prefer_cases or "").split(",") if x.strip()]
    controls_raw = _select_success_controls(rows, preferred_case_ids=preferred_cases, k=max(3, min(5, int(args.controls))))
    controls: List[Dict[str, Any]] = []
    for r in controls_raw:
        s = _summarize_row(r)
        # Controls are not failures; keep fields for table alignment.
        s["failure_tag"] = "—"
        s["failure_rationale"] = "success_control"
        controls.append(s)

    # Build output payload.
    stamp = _utc_stamp()
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / f"audit_model_chain_failures_m3_5_6a_{stamp}.json"
    out_md = out_dir / f"audit_model_chain_failures_m3_5_6a_{stamp}.md"

    # Hint: based on current evidence (all failures in day; validator not reached).
    slots = sorted({str(x.get("time_slot") or "") for x in failures})
    conclusion_hint = (
        "失败集中在 day 且表现为 used_model_chain=false/validator_ok=None；更像识别/打标链路未命中，但需补 raw payload/json 观测确认。"
        if slots == ["day"]
        else "失败分布不止 day；需补 raw payload/json 观测进一步确认。"
    )

    payload: Dict[str, Any] = {
        "schema": "luna.voice.audit_m3_5_6a_model_chain.v1",
        "source_log": str(src),
        "git_head": git_head,
        "extracted_at_utc": datetime.now(timezone.utc).isoformat(),
        "failure_set_spec": {
            "routing_suggestion_in": ["route_to_turbo", "route_to_plus"],
            "failure_any_of": ["used_model_chain==false", "validator_ok!=true", "fallback==true"],
            "exclude": ["route_to_rule_or_reject"],
        },
        "note": {
            "raw_payload_fields_missing_in_m3_5_6_rows": True,
            "allowed_failure_tags": list(FAILURE_TAGS),
        },
        "counts": {
            "rows_total": len(rows),
            "model_rows_total": len(model_rows),
            "failure_rows_total": len(failures),
            "controls_rows_total": len(controls),
            "failure_by_time_slot": {
                k: sum(1 for x in failures if x.get("time_slot") == k)
                for k in sorted({x.get("time_slot") for x in failures})
            },
        },
        "failures": failures,
        "controls": controls,
        "conclusion_hint": conclusion_hint,
    }

    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_markdown(
        out_path=out_md,
        source_log=src,
        git_head=git_head,
        failures=failures,
        controls=controls,
        conclusion_hint=conclusion_hint,
    )

    print("M3.5.6a audit OK")
    print("  out_json:", str(out_json))
    print("  out_md  :", str(out_md))
    print("  failures_n:", len(failures), "slots:", sorted({x.get("time_slot") for x in failures}))


if __name__ == "__main__":
    main()


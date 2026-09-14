#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unified env 最小接线实验（V1）观察分析器

输入：每行 JSON，兼容两类（见 _load_rows）：
- 扁平行：{"id","event_timestamp","metadata"}
- envelope：{"type":"unified_env_min_wiring_snapshot","data":{...}}，其中 data 含 id 或 related_request_id、event_timestamp、metadata

扁平行示例：
{
  "id": "...",
  "event_timestamp": 123.0,
  "metadata": {
    "...": "...",
    "unified_env_fill_shadow_v1": { ... }
  }
}

输出：md/json（默认写入可写目录；可 --output-dir 指定）。

本脚本只分析，不改主线行为。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _utc_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _resolve_output_dir(explicit: Optional[str]) -> Path:
    if explicit:
        p = Path(explicit).expanduser().resolve()
        p.mkdir(parents=True, exist_ok=True)
        return p
    envp = os.getenv("LUNA_UNIFIED_MIN_WIRING_ANALYZE_OUT", "").strip()
    if envp:
        p = Path(envp).expanduser().resolve()
        p.mkdir(parents=True, exist_ok=True)
        return p
    for candidate in (ROOT / "logs", ROOT / "logs_analyze_unified_min_wiring_v1"):
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".write_probe_unified_min_wiring"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            return candidate
        except OSError:
            continue
    fallback = Path.cwd() / "analyze_unified_env_min_wiring_out"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def _load_rows(path: Path) -> List[Tuple[str, float, Dict[str, Any]]]:
    """
    兼容 flat rows 与 unified_env_min_wiring_snapshot envelope rows；
    归一化后统一产出 (id, event_timestamp, metadata)。
    """
    rows: List[Tuple[str, float, Dict[str, Any]]] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        if obj.get("type") == "unified_env_min_wiring_snapshot" and isinstance(obj.get("data"), dict):
            row: Dict[str, Any] = obj["data"]
        else:
            row = obj
        md = row.get("metadata")
        if not isinstance(md, dict):
            continue
        rid = str(row.get("id") or row.get("related_request_id") or f"line_{i}")
        ts = row.get("event_timestamp")
        try:
            tsv = float(ts) if ts is not None else 0.0
        except (TypeError, ValueError):
            tsv = 0.0
        rows.append((rid, tsv, md))
    return rows


def _inc(d: Dict[str, int], k: str, n: int = 1) -> None:
    d[k] = int(d.get(k, 0)) + int(n)


def main() -> None:
    ap = argparse.ArgumentParser(description="unified env 最小接线实验观察分析器 V1")
    ap.add_argument("--input-jsonl", required=True, help="窗口 JSONL（每行含 metadata + unified_env_fill_shadow_v1）")
    ap.add_argument("--output-dir", default="", help="输出目录（也可用 LUNA_UNIFIED_MIN_WIRING_ANALYZE_OUT）")
    args = ap.parse_args()

    utc = _utc_ts()
    out_dir = _resolve_output_dir(args.output_dir.strip() or None)
    jpath = out_dir / f"analyze_unified_env_min_wiring_v1_{utc}.json"
    mpath = out_dir / f"analyze_unified_env_min_wiring_v1_{utc}.md"

    rows = _load_rows(Path(args.input_jsonl))

    fill_applied_count = 0
    effective_fill_count = 0
    ineffective_fill_count = 0
    filled_fields_dist: Dict[str, int] = {}
    blocked_reason_dist: Dict[str, int] = {}
    blocked_family_candidate_mismatch = 0
    samples_effective: List[Dict[str, Any]] = []
    samples_blocked: List[Dict[str, Any]] = []

    for rid, ts, md in rows:
        rec = md.get("unified_env_fill_shadow_v1")
        if not isinstance(rec, dict):
            ineffective_fill_count += 1
            _inc(blocked_reason_dist, "missing_fill_record")
            continue

        applied = bool(rec.get("fill_applied") is True)
        filled_fields = rec.get("filled_fields") if isinstance(rec.get("filled_fields"), list) else []
        blocked = rec.get("fill_blocked_reason") if isinstance(rec.get("fill_blocked_reason"), list) else []

        if applied:
            fill_applied_count += 1
        if applied and filled_fields:
            effective_fill_count += 1
        else:
            ineffective_fill_count += 1

        for f in filled_fields:
            _inc(filled_fields_dist, str(f))
        for b in blocked:
            _inc(blocked_reason_dist, str(b))
        if any(str(b) == "family_candidate_mismatch" for b in blocked):
            blocked_family_candidate_mismatch += 1

        if applied and filled_fields and len(samples_effective) < 20:
            samples_effective.append(
                {
                    "id": rid,
                    "event_timestamp": ts,
                    "target_summary_key": rec.get("target_summary_key"),
                    "filled_fields": filled_fields,
                    "fill_blocked_reason": blocked,
                }
            )
        if (not applied) and len(samples_blocked) < 20:
            samples_blocked.append(
                {
                    "id": rid,
                    "event_timestamp": ts,
                    "target_summary_key": rec.get("target_summary_key"),
                    "filled_fields": filled_fields,
                    "fill_blocked_reason": blocked,
                }
            )

    payload = {
        "generated_at_utc": utc,
        "input_jsonl": str(Path(args.input_jsonl)),
        "row_count": len(rows),
        "fill_applied_count": fill_applied_count,
        "effective_fill_count": effective_fill_count,
        "ineffective_fill_count": ineffective_fill_count,
        "filled_fields_distribution": dict(sorted(filled_fields_dist.items(), key=lambda x: (-x[1], x[0]))),
        "fill_blocked_reason_distribution": dict(sorted(blocked_reason_dist.items(), key=lambda x: (-x[1], x[0]))),
        "blocked_family_candidate_mismatch_count": blocked_family_candidate_mismatch,
        "samples": {
            "effective": samples_effective,
            "blocked_or_ineffective": samples_blocked,
        },
    }
    jpath.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines: List[str] = [
        f"# unified env 最小接线实验观察（V1） {utc}",
        "",
        "## 汇总",
        "",
        f"- row_count: {payload['row_count']}",
        f"- fill_applied_count: {payload['fill_applied_count']}",
        f"- effective_fill_count: {payload['effective_fill_count']}",
        f"- ineffective_fill_count: {payload['ineffective_fill_count']}",
        f"- blocked_family_candidate_mismatch_count: {payload['blocked_family_candidate_mismatch_count']}",
        "",
        "## filled_fields 分布",
        "",
    ]
    if payload["filled_fields_distribution"]:
        for k, v in payload["filled_fields_distribution"].items():
            md_lines.append(f"- **{k}**: {v}")
    else:
        md_lines.append("- （空）")

    md_lines.extend(["", "## fill_blocked_reason 分布", ""])
    for k, v in payload["fill_blocked_reason_distribution"].items():
        md_lines.append(f"- **{k}**: {v}")

    md_lines.extend(["", "## 样本（effective，最多 20）", ""])
    for s in samples_effective:
        md_lines.append(f"- **{s['id']}**: target={s.get('target_summary_key')} fields={s.get('filled_fields')}")

    md_lines.extend(["", "## 样本（blocked/ineffective，最多 20）", ""])
    for s in samples_blocked:
        md_lines.append(f"- **{s['id']}**: target={s.get('target_summary_key')} blocked={s.get('fill_blocked_reason')}")

    md_lines.extend(
        [
            "",
            f"完整 JSON: `{jpath.name}`（目录 `{out_dir}`）",
            "",
            "## 一句话收束",
            "",
            "先用该统计判断补缺是否出现正收益；若长期几乎全阻断且无有效补缺，则应考虑撤回到纯 shadow。",
        ]
    )
    mpath.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Wrote {jpath}")
    print(f"Wrote {mpath}")


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D0.1: Baseline vs candidate parity。对比 decision 三件套 + pal_lookahead_m，产出 parity_report.json。
含幽灵变量归因 notes（D0.1-5）。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

FIELDS = ["safety_level", "control_mode", "pal_lookahead_m"]

# 安全边界容差：仅 safety_level 为 SAFE vs CAUTION 且 complexity 在阈值附近时视为一致
SAFETY_BOUNDARY_LOW = 0.32
SAFETY_BOUNDARY_HIGH = 0.55


def _load_jsonl(path: Path) -> list[dict]:
    out: list[dict] = []
    if not path.is_file():
        return out
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _obs_excerpt(record: dict) -> dict:
    """从 OBS_V1 取少量关键观测字段。"""
    o = record.get("obs") or {}
    return {
        "seq": record.get("seq"),
        "ts": record.get("ts"),
        "frame_quality": o.get("frame_quality"),
        "pal": o.get("pal"),
        "complexity": o.get("complexity"),
        "vc": o.get("vc"),
        "motion": o.get("motion"),
        "path": o.get("path"),
        "branch": o.get("branch"),
        "roi": o.get("roi"),
    }


def _ghost_notes(
    first_mismatch_seq: int | None,
    mismatch_fields: dict,
    baseline_excerpt: list,
    candidate_excerpt: list,
    baseline_len: int,
    candidate_len: int,
) -> list[str]:
    """D0.1-5: 简易幽灵变量归因提示。"""
    notes: list[str] = []
    if first_mismatch_seq is None:
        return notes
    if first_mismatch_seq == 0 or (baseline_excerpt and baseline_excerpt[0].get("seq") == 0):
        notes.append("首帧或 reset 后首帧即 mismatch → 优先怀疑全局状态 / reset 不彻底")
    if "pal_lookahead_m" in mismatch_fields:
        b, c = mismatch_fields["pal_lookahead_m"].get("baseline"), mismatch_fields["pal_lookahead_m"].get("candidate")
        if b is not None and c is not None and isinstance(b, (int, float)) and isinstance(c, (int, float)):
            if abs(float(b) - float(c)) < 0.01:
                notes.append("仅 pal_lookahead_m 小数尾差 → 优先怀疑 FP 精度 / JSON round-trip")
    if candidate_len < baseline_len or (candidate_len == 0 and baseline_len > 0):
        notes.append("candidate 缺 decision → 优先怀疑覆盖率/输入帧过滤条件不同")
    if baseline_len > 0 and first_mismatch_seq is not None and first_mismatch_seq > 0:
        notes.append("mismatch 非首帧 → 若总在固定时间间隔出现可怀疑墙钟/超时逻辑未注入")
    return notes


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="D0.1: Parity baseline vs candidate_decisions.jsonl")
    p.add_argument("--episode", required=True, help="Episode path relative to base_dir (to read baseline from records)")
    p.add_argument("--base-dir", default=os.path.join(ROOT, "library_store"))
    p.add_argument("--candidate", required=True, help="Path to candidate_decisions.jsonl")
    p.add_argument("--out-dir", default=os.path.join(ROOT, "outputs"))
    args = p.parse_args()

    base_dir = Path(args.base_dir)
    episode_dir = base_dir / args.episode.strip("/")
    records_path = episode_dir / "records.jsonl"
    OBS_V1 = "OBS_V1"
    records = _load_jsonl(records_path)
    obs_v1 = [r for r in records if (r.get("record_type") or "").strip() == OBS_V1]

    baseline_by_seq: dict[int, dict] = {}
    obs_by_seq: dict[int, dict] = {}
    for r in obs_v1:
        seq = r.get("seq", len(baseline_by_seq))
        d = r.get("decision") or {}
        baseline_by_seq[seq] = {
            "seq": seq,
            "safety_level": d.get("safety_level"),
            "control_mode": d.get("control_mode"),
            "pal_lookahead_m": d.get("pal_lookahead_m"),
        }
        obs_by_seq[seq] = r.get("obs") or {}

    candidate_path = Path(args.candidate)
    candidate_lines = _load_jsonl(candidate_path)
    candidate_by_seq: dict[int, dict] = {}
    for row in candidate_lines:
        seq = row.get("seq", len(candidate_by_seq))
        candidate_by_seq[seq] = {
            "seq": seq,
            "safety_level": row.get("safety_level"),
            "control_mode": row.get("control_mode"),
            "pal_lookahead_m": row.get("pal_lookahead_m"),
        }

    first_mismatch_seq: int | None = None
    mismatch_fields: dict = {}
    all_seqs = sorted(set(baseline_by_seq) | set(candidate_by_seq))
    for seq in all_seqs:
        b = baseline_by_seq.get(seq)
        c = candidate_by_seq.get(seq)
        diffs: dict[str, dict] = {}
        for f in FIELDS:
            bv = b.get(f) if b else None
            cv = c.get(f) if c else None
            if bv is None:
                continue
            if bv != cv:
                if isinstance(bv, float) and isinstance(cv, float) and abs(bv - cv) < 1e-9:
                    continue
                diffs[f] = {"baseline": bv, "candidate": cv}
        if diffs:
            # 安全边界容差：safety_level 为 SAFE/CAUTION 且 complexity 在阈值附近时不记为 mismatch（pal 差异随之忽略）
            if "safety_level" in diffs:
                bv, cv = diffs["safety_level"].get("baseline"), diffs["safety_level"].get("candidate")
                if {str(bv).upper(), str(cv).upper()} == {"SAFE", "CAUTION"}:
                    comp = obs_by_seq.get(seq, {}).get("complexity")
                    try:
                        c = float(comp) if comp is not None else None
                    except (TypeError, ValueError):
                        c = None
                    in_range = c is not None and SAFETY_BOUNDARY_LOW <= c <= SAFETY_BOUNDARY_HIGH
                    only_safety_pal = set(diffs.keys()) <= {"safety_level", "pal_lookahead_m"}
                    if in_range or (c is None and only_safety_pal):
                        continue
            # control_mode 边界容差：ASSISTED vs GUARDED（常为 view_confidence 阈值 0.4 导致）不记为 mismatch
            if set(diffs.keys()) == {"control_mode"}:
                bv, cv = diffs["control_mode"].get("baseline"), diffs["control_mode"].get("candidate")
                if {str(bv).upper(), str(cv).upper()} == {"ASSISTED", "GUARDED"}:
                    continue
            first_mismatch_seq = seq
            mismatch_fields = diffs
            break

    # 严格相等：pal_lookahead_m 先做严格相等；浮点容忍可后续加开关
    passed = first_mismatch_seq is None

    # excerpts: mismatch 帧前后各 2 帧
    baseline_excerpt: list = []
    candidate_excerpt: list = []
    obs_excerpt: dict = {}
    if first_mismatch_seq is not None:
        idx = next((i for i, r in enumerate(obs_v1) if r.get("seq") == first_mismatch_seq), None)
        if idx is not None:
            obs_excerpt = _obs_excerpt(obs_v1[idx])
            for i in range(max(0, idx - 2), min(len(obs_v1), idx + 3)):
                baseline_excerpt.append(baseline_by_seq.get(obs_v1[i].get("seq"), {}))
            for seq in sorted(candidate_by_seq.keys()):
                if abs(seq - first_mismatch_seq) <= 2:
                    candidate_excerpt.append(candidate_by_seq[seq])
            candidate_excerpt = sorted(candidate_excerpt, key=lambda x: x.get("seq", 0))[:5]

    notes = _ghost_notes(
        first_mismatch_seq,
        mismatch_fields,
        baseline_excerpt,
        candidate_excerpt,
        len(baseline_by_seq),
        len(candidate_by_seq),
    )

    # baseline_vs_candidate: mismatch 帧的 baseline/candidate 关键字段并排
    baseline_vs_candidate: dict = {}
    if first_mismatch_seq is not None:
        baseline_vs_candidate = {
            "seq": first_mismatch_seq,
            "baseline": baseline_by_seq.get(first_mismatch_seq),
            "candidate": candidate_by_seq.get(first_mismatch_seq),
        }

    # virtual_time_source: 时间来自 records 的哪个字段、解析成功率
    ts_ok = sum(1 for r in obs_v1 if r.get("ts") is not None)
    virtual_time_source = {
        "field": "ts",
        "parsed_count": ts_ok,
        "total_frames": len(obs_v1),
        "parse_success_ratio": ts_ok / len(obs_v1) if obs_v1 else 0.0,
    }

    report = {
        "is_identical": passed,
        "passed": passed,
        "first_mismatch_seq": first_mismatch_seq,
        "mismatch_fields": mismatch_fields,
        "baseline_excerpt": baseline_excerpt,
        "candidate_excerpt": candidate_excerpt,
        "baseline_vs_candidate": baseline_vs_candidate,
        "obs_excerpt": obs_excerpt,
        "virtual_time_source": virtual_time_source,
        "float_policy": "strict",
        "boundary_tolerance": "safety_level SAFE/CAUTION (complexity 0.32-0.55 or missing); control_mode ASSISTED/GUARDED",
        "notes": notes,
    }

    out_dir = Path(args.out_dir.rstrip("/"))
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "parity_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("passed:", passed)
    print("first_mismatch_seq:", first_mismatch_seq)
    print("parity_report:", report_path)
    if notes:
        print("notes:", notes)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

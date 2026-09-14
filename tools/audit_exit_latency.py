#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guardian Discipline Phase 1: 退出纪律审计。
基于 control_mode 行为（与 A3 risk 数值解耦）评估 B 型配置是否存在粘滞型 Goodhart。
输入：baseline / candidate 的 replay_output.jsonl；输出：exit_audit_report.json + .md。
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# 风险态：仅基于 control_mode，与 risk_raw/threshold 无关
RISK_STATE_MODES = frozenset({"CAUTION", "GUARDED"})
ENTRY_TOLERANCE_FRAMES = 5
DEFAULT_TOP_K = 10


def _control_mode(rec: Dict[str, Any]) -> str:
    """从一行 replay 取 control_mode，缺失则 NONE。"""
    dec = rec.get("decision")
    if not dec or not isinstance(dec, dict):
        return "NONE"
    cm = dec.get("control_mode")
    if cm is None or (isinstance(cm, str) and not cm.strip()):
        return "NONE"
    return (cm if isinstance(cm, str) else str(cm)).strip().upper()


def _is_risk_state(mode: str) -> bool:
    return mode in RISK_STATE_MODES


def _load_seqs_and_modes(path: str) -> List[Tuple[int, str]]:
    """返回 [(seq, control_mode), ...] 按行序。"""
    out: List[Tuple[int, str]] = []
    if not Path(path).is_file():
        return out
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            seq = rec.get("seq")
            if seq is None:
                continue
            try:
                seq = int(seq)
            except (TypeError, ValueError):
                continue
            mode = _control_mode(rec)
            out.append((seq, mode))
    return out


def _extract_events(seq_mode_list: List[Tuple[int, str]]) -> List[Dict[str, Any]]:
    """
    从 (seq, mode) 列表提取事件。
    event: entry_seq（进入 risk 的第一帧）, exit_seq（退出 risk 的第一帧，该帧已非 risk）,
           dwell_frames = exit_seq - entry_seq。
    先按 seq 排序，避免乱序 replay 产生负 dwell。
    """
    sorted_list = sorted(seq_mode_list, key=lambda x: x[0])
    events: List[Dict[str, Any]] = []
    in_risk = False
    entry_seq: Optional[int] = None
    for seq, mode in sorted_list:
        risk = _is_risk_state(mode)
        if not in_risk and risk:
            in_risk = True
            entry_seq = seq
        elif in_risk and not risk:
            in_risk = False
            if entry_seq is not None:
                dwell = max(0, seq - entry_seq)
                events.append({
                    "entry_seq": entry_seq,
                    "exit_seq": seq,
                    "dwell_frames": dwell,
                })
            entry_seq = None
    if in_risk and entry_seq is not None:
        # 末尾仍在 risk，用最后一帧的下一帧作为虚拟 exit（dwell = 最后一帧 - entry + 1）
        last_seq = sorted_list[-1][0] if sorted_list else entry_seq
        events.append({
            "entry_seq": entry_seq,
            "exit_seq": last_seq + 1,
            "dwell_frames": max(0, last_seq - entry_seq + 1),
        })
    return events


def _seq_set(entry: int, exit_seq: int) -> set:
    """事件覆盖的 seq 集合 [entry_seq, exit_seq)。"""
    return set(range(entry, exit_seq))


def _match_baseline_to_candidate(
    baseline_events: List[Dict[str, Any]],
    candidate_events: List[Dict[str, Any]],
    tolerance: int,
) -> Tuple[List[Tuple[Dict, Dict]], List[Dict], List[Dict]]:
    """
    按 baseline 事件为锚点匹配 candidate 事件（entry 最近且 diff ≤ tolerance）。
    返回 (matched_pairs, unmatched_baseline_events, baseline_no_entry_candidate_events)。
    """
    matched_pairs: List[Tuple[Dict, Dict]] = []
    used_cand = set()
    for be in baseline_events:
        b_entry = be["entry_seq"]
        best_cand: Optional[Dict] = None
        best_diff: Optional[int] = None
        for i, ce in enumerate(candidate_events):
            if i in used_cand:
                continue
            diff = abs(ce["entry_seq"] - b_entry)
            if diff <= tolerance and (best_diff is None or diff < best_diff):
                best_diff = diff
                best_cand = (i, ce)
        if best_cand is not None:
            i, ce = best_cand
            used_cand.add(i)
            matched_pairs.append((be, ce))
    matched_baseline_entries = {p[0]["entry_seq"] for p in matched_pairs}
    unmatched_baseline = [be for be in baseline_events if be["entry_seq"] not in matched_baseline_entries]
    baseline_no_entry = [candidate_events[i] for i in range(len(candidate_events)) if i not in used_cand]
    return matched_pairs, unmatched_baseline, baseline_no_entry


def run_audit(
    baseline_path: str,
    candidate_path: str,
    out_path: Optional[str] = None,
    mode: str = "risk_states",
    top_k: int = DEFAULT_TOP_K,
) -> Dict[str, Any]:
    """
    执行退出延迟与滞回效率审计，返回完整 report 字典（含 summary, events_matched, events_baseline_no_entry, top_offenders）。
    若 out_path 给定，会写入 .json 与同目录 .md。
    """
    base_list = _load_seqs_and_modes(baseline_path)
    cand_list = _load_seqs_and_modes(candidate_path)
    base_events = _extract_events(base_list)
    cand_events = _extract_events(cand_list)

    matched_pairs, unmatched_baseline, baseline_no_entry_events = _match_baseline_to_candidate(
        base_events, cand_events, ENTRY_TOLERANCE_FRAMES
    )

    # Exit latency & overlap per matched pair
    events_matched: List[Dict[str, Any]] = []
    exit_latencies: List[int] = []
    total_overlap = 0
    total_candidate_frames = 0
    for be, ce in matched_pairs:
        exit_latency_frames = ce["exit_seq"] - be["exit_seq"]
        exit_latencies.append(exit_latency_frames)
        b_set = _seq_set(be["entry_seq"], be["exit_seq"])
        c_set = _seq_set(ce["entry_seq"], ce["exit_seq"])
        overlap = len(c_set & b_set)
        c_frames = len(c_set)
        total_overlap += overlap
        total_candidate_frames += c_frames
        efficiency = (overlap / c_frames) if c_frames else 1.0
        events_matched.append({
            "baseline_entry_seq": be["entry_seq"],
            "baseline_exit_seq": be["exit_seq"],
            "candidate_entry_seq": ce["entry_seq"],
            "candidate_exit_seq": ce["exit_seq"],
            "baseline_dwell_frames": be["dwell_frames"],
            "candidate_dwell_frames": ce["dwell_frames"],
            "exit_latency_frames": exit_latency_frames,
            "overlap_frames": overlap,
            "candidate_frames": c_frames,
            "efficiency": round(efficiency, 4),
        })
    hysteresis_efficiency = (total_overlap / total_candidate_frames) if total_candidate_frames else 1.0

    # Percentiles
    exit_latencies_sorted = sorted(exit_latencies) if exit_latencies else [0]
    n = len(exit_latencies_sorted)
    p50 = exit_latencies_sorted[int((n - 1) * 0.50)] if n else 0
    p95 = exit_latencies_sorted[int((n - 1) * 0.95)] if n else 0
    max_lat = max(exit_latencies) if exit_latencies else 0

    events_baseline_no_entry = [
        {
            "candidate_entry_seq": e["entry_seq"],
            "candidate_exit_seq": e["exit_seq"],
            "candidate_dwell_frames": e["dwell_frames"],
        }
        for e in baseline_no_entry_events
    ]

    # Top offenders: exit_latency 按 exit_latency_frames 降序；baseline_no_entry 按 candidate_dwell_frames 降序
    top_exit = sorted(events_matched, key=lambda x: -x["exit_latency_frames"])[:top_k]
    top_no_entry = sorted(events_baseline_no_entry, key=lambda x: -x["candidate_dwell_frames"])[:top_k]

    # 真实视频六指标：guarded_tail_ratio（candidate 中 GUARDED 帧占比）, max_dwell_frames（candidate 单事件最长持续帧数）
    total_cand_frames = len(cand_list)
    guarded_frames = sum(1 for _, m in cand_list if m == "GUARDED")
    guarded_tail_ratio = round(guarded_frames / total_cand_frames, 4) if total_cand_frames else 0.0
    max_dwell_frames = max((max(0, e["dwell_frames"]) for e in cand_events), default=0)

    summary = {
        "exit_latency_p50": p50,
        "exit_latency_p95": p95,
        "exit_latency_max": max_lat,
        "matched_event_count": len(matched_pairs),
        "baseline_event_count": len(base_events),
        "candidate_event_count": len(cand_events),
        "baseline_no_entry_count": len(baseline_no_entry_events),
        "missing_candidate_event_count": len(unmatched_baseline),
        "hysteresis_efficiency": round(hysteresis_efficiency, 4),
        "guarded_tail_ratio": guarded_tail_ratio,
        "max_dwell_frames": max_dwell_frames,
    }
    report = {
        "summary": summary,
        "events_matched": events_matched,
        "events_baseline_no_entry": events_baseline_no_entry,
        "top_offenders": {
            "exit_latency": top_exit,
            "baseline_no_entry": top_no_entry,
        },
    }

    if out_path:
        out_p = Path(out_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        md_path = out_p.with_suffix(".md")
        _write_md_report(report, md_path, top_k)

    return report


def _write_md_report(report: Dict[str, Any], md_path: Path, top_k: int) -> None:
    s = report["summary"]
    lines = [
        "# Exit Latency Audit Report",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Exit Latency p50 | {s['exit_latency_p50']} |",
        f"| Exit Latency p95 | {s['exit_latency_p95']} |",
        f"| Exit Latency max | {s['exit_latency_max']} |",
        f"| Hysteresis Efficiency | {s['hysteresis_efficiency']} |",
        f"| baseline_no_entry_count | {s['baseline_no_entry_count']} |",
        f"| matched_event_count | {s['matched_event_count']} |",
        f"| missing_candidate_event_count | {s['missing_candidate_event_count']} |",
        f"| guarded_tail_ratio | {s.get('guarded_tail_ratio', 'N/A')} |",
        f"| max_dwell_frames | {s.get('max_dwell_frames', 'N/A')} |",
        "",
        "## Top-3 Offenders (Exit Latency)",
        "",
    ]
    for i, ev in enumerate(report["top_offenders"]["exit_latency"][:3], 1):
        lines.append(f"{i}. exit_latency_frames={ev['exit_latency_frames']} (baseline_exit={ev['baseline_exit_seq']}, candidate_exit={ev['candidate_exit_seq']})")
    lines.extend([
        "",
        "## Top-3 Offenders (Baseline No Entry)",
        "",
    ])
    for i, ev in enumerate(report["top_offenders"]["baseline_no_entry"][:3], 1):
        lines.append(f"{i}. candidate_dwell_frames={ev['candidate_dwell_frames']} (entry={ev['candidate_entry_seq']}, exit={ev['candidate_exit_seq']})")
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="Guardian Discipline Phase 1: exit latency audit")
    p.add_argument("--baseline", required=True, help="Path to baseline replay_output.jsonl")
    p.add_argument("--candidate", required=True, help="Path to candidate replay_output.jsonl")
    p.add_argument("--out", default="", help="Output exit_audit_report.json path (default: same dir as candidate)")
    p.add_argument("--mode", default="risk_states", help="Mode (default risk_states)")
    p.add_argument("--print-topk", type=int, default=DEFAULT_TOP_K, help="Top-k offenders (default 10)")
    args = p.parse_args()
    baseline_path = Path(args.baseline).resolve()
    candidate_path = Path(args.candidate).resolve()
    if not baseline_path.is_file():
        print(f"ERROR: baseline not found: {baseline_path}", file=sys.stderr)
        return 2
    if not candidate_path.is_file():
        print(f"ERROR: candidate not found: {candidate_path}", file=sys.stderr)
        return 2
    out_path = args.out
    if not out_path:
        out_path = str(candidate_path.parent / "exit_audit_report.json")
    report = run_audit(
        str(baseline_path),
        str(candidate_path),
        out_path=out_path,
        mode=args.mode,
        top_k=args.print_topk,
    )
    s = report["summary"]
    print("exit_latency_p50:", s["exit_latency_p50"])
    print("exit_latency_p95:", s["exit_latency_p95"])
    print("exit_latency_max:", s["exit_latency_max"])
    print("hysteresis_efficiency:", s["hysteresis_efficiency"])
    print("baseline_no_entry_count:", s["baseline_no_entry_count"])
    print("Written:", out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())

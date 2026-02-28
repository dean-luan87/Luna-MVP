#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A1 v0 验收：读 trace，按冻结版对照表给出「通过 / 不通过」裁决。
用法: python3 tools/verify_a1_acceptance.py [logs/a3_trace.jsonl]
"""

import json
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from intervention.engagement_v0 import (
    L2_HOLD_ENGAGED_SAMPLES,
    PAL_L2_THRESHOLD,
    VC_L2_THRESHOLD,
)


def load_rows(path: str):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    return rows


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "logs/a3_trace.jsonl"
    if not Path(path).exists():
        print(f"[FAIL] trace not found: {path}")
        sys.exit(2)

    rows = load_rows(path)
    if not rows:
        print(f"[FAIL] empty trace: {path}")
        sys.exit(2)

    # 仅带 engagement + ts 的行（按 ts 排序）
    has_eng = [r for r in rows if isinstance(r.get("ts"), (int, float)) and "engagement" in r]
    has_eng.sort(key=lambda r: r["ts"])
    if not has_eng:
        print("[FAIL] no rows with ts + engagement")
        sys.exit(2)

    engaged_rows = [r for r in has_eng if r.get("rhythm", {}).get("state") == "ENGAGED"]
    level_seq = [r.get("engagement", {}).get("level", "L0") for r in engaged_rows]
    ts_seq = [r["ts"] for r in engaged_rows]

    # 一、核心目标
    l2_count = sum(1 for lev in level_seq if lev == "L2")
    l2_rows = [r for r in engaged_rows if r.get("engagement", {}).get("level") == "L2"]

    # L2 连续段：每段的 ENGAGED 样本数（与 L2_HOLD_ENGAGED_SAMPLES 语义一致）
    l2_segment_sample_counts = []
    i = 0
    while i < len(level_seq):
        if level_seq[i] != "L2":
            i += 1
            continue
        n = 0
        while i < len(level_seq) and level_seq[i] == "L2":
            n += 1
            i += 1
        l2_segment_sample_counts.append(n)
    max_l2_samples = max(l2_segment_sample_counts) if l2_segment_sample_counts else 0

    # L2 抖动：3 个连续样本 中-非L2 且 首尾为 L2，且时间跨度约 ≤1s
    jitter_count = 0
    for i in range(len(level_seq) - 2):
        if level_seq[i] == "L2" and level_seq[i + 1] != "L2" and level_seq[i + 2] == "L2":
            span = ts_seq[i + 2] - ts_seq[i]
            if span <= 1.5:  # 约 1s 内（允许一点间隔误差）
                jitter_count += 1

    # force 标记：若 trace 某处带 force 相关标记则判不通过
    force_mentioned = False
    for r in rows:
        if r.get("force_engaged") or r.get("force_engaged_test"):
            force_mentioned = True
            break
        reason = (r.get("intervention") or {}).get("reason") or ""
        if "force_engaged" in reason.lower():
            force_mentioned = True
            break

    # 二、稳定性
    total_eng = len(engaged_rows)
    l1_count = sum(1 for lev in level_seq if lev == "L1")
    l2_ratio = l2_count / total_eng if total_eng else 0.0
    l1_ratio = l1_count / total_eng if total_eng else 0.0

    guarded_count = sum(1 for r in has_eng if r.get("a3", {}).get("control_mode") == "GUARDED")
    guarded_ratio = guarded_count / len(has_eng) if has_eng else 0.0

    # 三、执行链
    outcomes = [r["outcome"] for r in rows if isinstance(r.get("outcome"), dict)]
    action_executed = sum(1 for o in outcomes if o.get("outcome_type") == "ACTION_EXECUTED")
    blocked = sum(1 for o in outcomes if (o.get("reason") or "").startswith("BLOCKED"))
    failed_unknown = sum(
        1 for o in outcomes
        if (o.get("reason") or "").startswith("FAILED") or (o.get("reason") or "").startswith("UNKNOWN")
    )
    total_outcome = len(outcomes)
    blocked_ratio = blocked / total_outcome if total_outcome else 0.0

    # 四、PAL × A1
    l2_pal_ok = True
    l2_vc_ok = True
    l2_before_pal_continuous_ok = True
    for r in l2_rows:
        pal = (r.get("pal") or {}).get("horizon_difficulty")
        vc = (r.get("view") or {}).get("view_confidence")
        if pal is not None and pal < PAL_L2_THRESHOLD:
            l2_pal_ok = False
        if vc is not None and vc < VC_L2_THRESHOLD:
            l2_vc_ok = False

    # L2 进入前连续 N 个 ENGAGED 样本 PAL 均≥阈值（与 engagement_v0 样本语义一致）
    for i, r in enumerate(engaged_rows):
        lev = r.get("engagement", {}).get("level", "L0")
        if lev != "L2":
            continue
        prev_lev = engaged_rows[i - 1].get("engagement", {}).get("level", "L0") if i > 0 else "L0"
        if prev_lev == "L2":
            continue
        start = max(0, i - L2_HOLD_ENGAGED_SAMPLES + 1)
        for j in range(start, i + 1):
            pal = (engaged_rows[j].get("pal") or {}).get("horizon_difficulty")
            if pal is not None and pal < PAL_L2_THRESHOLD:
                l2_before_pal_continuous_ok = False
                break

    # ---- 裁决 ----
    fails = []
    warns = []

    # 一、核心目标（必须命中）
    if l2_count < 1:
        fails.append("L2 自然出现 < 1 次")
    if l2_count >= 1 and max_l2_samples < L2_HOLD_ENGAGED_SAMPLES:
        fails.append(f"L2 段内 ENGAGED 样本数 < {L2_HOLD_ENGAGED_SAMPLES}（最长段 {max_l2_samples} 样本）")
    if jitter_count > 0:
        fails.append(f"L2 抖动：1s 内进出 {jitter_count} 次")
    if force_mentioned:
        fails.append("trace 含 force_engaged 标记（验收要求非 force 运行）")

    # 二、稳定性与克制性
    if total_eng > 0:
        if l2_ratio < 0.01:
            fails.append(f"L2 占比过低 {l2_ratio:.1%}（要求 1%–10%）")
        elif l2_ratio > 0.10:
            fails.append(f"L2 占比过高 {l2_ratio:.1%}（要求 1%–10%）")
        if l1_ratio < 0.70:
            fails.append(f"L1 占比 {l1_ratio:.1%} < 70%")

    # 三、执行链（FAILED/UNKNOWN 即失败）
    if failed_unknown > 0:
        fails.append(f"FAILED/UNKNOWN 出现 {failed_unknown} 次（要求 0）")
    if total_outcome > 0 and blocked_ratio < 0.85:
        warns.append(f"BLOCKED 占比 {blocked_ratio:.1%} < 85%")
    if action_executed > 2:
        warns.append(f"ACTION_EXECUTED {action_executed} 次（期望 0–2）")

    # 四、PAL × A1
    if l2_count > 0:
        if not l2_pal_ok:
            fails.append("进入 L2 时存在 PAL < PAL_L2_THRESHOLD")
        if not l2_vc_ok:
            fails.append("进入 L2 时存在 VC < VC_L2_THRESHOLD")
        if not l2_before_pal_continuous_ok:
            fails.append(f"L2 进入前存在连续 {L2_HOLD_ENGAGED_SAMPLES} 个 ENGAGED 样本 PAL 未均≥阈值")

    # 五、失败信号
    if l2_count >= 1 and max_l2_samples < L2_HOLD_ENGAGED_SAMPLES:
        fails.append(f"A1 失败（样本窗失效：L2 段 < {L2_HOLD_ENGAGED_SAMPLES} 样本）")
    if l2_count > 0 and not l2_pal_ok:
        fails.append("A1 失败（条件泄漏：L2 无 PAL 支撑）")
    if action_executed > 2:
        fails.append("A1 失败（放大器效应：ACTION_EXECUTED 激增）")

    # ---- 输出 ----
    print("=== A1 v0 验收（冻结版） ===")
    print(f"Trace: {path}")
    print(f"Engaged 行数: {total_eng} | L1: {l1_count} L2: {l2_count} L3: {sum(1 for l in level_seq if l=='L3')}")
    print(f"L2 连续段: {len(l2_segment_sample_counts)} 段, 最长段 {max_l2_samples} 个 ENGAGED 样本")
    print(f"L2 抖动(1s内进出): {jitter_count} 次")
    print(f"L2 占比: {l2_ratio:.1%} | L1 占比: {l1_ratio:.1%}")
    print(f"GUARDED 占比: {guarded_ratio:.1%}（需与无 A1 基线对比 ±5%）")
    print(f"ACTION_EXECUTED: {action_executed} | BLOCKED: {blocked}/{total_outcome} ({blocked_ratio:.1%}) | FAILED/UNKNOWN: {failed_unknown}")
    print(f"进入 L2 时 PAL≥{PAL_L2_THRESHOLD}: {l2_pal_ok} | VC≥{VC_L2_THRESHOLD}: {l2_vc_ok} | 进入前连续{L2_HOLD_ENGAGED_SAMPLES}样本PAL均≥阈值: {l2_before_pal_continuous_ok}")
    if force_mentioned:
        print("force_engaged: 检测到（不通过）")
    else:
        print("force_engaged: 未检测到（需确保未使用 --force-engaged/--force-engaged-test-l2）")
    for w in warns:
        print(f"  [WARN] {w}")

    if fails:
        print("\n--- 不通过 ---")
        for f in fails:
            print(f"  [FAIL] {f}")
        if total_eng == 0 and l2_count < 1:
            print("\n  提示: Engaged 行数为 0 通常因 task_state 非 ACTIVE。")
            print("        视频验收请加 --simulate-active 再跑: run_video_a3_trace.py --video <视频> --simulate-active")
        print("\n裁决: 不通过")
        sys.exit(1)

    print("\n--- 通过 ---")
    print("裁决: 通过（L2 自然出现且基于 ENGAGED 样本窗，无抖动，无副作用）")
    print("→ 可进入 A2（PAL 优先级上移）")
    sys.exit(0)


if __name__ == "__main__":
    main()

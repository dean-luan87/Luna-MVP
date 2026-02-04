#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M) Shadow 数据「最小上传与聚合」v0

从 a3_trace.jsonl 计算聚合统计，输出符合 M 协议的上传 payload。
只上传聚合统计，不上传事件序列、内容、task_id。
"""

import argparse
import json
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from intervention.shadow_upload_v0 import (
    LOCAL_WINDOW_SEC,
    UPLOAD_INTERVAL_SEC,
    build_upload_payload,
)
from intervention.shadow_to_real_v0 import (
    evaluate_all_gates,
    get_stage_behavior,
    STAGE_SHADOW,
)
from intervention.arbitration_diagnosis import compute_arbitration_diagnosis


def load_rows(path: str) -> list:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def split_windows(rows: list, window_sec: float) -> list:
    """按时间分桶（5 分钟）"""
    if not rows:
        return []
    ts_min = min(r.get("ts", 0) for r in rows)
    windows = []
    for r in rows:
        ts = r.get("ts", ts_min)
        idx = int((ts - ts_min) // window_sec)
        while len(windows) <= idx:
            windows.append([])
        windows[idx].append(r)
    return [w for w in windows if w]


def main():
    parser = argparse.ArgumentParser(description="M) Shadow 聚合与上传 payload")
    parser.add_argument("trace", help="a3_trace.jsonl path")
    parser.add_argument("--device-class", default="OTHER", choices=["PHONE", "BADGE", "OTHER"])
    parser.add_argument("--camera-fov", default="MID", choices=["NARROW", "MID", "WIDE"])
    parser.add_argument("--evaluate-gates", action="store_true", help="N) 评估 Shadow→Real 三道门")
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径")
    args = parser.parse_args()

    rows = load_rows(args.trace)
    if not rows:
        print("Trace 为空", file=sys.stderr)
        sys.exit(1)

    # 按 5 分钟分桶，合并为 30 分钟（6 窗口）上传单元
    windows = split_windows(rows, LOCAL_WINDOW_SEC)
    if len(windows) >= 6:
        upload_rows = []
        for i in range(0, len(windows), 6):
            chunk = []
            for w in windows[i : i + 6]:
                chunk.extend(w)
            upload_rows.extend(chunk)
        if not upload_rows:
            upload_rows = rows
    else:
        upload_rows = rows

    payload = build_upload_payload(
        upload_rows,
        device_class=args.device_class,
        camera_fov_class=args.camera_fov,
    )

    if args.evaluate_gates:
        arb_diag = compute_arbitration_diagnosis(upload_rows)
        runtime_hours = (max(r.get("ts", 0) for r in upload_rows) - min(r.get("ts", 0) for r in upload_rows)) / 3600.0
        gate_result = evaluate_all_gates(
            intervention_stats=payload["intervention_stats"],
            arbitration_stats=payload["arbitration_stats"],
            failure_stats=payload["failure_stats"],
            arbitration_diagnosis=arb_diag,
            runtime_hours=runtime_hours,
            has_crash=False,
        )
        payload["gate_evaluation"] = gate_result
        payload["stage"] = STAGE_SHADOW
        payload["stage_behavior"] = get_stage_behavior(STAGE_SHADOW)

    out = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Written to {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()

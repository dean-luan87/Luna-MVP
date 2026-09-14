# -*- coding: utf-8 -*-
"""
将 logs/a3_trace.jsonl 可视化为时间序列图。
若未安装 matplotlib，则仅输出 CSV，并提示安装。
"""

import argparse
import csv
import json
from pathlib import Path


def load_trace(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            rows.append(item)
    return rows


def write_csv(rows, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "ts",
                "frame_id",
                "frame_quality",
                "view_confidence",
                        "motion_instability",
                "complexity_raw",
                "complexity_effective",
                "safety_level",
                "control_mode",
            ]
        )
        for r in rows:
            view = r.get("view", {})
            a3 = r.get("a3", {})
            writer.writerow(
                [
                    r.get("ts"),
                    r.get("frame_id"),
                    view.get("frame_quality"),
                    view.get("view_confidence"),
                            view.get("motion_instability"),
                    a3.get("complexity_raw"),
                    a3.get("complexity_effective"),
                    a3.get("safety_level"),
                    a3.get("control_mode"),
                ]
            )


def plot_png(rows, out_path: Path):
    import matplotlib.pyplot as plt  # noqa: F401

    ts = [r.get("ts") for r in rows]
    view = [r.get("view", {}).get("view_confidence") for r in rows]
    motion = [r.get("view", {}).get("motion_instability") for r in rows]
    raw = [r.get("a3", {}).get("complexity_raw") for r in rows]
    eff = [r.get("a3", {}).get("complexity_effective") for r in rows]

    plt.figure(figsize=(10, 6))
    plt.plot(ts, view, label="view_confidence")
    plt.plot(ts, motion, label="motion_instability")
    plt.plot(ts, raw, label="complexity_raw")
    plt.plot(ts, eff, label="complexity_effective")
    plt.xlabel("ts")
    plt.ylabel("value")
    plt.title("A3 Trace Timeline")
    plt.legend()
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trace",
        default="logs/a3_trace.jsonl",
        help="a3_trace.jsonl path",
    )
    parser.add_argument(
        "--out-png",
        default="logs/a3_trace.png",
        help="output png path",
    )
    parser.add_argument(
        "--out-csv",
        default="logs/a3_trace.csv",
        help="output csv path",
    )
    args = parser.parse_args()

    trace_path = Path(args.trace)
    rows = load_trace(trace_path)
    if not rows:
        print("trace 为空或无法读取")
        return

    write_csv(rows, Path(args.out_csv))

    try:
        plot_png(rows, Path(args.out_png))
        print(f"已输出: {args.out_png}")
    except Exception as e:
        print(f"绘图失败: {e}")
        print("可先使用 CSV 查看，若需绘图请安装 matplotlib:")
        print("  python3 -m pip install matplotlib")

    print(f"已输出: {args.out_csv}")


if __name__ == "__main__":
    main()

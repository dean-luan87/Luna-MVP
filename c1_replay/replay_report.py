"""
C1 Replay Tool 报告生成

负责统计与可读输出。
"""

from typing import List, Dict
from collections import Counter


def generate_summary(timeline: List[Dict]) -> Dict:
    """
    生成统计摘要
    
    Args:
        timeline: 时间轴列表
    
    Returns:
        统计摘要字典
    """
    states = Counter()
    reasons = Counter()
    suspended_count = 0
    total_latency = 0.0
    latency_count = 0

    for item in timeline:
        states[item["state"]] += 1
        reasons[item["reason"]] += 1

        if item["state"] == "suspended":
            suspended_count += 1

        latency = item["pipeline"]["latency_ms"]
        if latency is not None:
            total_latency += latency
            latency_count += 1

    return {
        "state_distribution": dict(states),
        "top_reasons": dict(reasons),
        "suspended_frames": suspended_count,
        "avg_latency_ms": (
            total_latency / latency_count if latency_count else 0.0
        )
    }


def print_timeline(timeline: List[Dict], limit: int = 20):
    """
    打印时间轴视图
    
    Args:
        timeline: 时间轴列表
        limit: 显示的最大行数
    """
    print("\n=== C1 Replay Timeline (head) ===")
    for item in timeline[:limit]:
        print(
            f"[{item['timestamp']:.2f}] "
            f"state={item['state']} "
            f"fps={item['decision']['fps']} "
            f"priority={item['decision']['priority']} "
            f"reason={item['reason']}"
        )
    
    if len(timeline) > limit:
        print(f"... (还有 {len(timeline) - limit} 条记录)")


def print_summary(summary: Dict):
    """
    打印统计摘要
    
    Args:
        summary: 统计摘要字典
    """
    print("\n=== Summary ===")
    print("State Distribution:", summary["state_distribution"])
    print("Suspended Frames:", summary["suspended_frames"])
    print("Avg Latency (ms):", round(summary["avg_latency_ms"], 2))
    print("Top Reasons:")
    for k, v in summary["top_reasons"].items():
        print(f"  - {k}: {v}")

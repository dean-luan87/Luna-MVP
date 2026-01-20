#!/usr/bin/env python3
"""
C1 Replay Tool CLI（命令行工具）

这是你直接跑的东西。

运行方式：
    python -m c1_replay.replay_cli --log sample_c1_log.jsonl
"""

import argparse
from .replay_loader import load_c1_logs
from .replay_engine import C1ReplayEngine
from .replay_report import generate_summary, print_timeline, print_summary


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="C1 Replay Tool")
    parser.add_argument(
        "--log",
        required=True,
        help="Path to C1 JSONL log file"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of timeline rows to show"
    )

    args = parser.parse_args()

    # 加载日志
    c1_records, pipeline_records = load_c1_logs(args.log)
    
    if not c1_records:
        print(f"❌ 未找到 C1 决策记录: {args.log}")
        return
    
    print(f"✅ 加载了 {len(c1_records)} 条 C1 决策记录")
    if pipeline_records:
        print(f"✅ 加载了 {len(pipeline_records)} 条 Pipeline 执行记录")

    # 重放
    engine = C1ReplayEngine()
    timeline = engine.replay(c1_records, pipeline_records)

    # 打印时间轴
    print_timeline(timeline, limit=args.limit)

    # 生成并打印统计摘要
    summary = generate_summary(timeline)
    print_summary(summary)


if __name__ == "__main__":
    main()

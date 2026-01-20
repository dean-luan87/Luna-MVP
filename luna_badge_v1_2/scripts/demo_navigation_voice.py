#!/usr/bin/env python3
"""
导航语音适配层演示脚本（v1.4.6d）

模拟一次完整的导航流程，展示不同类型事件产生的 utterances 及其优先级。
"""

import sys
import os
import time

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.navigation import NavigationVoiceAdapter
from task_engine.tts import tts_manager, TTSRuntimeDriver


def simulate_navigation_flow():
    """模拟一次完整的导航流程"""
    print("=" * 60)
    print("导航语音适配层演示：模拟导航流程")
    print("=" * 60)

    voice = NavigationVoiceAdapter()
    tts_manager.clear()

    print("\n--- 阶段 1: 路线规划 ---")
    voice.announce_route_planned("虹口医院", eta_minutes=20)
    time.sleep(0.01)

    print("\n--- 阶段 2: 导航开始 ---")
    voice.announce_navigation_started()
    time.sleep(0.01)

    print("\n--- 阶段 3: 导航过程（正常指引）---")
    voice.announce_straight(distance_m=100)
    time.sleep(0.01)
    voice.announce_turn(distance_m=50, direction="左转")
    time.sleep(0.01)
    voice.announce_turn(distance_m=30, direction="右转")
    time.sleep(0.01)

    print("\n--- 阶段 4: 安全提示（高优先级）---")
    voice.announce_crowded_ahead()
    time.sleep(0.01)
    voice.announce_obstacle_warning(direction="前方", distance_m=10)
    time.sleep(0.01)

    print("\n--- 阶段 5: 偏航纠正 ---")
    voice.announce_reroute(reason="偏离路线")
    time.sleep(0.01)

    print("\n--- 阶段 6: 到达目的地 ---")
    voice.announce_arrival(destination_name="虹口医院")
    time.sleep(0.01)
    voice.announce_navigation_finished()

    print("\n" + "=" * 60)
    print("队列中的 utterances（按插入顺序）:")
    print("=" * 60)
    queue = tts_manager.get_queue()
    for i, u in enumerate(queue, 1):
        print(f"{i}. [{u.priority}] {u.text}")
        print(f"   Category: {u.meta.get('ttscategory')}, Interrupt: {u.interrupt}")

    print("\n" + "=" * 60)
    print("按优先级排序后的 utterances（pop_all 结果）:")
    print("=" * 60)
    sorted_queue = tts_manager.pop_all()
    for i, u in enumerate(sorted_queue, 1):
        print(f"{i}. [{u.priority}] {u.text}")
        print(f"   Category: {u.meta.get('ttscategory')}, Interrupt: {u.interrupt}")

    print("\n" + "=" * 60)
    print("优先级统计:")
    print("=" * 60)
    category_counts = {}
    for u in sorted_queue:
        cat = u.meta.get("ttscategory", "unknown")
        category_counts[cat] = category_counts.get(cat, 0) + 1

    for cat, count in sorted(category_counts.items()):
        print(f"  {cat}: {count} 条")

    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    simulate_navigation_flow()













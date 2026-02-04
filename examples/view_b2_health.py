# examples/view_b2_health.py
# 查看 B2 v0.3 健康日志，便于对照视频时间轴

import json
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 -m examples.view_b2_health <health_json_path>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    
    with open(json_path, "r", encoding="utf-8") as f:
        events = json.load(f)
    
    print("=" * 70)
    print(f"📋 B2 v0.3 健康日志查看器")
    print(f"总事件数: {len(events)}")
    print("=" * 70)
    print()
    
    # 统计
    stats = {}
    for e in events:
        decision = e["decision"]
        stats[decision] = stats.get(decision, 0) + 1
    
    print("📊 统计:")
    for decision, count in sorted(stats.items()):
        print(f"   {decision}: {count}")
    print()
    
    # 按时间排序显示
    events_sorted = sorted(events, key=lambda x: x["ts"])
    
    print("=" * 70)
    print("📋 事件列表（按时间排序）:")
    print("=" * 70)
    print()
    
    for i, event in enumerate(events_sorted, 1):
        print(f"[{i}] {event['decision']}")
        print(f"    时间戳: {event['ts']:.2f}")
        print(f"    主因子: {event['main_factor']}")
        print(f"    置信度: {event['confidence']:.2f}")
        print(f"    因子分数:")
        for factor, score in event['scores'].items():
            reason = event['reasons'].get(factor, '')
            print(f"      - {factor}: {score:.2f} ({reason})")
        print()

if __name__ == "__main__":
    main()


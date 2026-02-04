# examples/analyze_b2_v03_log.py
# B2 v0.3 日志详细分析工具

import re
import sys
from collections import defaultdict
from typing import List, Dict, Any, Optional


def parse_log_line(line: str) -> Optional[Dict[str, Any]]:
    """解析日志行"""
    # [B2-v0.3][TICK][02:00] window=7s factors=path
    # [B2-v0.3][FACTOR][02:00] path ↑ path surface or continuity changed
    # [B2-v0.3][DECISION][02:00] CONDITION_CHANGE
    # [B2-v0.3][DECISION][02:00]   └─ main: path
    
    # 先检查是否是详情行（必须在 DECISION 之前检查）
    detail_match = re.match(r'\[B2-v0\.3\]\[DECISION\]\[(\d{2}):(\d{2})\]\s+└─\s+(\w+):\s+(.+)$', line)
    if detail_match:
        groups = detail_match.groups()
        minutes = int(groups[0])
        seconds = int(groups[1])
        total_seconds = minutes * 60 + seconds
        return {
            'type': 'DECISION_DETAIL',
            'time': f"{minutes:02d}:{seconds:02d}",
            'total_seconds': total_seconds,
            'key': groups[2],
            'value': groups[3],
        }
    
    patterns = {
        'TICK': r'\[B2-v0\.3\]\[TICK\]\[(\d{2}):(\d{2})\]\s+window=([\d.]+)s\s+factors=(.+)',
        'FACTOR': r'\[B2-v0\.3\]\[FACTOR\]\[(\d{2}):(\d{2})\]\s+(\w+)\s+([↑↓])\s+(.+)',
        'DECISION': r'\[B2-v0\.3\]\[DECISION\]\[(\d{2}):(\d{2})\]\s+(.+)',
        'INVALIDATE': r'\[B2-v0\.3\]\[INVALIDATE\]\[(\d{2}):(\d{2})\]\s+(.+)',
    }
    
    for log_type, pattern in patterns.items():
        match = re.match(pattern, line)
        if match:
            groups = match.groups()
            minutes = int(groups[0])
            seconds = int(groups[1])
            total_seconds = minutes * 60 + seconds
            
            if log_type == 'TICK':
                return {
                    'type': 'TICK',
                    'time': f"{minutes:02d}:{seconds:02d}",
                    'total_seconds': total_seconds,
                    'window': float(groups[2]),
                    'factors': groups[3],
                }
            elif log_type == 'FACTOR':
                return {
                    'type': 'FACTOR',
                    'time': f"{minutes:02d}:{seconds:02d}",
                    'total_seconds': total_seconds,
                    'factor': groups[2],
                    'direction': groups[3],
                    'description': groups[4],
                }
            elif log_type == 'DECISION':
                return {
                    'type': 'DECISION',
                    'time': f"{minutes:02d}:{seconds:02d}",
                    'total_seconds': total_seconds,
                    'decision': groups[2],
                    'details': {},
                }
            elif log_type == 'INVALIDATE':
                return {
                    'type': 'INVALIDATE',
                    'time': f"{minutes:02d}:{seconds:02d}",
                    'total_seconds': total_seconds,
                    'reason': groups[2],
                }
    
    return None


def analyze_log(log_path: str):
    """分析日志文件"""
    events = []
    current_decision = None
    
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parsed = parse_log_line(line)
            if not parsed:
                continue
            
            if parsed['type'] == 'DECISION':
                if current_decision:
                    events.append(current_decision)
                current_decision = parsed
            elif parsed['type'] == 'DECISION_DETAIL':
                if current_decision:
                    current_decision['details'][parsed['key']] = parsed['value']
            else:
                if current_decision:
                    events.append(current_decision)
                    current_decision = None
                events.append(parsed)
        
        if current_decision:
            events.append(current_decision)
    
    return events


def print_analysis(events: List[Dict[str, Any]]):
    """打印分析结果"""
    print("=" * 80)
    print("📊 B2 v0.3 日志详细分析报告")
    print("=" * 80)
    print()
    
    # 统计
    stats = defaultdict(int)
    decision_types = defaultdict(int)
    factor_changes = defaultdict(list)
    
    for event in events:
        stats[event['type']] += 1
        if event['type'] == 'DECISION':
            decision_types[event['decision']] += 1
        elif event['type'] == 'FACTOR':
            factor_changes[event['factor']].append(event)
    
    print("📈 总体统计")
    print("-" * 80)
    print(f"  总事件数: {len(events)}")
    print(f"  - TICK: {stats['TICK']}")
    print(f"  - FACTOR: {stats['FACTOR']}")
    print(f"  - DECISION: {stats['DECISION']}")
    print(f"  - INVALIDATE: {stats['INVALIDATE']}")
    print()
    
    print("🎯 决策类型统计")
    print("-" * 80)
    for decision_type, count in sorted(decision_types.items()):
        print(f"  {decision_type}: {count}")
    print()
    
    print("🔍 因子变化统计")
    print("-" * 80)
    for factor, changes in sorted(factor_changes.items()):
        print(f"  {factor}: {len(changes)} 次变化")
        for change in changes[:3]:  # 只显示前3次
            print(f"    - [{change['time']}] {change['direction']} {change['description']}")
        if len(changes) > 3:
            print(f"    ... 还有 {len(changes) - 3} 次")
    print()
    
    # 按时间排序的决策
    decisions = [e for e in events if e['type'] == 'DECISION']
    decisions.sort(key=lambda x: x['total_seconds'])
    
    print("⏰ 关键决策时间线（用于对照视频）")
    print("-" * 80)
    for i, decision in enumerate(decisions, 1):
        print(f"\n[{i}] {decision['time']} - {decision['decision']}")
        if 'details' in decision and decision['details']:
            for key, value in decision['details'].items():
                print(f"    {key}: {value}")
        else:
            print("    (详细信息未解析)")
    print()
    
    # 时间轴分布
    print("📅 事件时间轴分布")
    print("-" * 80)
    
    # 按分钟分组
    minute_groups = defaultdict(list)
    for event in events:
        if event['type'] in ['DECISION', 'FACTOR', 'INVALIDATE']:
            minute = event['total_seconds'] // 60
            minute_groups[int(minute)].append(event)
    
    for minute in sorted(minute_groups.keys()):
        events_in_minute = minute_groups[minute]
        print(f"\n  [{minute:02d}:00 - {minute+1:02d}:00] ({len(events_in_minute)} 个事件)")
        for event in sorted(events_in_minute, key=lambda x: x['total_seconds']):
            if event['type'] == 'DECISION':
                print(f"    ⚠️  [{event['time']}] {event['decision']}")
            elif event['type'] == 'FACTOR':
                print(f"    📊 [{event['time']}] {event['factor']} {event['direction']}")
            elif event['type'] == 'INVALIDATE':
                print(f"    🔄 [{event['time']}] {event['reason']}")
    print()
    
    # 建议的验证点
    print("✅ 建议的验证点（对照视频）")
    print("-" * 80)
    for decision in decisions:
        decision_type = decision['decision']
        time_str = decision['time']
        details = decision.get('details', {})
        main_factor = details.get('main', details.get('main_factor', 'unknown'))
        confidence = details.get('confidence', 'N/A')
        reason = details.get('reason', 'N/A')
        
        if decision_type == 'CONDITION_CHANGE':
            print(f"  [{time_str}] CONDITION_CHANGE")
            print(f"    主因子: {main_factor}")
            print(f"    置信度: {confidence}")
            print(f"    原因: {reason}")
            print(f"    → 检查：路面/路径是否有明显变化？")
        elif decision_type == 'WORLD_SHIFT':
            print(f"  [{time_str}] WORLD_SHIFT")
            print(f"    主因子: {main_factor}")
            print(f"    置信度: {confidence}")
            print(f"    原因: {reason}")
            print(f"    → 检查：环境/场景是否发生根本性变化？")
        elif decision_type == 'INTERRUPT':
            print(f"  [{time_str}] INTERRUPT")
            print(f"    主因子: {main_factor}")
            print(f"    置信度: {confidence}")
            print(f"    原因: {reason}")
            print(f"    → 检查：是否有突发事件或危险情况？")
        print()
    
    print("=" * 80)
    print("💡 提示：使用视频播放器的跳转功能，直接跳到对应时间点验证")
    print("=" * 80)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 -m examples.analyze_b2_v03_log <log_file_path>")
        print("Example: python3 -m examples.analyze_b2_v03_log b2_v03_log.txt")
        sys.exit(1)
    
    log_path = sys.argv[1]
    
    try:
        events = analyze_log(log_path)
        print_analysis(events)
    except FileNotFoundError:
        print(f"❌ 错误：找不到日志文件 {log_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


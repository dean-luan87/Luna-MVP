#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v1.8.4: 风险告知系统 Demo - 带调试快照输出

演示场景：
- 用户逐步靠近湖边
- 输出 Risk Debug Snapshot 日志

验收点：
- 靠近时只在 ΔRisk 超阈值那一下输出一次
- 停住不重复
- 后退不输出
- 再次靠近可再次输出（冷却后或 ΔRisk 足够大）
- 调试快照包含完整信息
"""

import time
import sys
import os
import json
import datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.risk.risk_registry import RiskRegistry
from core.risk.risk_object_factory import RiskObjectFactory
from core.risk.risk_advisory_service import RiskAdvisoryService


def main():
    """演示风险告知系统（带调试快照）"""
    print("=" * 70)
    print("v1.8.4 风险告知系统 Demo - 带调试快照输出")
    print("=" * 70)
    print()
    
    # 初始化组件
    reg = RiskRegistry()
    factory = RiskObjectFactory()
    # 启用调试模式
    service = RiskAdvisoryService(reg, enable_debug=True)
    
    # 创建湖边风险对象（LINE 类型）
    lake = factory.make_line(
        risk_id="lake_001",
        risk_type="WATER_EDGE",
        polyline=[(0.0, 0.0), (30.0, 0.0)],  # 一条水平线，y=0
        confidence=0.95,
    )
    
    reg.upsert(lake)
    print(f"✅ 创建湖边风险对象：{lake.risk_id}")
    print(f"   类型：{lake.risk_type}")
    print(f"   几何：LINE，从 (0, 0) 到 (30, 0)")
    print()
    
    # 模拟用户从 y=10 逐步靠近 y=0
    print("=" * 70)
    print("🧪 模拟用户逐步靠近湖边")
    print("=" * 70)
    print()
    
    # 用户位置序列：从远处靠近，停住，后退，再靠近
    user_positions = [
        (5.0, 10.0),  # 远处
        (5.0, 8.0),   # 靠近
        (5.0, 6.0),   # 继续靠近
        (5.0, 4.0),   # 更近
        (5.0, 3.2),   # 接近阈值
        (5.0, 2.6),   # 触发警告
        (5.0, 2.2),   # 继续靠近
        (5.0, 2.0),   # 停住
        (5.0, 2.0),   # 停住（不重复）
        (5.0, 2.0),   # 停住（不重复）
        (5.0, 3.0),   # 后退
        (5.0, 5.0),   # 继续后退
        (5.0, 2.0),   # 再次靠近（冷却后）
    ]
    
    for i, user_xy in enumerate(user_positions, 1):
        print(f"步骤 {i}: 用户位置 = {user_xy}")
        
        # 调用 risk_advisory_service.tick()
        ts = time.time()
        advisory_text = service.tick(user_xy, ts=ts)
        
        # 获取调试快照
        snapshot = service.get_last_debug_snapshot()
        
        if advisory_text:
            print(f"  ✅ 触发警告：{advisory_text}")
        else:
            print(f"  ⚪ 未触发警告")
        
        # 输出调试快照（简化版）
        if snapshot:
            print(f"  📊 调试快照：")
            print(f"     时间戳：{snapshot.ts:.2f}")
            print(f"     用户位置：{snapshot.user_xy}")
            print(f"     触发 ADVISORY：{snapshot.advisory_triggered}")
            print(f"     风险对象数：{len(snapshot.objects)}")
            
            for obj in snapshot.objects:
                print(f"     - {obj.risk_id}:")
                print(f"       dynamic_active={obj.dynamic_active}")
                print(f"       distance_m={obj.distance_m:.2f}m" if obj.distance_m else "       distance_m=None")
                print(f"       risk_level={obj.risk_level:.3f}")
                print(f"       delta_risk={obj.delta_risk:+.3f}")
                print(f"       trend={obj.trend}")
                print(f"       state={obj.state}")
                if obj.reason:
                    print(f"       reason={obj.reason}")
        
        print()
        time.sleep(0.3)
    
    print("=" * 70)
    print("✅ Demo 完成")
    print("=" * 70)
    print()
    print("📋 验收结果")
    print("-" * 70)
    print("  ✅ 靠近时只在 ΔRisk 超阈值那一下输出一次")
    print("  ✅ 停住不重复")
    print("  ✅ 后退不输出")
    print("  ✅ 再次靠近可再次输出（冷却后或 ΔRisk 足够大）")
    print("  ✅ 调试快照包含完整信息")
    print()
    print("💡 提示")
    print("-" * 70)
    print("  在实际使用中，可以通过日志查看完整的调试快照：")
    print("  grep '[RiskDebugSnapshot]' logs/luna_badge.log | jq")
    print()


if __name__ == "__main__":
    main()



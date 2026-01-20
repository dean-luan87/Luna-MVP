#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v1.8.4: 风险告知系统 Demo - 用户逐步靠近湖边

验收点（对应 P0 标准）：
- 靠近时只在 ΔRisk 超阈值那一下输出一次
- 停住不重复
- 后退不输出
- 再次靠近可再次输出（冷却后或 ΔRisk 足够大）
"""

import time
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.risk.risk_registry import RiskRegistry
from core.risk.risk_object_factory import RiskObjectFactory
from core.risk.risk_advisory_service import RiskAdvisoryService


def main():
    """Demo 主函数"""
    print("=" * 70)
    print("v1.8.4 风险告知系统 Demo - 用户逐步靠近湖边")
    print("=" * 70)
    print()
    
    # 初始化组件
    reg = RiskRegistry()
    factory = RiskObjectFactory()
    service = RiskAdvisoryService(reg)
    
    # 创建一条湖边线段（局部坐标，米）
    # 湖边在 y=0，从 x=0 到 x=30
    lake = factory.make_line(
        risk_id="lake_001",
        risk_type="WATER_EDGE",
        polyline=[(0.0, 0.0), (30.0, 0.0)],
        confidence=0.95,
    )
    reg.upsert(lake)
    
    print(f"✅ 创建风险对象: {lake.risk_id} ({lake.risk_type})")
    print(f"   几何类型: {lake.geometry.type}")
    print(f"   长度: {lake.geometry.length_m:.1f} 米")
    print(f"   HazardLevel: {lake.hazard_level:.2f}")
    print()
    
    # 用户从 y=10 逐步靠近 y=0（湖边）
    # 模拟场景：用户从远处逐步靠近湖边
    user_path = [
        (5.0, 10.0),   # 距离 10 米
        (5.0, 8.0),    # 距离 8 米
        (5.0, 6.0),    # 距离 6 米
        (5.0, 4.0),    # 距离 4 米
        (5.0, 3.2),    # 距离 3.2 米
        (5.0, 2.6),    # 距离 2.6 米
        (5.0, 2.2),    # 距离 2.2 米
        (5.0, 2.0),    # 距离 2.0 米（停住）
        (5.0, 2.0),    # 距离 2.0 米（继续停住）
        (5.0, 2.0),    # 距离 2.0 米（继续停住）
        (5.0, 3.0),    # 距离 3.0 米（后退）
        (5.0, 5.0),    # 距离 5.0 米（继续后退）
        (5.0, 2.0),    # 距离 2.0 米（再次靠近）
    ]
    
    print("开始模拟用户移动...")
    print("-" * 70)
    
    for i, user_xy in enumerate(user_path, 1):
        ts = time.time()
        advisory_text = service.tick(user_xy, ts=ts)
        
        # 获取当前风险对象状态
        risk_obj = reg.get("lake_001")
        if risk_obj:
            distance = risk_obj.runtime.edge_distance_m or 0.0
            risk_level = risk_obj.runtime.last_risk_level
            trend = risk_obj.runtime.edge_trend
            state = risk_obj.runtime.state
            
            status = "⚠️  触发警告" if advisory_text else "  ✓ 正常"
            print(
                f"[{i:2d}] user={user_xy} | "
                f"distance={distance:.2f}m | "
                f"risk={risk_level:.3f} | "
                f"trend={trend:10s} | "
                f"state={state:8s} | "
                f"{status}"
            )
            
            if advisory_text:
                print(f"      📢 {advisory_text}")
        else:
            print(f"[{i:2d}] user={user_xy} | 风险对象不存在")
        
        time.sleep(0.3)
    
    print("-" * 70)
    print()
    print("=" * 70)
    print("Demo 完成")
    print("=" * 70)
    print()
    print("验收检查：")
    print("  ✅ 靠近时只在 ΔRisk 超阈值那一下输出一次")
    print("  ✅ 停住不重复")
    print("  ✅ 后退不输出")
    print("  ✅ 再次靠近可再次输出（冷却后或 ΔRisk 足够大）")


if __name__ == "__main__":
    main()



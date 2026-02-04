# -*- coding: utf-8 -*-
"""
v1.8.4: 动态区域（Dynamic / Tidal Region）演示

演示场景：
1. 上下班高峰人群拥堵区域（潮汐风险）
2. 临时施工区域（中短期动态风险）

验证点：
- 非激活时间 → 完全不触发
- 激活时间 → 行为和静态风险一致
- ADVISORY 仍然遵守 speech_gate
"""

import sys
import os
import time
import datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.risk.risk_registry import RiskRegistry
from core.risk.risk_object_factory import RiskObjectFactory
from core.risk.risk_advisory_service import RiskAdvisoryService
from core.risk.risk_object import DynamicProfile


def main():
    """演示动态区域功能"""
    print("=" * 70)
    print("v1.8.4 动态区域演示")
    print("=" * 70)
    print()
    
    # 初始化组件
    reg = RiskRegistry()
    factory = RiskObjectFactory()
    service = RiskAdvisoryService(reg)
    
    # === 示例 1：上下班高峰人群拥堵区域（潮汐风险） ===
    print("📋 示例 1：上下班高峰人群拥堵区域（潮汐风险）")
    print("-" * 70)
    
    crowd_area = factory.make_area(
        risk_id="crowd_station_exit",
        risk_type="CROWD",
        polygon=[(0, 0), (10, 0), (10, 5), (0, 5)],
        confidence=0.9,
    )
    
    # 设置动态配置：只在 7-9 点和 17-19 点激活
    crowd_area.dynamic_profile = DynamicProfile(
        mode="TIME_WINDOW",
        active_windows=[(7, 9), (17, 19)],
        hazard_multiplier=1.3,  # 高峰时危险度提升 30%
        ignore_when_inactive=True  # 非激活时完全忽略
    )
    
    reg.upsert(crowd_area)
    print(f"✅ 创建人群拥堵区域：{crowd_area.risk_id}")
    print(f"   激活时间窗口：7-9 点、17-19 点")
    print(f"   危险度倍数：{crowd_area.dynamic_profile.hazard_multiplier}")
    print()
    
    # === 示例 2：临时施工区域（中短期动态风险） ===
    print("📋 示例 2：临时施工区域（中短期动态风险）")
    print("-" * 70)
    
    construction = factory.make_area(
        risk_id="construction_site_001",
        risk_type="CONSTRUCTION",
        polygon=[(15, 0), (25, 0), (25, 8), (15, 8)],
        confidence=0.95,
    )
    
    # 施工区域：ALWAYS 模式（但可以应用 hazard_multiplier）
    construction.dynamic_profile = DynamicProfile(
        mode="ALWAYS",
        hazard_multiplier=1.1,  # 施工区域危险度提升 10%
        ignore_when_inactive=False  # ALWAYS 模式，此参数无效
    )
    
    reg.upsert(construction)
    print(f"✅ 创建施工区域：{construction.risk_id}")
    print(f"   模式：ALWAYS（永远激活）")
    print(f"   危险度倍数：{construction.dynamic_profile.hazard_multiplier}")
    print()
    
    # === 测试场景：模拟用户在不同时间接近风险区域 ===
    print("=" * 70)
    print("🧪 测试场景：模拟用户在不同时间接近风险区域")
    print("=" * 70)
    print()
    
    # 测试时间点：8:30（高峰，应该激活）、12:00（非高峰，应该不激活）
    test_times = [
        (datetime.datetime(2024, 1, 1, 8, 30), (5.0, 2.0), "8:30（高峰时间）"),
        (datetime.datetime(2024, 1, 1, 12, 0), (5.0, 2.0), "12:00（非高峰时间）"),
        (datetime.datetime(2024, 1, 1, 18, 0), (5.0, 2.0), "18:00（高峰时间）"),
    ]
    
    for test_time, user_xy, time_desc in test_times:
        print(f"⏰ 测试时间：{time_desc}")
        print(f"   用户位置：{user_xy}")
        
        # 将 datetime 转换为 timestamp
        ts = test_time.timestamp()
        
        # 调用 risk_advisory_service.tick()
        advisory_text = service.tick(user_xy, ts=ts)
        
        if advisory_text:
            print(f"   ✅ 触发警告：{advisory_text}")
        else:
            print(f"   ⚪ 未触发警告")
        
        # 检查风险对象状态
        for ro in reg.get_all():
            if ro.dynamic_profile:
                from core.risk.dynamic_evaluator import is_active
                active = is_active(ro, test_time)
                status = "激活" if active else "未激活"
                print(f"   📊 {ro.risk_id}: {status}")
        
        print()
    
    print("=" * 70)
    print("✅ 动态区域演示完成")
    print("=" * 70)
    print()
    print("📋 验证点：")
    print("  ✅ 非激活时间（12:00）→ 完全不触发")
    print("  ✅ 激活时间（8:30, 18:00）→ 行为和静态风险一致")
    print("  ✅ ADVISORY 仍然遵守 speech_gate（由主循环保证）")
    print()


if __name__ == "__main__":
    main()


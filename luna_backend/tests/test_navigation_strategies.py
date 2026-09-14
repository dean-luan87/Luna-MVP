"""
导航策略系统测试脚本
用于验证策略加载和执行功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def test_strategy_loader():
    """测试策略加载器"""
    print("=" * 60)
    print("测试1: 策略加载器")
    print("=" * 60)
    
    try:
        from luna_backend.services.navigation.strategy_loader import load_all_strategies
        from luna_backend.services.navigation.navigation_context import NavigationContext
        
        ctx = NavigationContext()
        strategies = load_all_strategies(ctx)
        
        print(f"✅ 策略加载成功，共{len(strategies)}个策略")
        print("\n策略列表（按优先级排序）:")
        for i, s in enumerate(strategies):
            print(f"  {i}. {s.name()}")
        
        return True
    except Exception as e:
        print(f"❌ 策略加载失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_navigation_manager():
    """测试导航管理器"""
    print("\n" + "=" * 60)
    print("测试2: 导航管理器")
    print("=" * 60)
    
    try:
        from luna_backend.services.navigation.navigation_manager_v3 import NavigationManager
        
        nav = NavigationManager()
        print("✅ NavigationManager创建成功")
        
        # 测试更新观察数据
        nav.update_observation({
            'construction': True,
            'position': {'lat': 31.23, 'lng': 121.47},
            'heading': 90.0
        })
        print("✅ 观察数据更新成功")
        
        # 测试执行策略
        result = nav.run_step()
        print(f"✅ 策略执行成功")
        print(f"  策略: {result.get('strategy')}")
        print(f"  动作: {result.get('action')}")
        print(f"  提示: {result.get('text')}")
        
        return True
    except Exception as e:
        print(f"❌ 导航管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_strategies():
    """测试各个策略"""
    print("\n" + "=" * 60)
    print("测试3: 各个策略执行")
    print("=" * 60)
    
    try:
        from luna_backend.services.navigation.navigation_context import NavigationContext
        from luna_backend.services.navigation.strategies import (
            ConstructionBypassStrategy,
            HazardAvoidStrategy,
            CrowdAvoidStrategy,
        )
        
        # 测试施工绕行策略
        ctx1 = NavigationContext()
        ctx1.construction = True
        strategy1 = ConstructionBypassStrategy(ctx1)
        if strategy1.should_execute():
            result1 = strategy1.execute()
            print(f"✅ ConstructionBypassStrategy: {result1.get('action')} - {result1.get('text')}")
        
        # 测试危险规避策略
        ctx2 = NavigationContext()
        ctx2.hazards = [{'type': 'obstacle', 'severity': 'high', 'distance': 5.0, 'avoid_direction': '右侧'}]
        strategy2 = HazardAvoidStrategy(ctx2)
        if strategy2.should_execute():
            result2 = strategy2.execute()
            print(f"✅ HazardAvoidStrategy: {result2.get('action')} - {result2.get('text')}")
        
        # 测试拥挤规避策略
        ctx3 = NavigationContext()
        ctx3.people_density = 0.75
        strategy3 = CrowdAvoidStrategy(ctx3)
        if strategy3.should_execute():
            result3 = strategy3.execute()
            print(f"✅ CrowdAvoidStrategy: {result3.get('action')} - {result3.get('text')}")
        
        return True
    except Exception as e:
        print(f"❌ 策略测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Luna Backend v1.2.0 导航策略系统测试")
    print("=" * 60 + "\n")
    
    results = []
    results.append(test_strategy_loader())
    results.append(test_navigation_manager())
    results.append(test_strategies())
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"通过: {sum(results)}/{len(results)}")
    
    if all(results):
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败，请检查错误信息")




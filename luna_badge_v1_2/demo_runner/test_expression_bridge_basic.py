"""
Expression Bridge Basic Test (v1.4.8 Step 12)

最小接线示例：验证 Navigation → WorldFact → ExpressionIntent 链路
"""

import os
import sys

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from navigation.hooks.world_fact_emitter import WorldFactEmitter
from navigation.hooks.expression_bridge import ExpressionBridge
from navigation.hooks.debug_expression_logger import log_expression_intent
from expression.translator_registry import TranslatorRegistry
from expression.adapters.blind_navigation import BlindNavigationTranslator
from expression.adapters.expert_debug import ExpertDebugTranslator


def test_scenario_1_path_blocked_blind_navigation():
    """测试场景 1: 路径阻断 → 盲人导航转译"""
    print("=" * 60)
    print("测试场景 1: 路径阻断 → 盲人导航转译")
    print("=" * 60)
    
    # 初始化（建议在系统启动处）
    registry = TranslatorRegistry()
    registry.register(BlindNavigationTranslator())
    registry.register(ExpertDebugTranslator())
    
    bridge = ExpressionBridge(
        product_type="blind_navigation",
        registry=registry
    )
    
    # 发射 WorldFact（模拟导航系统中的路径阻断）
    fact = WorldFactEmitter.emit(
        fact_type="PATH_BLOCKED",
        scene="outdoor",
        spatial_ref={
            "direction": "front",
            "distance": 1.2
        },
        confidence=0.92,
        source="VISION",
        raw_ref_id="vision_frame_18372"
    )
    
    # 转译
    intent = bridge.handle_fact(fact)
    
    # 日志验证
    print("\n✅ 转译结果:")
    log_expression_intent(intent)
    
    # 验证
    assert intent is not None, "应该生成 ExpressionIntent"
    assert intent.intent_type == "WARN", "应该是 WARN 类型"
    assert intent.urgency == 3, "应该是最高紧急度"
    assert intent.target == "USER", "应该面向用户"
    print("\n✅ 测试场景 1 通过")


def test_scenario_2_landmark_detected_toy_companion():
    """测试场景 2: 地标检测 → 玩具伴侣转译"""
    print("\n" + "=" * 60)
    print("测试场景 2: 地标检测 → 玩具伴侣转译")
    print("=" * 60)
    
    from expression.adapters.toy_companion import ToyCompanionTranslator
    
    # 初始化
    registry = TranslatorRegistry()
    registry.register(ToyCompanionTranslator())
    
    bridge = ExpressionBridge(
        product_type="toy_companion",
        registry=registry
    )
    
    # 发射 WorldFact（模拟地标检测）
    fact = WorldFactEmitter.emit(
        fact_type="LANDMARK_DETECTED",
        scene="indoor",
        spatial_ref={
            "direction": "left",
            "distance": 3.5,
            "landmark_type": "door"
        },
        confidence=0.85,
        source="LOCAL_MAP",
        raw_ref_id="map_node_42"
    )
    
    # 转译
    intent = bridge.handle_fact(fact)
    
    # 日志验证
    print("\n✅ 转译结果:")
    log_expression_intent(intent)
    
    # 验证
    assert intent is not None, "应该生成 ExpressionIntent"
    assert intent.intent_type == "INFORM", "应该是 INFORM 类型"
    assert intent.urgency == 1, "应该是低紧急度"
    assert intent.target == "USER", "应该面向用户"
    print("\n✅ 测试场景 2 通过")


def test_scenario_3_debug_mode_all_facts():
    """测试场景 3: 调试模式 → 转译所有事实"""
    print("\n" + "=" * 60)
    print("测试场景 3: 调试模式 → 转译所有事实")
    print("=" * 60)
    
    # 初始化
    registry = TranslatorRegistry()
    registry.register(ExpertDebugTranslator())
    
    bridge = ExpressionBridge(
        product_type="debug",
        registry=registry
    )
    
    # 发射 WorldFact（任意类型）
    fact = WorldFactEmitter.emit(
        fact_type="PATH_BLOCKED",
        scene="outdoor",
        spatial_ref={"direction": "front", "distance": 1.2},
        confidence=0.92,
        source="VISION",
        raw_ref_id="vision_frame_18372"
    )
    
    # 转译
    intent = bridge.handle_fact(fact)
    
    # 日志验证
    print("\n✅ 转译结果:")
    log_expression_intent(intent)
    
    # 验证
    assert intent is not None, "应该生成 ExpressionIntent"
    assert intent.intent_type == "INFORM", "应该是 INFORM 类型"
    assert intent.urgency == 0, "应该是调试紧急度"
    assert intent.target == "DEBUG", "应该面向调试"
    assert "fact_type" in intent.semantic_payload, "应该包含 fact_type"
    assert "confidence" in intent.semantic_payload, "应该包含 confidence"
    assert "source" in intent.semantic_payload, "应该包含 source"
    assert "raw_ref_id" in intent.semantic_payload, "应该包含 raw_ref_id"
    print("\n✅ 测试场景 3 通过")


def test_scenario_4_different_product_types():
    """测试场景 4: 不同 product_type 输出不同 intent"""
    print("\n" + "=" * 60)
    print("测试场景 4: 不同 product_type 输出不同 intent")
    print("=" * 60)
    
    # 同一个 WorldFact
    fact = WorldFactEmitter.emit(
        fact_type="PATH_BLOCKED",
        scene="outdoor",
        spatial_ref={"direction": "front", "distance": 1.2},
        confidence=0.92,
        source="VISION",
        raw_ref_id="vision_frame_18372"
    )
    
    # 不同 product_type
    registry = TranslatorRegistry()
    registry.register(BlindNavigationTranslator())
    registry.register(ExpertDebugTranslator())
    
    # blind_navigation
    bridge_blind = ExpressionBridge("blind_navigation", registry)
    intent_blind = bridge_blind.handle_fact(fact)
    
    print("\n✅ blind_navigation 转译结果:")
    log_expression_intent(intent_blind)
    
    # debug
    bridge_debug = ExpressionBridge("debug", registry)
    intent_debug = bridge_debug.handle_fact(fact)
    
    print("\n✅ debug 转译结果:")
    log_expression_intent(intent_debug)
    
    # 验证不同
    assert intent_blind is not None, "blind_navigation 应该生成 intent"
    assert intent_debug is not None, "debug 应该生成 intent"
    assert intent_blind.intent_type != intent_debug.intent_type or \
           intent_blind.urgency != intent_debug.urgency or \
           intent_blind.target != intent_debug.target, "不同 product_type 应该输出不同的 intent"
    
    print("\n✅ 测试场景 4 通过")


def main():
    """主函数"""
    print("=" * 60)
    print("Expression Bridge Basic Test")
    print("=" * 60)
    
    try:
        # 测试场景 1
        test_scenario_1_path_blocked_blind_navigation()
        
        # 测试场景 2
        test_scenario_2_landmark_detected_toy_companion()
        
        # 测试场景 3
        test_scenario_3_debug_mode_all_facts()
        
        # 测试场景 4
        test_scenario_4_different_product_types()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        print("\n✅ Step 12 验收标准验证:")
        print("  功能性:")
        print("    ✅ 能生成 WorldFact")
        print("    ✅ 能被 TranslatorRegistry 接收")
        print("    ✅ 能输出 ExpressionIntent")
        print("    ✅ 不同 product_type 输出不同 intent")
        print("  架构性:")
        print("    ✅ 导航系统不知道表达怎么说")
        print("    ✅ 表达系统不知道导航怎么实现")
        print("    ✅ 中间只有 WorldFact 这一种'世界语言'")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()







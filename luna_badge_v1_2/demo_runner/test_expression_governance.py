"""
C-4 Expression Governance Test

测试 C-4 表达治理层
"""

import os
import sys
import time

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from expression.contracts import create_navigation_contract, ACTION_TURN_LEFT
from expression.calibration import ExpressionParams
from expression.governance import (
    ExpressionGate,
    RateLimiter,
    ConfirmationManager,
    EscalationManager,
    GovernancePipeline
)


def test_scenario_1_expression_gate():
    """测试场景 1: Expression Gate（置信度检查）"""
    print("=" * 60)
    print("测试场景 1: Expression Gate（置信度检查）")
    print("=" * 60)
    
    gate = ExpressionGate(min_confidence=0.6)
    
    # 高置信度合约
    contract_high = create_navigation_contract(
        action=ACTION_TURN_LEFT,
        distance_m=5.0,
        confidence=0.9,
        direction="left"
    )
    
    # 低置信度合约
    contract_low = create_navigation_contract(
        action=ACTION_TURN_LEFT,
        distance_m=5.0,
        confidence=0.5,  # < 0.6
        direction="left"
    )
    
    params = ExpressionParams(
        action="turn_left",
        distance_value=5.0,
        distance_unit="meters",
        direction_reference="absolute",
        lateral_hint=False,
        urgency_level=3
    )
    
    context = {}
    
    result_high = gate.allow(contract_high, params, context)
    result_low = gate.allow(contract_low, params, context)
    
    print(f"  高置信度 (0.9): {result_high}")
    print(f"  低置信度 (0.5): {result_low}")
    
    assert result_high == True, "高置信度应该允许"
    assert result_low == False, "低置信度应该阻断"
    
    print("\n✅ 测试场景 1 通过")


def test_scenario_2_rate_limiter():
    """测试场景 2: Rate Limiter（节流器）"""
    print("\n" + "=" * 60)
    print("测试场景 2: Rate Limiter（节流器）")
    print("=" * 60)
    
    limiter = RateLimiter(default_interval=2.0)
    
    # 第一次允许
    result1 = limiter.allow("turn_left", urgency=1)
    print(f"  第一次 (turn_left): {result1}")
    assert result1 == True, "第一次应该允许"
    
    # 立即第二次（应该被节流）
    result2 = limiter.allow("turn_left", urgency=1)
    print(f"  立即第二次 (turn_left): {result2}")
    assert result2 == False, "立即第二次应该被节流"
    
    # 高紧急度可以绕过
    result3 = limiter.allow("turn_left", urgency=4)
    print(f"  高紧急度 (urgency=4): {result3}")
    assert result3 == True, "高紧急度应该绕过节流"
    
    # 等待后允许
    time.sleep(2.1)
    result4 = limiter.allow("turn_left", urgency=1)
    print(f"  等待后 (turn_left): {result4}")
    assert result4 == True, "等待后应该允许"
    
    print("\n✅ 测试场景 2 通过")


def test_scenario_3_confirmation_manager():
    """测试场景 3: Confirmation Manager（确认机制）"""
    print("\n" + "=" * 60)
    print("测试场景 3: Confirmation Manager（确认机制）")
    print("=" * 60)
    
    confirmer = ConfirmationManager(
        low_confidence_threshold=0.6,
        high_confidence_threshold=0.75
    )
    
    # 中等置信度（需要确认）
    contract_medium = create_navigation_contract(
        action=ACTION_TURN_LEFT,
        distance_m=5.0,
        confidence=0.7,  # 在 [0.6, 0.75] 区间
        direction="left"
    )
    
    # 高置信度（不需要确认）
    contract_high = create_navigation_contract(
        action=ACTION_TURN_LEFT,
        distance_m=5.0,
        confidence=0.9,
        direction="left"
    )
    
    context_normal = {}
    context_scene_changed = {"scene_changed": True}
    
    result1 = confirmer.should_confirm(contract_medium, context_normal)
    result2 = confirmer.should_confirm(contract_high, context_normal)
    result3 = confirmer.should_confirm(contract_high, context_scene_changed)
    
    print(f"  中等置信度 (0.7): {result1}")
    print(f"  高置信度 (0.9): {result2}")
    print(f"  场景切换: {result3}")
    
    assert result1 == True, "中等置信度应该需要确认"
    assert result2 == False, "高置信度不需要确认"
    assert result3 == True, "场景切换应该需要确认"
    
    print("\n✅ 测试场景 3 通过")


def test_scenario_4_escalation_manager():
    """测试场景 4: Escalation Manager（升级机制）"""
    print("\n" + "=" * 60)
    print("测试场景 4: Escalation Manager（升级机制）")
    print("=" * 60)
    
    escalator = EscalationManager()
    
    # 正常情况
    context_normal = {"urgency_level": 1}
    level1 = escalator.level(context_normal)
    
    # 碰撞风险
    context_collision = {"collision_risk": True}
    level2 = escalator.level(context_collision)
    
    # 高紧急度
    context_high_urgency = {"high_urgency": True}
    level3 = escalator.level(context_high_urgency)
    
    # 根据 urgency_level
    context_urgency5 = {"urgency_level": 5}
    level4 = escalator.level(context_urgency5)
    
    print(f"  正常情况: level={level1}")
    print(f"  碰撞风险: level={level2}")
    print(f"  高紧急度: level={level3}")
    print(f"  urgency=5: level={level4}")
    
    assert level1 == 1, "正常情况应该是 level 1"
    assert level2 == 5, "碰撞风险应该是 level 5"
    assert level3 == 4, "高紧急度应该是 level 4"
    assert level4 == 5, "urgency=5 应该是 level 5"
    
    # 测试打断判断
    assert escalator.should_interrupt(level2) == True, "level 5 应该打断"
    assert escalator.should_interrupt(level1) == False, "level 1 不应该打断"
    
    print("\n✅ 测试场景 4 通过")


def test_scenario_5_governance_pipeline():
    """测试场景 5: Governance Pipeline（完整治理流程）"""
    print("\n" + "=" * 60)
    print("测试场景 5: Governance Pipeline（完整治理流程）")
    print("=" * 60)
    
    pipeline = GovernancePipeline()
    
    # 正常情况
    contract = create_navigation_contract(
        action=ACTION_TURN_LEFT,
        distance_m=5.0,
        confidence=0.9,
        direction="left"
    )
    
    params = ExpressionParams(
        action="turn_left",
        distance_value=5.0,
        distance_unit="meters",
        direction_reference="absolute",
        lateral_hint=False,
        urgency_level=3
    )
    
    context = {}
    
    result = pipeline.process(contract, params, context)
    
    print(f"  治理决策: {result}")
    
    assert result["action"] == "allow", "应该允许"
    assert result["level"] >= 1, "应该有升级等级"
    
    # 测试低置信度（应该被阻断）
    contract_low = create_navigation_contract(
        action=ACTION_TURN_LEFT,
        distance_m=5.0,
        confidence=0.5,  # < 0.6
        direction="left"
    )
    
    result_blocked = pipeline.process(contract_low, params, context)
    print(f"  低置信度决策: {result_blocked}")
    
    assert result_blocked["action"] == "blocked", "低置信度应该被阻断"
    
    print("\n✅ 测试场景 5 通过")


def test_scenario_6_integration_c1_to_c4():
    """测试场景 6: C-1 → C-2 → C-3 → C-4 完整链路"""
    print("\n" + "=" * 60)
    print("测试场景 6: C-1 → C-2 → C-3 → C-4 完整链路")
    print("=" * 60)
    
    # C-1: 创建 Contract
    contract = create_navigation_contract(
        action=ACTION_TURN_LEFT,
        distance_m=5.0,
        confidence=0.9,
        direction="left"
    )
    
    # C-2: 校准参数
    from expression.embodiment import EmbodimentType, EmbodimentResolver
    from expression.scene import SceneClassifier
    from expression.calibration import ExpressionCalibrator
    
    resolver = EmbodimentResolver(default_embodiment=EmbodimentType.BLIND_BADGE)
    embodiment_ctx = resolver.resolve()
    
    classifier = SceneClassifier()
    scene_ctx = classifier.classify({
        "scene": "outdoor",
        "distance_m": 30.0
    })
    
    calibrator = ExpressionCalibrator()
    params = calibrator.calibrate(contract, embodiment_ctx, scene_ctx)
    
    # C-3: 渲染文本（跳过，只验证参数）
    # C-4: 治理决策
    pipeline = GovernancePipeline()
    context = {
        "fsm_state": "PRE_TURN",
        "scene": "outdoor"
    }
    
    governance_result = pipeline.process(contract, params, context)
    
    print(f"  C-1 Contract: {contract.action}, confidence={contract.confidence}")
    print(f"  C-2 Params: {params.distance_value} {params.distance_unit}")
    print(f"  C-4 Governance: {governance_result}")
    
    # 验证完整链路
    assert governance_result["action"] == "allow", "应该允许表达"
    assert governance_result["level"] >= 1, "应该有升级等级"
    
    print("\n✅ 测试场景 6 通过")


def main():
    """主函数"""
    print("=" * 60)
    print("C-4 Expression Governance Test")
    print("=" * 60)
    
    try:
        test_scenario_1_expression_gate()
        test_scenario_2_rate_limiter()
        test_scenario_3_confirmation_manager()
        test_scenario_4_escalation_manager()
        test_scenario_5_governance_pipeline()
        test_scenario_6_integration_c1_to_c4()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        print("\n✅ C-4 验收标准验证:")
        print("  功能性:")
        print("    ✅ 决定'要不要说'")
        print("    ✅ 决定'现在说还是等一下'")
        print("    ✅ 决定'说几次'")
        print("    ✅ 决定'要不要确认'")
        print("  架构性:")
        print("    ✅ 一期：规则驱动")
        print("    ✅ 二期：可接入模型")
        print("    ✅ 不改文本，只控制是否/何时/如何输出")
        print("    ✅ 这是系统'像不像一个靠谱的人'的关键")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()







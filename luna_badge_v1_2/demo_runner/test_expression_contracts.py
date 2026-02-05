"""
Expression Contracts Test (C-1)

测试合约创建和验证
"""

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from expression.contracts import (
    BaseExpressionContract,
    NavigationExpressionContract,
    create_navigation_contract,
    ACTION_GO_STRAIGHT,
    ACTION_TURN_LEFT,
    ACTION_STOP,
)
from expression.validators import ContractValidator, ValidationResult


def test_scenario_1_valid_turn_left_contract():
    """测试场景 1: ✅ 合法 turn_left contract → valid"""
    print("=" * 60)
    print("测试场景 1: ✅ 合法 turn_left contract → valid")
    print("=" * 60)
    
    validator = ContractValidator()
    
    contract = create_navigation_contract(
        action=ACTION_TURN_LEFT,
        distance_m=5.0,
        confidence=0.9,
        direction="left"
    )
    
    result = validator.validate(contract)
    
    print(f"  验证结果: valid={result.is_valid}")
    print(f"  错误: {result.errors}")
    print(f"  警告: {result.warnings}")
    
    assert result.is_valid, "合法 turn_left contract 应该通过验证"
    assert len(result.errors) == 0, "不应该有错误"
    
    print("\n✅ 测试场景 1 通过")


def test_scenario_2_turn_left_no_direction():
    """测试场景 2: ❌ turn_left 但无 direction → invalid"""
    print("\n" + "=" * 60)
    print("测试场景 2: ❌ turn_left 但无 direction → invalid")
    print("=" * 60)
    
    validator = ContractValidator()
    
    contract = create_navigation_contract(
        action=ACTION_TURN_LEFT,
        distance_m=5.0,
        confidence=0.9,
        direction=None  # 缺少 direction
    )
    
    result = validator.validate(contract)
    
    print(f"  验证结果: valid={result.is_valid}")
    print(f"  错误: {result.errors}")
    
    assert not result.is_valid, "turn_left 但无 direction 应该验证失败"
    assert any("direction" in err.lower() for err in result.errors), "应该包含 direction 相关错误"
    
    print("\n✅ 测试场景 2 通过")


def test_scenario_3_negative_distance():
    """测试场景 3: ❌ negative distance → invalid"""
    print("\n" + "=" * 60)
    print("测试场景 3: ❌ negative distance → invalid")
    print("=" * 60)
    
    validator = ContractValidator()
    
    contract = create_navigation_contract(
        action=ACTION_GO_STRAIGHT,
        distance_m=-5.0,  # 负数距离
        confidence=0.9
    )
    
    result = validator.validate(contract)
    
    print(f"  验证结果: valid={result.is_valid}")
    print(f"  错误: {result.errors}")
    
    assert not result.is_valid, "negative distance 应该验证失败"
    assert any("distance" in err.lower() for err in result.errors), "应该包含 distance 相关错误"
    
    print("\n✅ 测试场景 3 通过")


def test_scenario_4_confidence_out_of_range():
    """测试场景 4: ❌ confidence > 1 → invalid"""
    print("\n" + "=" * 60)
    print("测试场景 4: ❌ confidence > 1 → invalid")
    print("=" * 60)
    
    validator = ContractValidator()
    
    contract = create_navigation_contract(
        action=ACTION_GO_STRAIGHT,
        distance_m=10.0,
        confidence=1.5  # 超出范围
    )
    
    result = validator.validate(contract)
    
    print(f"  验证结果: valid={result.is_valid}")
    print(f"  错误: {result.errors}")
    
    assert not result.is_valid, "confidence > 1 应该验证失败"
    assert any("confidence" in err.lower() for err in result.errors), "应该包含 confidence 相关错误"
    
    print("\n✅ 测试场景 4 通过")


def test_scenario_5_stop_with_distance_zero():
    """测试场景 5: ✅ stop + distance 0 → valid"""
    print("\n" + "=" * 60)
    print("测试场景 5: ✅ stop + distance 0 → valid")
    print("=" * 60)
    
    validator = ContractValidator()
    
    contract = create_navigation_contract(
        action=ACTION_STOP,
        distance_m=0.0,  # distance 0 对于 stop 是合法的
        confidence=0.9
    )
    
    result = validator.validate(contract)
    
    print(f"  验证结果: valid={result.is_valid}")
    print(f"  错误: {result.errors}")
    print(f"  警告: {result.warnings}")
    
    assert result.is_valid, "stop + distance 0 应该通过验证"
    # 可能有警告，但不应该有错误
    assert len(result.errors) == 0, "不应该有错误"
    
    print("\n✅ 测试场景 5 通过")


def test_scenario_6_base_contract_creation():
    """测试场景 6: BaseExpressionContract 创建"""
    print("\n" + "=" * 60)
    print("测试场景 6: BaseExpressionContract 创建")
    print("=" * 60)
    
    import time
    
    contract = BaseExpressionContract(
        intent_type="navigation",
        source="fsm",
        confidence=0.9,
        timestamp=time.time()
    )
    
    assert contract.intent_type == "navigation"
    assert contract.source == "fsm"
    assert contract.confidence == 0.9
    
    contract_dict = contract.to_dict()
    assert "intent_type" in contract_dict
    assert "source" in contract_dict
    assert "confidence" in contract_dict
    assert "timestamp" in contract_dict
    
    print(f"  合约: {contract_dict}")
    print("\n✅ 测试场景 6 通过")


def main():
    """主函数"""
    print("=" * 60)
    print("Expression Contracts Test (C-1)")
    print("=" * 60)
    
    try:
        test_scenario_1_valid_turn_left_contract()
        test_scenario_2_turn_left_no_direction()
        test_scenario_3_negative_distance()
        test_scenario_4_confidence_out_of_range()
        test_scenario_5_stop_with_distance_zero()
        test_scenario_6_base_contract_creation()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()







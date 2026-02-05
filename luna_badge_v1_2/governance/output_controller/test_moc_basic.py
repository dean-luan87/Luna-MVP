#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOC 基础功能测试

验证 Model Output Controller 的核心功能：
1. 输出标准化
2. 输出验证
3. 冲突检测
4. 仲裁决策
5. 完整流程
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from governance.output_controller.controller import ModelOutputController


def test_single_output():
    """测试单个模型输出"""
    print("\n=== 测试 1: 单个模型输出 ===")
    moc = ModelOutputController()
    
    outputs = [
        {
            "model_id": "vision_model_v1",
            "model_version": "1.0",
            "result": {"action": "turn_left", "distance": 5},
            "confidence": 0.9
        }
    ]
    
    result = moc.process("navigation", outputs)
    assert result["decision"] == "commit", "应该选择 commit"
    assert result["used_model"]["model_id"] == "vision_model_v1", "应该使用 vision_model_v1"
    print(f"✓ 决策: {result['decision']}")
    print(f"✓ 原因: {result['reason']}")
    print(f"✓ 使用的模型: {result['used_model']['model_id']}")


def test_conflict_detection():
    """测试冲突检测"""
    print("\n=== 测试 2: 冲突检测 ===")
    moc = ModelOutputController()
    
    outputs = [
        {
            "model_id": "model_a",
            "result": {"action": "turn_left", "distance": 5},
            "confidence": 0.9
        },
        {
            "model_id": "model_b",
            "result": {"action": "turn_right", "distance": 5},  # 冲突：方向不同
            "confidence": 0.8
        }
    ]
    
    result = moc.process("navigation", outputs)
    conflicts = result["decision_trace"]["conflicts_detected"]
    print(f"✓ 检测到冲突数: {len(conflicts)}")
    if conflicts:
        print(f"✓ 冲突类型: {conflicts[0]['type']}")
        print(f"✓ 涉及模型: {conflicts[0]['models']}")


def test_primary_model_priority():
    """测试主模型优先级"""
    print("\n=== 测试 3: 主模型优先级 ===")
    moc = ModelOutputController()
    
    outputs = [
        {
            "model_id": "backup_vision_model",  # 次模型
            "result": {"action": "turn_left", "distance": 5},
            "confidence": 0.9
        },
        {
            "model_id": "vision_model_v1",  # 主模型
            "result": {"action": "turn_left", "distance": 5},
            "confidence": 0.8
        }
    ]
    
    result = moc.process("navigation", outputs)
    assert result["decision"] == "commit", "应该选择 commit"
    assert result["used_model"]["model_id"] == "vision_model_v1", "应该优先选择主模型"
    print(f"✓ 决策: {result['decision']}")
    print(f"✓ 使用的模型: {result['used_model']['model_id']} (主模型优先)")


def test_fallback_on_conflict():
    """测试冲突时触发 fallback"""
    print("\n=== 测试 4: 冲突触发 fallback ===")
    moc = ModelOutputController()
    
    outputs = [
        {
            "model_id": "unknown_model_a",  # 非主/次模型
            "result": {"action": "turn_left", "distance": 5},
            "confidence": 0.9
        },
        {
            "model_id": "unknown_model_b",  # 非主/次模型，且冲突
            "result": {"action": "turn_right", "distance": 5},
            "confidence": 0.8
        }
    ]
    
    result = moc.process("navigation", outputs)
    print(f"✓ 决策: {result['decision']}")
    print(f"✓ 原因: {result['reason']}")
    if result["decision"] == "fallback":
        print("✓ 正确触发 fallback")


def test_invalid_output_filtering():
    """测试无效输出过滤"""
    print("\n=== 测试 5: 无效输出过滤 ===")
    moc = ModelOutputController()
    
    outputs = [
        {
            "model_id": "valid_model",
            "result": {"action": "turn_left", "distance": 5},
            "confidence": 0.9
        },
        {
            "model_id": "invalid_model",
            # 缺少 result/data/output 字段
            "confidence": 0.8
        },
        {
            "model_id": "null_model",
            "result": None,  # data 为 None
            "confidence": 0.7
        }
    ]
    
    result = moc.process("navigation", outputs)
    valid_count = result["decision_trace"]["valid_outputs_count"]
    total_count = result["decision_trace"]["total_outputs_count"]
    print(f"✓ 总输出数: {total_count}")
    print(f"✓ 有效输出数: {valid_count}")
    assert valid_count == 1, "应该只保留1个有效输出"
    assert result["decision"] == "commit", "应该选择 commit"


def main():
    """运行所有测试"""
    print("=" * 60)
    print("MOC 基础功能测试")
    print("=" * 60)
    
    try:
        test_single_output()
        test_conflict_detection()
        test_primary_model_priority()
        test_fallback_on_conflict()
        test_invalid_output_filtering()
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())






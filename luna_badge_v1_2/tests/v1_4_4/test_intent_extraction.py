#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试意图提取功能

测试 Command Layer 的意图提取能力：
- 命令前缀检测
- 语义归一化
- 地点提取
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from command_layer.prefix_detector import detect_prefix
from command_layer.semantic_normalizer import normalize_command
from command_layer.ecs_resolver import resolve_slots, FakeMemoryClient, FakePOIClient


def test_prefix_detection():
    """测试命令前缀检测"""
    print("=" * 60)
    print("测试 1: 命令前缀检测")
    print("=" * 60)
    
    test_cases = [
        ("Luna，请带我去医院", True, "请带我去医院"),
        ("Luna, 去711", True, "去711"),
        ("Luna 请帮我导航", True, "帮我导航"),
        ("我想出去走走", False, None),
        ("Luna", True, None),  # 空命令
    ]
    
    passed = 0
    for text, expected_is_command, expected_command_text in test_cases:
        envelope = detect_prefix(text)
        is_pass = (
            envelope.is_command == expected_is_command and
            envelope.command_text == expected_command_text
        )
        status = "✅" if is_pass else "❌"
        print(f"{status} 输入: {text}")
        print(f"   是否命令: {envelope.is_command} (期望: {expected_is_command})")
        print(f"   命令文本: {envelope.command_text} (期望: {expected_command_text})")
        if is_pass:
            passed += 1
        print()
    
    print(f"通过: {passed}/{len(test_cases)}")
    return passed == len(test_cases)


def test_semantic_normalization():
    """测试语义归一化"""
    print("=" * 60)
    print("测试 2: 语义归一化")
    print("=" * 60)
    
    test_cases = [
        ("带我去医院", "NAVIGATE", "hospital"),
        ("取消导航", "CANCEL_TASK", None),
        ("顺便去711", "INSERT_TASK", "convenience_store"),
        ("改去医院", "REPLACE_TASK", "hospital"),
        ("无法识别的命令", "UNKNOWN", None),
    ]
    
    passed = 0
    for text, expected_intent, expected_category in test_cases:
        normalized = normalize_command(text)
        is_pass = normalized.intent_type == expected_intent
        if expected_category:
            is_pass = is_pass and normalized.slots.get("place_category") == expected_category
        
        status = "✅" if is_pass else "❌"
        print(f"{status} 输入: {text}")
        print(f"   意图类型: {normalized.intent_type} (期望: {expected_intent})")
        print(f"   槽位: {normalized.slots}")
        if is_pass:
            passed += 1
        print()
    
    print(f"通过: {passed}/{len(test_cases)}")
    return passed == len(test_cases)


def test_ecs_resolution():
    """测试参数补全"""
    print("=" * 60)
    print("测试 3: 参数补全 (ECSv1)")
    print("=" * 60)
    
    from command_layer.semantic_normalizer import NormalizedCommand
    
    memory_client = FakeMemoryClient()
    poi_client = FakePOIClient()
    
    # 测试需要补全的命令
    normalized = NormalizedCommand(
        intent_type="NAVIGATE",
        slots={"place_category": "hospital", "place_name": None},
        need_confirm=True
    )
    
    resolution = resolve_slots(normalized, memory_client, poi_client)
    
    print(f"✅ 归一化命令: {normalized.intent_type}, slots={normalized.slots}")
    print(f"✅ 补全结果: resolved={resolution.resolved}, source={resolution.source}")
    print(f"✅ 补全后槽位: {resolution.slots}")
    
    is_pass = resolution.resolved and resolution.source == "memory"
    status = "✅" if is_pass else "❌"
    print(f"{status} 参数补全测试")
    print()
    
    return is_pass


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("Luna Badge v1.4.4 - 意图提取测试")
    print("=" * 60 + "\n")
    
    results = []
    
    results.append(("命令前缀检测", test_prefix_detection()))
    results.append(("语义归一化", test_semantic_normalization()))
    results.append(("参数补全", test_ecs_resolution()))
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print("\n⚠️  部分测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())













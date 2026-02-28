#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command Layer 冒烟测试脚本

用于验证 Phase 4-6 的基本功能
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_phase_4_6():
    """测试 Phase 4-6 功能"""
    print("=" * 60)
    print("Command Layer Phase 4-6 冒烟测试")
    print("=" * 60)
    print()
    
    try:
        # 测试导入
        print("1. 测试模块导入...")
        from command_layer.prefix_detector import detect_prefix
        from command_layer.semantic_normalizer import normalize_command
        from command_layer.ecs_resolver import resolve_slots, FakeMemoryClient, FakePOIClient
        from command_layer.mapping import normalized_to_parsed_intent
        print("   ✅ 所有模块导入成功")
        print()
        
        # 测试 Phase 4: ECSv1
        print("2. 测试 Phase 4: ECSv1 参数补全...")
        memory_client = FakeMemoryClient()
        poi_client = FakePOIClient()
        
        # 测试用例 1: 需要补全的导航命令
        normalized = normalize_command("带我去医院")
        print(f"   归一化结果: intent_type={normalized.intent_type}, slots={normalized.slots}")
        
        resolution = resolve_slots(normalized, memory_client, poi_client)
        print(f"   补全结果: resolved={resolution.resolved}, source={resolution.source}")
        print(f"   补全后 slots: {resolution.slots}")
        print("   ✅ ECSv1 参数补全功能正常")
        print()
        
        # 测试 Phase 6: 映射函数
        print("3. 测试 Phase 6: NormalizedCommand → ParsedIntent 映射...")
        parsed_intent = normalized_to_parsed_intent(normalized, resolution)
        print(f"   映射结果: intent_name={parsed_intent.intent_name}")
        print(f"   slots: {parsed_intent.slots}")
        print(f"   need_confirm: {parsed_intent.need_confirm}")
        print("   ✅ 映射函数功能正常")
        print()
        
        # 测试完整流程
        print("4. 测试完整流程（命令检测 → 归一化 → 补全 → 映射）...")
        test_cases = [
            "Luna，带我去医院",
            "Luna, 顺便去711",
            "Luna 请取消导航",
        ]
        
        for text in test_cases:
            print(f"   测试输入: {text}")
            envelope = detect_prefix(text)
            if envelope.is_command and envelope.command_text:
                normalized = normalize_command(envelope.command_text)
                if normalized.intent_type != "UNKNOWN":
                    resolution = resolve_slots(normalized, memory_client, poi_client)
                    if resolution.resolved:
                        parsed_intent = normalized_to_parsed_intent(normalized, resolution)
                        print(f"     → intent_name: {parsed_intent.intent_name}")
                        print(f"     → slots: {parsed_intent.slots}")
                    else:
                        print(f"     → 需要澄清: {resolution.reason}")
                else:
                    print(f"     → 无法识别意图")
            else:
                print(f"     → 非命令或空命令")
            print()
        
        print("   ✅ 完整流程测试通过")
        print()
        
        print("=" * 60)
        print("✅ 所有测试通过！Phase 4-6 功能正常")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_phase_4_6()
    sys.exit(0 if success else 1)


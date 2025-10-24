#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge - 快速架构验证脚本
简化版本，专注于架构完整性验证
"""

import sys
import os
import json

def print_header():
    """打印测试头部信息"""
    print("🌟 Luna Badge - 快速架构验证")
    print("=" * 50)

def test_imports():
    """测试模块导入"""
    print("\n🔍 测试模块导入...")
    
    try:
        # 核心模块
        from core import ConfigManager, SystemControl, AINavigation, config_manager
        print("✅ 核心模块导入成功")
        
        # 硬件模块
        from hal_mac.hardware_mac import MacHAL
        from hal_embedded.hardware_embedded import EmbeddedHAL
        print("✅ 硬件模块导入成功")
        
        return True
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_config():
    """测试配置管理"""
    print("\n🔍 测试配置管理...")
    
    try:
        from core import config_manager
        
        # 加载配置
        config = config_manager.load_config()
        print(f"✅ 配置加载成功: {config['platform']}")
        
        # 获取配置
        platform = config_manager.get_config("platform")
        print(f"✅ 配置获取成功: {platform}")
        
        return True
    except Exception as e:
        print(f"❌ 配置管理失败: {e}")
        return False

def test_instances():
    """测试实例创建"""
    print("\n🔍 测试实例创建...")
    
    try:
        from core import SystemControl, AINavigation, config_manager
        from hal_mac.hardware_mac import MacHAL
        
        # 创建实例
        system_control = SystemControl()
        ai_navigation = AINavigation()
        hal_interface = MacHAL()
        
        print("✅ 实例创建成功")
        
        # 测试基本方法
        status = system_control.get_status()
        print(f"✅ 系统状态获取: {status['current_state']}")
        
        ai_status = ai_navigation.get_status()
        print(f"✅ AI导航状态获取: {ai_status['is_running']}")
        
        return True
    except Exception as e:
        print(f"❌ 实例创建失败: {e}")
        return False

def test_workflow():
    """测试工作流程"""
    print("\n🔍 测试工作流程...")
    
    try:
        from core import SystemControl, config_manager
        from hal_mac.hardware_mac import MacHAL
        
        # 创建实例
        system_control = SystemControl()
        hal_interface = MacHAL()
        
        # 设置硬件接口
        system_control.set_hal_interface(hal_interface)
        
        # 测试状态变化
        system_control.enter_idle()
        print("✅ 进入空闲状态")
        
        system_control.wake_up()
        print("✅ 系统唤醒")
        
        return True
    except Exception as e:
        print(f"❌ 工作流程测试失败: {e}")
        return False

def main():
    """主函数"""
    print_header()
    
    tests = [
        ("模块导入", test_imports),
        ("配置管理", test_config),
        ("实例创建", test_instances),
        ("工作流程", test_workflow)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 Luna 架构运行循环通过！")
        print("✅ 所有模块导入成功")
        return 0
    else:
        print("❌ 部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())

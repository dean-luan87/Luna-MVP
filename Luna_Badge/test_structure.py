#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge - 项目结构测试脚本
"""

import sys
import os

def test_imports():
    """测试所有模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        # 测试核心模块
        from core import (
            ConfigManager, SystemControl, SystemState, ErrorCode, 
            AINavigation, NavigationModule, ModuleStatus, config_manager
        )
        print("✅ 核心模块导入成功")
        
        # 测试Mac硬件模块
        try:
            from hal_mac.hardware_mac import MacHAL
            print("✅ Mac硬件模块导入成功")
        except ImportError as e:
            print(f"⚠️ Mac硬件模块导入失败: {e}")
        
        # 测试嵌入式硬件模块
        try:
            from hal_embedded.hardware_embedded import EmbeddedHAL
            print("✅ 嵌入式硬件模块导入成功")
        except ImportError as e:
            print(f"⚠️ 嵌入式硬件模块导入失败: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_config():
    """测试配置管理"""
    print("\n🔍 测试配置管理...")
    
    try:
        from core import config_manager
        
        # 测试配置加载
        config = config_manager.load_config()
        print(f"✅ 配置加载成功: {config['platform']}")
        
        # 测试配置获取
        platform = config_manager.get_config("platform")
        print(f"✅ 配置获取成功: {platform}")
        
        # 测试配置设置
        success = config_manager.set_config("test.key", "test.value")
        print(f"✅ 配置设置成功: {success}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置管理测试失败: {e}")
        return False

def test_system_control():
    """测试系统控制"""
    print("\n🔍 测试系统控制...")
    
    try:
        from core import SystemControl, SystemState
        
        # 创建系统控制器
        system_control = SystemControl()
        print("✅ 系统控制器创建成功")
        
        # 测试状态获取
        status = system_control.get_status()
        print(f"✅ 系统状态获取成功: {status['current_state']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 系统控制测试失败: {e}")
        return False

def test_ai_navigation():
    """测试AI导航"""
    print("\n🔍 测试AI导航...")
    
    try:
        from core import AINavigation
        
        # 创建AI导航器
        ai_navigation = AINavigation()
        print("✅ AI导航器创建成功")
        
        # 测试状态获取
        status = ai_navigation.get_status()
        print(f"✅ AI导航状态获取成功: {status['is_running']}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI导航测试失败: {e}")
        return False

def test_hardware_interface():
    """测试硬件接口"""
    print("\n🔍 测试硬件接口...")
    
    try:
        from hal_mac.hardware_mac import MacHAL
        from hal_embedded.hardware_embedded import EmbeddedHAL
        
        # 测试Mac硬件接口
        mac_hal = MacHAL()
        print("✅ Mac硬件接口创建成功")
        
        # 测试嵌入式硬件接口
        embedded_hal = EmbeddedHAL()
        print("✅ 嵌入式硬件接口创建成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 硬件接口测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🌟 Luna Badge - 项目结构测试")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_system_control,
        test_ai_navigation,
        test_hardware_interface
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！项目结构正确")
        return 0
    else:
        print("❌ 部分测试失败，请检查项目结构")
        return 1

if __name__ == "__main__":
    sys.exit(main())

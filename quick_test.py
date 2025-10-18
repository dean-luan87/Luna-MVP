#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna-2 快速功能测试脚本
用于在新电脑上快速验证所有功能是否正常
"""

import sys
import subprocess
import time

def test_imports():
    """测试所有模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        import cv2
        print("✅ OpenCV 导入成功")
    except ImportError as e:
        print(f"❌ OpenCV 导入失败: {e}")
        return False
    
    try:
        import pyttsx3
        print("✅ pyttsx3 导入成功")
    except ImportError as e:
        print(f"❌ pyttsx3 导入失败: {e}")
        return False
    
    try:
        import edge_tts
        print("✅ edge-tts 导入成功")
    except ImportError as e:
        print(f"❌ edge-tts 导入失败: {e}")
        return False
    
    try:
        import openrouteservice
        print("✅ openrouteservice 导入成功")
    except ImportError as e:
        print(f"❌ openrouteservice 导入失败: {e}")
        return False
    
    return True

def test_voice_system():
    """测试语音系统"""
    print("\n🎤 测试语音系统...")
    
    try:
        # 测试系统 say 命令
        result = subprocess.run(["say", "语音系统测试"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ 系统语音播报正常")
        else:
            print("❌ 系统语音播报失败")
            return False
    except Exception as e:
        print(f"❌ 语音测试失败: {e}")
        return False
    
    return True

def test_camera():
    """测试摄像头"""
    print("\n🎥 测试摄像头...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✅ 摄像头读取正常")
                cap.release()
                return True
            else:
                print("❌ 摄像头读取失败")
                cap.release()
                return False
        else:
            print("❌ 摄像头无法打开")
            return False
    except Exception as e:
        print(f"❌ 摄像头测试失败: {e}")
        return False

def test_vision_modules():
    """测试视觉模块"""
    print("\n👁️ 测试视觉模块...")
    
    try:
        from voice import Speaker
        print("✅ 语音模块导入成功")
    except ImportError as e:
        print(f"❌ 语音模块导入失败: {e}")
        return False
    
    try:
        from navigation import VoiceNavigator
        print("✅ 导航模块导入成功")
    except ImportError as e:
        print(f"❌ 导航模块导入失败: {e}")
        return False
    
    return True

def test_api_config():
    """测试 API 配置"""
    print("\n🔑 测试 API 配置...")
    
    import os
    ors_key = os.getenv('ORS_API_KEY')
    if ors_key and ors_key != '你的_ORS_API_KEY':
        print("✅ OpenRouteService API 密钥已配置")
        return True
    else:
        print("⚠️ OpenRouteService API 密钥未配置")
        print("💡 请设置环境变量: export ORS_API_KEY='你的密钥'")
        return False

def run_quick_demo():
    """运行快速演示"""
    print("\n🚀 运行快速演示...")
    
    try:
        # 运行语音演示
        print("📢 播放欢迎语音...")
        subprocess.run(["say", "Luna-2 系统测试完成，所有功能正常"], timeout=10)
        print("✅ 语音演示完成")
        return True
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🎯 Luna-2 快速功能测试")
    print("=" * 40)
    
    tests = [
        ("模块导入", test_imports),
        ("语音系统", test_voice_system),
        ("摄像头", test_camera),
        ("视觉模块", test_vision_modules),
        ("API配置", test_api_config),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} 测试失败")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！Luna-2 系统就绪")
        run_quick_demo()
        return True
    else:
        print("⚠️ 部分测试失败，请检查环境配置")
        print("💡 运行 ./setup_environment.sh 重新配置环境")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

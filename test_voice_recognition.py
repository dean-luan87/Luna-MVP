#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音识别测试工具
测试语音识别模块的功能
"""

import time
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_voice_recognition():
    """测试语音识别功能"""
    print("🎤 测试语音识别功能")
    print("=" * 50)
    
    try:
        # 导入语音识别模块
        from utils.simple_voice_recognition import SimpleVoiceRecognition, listen_and_recognize
        
        print("✅ 语音识别模块导入成功")
        
        # 创建语音识别实例
        print("🔧 初始化语音识别模块...")
        vr = SimpleVoiceRecognition()
        
        if not vr.is_available:
            print("❌ 语音识别模块不可用")
            return False
        
        print("✅ 语音识别模块初始化成功")
        print(f"📊 模块状态: {vr.get_status()}")
        
        # 测试麦克风
        print("🎙️ 测试麦克风...")
        if vr.test_microphone():
            print("✅ 麦克风测试成功")
        else:
            print("❌ 麦克风测试失败")
            return False
        
        # 测试语音识别
        print("\n🔊 开始语音识别测试...")
        print("请说话（5秒内）...")
        
        recognized_text = vr.listen_and_recognize(timeout=5)
        
        if recognized_text and recognized_text.strip():
            print(f"✅ 识别成功: {recognized_text}")
        else:
            print("⚠️ 未识别到语音内容")
        
        # 测试便捷函数
        print("\n🔧 测试便捷函数...")
        print("请再次说话（5秒内）...")
        
        text = listen_and_recognize(timeout=5)
        
        if text and text.strip():
            print(f"✅ 便捷函数识别成功: {text}")
        else:
            print("⚠️ 便捷函数未识别到语音内容")
        
        print("\n🎉 语音识别测试完成")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请安装依赖: pip install SpeechRecognition pyaudio")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        logger.error(f"语音识别测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_voice_recognition()
    exit(0 if success else 1)

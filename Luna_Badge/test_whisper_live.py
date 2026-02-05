#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge Whisper 真实麦克风录音测试
测试实际录音和语音识别功能
"""

import logging
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_live_recognition():
    """测试真实麦克风录音识别"""
    print("=" * 60)
    print("🎤 Luna Badge Whisper 麦克风录音测试")
    print("=" * 60)
    print()
    
    try:
        from core.whisper_recognizer import get_whisper_recognizer
        
        # 初始化识别器
        print("正在初始化Whisper识别器...")
        recognizer = get_whisper_recognizer(model_name="base")
        
        if not recognizer.is_loaded:
            print("正在加载Whisper模型（首次可能需要下载）...")
            if not recognizer.load_model():
                print("❌ 模型加载失败")
                return
            print("✅ 模型加载成功")
        
        print()
        print("准备录音...")
        print("-" * 60)
        
        # 测试1: 中文语音识别
        print("\n测试 1: 中文语音识别（5秒）")
        print("请用中文说话，例如：创建新账号")
        print("3秒后开始录音...")
        import time
        for i in range(3, 0, -1):
            print(f"{i}...", end="", flush=True)
            time.sleep(1)
        print("\n🎤 开始录音...")
        
        text, details = recognizer.recognize_from_microphone(duration=5)
        
        print(f"\n✅ 识别结果: {text}")
        print(f"置信度: {details.get('confidence', 0):.2f}")
        print(f"语言: {details.get('language', 'unknown')}")
        
        # 测试2: 数字识别
        print("\n" + "-" * 60)
        print("\n测试 2: 数字语音识别（5秒）")
        print("请说出6位数字，例如：一二三四五六 或 1 2 3 4 5 6")
        print("3秒后开始录音...")
        for i in range(3, 0, -1):
            print(f"{i}...", end="", flush=True)
            time.sleep(1)
        print("\n🎤 开始录音...")
        
        text2, details2 = recognizer.recognize_from_microphone(duration=5)
        
        print(f"\n✅ 识别结果: {text2}")
        print(f"置信度: {details2.get('confidence', 0):.2f}")
        
        # 测试中文数字转换
        from core.voice_verification_code import VoiceVerificationCodeHandler
        handler = VoiceVerificationCodeHandler()
        code = handler._convert_chinese_numbers_to_digits(text2)
        print(f"转换结果: {code}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_live_recognition()


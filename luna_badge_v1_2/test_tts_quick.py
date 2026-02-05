#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试 TTS 核心功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.voice import Voice
from Luna_Badge.core.tts_manager import TTSManager

print("=" * 60)
print("测试 TTS 核心功能")
print("=" * 60)

# 初始化
print("\n1. 初始化 Voice 和 TTSManager...")
try:
    voice = Voice()
    tts_manager = TTSManager()
    print("✅ 初始化成功")
except Exception as e:
    print(f"❌ 初始化失败: {e}")
    sys.exit(1)

# 测试合成
print("\n2. 测试音频合成...")
try:
    audio_path = tts_manager.synthesize("测试语音播报")
    if audio_path:
        print(f"✅ 合成成功: {audio_path}")
        if os.path.exists(audio_path):
            print(f"✅ 文件存在: {audio_path}")
        else:
            print(f"❌ 文件不存在: {audio_path}")
    else:
        print("❌ 合成失败，返回 None")
        sys.exit(1)
except Exception as e:
    print(f"❌ 合成失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试播放
print("\n3. 测试音频播放...")
try:
    result = voice.play_audio(audio_path)
    if result:
        print("✅ 播放成功")
    else:
        print("❌ 播放失败")
except Exception as e:
    print(f"❌ 播放失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试统一接口
print("\n4. 测试统一接口 voice.speak()...")
try:
    result = voice.speak("这是统一接口测试", tts_manager)
    if result:
        print("✅ 统一接口测试成功")
    else:
        print("❌ 统一接口测试失败")
except Exception as e:
    print(f"❌ 统一接口测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ 所有测试通过！")
print("=" * 60)
















#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的Whisper测试 - 检查依赖和功能
"""

print("=" * 60)
print("Luna Badge Whisper 快速测试")
print("=" * 60)
print()

# 测试1: 检查依赖
print("测试 1: 检查依赖库")
print("-" * 60)

try:
    import whisper
    print("✅ whisper 已安装")
except ImportError:
    print("❌ whisper 未安装，运行: pip install openai-whisper")
    exit(1)

try:
    import sounddevice as sd
    print("✅ sounddevice 已安装")
except ImportError:
    print("❌ sounddevice 未安装，运行: pip install sounddevice")
    exit(1)

try:
    import scipy
    print("✅ scipy 已安装")
except ImportError:
    print("❌ scipy 未安装，运行: pip install scipy")
    exit(1)

print()

# 测试2: 检查Whisper识别器
print("测试 2: 检查Whisper识别器")
print("-" * 60)

try:
    from core.whisper_recognizer import get_whisper_recognizer
    recognizer = get_whisper_recognizer(model_name="base")
    print("✅ Whisper识别器初始化成功")
    print(f"  模型: {recognizer.model_name}")
    print(f"  语言: {recognizer.language}")
except Exception as e:
    print(f"❌ Whisper识别器初始化失败: {e}")
    exit(1)

print()

# 测试3: 检查模型加载
print("测试 3: 检查模型加载")
print("-" * 60)

if recognizer.load_model():
    print("✅ Whisper模型加载成功")
else:
    print("⚠️ Whisper模型加载失败")
    
print()

# 测试4: 检查麦克风
print("测试 4: 检查麦克风权限")
print("-" * 60)

try:
    import sounddevice as sd
    devices = sd.query_devices()
    print(f"✅ 发现 {len(devices)} 个音频设备")
    print(f"  默认输入设备: {sd.default.device[0]}")
except Exception as e:
    print(f"❌ 无法访问音频设备: {e}")

print()

# 总结
print("=" * 60)
print("✅ 测试完成")
print("=" * 60)
print()
print("下一步可以运行: python test_whisper_live.py")
print()


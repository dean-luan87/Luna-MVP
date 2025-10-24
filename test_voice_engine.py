#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音引擎测试工具
自动检测系统可用语音并测试中文语音播报
"""

import platform
import time
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_pyttsx3_voices():
    """测试pyttsx3可用语音"""
    try:
        import pyttsx3
        print("=" * 60)
        print("🔍 检测pyttsx3可用语音引擎...")
        print("=" * 60)
        
        # 在Mac上强制使用nsss驱动
        if platform.system() == 'Darwin':
            print("🍎 Mac系统检测到，使用nsss驱动...")
            try:
                engine = pyttsx3.init(driverName="nsss")
                print("✅ nsss驱动初始化成功")
            except Exception as e:
                print(f"⚠️ nsss驱动初始化失败: {e}")
                print("🔄 尝试使用默认驱动...")
                engine = pyttsx3.init()
        else:
            engine = pyttsx3.init()
        
        if not engine:
            print("❌ 无法初始化pyttsx3引擎")
            return None
        
        # 获取所有可用语音
        voices = engine.getProperty('voices')
        if not voices:
            print("❌ 未找到可用语音")
            return None
        
        print(f"\n📋 发现 {len(voices)} 个可用语音:")
        print("-" * 60)
        
        chinese_voices = []
        for i, voice in enumerate(voices):
            voice_id = voice.id
            voice_name = voice.name
            voice_languages = getattr(voice, 'languages', [])
            
            print(f"语音 {i+1}:")
            print(f"  ID: {voice_id}")
            print(f"  名称: {voice_name}")
            print(f"  语言: {voice_languages}")
            
            # 检查是否为中文语音
            is_chinese = False
            if voice_languages:
                for lang in voice_languages:
                    if any(keyword in str(lang).lower() for keyword in ['zh', 'chinese', 'cn', 'mandarin']):
                        is_chinese = True
                        break
            
            # 检查名称中是否包含中文关键词
            if not is_chinese:
                name_lower = voice_name.lower()
                if any(keyword in name_lower for keyword in ['chinese', 'zh', 'cn', 'mandarin', 'ting-ting', 'xiaoyi']):
                    is_chinese = True
            
            if is_chinese:
                chinese_voices.append((i+1, voice_id, voice_name, voice_languages))
                print(f"  🌏 中文语音: 是")
            else:
                print(f"  🌏 中文语音: 否")
            print()
        
        # 显示中文语音汇总
        if chinese_voices:
            print("🎯 发现的中文语音:")
            print("-" * 40)
            for idx, voice_id, voice_name, voice_languages in chinese_voices:
                print(f"  {idx}. {voice_name} (ID: {voice_id})")
        else:
            print("⚠️ 未发现中文语音，将使用默认语音")
        
        return engine, chinese_voices
        
    except ImportError:
        print("❌ pyttsx3未安装，请运行: pip install pyttsx3")
        return None
    except Exception as e:
        print(f"❌ pyttsx3测试失败: {e}")
        return None

def test_voice_speaking(engine, chinese_voices):
    """测试语音播报"""
    if not engine:
        print("❌ 引擎不可用，跳过语音测试")
        return False
    
    try:
        print("\n" + "=" * 60)
        print("🔊 开始语音播报测试...")
        print("=" * 60)
        
        # 设置语音参数
        engine.setProperty('rate', 150)  # 语速
        engine.setProperty('volume', 0.8)  # 音量
        
        # 选择最佳语音
        selected_voice = None
        if chinese_voices:
            # 优先选择第一个中文语音
            selected_voice = chinese_voices[0][1]  # 使用voice_id
            print(f"🎯 选择中文语音: {chinese_voices[0][2]} (ID: {selected_voice})")
        else:
            # 使用默认语音
            voices = engine.getProperty('voices')
            if voices:
                selected_voice = voices[0].id
                print(f"🎯 使用默认语音: {voices[0].name} (ID: {selected_voice})")
        
        if selected_voice:
            engine.setProperty('voice', selected_voice)
        
        # 测试语音播报
        test_text = "Luna 测试语音，语音模块运行正常"
        print(f"📢 播报内容: {test_text}")
        print("⏳ 正在播报...")
        
        # 开始播报
        engine.say(test_text)
        engine.runAndWait()
        
        print("✅ 语音播报完成")
        print(f"✅ 语音模块已完成测试，当前语音ID为：{selected_voice}")
        
        return True
        
    except Exception as e:
        print(f"❌ 语音播报测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🎤 Luna 语音引擎测试工具")
    print("=" * 60)
    print(f"🖥️ 操作系统: {platform.system()}")
    print(f"🐍 Python版本: {platform.python_version()}")
    print()
    
    # 测试pyttsx3
    result = test_pyttsx3_voices()
    if result:
        engine, chinese_voices = result
        test_voice_speaking(engine, chinese_voices)
    else:
        print("❌ 语音引擎测试失败")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 语音引擎测试完成")
    print("=" * 60)
    return True

if __name__ == "__main__":
    main()


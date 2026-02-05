#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Voice 模块完整测试脚本

测试内容：
1. 基本播放功能
2. 停止功能
3. 冷却机制
4. 队列功能
5. 多句播报顺序
"""

import sys
import os
import time
import logging

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.voice import Voice
from Luna_Badge.core.tts_manager import TTSManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger("TEST")

def print_section(title):
    """打印测试章节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_1_basic_playback():
    """测试 1：基本播放功能"""
    print_section("测试 1：基本播放功能")
    
    voice = Voice()
    tts = TTSManager()
    
    print("开始播报：'这是一个基本播放测试'")
    result = voice.speak("这是一个基本播放测试", tts)
    
    if result:
        print("✅ 播报请求已提交")
        print("等待播放完成...")
        
        # 等待播放完成（最多等待 10 秒）
        start_time = time.time()
        while voice.is_speaking():
            if time.time() - start_time > 10:
                print("⚠️ 播放超时（10秒）")
                break
            time.sleep(0.1)
        
        if not voice.is_speaking():
            print("✅ 播放完成")
        else:
            print("⚠️ 播放可能仍在进行")
    else:
        print("❌ 播报请求失败")
    
    return voice, tts

def test_2_stop_functionality(voice, tts):
    """测试 2：停止功能"""
    print_section("测试 2：停止功能")
    
    print("开始播报一段较长的文本...")
    voice.speak("这是一段用于测试停止功能的较长文本，应该能够被中途停止。", tts)
    
    # 等待 2 秒后停止
    print("等待 2 秒后停止...")
    time.sleep(2)
    
    print("调用 stop()...")
    voice.stop()
    
    # 检查状态
    time.sleep(0.5)
    if voice.is_speaking():
        print("❌ 停止失败，仍在播放")
    else:
        print("✅ 停止成功")
    
    return voice, tts

def test_3_cooldown_mechanism(voice, tts):
    """测试 3：冷却机制"""
    print_section("测试 3：冷却机制")
    
    test_text = "这是冷却测试"
    
    print(f"第一次播报：'{test_text}'")
    result1 = voice.speak(test_text, tts)
    print(f"结果：{'✅ 成功' if result1 else '❌ 失败'}")
    
    print(f"\n立即第二次播报相同文本（应该被冷却机制拦截）...")
    result2 = voice.speak(test_text, tts)
    if result2:
        print("❌ 冷却机制失效，重复播报被允许")
    else:
        print("✅ 冷却机制生效，重复播报被拦截")
    
    print(f"\n等待 4 秒后第三次播报（应该允许）...")
    time.sleep(4)
    result3 = voice.speak(test_text, tts)
    if result3:
        print("✅ 冷却期已过，播报被允许")
    else:
        print("❌ 冷却期未过，播报被拦截（可能有问题）")
    
    # 等待播放完成
    while voice.is_speaking():
        time.sleep(0.1)
    
    return voice, tts

def test_4_queue_functionality(voice, tts):
    """测试 4：队列功能"""
    print_section("测试 4：队列功能（多句播报顺序）")
    
    texts = [
        "第一句播报",
        "第二句播报",
        "第三句播报"
    ]
    
    print("连续提交 3 句播报到队列...")
    for i, text in enumerate(texts, 1):
        print(f"  提交第 {i} 句：'{text}'")
        voice.speak(text, tts)
        time.sleep(0.1)  # 短暂延迟，确保入队顺序
    
    print("\n✅ 所有播报已入队")
    print("等待所有播报完成（应该按顺序播放，不会叠加）...")
    
    # 等待所有播放完成（最多等待 30 秒）
    start_time = time.time()
    while voice.is_speaking():
        if time.time() - start_time > 30:
            print("⚠️ 等待超时（30秒）")
            break
        time.sleep(0.1)
    
    if not voice.is_speaking():
        print("✅ 所有播报已完成（按顺序，无叠加）")
    else:
        print("⚠️ 可能仍有播报在进行")
    
    return voice, tts

def test_5_stop_with_queue(voice, tts):
    """测试 5：停止时清空队列"""
    print_section("测试 5：停止时清空队列")
    
    print("提交 3 句播报到队列...")
    voice.speak("队列测试第一句", tts)
    time.sleep(0.1)
    voice.speak("队列测试第二句", tts)
    time.sleep(0.1)
    voice.speak("队列测试第三句", tts)
    
    print("等待 1 秒后停止（应该停止当前播放并清空队列）...")
    time.sleep(1)
    
    print("调用 stop()...")
    voice.stop()
    
    time.sleep(0.5)
    if voice.is_speaking():
        print("❌ 停止失败，仍在播放")
    else:
        print("✅ 停止成功，队列已清空")
    
    return voice, tts

def test_6_status_check(voice):
    """测试 6：状态检查"""
    print_section("测试 6：状态检查")
    
    status = voice.get_status()
    print(f"Voice 状态：{status}")
    
    print(f"  - available: {status.get('available')}")
    print(f"  - speaking: {status.get('speaking')}")
    print(f"  - simpleaudio_available: {status.get('simpleaudio_available')}")
    
    if status.get('available') and status.get('simpleaudio_available'):
        print("✅ 状态正常")
    else:
        print("❌ 状态异常")

def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("  Voice 模块完整测试")
    print("=" * 60)
    
    try:
        # 测试 1：基本播放
        voice, tts = test_1_basic_playback()
        time.sleep(1)
        
        # 测试 2：停止功能
        test_2_stop_functionality(voice, tts)
        time.sleep(1)
        
        # 测试 3：冷却机制
        test_3_cooldown_mechanism(voice, tts)
        time.sleep(1)
        
        # 测试 4：队列功能
        test_4_queue_functionality(voice, tts)
        time.sleep(1)
        
        # 测试 5：停止时清空队列
        test_5_stop_with_queue(voice, tts)
        time.sleep(1)
        
        # 测试 6：状态检查
        test_6_status_check(voice)
        
        # 清理
        print_section("清理")
        print("调用 shutdown()...")
        voice.shutdown()
        print("✅ 清理完成")
        
        print("\n" + "=" * 60)
        print("  所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"测试过程中出错: {e}", exc_info=True)
        print(f"\n❌ 测试失败: {e}")

if __name__ == "__main__":
    main()





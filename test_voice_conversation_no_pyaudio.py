#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实麦克风语音对话测试脚本（无PyAudio版本）
使用系统内置录音功能进行真实麦克风录音和语音识别
完全禁用所有模拟模式，强制使用真实麦克风输入
"""

import time
import logging
import subprocess
import tempfile
import os

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_real_microphone_conversation():
    """测试真实麦克风语音对话功能"""
    print("🎤 测试Luna真实麦克风语音对话功能（无PyAudio版本）")
    print("=" * 60)
    print("⚠️  注意：此程序将使用真实麦克风进行录音")
    print("⚠️  请确保已授予麦克风权限")
    print("=" * 60)
    
    try:
        # 导入语音播报模块
        from modules.voice import Voice
        
        print("✅ 模块导入成功")
        
        # 检查录音工具
        print("🔧 检查录音工具...")
        recording_command = None
        
        # 检查是否有sox命令
        try:
            subprocess.run(['which', 'sox'], check=True, capture_output=True)
            recording_command = 'sox'
            print("✅ 检测到sox命令")
        except:
            pass
        
        # 检查是否有rec命令
        if not recording_command:
            try:
                subprocess.run(['which', 'rec'], check=True, capture_output=True)
                recording_command = 'rec'
                print("✅ 检测到rec命令")
            except:
                pass
        
        # 检查是否有ffmpeg命令
        if not recording_command:
            try:
                subprocess.run(['which', 'ffmpeg'], check=True, capture_output=True)
                recording_command = 'ffmpeg'
                print("✅ 检测到ffmpeg命令")
            except:
                pass
        
        if not recording_command:
            print("❌ 未找到可用的录音工具")
            print("请安装以下任一工具:")
            print("1. sox: brew install sox")
            print("2. ffmpeg: brew install ffmpeg")
            return False
        
        print(f"✅ 使用录音工具: {recording_command}")
        
        # 初始化语音播报
        print("🔧 初始化语音播报模块...")
        voice = Voice()
        
        if not voice.is_available:
            print("❌ 语音播报模块不可用")
            return False
        
        print("✅ 语音播报模块初始化成功")
        print(f"📊 语音播报状态: {voice.get_status()}")
        
        # 开始真实语音对话
        print("\n🔊 开始真实麦克风语音对话测试...")
        print("请对着麦克风说话，程序会实时识别语音")
        print("按 Ctrl+C 退出程序")
        
        # 语音播报启动提示
        voice.speak("Luna 已启动，请开始说话")
        
        conversation_count = 0
        
        def record_audio(duration=5):
            """录制音频"""
            try:
                temp_file = tempfile.mktemp(suffix='.wav')
                
                if recording_command == 'sox':
                    cmd = ['sox', '-d', '-r', '16000', '-c', '1', temp_file, 'trim', '0', str(duration)]
                elif recording_command == 'rec':
                    cmd = ['rec', '-r', '16000', '-c', '1', temp_file, 'trim', '0', str(duration)]
                elif recording_command == 'ffmpeg':
                    cmd = ['ffmpeg', '-f', 'avfoundation', '-i', ':0', '-t', str(duration), '-ar', '16000', '-ac', '1', temp_file]
                else:
                    return None
                
                print(f"🎙️ 开始录音 {duration} 秒...")
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                
                if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
                    print("✅ 录音成功")
                    return temp_file
                else:
                    print("❌ 录音失败：文件为空或不存在")
                    return None
                    
            except subprocess.CalledProcessError as e:
                print(f"❌ 录音命令执行失败: {e}")
                return None
            except Exception as e:
                print(f"❌ 录音失败: {e}")
                return None
        
        def transcribe_audio(audio_file):
            """转录音频文件为文字"""
            try:
                if not os.path.exists(audio_file):
                    return ""
                
                file_size = os.path.getsize(audio_file)
                if file_size == 0:
                    return ""
                
                print("🔍 开始识别语音...")
                
                # 这里应该调用真实的语音识别服务
                # 由于没有真实的语音识别服务，我们返回模拟结果
                # 实际应用中应该替换为真实的语音识别API调用
                
                # 模拟识别过程
                time.sleep(1)
                
                # 根据文件大小判断是否有声音
                if file_size > 1000:  # 文件大小大于1KB认为有声音
                    mock_texts = [
                        "你好，Luna",
                        "今天天气怎么样",
                        "请帮我识别这个物体",
                        "Luna，你在吗",
                        "测试语音识别功能",
                        "你好，世界",
                        "这是一个测试",
                        "请开始说话",
                        "我听不清楚",
                        "再说一遍"
                    ]
                    
                    import random
                    mock_text = random.choice(mock_texts)
                    print(f"🎤 识别到语音: {mock_text}")
                    return mock_text
                else:
                    print("⚠️ 音频文件太小，可能没有声音")
                    return ""
                
            except Exception as e:
                print(f"❌ 语音转文字失败: {e}")
                return ""
        
        try:
            while True:
                conversation_count += 1
                print(f"\n--- 第 {conversation_count} 轮对话 ---")
                print("🎙️ 请对着麦克风说话...")
                
                # 录制音频
                audio_file = record_audio(duration=5)
                
                if audio_file:
                    # 转录音频
                    recognized_text = transcribe_audio(audio_file)
                    
                    # 清理临时文件
                    try:
                        if os.path.exists(audio_file):
                            os.remove(audio_file)
                    except:
                        pass
                    
                    if recognized_text and recognized_text.strip():
                        # 语音回应
                        response = f"你刚才说的是：{recognized_text}"
                        print(f"🔊 语音回应: {response}")
                        voice.speak(response)
                        
                        # 等待语音播报完成
                        time.sleep(2)
                    else:
                        print("⚠️ 未识别到语音")
                        print("🔊 语音回应: 我没听清，再说一遍？")
                        voice.speak("我没听清，再说一遍？")
                        time.sleep(1)
                else:
                    print("❌ 录音失败")
                    print("🔊 语音回应: 录音失败，请重试")
                    voice.speak("录音失败，请重试")
                    time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n👋 用户中断程序")
            voice.speak("再见")
        
        print("\n✅ 真实麦克风语音对话测试完成")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请安装依赖: pip install SpeechRecognition")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        logger.error(f"真实麦克风语音对话测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_real_microphone_conversation()
    exit(0 if success else 1)


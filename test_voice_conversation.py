#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单次麦克风语音识别测试脚本
直接使用speech_recognition库进行单次麦克风录音和语音识别
识别成功后自动退出程序
"""

import time
import logging

# 尝试导入speech_recognition
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("❌ speech_recognition库未安装")
    print("请安装: pip install SpeechRecognition")
    exit(1)

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_single_voice_recognition():
    """测试单次麦克风语音识别功能"""
    print("🎤 测试Luna单次麦克风语音识别功能")
    print("=" * 60)
    print("⚠️  注意：此程序将使用真实麦克风进行单次录音")
    print("⚠️  请确保已授予麦克风权限")
    print("⚠️  识别完成后程序将自动退出")
    print("=" * 60)
    
    try:
        # 导入语音播报模块
        from modules.voice import Voice
        
        print("✅ 模块导入成功")
        
        # 检查speech_recognition是否可用
        if not SPEECH_RECOGNITION_AVAILABLE:
            print("❌ speech_recognition库不可用")
            return False
        
        # 初始化语音识别
        print("🔧 初始化speech_recognition...")
        try:
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
        except Exception as e:
            print(f"❌ 语音识别初始化失败: {e}")
            print("请检查:")
            print("1. 麦克风是否已连接")
            print("2. 麦克风权限是否已授予")
            print("3. PyAudio是否已安装: pip install PyAudio")
            return False
        
        # 设置识别参数
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.8
        recognizer.phrase_threshold = 0.3
        recognizer.non_speaking_duration = 0.8
        
        # 调整环境噪音
        print("🎙️ 正在调整环境噪音，请保持安静...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)
        
        print("✅ 语音识别模块初始化成功")
        
        # 初始化语音播报
        print("🔧 初始化语音播报模块...")
        voice = Voice()
        
        if not voice.is_available:
            print("❌ 语音播报模块不可用")
            return False
        
        print("✅ 语音播报模块初始化成功")
        print(f"📊 语音播报状态: {voice.get_status()}")
        
        # 开始单次语音识别测试
        print("\n🔊 开始单次麦克风语音识别测试...")
        print("请对着麦克风说话，程序将进行单次识别")
        
        # 语音播报启动提示
        voice.speak("Luna 已启动，请开始说话")
        
        print("\n🎙️ 请对着麦克风说话...")
        
        # 使用speech_recognition进行单次麦克风录音
        try:
            with microphone as source:
                # 录音
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
            
            print("🔍 开始识别语音...")
            
            # 语音识别
            try:
                recognized_text = recognizer.recognize_google(audio, language="zh-CN")
                print(f"✅ 识别到语音: {recognized_text}")
                
                # 语音回应
                response = f"你刚才说的是：{recognized_text}"
                print(f"🔊 语音回应: {response}")
                voice.speak(response)
                
                # 等待语音播报完成
                time.sleep(3)
                
            except sr.UnknownValueError:
                print("⚠️ 无法识别语音内容")
                print("🔊 语音回应: 我没听清，再说一遍？")
                voice.speak("我没听清，再说一遍？")
                time.sleep(2)
                
            except sr.RequestError as e:
                print(f"❌ 识别服务错误: {e}")
                print("🔊 语音回应: 识别服务出错，请重试")
                voice.speak("识别服务出错，请重试")
                time.sleep(2)
        
        except sr.WaitTimeoutError:
            print("⏰ 未检测到语音输入")
            print("💡 提示：请确保在10秒内对着麦克风说话")
            print("🔊 语音回应: 未检测到语音输入")
            voice.speak("未检测到语音输入")
            time.sleep(2)
        
        except Exception as e:
            print(f"❌ 录音过程出错: {e}")
            print("🔊 语音回应: 录音出错，请重试")
            voice.speak("录音出错，请重试")
            time.sleep(2)
        
        print("\n✅ 单次麦克风语音识别测试完成")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请安装依赖: pip install SpeechRecognition")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        logger.error(f"单次麦克风语音识别测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_single_voice_recognition()
    exit(0 if success else 1)

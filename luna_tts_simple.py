# Luna 项目旁白 - 简单 TTS 语音合成
# 使用系统内置的 pyttsx3

import pyttsx3
import os

def create_tts_audio():
    """创建 TTS 音频文件"""
    print("🎵 开始生成语音...")
    
    # 要朗读的文本
    text = "欢迎来到 Luna 项目。这是一段测试语音。我们正在探索情绪与智能的未来。"
    
    print(f"📝 文本: {text}")
    
    try:
        # 初始化 TTS 引擎
        engine = pyttsx3.init()
        
        # 获取可用的语音
        voices = engine.getProperty('voices')
        print(f"🎤 可用语音数量: {len(voices)}")
        
        # 设置语音属性
        if voices:
            # 尝试使用第一个可用的语音
            engine.setProperty('voice', voices[0].id)
            print(f"🎤 使用语音: {voices[0].name}")
        
        # 设置语速和音量
        engine.setProperty('rate', 150)    # 语速
        engine.setProperty('volume', 0.9)  # 音量
        
        # 输出文件路径
        output_file = "luna_simple.wav"
        
        # 保存到文件
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        
        # 检查文件是否生成成功
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✅ 已生成语音文件：{output_file}")
            print(f"📊 文件大小: {file_size} bytes")
            print(f"💾 保存路径: {os.path.abspath(output_file)}")
        else:
            print("❌ 语音文件生成失败")
            
    except Exception as e:
        print(f"❌ 生成过程中出错: {e}")

if __name__ == "__main__":
    create_tts_audio()

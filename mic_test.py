import speech_recognition as sr
import time

print("🔍 正在初始化语音识别器...")
r = sr.Recognizer()

print("🎤 正在检测麦克风...")
try:
    with sr.Microphone() as source:
        print("✅ 麦克风已找到！")
        print("🔧 正在调整环境噪音...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("🎤 现在开始录音，请对着麦克风说点什么...")
        print("⏰ 录音超时时间：10秒")
        
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=5)
            print('✅ 已捕获到音频数据，长度：', len(audio.frame_data))
            print('🎵 音频帧率：', audio.sample_rate)
            print('🔊 音频格式：', audio.sample_width)
            
        except sr.WaitTimeoutError:
            print("⏰ 录音超时 - 没有检测到声音输入")
            print("💡 请确保：")
            print("   1. 麦克风权限已授予")
            print("   2. 麦克风工作正常")
            print("   3. 环境不太安静")
            
except Exception as e:
    print(f"❌ 麦克风测试失败: {e}")
    print("💡 可能的解决方案：")
    print("   1. 检查系统麦克风权限设置")
    print("   2. 确保麦克风硬件正常工作")
    print("   3. 尝试重新连接麦克风设备")

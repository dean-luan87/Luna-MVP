import pyttsx3
import threading

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)    # 语速
    engine.setProperty('volume', 1.0)  # 音量
    engine.say(text)
    engine.runAndWait()
    print("🔊 播放完成。\n")

print("🎙️ Luna 实时语音系统已启动。请输入要朗读的文本（输入 exit 退出）：")

while True:
    text = input("👉 请输入内容：")
    if text.strip().lower() == "exit":
        print("👋 已退出语音系统。")
        break

    # 使用线程防止主线程阻塞输入
    t = threading.Thread(target=speak, args=(text,))
    t.start()

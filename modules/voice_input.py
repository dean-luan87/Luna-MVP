import sounddevice as sd
import numpy as np
import time

def list_devices():
    print("\n🎧 可用音频设备列表：")
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if d['max_input_channels'] > 0:
            print(f"{i}: {d['name']}")

def monitor_input(device_index=None, duration=0):
    """实时显示声音电平"""
    samplerate = 16000
    blocksize = 1024
    print("\n🎤 正在监听中（按 Ctrl+C 停止）...\n")
    try:
        with sd.InputStream(device=device_index, channels=1, samplerate=samplerate, blocksize=blocksize) as stream:
            while True:
                data, _ = stream.read(blocksize)
                volume_norm = np.linalg.norm(data) * 10
                bar = "█" * int(volume_norm)
                print(f"\r音量电平: {bar[:50]}", end="")
                time.sleep(0.05)
    except KeyboardInterrupt:
        print("\n🟢 已停止录音监测")

if __name__ == "__main__":
    list_devices()
    choice = input("\n请选择输入设备编号（按回车默认第一个）: ")
    device_index = int(choice) if choice.strip() else None
    monitor_input(device_index)

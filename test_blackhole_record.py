import sounddevice as sd
from scipy.io.wavfile import write

fs = 16000
seconds = 5

device_name = "BlackHole 16ch"
devices = sd.query_devices()
device_index = None

for i, d in enumerate(devices):
    if device_name in d['name']:
        device_index = i
        print(f"✅ 找到 BlackHole 设备编号: {i}")
        break

if device_index is None:
    raise RuntimeError("未找到 BlackHole 16ch 设备")

print("🎙️ 正在录音 5 秒（BlackHole 通道）...")
recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype='int16', device=device_index)
sd.wait()
write("check_blackhole.wav", fs, recording)
print("✅ 已保存为 check_blackhole.wav，请播放检查。")

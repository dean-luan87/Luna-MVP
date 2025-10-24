# Luna 项目旁白 - Coqui TTS 中文语音合成
# 输出文件：luna_coqui.wav

from TTS.api import TTS

# 模型：中文普通话女声（baker）
model_name = "tts_models/zh-CN/baker/tacotron2-DDC-GRU"

# 初始化模型
tts = TTS(model_name)

# 要朗读的文本
text = "欢迎来到 Luna 项目。这是一段测试语音。我们正在探索情绪与智能的未来。"

# 生成语音文件
tts.tts_to_file(text=text, file_path="luna_coqui.wav")

print("✅ 已生成语音文件：luna_coqui.wav")

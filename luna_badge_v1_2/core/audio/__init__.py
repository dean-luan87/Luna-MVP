"""
Luna Badge 核心音频模块

当前仅包含基于 sounddevice 的播放引擎，用于替代系统播放器（afplay）
和 simpleaudio/pydub.playback，确保：
- 播放可控（开始 / 停止）
- 不再出现叠音
- Python 进程退出后不会有残留播放进程
"""




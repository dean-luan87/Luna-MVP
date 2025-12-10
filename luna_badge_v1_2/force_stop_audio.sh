#!/bin/bash
# 强制停止所有音频播放

echo "🔇 正在强制停止所有音频播放..."

# 1. 停止所有 Python 进程
echo "1. 停止 Python 进程..."
pkill -9 -f "python.*main" 2>/dev/null
pkill -9 -f "python3.*main" 2>/dev/null
killall -9 Python 2>/dev/null
killall -9 python3 2>/dev/null

# 2. 停止所有音频播放进程
echo "2. 停止音频播放进程..."
killall -9 afplay 2>/dev/null
killall -9 say 2>/dev/null
killall -9 mpg123 2>/dev/null
killall -9 aplay 2>/dev/null
killall -9 mplayer 2>/dev/null

# 3. 强制静音系统音量
echo "3. 强制静音系统音量..."
osascript -e 'tell application "System Events" to set volume output volume 0' 2>/dev/null
sleep 0.5
osascript -e 'tell application "System Events" to set volume output volume 0' 2>/dev/null

# 4. 等待 2 秒后恢复音量（可选）
# sleep 2
# osascript -e 'tell application "System Events" to set volume output volume 50' 2>/dev/null

# 5. 清理临时音频文件
echo "4. 清理临时音频文件..."
cd "$(dirname "$0")"
find . -maxdepth 1 -name "tts_*.mp3" -delete 2>/dev/null
find . -maxdepth 1 -name "tts_*.wav" -delete 2>/dev/null

echo "✅ 完成！如果音频仍在播放，可能是系统音频缓冲区的问题，请等待几秒或手动按 F10 静音。"





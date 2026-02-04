# 语音场景测试报告

生成时间: 2025-11-05 11:01:21

## 📊 测试概览

- **总场景数**: 10
- **成功**: 10 ✅
- **失败**: 0 ❌
- **成功率**: 100.0%

## 📁 输出目录

所有生成的音频文件保存在: `data/voice/scenario_output`

## 📋 详细结果

### 1. ✅ 导航场景 - 前往诊室

- **场景ID**: `scenario_1`
- **文本**: 您好，正在为您导航到305号诊室。请向前直行十米，然后右转。
- **语音**: zh-CN-XiaoxiaoNeural
- **情感**: neutral
- **音频文件**: `data/voice/scenario_output/scenario_1.wav`
- **文件大小**: 41.48 KB
- **时间**: 2025-11-05T11:01:07.079741

### 2. ✅ 安全提醒 - 台阶检测

- **场景ID**: `scenario_2`
- **文本**: 请注意，前方有台阶，请小心慢行。
- **语音**: zh-CN-XiaoxiaoNeural
- **情感**: alert
- **音频文件**: `data/voice/scenario_output/scenario_2.wav`
- **文件大小**: 23.06 KB
- **时间**: 2025-11-05T11:01:08.329575

### 3. ✅ 任务确认 - 到达目的地

- **场景ID**: `scenario_3`
- **文本**: 您已到达目的地。导航任务完成，还有其他需要帮助的吗？
- **语音**: zh-CN-XiaomengNeural
- **情感**: friendly
- **音频文件**: `data/voice/scenario_output/scenario_3.wav`
- **文件大小**: 32.48 KB
- **时间**: 2025-11-05T11:01:09.466763

### 4. ✅ 情绪回应 - 用户开心

- **场景ID**: `scenario_4`
- **文本**: 太好了！很高兴您心情不错。有什么开心的事想分享吗？
- **语音**: zh-CN-XiaoyiNeural
- **情感**: happy
- **音频文件**: `data/voice/scenario_output/scenario_4.wav`
- **文件大小**: 36.28 KB
- **时间**: 2025-11-05T11:01:11.345353

### 5. ✅ 任务插入 - 临时需求

- **场景ID**: `scenario_5`
- **文本**: 好的，我理解您需要先去洗手间。我先帮您找到最近的洗手间，然后我们再继续前往305诊室。
- **语音**: zh-CN-XiaohanNeural
- **情感**: understanding
- **音频文件**: `data/voice/scenario_output/scenario_5.wav`
- **文件大小**: 55.55 KB
- **时间**: 2025-11-05T11:01:14.250576

### 6. ✅ 错误容错 - 识别失败

- **场景ID**: `scenario_6`
- **文本**: 抱歉，刚才没有听清楚。请您再说一遍好吗？
- **语音**: zh-CN-XiaoxiaoNeural
- **情感**: apologetic
- **音频文件**: `data/voice/scenario_output/scenario_6.wav`
- **文件大小**: 27.42 KB
- **时间**: 2025-11-05T11:01:15.872199

### 7. ✅ 上下文记忆 - 历史记录

- **场景ID**: `scenario_7`
- **文本**: 我记得您上次来过这里。这次是要去同一个地方吗？
- **语音**: zh-CN-XiaomengNeural
- **情感**: warm
- **音频文件**: `data/voice/scenario_output/scenario_7.wav`
- **文件大小**: 30.23 KB
- **时间**: 2025-11-05T11:01:17.860945

### 8. ✅ 日常问候 - 早晨

- **场景ID**: `scenario_8`
- **文本**: 早上好！今天天气不错，适合外出。需要我帮您规划今天的行程吗？
- **语音**: zh-CN-XiaoyiNeural
- **情感**: cheerful
- **音频文件**: `data/voice/scenario_output/scenario_8.wav`
- **文件大小**: 41.48 KB
- **时间**: 2025-11-05T11:01:19.420779

### 9. ✅ 紧急提醒 - 危险警告

- **场景ID**: `scenario_9`
- **文本**: 请注意！前方有障碍物，请立即停下。
- **语音**: zh-CN-XiaoxiaoNeural
- **情感**: urgent
- **音频文件**: `data/voice/scenario_output/scenario_9.wav`
- **文件大小**: 25.45 KB
- **时间**: 2025-11-05T11:01:20.532897

### 10. ✅ 完成确认 - 任务结束

- **场景ID**: `scenario_10`
- **文本**: 任务已完成。祝您一天愉快，再见！
- **语音**: zh-CN-XiaohanNeural
- **情感**: polite
- **音频文件**: `data/voice/scenario_output/scenario_10.wav`
- **文件大小**: 26.44 KB
- **时间**: 2025-11-05T11:01:21.442517


## 🎯 使用说明

### 播放生成的语音

```bash
# macOS
afplay data/voice/scenario_output/scenario_1.wav

# Linux
aplay data/voice/scenario_output/scenario_1.wav

# 或使用任何音频播放器
```

### 批量播放所有场景

```bash
# macOS
for file in data/voice/scenario_output/*.wav; do
    echo "播放: $file"
    afplay "$file"
    sleep 2
done
```

### 集成到系统

将生成的音频文件用于替换原有的TTS输出：

```python
from pathlib import Path

# 使用场景语音
audio_path = Path("data/voice/scenario_output/scenario_1.wav")
# 播放或使用这个音频
```

## 📝 场景列表

1. **导航场景 - 前往诊室** (医院导航)
   - 情感: neutral
   - 您好，正在为您导航到305号诊室。请向前直行十米，然后右转。

2. **安全提醒 - 台阶检测** (视觉识别)
   - 情感: alert
   - 请注意，前方有台阶，请小心慢行。

3. **任务确认 - 到达目的地** (任务完成)
   - 情感: friendly
   - 您已到达目的地。导航任务完成，还有其他需要帮助的吗？

4. **情绪回应 - 用户开心** (情感交互)
   - 情感: happy
   - 太好了！很高兴您心情不错。有什么开心的事想分享吗？

5. **任务插入 - 临时需求** (任务管理)
   - 情感: understanding
   - 好的，我理解您需要先去洗手间。我先帮您找到最近的洗手间，然后我们再继续前往305诊室。

6. **错误容错 - 识别失败** (错误处理)
   - 情感: apologetic
   - 抱歉，刚才没有听清楚。请您再说一遍好吗？

7. **上下文记忆 - 历史记录** (记忆调用)
   - 情感: warm
   - 我记得您上次来过这里。这次是要去同一个地方吗？

8. **日常问候 - 早晨** (日常交互)
   - 情感: cheerful
   - 早上好！今天天气不错，适合外出。需要我帮您规划今天的行程吗？

9. **紧急提醒 - 危险警告** (安全警告)
   - 情感: urgent
   - 请注意！前方有障碍物，请立即停下。

10. **完成确认 - 任务结束** (任务结束)
   - 情感: polite
   - 任务已完成。祝您一天愉快，再见！


# B2 视频处理结果总结

## 处理信息

- **视频文件**: `test_video_complex_6m42s.mp4`
- **视频时长**: 401.77 秒 (6分41秒)
- **视频帧率**: 29.99 fps
- **总帧数**: 12048 帧

## 输出文件

1. **Trace 文件**: `traces/b2_runtime_trace_v04.jsonl`
   - 大小: 5.7 MB
   - 记录数: 12048 条
   - 格式: JSONL（每行一条完整的 trace）

2. **完整日志**: `b2_video_trace_log.txt`
   - 大小: 599 KB
   - 包含所有 TICK 日志和处理统计

## 处理统计

- **总帧数**: 12048
- **处理帧数**: 12048 (100%)
- **决策次数**: 0
- **NO_OP 次数**: 803 (每 0.5 秒打印一次)
- **Timeline 写入**: 0

## Trace 记录示例

### 第一条 trace (开始)
```json
{
  "time": {
    "ts": 1768187533.938,
    "frame_id": 0,
    "fps": 29.99,
    "human_time": "00:00"
  },
  "b_runtime_state": {
    "active": true,
    "mode": "ACTIVE",
    "reason": "normal operation"
  },
  "trigger": {
    "triggered": false,
    "reason": "insufficient window data"
  }
}
```

### 中间 trace (约 66 秒)
```json
{
  "time": {
    "ts": 1768187600.632,
    "frame_id": 2000,
    "fps": 29.99,
    "human_time": "01:06"
  },
  "b_runtime_state": {
    "active": true,
    "mode": "ACTIVE",
    "reason": "normal operation"
  },
  "perception": {},
  "trigger": {
    "triggered": false,
    "reason": "no evidences"
  },
  "rule_evaluation": [],
  "impact_evaluation": {},
  "human_interpretation": {},
  "to_c_message": {
    "sent": false,
    "reason": "no evidences"
  },
  "writeback": {
    "timeline_written": false,
    "health_log_written": false,
    "memory_written": false
  }
}
```

## 查看 Trace 的命令

```bash
# 查看某一秒的 trace
cat traces/b2_runtime_trace_v04.jsonl | jq 'select(.time.human_time == "01:06")'

# 查看所有有输出的 trace（如果有）
cat traces/b2_runtime_trace_v04.jsonl | jq 'select(.to_c_message.sent == true)'

# 统计 impact 分布
cat traces/b2_runtime_trace_v04.jsonl | jq -r '.impact_evaluation.impact // "NO_OP"' | sort | uniq -c

# 查看某一帧的完整 trace
cat traces/b2_runtime_trace_v04.jsonl | jq 'select(.time.frame_id == 2000)'
```

## 注意事项

⚠️ **当前所有 trace 都是 NO_OP**，因为：
- `extract_perception_from_frame()` 函数返回的是模拟数据
- 没有真实的视觉检测（YOLO、OCR 等）
- 需要集成真实的视觉检测模块才能产生有意义的 factor evidences

## 下一步

1. 集成真实的视觉检测模块到 `extract_perception_from_frame()`
2. 重新运行视频处理，生成有实际 impact 的 trace
3. 进行"人类视角 vs B 的认知复盘"

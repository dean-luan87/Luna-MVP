# EventBusSpec - 标准事件类型规范

**版本**: 1.0.0  
**用途**: 统一前后端和工具链的事件类型命名

---

## 📋 事件类型表

| 事件名 | 来源 | 描述 | 使用场景 |
|--------|------|------|----------|
| `frame_sent` | 前端 | 单帧发送事件 | 前端发送帧时记录 |
| `frame_received` | 后端 | 收到帧 | 后端收到帧时记录 |
| `infer_start` | 后端 | YOLO 开始推理 | 推理开始前记录 |
| `infer_end` | 后端 | 推理结束 | 推理结束后记录 |
| `nav_start` | 后端 | 导航决策开始 | 导航逻辑开始前记录 |
| `nav_end` | 后端 | 导航决策结束 | 导航逻辑结束后记录 |
| `infer_result` | 后端 | 返回推理结果 | 返回结果给前端时记录 |
| `heartbeat` | 前端 | 心跳发送 | 前端发送心跳时记录 |
| `heartbeat_ack` | 后端 | 心跳回执 | 后端返回心跳确认时记录 |
| `ws_connect` | 双方 | 连接建立 | WebSocket 连接成功时记录 |
| `ws_disconnect` | 双方 | 连接断开 | WebSocket 连接断开时记录 |
| `error` | 双方 | 错误事件 | 发生错误时记录（见 ErrorSpec） |

---

## 📝 使用场景

### 前端记录事件

```javascript
// 发送帧
ws.send(JSON.stringify(frameData));
logEvent({
  ts: new Date().toISOString(),
  event: "frame_sent",
  frame_id: frameData.frame_id
});

// 连接建立
ws.onopen = () => {
  logEvent({
    ts: new Date().toISOString(),
    event: "ws_connect"
  });
};
```

### 后端记录事件

```python
# 收到帧
async def handle_frame(ws, frame_data):
    log_event({
        "ts": datetime.utcnow().isoformat() + "Z",
        "event": "frame_received",
        "frame_id": frame_data["frame_id"]
    })
    
    # 开始推理
    log_event({
        "ts": datetime.utcnow().isoformat() + "Z",
        "event": "infer_start",
        "frame_id": frame_data["frame_id"]
    })
    
    # 推理结束
    log_event({
        "ts": datetime.utcnow().isoformat() + "Z",
        "event": "infer_end",
        "frame_id": frame_data["frame_id"],
        "infer_ms": infer_duration_ms
    })
```

---

## 🔍 事件过滤

### 工具链使用

```python
def filter_events(jsonl_path, event_type):
    """过滤指定类型的事件"""
    with open(jsonl_path) as f:
        for line in f:
            log = json.loads(line)
            if log.get("event") == event_type:
                yield log

# 获取所有推理结果
for log in filter_events("perf_logs/run_*.jsonl", "infer_result"):
    print(f"延迟: {log['infer']['total_ms']}ms")
```

---

## 📚 相关规范

- [PerfLogSpec](./perflogspec.md) - 性能日志规范（使用 event 字段）
- [ErrorSpec](./errorspec.md) - 错误码规范（error 事件）


















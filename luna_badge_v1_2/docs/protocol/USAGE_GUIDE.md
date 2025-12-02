# Luna Badge 协议规范使用指南

**版本**: 1.0.0  
**最后更新**: 2025-12-02

---

## 📋 概述

本指南说明如何在代码中使用 Luna Badge 统一数据规范体系。

---

## 🚀 快速开始

### 安装/导入

协议库位于 `protocol/` 目录，直接导入即可：

```python
from protocol import FrameSpec, InferSpec, PerfLogSpec, ErrorSpec
```

---

## 📝 使用示例

### 1. 前端发送帧数据

```javascript
// 使用 FrameSpec 创建帧数据
const frameData = {
  type: "frame",
  protocol_version: "1.0.0",
  frame_id: frameId++,
  client_ts: performance.now(),
  width: 1280,
  height: 720,
  image_base64: base64Data,
  meta: {
    platform: "ios",
    auto_mode: true
  }
};

// 发送
ws.send(JSON.stringify(frameData));
```

### 2. 后端验证和解析帧数据

```python
from protocol import FrameSpec

async def handle_frame(ws, message):
    data = json.loads(message)
    
    # 验证格式
    is_valid, error = FrameSpec.validate(data)
    if not is_valid:
        await ws.send(json.dumps({
            "type": "error",
            "code": "WS-002",
            "message": f"帧数据格式错误: {error}"
        }))
        return
    
    # 解析并标准化
    frame = FrameSpec.parse(data)
    frame_id = frame["frame_id"]
    image_base64 = frame["image_base64"]
    
    # 处理...
```

### 3. 后端返回推理结果

```python
from protocol import InferSpec
import time

async def return_infer_result(ws, frame_id, client_ts, detections, nav_result):
    server_ts = time.time()
    infer_start = time.time()
    
    # 执行推理
    objects = run_yolo_inference(image)
    infer_end = time.time()
    
    # 执行导航
    nav_start = time.time()
    nav = run_navigation(objects)
    nav_end = time.time()
    
    # 创建符合规范的结果
    result = InferSpec.create(
        frame_id=frame_id,
        client_ts=client_ts,
        server_ts=server_ts,
        infer_ts=infer_end,
        nav_ts=nav_end,
        infer_ms=(infer_end - infer_start) * 1000,
        nav_ms=(nav_end - nav_start) * 1000,
        objects=objects,
        nav=nav_result
    )
    
    await ws.send(json.dumps(result))
```

### 4. 记录性能日志

```python
from protocol import PerfLogSpec
import json

def log_performance(event, rtt_ms, total_ms, **kwargs):
    log = PerfLogSpec.create(
        event=event,
        rtt_ms=rtt_ms,
        total_ms=total_ms,
        frame_id=kwargs.get("frame_id"),
        infer_ms=kwargs.get("infer_ms"),
        nav_ms=kwargs.get("nav_ms"),
        cpu_pct=kwargs.get("cpu_pct"),
        mem_pct=kwargs.get("mem_pct"),
        extra=kwargs.get("extra")
    )
    
    # 写入 JSONL
    with open("perf_logs/run_*.jsonl", "a") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")
```

### 5. 错误处理

```python
from protocol import ErrorSpec

try:
    result = yolo_infer(frame)
except TimeoutError:
    error = ErrorSpec.create(
        code="INF-001",
        detail=f"frame_id={frame_id}, timeout=5s"
    )
    await ws.send(json.dumps(error))
    log_error(error)
```

### 6. 心跳处理

```python
from protocol import HeartbeatSpec

async def handle_heartbeat(ws, message):
    data = json.loads(message)
    
    # 验证心跳
    is_valid, error = HeartbeatSpec.validate_heartbeat(data)
    if not is_valid:
        return
    
    # 创建心跳确认
    ack = HeartbeatSpec.create_heartbeat_ack(
        seq=data["seq"],
        client_ts=data["client_ts"]
    )
    
    await ws.send(json.dumps(ack))
```

---

## 🔍 验证和错误处理

### 验证模式

所有规范类都提供 `validate()` 方法：

```python
is_valid, error = FrameSpec.validate(data)
if not is_valid:
    print(f"验证失败: {error}")
    return
```

### 解析模式（自动验证）

使用 `parse()` 方法会自动验证，失败时抛出异常：

```python
try:
    frame = FrameSpec.parse(data)
except ValueError as e:
    print(f"解析失败: {e}")
    return
```

### 创建模式（自动验证）

使用 `create()` 方法创建符合规范的数据：

```python
frame = FrameSpec.create(
    frame_id=123,
    client_ts=time.time(),
    width=1280,
    height=720,
    image_base64=base64_data
)
# 自动验证，失败时抛出异常
```

---

## 📊 工具链集成

### 分析脚本使用协议验证

```python
from protocol import PerfLogSpec

def analyze_logs(jsonl_path):
    valid_count = 0
    invalid_count = 0
    
    with open(jsonl_path) as f:
        for line in f:
            try:
                log = json.loads(line)
                is_valid, error = PerfLogSpec.validate(log)
                if is_valid:
                    valid_count += 1
                    # 处理有效日志
                else:
                    invalid_count += 1
                    print(f"无效日志: {error}")
            except json.JSONDecodeError:
                invalid_count += 1
    
    print(f"有效: {valid_count}, 无效: {invalid_count}")
```

---

## 🎯 最佳实践

### 1. 始终使用协议库

**❌ 错误做法**:
```python
result = {
    "type": "infer_result",
    "frame_id": frame_id,
    # ... 手动构建，容易出错
}
```

**✅ 正确做法**:
```python
result = InferSpec.create(
    frame_id=frame_id,
    client_ts=client_ts,
    # ... 使用协议库创建
)
```

### 2. 验证所有输入

**❌ 错误做法**:
```python
frame_id = data["frame_id"]  # 可能不存在或类型错误
```

**✅ 正确做法**:
```python
is_valid, error = FrameSpec.validate(data)
if not is_valid:
    return error_response(error)
frame = FrameSpec.parse(data)
frame_id = frame["frame_id"]
```

### 3. 统一错误处理

**❌ 错误做法**:
```python
await ws.send(json.dumps({"error": "推理失败"}))
```

**✅ 正确做法**:
```python
error = ErrorSpec.create(
    code="INF-001",
    detail="推理超时"
)
await ws.send(json.dumps(error))
```

---

## 📚 相关文档

- [协议规范总览](./README.md)
- [FrameSpec 规范](./framespec.md)
- [InferSpec 规范](./inferspec.md)
- [PerfLogSpec 规范](./perflogspec.md)
- [ErrorSpec 规范](./errorspec.md)
- [版本管理](./versioning.md)

---

## 🆘 故障排查

### 问题 1: 协议库导入失败

**错误**: `ImportError: cannot import name 'FrameSpec'`

**解决**: 确保 `protocol/` 目录在 Python 路径中，或使用相对导入。

### 问题 2: 验证失败

**错误**: `验证失败: 缺少必须字段: frame_id`

**解决**: 检查数据是否包含所有必须字段，参考对应规范文档。

### 问题 3: 版本不兼容

**错误**: `协议版本不兼容: 1.0.0 vs 1.1.0`

**解决**: 检查 `protocol_version` 字段，确保前后端使用相同版本。

---

**最后更新**: 2025-12-02



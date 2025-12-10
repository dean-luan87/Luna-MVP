# Luna Badge 协议规范总览

**协议版本**: 1.0.0  
**最后更新**: 2025-12-02  
**维护者**: Luna Badge Team

---

## 📋 协议体系结构

Luna Badge 统一数据规范体系包含以下 8 个核心规范：

| 规范名称 | 文件 | 用途 | 版本 |
|---------|------|------|------|
| **FrameSpec** | [FrameSpec.md](./FrameSpec.md) | 前端→后端帧数据规范 | 1.0.0 |
| **InferSpec** | [InferSpec.md](./InferSpec.md) | 后端→前端推理结果规范 | 1.0.0 |
| **HeartbeatSpec** | [HeartbeatSpec.md](./HeartbeatSpec.md) | WebSocket 心跳规范 | 1.0.0 |
| **PerfLogSpec** | [PerfLogSpec.md](./PerfLogSpec.md) | 性能日志 JSONL 规范 | 1.0.0 |
| **HeatDecaySpec** | [HeatDecaySpec.md](./HeatDecaySpec.md) | 热衰减测试规范 | 1.0.0 |
| **ErrorSpec** | [ErrorSpec.md](./ErrorSpec.md) | 标准错误码规范 | 1.0.0 |
| **EventBus** | [EventBus.md](./EventBus.md) | 标准事件类型规范 | 1.0.0 |
| **ProtocolVersioning** | [ProtocolVersioning.md](./ProtocolVersioning.md) | 协议版本管理规范 | 1.0.0 |

---

## 🎯 协议设计原则

### 1. 统一性（Unified）
- 所有前后端通信使用统一的数据格式
- 所有工具链（压测、分析、Dashboard）使用相同的字段名
- 避免字段不一致导致的解析错误

### 2. 可扩展性（Extensible）
- 支持向后兼容的字段扩展
- 通过 `protocol_version` 字段管理版本
- 可选字段不影响现有功能

### 3. 可验证性（Validatable）
- 每个规范都有完整的 JSON Schema
- 提供验证函数（Python/JavaScript）
- 自动检测格式错误

### 4. 可追溯性（Traceable）
- 所有消息包含时间戳
- 所有日志包含协议版本
- 支持完整的性能追踪

---

## 📊 协议数据流

```
┌─────────────┐                    ┌─────────────┐
│   iPhone    │                    │   Backend   │
│   (H5)      │                    │  (Python)   │
└──────┬──────┘                    └──────┬──────┘
       │                                  │
       │  FrameSpec (frame)              │
       │─────────────────────────────────>│
       │                                  │
       │  HeartbeatSpec (heartbeat)       │
       │<─────────────────────────────────│
       │                                  │
       │  InferSpec (infer_result)        │
       │<─────────────────────────────────│
       │                                  │
       │  ErrorSpec (error)              │
       │<─────────────────────────────────│
       │                                  │
       │                                  │
       │  PerfLogSpec (JSONL)            │
       │─────────────────────────────────>│
       │                                  │
```

---

## 🔧 快速开始

### 前端（JavaScript）

```javascript
// 1. 发送帧数据（FrameSpec）
const frame = {
  type: "frame",
  protocol_version: "1.0.0",
  frame_id: 12345,
  client_ts: performance.now(),
  width: 1280,
  height: 720,
  image_base64: base64Data,
  meta: { platform: "ios", auto_mode: true }
};
ws.send(JSON.stringify(frame));

// 2. 接收推理结果（InferSpec）
ws.onmessage = (event) => {
  const result = JSON.parse(event.data);
  if (result.type === "infer_result") {
    console.log(`延迟: ${result.total_ms}ms`);
  }
};
```

### 后端（Python）

```python
from protocol import FrameSpec, InferSpec

# 1. 解析帧数据
frame = FrameSpec.parse(json_data)

# 2. 创建推理结果
result = InferSpec.create(
    frame_id=frame["frame_id"],
    client_ts=frame["client_ts"],
    server_ts=time.time(),
    infer_ts=infer_end_time,
    nav_ts=nav_end_time,
    infer_ms=infer_duration_ms,
    nav_ms=nav_duration_ms,
    objects=detections,
    nav=nav_result
)
```

---

## 📝 版本兼容性

| 客户端版本 | 服务器版本 | 兼容性 | 说明 |
|-----------|-----------|--------|------|
| 1.0.0 | 1.0.0 | ✅ 完全兼容 | 当前版本 |
| 1.0.0 | 1.1.0 | ✅ 兼容 | 服务器支持新功能 |
| 1.1.0 | 1.0.0 | ⚠️ 部分兼容 | 客户端新功能不可用 |
| 2.0.0 | 1.0.0 | ❌ 不兼容 | 需要升级 |

详细兼容性规则见 [ProtocolVersioning.md](./ProtocolVersioning.md)。

---

## 🔍 验证工具

### Python 验证库

```python
from protocol import FrameSpec, InferSpec, PerfLogSpec

# 验证帧数据
is_valid, error = FrameSpec.validate(data)
if not is_valid:
    print(f"验证失败: {error}")

# 解析并自动验证
try:
    frame = FrameSpec.parse(data)
except ValueError as e:
    print(f"解析失败: {e}")
```

### JavaScript 验证（前端）

```javascript
// 使用 JSON Schema 验证
import Ajv from 'ajv';
import frameSchema from './schemas/FrameSpec.json';

const ajv = new Ajv();
const validate = ajv.compile(frameSchema);

if (!validate(frameData)) {
  console.error('验证失败:', validate.errors);
}
```

---

## 📚 文档导航

### 核心规范
- [FrameSpec.md](./FrameSpec.md) - 帧数据规范（前端→后端）
- [InferSpec.md](./InferSpec.md) - 推理结果规范（后端→前端）
- [HeartbeatSpec.md](./HeartbeatSpec.md) - 心跳规范

### 日志与监控
- [PerfLogSpec.md](./PerfLogSpec.md) - 性能日志规范
- [HeatDecaySpec.md](./HeatDecaySpec.md) - 热衰减测试规范

### 错误与事件
- [ErrorSpec.md](./ErrorSpec.md) - 错误码规范
- [EventBus.md](./EventBus.md) - 事件类型规范

### 版本管理
- [ProtocolVersioning.md](./ProtocolVersioning.md) - 协议版本管理

---

## 🆘 故障排查

### 问题 1: 协议版本不兼容

**错误**: `协议版本不兼容: 1.0.0 vs 1.1.0`

**解决**: 检查 `protocol_version` 字段，确保前后端使用相同主版本号。

### 问题 2: 字段验证失败

**错误**: `缺少必须字段: frame_id`

**解决**: 参考对应规范文档，确保包含所有必须字段。

### 问题 3: JSON Schema 验证失败

**错误**: `JSON Schema 验证失败`

**解决**: 使用协议验证库自动检查，或参考规范文档的 JSON Schema。

---

## 📞 支持

- **文档**: [docs/protocol/](./)
- **代码**: [protocol/](../../protocol/)
- **问题反馈**: 提交 Issue 或联系团队

---

**最后更新**: 2025-12-02






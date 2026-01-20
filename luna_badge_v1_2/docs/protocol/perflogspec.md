# PerfLogSpec - 性能日志 JSONL 规范

**版本**: 1.0.0  
**最后更新**: 2025-12-02  
**用途**: 所有压测 / iPhone 前端真实数据的统一日志格式

---

## 📋 JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PerfLogSpec",
  "type": "object",
  "required": [
    "ts",
    "protocol_version",
    "event",
    "network",
    "infer"
  ],
  "properties": {
    "ts": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 时间戳（UTC），格式：YYYY-MM-DDTHH:mm:ss.sssZ"
    },
    "protocol_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "协议版本号"
    },
    "event": {
      "type": "string",
      "enum": [
        "frame_sent",
        "frame_received",
        "infer_start",
        "infer_end",
        "nav_start",
        "nav_end",
        "infer_result",
        "heartbeat",
        "heartbeat_ack",
        "ws_connect",
        "ws_disconnect",
        "error"
      ],
      "description": "事件类型（见 EventBus 规范）"
    },
    "frame_id": {
      "type": "integer",
      "minimum": 0,
      "description": "帧 ID（仅 infer_result 事件需要）"
    },
    "network": {
      "type": "object",
      "required": ["rtt_ms"],
      "properties": {
        "rtt_ms": {
          "type": "number",
          "minimum": 0,
          "description": "网络往返延迟（毫秒）"
        },
        "upload_ms": {
          "type": "number",
          "minimum": 0,
          "description": "上传延迟（毫秒）"
        },
        "download_ms": {
          "type": "number",
          "minimum": 0,
          "description": "下载延迟（毫秒）"
        }
      }
    },
    "infer": {
      "type": "object",
      "required": ["total_ms"],
      "properties": {
        "infer_ms": {
          "type": "number",
          "minimum": 0,
          "description": "YOLO 推理耗时（毫秒）"
        },
        "nav_ms": {
          "type": "number",
          "minimum": 0,
          "description": "导航决策耗时（毫秒）"
        },
        "total_ms": {
          "type": "number",
          "minimum": 0,
          "description": "总耗时（毫秒）"
        }
      }
    },
    "system": {
      "type": "object",
      "properties": {
        "cpu_pct": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "CPU 使用率（0-100）"
        },
        "mem_pct": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "内存使用率（0-100）"
        },
        "gpu_util": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "GPU 使用率（0-100，可选）"
        },
        "gpu_temp": {
          "type": "number",
          "description": "GPU 温度（摄氏度，可选）"
        }
      }
    },
    "extra": {
      "type": "object",
      "description": "额外信息（可选）",
      "properties": {
        "platform": {
          "type": "string",
          "enum": ["ios", "android", "web"]
        },
        "gps": {
          "type": "array",
          "items": {"type": "number"},
          "minItems": 2,
          "maxItems": 2,
          "description": "GPS 坐标 [lat, lon]"
        },
        "run_id": {
          "type": "string",
          "description": "运行 ID"
        }
      }
    }
  }
}
```

---

## ✅ 字段说明

### 必须字段（强校验）

| 字段 | 类型 | 约束 | 说明 | 示例 |
|------|------|------|------|------|
| `ts` | string | ISO 8601 | ISO 8601 时间戳（UTC） | `"2025-01-18T13:20:15.123Z"` |
| `protocol_version` | string | `"\\d+\\.\\d+\\.\\d+"` | 协议版本号 | `"1.0.0"` |
| `event` | string | 枚举值 | 事件类型（见 EventBus） | `"infer_result"` |
| `network.rtt_ms` | number | `>= 0` | 网络往返延迟（毫秒） | `42.3` |
| `infer.total_ms` | number | `>= 0` | 总推理耗时（毫秒） | `12.8` |

### 可选字段（弱校验）

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `frame_id` | integer | 帧 ID | `null` |
| `network.upload_ms` | number | 上传延迟 | `null` |
| `network.download_ms` | number | 下载延迟 | `null` |
| `infer.infer_ms` | number | YOLO 推理耗时 | `null` |
| `infer.nav_ms` | number | 导航决策耗时 | `null` |
| `system.cpu_pct` | number | CPU 使用率 | `null` |
| `system.mem_pct` | number | 内存使用率 | `null` |
| `system.gpu_util` | number | GPU 使用率 | `null` |
| `system.gpu_temp` | number | GPU 温度 | `null` |
| `extra` | object | 额外信息 | `null` |

---

## 📝 使用示例

### 示例 1: 推理结果日志

```json
{
  "ts": "2025-01-18T13:20:15.123Z",
  "protocol_version": "1.0.0",
  "event": "infer_result",
  "frame_id": 12345,
  "network": {
    "rtt_ms": 42.3,
    "upload_ms": 20.1,
    "download_ms": 22.2
  },
  "infer": {
    "infer_ms": 7.5,
    "nav_ms": 3.1,
    "total_ms": 12.8
  },
  "system": {
    "cpu_pct": 23.1,
    "mem_pct": 62.5
  },
  "extra": {
    "platform": "ios",
    "run_id": "run_20250118_132000"
  }
}
```

### 示例 2: 心跳日志

```json
{
  "ts": "2025-01-18T13:20:18.456Z",
  "protocol_version": "1.0.0",
  "event": "heartbeat_ack",
  "network": {
    "rtt_ms": 15.2
  },
  "infer": {
    "total_ms": 0.0
  },
  "extra": {
    "platform": "ios"
  }
}
```

### 示例 3: 连接事件日志

```json
{
  "ts": "2025-01-18T13:20:10.000Z",
  "protocol_version": "1.0.0",
  "event": "ws_connect",
  "network": {
    "rtt_ms": 0.0
  },
  "infer": {
    "total_ms": 0.0
  },
  "extra": {
    "platform": "ios"
  }
}
```

---

## 🔍 约束规则

### 必须字段（Must）

1. **ts**: 必须为有效的 ISO 8601 格式（UTC）
2. **protocol_version**: 必须符合版本号格式
3. **event**: 必须是 EventBus 规范中定义的事件类型
4. **network.rtt_ms**: 必须为非负数
5. **infer.total_ms**: 必须为非负数

### 可选字段（Optional）

- `frame_id`: 仅 `infer_result` 事件需要
- `system`: 系统资源信息可选
- `extra`: 额外信息可选

### 字段关系

- `infer.total_ms` 应该等于 `infer.infer_ms + infer.nav_ms`（允许 ±0.1ms 误差）
- `network.rtt_ms` 应该等于 `network.upload_ms + network.download_ms`（允许 ±0.1ms 误差）

---

## ⚠️ 异常情况说明

### 异常 1: 时间戳格式错误

**错误**: `ts 格式无效: 2025-01-18 13:20:15`

**处理**: 使用 ISO 8601 格式，例如 `"2025-01-18T13:20:15.123Z"`

### 异常 2: 事件类型无效

**错误**: `未知事件类型: unknown_event`

**处理**: 使用 EventBus 规范中定义的事件类型

---

## 🔄 跨版本兼容策略

### 1.0.0 → 1.1.0（向后兼容）

**变更**: 新增 `system.gpu_util` 和 `system.gpu_temp` 字段（可选）

**兼容性**: ✅ 完全兼容
- 1.0.0 工具链：忽略新字段，正常工作
- 1.1.0 工具链：支持新字段，向后兼容 1.0.0

---

## 📚 相关规范

- [EventBus.md](./EventBus.md) - 事件类型规范
- [InferSpec.md](./InferSpec.md) - 推理结果规范
- [HeatDecaySpec.md](./HeatDecaySpec.md) - 热衰减规范

---

**最后更新**: 2025-12-02
















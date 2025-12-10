# HeartbeatSpec - WebSocket 心跳规范

**版本**: 1.0.0  
**最后更新**: 2025-12-02  
**用途**: 前端和后端之间的心跳保活机制

---

## 📋 JSON Schema

### 前端心跳（type: "heartbeat"）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "HeartbeatSpec",
  "type": "object",
  "required": ["type", "protocol_version", "seq", "client_ts"],
  "properties": {
    "type": {
      "type": "string",
      "enum": ["heartbeat"],
      "description": "消息类型，固定为 'heartbeat'"
    },
    "protocol_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "协议版本号"
    },
    "seq": {
      "type": "integer",
      "minimum": 0,
      "description": "心跳序号，单调递增"
    },
    "client_ts": {
      "type": "number",
      "minimum": 0,
      "description": "客户端发送时间戳（毫秒）"
    }
  }
}
```

### 后端心跳确认（type: "heartbeat_ack"）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "HeartbeatAckSpec",
  "type": "object",
  "required": ["type", "protocol_version", "seq", "client_ts", "server_ts"],
  "properties": {
    "type": {
      "type": "string",
      "enum": ["heartbeat_ack"],
      "description": "消息类型，固定为 'heartbeat_ack'"
    },
    "protocol_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "seq": {
      "type": "integer",
      "minimum": 0,
      "description": "心跳序号（原样回显）"
    },
    "client_ts": {
      "type": "number",
      "minimum": 0,
      "description": "客户端时间戳（原样回显）"
    },
    "server_ts": {
      "type": "number",
      "minimum": 0,
      "description": "服务器收到时间戳（毫秒）"
    }
  }
}
```

---

## ✅ 字段说明

### 前端心跳（type: "heartbeat"）

| 字段 | 类型 | 约束 | 说明 | 示例 |
|------|------|------|------|------|
| `type` | string | `"heartbeat"` | 消息类型 | `"heartbeat"` |
| `protocol_version` | string | `"\\d+\\.\\d+\\.\\d+"` | 协议版本号 | `"1.0.0"` |
| `seq` | integer | `>= 0` | 心跳序号，单调递增 | `25` |
| `client_ts` | number | `>= 0` | 客户端发送时间戳 | `1737212345.123` |

### 后端心跳确认（type: "heartbeat_ack"）

| 字段 | 类型 | 约束 | 说明 | 示例 |
|------|------|------|------|------|
| `type` | string | `"heartbeat_ack"` | 消息类型 | `"heartbeat_ack"` |
| `protocol_version` | string | `"\\d+\\.\\d+\\.\\d+"` | 协议版本号 | `"1.0.0"` |
| `seq` | integer | `>= 0` | 心跳序号（原样回显） | `25` |
| `client_ts` | number | `>= 0` | 客户端时间戳（原样回显） | `1737212345.123` |
| `server_ts` | number | `>= 0` | 服务器收到时间戳 | `1737212345.124` |

---

## 📝 使用示例

### 示例 1: 前端发送心跳

```json
{
  "type": "heartbeat",
  "protocol_version": "1.0.0",
  "seq": 25,
  "client_ts": 1737212345.123
}
```

### 示例 2: 后端返回心跳确认

```json
{
  "type": "heartbeat_ack",
  "protocol_version": "1.0.0",
  "seq": 25,
  "client_ts": 1737212345.123,
  "server_ts": 1737212345.124
}
```

---

## 🔍 约束规则

### 必须字段（Must）

1. **type**: 必须为 `"heartbeat"` 或 `"heartbeat_ack"`
2. **protocol_version**: 必须符合版本号格式
3. **seq**: 必须为非负整数，前端发送时单调递增
4. **client_ts**: 必须为非负数，前端使用 `performance.now()` 获取
5. **server_ts**: 心跳确认中必须存在，且 `server_ts >= client_ts`

### 可选字段（Optional）

无

---

## ⚙️ 配置建议

### 心跳间隔

- **前端发送间隔**: 3-5 秒（推荐 3 秒）
- **超时检测**: 连续 3 次心跳无响应视为连接断开
- **重连策略**: 指数退避，最大延迟 10 秒

### RTT 计算

```javascript
// 前端计算 RTT
const rtt = performance.now() - heartbeat_ack.client_ts;
console.log(`心跳 RTT: ${rtt.toFixed(1)}ms`);
```

---

## ⚠️ 异常情况说明

### 异常 1: 心跳超时

**场景**: 连续 3 次心跳无响应

**处理**: 
- 前端：触发自动重连
- 记录事件：`ws_disconnect`（见 EventBus 规范）

### 异常 2: 心跳序号不连续

**场景**: 收到的心跳确认序号与发送的不一致

**处理**: 
- 记录警告日志
- 继续正常工作（不中断连接）

---

## 🔄 跨版本兼容策略

### 1.0.0 → 1.1.0（向后兼容）

**变更**: 新增 `heartbeat_ack.rtt_ms` 字段（可选，服务器计算的 RTT）

**兼容性**: ✅ 完全兼容
- 1.0.0 客户端：忽略新字段，正常工作
- 1.1.0 服务器：支持新字段，向后兼容 1.0.0

---

## 📚 相关规范

- [EventBus.md](./EventBus.md) - 事件类型规范（heartbeat, heartbeat_ack）
- [ErrorSpec.md](./ErrorSpec.md) - 错误码规范（WS-003: WS 意外断开）
- [ProtocolVersioning.md](./ProtocolVersioning.md) - 版本管理规范

---

**最后更新**: 2025-12-02





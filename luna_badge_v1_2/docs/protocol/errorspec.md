# ErrorSpec - 标准错误码规范

**版本**: 1.0.0  
**最后更新**: 2025-12-02  
**用途**: 统一前后端错误码，便于前端显示和日志分析

---

## 📋 JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ErrorSpec",
  "type": "object",
  "required": [
    "type",
    "protocol_version",
    "code",
    "message"
  ],
  "properties": {
    "type": {
      "type": "string",
      "enum": ["error"],
      "description": "消息类型，固定为 'error'"
    },
    "protocol_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "协议版本号"
    },
    "code": {
      "type": "string",
      "pattern": "^[A-Z]{3}-\\d{3}$",
      "description": "错误码，格式：XXX-###"
    },
    "message": {
      "type": "string",
      "minLength": 1,
      "description": "错误消息（人类可读）"
    },
    "detail": {
      "type": "string",
      "description": "错误详情（技术信息）"
    },
    "client_ts": {
      "type": "number",
      "minimum": 0,
      "description": "客户端时间戳（可选）"
    },
    "server_ts": {
      "type": "number",
      "minimum": 0,
      "description": "服务器时间戳（可选）"
    }
  }
}
```

---

## ✅ 字段说明

### 必须字段（强校验）

| 字段 | 类型 | 约束 | 说明 | 示例 |
|------|------|------|------|------|
| `type` | string | `"error"` | 消息类型 | `"error"` |
| `protocol_version` | string | `"\\d+\\.\\d+\\.\\d+"` | 协议版本号 | `"1.0.0"` |
| `code` | string | `"[A-Z]{3}-\\d{3}"` | 错误码 | `"NAV-002"` |
| `message` | string | 非空 | 错误消息（人类可读） | `"导航路径规划失败"` |

### 可选字段（弱校验）

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `detail` | string | 错误详情（技术信息） | `null` |
| `client_ts` | number | 客户端时间戳 | `null` |
| `server_ts` | number | 服务器时间戳 | `null` |

---

## 📋 错误码表

### 摄像头相关（CAM-###）

| Code | 描述 | 严重程度 | 处理建议 |
|------|------|----------|----------|
| `CAM-001` | 相机权限被拒绝 | 高 | 提示用户授权相机权限 |
| `CAM-002` | 无法获取相机数据 | 高 | 检查相机硬件连接 |
| `CAM-003` | 帧编码失败 | 中 | 降低图像质量或分辨率 |

### WebSocket 相关（WS-###）

| Code | 描述 | 严重程度 | 处理建议 |
|------|------|----------|----------|
| `WS-001` | WS 连接失败 | 高 | 自动重连 |
| `WS-002` | WS 发送数据失败 | 中 | 重试发送 |
| `WS-003` | WS 意外断开 | 高 | 自动重连 |

### 推理相关（INF-###）

| Code | 描述 | 严重程度 | 处理建议 |
|------|------|----------|----------|
| `INF-001` | YOLO 推理超时 | 中 | 降级模型或降低 FPS |
| `INF-002` | 推理结果为空 | 低 | 继续下一帧 |
| `INF-003` | 模型加载失败 | 高 | 检查模型文件 |

### 导航相关（NAV-###）

| Code | 描述 | 严重程度 | 处理建议 |
|------|------|----------|----------|
| `NAV-001` | 无法生成导航决策 | 中 | 使用默认安全策略 |
| `NAV-002` | 地图/路径规划失败 | 中 | 降级到简单导航 |
| `NAV-003` | 导航超时 | 低 | 跳过当前帧 |

### 系统相关（SYS-###）

| Code | 描述 | 严重程度 | 处理建议 |
|------|------|----------|----------|
| `SYS-001` | CPU/内存过载 | 高 | 降级模型、降低 FPS |
| `SYS-002` | GPU 过热 | 高 | 暂停推理、等待降温 |
| `SYS-003` | 磁盘空间不足 | 高 | 清理日志文件 |

### 协议相关（PROTO-###）

| Code | 描述 | 严重程度 | 处理建议 |
|------|------|----------|----------|
| `PROTO-001` | 协议版本不兼容 | 高 | 升级客户端或服务器 |
| `PROTO-002` | 消息格式错误 | 中 | 检查消息格式 |

---

## 📝 使用示例

### 示例 1: 摄像头权限错误

```json
{
  "type": "error",
  "protocol_version": "1.0.0",
  "code": "CAM-001",
  "message": "相机权限被拒绝",
  "detail": "getUserMedia failed: NotAllowedError",
  "client_ts": 1737212345.123
}
```

### 示例 2: 推理超时

```json
{
  "type": "error",
  "protocol_version": "1.0.0",
  "code": "INF-001",
  "message": "YOLO 推理超时",
  "detail": "frame_id=12345, timeout=5s",
  "server_ts": 1737212345.456
}
```

### 示例 3: 协议版本不兼容

```json
{
  "type": "error",
  "protocol_version": "1.0.0",
  "code": "PROTO-001",
  "message": "协议版本不兼容",
  "detail": "客户端版本 0.9.0 与服务器版本 1.0.0 不兼容",
  "server_ts": 1737212345.789
}
```

---

## 🔍 约束规则

### 必须字段（Must）

1. **type**: 必须为 `"error"`
2. **protocol_version**: 必须符合版本号格式
3. **code**: 必须符合 `XXX-###` 格式（3 个大写字母 + 3 个数字）
4. **message**: 必须为非空字符串

### 错误码格式

- **前缀**: 3 个大写字母，表示错误类别
  - `CAM`: 摄像头相关
  - `WS`: WebSocket 相关
  - `INF`: 推理相关
  - `NAV`: 导航相关
  - `SYS`: 系统相关
  - `PROTO`: 协议相关
- **编号**: 3 位数字，从 001 开始

---

## ⚠️ 异常情况说明

### 异常 1: 未知错误码

**场景**: 收到未定义的错误码

**处理**: 
- 前端：显示通用错误消息
- 记录日志：包含完整错误信息

### 异常 2: 错误码格式错误

**场景**: 错误码不符合 `XXX-###` 格式

**处理**: 
- 后端：拒绝该错误消息
- 返回 `PROTO-002`（消息格式错误）

---

## 🔄 跨版本兼容策略

### 1.0.0 → 1.1.0（向后兼容）

**变更**: 新增 `NAV-004`（路径优化失败）错误码

**兼容性**: ✅ 完全兼容
- 1.0.0 客户端：显示通用错误消息
- 1.1.0 客户端：显示具体错误消息

---

## 📚 相关规范

- [EventBus.md](./EventBus.md) - 事件类型规范（error 事件）
- [PerfLogSpec.md](./PerfLogSpec.md) - 性能日志规范
- [ProtocolVersioning.md](./ProtocolVersioning.md) - 版本管理规范

---

**最后更新**: 2025-12-02
















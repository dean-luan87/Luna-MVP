# FrameSpec - 前端到后端帧数据规范

**版本**: 1.0.0  
**最后更新**: 2025-12-02  
**用途**: 前端（iPhone/Android/Web）发送帧数据到后端

---

## 📋 JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "FrameSpec",
  "type": "object",
  "required": [
    "type",
    "protocol_version",
    "frame_id",
    "client_ts",
    "width",
    "height",
    "image_base64"
  ],
  "properties": {
    "type": {
      "type": "string",
      "enum": ["frame"],
      "description": "消息类型，固定为 'frame'"
    },
    "protocol_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "协议版本号，格式：MAJOR.MINOR.PATCH"
    },
    "frame_id": {
      "type": "integer",
      "minimum": 0,
      "description": "帧序号，单调递增，从 0 或 1 开始"
    },
    "client_ts": {
      "type": "number",
      "minimum": 0,
      "description": "客户端时间戳（毫秒），使用 performance.now() 或 Date.now()"
    },
    "width": {
      "type": "integer",
      "minimum": 1,
      "maximum": 7680,
      "description": "图像宽度（像素）"
    },
    "height": {
      "type": "integer",
      "minimum": 1,
      "maximum": 4320,
      "description": "图像高度（像素）"
    },
    "image_base64": {
      "type": "string",
      "minLength": 1,
      "description": "Base64 编码的 JPEG 图像，不含 'data:image/jpeg;base64,' 前缀"
    },
    "meta": {
      "type": "object",
      "description": "元数据（可选）",
      "properties": {
        "platform": {
          "type": "string",
          "enum": ["ios", "android", "web"],
          "description": "平台标识"
        },
        "user_agent": {
          "type": "string",
          "description": "浏览器 User-Agent"
        },
        "auto_mode": {
          "type": "boolean",
          "description": "是否连续导航模式"
        },
        "camera_facing": {
          "type": "string",
          "enum": ["rear", "front"],
          "description": "摄像头朝向"
        },
        "network": {
          "type": "string",
          "enum": ["wifi", "5g", "4g", "other"],
          "description": "网络类型"
        },
        "gps": {
          "type": "object",
          "description": "GPS 位置信息",
          "properties": {
            "lat": {
              "type": "number",
              "minimum": -90,
              "maximum": 90
            },
            "lon": {
              "type": "number",
              "minimum": -180,
              "maximum": 180
            },
            "accuracy": {
              "type": "number",
              "minimum": 0,
              "description": "精度（米）"
            }
          }
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
| `type` | string | `"frame"` | 消息类型，固定值 | `"frame"` |
| `protocol_version` | string | `"\\d+\\.\\d+\\.\\d+"` | 协议版本号 | `"1.0.0"` |
| `frame_id` | integer | `>= 0` | 帧序号，单调递增 | `12345` |
| `client_ts` | number | `>= 0` | 客户端时间戳（毫秒） | `1737212345.233` |
| `width` | integer | `1-7680` | 图像宽度（像素） | `1280` |
| `height` | integer | `1-4320` | 图像高度（像素） | `720` |
| `image_base64` | string | 非空 | Base64 编码的 JPEG 图像 | `"/9j/4AAQSkZJRg..."` |

### 可选字段（弱校验）

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `meta.platform` | string | 平台标识 | `null` |
| `meta.user_agent` | string | 浏览器 User-Agent | `null` |
| `meta.auto_mode` | boolean | 是否连续导航模式 | `false` |
| `meta.camera_facing` | string | 摄像头朝向 | `null` |
| `meta.network` | string | 网络类型 | `null` |
| `meta.gps` | object | GPS 位置信息 | `null` |

---

## 📝 使用示例

### 示例 1: 基础帧数据

```json
{
  "type": "frame",
  "protocol_version": "1.0.0",
  "frame_id": 12345,
  "client_ts": 1737212345.233,
  "width": 1280,
  "height": 720,
  "image_base64": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAoADwDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXp7fH1+f3/9oADAMBAAIRAxEAPwD3+iiigAooooAKKKKAP//Z"
}
```

### 示例 2: 完整帧数据（含元数据）

```json
{
  "type": "frame",
  "protocol_version": "1.0.0",
  "frame_id": 12345,
  "client_ts": 1737212345.233,
  "width": 1280,
  "height": 720,
  "image_base64": "/9j/4AAQSkZJRg...",
  "meta": {
    "platform": "ios",
    "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    "auto_mode": true,
    "camera_facing": "rear",
    "network": "wifi",
    "gps": {
      "lat": 31.23,
      "lon": 121.47,
      "accuracy": 12.3
    }
  }
}
```

---

## 🔍 约束规则

### 必须字段（Must）

1. **type**: 必须为 `"frame"`，其他值将被拒绝
2. **protocol_version**: 必须符合 `MAJOR.MINOR.PATCH` 格式
3. **frame_id**: 必须为非负整数，建议从 0 或 1 开始，单调递增
4. **client_ts**: 必须为非负数，建议使用 `performance.now()` 获取高精度时间戳
5. **width/height**: 必须在 1-7680（宽）和 1-4320（高）范围内
6. **image_base64**: 必须为非空字符串，且为有效的 Base64 编码

### 可选字段（Optional）

- `meta` 对象及其所有子字段均为可选
- 如果提供 `meta.gps`，则 `lat` 和 `lon` 必须在有效范围内
- `meta.network` 如果提供，必须是枚举值之一

---

## ⚠️ 异常情况说明

### 异常 1: 缺少必须字段

**错误**: `缺少必须字段: frame_id`

**处理**: 后端应返回 `ErrorSpec`，错误码 `WS-002`（WS 发送数据失败）

### 异常 2: 图像格式无效

**错误**: `image_base64 格式无效`

**处理**: 后端应返回 `ErrorSpec`，错误码 `CAM-003`（帧编码失败）

### 异常 3: 协议版本不兼容

**错误**: `协议版本不兼容: 0.9.0 vs 1.0.0`

**处理**: 后端应返回 `ErrorSpec`，错误码 `PROTO-001`（协议版本不兼容）

---

## 🔄 跨版本兼容策略

### 1.0.0 → 1.1.0（向后兼容）

**变更**: 新增 `meta.battery_level` 字段（可选）

**兼容性**: ✅ 完全兼容
- 1.0.0 客户端：忽略新字段，正常工作
- 1.1.0 服务器：支持新字段，向后兼容 1.0.0

### 1.x.x → 2.0.0（不兼容）

**变更**: 移除 `image_base64`，改为 `image_url`

**兼容性**: ❌ 不兼容
- 需要客户端和服务端同时升级
- 提供迁移工具和文档

---

## 📚 相关规范

- [InferSpec.md](./InferSpec.md) - 后端返回的推理结果规范
- [ErrorSpec.md](./ErrorSpec.md) - 错误码规范
- [ProtocolVersioning.md](./ProtocolVersioning.md) - 版本管理规范

---

**最后更新**: 2025-12-02

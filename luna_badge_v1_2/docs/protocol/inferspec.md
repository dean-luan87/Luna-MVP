# InferSpec - 后端到前端推理结果规范

**版本**: 1.0.0  
**最后更新**: 2025-12-02  
**用途**: 后端返回推理结果给前端

---

## 📋 JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "InferSpec",
  "type": "object",
  "required": [
    "type",
    "protocol_version",
    "frame_id",
    "client_ts",
    "server_ts",
    "infer_ts",
    "nav_ts",
    "infer_ms",
    "nav_ms",
    "total_ms"
  ],
  "properties": {
    "type": {
      "type": "string",
      "enum": ["infer_result"],
      "description": "消息类型，固定为 'infer_result'"
    },
    "protocol_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "协议版本号"
    },
    "frame_id": {
      "type": "integer",
      "minimum": 0,
      "description": "对应的帧 ID（原样回显）"
    },
    "client_ts": {
      "type": "number",
      "minimum": 0,
      "description": "客户端时间戳（原样回显）"
    },
    "server_ts": {
      "type": "number",
      "minimum": 0,
      "description": "服务器收到帧的时间戳（毫秒）"
    },
    "infer_ts": {
      "type": "number",
      "minimum": 0,
      "description": "YOLO 推理结束时间戳（毫秒）"
    },
    "nav_ts": {
      "type": "number",
      "minimum": 0,
      "description": "导航决策结束时间戳（毫秒）"
    },
    "infer_ms": {
      "type": "number",
      "minimum": 0,
      "description": "YOLO 推理耗时（毫秒）"
    },
    "nav_ms": {
      "type": "number",
      "minimum": 0,
      "description": "导航逻辑耗时（毫秒）"
    },
    "total_ms": {
      "type": "number",
      "minimum": 0,
      "description": "总耗时（infer_ms + nav_ms，不含网络）"
    },
    "objects": {
      "type": "array",
      "description": "检测到的对象列表",
      "items": {
        "type": "object",
        "required": ["cls", "conf", "bbox"],
        "properties": {
          "cls": {
            "type": "string",
            "description": "类别名称"
          },
          "conf": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "置信度（0-1）"
          },
          "bbox": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 4,
            "maxItems": 4,
            "description": "边界框 [x1, y1, x2, y2]"
          }
        }
      }
    },
    "nav": {
      "type": "object",
      "description": "导航决策信息",
      "properties": {
        "decision": {
          "type": "string",
          "enum": ["turn_left", "turn_right", "straight", "stop"],
          "description": "导航决策"
        },
        "danger_level": {
          "type": "integer",
          "minimum": 0,
          "maximum": 3,
          "description": "危险等级：0=安全, 1=低, 2=中, 3=高"
        },
        "text": {
          "type": "string",
          "description": "导航提示文本"
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
| `type` | string | `"infer_result"` | 消息类型 | `"infer_result"` |
| `protocol_version` | string | `"\\d+\\.\\d+\\.\\d+"` | 协议版本号 | `"1.0.0"` |
| `frame_id` | integer | `>= 0` | 对应的帧 ID | `12345` |
| `client_ts` | number | `>= 0` | 客户端时间戳（原样回显） | `1737212345.233` |
| `server_ts` | number | `>= 0` | 服务器收到时间戳 | `1737212345.255` |
| `infer_ts` | number | `>= 0` | YOLO 推理结束时间戳 | `1737212345.260` |
| `nav_ts` | number | `>= 0` | 导航决策结束时间戳 | `1737212345.263` |
| `infer_ms` | number | `>= 0` | YOLO 推理耗时（毫秒） | `7.5` |
| `nav_ms` | number | `>= 0` | 导航逻辑耗时（毫秒） | `3.1` |
| `total_ms` | number | `>= 0` | 总耗时（`infer_ms + nav_ms`） | `12.8` |

### 可选字段（弱校验）

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `objects` | array | 检测到的对象列表 | `[]` |
| `nav` | object | 导航决策信息 | `null` |

---

## 📝 使用示例

### 示例 1: 完整推理结果

```json
{
  "type": "infer_result",
  "protocol_version": "1.0.0",
  "frame_id": 12345,
  "client_ts": 1737212345.233,
  "server_ts": 1737212345.255,
  "infer_ts": 1737212345.260,
  "nav_ts": 1737212345.263,
  "infer_ms": 7.5,
  "nav_ms": 3.1,
  "total_ms": 12.8,
  "objects": [
    {
      "cls": "person",
      "conf": 0.71,
      "bbox": [100, 200, 300, 600]
    },
    {
      "cls": "chair",
      "conf": 0.85,
      "bbox": [400, 300, 500, 550]
    }
  ],
  "nav": {
    "decision": "turn_left",
    "danger_level": 2,
    "text": "请稍微向右侧行走"
  }
}
```

### 示例 2: 仅推理结果（无导航）

```json
{
  "type": "infer_result",
  "protocol_version": "1.0.0",
  "frame_id": 12345,
  "client_ts": 1737212345.233,
  "server_ts": 1737212345.255,
  "infer_ts": 1737212345.260,
  "nav_ts": 1737212345.260,
  "infer_ms": 7.5,
  "nav_ms": 0.0,
  "total_ms": 7.5,
  "objects": [
    {
      "cls": "person",
      "conf": 0.71,
      "bbox": [100, 200, 300, 600]
    }
  ]
}
```

---

## 🔍 约束规则

### 必须字段（Must）

1. **type**: 必须为 `"infer_result"`
2. **protocol_version**: 必须符合版本号格式
3. **frame_id**: 必须与原帧数据中的 `frame_id` 一致
4. **client_ts**: 必须原样回显前端发送的 `client_ts`
5. **时间戳关系**: `server_ts <= infer_ts <= nav_ts`
6. **耗时关系**: `total_ms = infer_ms + nav_ms`（允许 ±0.1ms 误差）
7. **耗时非负**: 所有 `*_ms` 字段必须 >= 0

### 可选字段（Optional）

- `objects`: 可以为空数组 `[]`
- `nav`: 如果无导航逻辑，可以省略或设置 `nav_ms = 0`

---

## ⚠️ 异常情况说明

### 异常 1: 推理超时

**场景**: YOLO 推理超过 5 秒

**处理**: 返回 `ErrorSpec`，错误码 `INF-001`（YOLO 推理超时）

### 异常 2: 推理结果为空

**场景**: 未检测到任何对象

**处理**: 正常返回，`objects` 为空数组 `[]`

### 异常 3: 导航决策失败

**场景**: 无法生成导航决策

**处理**: 返回 `ErrorSpec`，错误码 `NAV-001`（无法生成导航决策）

---

## 🔄 跨版本兼容策略

### 1.0.0 → 1.1.0（向后兼容）

**变更**: 新增 `objects[].track_id` 字段（可选，用于对象追踪）

**兼容性**: ✅ 完全兼容
- 1.0.0 客户端：忽略新字段，正常工作
- 1.1.0 服务器：支持新字段，向后兼容 1.0.0

### 1.x.x → 2.0.0（不兼容）

**变更**: 移除 `infer_ms` 和 `nav_ms`，改为 `timings` 对象

**兼容性**: ❌ 不兼容
- 需要客户端和服务端同时升级
- 提供迁移工具

---

## 📚 相关规范

- [FrameSpec.md](./FrameSpec.md) - 前端发送的帧数据规范
- [PerfLogSpec.md](./PerfLogSpec.md) - 性能日志规范
- [ErrorSpec.md](./ErrorSpec.md) - 错误码规范

---

**最后更新**: 2025-12-02

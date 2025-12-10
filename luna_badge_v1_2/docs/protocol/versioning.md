# 协议版本管理

**版本**: 1.0.0  
**用途**: 支持协议版本升级和兼容性管理

---

## 📋 版本号规范

### 格式

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: 不兼容的协议变更
- **MINOR**: 向后兼容的新功能
- **PATCH**: 向后兼容的 bug 修复

### 当前版本

- **协议版本**: 1.0.0
- **发布日期**: 2025-12-02

---

## 📋 版本标识

### 在消息中包含版本号

所有规范消息都应包含 `protocol_version` 字段：

```json
{
  "type": "frame",
  "protocol_version": "1.0.0",
  "frame_id": 12345,
  // ... 其他字段
}
```

### 版本协商

#### 前端请求

```javascript
const handshake = {
  type: "handshake",
  protocol_version: "1.0.0",
  client_capabilities: ["frame", "heartbeat"]
};
ws.send(JSON.stringify(handshake));
```

#### 后端响应

```json
{
  "type": "handshake_ack",
  "protocol_version": "1.0.0",
  "server_capabilities": ["frame", "heartbeat", "nav"],
  "supported_versions": ["1.0.0"]
}
```

---

## 🔄 版本兼容性

### 兼容性矩阵

| 前端版本 | 后端版本 | 兼容性 |
|----------|----------|--------|
| 1.0.0 | 1.0.0 | ✅ 完全兼容 |
| 1.0.0 | 1.1.0 | ✅ 兼容（后端支持新功能） |
| 1.1.0 | 1.0.0 | ⚠️ 部分兼容（前端新功能不可用） |
| 2.0.0 | 1.0.0 | ❌ 不兼容 |

### 兼容性检查

```python
def check_compatibility(client_version: str, server_version: str) -> bool:
    """检查版本兼容性"""
    client_major = int(client_version.split(".")[0])
    server_major = int(server_version.split(".")[0])
    
    # 主版本号必须相同
    if client_major != server_major:
        return False
    
    # 次版本号：客户端可以 <= 服务器
    client_minor = int(client_version.split(".")[1])
    server_minor = int(server_version.split(".")[1])
    
    return client_minor <= server_minor
```

---

## 📝 版本升级指南

### 1.0.0 → 1.1.0（示例）

**变更内容**:
- 新增 `meta.gps` 字段（可选）
- 新增 `nav.danger_level` 字段（可选）

**兼容性**: ✅ 向后兼容

**升级步骤**:
1. 后端支持新字段（可选）
2. 前端逐步采用新字段
3. 工具链更新以支持新字段

### 1.x.x → 2.0.0（示例）

**变更内容**:
- 移除 `infer_ms` 字段，改为 `infer.duration_ms`
- 重构 `objects` 结构

**兼容性**: ❌ 不兼容

**升级步骤**:
1. 发布迁移指南
2. 提供兼容层（同时支持新旧格式）
3. 逐步迁移所有客户端
4. 移除兼容层

---

## 🔍 版本检测

### 前端检测

```javascript
function detectProtocolVersion(serverResponse) {
  const version = serverResponse.protocol_version || "1.0.0";
  console.log(`服务器协议版本: ${version}`);
  
  // 检查兼容性
  if (!isCompatible("1.0.0", version)) {
    alert(`协议版本不兼容: 客户端 1.0.0 vs 服务器 ${version}`);
  }
}
```

### 后端检测

```python
def validate_protocol_version(data: dict) -> bool:
    client_version = data.get("protocol_version", "1.0.0")
    server_version = "1.0.0"
    
    if not check_compatibility(client_version, server_version):
        raise ValueError(f"协议版本不兼容: {client_version} vs {server_version}")
    
    return True
```

---

## 📚 版本历史

### 1.0.0 (2025-12-02)

- 初始版本
- 定义所有核心规范（FrameSpec, InferSpec, HeartbeatSpec, PerfLogSpec, HeatDecaySpec, EventBusSpec, ErrorSpec）

---

## 📚 相关规范

- [FrameSpec](./framespec.md) - 帧数据规范
- [InferSpec](./inferspec.md) - 推理结果规范
- [HeartbeatSpec](./heartbeatspec.md) - 心跳规范







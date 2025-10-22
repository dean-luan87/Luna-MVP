# Luna Badge Cloud Backend Design 云端后台系统设计

**版本**: v2.0  
**发布日期**: 2025-01-22  
**文档类型**: 系统设计  

---

## 📋 目录

1. [后台系统总体结构说明](#后台系统总体结构说明)
2. [功能模块表格](#功能模块表格)
3. [数据库表结构](#数据库表结构)
4. [数据流结构图](#数据流结构图)
5. [接口定义示例](#接口定义示例)
6. [安全机制](#安全机制)
7. [OTA 更新逻辑](#ota-更新逻辑)
8. [未来扩展规划](#未来扩展规划)
9. [附录：部署方式与运行示例](#附录部署方式与运行示例)

---

## 🏗️ 后台系统总体结构说明

### 技术栈选择
- **后端框架**: FastAPI (Python 3.10+)
- **消息队列**: MQTT (Eclipse Mosquitto)
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **缓存**: Redis
- **认证**: JWT + OAuth2
- **文档**: OpenAPI/Swagger
- **部署**: Docker + Docker Compose

### 系统架构
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   设备端        │    │   云端后台      │    │   管理端        │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ Luna Badge  │ │◄──►│ │ FastAPI     │ │◄──►│ │ Web管理界面 │ │
│ │ 硬件设备    │ │    │ │ 后台服务    │ │    │ │ 手机App     │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ MQTT客户端  │ │◄──►│ │ MQTT Broker │ │    │ │ REST API    │ │
│ │ 数据上报    │ │    │ │ 消息队列    │ │    │ │ 接口调用    │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 核心组件
- **API Gateway**: 统一入口，路由分发，认证授权
- **Device Manager**: 设备管理，注册认证，状态监控
- **Data Processor**: 数据处理，日志分析，告警触发
- **Config Manager**: 配置管理，参数同步，版本控制
- **Update Manager**: OTA更新，版本管理，回滚机制
- **Log Manager**: 日志收集，存储分析，查询检索

---

## 📊 功能模块表格

### 日志中心模块

| 功能 | 描述 | 技术实现 | 优先级 |
|------|------|----------|--------|
| 日志收集 | 设备日志实时收集 | MQTT + WebSocket | 高 |
| 日志存储 | 结构化日志存储 | SQLite/PostgreSQL | 高 |
| 日志查询 | 多维度日志查询 | REST API + 索引 | 高 |
| 日志分析 | 日志数据分析和统计 | Python + Pandas | 中 |
| 告警触发 | 基于日志的告警机制 | 规则引擎 | 中 |
| 日志导出 | 日志数据导出功能 | CSV/JSON导出 | 低 |

### 参数中心模块

| 功能 | 描述 | 技术实现 | 优先级 |
|------|------|----------|--------|
| 参数配置 | 设备参数在线配置 | REST API | 高 |
| 参数同步 | 参数变更实时同步 | MQTT推送 | 高 |
| 版本管理 | 参数版本控制 | Git-like版本管理 | 中 |
| 批量配置 | 多设备批量参数配置 | 批量操作API | 中 |
| 配置模板 | 参数配置模板管理 | 模板引擎 | 低 |
| 配置验证 | 参数有效性验证 | 验证规则引擎 | 中 |

### 版本控制模块

| 功能 | 描述 | 技术实现 | 优先级 |
|------|------|----------|--------|
| 版本管理 | 软件版本管理 | Git + 版本标签 | 高 |
| OTA更新 | 在线升级功能 | 增量更新 | 高 |
| 回滚机制 | 版本回滚功能 | 版本切换 | 中 |
| 灰度发布 | 灰度发布机制 | 分批次发布 | 中 |
| 更新通知 | 更新通知推送 | MQTT + 推送服务 | 低 |
| 更新统计 | 更新成功率统计 | 数据分析 | 低 |

### SDK管理模块

| 功能 | 描述 | 技术实现 | 优先级 |
|------|------|----------|--------|
| SDK发布 | 模块SDK发布管理 | 包管理器 | 高 |
| 依赖管理 | SDK依赖关系管理 | 依赖解析器 | 中 |
| 版本兼容 | 版本兼容性检查 | 兼容性矩阵 | 中 |
| SDK文档 | SDK文档自动生成 | 文档生成器 | 低 |
| 示例代码 | SDK使用示例 | 代码模板 | 低 |
| 测试框架 | SDK测试框架 | 单元测试 | 中 |

### 模块更新模块

| 功能 | 描述 | 技术实现 | 优先级 |
|------|------|----------|--------|
| 热更新 | 模块热更新功能 | 动态加载 | 高 |
| 依赖检查 | 模块依赖检查 | 依赖图分析 | 中 |
| 更新策略 | 更新策略配置 | 策略引擎 | 中 |
| 回滚支持 | 模块更新回滚 | 版本快照 | 中 |
| 更新日志 | 更新日志记录 | 变更日志 | 低 |
| 性能监控 | 更新性能监控 | 性能指标 | 低 |

### 错误码中心模块

| 功能 | 描述 | 技术实现 | 优先级 |
|------|------|----------|--------|
| 错误码定义 | 标准化错误码定义 | 错误码数据库 | 高 |
| 错误查询 | 错误码查询接口 | REST API | 高 |
| 处理指南 | 错误处理指南 | 文档系统 | 中 |
| 统计分析 | 错误统计分析 | 数据分析 | 中 |
| 自动修复 | 错误自动修复建议 | 规则引擎 | 低 |
| 国际化 | 错误码国际化支持 | 多语言系统 | 低 |

---

## 🗄️ 数据库表结构

### Device 设备表
```sql
CREATE TABLE devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id VARCHAR(64) UNIQUE NOT NULL,
    device_name VARCHAR(128) NOT NULL,
    device_type VARCHAR(32) NOT NULL,
    hardware_version VARCHAR(16),
    software_version VARCHAR(16),
    mac_address VARCHAR(17),
    ip_address VARCHAR(15),
    status VARCHAR(16) DEFAULT 'offline',
    last_heartbeat TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    config_version VARCHAR(16),
    location_info JSON,
    device_info JSON
);
```

### Module 模块表
```sql
CREATE TABLE modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_name VARCHAR(64) UNIQUE NOT NULL,
    module_type VARCHAR(32) NOT NULL,
    module_version VARCHAR(16) NOT NULL,
    description TEXT,
    dependencies JSON,
    config_schema JSON,
    api_endpoints JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    download_url VARCHAR(256),
    checksum VARCHAR(64)
);
```

### Version 版本表
```sql
CREATE TABLE versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_number VARCHAR(16) UNIQUE NOT NULL,
    version_type VARCHAR(16) NOT NULL, -- 'stable', 'beta', 'alpha'
    release_notes TEXT,
    download_url VARCHAR(256),
    file_size INTEGER,
    checksum VARCHAR(64),
    is_force_update BOOLEAN DEFAULT FALSE,
    min_compatible_version VARCHAR(16),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    released_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

### ErrorLog 错误日志表
```sql
CREATE TABLE error_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id VARCHAR(64) NOT NULL,
    error_code VARCHAR(16) NOT NULL,
    error_level VARCHAR(16) NOT NULL, -- 'critical', 'error', 'warning', 'info'
    error_message TEXT NOT NULL,
    error_details JSON,
    module_name VARCHAR(64),
    stack_trace TEXT,
    occurred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    resolution TEXT,
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);
```

### Config 配置表
```sql
CREATE TABLE configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id VARCHAR(64),
    module_name VARCHAR(64),
    config_key VARCHAR(128) NOT NULL,
    config_value TEXT NOT NULL,
    config_type VARCHAR(16) DEFAULT 'string',
    is_encrypted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version VARCHAR(16) DEFAULT '1.0',
    FOREIGN KEY (device_id) REFERENCES devices(device_id),
    FOREIGN KEY (module_name) REFERENCES modules(module_name)
);
```

### User 用户表
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(128) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(16) DEFAULT 'user', -- 'admin', 'user', 'guest'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    profile_info JSON
);
```

---

## 🔄 数据流结构图

### 设备 ↔ 云 ↔ 手机端数据流

```
┌─────────────────────────────────────────────────────────────────┐
│                        数据流向图                                │
└─────────────────────────────────────────────────────────────────┘

设备端 ──────────────────────── 云端后台 ──────────────────────── 管理端
  │                                │                                │
  │ 1. 设备注册                    │                                │
  ├────────────────────────────────►│                                │
  │                                │                                │
  │ 2. 心跳数据                    │                                │
  ├────────────────────────────────►│                                │
  │                                │                                │
  │ 3. 日志数据                    │                                │
  ├────────────────────────────────►│                                │
  │                                │                                │
  │ 4. 状态数据                    │                                │
  ├────────────────────────────────►│                                │
  │                                │                                │
  │ 5. 配置推送                    │                                │
  │◄────────────────────────────────┤                                │
  │                                │                                │
  │ 6. 命令下发                    │                                │
  │◄────────────────────────────────┤                                │
  │                                │                                │
  │                                │ 7. 设备列表查询                │
  │                                │◄────────────────────────────────┤
  │                                │                                │
  │                                │ 8. 配置修改                    │
  │                                │◄────────────────────────────────┤
  │                                │                                │
  │                                │ 9. 日志查询                    │
  │                                │◄────────────────────────────────┤
  │                                │                                │
  │                                │ 10. 状态监控                   │
  │                                │◄────────────────────────────────┤
```

### 数据流说明
- **设备注册**: 设备首次连接时进行注册认证
- **心跳数据**: 定期发送设备状态和健康信息
- **日志数据**: 实时上报设备运行日志
- **状态数据**: 设备运行状态和性能数据
- **配置推送**: 云端向设备推送配置更新
- **命令下发**: 云端向设备发送控制命令
- **管理查询**: 管理端查询设备信息和状态
- **配置管理**: 管理端修改设备配置
- **日志查询**: 管理端查询设备日志
- **状态监控**: 管理端监控设备状态

---

## 🔌 接口定义示例

### REST API 接口

#### 设备管理接口
```python
# 设备注册
POST /api/v1/devices/register
{
    "device_id": "luna_badge_001",
    "device_name": "Luna Badge 001",
    "hardware_version": "v1.0",
    "mac_address": "00:11:22:33:44:55"
}

# 设备列表查询
GET /api/v1/devices?page=1&limit=10&status=online

# 设备详情查询
GET /api/v1/devices/{device_id}

# 设备配置更新
PUT /api/v1/devices/{device_id}/config
{
    "config_key": "detection_interval",
    "config_value": "5",
    "config_type": "integer"
}
```

#### 日志管理接口
```python
# 日志查询
GET /api/v1/logs?device_id={device_id}&level=error&start_time=2025-01-01&end_time=2025-01-31

# 日志统计
GET /api/v1/logs/statistics?device_id={device_id}&period=7d

# 日志导出
GET /api/v1/logs/export?device_id={device_id}&format=csv
```

#### 版本管理接口
```python
# 版本列表
GET /api/v1/versions?type=stable

# 检查更新
GET /api/v1/versions/check?current_version=v1.0.0

# 版本下载
GET /api/v1/versions/{version_id}/download
```

### MQTT Topic 示例

#### 设备上报主题
```python
# 设备心跳
luna/device/{device_id}/heartbeat
{
    "timestamp": "2025-01-22T10:30:00Z",
    "status": "online",
    "cpu_usage": 45.2,
    "memory_usage": 67.8,
    "temperature": 42.5
}

# 设备日志
luna/device/{device_id}/logs
{
    "timestamp": "2025-01-22T10:30:00Z",
    "level": "info",
    "module": "yolo",
    "message": "Detection completed",
    "details": {"objects_detected": 3}
}

# 设备状态
luna/device/{device_id}/status
{
    "timestamp": "2025-01-22T10:30:00Z",
    "modules": {
        "yolo": "running",
        "whisper": "running",
        "tts": "idle"
    },
    "performance": {
        "fps": 15.2,
        "latency": 120
    }
}
```

#### 云端下发主题
```python
# 配置更新
luna/device/{device_id}/config/update
{
    "config_key": "detection_interval",
    "config_value": "5",
    "timestamp": "2025-01-22T10:30:00Z"
}

# 命令下发
luna/device/{device_id}/command
{
    "command": "restart_module",
    "module": "yolo",
    "timestamp": "2025-01-22T10:30:00Z"
}

# OTA更新
luna/device/{device_id}/update
{
    "version": "v1.1.0",
    "download_url": "https://api.luna.com/v1/versions/v1.1.0/download",
    "checksum": "sha256:abc123...",
    "force_update": false
}
```

---

## 🔒 安全机制

### JWT 认证机制
```python
# JWT Token 结构
{
    "header": {
        "alg": "HS256",
        "typ": "JWT"
    },
    "payload": {
        "device_id": "luna_badge_001",
        "user_id": 123,
        "role": "device",
        "exp": 1640995200,  # 过期时间
        "iat": 1640908800   # 签发时间
    },
    "signature": "HMACSHA256(base64UrlEncode(header) + '.' + base64UrlEncode(payload), secret)"
}
```

### 签名校验机制
```python
# 请求签名生成
def generate_signature(method, path, body, timestamp, secret_key):
    message = f"{method}{path}{body}{timestamp}"
    signature = hmac.new(
        secret_key.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature

# 请求头示例
headers = {
    "Authorization": "Bearer {jwt_token}",
    "X-Timestamp": "1640908800",
    "X-Signature": "sha256:abc123...",
    "Content-Type": "application/json"
}
```

### 防篡改机制
- **数据完整性校验**: 使用HMAC-SHA256确保数据完整性
- **时间戳验证**: 防止重放攻击，时间窗口5分钟
- **设备指纹**: 基于硬件特征生成设备指纹
- **加密传输**: 所有敏感数据使用TLS 1.3加密传输

### 权限控制
```python
# 权限定义
PERMISSIONS = {
    "admin": ["read", "write", "delete", "manage"],
    "user": ["read", "write"],
    "device": ["read", "write_own_data"],
    "guest": ["read"]
}

# 权限检查中间件
@app.middleware("http")
async def check_permissions(request: Request, call_next):
    # 权限检查逻辑
    pass
```

---

## 🔄 OTA 更新逻辑

### 更新流程
```python
# 1. 检查更新
def check_update(current_version):
    latest_version = get_latest_version()
    if compare_versions(latest_version, current_version) > 0:
        return {
            "has_update": True,
            "latest_version": latest_version,
            "update_info": get_update_info(latest_version)
        }
    return {"has_update": False}

# 2. 下载更新
def download_update(version, device_id):
    download_url = generate_download_url(version, device_id)
    return {
        "download_url": download_url,
        "file_size": get_file_size(version),
        "checksum": get_checksum(version)
    }

# 3. 安装更新
def install_update(update_file, checksum):
    if verify_checksum(update_file, checksum):
        backup_current_version()
        install_new_version(update_file)
        return {"status": "success"}
    else:
        return {"status": "failed", "error": "checksum_mismatch"}

# 4. 回滚机制
def rollback_update():
    if backup_exists():
        restore_backup()
        return {"status": "rollback_success"}
    return {"status": "rollback_failed"}
```

### 更新策略
- **强制更新**: 安全漏洞修复，必须立即更新
- **可选更新**: 功能增强，用户可选择是否更新
- **灰度发布**: 分批次发布，降低风险
- **回滚支持**: 更新失败时自动回滚到稳定版本

---

## 🚀 未来扩展规划

### Pro 阶段 (2025-06-30)
- **AI模型优化**: 模型压缩、量化、边缘计算优化
- **多模态交互**: 视觉、语音、触觉多模态融合
- **智能决策**: 基于AI的智能决策系统
- **高级分析**: 深度数据分析和预测功能

### Max 阶段 (2025-12-31)
- **大规模部署**: 支持数万台设备同时在线
- **企业级安全**: 企业级安全认证和合规
- **全球部署**: 多地域部署和CDN加速
- **商业化功能**: 付费功能、订阅服务、API收费

### 技术演进路线
- **微服务架构**: 从单体应用演进为微服务架构
- **容器化部署**: 全面容器化部署和编排
- **云原生**: 云原生架构和Serverless函数
- **边缘计算**: 边缘计算节点和边缘AI推理

---

## 📋 附录：部署方式与运行示例

### Docker 部署
```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/luna
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
      - mqtt

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=luna
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data

  mqtt:
    image: eclipse-mosquitto:2.0
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf

volumes:
  postgres_data:
  redis_data:
```

### 运行示例
```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f api

# 访问API文档
curl http://localhost:8000/docs

# 测试设备注册
curl -X POST http://localhost:8000/api/v1/devices/register \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "luna_badge_001",
    "device_name": "Luna Badge 001",
    "hardware_version": "v1.0",
    "mac_address": "00:11:22:33:44:55"
  }'
```

### 监控和运维
- **健康检查**: `/health` 端点监控服务状态
- **性能监控**: Prometheus + Grafana 监控系统性能
- **日志聚合**: ELK Stack 日志收集和分析
- **告警通知**: AlertManager 告警通知机制

---

**文档结束**

*Luna Badge Cloud Backend v2.0 - 让云端更智能，让管理更简单*

# Luna Badge 后端开发规范 (v1.2.0)

**版本**: 1.2.0  
**更新日期**: 2025-11-19  
**适用范围**: Luna Backend 所有模块

---

## 📋 目录

1. [架构原则](#1-架构原则)
2. [文件职责说明](#2-文件职责说明)
3. [统一日志格式](#3-统一日志格式)
4. [API返回格式](#4-api返回格式)
5. [错误码使用规范](#5-错误码使用规范)
6. [代码迁移指南](#6-代码迁移指南)

---

## 1. 架构原则

### 1.1 单一职责原则

每个文件只负责一个功能域，不允许跨域写逻辑。

**✅ 正确示例**:
```python
# services/navigation/planner.py - 只处理路线规划
def plan_route(start, end):
    # 只包含路径规划逻辑
    pass
```

**❌ 错误示例**:
```python
# 不要在 planner.py 中写 TTS 逻辑
def plan_route(start, end):
    # 路径规划
    ...
    # ❌ 不要在这里调用 TTS
    tts_manager.speak("路径规划完成")
```

### 1.2 路由层禁止业务逻辑

路由层 (`routes/`) 只负责：
- 参数解析和验证
- 调用 service 层方法
- 返回标准响应格式

**✅ 正确示例**:
```python
# routes/navigation_routes.py
@bp.route('/api/navigation/start', methods=['POST'])
def start_navigation():
    data = request.get_json()
    destination = data.get('destination')
    
    if not destination:
        return api_error(9001, {"field": "destination"})
    
    try:
        result = navigation_service.start(destination)
        return api_success(result)
    except NavigationException as e:
        return api_exception(e, e.error_code)
```

**❌ 错误示例**:
```python
# ❌ 不要在路由层写业务逻辑
@bp.route('/api/navigation/start', methods=['POST'])
def start_navigation():
    # ❌ 不要在这里写路径规划算法
    path = calculate_path(...)
    # ❌ 不要在这里调用模型
    yolo_result = yolo.detect(...)
```

### 1.3 业务逻辑统一放在 services 层

所有业务逻辑、算法、模型调用都在 `services/` 目录下。

### 1.4 工程日志必须可溯源

使用统一的日志格式，详见 [统一日志格式](#3-统一日志格式)。

### 1.5 错误码必须能定位到模块

使用错误码体系，详见 [错误码使用规范](#5-错误码使用规范)。

### 1.6 模块化设计

视觉、导航、TTS 等模块必须独立，便于后续扩展：
- 医院流程
- 地铁结构
- 商场结构
- 任务链
- 场景理解
- 家庭组记忆

---

## 2. 文件职责说明

### 2.1 app.py

**职责**:
- 加载配置
- 初始化 services
- 注册 routes
- 启动 HTTPS/HTTP 服务器

**不包含**:
- 业务逻辑
- 路由处理
- 模型初始化

### 2.2 routes/

**职责**:
- 定义 API 端点
- 参数解析和验证
- 调用 service 层
- 返回标准响应

**不包含**:
- 业务逻辑
- 算法实现
- 模型调用

### 2.3 services/

**职责**:
- 所有业务逻辑
- 算法实现
- 模型调用
- 数据处理

**结构**:
```
services/
├── tts/              # TTS 服务
├── vision/           # 视觉服务
│   └── detectors/    # 各种检测器
├── navigation/       # 导航服务
├── scene/            # 场景记忆服务
├── event/            # 事件系统
└── system/           # 系统服务
```

### 2.4 core/

**职责**:
- 日志系统 (`logger.py`)
- 异常体系 (`exceptions.py`)
- 统一响应 (`response.py`)
- 错误管理 (`error_manager.py`)
- 工具函数 (`utils.py`)

### 2.5 config/

**职责**:
- 应用配置 (`settings.py`)
- 常量定义 (`constants.py`)
- 错误码体系 (`error_codes.py`)

---

## 3. 统一日志格式

### 3.1 日志格式规范

```
[LUNA][模块名][LEVEL] message { details }
```

**示例**:
```
[LUNA][Vision][WARN] ROI detect failed {error: "image format invalid", image_size: "1920x1080"}
[LUNA][TTS][INFO] TTS cache hit {text_hash: "abc123", latency_ms: 2}
[LUNA][Navigation][ERROR] Path planning failed {error_code: 5001, start: "A", end: "B"}
```

### 3.2 使用方式

```python
from core import logger

# 信息日志
logger.info("TTS 播报成功", details={"text_length": 100}, module="TTS")

# 警告日志
logger.warn("ROI 提取失败", details={"error": str(e)}, module="Vision")

# 错误日志
logger.error("导航初始化失败", details={"error_code": 3001}, module="Navigation")
```

### 3.3 日志级别

- `DEBUG`: 调试信息（开发环境）
- `INFO`: 一般信息（正常运行）
- `WARN`: 警告信息（可恢复的错误）
- `ERROR`: 错误信息（需要关注的问题）

---

## 4. API返回格式

### 4.1 成功响应

```json
{
  "success": true,
  "error_code": 0,
  "data": {
    // 实际数据
  },
  "message": "操作成功"  // 可选
}
```

### 4.2 错误响应

```json
{
  "success": false,
  "error_code": 3001,
  "error_message": "导航管理器未初始化",
  "details": {
    // 错误详情（可选）
  }
}
```

### 4.3 使用方式

```python
from core import api_success, api_error

# 成功响应
return api_success(data={"result": "ok"})

# 错误响应
return api_error(3001, details={"module": "navigation"})
```

---

## 5. 错误码使用规范

### 5.1 错误码格式

`MFFF` 格式：
- `M`: 模块编码（1位）
- `FFF`: 具体错误（3位）

### 5.2 模块编码

| 模块 | 代码 | 范围 |
|------|------|------|
| TTS | 1 | 1001-1999 |
| Vision | 2 | 2001-2999 |
| Navigation | 3 | 3001-3999 |
| Scene | 4 | 4001-4999 |
| Path | 5 | 5001-5999 |
| Performance | 6 | 6001-6999 |
| Event | 7 | 7001-7999 |
| System | 8 | 8001-8999 |
| Common | 9 | 9001-9999 |

### 5.3 使用方式

```python
from config.error_codes import NAV_MANAGER_NOT_INIT
from core import api_error

# 直接使用错误码常量
if navigation_manager is None:
    return api_error(NAV_MANAGER_NOT_INIT)

# 带详情
return api_error(NAV_MANAGER_NOT_INIT, details={"module": "navigation"})
```

### 5.4 异常处理

```python
from core.exceptions import NavigationException
from config.error_codes import NAV_MANAGER_NOT_INIT

try:
    result = navigation_service.start(destination)
except NavigationException as e:
    return api_exception(e, e.error_code)
except Exception as e:
    return api_exception(e, 9003, details={"original_error": str(e)})
```

---

## 6. 代码迁移指南

### 6.1 从 web_test_server.py 迁移

**步骤1**: 识别功能模块
- TTS 相关 → `services/tts/`
- 视觉相关 → `services/vision/`
- 导航相关 → `services/navigation/`
- 路由相关 → `routes/`

**步骤2**: 提取路由
```python
# 原代码 (web_test_server.py)
@app.route('/api/tts', methods=['POST'])
def tts():
    # 业务逻辑
    pass

# 新代码 (routes/tts_routes.py)
from flask import Blueprint
from services.tts import tts_service
from core import api_success, api_error

bp = Blueprint('tts', __name__)

@bp.route('/api/tts', methods=['POST'])
def tts():
    # 只负责参数解析和调用service
    data = request.get_json()
    result = tts_service.speak(data.get('text'))
    return api_success(result)
```

**步骤3**: 提取业务逻辑
```python
# services/tts/tts_manager.py
class TTSManager:
    def speak(self, text: str):
        # 业务逻辑
        pass
```

### 6.2 迁移检查清单

- [ ] 路由层只包含参数解析和service调用
- [ ] 业务逻辑都在services层
- [ ] 使用统一日志格式
- [ ] 使用统一响应格式
- [ ] 使用错误码体系
- [ ] 异常处理规范

---

## 📚 相关文档

- [错误码体系](../config/error_codes.py)
- [API文档](./API.md) (待创建)
- [部署指南](./DEPLOYMENT.md) (待创建)

---

**版本**: 1.2.0  
**最后更新**: 2025-11-19




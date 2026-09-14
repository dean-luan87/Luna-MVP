# Luna Backend v1.2.0 迁移指南

本文档指导如何从 `web_test_server.py` 迁移到新的模块化架构。

## 📋 迁移步骤

### 阶段1: 基础框架搭建 ✅

- [x] 创建目录结构
- [x] 创建核心模块（logger, exceptions, response）
- [x] 创建错误码体系
- [x] 创建配置管理

### 阶段2: 路由层迁移

**目标**: 将 `web_test_server.py` 中的路由提取到 `routes/` 目录

**步骤**:

1. 识别所有 `@app.route` 装饰器
2. 按功能分类（TTS、导航、视觉等）
3. 创建对应的路由文件
4. 提取参数解析逻辑
5. 调用 service 层方法

**示例**:

```python
# 原代码 (web_test_server.py)
@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text')
    # ... 业务逻辑

# 新代码 (routes/tts_routes.py)
from flask import Blueprint, request
from services.tts import tts_service
from core import api_success, api_error
from config.error_codes import TTS_TEXT_EMPTY

bp = Blueprint('tts', __name__)

@bp.route('/tts', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return api_error(TTS_TEXT_EMPTY)
    
    try:
        result = tts_service.speak(text)
        return api_success(result)
    except Exception as e:
        return api_exception(e)
```

### 阶段3: 服务层迁移

**目标**: 将业务逻辑提取到 `services/` 目录

**步骤**:

1. 识别业务逻辑代码块
2. 创建对应的 service 类
3. 实现业务方法
4. 使用统一日志和错误处理

**示例**:

```python
# services/tts/tts_manager.py
from core import logger
from core.exceptions import TTSException
from config.error_codes import TTS_TEXT_EMPTY, TTS_ENGINE_ERROR

class TTSManager:
    def __init__(self):
        # 初始化 TTS 引擎
        pass
    
    def speak(self, text: str):
        if not text:
            raise TTSException(TTS_TEXT_EMPTY)
        
        try:
            # 业务逻辑
            result = self._do_speak(text)
            logger.info("TTS 播报成功", details={"text_length": len(text)}, module="TTS")
            return result
        except Exception as e:
            logger.error("TTS 播报失败", details={"error": str(e)}, module="TTS")
            raise TTSException(TTS_ENGINE_ERROR, details={"exception": str(e)})
    
    def _do_speak(self, text: str):
        # 实际 TTS 实现
        pass
```

### 阶段4: 测试和验证

1. 单元测试每个 service
2. 集成测试路由
3. 端到端测试 API
4. 性能测试

## 🔍 迁移检查清单

### 路由层

- [ ] 只包含参数解析和验证
- [ ] 调用 service 层方法
- [ ] 使用统一响应格式
- [ ] 异常处理规范

### 服务层

- [ ] 业务逻辑完整
- [ ] 使用统一日志
- [ ] 使用错误码
- [ ] 异常处理规范

### 整体

- [ ] 所有路由已迁移
- [ ] 所有业务逻辑已迁移
- [ ] 测试通过
- [ ] 文档更新

## 📝 迁移示例

### TTS 模块迁移

**原代码位置**: `web_test_server.py` 第 XXXX-YYYY 行

**迁移到**:
- 路由: `routes/tts_routes.py`
- 服务: `services/tts/tts_manager.py`
- 缓存: `services/tts/tts_cache.py`
- 分段: `services/tts/tts_splitter.py`

### 视觉模块迁移

**原代码位置**: `web_test_server.py` 第 XXXX-YYYY 行

**迁移到**:
- 路由: `routes/visual_routes.py`
- 引擎: `services/vision/engine.py`
- 检测器: `services/vision/detectors/`

### 导航模块迁移

**原代码位置**: `web_test_server.py` 第 XXXX-YYYY 行

**迁移到**:
- 路由: `routes/navigation_routes.py`
- 管理器: `services/navigation/manager.py`
- 规划器: `services/navigation/planner.py`

## 🚀 快速开始迁移

1. 选择一个模块（建议从 TTS 开始）
2. 创建路由文件
3. 创建服务文件
4. 迁移代码
5. 测试验证
6. 重复步骤1-5

---

**版本**: 1.2.0  
**最后更新**: 2025-11-19




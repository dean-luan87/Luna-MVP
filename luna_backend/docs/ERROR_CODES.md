# Luna Backend 错误码体系文档 (v1.2.0)

**版本**: 1.2.0  
**更新日期**: 2025-11-19  
**用途**: 通过错误码快速定位问题模块和代码位置

---

## 📋 目录

- [错误码格式说明](#错误码格式说明)
- [模块分类](#模块分类)
- [快速查找](#快速查找)
- [使用指南](#使用指南)

---

## 🔢 错误码格式说明

### 格式规范

**MFFF** 格式：
- **M**: 模块编码（1位数字，1-9）
- **FFF**: 具体错误（3位数字，001-999）

### 示例

```
2001 → Vision模块，错误码001（视觉引擎未初始化）
3004 → Navigation模块，错误码004（导航启动失败）
1002 → TTS模块，错误码002（TTS引擎调用失败）
```

---

## 📦 模块分类

### 1. TTS 模块 (1xxx)

| 错误码 | 常量名 | 错误消息 | 可能原因 | 定位文件 |
|--------|--------|----------|----------|----------|
| **1001** | `TTS_NOT_INITIALIZED` | TTS 模块未初始化 | TTS管理器初始化失败 | `services/__init__.py` |
| **1002** | `TTS_ENGINE_ERROR` | TTS 引擎调用失败 | edge-tts调用异常 | `routes/tts_routes.py:generate_audio_segment()` |
| **1003** | `TTS_TEXT_EMPTY` | TTS 文本为空 | 请求参数缺失 | `routes/tts_routes.py:text_to_speech()` |
| **1004** | `TTS_SPLIT_FAILED` | TTS 文本分段失败 | 文本分段逻辑异常 | `routes/tts_routes.py:split_text()` |
| **1005** | `TTS_CACHE_WRITE_FAILED` | TTS 缓存写入失败 | 缓存文件写入异常 | `core/fast_tts_cache.py` |
| **1006** | `TTS_CACHE_READ_FAILED` | TTS 缓存读取失败 | 缓存文件读取异常 | `core/fast_tts_cache.py` |

**相关文件**:
- `routes/tts_routes.py` - TTS路由处理
- `services/tts/tts_manager.py` - TTS管理器（待迁移）
- `core/fast_tts_cache.py` - TTS缓存系统

---

### 2. Vision 模块 (2xxx)

| 错误码 | 常量名 | 错误消息 | 可能原因 | 定位文件 |
|--------|--------|----------|----------|----------|
| **2001** | `VISION_NOT_INITIALIZED` | 视觉引擎未初始化 | VisionOCREngine初始化失败 | `services/__init__.py` |
| **2002** | `IMAGE_FORMAT_INVALID` | 图片格式错误 | 图片解码失败 | `routes/visual_routes.py:image_to_numpy()` |
| **2003** | `ROI_EXTRACT_FAILED` | 显著性区域提取失败 | ROI提取算法异常 | `core/vision_ocr_engine.py` |
| **2004** | `YOLO_DETECT_FAILED` | 目标检测失败 | YOLO模型调用异常 | `core/vision_ocr_engine.py` |
| **2005** | `OCR_FAILED` | 文字识别失败 | OCR模型调用异常 | `core/vision_ocr_engine.py` |
| **2006** | `VISION_PIPELINE_ERROR` | 视觉处理流程发生错误 | 视觉处理管道异常 | `routes/visual_routes.py` |

**相关文件**:
- `routes/visual_routes.py` - 视觉路由处理
- `core/vision_ocr_engine.py` - 视觉OCR引擎
- `core/step_detector.py` - 台阶检测器
- `core/hazard_detector.py` - 危险检测器
- `core/signboard_detector.py` - 标识牌检测器

---

### 3. Navigation 模块 (3xxx)

| 错误码 | 常量名 | 错误消息 | 可能原因 | 定位文件 |
|--------|--------|----------|----------|----------|
| **3001** | `NAV_NOT_INITIALIZED` | 导航管理器未初始化 | NavigationManager初始化失败 | `services/__init__.py` |
| **3002** | `NAV_ROUTE_EMPTY` | 路径为空 | 路径规划结果为空 | `routes/navigation_routes.py:plan_route()` |
| **3003** | `NAV_UPDATE_FAILED` | 导航位置更新失败 | 位置更新逻辑异常 | `routes/navigation_routes.py:update_position()` |
| **3004** | `NAV_START_FAILED` | 导航启动失败 | 导航启动逻辑异常 | `routes/navigation_routes.py:start_navigation()` |
| **3005** | `NAV_ALREADY_RUNNING` | 当前已有导航任务 | 导航已在运行中 | `routes/navigation_routes.py:start_navigation()` |
| **3006** | `NAV_WAYPOINT_ERROR` | 航点推进异常 | 航点更新逻辑异常 | `core/navigation_manager.py` |

**相关文件**:
- `routes/navigation_routes.py` - 导航路由处理
- `core/navigation_manager.py` - 导航管理器
- `core/path_planner.py` - 路径规划器

---

### 4. Scene 模块 (4xxx)

| 错误码 | 常量名 | 错误消息 | 可能原因 | 定位文件 |
|--------|--------|----------|----------|----------|
| **4001** | `SCENE_NODE_DETECT_FAILED` | 节点检测失败 | 场景节点检测异常 | `core/scene_memory_system.py` |
| **4002** | `SCENE_MAP_WRITE_FAILED` | 地图记忆写入失败 | 地图数据写入异常 | `core/scene_memory_system.py` |
| **4003** | `SCENE_TOPOLOGY_FAILED` | 拓扑构建失败 | 拓扑图构建异常 | `core/scene_memory_system.py` |
| **4004** | `SCENE_STRUCTURE_FAILED` | 结构分析失败 | 场景结构分析异常 | `core/scene_memory_system.py` |

**相关文件**:
- `core/scene_memory_system.py` - 场景记忆系统

---

### 5. Path 模块 (5xxx)

| 错误码 | 常量名 | 错误消息 | 可能原因 | 定位文件 |
|--------|--------|----------|----------|----------|
| **5001** | `PATH_PLANNING_FAILED` | 路径规划失败 | 路径规划算法异常 | `routes/navigation_routes.py:plan_route()` |
| **5002** | `PATH_MULTI_TARGET_ERROR` | 多目标路径错误 | 多目标路径计算异常 | `core/path_planner.py` |
| **5003** | `PATH_EXIT_DETECT_FAILED` | 出口识别失败 | 出口检测异常 | `core/path_planner.py` |

**相关文件**:
- `core/path_planner.py` - 路径规划器

---

### 6. Performance 模块 (6xxx)

| 错误码 | 常量名 | 错误消息 | 可能原因 | 定位文件 |
|--------|--------|----------|----------|----------|
| **6001** | `PERF_DEGRADE_ERROR` | 降级模块异常 | 优雅降级逻辑异常 | `core/graceful_degrader.py` |
| **6002** | `PERF_STATS_ERROR` | 性能统计计算错误 | 性能指标计算异常 | `routes/metrics_routes.py:get_performance_metrics_route()` |

**相关文件**:
- `routes/metrics_routes.py` - 性能指标路由
- `core/graceful_degrader.py` - 优雅降级器

---

### 7. Event 模块 (7xxx)

| 错误码 | 常量名 | 错误消息 | 可能原因 | 定位文件 |
|--------|--------|----------|----------|----------|
| **7001** | `EVENT_BRIDGE_FAILED` | 事件桥接失败 | 事件桥接逻辑异常 | `services/event/unified_event_bridge.py` |
| **7002** | `EVENT_NAV_TRIGGER_FAILED` | NAV事件触发失败 | 导航事件触发异常 | `services/event/unified_events.py` |
| **7003** | `EVENT_EMOTION_HOOK_ERROR` | 情绪钩子异常 | 情绪处理异常 | `services/event/emotion_hook.py` |

**相关文件**:
- `services/event/` - 事件系统（待迁移）

---

### 8. System 模块 (8xxx)

| 错误码 | 常量名 | 错误消息 | 可能原因 | 定位文件 |
|--------|--------|----------|----------|----------|
| **8001** | `SYS_SSL_LOAD_FAILED` | SSL 加载失败 | SSL证书文件不存在或无效 | `routes/system_routes.py:download_cert()` |
| **8002** | `SYS_CONFIG_ERROR` | 配置错误 | 配置文件读取异常 | `config/settings.py` |

**相关文件**:
- `routes/system_routes.py` - 系统路由
- `config/settings.py` - 配置管理

---

### 9. Common 模块 (9xxx)

| 错误码 | 常量名 | 错误消息 | 可能原因 | 定位文件 |
|--------|--------|----------|----------|----------|
| **9001** | `PARAM_MISSING` | 缺少必要参数 | API请求参数缺失 | 各路由文件 |
| **9002** | `PARAM_INVALID` | 参数格式错误 | API请求参数格式不正确 | 各路由文件 |
| **9003** | `UNKNOWN_ERROR` | 未知错误 | 未分类的异常 | 各路由文件 |

**相关文件**:
- 所有路由文件

---

## 🔍 快速查找

### 按错误码查找

```bash
# 查找错误码对应的信息
grep -r "ERR.VISION_NOT_INITIALIZED" luna_backend/
```

### 按模块查找

```bash
# 查找Vision模块所有错误码
grep -E "2[0-9]{3}" config/error_codes.py
```

### 按文件查找

```bash
# 查找某个文件使用的错误码
grep -E "ERR\.[A-Z_]+" routes/visual_routes.py
```

---

## 📝 使用指南

### 1. 在代码中使用错误码

```python
from config.error_codes import ERR
from core.response import api_error
from core.logger import log_error

# 在路由中使用
@visual_bp.route("/api/recognize", methods=["POST"])
def recognize():
    vision_engine = get_vision_engine()
    if vision_engine is None:
        return api_error(ERR.VISION_NOT_INITIALIZED, http_status=500)
    
    # ... 业务逻辑 ...
    
    except Exception as e:
        log_error(logger, ERR.VISION_PIPELINE_ERROR, "视觉识别失败", {
            "exception": str(e),
            "file": __file__,
            "function": "recognize"
        })
        return api_exception(e, ERR.VISION_PIPELINE_ERROR)
```

### 2. 在日志中查看错误码

日志格式：
```
[LUNA][Vision][ERROR] [ERR-2006] 视觉识别失败 { 
  "error_code": 2006, 
  "exception": "...", 
  "file": "routes/visual_routes.py",
  "function": "recognize",
  "line": 45
}
```

### 3. 通过错误码定位问题

**步骤1**: 查看错误码
```
错误码: 2006
```

**步骤2**: 查找错误码定义
```python
# config/error_codes.py
VISION_PIPELINE_ERROR = 2006  # 视觉处理流程发生错误
```

**步骤3**: 查找使用位置
```bash
grep -rn "VISION_PIPELINE_ERROR" luna_backend/
```

**步骤4**: 查看日志详情
```
[ERR-2006] 视觉识别失败 {
  "file": "routes/visual_routes.py",
  "function": "recognize",
  "line": 45,
  "exception": "cv2.imdecode failed"
}
```

**步骤5**: 定位到具体代码
```python
# routes/visual_routes.py:45
image_np = image_to_numpy(file.read())  # ← 这里出错
```

---

## 🛠️ 错误码查询工具

### Python脚本

```python
# tools/error_code_lookup.py
from config.error_codes import ERR, ERROR_MESSAGES, get_module_name

def lookup_error_code(code: int):
    """查询错误码信息"""
    module = get_module_name(code)
    message = ERROR_MESSAGES.get(code, "未知错误码")
    
    print(f"错误码: {code}")
    print(f"模块: {module}")
    print(f"消息: {message}")
    
    # 查找使用位置
    import subprocess
    result = subprocess.run(
        ["grep", "-rn", f"ERR\\.[A-Z_]+.*=.*{code}", "luna_backend/"],
        capture_output=True,
        text=True
    )
    if result.stdout:
        print(f"\n定义位置:\n{result.stdout}")

# 使用示例
lookup_error_code(2006)
```

---

## 📊 错误码统计

| 模块 | 错误码范围 | 已定义 | 可用空间 |
|------|-----------|--------|----------|
| TTS | 1001-1999 | 6 | 993 |
| Vision | 2001-2999 | 6 | 993 |
| Navigation | 3001-3999 | 6 | 993 |
| Scene | 4001-4999 | 4 | 995 |
| Path | 5001-5999 | 3 | 996 |
| Performance | 6001-6999 | 2 | 997 |
| Event | 7001-7999 | 3 | 996 |
| System | 8001-8999 | 2 | 997 |
| Common | 9001-9999 | 3 | 996 |
| **总计** | **1000-9999** | **35** | **9964** |

---

## 🔗 相关文档

- [工程规范](./ENGINEERING_STANDARDS.md)
- [架构文档](./V1.2.0_ARCHITECTURE.md)
- [错误码源码](../config/error_codes.py)

---

**版本**: 1.2.0  
**最后更新**: 2025-11-19




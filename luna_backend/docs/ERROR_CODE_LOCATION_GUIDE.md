# 错误码定位指南 (v1.2.0)

**用途**: 通过错误码快速定位到代码位置，快速修复bug

---

## 🎯 定位流程

### 步骤1: 获取错误码

从API响应或日志中获取错误码：

```json
{
  "success": false,
  "error_code": 2006,
  "error_message": "视觉处理流程发生错误"
}
```

或从日志：
```
[LUNA][Vision][ERROR] [ERR-2006] 视觉识别失败 { 
  "error_code": 2006, 
  "file": "routes/visual_routes.py",
  "function": "recognize",
  "line": "45"
}
```

### 步骤2: 查询错误码信息

#### 方法1: 使用查询工具

```bash
cd luna_backend
python tools/error_code_lookup.py 2006
```

输出：
```
============================================================
错误码: 2006
模块: Vision
消息: 视觉处理流程发生错误
============================================================

📝 常量定义:
  ERR.VISION_PIPELINE_ERROR = 2006

🔍 使用位置:
  config/error_codes.py:45:    VISION_PIPELINE_ERROR   = 2006

📂 代码中使用:
  routes/visual_routes.py:120: return api_exception(e, ERR.VISION_PIPELINE_ERROR)
```

#### 方法2: 查看错误码文档

打开 `docs/ERROR_CODES.md`，查找错误码2006：

| 错误码 | 常量名 | 错误消息 | 可能原因 | 定位文件 |
|--------|--------|----------|----------|----------|
| **2006** | `VISION_PIPELINE_ERROR` | 视觉处理流程发生错误 | 视觉处理管道异常 | `routes/visual_routes.py` |

#### 方法3: 直接查看代码

```bash
# 查找错误码定义
grep -rn "VISION_PIPELINE_ERROR" luna_backend/config/error_codes.py

# 查找错误码使用
grep -rn "VISION_PIPELINE_ERROR" luna_backend/
```

### 步骤3: 定位到具体代码

根据日志中的位置信息，直接定位：

```
file: routes/visual_routes.py
function: recognize
line: 45
```

打开 `routes/visual_routes.py`，找到第45行：

```python
@visual_bp.route("/api/recognize", methods=["POST"])
def recognize():
    # ... 前面的代码 ...
    
    try:
        results = vision_engine.detect_and_recognize(image_np)  # ← 第45行
    except Exception as e:
        log_error(logger, ERR.VISION_PIPELINE_ERROR, "视觉识别失败", {"exception": str(e)})
        return api_exception(e, ERR.VISION_PIPELINE_ERROR)
```

### 步骤4: 分析问题

根据错误详情分析：

1. **查看异常信息**: `details.exception` 字段
2. **查看调用栈**: 日志中的 `file`, `function`, `line`
3. **查看上下文**: 错误发生前后的代码逻辑

### 步骤5: 修复问题

根据分析结果修复代码，并确保：
- 错误码使用正确
- 日志记录完整
- 异常处理合理

---

## 📊 错误码映射表（快速查找）

### TTS模块 (1xxx)

| 错误码 | 常量名 | 定位文件 |
|--------|--------|----------|
| 1001 | `TTS_NOT_INITIALIZED` | `services/__init__.py` |
| 1002 | `TTS_ENGINE_ERROR` | `routes/tts_routes.py` |
| 1003 | `TTS_TEXT_EMPTY` | `routes/tts_routes.py` |
| 1004 | `TTS_SPLIT_FAILED` | `routes/tts_routes.py:split_text()` |
| 1005 | `TTS_CACHE_WRITE_FAILED` | `core/fast_tts_cache.py` |
| 1006 | `TTS_CACHE_READ_FAILED` | `core/fast_tts_cache.py` |

### Vision模块 (2xxx)

| 错误码 | 常量名 | 定位文件 |
|--------|--------|----------|
| 2001 | `VISION_NOT_INITIALIZED` | `services/__init__.py` |
| 2002 | `IMAGE_FORMAT_INVALID` | `routes/visual_routes.py:image_to_numpy()` |
| 2003 | `ROI_EXTRACT_FAILED` | `core/vision_ocr_engine.py` |
| 2004 | `YOLO_DETECT_FAILED` | `core/vision_ocr_engine.py` |
| 2005 | `OCR_FAILED` | `core/vision_ocr_engine.py` |
| 2006 | `VISION_PIPELINE_ERROR` | `routes/visual_routes.py` |

### Navigation模块 (3xxx)

| 错误码 | 常量名 | 定位文件 |
|--------|--------|----------|
| 3001 | `NAV_NOT_INITIALIZED` | `services/__init__.py` |
| 3002 | `NAV_ROUTE_EMPTY` | `routes/navigation_routes.py:plan_route()` |
| 3003 | `NAV_UPDATE_FAILED` | `routes/navigation_routes.py:update_position()` |
| 3004 | `NAV_START_FAILED` | `routes/navigation_routes.py:start_navigation()` |
| 3005 | `NAV_ALREADY_RUNNING` | `routes/navigation_routes.py:start_navigation()` |
| 3006 | `NAV_WAYPOINT_ERROR` | `core/navigation_manager.py` |

---

## 🔍 常见问题定位

### 问题1: 视觉识别失败

**错误码**: 2006  
**日志示例**:
```
[LUNA][Vision][ERROR] [ERR-2006] 视觉识别失败 {
  "error_code": 2006,
  "file": "routes/visual_routes.py",
  "function": "recognize",
  "line": "45",
  "exception": "cv2.imdecode failed"
}
```

**定位步骤**:
1. 打开 `routes/visual_routes.py`
2. 找到 `recognize()` 函数
3. 查看第45行附近的代码
4. 检查 `image_to_numpy()` 函数实现

### 问题2: TTS引擎调用失败

**错误码**: 1002  
**日志示例**:
```
[LUNA][TTS][ERROR] [ERR-1002] TTS生成失败 {
  "error_code": 1002,
  "file": "routes/tts_routes.py",
  "function": "text_to_speech",
  "line": "120",
  "exception": "edge_tts.Communicate failed"
}
```

**定位步骤**:
1. 打开 `routes/tts_routes.py`
2. 找到 `text_to_speech()` 函数
3. 查看 `generate_audio_segment()` 调用
4. 检查 edge-tts 连接和参数

### 问题3: 导航启动失败

**错误码**: 3004  
**日志示例**:
```
[LUNA][Navigation][ERROR] [ERR-3004] 启动导航失败 {
  "error_code": 3004,
  "file": "routes/navigation_routes.py",
  "function": "start_navigation",
  "line": "60",
  "exception": "NavigationManager.start_navigation() failed"
}
```

**定位步骤**:
1. 打开 `routes/navigation_routes.py`
2. 找到 `start_navigation()` 函数
3. 查看 `navigation_manager.start_navigation()` 调用
4. 检查 `core/navigation_manager.py` 实现

---

## 🛠️ 工具使用

### 错误码查询工具

```bash
# 查询单个错误码
python tools/error_code_lookup.py 2006

# 列出所有错误码
python tools/error_code_lookup.py --list
```

### 日志分析脚本

```bash
# 查找特定错误码的日志
grep "ERR-2006" logs/*.log

# 查找特定文件的错误
grep "routes/visual_routes.py" logs/*.log
```

---

## 📝 最佳实践

1. **使用错误码常量**: 不要硬编码错误码数字
2. **记录完整信息**: 日志中包含文件、函数、行号
3. **错误码文档化**: 新增错误码时更新文档
4. **统一错误处理**: 使用 `api_exception()` 统一处理异常

---

**版本**: 1.2.0  
**最后更新**: 2025-11-19




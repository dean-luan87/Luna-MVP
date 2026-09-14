# Luna Backend 快速参考 (v1.2.0)

## 🔍 错误码快速查找

### 按模块查找

| 模块 | 错误码范围 | 文档 |
|------|-----------|------|
| TTS | 1001-1999 | [ERROR_CODES.md](./ERROR_CODES.md#1-tts-模块-1xxx) |
| Vision | 2001-2999 | [ERROR_CODES.md](./ERROR_CODES.md#2-vision-模块-2xxx) |
| Navigation | 3001-3999 | [ERROR_CODES.md](./ERROR_CODES.md#3-navigation-模块-3xxx) |
| Scene | 4001-4999 | [ERROR_CODES.md](./ERROR_CODES.md#4-scene-模块-4xxx) |
| Path | 5001-5999 | [ERROR_CODES.md](./ERROR_CODES.md#5-path-模块-5xxx) |
| Performance | 6001-6999 | [ERROR_CODES.md](./ERROR_CODES.md#6-performance-模块-6xxx) |
| Event | 7001-7999 | [ERROR_CODES.md](./ERROR_CODES.md#7-event-模块-7xxx) |
| System | 8001-8999 | [ERROR_CODES.md](./ERROR_CODES.md#8-system-模块-8xxx) |
| Common | 9001-9999 | [ERROR_CODES.md](./ERROR_CODES.md#9-common-模块-9xxx) |

### 常用错误码

| 错误码 | 常量名 | 说明 |
|--------|--------|------|
| 2001 | `VISION_NOT_INITIALIZED` | 视觉引擎未初始化 |
| 2006 | `VISION_PIPELINE_ERROR` | 视觉处理流程错误 |
| 3001 | `NAV_NOT_INITIALIZED` | 导航管理器未初始化 |
| 3004 | `NAV_START_FAILED` | 导航启动失败 |
| 1002 | `TTS_ENGINE_ERROR` | TTS引擎调用失败 |
| 9001 | `PARAM_MISSING` | 缺少必要参数 |

---

## 📝 日志格式

### 标准格式

```
[LUNA][模块名][LEVEL] message { details }
```

### 错误日志格式（带位置信息）

```
[LUNA][Vision][ERROR] [ERR-2006] 视觉识别失败 {
  "error_code": 2006,
  "file": "routes/visual_routes.py",
  "function": "recognize",
  "line": "45",
  "exception": "..."
}
```

### 使用示例

```python
from core.logger import logger, log_error
from config.error_codes import ERR

# 普通日志
logger.info("处理完成", details={"count": 10}, module="Vision")

# 错误日志（自动记录位置）
log_error(logger, ERR.VISION_PIPELINE_ERROR, "视觉处理失败", {
    "exception": str(e)
})
```

---

## 🛠️ 工具使用

### 错误码查询

```bash
# 查询错误码
python tools/error_code_lookup.py 2006

# 列出所有错误码
python tools/error_code_lookup.py --list
```

### 日志分析

```bash
# 查找特定错误码
grep "ERR-2006" logs/*.log

# 查找特定文件
grep "routes/visual_routes.py" logs/*.log
```

---

## 📚 文档索引

- [错误码文档](./ERROR_CODES.md) - 完整的错误码分类和说明
- [错误码定位指南](./ERROR_CODE_LOCATION_GUIDE.md) - 如何通过错误码定位问题
- [工程规范](./ENGINEERING_STANDARDS.md) - 开发规范
- [架构文档](./V1.2.0_ARCHITECTURE.md) - 系统架构

---

**版本**: 1.2.0  
**最后更新**: 2025-11-19




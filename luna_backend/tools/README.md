# Luna Backend 工具集

## error_code_lookup.py

错误码查询工具，用于快速定位错误码对应的模块、消息和使用位置。

### 使用方法

```bash
# 查询单个错误码
python tools/error_code_lookup.py 2006

# 列出所有错误码
python tools/error_code_lookup.py --list
```

### 输出示例

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

---

## 相关文档

- [错误码文档](../docs/ERROR_CODES.md) - 完整的错误码分类和说明
- [错误码定位指南](../docs/ERROR_CODE_LOCATION_GUIDE.md) - 如何通过错误码定位问题




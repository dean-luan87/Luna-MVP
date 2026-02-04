# Vision Health API 使用指南

本文档介绍如何使用 Vision Health API 来监控和调试视觉模型的健康状态。

## 概述

Vision Health API 提供了完整的模型健康监控能力，包括：
- 模型调用统计（总次数、成功次数、失败次数）
- 成功率、平均置信度、平均最终得分
- 动态权重和启用状态
- 最近错误信息

## 组件

### 1. VisionDebugService

核心服务类，封装了从 MultiModelEngine 获取健康快照的功能。

```python
from core.vision import MultiModelEngine, VisionDebugService

engine = MultiModelEngine(max_workers=4)
debug_service = VisionDebugService(engine)

# 获取完整健康快照
snapshot = debug_service.get_health()
print(snapshot.to_dict())

# 获取特定任务类型的模型健康
detect_models = debug_service.get_model_block("detect")
```

### 2. HTTP API 服务

独立的 HTTP API 服务器，提供 RESTful 接口。

#### 启动服务

```bash
python scripts/vision_health_api_server.py
```

服务将在 `http://localhost:8082` 启动。

#### API 端点

**获取完整健康快照**
```
GET /api/debug/vision/health
```

响应示例：
```json
{
  "ok": true,
  "data": {
    "engine_status": {
      "total_task_types": 2
    },
    "models": {
      "detect": {
        "yolo11n": {
          "total_calls": 100,
          "success_calls": 95,
          "failure_calls": 5,
          "success_rate": 0.95,
          "avg_conf": 0.85,
          "avg_final_score": 0.85,
          "enabled": true,
          "weight": 0.6,
          "last_error": ""
        }
      }
    }
  }
}
```

**获取特定任务类型的模型健康**
```
GET /api/debug/vision/health/{task_type}
```

例如：
```
GET /api/debug/vision/health/detect
```

### 3. CLI 工具

命令行工具，用于本地调试和查看模型健康状态。

```bash
python scripts/vision_health_cli.py
```

输出示例：
```
=== Vision Model Health Snapshot ===
{
  'engine_status': {'total_task_types': 1},
  'models': {
    'detect': {
      'good_model': {
        'enabled': True,
        'weight': 0.5,
        'success_rate': 1.0,
        'total_calls': 20,
        'avg_conf': 0.9
      }
    }
  }
}
```

## 集成到现有应用

### Flask 应用集成

```python
from flask import Flask
from core.vision import MultiModelEngine
from scripts.vision_health_api_server import (
    create_vision_debug_blueprint,
    init_vision_debug_service
)

app = Flask(__name__)

# 初始化引擎
engine = MultiModelEngine(max_workers=4)

# 初始化调试服务
init_vision_debug_service(engine)

# 注册路由
blueprint = create_vision_debug_blueprint()
app.register_blueprint(blueprint, url_prefix="/api/debug")
```

### FastAPI 应用集成

```python
from fastapi import FastAPI
from core.vision import MultiModelEngine, VisionDebugService

app = FastAPI()

# 初始化引擎和服务
engine = MultiModelEngine(max_workers=4)
debug_service = VisionDebugService(engine)

@app.get("/api/debug/vision/health")
async def get_vision_health():
    snapshot = debug_service.get_health()
    return {"ok": True, "data": snapshot.to_dict()}
```

## 健康快照字段说明

### 模型统计字段

- `total_calls`: 总调用次数
- `success_calls`: 成功调用次数
- `failure_calls`: 失败调用次数
- `success_rate`: 成功率（0.0 - 1.0）
- `avg_conf`: 平均置信度（成功样本的平均 max_conf）
- `avg_final_score`: 平均最终得分（成功样本的平均 final_score）
- `last_error`: 最近一次错误信息
- `enabled`: 是否启用（可能被自动禁用）
- `weight`: 当前权重（已归一化）

### 引擎状态字段

- `total_task_types`: 已注册的任务类型数量

## 使用场景

### 1. 模型性能监控

定期查询健康快照，监控模型表现：
- 成功率下降 → 可能模型有问题
- 平均置信度下降 → 可能需要调整阈值
- 权重变化 → 系统自动调整的证据

### 2. 故障排查

查看 `last_error` 字段，了解模型失败原因：
- 超时错误 → 可能需要优化模型或硬件
- 内存错误 → 可能需要减少并发
- 模型加载错误 → 检查模型文件

### 3. 权重调优

观察权重变化趋势，验证动态调整策略：
- 表现好的模型权重应该上升
- 表现差的模型权重应该下降或被禁用

### 4. 运维 Dashboard

将健康快照数据可视化：
- 模型可靠性趋势图
- 权重变化曲线
- 成功率热力图
- 错误类型分布

## 注意事项

1. **性能影响**：健康快照查询是轻量级操作，但频繁查询可能影响性能
2. **数据持久化**：当前版本数据保存在内存中，重启后丢失
3. **并发安全**：ScoreLogger 和 MultiModelEngine 是线程安全的
4. **权限控制**：生产环境建议添加认证和授权

## 未来扩展

- 数据持久化（数据库/文件）
- Prometheus 指标导出
- 异常波动检测
- 模型版本管理
- 云端健康汇报













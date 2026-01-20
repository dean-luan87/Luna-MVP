# HeatDecaySpec - 热衰减测试规范

**版本**: 1.0.0  
**最后更新**: 2025-12-02  
**用途**: 10 分钟持续压测的系统资源监控日志

---

## 📋 JSON Schema

### JSONL 单条记录

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "HeatDecaySpec",
  "type": "object",
  "required": [
    "timestamp",
    "cpu_percent",
    "mem_percent"
  ],
  "properties": {
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 时间戳（UTC）"
    },
    "cpu_percent": {
      "type": "number",
      "minimum": 0,
      "maximum": 100,
      "description": "CPU 使用率（0-100）"
    },
    "mem_percent": {
      "type": "number",
      "minimum": 0,
      "maximum": 100,
      "description": "内存使用率（0-100）"
    },
    "gpu_util": {
      "type": "number",
      "minimum": 0,
      "maximum": 100,
      "description": "GPU 使用率（0-100，可选）"
    },
    "gpu_temp": {
      "type": "number",
      "description": "GPU 温度（摄氏度，可选）"
    },
    "lat_total_avg": {
      "type": "number",
      "minimum": 0,
      "description": "平均总延迟（毫秒，可选）"
    },
    "lat_infer_avg": {
      "type": "number",
      "minimum": 0,
      "description": "平均推理延迟（毫秒，可选）"
    },
    "lat_nav_avg": {
      "type": "number",
      "minimum": 0,
      "description": "平均导航延迟（毫秒，可选）"
    }
  }
}
```

### JSON 汇总报告

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "HeatDecaySummary",
  "type": "object",
  "required": [
    "run_id",
    "duration_sec",
    "interval_sec",
    "sample_count",
    "cpu_avg",
    "cpu_max",
    "mem_avg",
    "mem_max"
  ],
  "properties": {
    "run_id": {
      "type": "string",
      "description": "运行 ID，格式：heat_YYYYMMDD_HHMMSS"
    },
    "duration_sec": {
      "type": "integer",
      "minimum": 0,
      "description": "测试时长（秒）"
    },
    "interval_sec": {
      "type": "integer",
      "minimum": 1,
      "description": "采样间隔（秒）"
    },
    "sample_count": {
      "type": "integer",
      "minimum": 0,
      "description": "采样数量"
    },
    "cpu_avg": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "cpu_max": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "cpu_min": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "mem_avg": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "mem_max": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "mem_min": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "gpu_util_avg": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "gpu_util_max": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "gpu_temp_avg": {
      "type": "number"
    },
    "gpu_temp_max": {
      "type": "number"
    },
    "lat_total_avg": {
      "type": "number",
      "minimum": 0
    },
    "lat_infer_avg": {
      "type": "number",
      "minimum": 0
    },
    "lat_nav_avg": {
      "type": "number",
      "minimum": 0
    }
  }
}
```

---

## ✅ 字段说明

### JSONL 单条记录

| 字段 | 类型 | 约束 | 说明 | 必须 |
|------|------|------|------|------|
| `timestamp` | string | ISO 8601 | ISO 8601 时间戳（UTC） | ✅ |
| `cpu_percent` | number | 0-100 | CPU 使用率 | ✅ |
| `mem_percent` | number | 0-100 | 内存使用率 | ✅ |
| `gpu_util` | number | 0-100 | GPU 使用率 | ❌ |
| `gpu_temp` | number | - | GPU 温度（摄氏度） | ❌ |
| `lat_total_avg` | number | >= 0 | 平均总延迟（毫秒） | ❌ |
| `lat_infer_avg` | number | >= 0 | 平均推理延迟（毫秒） | ❌ |
| `lat_nav_avg` | number | >= 0 | 平均导航延迟（毫秒） | ❌ |

### JSON 汇总报告

| 字段 | 类型 | 说明 |
|------|------|------|
| `run_id` | string | 运行 ID |
| `duration_sec` | integer | 测试时长（秒） |
| `interval_sec` | integer | 采样间隔（秒） |
| `sample_count` | integer | 采样数量 |
| `cpu_avg/max/min` | number | CPU 统计 |
| `mem_avg/max/min` | number | 内存统计 |
| `gpu_util_avg/max` | number | GPU 使用率统计（可选） |
| `gpu_temp_avg/max` | number | GPU 温度统计（可选） |
| `lat_*_avg` | number | 延迟统计（可选） |

---

## 📝 使用示例

### 示例 1: JSONL 单条记录

```json
{
  "timestamp": "2025-01-18T13:22:01Z",
  "cpu_percent": 37.2,
  "mem_percent": 65.3,
  "gpu_util": 42.0,
  "gpu_temp": 68,
  "lat_total_avg": 118.2,
  "lat_infer_avg": 7.6,
  "lat_nav_avg": 3.5
}
```

### 示例 2: JSON 汇总报告

```json
{
  "run_id": "heat_20250118_132200",
  "duration_sec": 600,
  "interval_sec": 10,
  "sample_count": 60,
  "cpu_avg": 31.3,
  "cpu_max": 71.2,
  "cpu_min": 15.1,
  "mem_avg": 62.1,
  "mem_max": 75.0,
  "mem_min": 58.3,
  "gpu_util_avg": 35.2,
  "gpu_util_max": 68.5,
  "gpu_temp_avg": 65.2,
  "gpu_temp_max": 71,
  "lat_total_avg": 118.2,
  "lat_infer_avg": 7.6,
  "lat_nav_avg": 3.5
}
```

---

## 🔍 约束规则

### 必须字段（Must）

1. **timestamp**: 必须为有效的 ISO 8601 格式（UTC）
2. **cpu_percent**: 必须在 0-100 范围内
3. **mem_percent**: 必须在 0-100 范围内

### 可选字段（Optional）

- `gpu_util` 和 `gpu_temp`: 如果系统无 GPU，可以省略
- `lat_*_avg`: 如果未叠加性能日志，可以省略

### 文件命名

- **JSONL 文件**: `perf_logs/heat_YYYYMMDD_HHMMSS.jsonl`
- **JSON 汇总**: `perf_logs/heat_YYYYMMDD_HHMMSS.json`
- **CSV 文件**: `perf_logs/heat_YYYYMMDD_HHMMSS.csv`

---

## ⚠️ 异常情况说明

### 异常 1: GPU 数据缺失

**场景**: 系统无 GPU 或无法获取 GPU 数据

**处理**: `gpu_util` 和 `gpu_temp` 字段可以省略

### 异常 2: 采样间隔不一致

**场景**: 实际采样间隔与配置不一致

**处理**: 记录实际间隔，在汇总报告中标注

---

## 🔄 跨版本兼容策略

### 1.0.0 → 1.1.0（向后兼容）

**变更**: 新增 `disk_io_read_mb` 和 `disk_io_write_mb` 字段（可选）

**兼容性**: ✅ 完全兼容

---

## 📚 相关规范

- [PerfLogSpec.md](./PerfLogSpec.md) - 性能日志规范
- [EventBus.md](./EventBus.md) - 事件类型规范

---

**最后更新**: 2025-12-02
















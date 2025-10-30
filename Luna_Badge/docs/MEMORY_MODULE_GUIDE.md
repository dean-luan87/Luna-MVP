# 🧠 Luna Badge 记忆模块使用指南 v1.0

## 📋 概述

Luna Badge 记忆模块（Memory Module）是 EmotionMap 系统的核心组件之一，负责记录、缓存和上传用户的导航行为、情绪偏好和习惯数据，为后台用户画像分析和个性化推荐提供数据基础。

### 🎯 核心功能

- **📝 本地缓存**：在用户设备上缓存地图访问、节点情绪、操作行为
- **☁️ T+1上传**：每日自动在WiFi环境下上传昨天的数据到云端
- **🔒 隐私保护**：WiFi-only上传，支持数据加密和增量同步
- **📊 行为分析**：为后台用户画像、习惯学习、路线推荐提供数据

---

## 🧩 模块架构

```
memory_store/
├── local_memory/              # 本地记忆存储
│   ├── 2025-10-30_user123_memory.json
│   └── 2025-10-31_user123_memory.json
├── uploaded_flags/            # 已上传标记
│   └── 2025-10-30_user123.uploaded
├── packages/                  # 打包数据（临时）
│   └── memory_package_20251030_120000.json.gz
└── tools/
    ├── memory_writer.py       # 记忆写入器
    └── memory_collector.py    # 记忆收集器

task_chain/timers/
└── memory_uploader.py         # 记忆上传器（T+1 + WiFi）

config/
└── memory_schema.json         # 数据结构标准
```

---

## 📚 API 使用

### 1. MemoryWriter - 记忆写入器

**功能**：记录用户地图访问、节点情绪、操作行为

#### 初始化

```python
from memory_store.tools.memory_writer import MemoryWriter

writer = MemoryWriter(user_id="user_123")
```

#### 记录地图访问

```python
writer.record_map_visit(
    map_id="hospital_outpatient",
    nodes_visited=["entrance", "toilet", "elevator_3f", "consult_301"],
    emotion_tags={
        "toilet": "推荐",
        "elevator_3f": "焦躁",
        "consult_301": "安静"
    },
    duration_minutes=37,
    path=["entrance→toilet→elevator→consult_301"]
)
```

#### 记录应用行为

```python
# 请求导航指引
writer.record_app_behavior("asked_for_guidance")

# 使用语音输入
writer.record_app_behavior("used_voice_input")

# 查找附近厕所（计数型）
writer.record_app_behavior("requested_nearby_toilet")
writer.record_app_behavior("requested_nearby_toilet")
```

#### 写入完整记忆

```python
map_data = {
    "map_id": "hospital_outpatient",
    "nodes_visited": ["entrance", "toilet", "elevator_3f"],
    "emotion_tags": {"toilet": "推荐"},
    "duration_minutes": 37
}

app_behavior = {
    "asked_for_guidance": True,
    "used_voice_input": True,
    "requested_nearby_toilet": 2
}

writer.write_user_memory(map_data, app_behavior)
```

---

### 2. MemoryCollector - 记忆收集器

**功能**：收集待上传的记忆文件，打包数据，标记已上传状态

#### 初始化

```python
from memory_store.tools.memory_collector import MemoryCollector

collector = MemoryCollector()
```

#### 收集待上传记忆

```python
# 收集昨天的记忆（T+1）
pending = collector.collect_pending_memories()

# 收集指定日期
pending = collector.collect_pending_memories(date="2025-10-29")
```

#### 创建上传包

```python
# 压缩打包
package_path = collector.create_upload_package(pending, compress=True)

# 不压缩
package_path = collector.create_upload_package(pending, compress=False)
```

#### 标记已上传

```python
for memory_item in pending:
    collector.mark_as_uploaded(memory_item["file"])
```

#### 查看统计

```python
stats = collector.get_statistics()
print(f"总文件数: {stats['total_files']}")
print(f"已上传: {stats['uploaded_files']}")
print(f"待上传: {stats['pending_files']}")
print(f"总大小: {stats['total_size_kb']} KB")
```

---

### 3. MemoryUploader - 记忆上传器

**功能**：T+1自动上传记忆数据到云端（仅WiFi环境）

#### 初始化

```python
from task_chain.timers.memory_uploader import MemoryUploader

# 使用默认HTTP上传
uploader = MemoryUploader(
    upload_api_url="https://api.luna-project.com/v1/user/memory"
)

# 使用自定义上传函数
def custom_upload_func(memories):
    # 自定义上传逻辑
    return {"success": True}

uploader = MemoryUploader(
    upload_api_url="https://api.luna-project.com/v1/user/memory",
    upload_func=custom_upload_func
)
```

#### 检查WiFi

```python
if uploader.check_wifi_connected():
    print("📶 WiFi已连接")
else:
    print("⚠️ WiFi未连接")
```

#### 检查上传条件（T+1）

```python
# 检查昨天的记忆是否满足T+1条件
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
if uploader.should_upload(yesterday):
    print("✅ 可以上传")
```

#### 上传待上传记忆

```python
result = uploader.upload_pending_memories(retry_on_failure=True)

print(f"成功: {result['success']}")
print(f"上传数量: {result['uploaded_count']}")
```

---

## 🔄 完整工作流程

### 日常使用

```python
from memory_store.tools.memory_writer import MemoryWriter

# 1. 创建写入器
writer = MemoryWriter(user_id="user_123")

# 2. 记录地图访问
writer.record_map_visit(
    map_id="hospital_outpatient",
    nodes_visited=["entrance", "toilet", "elevator"],
    emotion_tags={"toilet": "推荐"},
    duration_minutes=25
)

# 3. 记录操作行为
writer.record_app_behavior("asked_for_guidance")
writer.record_app_behavior("used_voice_input")
```

### T+1自动上传

```python
from task_chain.timers.memory_uploader import MemoryUploader

# 1. 初始化上传器
uploader = MemoryUploader(
    upload_api_url="https://api.luna-project.com/v1/user/memory"
)

# 2. 上传昨天的记忆
result = uploader.upload_pending_memories()

if result["success"]:
    print(f"✅ 成功上传 {result['uploaded_count']} 条记忆")
else:
    print("❌ 上传失败，下次再试")
```

---

## 📊 数据结构

### 记忆文件格式

```json
{
  "user_id": "user_123",
  "date": "2025-10-30",
  "maps": [
    {
      "map_id": "hospital_outpatient",
      "nodes_visited": ["entrance", "toilet", "elevator_3f"],
      "emotion_tags": {
        "toilet": "推荐",
        "elevator_3f": "焦躁"
      },
      "duration_minutes": 37,
      "path": ["entrance→toilet→elevator"]
    }
  ],
  "app_behavior": {
    "asked_for_guidance": true,
    "used_voice_input": true,
    "requested_nearby_toilet": 2
  },
  "created_at": "2025-10-30T17:49:31.976655",
  "updated_at": "2025-10-30T18:00:00.000000"
}
```

---

## 🔒 隐私与安全

### WiFi-Only上传

记忆上传仅在使用WiFi时执行：

```python
if uploader.check_wifi_connected():
    result = uploader.upload_pending_memories()
else:
    print("⚠️ WiFi未连接，跳过上传")
```

### T+1延迟上传

- 当日数据**不**立即上传
- 次日（T+1）统一上传
- 为后台分析提供完整日度数据

### 已上传标记

- 上传成功后生成 `.uploaded` 标记文件
- 防止重复上传
- 支持增量同步

---

## 🧪 测试示例

### 完整测试流程

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta
from memory_store.tools.memory_writer import MemoryWriter
from memory_store.tools.memory_collector import MemoryCollector
from task_chain.timers.memory_uploader import MemoryUploader

logging.basicConfig(level=logging.INFO)

# 1. 写入测试数据
writer = MemoryWriter(user_id="test_user")
writer.record_map_visit(
    map_id="test_map",
    nodes_visited=["node1", "node2"],
    emotion_tags={"node1": "安静"},
    duration_minutes=15
)

# 2. 收集待上传记忆
collector = MemoryCollector()
pending = collector.collect_pending_memories()

# 3. 创建上传包
package = collector.create_upload_package(pending, compress=True)

# 4. 模拟上传
def mock_upload(memories):
    print(f"📤 模拟上传 {len(memories)} 条记忆")
    return {"success": True}

uploader = MemoryUploader(
    upload_api_url="https://api.luna-project.com/v1/user/memory",
    upload_func=mock_upload
)

result = uploader.upload_pending_memories()
print(f"上传结果: {result}")

# 5. 标记已上传
if result["success"]:
    for memory_item in pending:
        collector.mark_as_uploaded(memory_item["file"])
```

---

## 📌 集成建议

### 1. EmotionMap系统集成

在生成情绪地图后记录访问：

```python
from core.emotional_map_card_generator_enhanced import EmotionalMapCardGeneratorEnhanced
from memory_store.tools.memory_writer import MemoryWriter

# 生成地图
generator = EmotionalMapCardGeneratorEnhanced()
result = generator.generate_emotional_map("hospital_main")

# 记录访问
writer = MemoryWriter()
writer.record_map_visit(
    map_id="hospital_main",
    nodes_visited=["entrance", "toilet", "elevator"],
    emotion_tags={"toilet": "推荐"}
)
```

### 2. 定时上传任务

使用 `cron` 或系统任务调度器：

```bash
# 每天凌晨2点上传昨天的记忆
0 2 * * * cd /path/to/Luna_Badge && python3 task_chain/timers/memory_uploader.py
```

或在Python中：

```python
import schedule
import time

def upload_memories():
    uploader = MemoryUploader("https://api.luna-project.com/v1/user/memory")
    uploader.upload_pending_memories()

# 每天凌晨2点执行
schedule.every().day.at("02:00").do(upload_memories)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 🐛 常见问题

### Q1: WiFi检测失败

**问题**：`check_wifi_connected()` 返回 `False` 但实际已连接

**解决**：根据系统调整检测逻辑（macOS/Linux），或手动设置WiFi状态

### Q2: 重复上传

**问题**：同一条记忆被多次上传

**解决**：确保上传成功后调用 `mark_as_uploaded()` 标记

### Q3: 数据合并冲突

**问题**：同一天多次写入导致数据混乱

**解决**：MemoryWriter 自动合并同一天的记忆，使用 `updated_at` 字段跟踪更新时间

---

## 📚 相关文档

- `config/memory_schema.json` - 数据结构标准
- `MEMORY_MODULE_GUIDE.md` - 本文档
- `CROSS_DEVICE_SYNC_GUIDE.md` - 跨设备同步指南
- `MAP_SHARING_GUIDE.md` - 地图共享指南

---

## ✅ 总结

Luna Badge 记忆模块 v1.0 提供了完整的用户数据记录、缓存和上传解决方案：

- ✅ **本地缓存**：低功耗、安全存储
- ✅ **T+1上传**：隐私保护、完整数据
- ✅ **WiFi检测**：节省流量、保证质量
- ✅ **增量同步**：避免重复、高效传输
- ✅ **后台分析**：用户画像、智能推荐

准备就绪！🚀

# Luna 记忆模块使用指南

## 🎯 核心功能

记忆模块提供用户端缓存管理和后台分析数据上传功能。

---

## 📋 目录

1. [架构概述](#架构概述)
2. [缓存管理](#缓存管理)
3. [t+1上传机制](#t+1上传机制)
4. [使用示例](#使用示例)

---

## 架构概述

```
┌─────────────────────────────────────────────────────────┐
│                  记忆模块架构                             │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐      ┌──────────────┐                │
│  │  缓存管理器  │  ──►  │  后台上传器  │                │
│  │              │      │              │                │
│  │ - 地图缓存   │      │ - WiFi检测   │                │
│  │ - 场景缓存   │      │ - t+1上传    │                │
│  │ - 行为记录   │      │ - 队列管理   │                │
│  │ - 偏好设置   │      │              │                │
│  └──────────────┘      └──────────────┘                │
│          │                      │                        │
│          ▼                      ▼                        │
│  ┌──────────────────────────────────┐                   │
│  │        本地缓存存储                │                   │
│  │  - maps_cache.json                │                   │
│  │  - scenes_cache.json              │                   │
│  │  - user_behavior_cache.json       │                   │
│  │  - upload_queue.json              │                   │
│  └──────────────────────────────────┘                   │
│                                                           │
│          ▲                      ▼                        │
│          │                ┌──────────────┐               │
│          │                │   云端存储    │               │
│          │                │              │               │
│          │                │ - S3/OSS     │               │
│          │                │ - 数据分析   │               │
│          │                └──────────────┘               │
│          │                                                │
└──────────────────────────────────────────────────────────┘
```

---

## 缓存管理

### 地图缓存

```python
from core.memory_cache_manager import MemoryCacheManager

cache_manager = MemoryCacheManager()

# 缓存地图
map_data = {
    "map_id": "hospital_main",
    "path_name": "医院导航路径",
    "nodes": [...]
}

metadata = {
    "created_at": "2025-10-30T10:00:00",
    "regions": ["挂号大厅", "三楼病区"]
}

cache_manager.cache_map(map_data, metadata)
```

### 场景记忆缓存

```python
# 缓存场景
scene_data = {
    "scene_id": "scene_001",
    "location": "虹口医院",
    "caption": "医院入口",
    "image_path": "data/scenes/scene_001.jpg"
}

cache_manager.cache_scene(scene_data)
```

### 用户行为记录

```python
# 记录导航事件
cache_manager.record_navigation_event("start_navigation", {
    "destination": "虹口医院",
    "route_type": "walking",
    "distance": 1000,
    "start_time": "2025-10-30T10:00:00"
})

# 记录语音交互
cache_manager.record_voice_interaction("voice_command", {
    "command": "导航到虹口医院",
    "result": "success",
    "response_time": 0.5
})

# 记录偏好变化
cache_manager.update_user_preferences({
    "voice_speed": "normal",
    "prefer_walk": True,
    "avoid_transfer": False
})
```

### 获取缓存统计

```python
stats = cache_manager.get_cache_stats()
print(f"总地图数: {stats['total_maps']}")
print(f"未上传: {stats['unuploaded_maps']}")
print(f"缓存大小: {stats['cache_size_kb']} KB")
```

---

## t+1上传机制

### 设计原理

**t+1机制**：上次上传后至少间隔1小时才进行下一次上传

**优势**：
- ✅ 节省流量：批量上传，减少网络请求
- ✅ 降低功耗：减少频繁上传对电池的影响
- ✅ 智能触发：只在WiFi环境下自动上传
- ✅ 数据聚合：一小时内的数据合并上传

### 实现流程

```python
from core.background_uploader import BackgroundUploader

# 定义上传函数
def upload_to_cloud(upload_package):
    """实际上传函数"""
    import requests
    
    try:
        response = requests.post(
            "https://api.luna-project.com/v1/upload",
            json=upload_package,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30
        )
        
        if response.status_code == 200:
            return {"success": True}
        else:
            return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}

# 初始化上传器
cache_manager = MemoryCacheManager()
uploader = BackgroundUploader(
    cache_manager=cache_manager,
    upload_func=upload_to_cloud,
    wifi_check_interval=30,      # 30秒检测一次WiFi
    upload_check_interval=300    # 5分钟检查一次上传
)

# 启动后台上传服务
uploader.start()

# 停止服务（应用退出时）
uploader.stop()
```

### WiFi检测

系统会自动检测WiFi连接状态：

```python
# macOS
uploader.is_wifi_connected  # True/False

# Linux/RV1126
# 使用nmcli命令检测
```

### 手动强制上传

```python
# 立即上传（不等待t+1）
success = uploader.force_upload_now()

if success:
    print("✅ 上传成功")
else:
    print("❌ 上传失败")
```

### 获取上传状态

```python
status = uploader.get_status()

print(f"WiFi连接: {status['is_wifi_connected']}")
print(f"上次上传: {status['last_upload_time']}")
print(f"待上传: {status['pending_uploads']}")
```

---

## 使用示例

### 完整示例

```python
#!/usr/bin/env python3
"""Luna 记忆模块完整示例"""

import logging
from core.memory_cache_manager import MemoryCacheManager
from core.background_uploader import BackgroundUploader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    # 1. 初始化缓存管理器
    cache_manager = MemoryCacheManager(cache_dir="data/cache")
    
    # 2. 定义上传函数
    def upload_to_cloud(upload_package):
        """实际上传函数（替换为真实API）"""
        print(f"📤 上传数据包: {len(upload_package['maps'])}个地图")
        return {"success": True}
    
    # 3. 初始化上传器
    uploader = BackgroundUploader(
        cache_manager=cache_manager,
        upload_func=upload_to_cloud
    )
    
    # 4. 模拟使用场景
    print("=" * 60)
    print("🎨 模拟使用场景")
    print("=" * 60)
    
    # 用户生成地图
    print("\n1. 用户生成地图...")
    map_data = {
        "map_id": "test_hospital",
        "path_name": "医院导航",
        "nodes": [
            {"node_id": "n1", "label": "入口", "type": "entrance"},
            {"node_id": "n2", "label": "诊室", "type": "destination"}
        ]
    }
    cache_manager.cache_map(map_data)
    
    # 用户导航
    print("2. 用户开始导航...")
    cache_manager.record_navigation_event("start_navigation", {
        "destination": "虹口医院",
        "route": "walking"
    })
    
    # 语音交互
    print("3. 用户语音交互...")
    cache_manager.record_voice_interaction("voice_command", {
        "command": "导航到虹口医院",
        "result": "success"
    })
    
    # 5. 显示缓存统计
    print("\n4. 缓存统计...")
    stats = cache_manager.get_cache_stats()
    print(f"  总地图数: {stats['total_maps']}")
    print(f"  未上传: {stats['unuploaded_maps']}")
    print(f"  缓存大小: {stats['cache_size_kb']} KB")
    
    # 6. 启动后台上传
    print("\n5. 启动后台上传服务...")
    uploader.start()
    
    # 7. 显示上传状态
    status = uploader.get_status()
    print(f"  WiFi连接: {status['is_wifi_connected']}")
    print(f"  服务运行: {status['is_running']}")
    
    # 8. 强制上传（测试）
    print("\n6. 强制上传测试...")
    uploader.force_upload_now()
    
    # 9. 停止服务
    print("\n7. 停止服务...")
    uploader.stop()

if __name__ == "__main__":
    main()
```

---

## 数据上传包结构

上传包格式：

```json
{
  "timestamp": "2025-10-30T17:00:00",
  "maps": [
    {
      "map_id": "hospital_main",
      "path_name": "医院导航路径",
      "nodes": [...],
      "metadata": {...}
    }
  ],
  "scenes": [
    {
      "scene_id": "scene_001",
      "location": "虹口医院",
      "caption": "医院入口",
      "cached_at": "2025-10-30T10:00:00"
    }
  ],
  "behaviors": [
    {
      "behavior_type": "navigation",
      "data": {
        "event_type": "start_navigation",
        "data": {...},
        "timestamp": "2025-10-30T10:00:00"
      }
    }
  ],
  "preferences": {
    "voice_speed": "normal",
    "prefer_walk": true
  },
  "metadata": {
    "maps_count": 1,
    "scenes_count": 1,
    "behaviors_count": 5
  }
}
```

---

## 最佳实践

### 1. 内存管理

```python
# 定期清理已上传的旧数据（保留最近30天）
cache_manager.cleanup_old_uploaded_data(days=30)
```

### 2. 错误处理

```python
try:
    cache_manager.cache_map(map_data)
except Exception as e:
    logger.error(f"缓存失败: {e}")
    # 降级处理：保存到本地文件
```

### 3. 数据压缩

```python
# 大文件先压缩再缓存
import gzip

compressed_data = gzip.compress(json.dumps(map_data).encode())
cache_manager.cache_compressed_map(compressed_data)
```

### 4. 隐私保护

```python
# 敏感数据脱敏处理
def anonymize_data(data):
    # 移除个人信息
    data.pop("user_name", None)
    data.pop("phone_number", None)
    return data

cache_manager.cache_map(anonymize_data(map_data))
```

---

## 总结

记忆模块提供了：

- ✅ **本地缓存**：快速读写，离线可用
- ✅ **t+1上传**：智能批量上传，节省资源
- ✅ **WiFi检测**：自动检测网络环境
- ✅ **队列管理**：可靠的消息队列系统
- ✅ **数据分析**：丰富的行为数据采集

**核心价值**：让Luna真正理解用户，持续优化体验！


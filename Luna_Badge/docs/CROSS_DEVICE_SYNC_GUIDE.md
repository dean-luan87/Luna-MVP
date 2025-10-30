# Luna 跨设备记忆同步方案

## 🎯 核心目标

支持用户在切换设备时，通过登录账号下载并恢复所有地图记忆和导航数据。

---

## 📋 目录

1. [整体架构](#整体架构)
2. [数据模型](#数据模型)
3. [云端存储方案](#云端存储方案)
4. [同步流程](#同步流程)
5. [实现示例](#实现示例)

---

## 整体架构

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  设备A (Mac)    │  ────►  │   云端存储服务    │  ────►  │ 设备B (RV1126)  │
│                │         │                  │         │                │
│ - 地图生成      │         │ - 用户账号管理    │         │ - 地图下载      │
│ - 数据上传      │         │ - 记忆数据存储    │         │ - 数据恢复      │
│ - 路径记录      │         │ - 版本控制        │         │ - 导航使用      │
└─────────────────┘         └──────────────────┘         └─────────────────┘
      ▲                           ▲                                ▲
      │                           │                                │
      └─────────────── 用户账号登录 ───────────────────────────────┘
```

---

## 数据模型

### 用户账号数据结构

```json
{
  "user_id": "user_123456",
  "username": "张三",
  "created_at": "2025-10-01T10:00:00",
  "devices": [
    {
      "device_id": "mac_001",
      "device_name": "MacBook Pro",
      "last_sync": "2025-10-30T17:30:00"
    },
    {
      "device_id": "rv1126_001",
      "device_name": "Luna Badge",
      "last_sync": "2025-10-30T16:00:00"
    }
  ]
}
```

### 地图记忆数据结构

```json
{
  "user_id": "user_123456",
  "maps": [
    {
      "map_id": "hospital_main_enhanced",
      "path_id": "hospital_main_enhanced",
      "version": "1.0",
      "created_at": "2025-10-30T16:29:28",
      "last_modified": "2025-10-30T16:29:28",
      "data": {
        "path_name": "医院完整导航路径",
        "nodes": [...],
        "regions": [...],
        "metadata": {...}
      },
      "files": {
        "image": "hospital_main_enhanced_emotional.png",
        "metadata": "hospital_main_enhanced_emotional.meta.json"
      }
    }
  ],
  "total_maps": 1,
  "storage_used": "2.5MB"
}
```

### 场景记忆数据结构

```json
{
  "user_id": "user_123456",
  "scenes": [
    {
      "scene_id": "scene_001",
      "location": "虹口医院",
      "captured_at": "2025-10-30T10:00:00",
      "images": [
        "scene_images/scene_001_1.jpg",
        "scene_images/scene_001_2.jpg"
      ],
      "annotations": {
        "doorplate": "内分泌科",
        "landmarks": ["电梯", "卫生间"],
        "emotions": ["安静"]
      }
    }
  ],
  "total_scenes": 5
}
```

### 用户偏好数据结构

```json
{
  "user_id": "user_123456",
  "preferences": {
    "navigation": {
      "prefer_walk": true,
      "avoid_transfer": false,
      "voice_speed": "normal",
      "notification_level": "normal"
    },
    "memory": {
      "auto_save": true,
      "cloud_sync": true,
      "retention_days": 30
    }
  },
  "family_faces": [
    {
      "face_id": "face_001",
      "label": "妈妈",
      "relationship": "mother"
    }
  ]
}
```

---

## 云端存储方案

### 方案 A：基于云存储服务（推荐）

#### AWS S3 / 阿里云OSS

```python
import boto3
from pathlib import Path

class CloudMapStorage:
    """云端地图存储"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.bucket_name = "luna-user-maps"
        self.s3_client = boto3.client('s3')
    
    def upload_map(self, map_data: dict, map_files: dict):
        """上传地图数据"""
        # 上传JSON数据
        json_key = f"{self.user_id}/maps/{map_data['map_id']}/data.json"
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=json_key,
            Body=json.dumps(map_data, ensure_ascii=False)
        )
        
        # 上传PNG图像
        if "image" in map_files:
            image_key = f"{self.user_id}/maps/{map_data['map_id']}/map.png"
            self.s3_client.upload_file(
                map_files["image"],
                self.bucket_name,
                image_key
            )
        
        return True
    
    def download_map(self, map_id: str, local_dir: str):
        """下载地图数据"""
        map_dir = Path(local_dir)
        map_dir.mkdir(parents=True, exist_ok=True)
        
        # 下载JSON
        json_key = f"{self.user_id}/maps/{map_id}/data.json"
        self.s3_client.download_file(
            self.bucket_name,
            json_key,
            str(map_dir / f"{map_id}.json")
        )
        
        # 下载PNG
        image_key = f"{self.user_id}/maps/{map_id}/map.png"
        self.s3_client.download_file(
            self.bucket_name,
            image_key,
            str(map_dir / f"{map_id}.png")
        )
        
        return True
    
    def list_user_maps(self):
        """列出用户的所有地图"""
        prefix = f"{self.user_id}/maps/"
        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=prefix
        )
        
        maps = []
        for obj in response.get('Contents', []):
            if obj['Key'].endswith('/data.json'):
                map_id = obj['Key'].split('/')[-2]
                maps.append(map_id)
        
        return maps
```

#### 文件结构

```
luna-user-maps/
├── user_123456/
│   ├── maps/
│   │   ├── hospital_main_enhanced/
│   │   │   ├── data.json
│   │   │   ├── map.png
│   │   │   └── metadata.json
│   │   └── mall_navigation/
│   │       ├── data.json
│   │       ├── map.png
│   │       └── metadata.json
│   ├── scenes/
│   │   ├── scene_001/
│   │   │   ├── image1.jpg
│   │   │   ├── image2.jpg
│   │   │   └── metadata.json
│   ├── preferences.json
│   └── devices.json
```

---

## 同步流程

### 1. 首次上传（设备A）

```python
def sync_maps_to_cloud(user_id: str, local_map_dir: str):
    """将本地地图同步到云端"""
    loader = LunaMapLoader(local_map_dir)
    storage = CloudMapStorage(user_id)
    
    # 列出所有本地地图
    local_maps = loader.list_available_maps()
    
    sync_results = []
    for map_id in local_maps:
        # 加载地图数据
        map_card = loader.load_map_card(map_id)
        
        if not map_card:
            continue
        
        # 上传到云端
        result = storage.upload_map(
            map_data=map_card["metadata"],
            map_files={
                "image": map_card["image"]
            }
        )
        
        sync_results.append({
            "map_id": map_id,
            "status": "success" if result else "failed"
        })
    
    return sync_results
```

### 2. 新设备下载（设备B）

```python
def sync_maps_from_cloud(user_id: str, local_map_dir: str):
    """从云端下载地图到本地"""
    storage = CloudMapStorage(user_id)
    loader = LunaMapLoader(local_map_dir)
    
    # 列出云端所有地图
    cloud_maps = storage.list_user_maps()
    
    download_results = []
    for map_id in cloud_maps:
        # 检查本地是否已存在
        if map_id in loader.list_available_maps():
            logger.info(f"地图已存在：{map_id}，跳过")
            continue
        
        # 下载地图
        result = storage.download_map(map_id, local_map_dir)
        
        download_results.append({
            "map_id": map_id,
            "status": "success" if result else "failed"
        })
    
    return download_results
```

### 3. 增量同步

```python
def incremental_sync(user_id: str, local_map_dir: str):
    """增量同步（只同步更新的地图）"""
    loader = LunaMapLoader(local_map_dir)
    storage = CloudMapStorage(user_id)
    
    # 获取云端地图元信息
    cloud_maps_info = storage.get_maps_metadata(user_id)
    
    # 获取本地地图信息
    local_maps_info = loader.list_available_maps_with_metadata()
    
    # 比较并决定同步方向
    sync_actions = []
    
    for cloud_map in cloud_maps_info:
        map_id = cloud_map["map_id"]
        local_map = local_maps_info.get(map_id)
        
        if not local_map:
            # 云端有，本地没有 -> 下载
            sync_actions.append({
                "action": "download",
                "map_id": map_id
            })
        elif cloud_map["last_modified"] > local_map["last_modified"]:
            # 云端更新 -> 下载
            sync_actions.append({
                "action": "download",
                "map_id": map_id
            })
    
    for local_map in local_maps_info.values():
        map_id = local_map["map_id"]
        if map_id not in cloud_maps_info:
            # 本地有，云端没有 -> 上传
            sync_actions.append({
                "action": "upload",
                "map_id": map_id
            })
    
    # 执行同步
    for action in sync_actions:
        if action["action"] == "download":
            storage.download_map(action["map_id"], local_map_dir)
        else:
            map_card = loader.load_map_card(action["map_id"])
            storage.upload_map(map_card["metadata"], map_card)
    
    return sync_actions
```

---

## 实现示例

### 完整同步管理器

```python
import json
import os
from datetime import datetime
from pathlib import Path

class LunaCloudSync:
    """Luna 云端同步管理器"""
    
    def __init__(self, user_id: str, api_key: str):
        self.user_id = user_id
        self.api_key = api_key
        self.cloud_storage = CloudMapStorage(user_id)
        self.local_loader = LunaMapLoader()
    
    def login(self, username: str, password: str) -> bool:
        """登录账号"""
        # 调用登录API
        auth_result = self._authenticate(username, password)
        
        if auth_result:
            # 保存用户信息
            self._save_user_info(auth_result)
            self.user_id = auth_result["user_id"]
            return True
        
        return False
    
    def sync_all_maps(self) -> dict:
        """同步所有地图"""
        logger.info(f"🔄 开始同步地图：用户 {self.user_id}")
        
        # 增量同步
        sync_actions = incremental_sync(self.user_id, "data/map_cards")
        
        # 统计
        stats = {
            "downloaded": 0,
            "uploaded": 0,
            "skipped": 0
        }
        
        for action in sync_actions:
            if action["action"] == "download":
                stats["downloaded"] += 1
            elif action["action"] == "upload":
                stats["uploaded"] += 1
            elif action["action"] == "skip":
                stats["skipped"] += 1
        
        logger.info(f"✅ 同步完成：下载{stats['downloaded']}个，上传{stats['uploaded']}个，跳过{stats['skipped']}个")
        
        return stats
    
    def backup_all_data(self, backup_path: str):
        """备份所有数据（用于手动备份）"""
        backup_dir = Path(backup_path)
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 备份地图
        maps_backup = backup_dir / "maps"
        maps_backup.mkdir(exist_ok=True)
        # ...复制地图文件
        
        # 备份场景记忆
        scenes_backup = backup_dir / "scenes"
        scenes_backup.mkdir(exist_ok=True)
        # ...复制场景文件
        
        # 备份用户偏好
        with open(backup_dir / "preferences.json", 'w') as f:
            json.dump(self._load_preferences(), f)
        
        logger.info(f"✅ 备份完成：{backup_path}")
    
    def restore_from_backup(self, backup_path: str):
        """从备份恢复数据"""
        backup_dir = Path(backup_path)
        
        # 恢复地图
        # ...
        
        # 恢复场景记忆
        # ...
        
        # 恢复用户偏好
        # ...
        
        logger.info(f"✅ 恢复完成：从 {backup_path}")
    
    def get_sync_status(self) -> dict:
        """获取同步状态"""
        return {
            "last_sync": self._get_last_sync_time(),
            "total_maps_cloud": len(self.cloud_storage.list_user_maps()),
            "total_maps_local": len(self.local_loader.list_available_maps()),
            "last_device": self._get_last_device()
        }
```

---

## 使用流程

### 场景1：新设备初始化

```python
# 1. 登录账号
sync_manager = LunaCloudSync(None, None)
if sync_manager.login("张三", "password"):
    print("✅ 登录成功")
    
    # 2. 下载所有地图
    sync_stats = sync_manager.sync_all_maps()
    
    # 3. 验证地图
    loader = LunaMapLoader()
    downloaded_maps = loader.list_available_maps()
    print(f"📥 已下载{len(downloaded_maps)}个地图")
```

### 场景2：日常同步

```python
# 定期同步（例如：每小时）
def periodic_sync():
    sync_manager = LunaCloudSync(user_id, api_key)
    stats = sync_manager.sync_all_maps()
    
    # 记录同步日志
    sync_manager.log_sync_event(stats)

# 设置定时任务
schedule.every(1).hours.do(periodic_sync)
```

### 场景3：手动备份

```python
# 导出所有数据
sync_manager = LunaCloudSync(user_id, api_key)
backup_path = f"backup/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
sync_manager.backup_all_data(backup_path)

# 导入到新设备
new_sync_manager = LunaCloudSync(new_user_id, new_api_key)
new_sync_manager.restore_from_backup(backup_path)
```

---

## 总结

通过云端同步方案，用户可以：

1. ✅ **无缝切换设备**：登录后自动下载所有地图记忆
2. ✅ **数据安全**：云端备份，不丢失
3. ✅ **增量同步**：只同步更改，节省流量
4. ✅ **跨平台使用**：Mac、RV1126、云端都可访问
5. ✅ **版本控制**：自动处理冲突
6. ✅ **离线备份**：支持本地备份和恢复

**核心价值**：记忆跟随用户，而非设备！


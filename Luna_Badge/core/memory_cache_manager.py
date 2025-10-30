#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna 记忆缓存管理器
支持用户端缓存管理和t+1上传机制
"""

import json
import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib

logger = logging.getLogger(__name__)


class MemoryCacheManager:
    """记忆缓存管理器"""
    
    def __init__(self, cache_dir: str = "data/cache"):
        """初始化缓存管理器"""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 缓存文件
        self.maps_cache_file = self.cache_dir / "maps_cache.json"
        self.scenes_cache_file = self.cache_dir / "scenes_cache.json"
        self.user_behavior_cache_file = self.cache_dir / "user_behavior_cache.json"
        self.upload_queue_file = self.cache_dir / "upload_queue.json"
        self.last_upload_file = self.cache_dir / "last_upload.json"
        
        # 初始化缓存
        self._init_cache()
        
        logger.info("💾 记忆缓存管理器初始化完成")
    
    def _init_cache(self):
        """初始化缓存文件"""
        if not self.maps_cache_file.exists():
            self._save_cache(self.maps_cache_file, {"maps": [], "last_update": None})
        
        if not self.scenes_cache_file.exists():
            self._save_cache(self.scenes_cache_file, {"scenes": [], "last_update": None})
        
        if not self.user_behavior_cache_file.exists():
            self._save_cache(self.user_behavior_cache_file, {
                "behaviors": [],
                "preferences": {},
                "habits": {},
                "last_update": None
            })
        
        if not self.upload_queue_file.exists():
            self._save_cache(self.upload_queue_file, {"queue": [], "last_check": None})
        
        if not self.last_upload_file.exists():
            self._save_cache(self.last_upload_file, {
                "last_upload_time": None,
                "upload_count": 0
            })
    
    def cache_map(self, map_data: Dict, metadata: Optional[Dict] = None) -> bool:
        """缓存地图数据
        
        Args:
            map_data: 地图数据
            metadata: 元数据
            
        Returns:
            是否成功
        """
        try:
            cache_data = self._load_cache(self.maps_cache_file)
            
            # 检查是否已存在
            map_id = map_data.get("map_id") or map_data.get("path_id")
            existing_maps = [m for m in cache_data.get("maps", []) if m.get("map_id") == map_id]
            
            if existing_maps:
                # 更新现有记录
                index = cache_data["maps"].index(existing_maps[0])
                cache_data["maps"][index] = {
                    "map_id": map_id,
                    "map_data": map_data,
                    "metadata": metadata,
                    "cached_at": datetime.now().isoformat(),
                    "uploaded": False
                }
            else:
                # 添加新记录
                cache_data["maps"].append({
                    "map_id": map_id,
                    "map_data": map_data,
                    "metadata": metadata,
                    "cached_at": datetime.now().isoformat(),
                    "uploaded": False
                })
            
            cache_data["last_update"] = datetime.now().isoformat()
            self._save_cache(self.maps_cache_file, cache_data)
            
            # 添加到上传队列
            self._add_to_upload_queue("map", map_id)
            
            logger.info(f"✅ 地图已缓存：{map_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 缓存地图失败：{e}")
            return False
    
    def cache_scene(self, scene_data: Dict) -> bool:
        """缓存场景记忆
        
        Args:
            scene_data: 场景数据
            
        Returns:
            是否成功
        """
        try:
            cache_data = self._load_cache(self.scenes_cache_file)
            
            scene_id = scene_data.get("scene_id") or f"scene_{int(time.time())}"
            
            cache_data["scenes"].append({
                "scene_id": scene_id,
                "scene_data": scene_data,
                "cached_at": datetime.now().isoformat(),
                "uploaded": False
            })
            
            cache_data["last_update"] = datetime.now().isoformat()
            self._save_cache(self.scenes_cache_file, cache_data)
            
            # 添加到上传队列
            self._add_to_upload_queue("scene", scene_id)
            
            logger.info(f"✅ 场景已缓存：{scene_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 缓存场景失败：{e}")
            return False
    
    def cache_user_behavior(self, behavior_type: str, behavior_data: Dict) -> bool:
        """缓存用户行为数据
        
        Args:
            behavior_type: 行为类型（navigation, voice, preference等）
            behavior_data: 行为数据
            
        Returns:
            是否成功
        """
        try:
            cache_data = self._load_cache(self.user_behavior_cache_file)
            
            behavior_id = f"{behavior_type}_{int(time.time())}"
            
            cache_data["behaviors"].append({
                "behavior_id": behavior_id,
                "behavior_type": behavior_type,
                "behavior_data": behavior_data,
                "timestamp": datetime.now().isoformat(),
                "cached_at": datetime.now().isoformat(),
                "uploaded": False
            })
            
            # 如果超过1000条行为记录，只保留最近1000条
            if len(cache_data["behaviors"]) > 1000:
                cache_data["behaviors"] = cache_data["behaviors"][-1000:]
            
            cache_data["last_update"] = datetime.now().isoformat()
            self._save_cache(self.user_behavior_cache_file, cache_data)
            
            # 添加到上传队列
            self._add_to_upload_queue("behavior", behavior_id)
            
            logger.debug(f"✅ 用户行为已缓存：{behavior_type}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 缓存用户行为失败：{e}")
            return False
    
    def update_user_preferences(self, preferences: Dict) -> bool:
        """更新用户偏好设置
        
        Args:
            preferences: 偏好设置
            
        Returns:
            是否成功
        """
        try:
            cache_data = self._load_cache(self.user_behavior_cache_file)
            
            # 合并偏好设置
            if "preferences" not in cache_data:
                cache_data["preferences"] = {}
            
            cache_data["preferences"].update(preferences)
            cache_data["last_update"] = datetime.now().isoformat()
            
            self._save_cache(self.user_behavior_cache_file, cache_data)
            
            # 标记偏好需要上传
            self._add_to_upload_queue("preference", "all")
            
            logger.info("✅ 用户偏好已更新")
            return True
            
        except Exception as e:
            logger.error(f"❌ 更新用户偏好失败：{e}")
            return False
    
    def record_navigation_event(self, event_type: str, data: Dict) -> bool:
        """记录导航事件
        
        Args:
            event_type: 事件类型
            data: 事件数据
            
        Returns:
            是否成功
        """
        event_data = {
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        return self.cache_user_behavior("navigation", event_data)
    
    def record_voice_interaction(self, interaction_type: str, data: Dict) -> bool:
        """记录语音交互
        
        Args:
            interaction_type: 交互类型
            data: 交互数据
            
        Returns:
            是否成功
        """
        interaction_data = {
            "interaction_type": interaction_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        return self.cache_user_behavior("voice", interaction_data)
    
    def get_cache_stats(self) -> Dict:
        """获取缓存统计信息
        
        Returns:
            统计信息字典
        """
        maps_cache = self._load_cache(self.maps_cache_file)
        scenes_cache = self._load_cache(self.scenes_cache_file)
        behavior_cache = self._load_cache(self.user_behavior_cache_file)
        upload_queue = self._load_cache(self.upload_queue_file)
        last_upload = self._load_cache(self.last_upload_file)
        
        stats = {
            "total_maps": len(maps_cache.get("maps", [])),
            "unuploaded_maps": len([m for m in maps_cache.get("maps", []) if not m.get("uploaded")]),
            "total_scenes": len(scenes_cache.get("scenes", [])),
            "unuploaded_scenes": len([s for s in scenes_cache.get("scenes", []) if not s.get("uploaded")]),
            "total_behaviors": len(behavior_cache.get("behaviors", [])),
            "unuploaded_behaviors": len([b for b in behavior_cache.get("behaviors", []) if not b.get("uploaded")]),
            "upload_queue_size": len(upload_queue.get("queue", [])),
            "last_upload_time": last_upload.get("last_upload_time"),
            "upload_count": last_upload.get("upload_count", 0),
            "cache_size_kb": self._calculate_cache_size()
        }
        
        return stats
    
    def _calculate_cache_size(self) -> float:
        """计算缓存大小（KB）"""
        total_size = 0
        
        for file_path in [
            self.maps_cache_file,
            self.scenes_cache_file,
            self.user_behavior_cache_file,
            self.upload_queue_file
        ]:
            if file_path.exists():
                total_size += file_path.stat().st_size
        
        return round(total_size / 1024, 2)
    
    def _add_to_upload_queue(self, data_type: str, data_id: str):
        """添加到上传队列
        
        Args:
            data_type: 数据类型
            data_id: 数据ID
        """
        queue_data = self._load_cache(self.upload_queue_file)
        
        # 检查是否已在队列中
        existing = [q for q in queue_data.get("queue", []) 
                   if q.get("data_type") == data_type and q.get("data_id") == data_id]
        
        if not existing:
            queue_data["queue"].append({
                "data_type": data_type,
                "data_id": data_id,
                "added_at": datetime.now().isoformat(),
                "retry_count": 0
            })
            
            queue_data["last_check"] = datetime.now().isoformat()
            self._save_cache(self.upload_queue_file, queue_data)
    
    def get_upload_queue(self) -> List[Dict]:
        """获取上传队列
        
        Returns:
            上传队列列表
        """
        queue_data = self._load_cache(self.upload_queue_file)
        return queue_data.get("queue", [])
    
    def clear_cache(self, confirm: bool = False) -> bool:
        """清空缓存（谨慎使用）
        
        Args:
            confirm: 确认标志
            
        Returns:
            是否成功
        """
        if not confirm:
            logger.warning("⚠️ 请确认是否要清空缓存")
            return False
        
        try:
            self._init_cache()
            logger.info("✅ 缓存已清空")
            return True
        except Exception as e:
            logger.error(f"❌ 清空缓存失败：{e}")
            return False
    
    def _load_cache(self, file_path: Path) -> Dict:
        """加载缓存数据"""
        if not file_path.exists():
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ 加载缓存失败 {file_path}: {e}")
            return {}
    
    def _save_cache(self, file_path: Path, data: Dict):
        """保存缓存数据"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"❌ 保存缓存失败 {file_path}: {e}")
    
    def export_cache_for_upload(self) -> Dict:
        """导出需要上传的缓存数据
        
        Returns:
            准备上传的数据包
        """
        maps_cache = self._load_cache(self.maps_cache_file)
        scenes_cache = self._load_cache(self.scenes_cache_file)
        behavior_cache = self._load_cache(self.user_behavior_cache_file)
        
        # 筛选未上传的数据
        unuploaded_maps = [m for m in maps_cache.get("maps", []) if not m.get("uploaded")]
        unuploaded_scenes = [s for s in scenes_cache.get("scenes", []) if not s.get("uploaded")]
        unuploaded_behaviors = [b for b in behavior_cache.get("behaviors", []) if not b.get("uploaded")]
        
        upload_package = {
            "timestamp": datetime.now().isoformat(),
            "maps": [m["map_data"] for m in unuploaded_maps],
            "scenes": [s["scene_data"] for s in unuploaded_scenes],
            "behaviors": [b["behavior_data"] for b in unuploaded_behaviors],
            "preferences": behavior_cache.get("preferences", {}),
            "metadata": {
                "maps_count": len(unuploaded_maps),
                "scenes_count": len(unuploaded_scenes),
                "behaviors_count": len(unuploaded_behaviors)
            }
        }
        
        return upload_package
    
    def mark_as_uploaded(self, data_type: str, data_id: str):
        """标记数据已上传
        
        Args:
            data_type: 数据类型
            data_id: 数据ID
        """
        if data_type == "map":
            cache_file = self.maps_cache_file
        elif data_type == "scene":
            cache_file = self.scenes_cache_file
        elif data_type == "behavior":
            cache_file = self.user_behavior_cache_file
        else:
            return
        
        cache_data = self._load_cache(cache_file)
        
        # 更新上传状态
        for item in cache_data.get("maps" if data_type == "map" else "scenes" if data_type == "scene" else "behaviors", []):
            if item.get("map_id" if data_type == "map" else "scene_id" if data_type == "scene" else "behavior_id") == data_id:
                item["uploaded"] = True
                item["uploaded_at"] = datetime.now().isoformat()
                break
        
        self._save_cache(cache_file, cache_data)
        
        # 从上传队列中移除
        queue_data = self._load_cache(self.upload_queue_file)
        queue_data["queue"] = [q for q in queue_data.get("queue", []) 
                              if not (q.get("data_type") == data_type and q.get("data_id") == data_id)]
        self._save_cache(self.upload_queue_file, queue_data)


# 测试函数
if __name__ == "__main__":
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 初始化缓存管理器
    cache_manager = MemoryCacheManager()
    
    # 测试地图缓存
    print("=" * 60)
    print("🗺️ 测试地图缓存")
    print("=" * 60)
    test_map = {
        "map_id": "test_map_001",
        "path_name": "测试路径",
        "nodes": []
    }
    cache_manager.cache_map(test_map)
    
    # 测试场景缓存
    print("\n🏞️ 测试场景缓存")
    print("=" * 60)
    test_scene = {
        "scene_id": "scene_001",
        "location": "虹口医院",
        "caption": "医院入口"
    }
    cache_manager.cache_scene(test_scene)
    
    # 测试用户行为缓存
    print("\n👤 测试用户行为缓存")
    print("=" * 60)
    cache_manager.record_navigation_event("start_navigation", {
        "destination": "虹口医院",
        "route_type": "walking"
    })
    
    cache_manager.record_voice_interaction("voice_command", {
        "command": "导航到虹口医院",
        "result": "success"
    })
    
    # 测试用户偏好
    print("\n⚙️ 测试用户偏好")
    print("=" * 60)
    cache_manager.update_user_preferences({
        "voice_speed": "normal",
        "prefer_walk": True
    })
    
    # 显示统计信息
    print("\n📊 缓存统计")
    print("=" * 60)
    stats = cache_manager.get_cache_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    # 导出上传数据包
    print("\n📦 导出上传数据包")
    print("=" * 60)
    upload_package = cache_manager.export_cache_for_upload()
    print(f"数据包大小：{json.dumps(upload_package).__len__()} 字节")
    print(f"包含 {upload_package['metadata']['maps_count']} 个地图")
    print(f"包含 {upload_package['metadata']['scenes_count']} 个场景")
    print(f"包含 {upload_package['metadata']['behaviors_count']} 个行为记录")


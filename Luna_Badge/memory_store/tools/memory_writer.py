#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 记忆写入器
记录用户在地图中的路径、节点、情绪印象和操作行为
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import os

logger = logging.getLogger(__name__)


class MemoryWriter:
    """记忆写入器"""
    
    def __init__(self, user_id: str = None, storage_dir: str = "memory_store/local_memory"):
        """初始化记忆写入器
        
        Args:
            user_id: 用户ID
            storage_dir: 存储目录
        """
        self.user_id = user_id or self._get_default_user_id()
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📝 记忆写入器初始化：用户 {self.user_id}")
    
    def _get_default_user_id(self) -> str:
        """获取默认用户ID"""
        # 尝试从配置文件读取
        config_file = Path("config/user_config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get("user_id", "anonymous")
            except:
                pass
        
        return "anonymous"
    
    def write_user_memory(self, 
                          map_data: Dict, 
                          app_behavior: Dict,
                          date: Optional[str] = None) -> bool:
        """记录用户记忆
        
        Args:
            map_data: 地图数据
            app_behavior: 应用行为数据
            date: 日期（默认为今天）
            
        Returns:
            是否成功
        """
        try:
            # 使用指定日期或今天
            date_str = date or datetime.now().strftime("%Y-%m-%d")
            
            # 构建记忆数据
            memory_data = {
                "user_id": self.user_id,
                "date": date_str,
                "maps": map_data if isinstance(map_data, list) else [map_data],
                "app_behavior": app_behavior,
                "created_at": datetime.now().isoformat()
            }
            
            # 生成文件名
            filename = f"{date_str}_{self.user_id}_memory.json"
            filepath = self.storage_dir / filename
            
            # 如果文件已存在，合并数据
            if filepath.exists():
                memory_data = self._merge_existing_memory(filepath, memory_data)
            
            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 记忆已写入：{filename}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 写入记忆失败：{e}")
            return False
    
    def _merge_existing_memory(self, filepath: Path, new_data: Dict) -> Dict:
        """合并现有记忆数据
        
        Args:
            filepath: 现有文件路径
            new_data: 新数据
            
        Returns:
            合并后的数据
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            
            # 合并地图数据
            existing_maps = existing_data.get("maps", [])
            new_maps = new_data.get("maps", [])
            
            # 将新地图添加到现有列表
            existing_maps.extend(new_maps)
            
            existing_data["maps"] = existing_maps
            
            # 合并应用行为
            existing_behavior = existing_data.get("app_behavior", {})
            new_behavior = new_data.get("app_behavior", {})
            
            # 合并计数型行为（累加）
            for key, value in new_behavior.items():
                if isinstance(value, (int, float)):
                    existing_behavior[key] = existing_behavior.get(key, 0) + value
                elif isinstance(value, bool):
                    existing_behavior[key] = value or existing_behavior.get(key, False)
                else:
                    existing_behavior[key] = value
            
            existing_data["app_behavior"] = existing_behavior
            
            # 更新创建时间
            existing_data["updated_at"] = datetime.now().isoformat()
            
            return existing_data
            
        except Exception as e:
            logger.error(f"❌ 合并记忆失败：{e}")
            return new_data
    
    def record_map_visit(self,
                        map_id: str,
                        nodes_visited: List[str],
                        emotion_tags: Dict[str, str] = None,
                        duration_minutes: float = 0,
                        path: List[str] = None,
                        date: Optional[str] = None) -> bool:
        """记录地图访问
        
        Args:
            map_id: 地图ID
            nodes_visited: 访问的节点列表
            emotion_tags: 情绪标签
            duration_minutes: 持续时间（分钟）
            path: 路径
            date: 指定日期（默认为今天）
            
        Returns:
            是否成功
        """
        map_data = {
            "map_id": map_id,
            "nodes_visited": nodes_visited,
            "emotion_tags": emotion_tags or {},
            "duration_minutes": duration_minutes,
            "path": path or []
        }
        
        app_behavior = {
            "asked_for_guidance": False,
            "used_voice_input": False,
            "requested_nearby_toilet": 0
        }
        
        return self.write_user_memory(map_data, app_behavior, date=date)
    
    def record_app_behavior(self, behavior_type: str, behavior_data: Dict = None) -> bool:
        """记录应用行为
        
        Args:
            behavior_type: 行为类型
            behavior_data: 行为数据
            
        Returns:
            是否成功
        """
        # 获取现有数据或创建新数据
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}_{self.user_id}_memory.json"
        filepath = self.storage_dir / filename
        
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
        else:
            memory_data = {
                "user_id": self.user_id,
                "date": date_str,
                "maps": [],
                "app_behavior": {}
            }
        
        # 更新行为数据
        if behavior_type == "asked_for_guidance":
            memory_data["app_behavior"]["asked_for_guidance"] = True
        elif behavior_type == "used_voice_input":
            memory_data["app_behavior"]["used_voice_input"] = True
        elif behavior_type == "requested_nearby_toilet":
            memory_data["app_behavior"]["requested_nearby_toilet"] = \
                memory_data["app_behavior"].get("requested_nearby_toilet", 0) + 1
        
        if behavior_data:
            memory_data["app_behavior"].update(behavior_data)
        
        # 保存
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ 行为已记录：{behavior_type}")
        return True


# 测试函数
if __name__ == "__main__":
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 初始化写入器
    writer = MemoryWriter(user_id="user_123")
    
    # 测试地图访问记录
    print("=" * 60)
    print("🗺️ 测试地图访问记录")
    print("=" * 60)
    
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
    
    # 测试应用行为记录
    print("\n📱 测试应用行为记录")
    print("=" * 60)
    
    writer.record_app_behavior("asked_for_guidance")
    writer.record_app_behavior("used_voice_input")
    writer.record_app_behavior("requested_nearby_toilet")
    writer.record_app_behavior("requested_nearby_toilet")
    
    # 读取并显示
    print("\n📖 读取记忆数据")
    print("=" * 60)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_user_123_memory.json"
    filepath = writer.storage_dir / filename
    
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            memory = json.load(f)
        print(json.dumps(memory, indent=2, ensure_ascii=False))



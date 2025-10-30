#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna 地图卡片加载器
用于跨设备分享和快速解析地图数据
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image
import re

logger = logging.getLogger(__name__)


class LunaMapLoader:
    """Luna 地图卡片加载器"""
    
    def __init__(self, map_dir: str = "data/map_cards"):
        """初始化加载器"""
        self.map_dir = Path(map_dir)
        self.map_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🗺️ 地图加载器初始化：{self.map_dir}")
    
    def load_map_card(self, map_id: str) -> Optional[Dict]:
        """加载地图卡片（图像+元数据）
        
        Args:
            map_id: 地图ID
            
        Returns:
            包含图像和元数据的字典，失败返回None
        """
        try:
            # 加载图像
            image_path = self.map_dir / f"{map_id}_emotional.png"
            image = Image.open(image_path) if image_path.exists() else None
            
            # 加载元数据
            meta_path = self.map_dir / f"{map_id}_emotional.meta.json"
            metadata = json.loads(meta_path.read_text(encoding='utf-8')) if meta_path.exists() else None
            
            if not metadata:
                logger.warning(f"⚠️ 地图元数据不存在：{map_id}")
                return None
            
            logger.info(f"✅ 地图卡片加载成功：{map_id}")
            
            return {
                "image": image,
                "metadata": metadata
            }
        except Exception as e:
            logger.error(f"❌ 加载地图失败：{e}")
            return None
    
    def load_path_data(self, path_id: str) -> Optional[Dict]:
        """加载原始路径数据
        
        Args:
            path_id: 路径ID
            
        Returns:
            路径数据字典，失败返回None
        """
        # 查找包含该路径的数据文件
        for json_file in self.map_dir.glob("*.json"):
            if json_file.stem.endswith("_meta"):
                continue
            
            try:
                data = json.loads(json_file.read_text(encoding='utf-8'))
                # 检查是否包含路径
                if "paths" in data:
                    for path in data["paths"]:
                        if path.get("path_id") == path_id:
                            logger.info(f"✅ 路径数据加载成功：{path_id}")
                            return path
            except Exception as e:
                logger.debug(f"解析文件失败：{json_file} - {e}")
                continue
        
        logger.warning(f"⚠️ 路径数据不存在：{path_id}")
        return None
    
    def parse_map_for_voice(self, metadata: Dict) -> str:
        """解析元数据生成语音提示
        
        Args:
            metadata: 地图元数据
            
        Returns:
            语音提示文本
        """
        if not metadata:
            return "无法解析地图信息"
        
        path_name = metadata.get("path_name", "未知路径")
        node_count = metadata.get("node_count", 0)
        total_distance = metadata.get("total_distance", "未知距离")
        regions = metadata.get("regions_detected", [])
        
        voice_text = f"导航路径：{path_name}，共{node_count}个节点，"
        voice_text += f"总距离{total_distance}，"
        
        if regions:
            voice_text += f"途经区域：{', '.join(regions)}"
        
        return voice_text
    
    def extract_navigation_sequence(self, path_data: Dict) -> List[Dict]:
        """提取导航序列
        
        Args:
            path_data: 路径数据
            
        Returns:
            导航序列列表
        """
        if not path_data or "nodes" not in path_data:
            return []
        
        sequence = []
        nodes = path_data["nodes"]
        
        for i, node in enumerate(nodes):
            label = node.get("label", f"节点{i+1}")
            distance = node.get("distance", 0)
            movement = node.get("movement", "walking")
            node_type = node.get("type", "")
            level = node.get("level", "")
            emotion = node.get("emotion", [])
            
            # 构建步骤描述
            movement_desc = self._get_movement_description(movement)
            
            step_info = {
                "step": i + 1,
                "action": movement_desc,
                "target": label,
                "type": node_type,
                "distance": distance,
                "level": level,
                "emotion": emotion
            }
            
            sequence.append(step_info)
        
        logger.info(f"✅ 导航序列已提取：{len(sequence)}个步骤")
        return sequence
    
    def _get_movement_description(self, movement: str) -> str:
        """获取移动方式描述"""
        movement_map = {
            "walking": "步行前往",
            "elevator": "乘电梯前往",
            "stairs": "通过楼梯前往",
            "bus": "乘公交车前往"
        }
        return movement_map.get(movement, "前往")
    
    def check_compatibility(self, metadata: Dict) -> bool:
        """检查版本兼容性
        
        Args:
            metadata: 地图元数据
            
        Returns:
            是否兼容
        """
        version = metadata.get("version", "0.9")
        
        # 支持的版本
        supported_versions = ["1.0", "1.1"]
        
        is_compatible = version in supported_versions
        
        if not is_compatible:
            logger.warning(f"⚠️ 地图版本不兼容：{version}")
        
        return is_compatible
    
    def validate_map_data(self, data: Dict) -> bool:
        """验证地图数据完整性
        
        Args:
            data: 地图数据
            
        Returns:
            是否有效
        """
        required_fields = ["path_id", "path_name"]
        
        for field in required_fields:
            if field not in data:
                logger.error(f"❌ 缺少必要字段：{field}")
                return False
        
        # 验证节点数据
        if "nodes" in data:
            for i, node in enumerate(data["nodes"]):
                if "node_id" not in node or "label" not in node:
                    logger.error(f"❌ 节点{i+1}数据不完整")
                    return False
        
        logger.info("✅ 地图数据验证通过")
        return True
    
    def safe_load_map(self, map_id: str) -> Optional[Dict]:
        """安全加载地图
        
        Args:
            map_id: 地图ID
            
        Returns:
            地图数据，失败返回None
        """
        try:
            map_card = self.load_map_card(map_id)
            
            if not map_card:
                return None
            
            # 验证
            metadata = map_card.get("metadata")
            if metadata and not self.validate_map_data(metadata):
                logger.error(f"❌ 地图数据不完整：{map_id}")
                return None
            
            # 检查兼容性
            if metadata and not self.check_compatibility(metadata):
                logger.error(f"❌ 地图版本不兼容：{map_id}")
                return None
            
            return map_card
        except FileNotFoundError as e:
            logger.error(f"❌ 地图文件不存在：{map_id}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"❌ 地图元数据解析失败：{map_id}")
            return None
        except Exception as e:
            logger.error(f"❌ 加载地图失败：{e}")
            return None
    
    def list_available_maps(self) -> List[str]:
        """列出所有可用地图
        
        Returns:
            地图ID列表
        """
        map_ids = set()
        
        # 查找所有元数据文件
        for meta_file in self.map_dir.glob("*_emotional.meta.json"):
            map_id = meta_file.stem.replace("_emotional", "")
            map_ids.add(map_id)
        
        logger.info(f"📋 找到{len(map_ids)}个可用地图")
        return sorted(list(map_ids))
    
    def get_map_summary(self, map_id: str) -> Optional[Dict]:
        """获取地图摘要信息
        
        Args:
            map_id: 地图ID
            
        Returns:
            摘要信息字典
        """
        map_card = self.safe_load_map(map_id)
        
        if not map_card:
            return None
        
        metadata = map_card.get("metadata", {})
        
        summary = {
            "map_id": map_id,
            "path_name": metadata.get("path_name"),
            "node_count": metadata.get("node_count"),
            "total_distance": metadata.get("total_distance"),
            "regions": metadata.get("regions_detected", []),
            "icon_types": metadata.get("icon_types", []),
            "generated_at": metadata.get("generation_timestamp")
        }
        
        return summary


# 测试函数
if __name__ == "__main__":
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 初始化加载器
    loader = LunaMapLoader("data/map_cards")
    
    # 列出所有地图
    print("=" * 60)
    print("📋 可用地图列表")
    print("=" * 60)
    available_maps = loader.list_available_maps()
    for map_id in available_maps:
        print(f"  - {map_id}")
    
    # 加载地图
    if available_maps:
        map_id = available_maps[0]
        print(f"\n🗺️ 加载地图：{map_id}")
        
        map_card = loader.safe_load_map(map_id)
        
        if map_card:
            metadata = map_card.get("metadata", {})
            
            # 显示元数据
            print("\n📊 元数据：")
            print(json.dumps(metadata, indent=2, ensure_ascii=False))
            
            # 生成语音提示
            voice_prompt = loader.parse_map_for_voice(metadata)
            print(f"\n🗣️ 语音提示：{voice_prompt}")
            
            # 加载路径数据
            path_data = loader.load_path_data(metadata.get("path_id"))
            
            # 提取导航序列
            if path_data:
                sequence = loader.extract_navigation_sequence(path_data)
                print("\n🗺️ 导航序列：")
                for step in sequence:
                    emotion_str = f"（{', '.join(step['emotion'])}）" if step['emotion'] else ""
                    print(f"  步骤{step['step']}：{step['action']}{step['target']}{emotion_str}（{step['distance']}米）")
        
        # 获取摘要
        summary = loader.get_map_summary(map_id)
        if summary:
            print("\n📋 地图摘要：")
            print(json.dumps(summary, indent=2, ensure_ascii=False))


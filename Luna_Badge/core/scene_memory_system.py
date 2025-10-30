#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 场景记忆系统
使用节点链式结构+关键节点图像生成手绘地图样式
"""

import json
import os
import cv2
import numpy as np
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class SceneNode:
    """场景节点"""
    node_id: str
    label: str                    # 节点标签（如"305室"）
    image_path: str               # 节点图像路径
    box: List[List[int]] = None   # 边界框坐标
    direction: str = ""           # 方向描述（如"左转前行15米"）
    notes: str = ""               # 备注
    timestamp: str = ""           # 时间戳
    confidence: float = 0.0       # 识别置信度
    node_type: str = "landmark"   # 节点类型: outdoor/walkway/indoor/facility/transit
    layer: str = "default"        # 图层: outdoor/indoor
    distance_meters: float = 0.0  # 距离（米）- 从上一个节点到当前节点
    facility_info: Dict[str, Any] = None  # 公共设施信息
    transit_info: Dict[str, Any] = None   # 公共交通信息
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)

@dataclass
class PathMemory:
    """路径记忆"""
    path_id: str                  # 路径ID
    path_name: str                # 路径名称
    nodes: List[SceneNode]        # 节点列表
    created_at: str = ""          # 创建时间
    updated_at: str = ""          # 更新时间
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "path_id": self.path_id,
            "path_name": self.path_name,
            "nodes": [node.to_dict() for node in self.nodes],
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class NodeDetector:
    """节点检测器 - 使用YOLO+OCR识别关键节点"""
    
    def __init__(self, vision_engine=None):
        """
        初始化节点检测器
        
        Args:
            vision_engine: 视觉OCR引擎实例
        """
        self.vision_engine = vision_engine
        
        # 关键节点关键词
        self.key_node_keywords = [
            # 门牌/房间
            "室", "号", "room", "office", "病房",
            # 电梯/楼梯
            "电梯", "楼梯", "escalator", "stair", "lift", "elevator", "stairs",
            # 出口/起点
            "出口", "入口", "exit", "entrance", "start",
            # 功能区
            "挂号", "收费", "药房", "科室", "检查",
            # 常见标识
            "洗手间", "toilet", "卫生间", "wc", "restroom",
            # 通用地点
            "hallway", "corridor", "hall",
        ]
        
        logger.info("🎯 节点检测器初始化完成")
    
    def detect_nodes(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        检测关键节点
        
        Args:
            image: 输入图像
            
        Returns:
            List[Dict]: 检测到的节点列表
        """
        if not self.vision_engine:
            return []
        
        try:
            # 使用视觉引擎进行识别
            results = self.vision_engine.detect_and_recognize(image)
            
            detected_nodes = []
            
            # 处理OCR识别结果
            for ocr_result in results.get('ocr_results', []):
                text = ocr_result.get('text', '')
                confidence = ocr_result.get('confidence', 0.0)
                box = ocr_result.get('box', [])
                
                # 检查是否包含关键节点关键词
                if self._is_key_node(text):
                    detected_nodes.append({
                        "text": text,
                        "confidence": confidence,
                        "box": box,
                        "type": self._classify_node_type(text)
                    })
            
            return detected_nodes
            
        except Exception as e:
            logger.error(f"❌ 节点检测失败: {e}")
            return []
    
    def _is_key_node(self, text: str) -> bool:
        """
        判断是否为关键节点
        
        Args:
            text: 识别的文本
            
        Returns:
            bool: 是否关键节点
        """
        text = text.lower()
        for keyword in self.key_node_keywords:
            if keyword.lower() in text:
                return True
        return False
    
    def _classify_node_type(self, text: str) -> str:
        """
        分类节点类型
        
        Args:
            text: 节点文本
            
        Returns:
            str: 节点类型
        """
        if any(kw in text for kw in ["室", "号", "room", "office"]):
            return "room"
        elif any(kw in text for kw in ["电梯", "楼梯", "lift", "stair"]):
            return "facility"
        elif any(kw in text for kw in ["出口", "入口", "exit", "entrance"]):
            return "exit"
        elif any(kw in text for kw in ["洗手间", "toilet", "卫生间"]):
            return "restroom"
        elif any(kw in text for kw in ["挂号", "科室", "收费"]):
            return "department"
        else:
            return "landmark"

class ImageCapturer:
    """图像捕获器 - 保存关键节点图像"""
    
    def __init__(self, base_dir: str = "data/scene_images"):
        """
        初始化图像捕获器
        
        Args:
            base_dir: 图像存储基础目录
        """
        self.base_dir = base_dir
        Path(self.base_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"📸 图像捕获器初始化完成 ({base_dir})")
    
    def capture_and_save(self, image: np.ndarray, node_id: str, 
                        box: List[List[int]] = None, path_name: str = "default") -> str:
        """
        捕获并保存节点图像
        
        Args:
            image: 原始图像
            node_id: 节点ID
            box: 边界框坐标（如果为None则保存整张图）
            path_name: 路径名称
            
        Returns:
            str: 保存的图像文件路径
        """
        try:
            # 裁剪图像区域（如果有边界框）
            if box:
                # 提取边界框的最小外接矩形
                box_np = np.array(box)
                x_min, y_min = box_np.min(axis=0)
                x_max, y_max = box_np.max(axis=0)
                
                # 裁剪图像
                captured_img = image[y_min:y_max, x_min:x_max]
            else:
                captured_img = image
            
            # 创建路径目录
            path_dir = os.path.join(self.base_dir, path_name)
            Path(path_dir).mkdir(parents=True, exist_ok=True)
            
            # 保存图像
            image_path = os.path.join(path_dir, f"{node_id}.jpg")
            cv2.imwrite(image_path, captured_img)
            
            logger.info(f"📸 图像已保存: {image_path}")
            return image_path
            
        except Exception as e:
            logger.error(f"❌ 图像保存失败: {e}")
            return ""

class MemoryMapper:
    """记忆映射器 - 构建路径链条结构"""
    
    def __init__(self, store_file: str = "data/scene_memory.json"):
        """
        初始化记忆映射器
        
        Args:
            store_file: 记忆存储文件
        """
        self.store_file = store_file
        self.memories: Dict[str, PathMemory] = {}
        self.load_memories()
        logger.info(f"🗺️ 记忆映射器初始化完成")
    
    def load_memories(self):
        """加载记忆数据"""
        if os.path.exists(self.store_file):
            try:
                with open(self.store_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for path_id, path_data in data.items():
                        nodes = [SceneNode(**node_data) for node_data in path_data.get('nodes', [])]
                        self.memories[path_id] = PathMemory(
                            path_id=path_id,
                            path_name=path_data.get('path_name', ''),
                            nodes=nodes,
                            created_at=path_data.get('created_at', ''),
                            updated_at=path_data.get('updated_at', '')
                        )
                logger.info(f"📂 加载了 {len(self.memories)} 条路径记忆")
            except Exception as e:
                logger.error(f"❌ 加载记忆失败: {e}")
    
    def save_memories(self):
        """保存记忆数据"""
        try:
            data = {path_id: memory.to_dict() for path_id, memory in self.memories.items()}
            with open(self.store_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"💾 记忆已保存")
        except Exception as e:
            logger.error(f"❌ 保存记忆失败: {e}")
    
    def add_path(self, path_id: str, path_name: str) -> bool:
        """
        添加新路径
        
        Args:
            path_id: 路径ID
            path_name: 路径名称
            
        Returns:
            bool: 是否成功
        """
        if path_id in self.memories:
            logger.warning(f"⚠️ 路径 {path_id} 已存在")
            return False
        
        self.memories[path_id] = PathMemory(
            path_id=path_id,
            path_name=path_name,
            nodes=[],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        self.save_memories()
        return True
    
    def add_node(self, path_id: str, node: SceneNode) -> bool:
        """
        添加节点到路径
        
        Args:
            path_id: 路径ID
            node: 场景节点
            
        Returns:
            bool: 是否成功
        """
        if path_id not in self.memories:
            logger.error(f"❌ 路径 {path_id} 不存在")
            return False
        
        self.memories[path_id].nodes.append(node)
        self.memories[path_id].updated_at = datetime.now().isoformat()
        self.save_memories()
        return True
    
    def append_node_to_path(self, path_id: str, node_data: Dict[str, Any], 
                           validate: bool = True) -> bool:
        """
        追加节点到路径（支持断点追加）
        
        Args:
            path_id: 路径ID
            node_data: 节点数据字典
            validate: 是否验证节点有效性
            
        Returns:
            bool: 是否成功
        """
        try:
            if path_id not in self.memories:
                logger.error(f"❌ 路径 {path_id} 不存在")
                return False
            
            # 验证节点数据
            if validate and not self._validate_node_data(node_data):
                logger.warning(f"⚠️ 节点数据验证失败")
                return False
            
            # 创建节点对象
            from core.scene_memory_system import SceneNode
            node = SceneNode(
                node_id=node_data.get("node_id", f"node_{len(self.memories[path_id].nodes) + 1:03d}"),
                label=node_data.get("label", ""),
                image_path=node_data.get("image_path", ""),
                box=node_data.get("box"),
                direction=node_data.get("direction", ""),
                notes=node_data.get("notes", ""),
                timestamp=node_data.get("timestamp", datetime.now().isoformat()),
                confidence=node_data.get("confidence", 0.0)
            )
            
            # 追加节点
            success = self.add_node(path_id, node)
            
            if success:
                logger.info(f"✅ 节点已追加到路径 {path_id}: {node.label}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ 追加节点失败: {e}")
            return False
    
    def _validate_node_data(self, node_data: Dict[str, Any]) -> bool:
        """
        验证节点数据有效性
        
        Args:
            node_data: 节点数据
            
        Returns:
            bool: 是否有效
        """
        required_fields = ["label", "image_path"]
        
        for field in required_fields:
            if field not in node_data or not node_data[field]:
                logger.warning(f"⚠️ 缺少必需字段: {field}")
                return False
        
        return True
    
    def get_path_statistics(self, path_id: str) -> Dict[str, Any]:
        """
        获取路径统计信息
        
        Args:
            path_id: 路径ID
            
        Returns:
            Dict: 统计信息
        """
        if path_id not in self.memories:
            return {}
        
        path_memory = self.memories[path_id]
        nodes = path_memory.nodes
        
        # 统计节点类型
        node_types = {}
        for node in nodes:
            node_type = self._classify_node_type(node.label)
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        # 计算时间跨度
        if len(nodes) > 0:
            first_time = nodes[0].timestamp
            last_time = nodes[-1].timestamp
        else:
            first_time = last_time = None
        
        return {
            "path_id": path_id,
            "path_name": path_memory.path_name,
            "total_nodes": len(nodes),
            "node_types": node_types,
            "created_at": path_memory.created_at,
            "updated_at": path_memory.updated_at,
            "first_node_time": first_time,
            "last_node_time": last_time
        }
    
    def _classify_node_type(self, label: str) -> str:
        """分类节点类型（复用NodeDetector的逻辑）"""
        label_lower = label.lower()
        
        if any(kw in label_lower for kw in ["room", "室", "office"]):
            return "room"
        elif any(kw in label_lower for kw in ["elevator", "电梯", "lift", "stair"]):
            return "facility"
        elif any(kw in label_lower for kw in ["exit", "出口", "entrance", "入口"]):
            return "exit"
        elif any(kw in label_lower for kw in ["toilet", "洗手间", "卫生间"]):
            return "restroom"
        else:
            return "landmark"
    
    def get_path(self, path_id: str) -> Optional[PathMemory]:
        """获取路径记忆"""
        return self.memories.get(path_id)
    
    def list_paths(self) -> List[str]:
        """列出所有路径ID"""
        return list(self.memories.keys())

class SceneMemorySystem:
    """场景记忆系统 - 主控制器"""
    
    def __init__(self):
        """初始化场景记忆系统"""
        from core.vision_ocr_engine import get_vision_ocr_engine
        
        # 初始化各组件
        self.vision_engine = get_vision_ocr_engine()
        self.node_detector = NodeDetector(self.vision_engine)
        self.image_capturer = ImageCapturer()
        self.memory_mapper = MemoryMapper()
        
        logger.info("🗺️ 场景记忆系统初始化完成")
    
    def record_node(self, image: np.ndarray, path_id: str = "current", 
                   path_name: str = "未命名路径") -> bool:
        """
        记录当前场景节点
        
        Args:
            image: 当前图像
            path_id: 路径ID
            path_name: 路径名称
            
        Returns:
            bool: 是否成功
        """
        try:
            # 如果路径不存在，创建路径
            if path_id not in self.memory_mapper.list_paths():
                self.memory_mapper.add_path(path_id, path_name)
            
            # 检测关键节点
            detected_nodes = self.node_detector.detect_nodes(image)
            
            if not detected_nodes:
                logger.warning("⚠️ 未检测到关键节点")
                return False
            
            # 保存第一个检测到的节点
            node = detected_nodes[0]
            
            # 生成节点ID
            node_count = len(self.memory_mapper.get_path(path_id).nodes)
            node_id = f"node_{node_count + 1:03d}"
            
            # 保存节点图像
            image_path = self.image_capturer.capture_and_save(
                image, node_id, node.get('box'), path_name
            )
            
            if not image_path:
                logger.error("❌ 图像保存失败")
                return False
            
            # 创建场景节点
            scene_node = SceneNode(
                node_id=node_id,
                label=node['text'],
                image_path=image_path,
                box=node['box'],
                confidence=node['confidence'],
                timestamp=datetime.now().isoformat()
            )
            
            # 添加到记忆
            success = self.memory_mapper.add_node(path_id, scene_node)
            
            if success:
                logger.info(f"✅ 节点已记录: {node['text']}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ 记录节点失败: {e}")
            return False
    
    def get_path_memory(self, path_id: str) -> Optional[PathMemory]:
        """获取路径记忆"""
        return self.memory_mapper.get_path(path_id)


# 全局实例
_scene_memory_system = None

def get_scene_memory_system() -> SceneMemorySystem:
    """获取全局场景记忆系统实例"""
    global _scene_memory_system
    if _scene_memory_system is None:
        _scene_memory_system = SceneMemorySystem()
    return _scene_memory_system


if __name__ == "__main__":
    # 测试场景记忆系统
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("🗺️ 场景记忆系统测试")
    print("=" * 60)
    
    system = SceneMemorySystem()
    
    # 测试记录节点
    print("\n测试记录节点...")
    test_image = np.ones((480, 640, 3), dtype=np.uint8) * 255
    # 添加测试文字
    import cv2
    cv2.putText(test_image, "305室", (50, 100), 
               cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
    
    success = system.record_node(test_image, "test_path", "测试路径")
    print(f"记录结果: {'✅成功' if success else '❌失败'}")
    
    # 获取路径
    path_memory = system.get_path_memory("test_path")
    if path_memory:
        print(f"\n路径: {path_memory.path_name}")
        print(f"节点数量: {len(path_memory.nodes)}")
        for node in path_memory.nodes:
            print(f"  - {node.label} ({node.node_id})")
    
    print("\n" + "=" * 60)

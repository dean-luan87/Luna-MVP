#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4 - 任务图加载器
从 .json 文件加载标准任务图对象
"""

import json
import logging
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class TaskGraph:
    """任务图数据结构"""
    graph_id: str
    scene: str
    goal: str
    nodes: List[Dict[str, Any]]
    edges: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None
    name: Optional[str] = None           # 可选的名称字段（兼容旧格式）
    description: Optional[str] = None    # 可选的描述字段（兼容旧格式）
    
    def __post_init__(self):
        if self.edges is None:
            self.edges = []
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    def to_json(self, file_path: str):
        """保存为JSON文件"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
            logger.info(f"✅ 任务图已保存: {file_path}")
        except Exception as e:
            logger.error(f"❌ 保存任务图失败: {e}")
            raise

class TaskGraphLoader:
    """任务图加载器"""
    
    def __init__(self, base_path: str = "task_graphs"):
        """
        初始化任务图加载器
        
        Args:
            base_path: 任务图文件基础路径
        """
        self.base_path = base_path
        self.logger = logging.getLogger("TaskGraphLoader")
    
    def load_from_file(self, file_path: str) -> TaskGraph:
        """
        从文件加载任务图
        
        Args:
            file_path: JSON文件路径（相对或绝对）
            
        Returns:
            TaskGraph: 任务图对象
        """
        try:
            # 处理相对路径
            if not os.path.isabs(file_path):
                full_path = os.path.join(self.base_path, file_path)
            else:
                full_path = file_path
            
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"任务图文件不存在: {full_path}")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 校验字段完整性
            self._validate_graph_data(data)
            
            # 创建任务图对象
            task_graph = TaskGraph(
                graph_id=data["graph_id"],
                scene=data.get("scene_type") or data.get("scene"),  # 兼容新旧格式
                goal=data["goal"],
                nodes=data["nodes"],
                edges=data.get("edges", []),
                metadata=data.get("metadata", {}),
                name=data.get("name"),  # 兼容旧格式
                description=data.get("description")  # 兼容旧格式
            )
            
            self.logger.info(f"✅ 任务图加载成功: {task_graph.graph_id} (场景: {task_graph.scene})")
            return task_graph
            
        except Exception as e:
            self.logger.error(f"❌ 加载任务图失败: {file_path}: {e}")
            raise
    
    def load_from_api(self, graph_id: str, api_url: str = "https://api.luna.ai/task/graph") -> Optional[TaskGraph]:
        """
        从API获取任务图（预留接口）
        
        Args:
            graph_id: 任务图ID
            api_url: API地址
            
        Returns:
            TaskGraph: 任务图对象，失败返回None
        """
        try:
            import requests
            
            response = requests.get(f"{api_url}/{graph_id}", timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self._validate_graph_data(data)
            
            task_graph = TaskGraph(
                graph_id=data["graph_id"],
                scene=data["scene"],
                goal=data["goal"],
                nodes=data["nodes"],
                edges=data.get("edges", []),
                metadata=data.get("metadata", {})
            )
            
            self.logger.info(f"✅ 从API加载任务图成功: {graph_id}")
            return task_graph
            
        except ImportError:
            self.logger.warning("⚠️ requests库未安装，无法从API加载")
            return None
        except Exception as e:
            self.logger.error(f"❌ 从API加载任务图失败: {graph_id}: {e}")
            return None
    
    def save_to_file(self, task_graph: TaskGraph, file_path: str):
        """
        保存任务图到文件
        
        Args:
            task_graph: 任务图对象
            file_path: 保存路径
        """
        task_graph.to_json(file_path)
    
    def _validate_graph_data(self, data: Dict[str, Any]):
        """
        校验任务图数据完整性
        
        Args:
            data: 任务图数据
            
        Raises:
            ValueError: 数据不完整或格式错误
        """
        required_fields = ["graph_id", "goal", "nodes"]
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"缺少必需字段: {field}")
        
        # 校验scene_type或scene字段（兼容新旧格式）
        if "scene_type" not in data and "scene" not in data:
            raise ValueError("缺少必需字段: scene_type 或 scene")
        
        # 如果只有scene字段，转换为scene_type（兼容旧格式）
        if "scene" in data and "scene_type" not in data:
            data["scene_type"] = data["scene"]
        
        # 校验nodes格式
        if not isinstance(data["nodes"], list):
            raise ValueError("nodes必须是列表")
        
        if len(data["nodes"]) == 0:
            raise ValueError("nodes不能为空")
        
        # 校验每个node的基本字段
        node_required_fields = ["id", "type"]
        for i, node in enumerate(data["nodes"]):
            for field in node_required_fields:
                if field not in node:
                    raise ValueError(f"节点{i}缺少必需字段: {field}")
        
        # 校验edges格式（如果存在）
        if "edges" in data and not isinstance(data["edges"], list):
            raise ValueError("edges必须是列表")
        
        self.logger.debug("✅ 任务图数据校验通过")


# 全局加载器实例
_global_loader: Optional[TaskGraphLoader] = None

def get_graph_loader(base_path: str = "task_graphs") -> TaskGraphLoader:
    """获取全局任务图加载器实例"""
    global _global_loader
    if _global_loader is None:
        _global_loader = TaskGraphLoader(base_path)
    return _global_loader


if __name__ == "__main__":
    # 测试任务图加载器
    print("📄 TaskGraphLoader测试")
    print("=" * 60)
    
    loader = get_graph_loader("task_graphs")
    
    # 测试1: 从文件加载
    print("\n1. 从文件加载任务图...")
    try:
        graph = loader.load_from_file("hospital_visit.json")
        print(f"   ✅ 加载成功: {graph.graph_id}")
        print(f"   📋 场景: {graph.scene}")
        print(f"   🎯 目标: {graph.goal}")
        print(f"   📦 节点数: {len(graph.nodes)}")
    except FileNotFoundError:
        print("   ⚠️ 文件不存在，跳过测试")
    
    # 测试2: 数据校验
    print("\n2. 测试数据校验...")
    try:
        invalid_data = {"graph_id": "test"}  # 缺少必需字段
        loader._validate_graph_data(invalid_data)
        print("   ❌ 校验应该失败")
    except ValueError as e:
        print(f"   ✅ 校验失败（预期）: {e}")
    
    print("\n🎉 TaskGraphLoader测试完成！")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
节点层级管理器
自动为节点分配层级标签，如"室外主路"、"医院一楼"、"医院三楼结构锚点"等
"""

import json
import os
import logging
from typing import Dict, List, Optional
import re

logger = logging.getLogger(__name__)

class NodeLayerManager:
    """节点层级管理器"""
    
    def __init__(self):
        """初始化层级管理器"""
        # 层级关键词映射
        self.level_keywords = {
            "室外": ["室外", "户外", "街道", "路边", "人行道", "马路", "广场", "公园"],
            "入口区": ["入口", "大门", "门厅", "大厅", "前台", "接待"],
            "一楼": ["一楼", "1F", "地面层", "底层", "首层"],
            "二楼": ["二楼", "2F", "二层"],
            "三楼": ["三楼", "3F", "三层"],
            "四楼": ["四楼", "4F", "四层"],
            "电梯间": ["电梯", "升降梯", "直梯", "扶梯"],
            "楼梯间": ["楼梯", "台阶", "步梯"],
            "走廊": ["走廊", "通道", "过道", "走道", "廊道"],
            "候诊区": ["候诊", "等待", "候诊室", "等候区"],
            "科室": ["科室", "诊室", "病房", "检查室"],
            "卫生间": ["厕所", "洗手间", "卫生间", "盥洗"],
            "终端节点": ["终点", "目的地", "到达", "最终"],
            "功能锚点": ["锚点", "关键点", "转乘", "换乘"],
        }
        
        # 楼层数字映射
        self.floor_patterns = [
            (r'(\d+)楼', lambda m: f"{m.group(1)}F"),
            (r'(\d+)F', lambda m: f"{m.group(1)}F"),
            (r'(\d+)层', lambda m: f"{m.group(1)}F"),
        ]
        
        logger.info("📊 节点层级管理器初始化完成")
    
    def assign_level(self, node: Dict) -> str:
        """
        为单个节点分配层级标签
        
        Args:
            node: 节点字典，包含label等字段
            
        Returns:
            str: 层级标签
        """
        label = node.get("label", "").lower()
        
        # 检查各种层级关键词
        for level_name, keywords in self.level_keywords.items():
            for keyword in keywords:
                if keyword.lower() in label:
                    # 如果是楼层相关，添加楼层信息
                    if level_name in ["一楼", "二楼", "三楼", "四楼"]:
                        return f"{level_name}{self._extract_specific_area(node)}"
                    return f"{level_name}{self._extract_specific_area(node)}"
        
        # 检查楼层数字模式
        for pattern, formatter in self.floor_patterns:
            match = re.search(pattern, node.get("label", ""), re.IGNORECASE)
            if match:
                return f"{formatter(match)} {self._extract_specific_area(node)}"
        
        # 默认层级判断
        parent_path = node.get("parent_path", "")
        if parent_path:
            return self._infer_level_from_path(parent_path, node)
        
        # 最后的默认值
        return self._get_default_level(node)
    
    def _extract_specific_area(self, node: Dict) -> str:
        """提取具体区域信息"""
        label = node.get("label", "")
        
        # 检查是否有具体区域描述
        area_keywords = ["东", "西", "南", "北", "左", "右", "前", "后", 
                        "主", "次", "侧", "边", "中部", "中央"]
        
        for keyword in area_keywords:
            if keyword in label:
                return f" {keyword}区"
        
        # 检查是否有特殊功能
        special_keywords = ["主", "副", "紧急", "专用", "公共", "无障碍"]
        for keyword in special_keywords:
            if keyword in label:
                return f" {keyword}"
        
        return ""
    
    def _infer_level_from_path(self, parent_path: str, node: Dict) -> str:
        """从父路径推断层级"""
        # 简单的路径层级推断逻辑
        if "医院" in parent_path or "hospital" in parent_path.lower():
            # 尝试推断楼层
            if "1" in parent_path or "一楼" in parent_path:
                return "医院一楼"
            elif "2" in parent_path or "二楼" in parent_path:
                return "医院二楼"
            elif "3" in parent_path or "三楼" in parent_path:
                return "医院三楼"
            return "医院内部结构"
        
        if "地铁" in parent_path or "subway" in parent_path.lower():
            return "地铁站内结构"
        
        if "公交" in parent_path or "bus" in parent_path.lower():
            return "公交站区域"
        
        if "商场" in parent_path or "mall" in parent_path.lower():
            return "商场内部结构"
        
        return self._get_default_level(node)
    
    def _get_default_level(self, node: Dict) -> str:
        """获取默认层级"""
        # 根据节点类型推断
        node_type = node.get("type", "").lower()
        
        type_to_level = {
            "building": "建筑内部",
            "hospital": "医疗建筑",
            "toilet": "辅助功能区",
            "elevator": "交通枢纽",
            "stairs": "交通枢纽",
            "entrance": "入口区",
            "exit": "出口区",
            "destination": "终端节点",
            "waypoint": "中间节点",
        }
        
        level = type_to_level.get(node_type, "未分类区域")
        
        # 检查是否是终端节点
        if node.get("is_terminal", False):
            return f"{level} / 终端节点"
        
        return level
    
    def update_all_levels(self, memory_store_path: str, 
                         output_path: str = None) -> Dict:
        """
        更新所有路径中的所有节点层级
        
        Args:
            memory_store_path: 记忆存储文件路径
            output_path: 输出文件路径（如果为None则覆盖原文件）
            
        Returns:
            Dict: 更新统计信息
        """
        if output_path is None:
            output_path = memory_store_path
        
        try:
            # 读取数据
            with open(memory_store_path, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            if "paths" not in memory_data:
                logger.error("记忆存储中没有路径数据")
                return {"error": "No paths data"}
            
            # 统计信息
            stats = {
                "total_paths": 0,
                "total_nodes": 0,
                "updated_nodes": 0,
                "level_distribution": {}
            }
            
            # 更新每个路径中的节点
            for path in memory_data["paths"]:
                stats["total_paths"] += 1
                nodes = path.get("nodes", [])
                
                for node in nodes:
                    stats["total_nodes"] += 1
                    
                    # 分配层级
                    new_level = self.assign_level(node)
                    old_level = node.get("level", "未设置")
                    
                    # 更新层级
                    node["level"] = new_level
                    stats["updated_nodes"] += 1
                    
                    # 统计层级分布
                    if new_level not in stats["level_distribution"]:
                        stats["level_distribution"][new_level] = 0
                    stats["level_distribution"][new_level] += 1
                    
                    logger.debug(f"节点 {node.get('label', 'N/A')}: {old_level} -> {new_level}")
            
            # 保存更新后的数据
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 已更新 {stats['updated_nodes']}/{stats['total_nodes']} 个节点的层级")
            
            # 打印统计信息
            logger.info("\n📊 层级分布:")
            for level, count in sorted(stats["level_distribution"].items(), 
                                     key=lambda x: x[1], reverse=True):
                logger.info(f"  {level}: {count}")
            
            return stats
            
        except FileNotFoundError:
            logger.error(f"文件不存在: {memory_store_path}")
            return {"error": "File not found"}
        except json.JSONDecodeError:
            logger.error(f"文件格式错误: {memory_store_path}")
            return {"error": "JSON decode error"}
        except Exception as e:
            logger.error(f"更新层级失败: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
    
    def get_level_hierarchy(self, memory_store_path: str) -> Dict:
        """
        获取所有层级结构
        
        Args:
            memory_store_path: 记忆存储文件路径
            
        Returns:
            Dict: 层级结构树
        """
        try:
            with open(memory_store_path, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            hierarchy = {}
            
            for path in memory_data.get("paths", []):
                for node in path.get("nodes", []):
                    level = node.get("level", "未分类")
                    if level not in hierarchy:
                        hierarchy[level] = []
                    
                    hierarchy[level].append({
                        "label": node.get("label"),
                        "path_name": path.get("path_name"),
                        "node_id": node.get("node_id"),
                    })
            
            return hierarchy
            
        except Exception as e:
            logger.error(f"获取层级结构失败: {e}")
            return {}

def main():
    """测试主函数"""
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    manager = NodeLayerManager()
    
    # 测试单个节点
    test_nodes = [
        {"label": "医院入口大门", "type": "entrance"},
        {"label": "一楼大厅", "type": "building"},
        {"label": "三楼电梯间", "type": "elevator"},
        {"label": "二楼东侧卫生间", "type": "toilet"},
        {"label": "室外马路", "type": "waypoint"},
        {"label": "地铁1号线站台", "type": "destination"},
    ]
    
    print("\n=== 节点层级分配测试 ===")
    for node in test_nodes:
        level = manager.assign_level(node)
        print(f"节点: {node['label']:20s} -> 层级: {level}")
    
    # 测试批量更新
    memory_file = "data/memory_store.json"
    if os.path.exists(memory_file):
        print("\n=== 批量更新节点层级 ===")
        stats = manager.update_all_levels(memory_file)
        print(f"\n更新统计: {stats}")

if __name__ == "__main__":
    main()


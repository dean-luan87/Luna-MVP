#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 地图卡片生成器
将路径结构转换为手绘地图样式
"""

import cv2
import numpy as np
import json
import os
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class MapCardGenerator:
    """地图卡片生成器"""
    
    def __init__(self, output_dir: str = "data/map_cards"):
        """
        初始化地图生成器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # 地图样式配置
        self.map_config = {
            "width": 1200,          # 地图宽度
            "height": 800,          # 地图高度
            "bg_color": (255, 248, 220),  # 米色背景
            "node_size": 60,        # 节点大小
            "line_width": 4,        # 连线宽度
            "text_size": 1.0,       # 文字大小
        }
        
        # 节点颜色映射
        self.node_colors = {
            "room": (100, 149, 237),      # 蓝色
            "facility": (255, 165, 0),    # 橙色
            "exit": (255, 99, 71),        # 红色
            "restroom": (152, 251, 152),  # 绿色
            "department": (186, 85, 211), # 紫色
            "landmark": (255, 215, 0),    # 金色
        }
        
        logger.info("🗺️ 地图卡片生成器初始化完成")
    
    def generate_map_card(self, path_memory, output_name: str = None) -> str:
        """
        生成地图卡片
        
        Args:
            path_memory: 路径记忆对象
            output_name: 输出文件名
            
        Returns:
            str: 生成的地图文件路径
        """
        try:
            # 创建画布
            img = self._create_canvas()
            
            # 计算节点布局
            nodes = path_memory.nodes
            layout = self._calculate_layout(len(nodes))
            
            # 绘制节点和连线
            self._draw_path(img, nodes, layout)
            
            # 添加标题和说明
            self._add_title(img, path_memory.path_name)
            
            # 保存地图
            if output_name is None:
                output_name = f"{path_memory.path_id}_map.png"
            
            output_path = os.path.join(self.output_dir, output_name)
            cv2.imwrite(output_path, img)
            
            logger.info(f"🗺️ 地图已生成: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ 地图生成失败: {e}")
            return ""
    
    def _create_canvas(self) -> np.ndarray:
        """创建画布"""
        width = self.map_config["width"]
        height = self.map_config["height"]
        bg_color = self.map_config["bg_color"]
        
        img = np.ones((height, width, 3), dtype=np.uint8)
        img[:, :] = bg_color
        
        return img
    
    def _calculate_layout(self, node_count: int) -> List[Tuple[int, int]]:
        """
        计算节点布局位置
        
        Args:
            node_count: 节点数量
            
        Returns:
            List[Tuple]: 节点位置列表
        """
        width = self.map_config["width"]
        height = self.map_config["height"]
        
        # 使用网格布局
        if node_count <= 3:
            # 横向排列
            x_step = width // (node_count + 1)
            positions = []
            for i in range(node_count):
                x = x_step * (i + 1)
                y = height // 2
                positions.append((x, y))
        else:
            # 折线排列
            positions = []
            rows = (node_count + 2) // 3
            for i in range(node_count):
                row = i // 3
                col = i % 3
                x = (width // 4) * (col + 1)
                y = (height // (rows + 1)) * (row + 1)
                positions.append((x, y))
        
        return positions
    
    def _draw_path(self, img: np.ndarray, nodes: List, layout: List[Tuple[int, int]]):
        """
        绘制路径
        
        Args:
            img: 图像画布
            nodes: 节点列表
            layout: 布局位置
        """
        # 绘制连线
        for i in range(len(layout) - 1):
            pt1 = layout[i]
            pt2 = layout[i + 1]
            cv2.line(img, pt1, pt2, (139, 139, 139), self.map_config["line_width"])
            
            # 添加方向箭头
            self._draw_arrow(img, pt1, pt2)
        
        # 绘制节点
        for i, (node, pos) in enumerate(zip(nodes, layout)):
            self._draw_node(img, node, pos, i + 1)
    
    def _draw_node(self, img: np.ndarray, node, pos: Tuple[int, int], index: int):
        """
        绘制单个节点
        
        Args:
            img: 图像画布
            node: 节点对象
            pos: 节点位置
            index: 节点序号
        """
        x, y = pos
        node_size = self.map_config["node_size"]
        
        # 获取节点类型和颜色
        node_type = self._get_node_type(node.label)
        color = self.node_colors.get(node_type, (128, 128, 128))
        
        # 绘制圆形节点
        cv2.circle(img, (x, y), node_size // 2, color, -1)
        cv2.circle(img, (x, y), node_size // 2, (0, 0, 0), 2)
        
        # 添加序号
        text = str(index)
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
        text_x = x - text_size[0] // 2
        text_y = y + text_size[1] // 2
        cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        # 添加标签文字（在节点上方）
        label_y = y - node_size // 2 - 10
        self._draw_wrapped_text(img, node.label, (x, label_y))
    
    def _draw_wrapped_text(self, img: np.ndarray, text: str, pos: Tuple[int, int], max_width: int = 100):
        """
        绘制自动换行文字
        
        Args:
            img: 图像画布
            text: 文字内容
            pos: 起始位置
            max_width: 最大宽度
        """
        x, y = pos
        words = text.split()
        line_height = 25
        
        current_line = ""
        current_y = y
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            text_size = cv2.getTextSize(test_line, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            
            if text_size[0] > max_width and current_line:
                # 绘制当前行
                text_w = cv2.getTextSize(current_line, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0][0]
                cv2.putText(img, current_line, (x - text_w // 2, current_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                current_line = word
                current_y -= line_height
            else:
                current_line = test_line
        
        # 绘制最后一行
        if current_line:
            text_w = cv2.getTextSize(current_line, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0][0]
            cv2.putText(img, current_line, (x - text_w // 2, current_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    def _draw_arrow(self, img: np.ndarray, pt1: Tuple[int, int], pt2: Tuple[int, int]):
        """
        绘制方向箭头
        
        Args:
            img: 图像画布
            pt1: 起点
            pt2: 终点
        """
        dx = pt2[0] - pt1[0]
        dy = pt2[1] - pt1[1]
        angle = np.arctan2(dy, dx)
        
        # 箭头大小
        arrow_length = 30
        
        # 箭头头部位置
        arrow_x = pt2[0] - int(np.cos(angle) * self.map_config["node_size"] // 2)
        arrow_y = pt2[1] - int(np.sin(angle) * self.map_config["node_size"] // 2)
        
        # 绘制箭头
        tip = (arrow_x, arrow_y)
        left = (arrow_x - int(arrow_length * np.cos(angle - np.pi / 6)),
                arrow_y - int(arrow_length * np.sin(angle - np.pi / 6)))
        right = (arrow_x - int(arrow_length * np.cos(angle + np.pi / 6)),
                 arrow_y - int(arrow_length * np.sin(angle + np.pi / 6)))
        
        cv2.fillPoly(img, [np.array([tip, left, right])], (139, 139, 139))
    
    def _add_title(self, img: np.ndarray, title: str):
        """
        添加标题
        
        Args:
            img: 图像画布
            title: 标题文字
        """
        text_size = cv2.getTextSize(title, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 2)[0]
        text_x = (self.map_config["width"] - text_size[0]) // 2
        text_y = 40
        
        cv2.putText(img, title, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
    
    def _get_node_type(self, label: str) -> str:
        """
        从标签推断节点类型
        
        Args:
            label: 节点标签
            
        Returns:
            str: 节点类型
        """
        label_lower = label.lower()
        
        if any(kw in label_lower for kw in ["room", "室", "号", "office"]):
            return "room"
        elif any(kw in label_lower for kw in ["elevator", "电梯", "lift", "stair", "楼梯"]):
            return "facility"
        elif any(kw in label_lower for kw in ["exit", "出口", "entrance", "入口"]):
            return "exit"
        elif any(kw in label_lower for kw in ["toilet", "洗手间", "卫生间", "wc", "restroom"]):
            return "restroom"
        elif any(kw in label_lower for kw in ["挂号", "科室", "收费", "department"]):
            return "department"
        else:
            return "landmark"


if __name__ == "__main__":
    # 测试地图生成器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    from core.scene_memory_system import get_scene_memory_system
    
    print("=" * 60)
    print("🗺️ 地图卡片生成器测试")
    print("=" * 60)
    
    # 获取场景记忆
    system = get_scene_memory_system()
    path_memory = system.get_path_memory("test_hospital_path")
    
    if path_memory and len(path_memory.nodes) > 0:
        # 生成地图
        generator = MapCardGenerator()
        map_path = generator.generate_map_card(path_memory)
        
        if map_path:
            print(f"✅ 地图已生成: {map_path}")
        else:
            print("❌ 地图生成失败")
    else:
        print("⚠️ 没有路径记忆可生成地图")
    
    print("\n" + "=" * 60)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 手绘风格地图生成器
参考"漫游安庆"地图风格，创建更有方向感和立体感的地图
"""

import cv2
import numpy as np
import json
import os
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class HanddrawnMapGenerator:
    """手绘风格地图生成器"""
    
    def __init__(self, output_dir: str = "data/map_cards"):
        """
        初始化手绘地图生成器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # 地图样式配置 - 更大画布，留白更多
        self.map_config = {
            "width": 2400,          # 地图宽度
            "height": 1800,         # 地图高度
            "bg_color": (249, 247, 238),  # 米黄色背景
            "text_color": (40, 40, 40),   # 深灰色文字
            "compass_size": 120,    # 指南针大小
        }
        
        # 图标颜色 - 使用温暖色调
        self.icon_colors = {
            "home": (231, 111, 81),        # 橙红色 - 起点
            "building": (52, 152, 219),    # 蓝色 - 建筑物
            "restroom": (46, 204, 113),    # 绿色 - 洗手间
            "elevator": (155, 89, 182),    # 紫色 - 电梯
            "transit": (241, 196, 15),     # 黄色 - 交通
            "facility": (230, 126, 34),    # 橙黄色 - 设施
            "destination": (231, 76, 60),  # 红色 - 终点
        }
        
        # 节点图例映射
        self.node_icons = {
            "hospital": "🏥",
            "elevator": "🛗",
            "restroom": "🚻",
            "subway": "🚇",
            "bus": "🚌",
            "stairs": "🪜",
            "entrance": "🚪",
            "room": "🚪",
            "bridge": "🌉",
            "park": "🌳",
        }
        
        logger.info("🗺️ 手绘地图生成器初始化完成")
    
    def generate_handdrawn_map(self, path_memory, output_name: str = None) -> str:
        """
        生成手绘风格地图
        
        Args:
            path_memory: 路径记忆对象
            output_name: 输出文件名
            
        Returns:
            str: 生成的地图文件路径
        """
        try:
            # 创建画布
            img = self._create_canvas()
            
            # 分析节点
            nodes = path_memory.nodes
            analyzed_nodes = self._analyze_nodes(nodes)
            
            # 计算手绘布局（2D空间布局，非线性）
            layout = self._calculate_handdrawn_layout(analyzed_nodes)
            
            # 绘制指南针
            self._draw_compass(img)
            
            # 绘制路径（带方向感）
            self._draw_handdrawn_path(img, analyzed_nodes, layout)
            
            # 添加标题和说明
            self._add_handdrawn_title(img, path_memory.path_name)
            
            # 添加信息面板
            self._add_info_panel(img, path_memory, analyzed_nodes, layout)
            
            # 保存地图
            if output_name is None:
                output_name = f"{path_memory.path_id}_handdrawn.png"
            
            output_path = os.path.join(self.output_dir, output_name)
            cv2.imwrite(output_path, img)
            
            logger.info(f"🗺️ 手绘地图已生成: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ 手绘地图生成失败: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def _analyze_nodes(self, nodes: List) -> List[Dict]:
        """分析节点"""
        analyzed = []
        total_distance = 0.0
        
        for i, node in enumerate(nodes):
            # 分析节点类型
            node_type = self._classify_node_type(node.label)
            icon = self._get_icon_for_node(node.label)
            
            # 估算距离
            distance = self._estimate_distance_from_label(node.label, node.direction)
            total_distance += distance
            
            analyzed.append({
                'original': node,
                'type': node_type,
                'icon': icon,
                'distance': distance,
                'cumulative': total_distance,
                'position': None  # 将在布局计算中确定
            })
        
        return analyzed
    
    def _classify_node_type(self, label: str) -> str:
        """分类节点类型"""
        label_lower = label.lower()
        
        if any(kw in label_lower for kw in ["入口", "entrance", "起点", "start"]):
            return "home"
        elif any(kw in label_lower for kw in ["终点", "目的地", "destination"]):
            return "destination"
        elif any(kw in label_lower for kw in ["地铁", "subway", "公交", "bus", "站"]):
            return "transit"
        elif any(kw in label_lower for kw in ["洗手间", "toilet", "卫生间"]):
            return "restroom"
        elif any(kw in label_lower for kw in ["电梯", "elevator"]):
            return "elevator"
        elif any(kw in label_lower for kw in ["医院", "hospital", "商场", "mall"]):
            return "facility"
        else:
            return "building"
    
    def _get_icon_for_node(self, label: str) -> str:
        """获取节点图标"""
        label_lower = label.lower()
        
        if "医院" in label_lower or "hospital" in label_lower:
            return "🏥"
        elif "洗手间" in label_lower or "toilet" in label_lower or "卫生间" in label_lower:
            return "🚻"
        elif "电梯" in label_lower or "elevator" in label_lower:
            return "🛗"
        elif "地铁" in label_lower or "subway" in label_lower:
            return "🚇"
        elif "公交" in label_lower or "bus" in label_lower:
            return "🚌"
        elif "入口" in label_lower or "entrance" in label_lower:
            return "🚪"
        elif "室" in label_lower or "room" in label_lower:
            return "🚪"
        elif "桥" in label_lower or "bridge" in label_lower:
            return "🌉"
        elif "公园" in label_lower or "park" in label_lower:
            return "🌳"
        else:
            return "📍"
    
    def _estimate_distance_from_label(self, label: str, direction: str) -> float:
        """从标签和方向估算距离"""
        import re
        
        # 先从direction提取
        if direction:
            numbers = re.findall(r'(\d+)', direction)
            if numbers:
                return float(numbers[0])
        
        # 从label提取
        numbers = re.findall(r'(\d+)', label)
        if numbers:
            return float(numbers[0])
        
        return 10.0  # 默认
    
    def _calculate_handdrawn_layout(self, nodes: List[Dict]) -> Dict:
        """计算手绘布局 - 2D空间分布"""
        width = self.map_config["width"]
        height = self.map_config["height"]
        
        # 预留指南针和标题区域
        compass_area = 200
        title_area = 100
        info_panel = 400
        
        # 可用区域
        available_width = width - info_panel - 100
        available_height = height - compass_area - title_area - 100
        
        layout = {
            'center_x': available_width // 2,
            'center_y': title_area + 150,
            'boundary': {
                'min_x': 100,
                'max_x': available_width,
                'min_y': title_area + 100,
                'max_y': height - 200
            },
            'node_radius': 100,  # 节点绘制半径
            'spacing_angle': 30,  # 节点间角度（度）
            'spiral_radius': 80,  # 螺旋半径增量
        }
        
        # 为每个节点分配2D位置（螺旋布局）
        start_angle = 0
        current_radius = 200
        
        for i, node in enumerate(nodes):
            angle = start_angle + i * layout['spacing_angle']
            angle_rad = np.deg2rad(angle)
            
            x = layout['center_x'] + current_radius * np.cos(angle_rad)
            y = layout['center_y'] + current_radius * np.sin(angle_rad)
            
            # 确保在边界内
            x = max(layout['boundary']['min_x'], min(layout['boundary']['max_x'], x))
            y = max(layout['boundary']['min_y'], min(layout['boundary']['max_y'], y))
            
            node['position'] = (int(x), int(y))
            node['angle'] = angle
            
            # 增加半径（螺旋效果）
            current_radius += layout['spiral_radius']
        
        return layout
    
    def _draw_compass(self, img: np.ndarray):
        """绘制指南针"""
        width = self.map_config["width"]
        size = self.map_config["compass_size"]
        
        # 指南针位置（右上角）
        center_x = width - 200
        center_y = 100
        
        # 绘制指南针外圈
        cv2.circle(img, (center_x, center_y), size, (50, 50, 50), 3)
        
        # 绘制方向标识
        # N (北)
        cv2.putText(img, "N", (center_x - 10, center_y - size + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (231, 76, 60), 3)
        # S (南)
        cv2.putText(img, "S", (center_x - 10, center_y + size - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (52, 152, 219), 3)
        # E (东)
        cv2.putText(img, "E", (center_x + size - 30, center_y + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (46, 204, 113), 3)
        # W (西)
        cv2.putText(img, "W", (center_x - size + 20, center_y + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (241, 196, 15), 3)
        
        # 绘制指南针指针（指北）
        cv2.arrowedLine(img, (center_x, center_y), (center_x, center_y - size + 40),
                       (231, 76, 60), 5, tipLength=0.3)
        
        # 绘制十字线
        cv2.line(img, (center_x - size + 20, center_y), (center_x + size - 20, center_y),
                (100, 100, 100), 2)
        cv2.line(img, (center_x, center_y - size + 20), (center_x, center_y + size - 20),
                (100, 100, 100), 2)
    
    def _draw_handdrawn_path(self, img: np.ndarray, nodes: List[Dict], layout: Dict):
        """绘制手绘风格路径"""
        if len(nodes) < 2:
            return
        
        # 绘制路径连线（带方向箭头）
        for i in range(len(nodes) - 1):
            from_node = nodes[i]
            to_node = nodes[i + 1]
            
            from_pos = from_node['position']
            to_pos = to_node['position']
            
            # 绘制路径线
            self._draw_path_segment(img, from_pos, to_pos, from_node, to_node)
        
        # 绘制节点
        for i, node in enumerate(nodes):
            self._draw_handdrawn_node(img, node, i, layout)
    
    def _draw_path_segment(self, img: np.ndarray, from_pos: Tuple, to_pos: Tuple,
                          from_node: Dict, to_node: Dict):
        """绘制路径段"""
        # 使用节点类型的颜色
        color = self.icon_colors.get(from_node['type'], (100, 100, 100))
        
        # 绘制路径线（稍微加粗，手绘风格）
        cv2.line(img, from_pos, to_pos, color, 8)
        
        # 计算箭头位置（接近终点）
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]
        length = np.sqrt(dx*dx + dy*dy)
        
        # 箭头起点（距离终点30%的位置）
        arrow_start_x = int(from_pos[0] + 0.7 * dx)
        arrow_start_y = int(from_pos[1] + 0.7 * dy)
        
        # 绘制方向箭头
        cv2.arrowedLine(img, (arrow_start_x, arrow_start_y), to_pos,
                       color, 6, tipLength=0.4)
        
        # 添加距离标签（路径中点）
        mid_x = (from_pos[0] + to_pos[0]) // 2
        mid_y = (from_pos[1] + to_pos[1]) // 2
        
        distance_text = f"{to_node['distance']:.0f}m"
        
        # 背景框
        (text_width, text_height), baseline = cv2.getTextSize(
            distance_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(img, 
                     (mid_x - text_width//2 - 5, mid_y - text_height - 5),
                     (mid_x + text_width//2 + 5, mid_y + baseline + 5),
                     (255, 255, 255), -1)
        
        # 距离文字
        cv2.putText(img, distance_text, 
                   (mid_x - text_width//2, mid_y + baseline//2),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    def _draw_handdrawn_node(self, img: np.ndarray, node: Dict, index: int, layout: Dict):
        """绘制手绘风格节点"""
        position = node['position']
        node_type = node['type']
        icon = node['icon']
        label = node['original'].label
        
        # 颜色
        color = self.icon_colors.get(node_type, (100, 100, 100))
        
        # 绘制节点圆圈（稍微不规则，手绘风格）
        radius = layout.get('node_radius', 100)
        self._draw_handdrawn_circle(img, position, radius, color)
        
        # 绘制节点编号
        cv2.putText(img, str(index + 1), 
                   (position[0] - 15, position[1] + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
        
        # 绘制图标（使用emoji，如果系统支持）
        icon_text = icon
        try:
            # 尝试绘制emoji（如果环境支持）
            cv2.putText(img, icon_text, 
                       (position[0] - 40, position[1] - 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
        except:
            pass
        
        # 绘制节点标签（简化，避免过长）
        label_short = label.split('（')[0].split('(')[0]
        label_short = label_short[:10]  # 最多10个字符
        
        # 计算文字宽度
        (text_width, text_height), baseline = cv2.getTextSize(
            label_short, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        
        # 标签背景框
        cv2.rectangle(img,
                     (position[0] - text_width//2 - 8, position[1] + radius + 15),
                     (position[0] + text_width//2 + 8, position[1] + radius + text_height + 20),
                     (255, 255, 255), -1)
        cv2.rectangle(img,
                     (position[0] - text_width//2 - 8, position[1] + radius + 15),
                     (position[0] + text_width//2 + 8, position[1] + radius + text_height + 20),
                     self.map_config["text_color"], 2)
        
        # 标签文字
        cv2.putText(img, label_short,
                   (position[0] - text_width//2, position[1] + radius + text_height + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.map_config["text_color"], 2)
    
    def _draw_handdrawn_circle(self, img: np.ndarray, center: Tuple, radius: int, color: Tuple):
        """绘制手绘风格圆圈（轻微不规则）"""
        # 绘制多个同心圆制造手绘效果
        for i in range(3):
            offset = i * 2
            cv2.circle(img, center, radius + offset, color, 3)
        
        # 主圆圈
        cv2.circle(img, center, radius, color, -1)
        cv2.circle(img, center, radius, (255, 255, 255), 2)
    
    def _add_handdrawn_title(self, img: np.ndarray, title: str):
        """添加标题"""
        # 主标题
        cv2.putText(img, title, (100, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, self.map_config["text_color"], 3)
        
        # 副标题
        subtitle = "Luna Badge Navigation Map"
        cv2.putText(img, subtitle, (100, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (120, 120, 120), 2)
    
    def _add_info_panel(self, img: np.ndarray, path_memory, nodes: List[Dict], layout: Dict):
        """添加信息面板"""
        width = self.map_config["width"]
        panel_x = width - 380
        panel_width = 360
        panel_height = self.map_config["height"] - 200
        
        # 面板背景
        cv2.rectangle(img, (panel_x, 100), (width - 20, self.map_config["height"] - 100),
                     (255, 255, 255), -1)
        cv2.rectangle(img, (panel_x, 100), (width - 20, self.map_config["height"] - 100),
                     self.map_config["text_color"], 3)
        
        y_offset = 130
        
        # 标题
        cv2.putText(img, "Path Info", (panel_x + 20, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.map_config["text_color"], 2)
        y_offset += 50
        
        # 总距离
        total_distance = sum(n['distance'] for n in nodes)
        if total_distance > 1000:
            total_text = f"Total: {total_distance/1000:.2f}km"
        else:
            total_text = f"Total: {total_distance:.0f}m"
        
        cv2.putText(img, total_text, (panel_x + 20, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (46, 204, 113), 2)
        y_offset += 40
        
        # 节点统计
        node_counts = {}
        for node in nodes:
            node_type = node['type']
            node_counts[node_type] = node_counts.get(node_type, 0) + 1
        
        cv2.putText(img, "Node Types:", (panel_x + 20, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.map_config["text_color"], 2)
        y_offset += 40
        
        for node_type, count in node_counts.items():
            type_text = f"  {node_type}: {count}"
            cv2.putText(img, type_text, (panel_x + 20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
            y_offset += 30
    
    def _create_canvas(self) -> np.ndarray:
        """创建画布"""
        width = self.map_config["width"]
        height = self.map_config["height"]
        bg_color = self.map_config["bg_color"]
        
        img = np.ones((height, width, 3), dtype=np.uint8)
        img[:, :] = bg_color
        
        return img


if __name__ == "__main__":
    # 测试手绘地图生成器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    from core.scene_memory_system import PathMemory, SceneNode
    
    print("=" * 60)
    print("🗺️ 手绘地图生成器测试")
    print("=" * 60)
    
    generator = HanddrawnMapGenerator()
    
    # 创建测试路径
    nodes = [
        SceneNode("n1", "医院主入口", "", timestamp=datetime.now().isoformat(), direction="起点"),
        SceneNode("n2", "电梯厅", "", timestamp=datetime.now().isoformat(), direction="前行20米"),
        SceneNode("n3", "挂号处", "", timestamp=datetime.now().isoformat(), direction="右转10米"),
        SceneNode("n4", "急诊科", "", timestamp=datetime.now().isoformat(), direction="继续前行15米"),
    ]
    
    path = PathMemory("test_handdrawn", "测试手绘地图", nodes)
    
    # 生成地图
    map_file = generator.generate_handdrawn_map(path, "test_handdrawn.png")
    
    if map_file:
        print(f"✅ 手绘地图已生成: {map_file}")
    else:
        print("❌ 地图生成失败")
    
    print("=" * 60)


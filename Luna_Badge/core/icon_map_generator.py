#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 图标地图生成器
使用实际图标文件替代emoji，解决乱码问题
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

class IconMapGenerator:
    """图标地图生成器"""
    
    def __init__(self, output_dir: str = "data/map_cards", icons_dir: str = "assets/icons/tabler"):
        """
        初始化图标地图生成器
        
        Args:
            output_dir: 输出目录
            icons_dir: 图标目录
        """
        self.output_dir = output_dir
        self.icons_dir = icons_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.icons_dir).mkdir(parents=True, exist_ok=True)
        
        # 导入SVG加载器
        try:
            from core.svg_icon_loader import SVGIconLoader
            self.svg_loader = SVGIconLoader
        except ImportError:
            self.svg_loader = None
            logger.warning("⚠️ SVG图标加载器导入失败")
        
        # 地图样式配置
        self.map_config = {
            "width": 2400,
            "height": 1800,
            "bg_color": (249, 247, 238),
            "text_color": (40, 40, 40),
            "compass_size": 120,
        }
        
        # 图标颜色
        self.icon_colors = {
            "home": (231, 111, 81),
            "building": (52, 152, 219),
            "restroom": (46, 204, 113),
            "elevator": (155, 89, 182),
            "transit": (241, 196, 15),
            "facility": (230, 126, 34),
            "destination": (231, 76, 60),
        }
        
        # 图标文件映射（Tabler SVG图标）
        self.icon_files = {
            "hospital": "hospital.svg",
            "toilet": "toilet.svg",
            "elevator": "elevator.svg",
            "subway": "subway.svg",
            "bus": "bus.svg",
            "home": "home.svg",
            "destination": "map-pin.svg",
            "info": "info-square.svg",
            "stairs": "stairs.svg",
            "door": "door-enter.svg",
            "building": "building.svg",
            "wheelchair": "wheelchair.svg",
            "user": "user.svg",
        }
        
        # 图标缓存
        self.icon_cache = {}
        self._load_icons()
        
        logger.info("🗺️ 图标地图生成器初始化完成")
    
    def _load_icons(self):
        """加载图标文件"""
        for key, filename in self.icon_files.items():
            icon_path = os.path.join(self.icons_dir, filename)
            if os.path.exists(icon_path):
                # 检查文件扩展名
                if filename.endswith('.svg'):
                    # 加载SVG图标
                    if self.svg_loader:
                        icon_img = self.svg_loader.load_svg_icon(icon_path, size=64)
                        if icon_img is not None:
                            self.icon_cache[key] = icon_img
                            logger.info(f"  ✅ 加载SVG图标: {filename}")
                        else:
                            logger.warning(f"  ⚠️ SVG图标加载失败: {filename}")
                    else:
                        logger.warning(f"  ⚠️ SVG加载器不可用: {filename}")
                else:
                    # 加载PNG图标
                    icon_img = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)
                    if icon_img is not None:
                        # 转换为RGBA
                        if len(icon_img.shape) == 2:
                            icon_img = cv2.cvtColor(icon_img, cv2.COLOR_GRAY2RGBA)
                        elif icon_img.shape[2] == 3:
                            icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGR2RGBA)
                        self.icon_cache[key] = icon_img
                        logger.info(f"  ✅ 加载PNG图标: {filename}")
                    else:
                        logger.warning(f"  ⚠️ 图标加载失败: {filename}")
            else:
                logger.warning(f"  ⚠️ 图标文件不存在: {icon_path}")
        
        # 如果未加载到足够的图标文件，使用简单的几何图形作为替代
        # 始终创建备用图标以确保至少有基础图标可用
        self._create_fallback_icons()
        
        # 统计加载结果
        loaded_count = len([k for k in self.icon_files.keys() if k in self.icon_cache])
        if loaded_count == 0:
            logger.warning("  ⚠️ 未找到任何图标文件，仅使用备用几何图形")
        else:
            logger.info(f"  📊 加载了 {loaded_count}/{len(self.icon_files)} 个图标文件")
    
    def _create_fallback_icons(self):
        """创建备用图标（简单几何图形）"""
        size = 64
        
        # 医院图标（十字）
        hospital = np.zeros((size, size, 4), dtype=np.uint8)
        center = size // 2
        cv2.rectangle(hospital, (center-20, center-5), (center+20, center+5), (52, 152, 219, 255), -1)
        cv2.rectangle(hospital, (center-5, center-20), (center+5, center+20), (52, 152, 219, 255), -1)
        self.icon_cache["hospital"] = hospital
        
        # 洗手间图标（马桶）
        toilet = np.zeros((size, size, 4), dtype=np.uint8)
        cv2.ellipse(toilet, (center, center+10), (20, 10), 0, 0, 360, (46, 204, 113, 255), -1)
        cv2.circle(toilet, (center, center), 15, (46, 204, 113, 255), 3)
        self.icon_cache["toilet"] = toilet
        
        # 电梯图标（矩形）
        elevator = np.zeros((size, size, 4), dtype=np.uint8)
        cv2.rectangle(elevator, (center-15, center-20), (center+15, center+20), (155, 89, 182, 255), -1)
        cv2.rectangle(elevator, (center-15, center-20), (center+15, center+20), (255, 255, 255, 255), 2)
        cv2.rectangle(elevator, (center-12, center-12), (center+12, center+12), (155, 89, 182, 255), 1)
        self.icon_cache["elevator"] = elevator
        
        # 地铁图标（M）
        subway = np.zeros((size, size, 4), dtype=np.uint8)
        cv2.putText(subway, "M", (center-25, center+25), cv2.FONT_HERSHEY_SIMPLEX, 
                   1.0, (241, 196, 15, 255), 2)
        self.icon_cache["subway"] = subway
        
        # 公交图标（BUS）
        bus = np.zeros((size, size, 4), dtype=np.uint8)
        cv2.putText(bus, "B", (center-25, center+25), cv2.FONT_HERSHEY_SIMPLEX,
                   1.0, (241, 196, 15, 255), 2)
        self.icon_cache["bus"] = bus
        
        # 家图标（房子）
        home = np.zeros((size, size, 4), dtype=np.uint8)
        points = np.array([[center, center-25], [center-20, center-10], [center+20, center-10]], np.int32)
        cv2.fillPoly(home, [points], (231, 111, 81, 255))
        cv2.rectangle(home, (center-15, center-10), (center+15, center+15), (231, 111, 81, 255), -1)
        cv2.rectangle(home, (center-3, center-3), (center+3, center+15), (255, 255, 255, 255), 2)
        self.icon_cache["home"] = home
        
        # 目的地图标（旗帜）
        destination = np.zeros((size, size, 4), dtype=np.uint8)
        cv2.circle(destination, (center, center), 20, (231, 76, 60, 255), -1)
        cv2.rectangle(destination, (center, center-20), (center+5, center), (231, 76, 60, 255), -1)
        self.icon_cache["destination"] = destination
        
        # 信息图标（i）
        info = np.zeros((size, size, 4), dtype=np.uint8)
        cv2.circle(info, (center, center), 20, (230, 126, 34, 255), -1)
        cv2.putText(info, "i", (center-5, center+8), cv2.FONT_HERSHEY_SIMPLEX,
                   0.8, (255, 255, 255, 255), 2)
        self.icon_cache["info"] = info
        
        logger.info("  ✅ 创建了备用图标")
    
    def generate_icon_map(self, path_memory, output_name: str = None) -> str:
        """生成图标地图"""
        try:
            img = self._create_canvas()
            
            nodes = path_memory.nodes
            analyzed_nodes = self._analyze_nodes(nodes)
            layout = self._calculate_layout(analyzed_nodes)
            
            self._draw_compass(img)
            self._draw_path_with_icons(img, analyzed_nodes, layout)
            self._add_title(img, path_memory.path_name)
            self._add_info_panel(img, path_memory, analyzed_nodes, layout)
            
            if output_name is None:
                output_name = f"{path_memory.path_id}_icon_map.png"
            
            output_path = os.path.join(self.output_dir, output_name)
            cv2.imwrite(output_path, img)
            
            logger.info(f"🗺️ 图标地图已生成: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ 图标地图生成失败: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def _analyze_nodes(self, nodes: List) -> List[Dict]:
        """分析节点"""
        analyzed = []
        total_distance = 0.0
        
        for i, node in enumerate(nodes):
            node_type = self._classify_node_type(node.label)
            icon_key = self._get_icon_key(node.label)
            
            distance = self._estimate_distance_from_label(node.label, node.direction)
            total_distance += distance
            
            analyzed.append({
                'original': node,
                'type': node_type,
                'icon_key': icon_key,
                'distance': distance,
                'cumulative': total_distance,
                'position': None
            })
        
        return analyzed
    
    def _classify_node_type(self, label: str) -> str:
        """分类节点类型"""
        label_lower = label.lower()
        
        if any(kw in label_lower for kw in ["入口", "entrance", "起点", "start"]):
            return "home"
        elif any(kw in label_lower for kw in ["终点", "目的地", "destination"]):
            return "destination"
        elif any(kw in label_lower for kw in ["地铁", "subway"]):
            return "transit"
        elif any(kw in label_lower for kw in ["公交", "bus"]):
            return "transit"
        elif any(kw in label_lower for kw in ["洗手间", "toilet", "卫生间"]):
            return "restroom"
        elif any(kw in label_lower for kw in ["电梯", "elevator"]):
            return "elevator"
        elif any(kw in label_lower for kw in ["医院", "hospital", "商场", "mall"]):
            return "facility"
        else:
            return "building"
    
    def _get_icon_key(self, label: str) -> str:
        """获取图标键"""
        label_lower = label.lower()
        
        if "医院" in label_lower or "hospital" in label_lower:
            return "hospital"
        elif "洗手间" in label_lower or "toilet" in label_lower:
            return "toilet"
        elif "电梯" in label_lower or "elevator" in label_lower:
            return "elevator"
        elif "地铁" in label_lower or "subway" in label_lower:
            return "subway"
        elif "公交" in label_lower or "bus" in label_lower:
            return "bus"
        elif "入口" in label_lower or "起点" in label_lower:
            return "home"
        elif "终点" in label_lower or "目的地" in label_lower:
            return "destination"
        elif "咨询" in label_lower or "info" in label_lower:
            return "info"
        else:
            return "building"
    
    def _estimate_distance_from_label(self, label: str, direction: str) -> float:
        """估算距离"""
        import re
        if direction:
            numbers = re.findall(r'(\d+)', direction)
            if numbers:
                return float(numbers[0])
        numbers = re.findall(r'(\d+)', label)
        if numbers:
            return float(numbers[0])
        return 10.0
    
    def _calculate_layout(self, nodes: List[Dict]) -> Dict:
        """计算布局"""
        width = self.map_config["width"]
        height = self.map_config["height"]
        
        available_width = width - 400 - 100
        available_height = height - 300 - 100
        
        layout = {
            'center_x': available_width // 2,
            'center_y': 250,
            'boundary': {
                'min_x': 100,
                'max_x': available_width,
                'min_y': 250,
                'max_y': height - 200
            },
            'node_radius': 100,
            'spacing_angle': 30,
            'spiral_radius': 80,
        }
        
        start_angle = 0
        current_radius = 200
        
        for i, node in enumerate(nodes):
            angle = start_angle + i * layout['spacing_angle']
            angle_rad = np.deg2rad(angle)
            
            x = layout['center_x'] + current_radius * np.cos(angle_rad)
            y = layout['center_y'] + current_radius * np.sin(angle_rad)
            
            x = max(layout['boundary']['min_x'], min(layout['boundary']['max_x'], x))
            y = max(layout['boundary']['min_y'], min(layout['boundary']['max_y'], y))
            
            node['position'] = (int(x), int(y))
            node['angle'] = angle
            current_radius += layout['spiral_radius']
        
        return layout
    
    def _draw_compass(self, img: np.ndarray):
        """绘制指南针"""
        width = self.map_config["width"]
        size = self.map_config["compass_size"]
        
        center_x = width - 200
        center_y = 100
        
        cv2.circle(img, (center_x, center_y), size, (50, 50, 50), 3)
        
        cv2.putText(img, "N", (center_x - 10, center_y - size + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (231, 76, 60), 3)
        cv2.putText(img, "S", (center_x - 10, center_y + size - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (52, 152, 219), 3)
        cv2.putText(img, "E", (center_x + size - 30, center_y + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (46, 204, 113), 3)
        cv2.putText(img, "W", (center_x - size + 20, center_y + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (241, 196, 15), 3)
        
        cv2.arrowedLine(img, (center_x, center_y), (center_x, center_y - size + 40),
                       (231, 76, 60), 5, tipLength=0.3)
        
        cv2.line(img, (center_x - size + 20, center_y), (center_x + size - 20, center_y),
                (100, 100, 100), 2)
        cv2.line(img, (center_x, center_y - size + 20), (center_x, center_y + size - 20),
                (100, 100, 100), 2)
    
    def _draw_path_with_icons(self, img: np.ndarray, nodes: List[Dict], layout: Dict):
        """绘制带图标的路径"""
        if len(nodes) < 2:
            return
        
        # 绘制节点
        for i, node in enumerate(nodes):
            self._draw_node_with_icon(img, node, i, layout)
        
        # 绘制路径线
        for i in range(len(nodes) - 1):
            from_node = nodes[i]
            to_node = nodes[i + 1]
            
            from_pos = from_node['position']
            to_pos = to_node['position']
            
            self._draw_path_segment(img, from_pos, to_pos, from_node, to_node)
    
    def _draw_path_segment(self, img: np.ndarray, from_pos: Tuple, to_pos: Tuple,
                          from_node: Dict, to_node: Dict):
        """绘制路径段"""
        color = self.icon_colors.get(from_node['type'], (100, 100, 100))
        
        cv2.line(img, from_pos, to_pos, color, 8)
        
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]
        
        arrow_start_x = int(from_pos[0] + 0.7 * dx)
        arrow_start_y = int(from_pos[1] + 0.7 * dy)
        
        cv2.arrowedLine(img, (arrow_start_x, arrow_start_y), to_pos,
                       color, 6, tipLength=0.4)
        
        mid_x = (from_pos[0] + to_pos[0]) // 2
        mid_y = (from_pos[1] + to_pos[1]) // 2
        
        distance_text = f"{to_node['distance']:.0f}m"
        
        (text_width, text_height), baseline = cv2.getTextSize(
            distance_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(img, 
                     (mid_x - text_width//2 - 5, mid_y - text_height - 5),
                     (mid_x + text_width//2 + 5, mid_y + baseline + 5),
                     (255, 255, 255), -1)
        
        cv2.putText(img, distance_text, 
                   (mid_x - text_width//2, mid_y + baseline//2),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    def _draw_node_with_icon(self, img: np.ndarray, node: Dict, index: int, layout: Dict):
        """绘制带图标的节点"""
        position = node['position']
        node_type = node['type']
        icon_key = node['icon_key']
        label = node['original'].label
        
        color = self.icon_colors.get(node_type, (100, 100, 100))
        radius = layout.get('node_radius', 100)
        
        # 绘制节点圆圈
        self._draw_circle(img, position, radius, color)
        
        # 绘制图标
        icon_img = self.icon_cache.get(icon_key)
        if icon_img is not None:
            self._draw_icon(img, position, icon_img, radius)
        
        # 绘制节点编号（在节点内部）
        cv2.putText(img, str(index + 1), 
                   (position[0] - 15, position[1] + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
        
        # 绘制标签（简化为节点编号下方）
        # 使用英文或数字替代中文字符
        node_type_text = node_type.upper()
        
        (text_width, text_height), baseline = cv2.getTextSize(
            node_type_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        
        cv2.rectangle(img,
                     (position[0] - text_width//2 - 8, position[1] + radius + 15),
                     (position[0] + text_width//2 + 8, position[1] + radius + text_height + 20),
                     (255, 255, 255), -1)
        cv2.rectangle(img,
                     (position[0] - text_width//2 - 8, position[1] + radius + 15),
                     (position[0] + text_width//2 + 8, position[1] + radius + text_height + 20),
                     self.map_config["text_color"], 2)
        
        cv2.putText(img, node_type_text,
                   (position[0] - text_width//2, position[1] + radius + text_height + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.map_config["text_color"], 2)
    
    def _draw_icon(self, img: np.ndarray, position: Tuple, icon_img: np.ndarray, node_radius: int):
        """绘制图标"""
        icon_size = node_radius - 20
        
        # 缩放图标
        h, w = icon_img.shape[:2]
        scale = min(icon_size / w, icon_size / h)
        new_w, new_h = int(w * scale), int(h * scale)
        
        icon_resized = cv2.resize(icon_img, (new_w, new_h))
        
        # 计算位置
        x1 = position[0] - new_w // 2
        y1 = position[1] - new_h // 2 - 10
        x2 = x1 + new_w
        y2 = y1 + new_h
        
        # 处理透明度
        if icon_resized.shape[2] == 4:
            alpha = icon_resized[:, :, 3] / 255.0
            for c in range(3):
                img[y1:y2, x1:x2, c] = (
                    alpha * icon_resized[:, :, c] + 
                    (1 - alpha) * img[y1:y2, x1:x2, c]
                )
        else:
            img[y1:y2, x1:x2] = icon_resized[:, :, :3]
    
    def _draw_circle(self, img: np.ndarray, center: Tuple, radius: int, color: Tuple):
        """绘制圆圈"""
        for i in range(3):
            offset = i * 2
            cv2.circle(img, center, radius + offset, color, 3)
        cv2.circle(img, center, radius, color, -1)
        cv2.circle(img, center, radius, (255, 255, 255), 2)
    
    def _add_title(self, img: np.ndarray, title: str):
        """添加标题 - 使用英文以避免中文乱码"""
        # 简化标题，避免中文字符
        safe_title = "Navigation Map"
        
        cv2.putText(img, safe_title, (100, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, self.map_config["text_color"], 3)
        
        # 使用路径ID作为副标题
        subtitle = "Luna Badge Path Guide"
        cv2.putText(img, subtitle, (100, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (120, 120, 120), 2)
    
    def _add_info_panel(self, img: np.ndarray, path_memory, nodes: List[Dict], layout: Dict):
        """添加信息面板"""
        width = self.map_config["width"]
        panel_x = width - 380
        
        cv2.rectangle(img, (panel_x, 100), (width - 20, self.map_config["height"] - 100),
                     (255, 255, 255), -1)
        cv2.rectangle(img, (panel_x, 100), (width - 20, self.map_config["height"] - 100),
                     self.map_config["text_color"], 3)
        
        y_offset = 130
        
        cv2.putText(img, "Path Info", (panel_x + 20, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.map_config["text_color"], 2)
        y_offset += 50
        
        total_distance = sum(n['distance'] for n in nodes)
        if total_distance > 1000:
            total_text = f"Total: {total_distance/1000:.2f}km"
        else:
            total_text = f"Total: {total_distance:.0f}m"
        
        cv2.putText(img, total_text, (panel_x + 20, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (46, 204, 113), 2)
        y_offset += 40
        
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
    import logging
    logging.basicConfig(level=logging.INFO)
    
    from core.scene_memory_system import PathMemory, SceneNode
    
    print("=" * 60)
    print("🗺️ 图标地图生成器测试")
    print("=" * 60)
    
    generator = IconMapGenerator()
    
    nodes = [
        SceneNode("n1", "医院主入口", "", timestamp=datetime.now().isoformat(), direction="起点"),
        SceneNode("n2", "电梯厅", "", timestamp=datetime.now().isoformat(), direction="前行20米"),
        SceneNode("n3", "挂号处", "", timestamp=datetime.now().isoformat(), direction="右转10米"),
    ]
    
    path = PathMemory("test_icon", "测试图标地图", nodes)
    
    map_file = generator.generate_icon_map(path, "test_icon_map.png")
    
    if map_file:
        print(f"✅ 图标地图已生成: {map_file}")
    else:
        print("❌ 地图生成失败")
    
    print("=" * 60)


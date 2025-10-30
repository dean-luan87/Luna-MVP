#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 增强地图生成器
支持分层显示、距离信息、公共设施查询和评估
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

class EnhancedMapGenerator:
    """增强地图生成器"""
    
    def __init__(self, output_dir: str = "data/map_cards"):
        """
        初始化增强地图生成器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # 地图样式配置
        self.map_config = {
            "width": 1600,          # 地图宽度
            "height": 1000,         # 地图高度
            "bg_color": (255, 248, 220),  # 米色背景
            "node_size": 80,        # 节点大小
            "line_width": 5,        # 连线宽度
            "text_size": 1.2,       # 文字大小
        }
        
        # 节点类型颜色映射（分层）
        self.node_colors = {
            "outdoor": (135, 206, 235),    # 天蓝色 - 室外节点
            "walkway": (144, 238, 144),    # 浅绿色 - 路径节点
            "indoor": (255, 165, 0),       # 橙色 - 室内节点
            "facility": (186, 85, 211),    # 紫色 - 公共设施
            "transit": (255, 99, 71),      # 红色 - 公共交通
            "landmark": (255, 215, 0),     # 金色 - 地标
        }
        
        # 图层配置
        self.layer_config = {
            "outdoor": {"opacity": 1.0, "z_order": 1},
            "indoor": {"opacity": 0.95, "z_order": 2},
        }
        
        logger.info("🗺️ 增强地图生成器初始化完成")
    
    def classify_node_type(self, node_label: str, node) -> Tuple[str, str]:
        """
        分类节点类型和图层
        
        Args:
            node_label: 节点标签
            node: 节点对象
            
        Returns:
            Tuple[str, str]: (节点类型, 图层)
        """
        label_lower = node_label.lower()
        
        # 公共交通
        if any(kw in label_lower for kw in ["地铁", "subway", "metro", "公交", "bus", "站"]):
            return ("transit", "outdoor")
        
        # 公共设施
        if any(kw in label_lower for kw in ["洗手间", "toilet", "卫生间", "wc", "电梯", "elevator", "扶梯", "escalator"]):
            return ("facility", "indoor")
        if any(kw in label_lower for kw in ["医院", "hospital", "商场", "mall", "超市", "supermarket"]):
            return ("facility", "indoor")
        
        # 室内节点
        if any(kw in label_lower for kw in ["室", "room", "office", "病房", "科室"]):
            return ("indoor", "indoor")
        
        # 路径节点
        if any(kw in label_lower for kw in ["口", "entrance", "exit", "走廊", "corridor", "过道"]):
            return ("walkway", "indoor")
        if any(kw in label_lower for kw in ["桥", "bridge", "道", "路", "road", "街", "street"]):
            return ("walkway", "outdoor")
        
        # 默认分类
        return ("landmark", "outdoor")
    
    def generate_enhanced_map_card(self, path_memory, output_name: str = None) -> str:
        """
        生成增强地图卡片
        
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
            analyzed_nodes = []
            total_distance = 0.0
            
            for i, node in enumerate(nodes):
                # 分类节点类型
                node_type, layer = self.classify_node_type(node.label, node)
                
                # 估算距离
                if i > 0:
                    prev_node = analyzed_nodes[-1]
                    distance = self._estimate_distance(prev_node, node)
                    total_distance += distance
                else:
                    distance = 0.0
                
                # 提取信息
                analyzed_node = {
                    'original': node,
                    'type': node_type,
                    'layer': layer,
                    'distance': distance,
                    'cumulative_distance': total_distance,
                    'facility_info': self._extract_facility_info(node),
                    'transit_info': self._extract_transit_info(node)
                }
                
                analyzed_nodes.append(analyzed_node)
            
            # 计算布局
            layout = self._calculate_enhanced_layout(analyzed_nodes)
            
            # 绘制地图（分图层）
            self._draw_enhanced_map(img, analyzed_nodes, layout)
            
            # 添加信息面板
            self._add_info_panel(img, path_memory, analyzed_nodes, total_distance)
            
            # 添加标题
            self._add_title(img, path_memory.path_name)
            
            # 保存地图
            if output_name is None:
                output_name = f"{path_memory.path_id}_enhanced_map.png"
            
            output_path = os.path.join(self.output_dir, output_name)
            cv2.imwrite(output_path, img)
            
            logger.info(f"🗺️ 增强地图已生成: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ 增强地图生成失败: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def _estimate_distance(self, prev_node, current_node) -> float:
        """估算节点间距离"""
        # 从direction字段提取距离
        direction = current_node.get('original', current_node).direction if isinstance(current_node, dict) else current_node.direction
        
        if isinstance(current_node, dict):
            current_node = current_node['original']
        
        if isinstance(prev_node, dict):
            prev_node = prev_node['original']
        
        # 简单提取数字（米）
        import re
        numbers = re.findall(r'(\d+)', direction)
        if numbers:
            return float(numbers[0])
        
        # 默认估算：基于时间或固定值
        return 10.0  # 默认10米
    
    def _extract_facility_info(self, node) -> Dict[str, Any]:
        """提取公共设施信息"""
        label = node.label
        label_lower = label.lower()
        
        facility_info = {}
        
        # 洗手间信息
        if any(kw in label_lower for kw in ["洗手间", "toilet", "卫生间"]):
            facility_info = {
                "type": "restroom",
                "available": True,
                "accessibility": "wheelchair_accessible"
            }
        
        # 电梯信息
        elif any(kw in label_lower for kw in ["电梯", "elevator"]):
            facility_info = {
                "type": "elevator",
                "capacity": "13人",
                "accessibility": "wheelchair_accessible"
            }
        
        # 医院信息
        elif any(kw in label_lower for kw in ["医院", "hospital"]):
            facility_info = {
                "type": "hospital",
                "services": ["emergency", "consultation"],
                "hours": "24小时"
            }
        
        # 商场信息
        elif any(kw in label_lower for kw in ["商场", "mall"]):
            facility_info = {
                "type": "shopping_mall",
                "services": ["shopping", "dining", "parking"],
                "hours": "10:00-22:00"
            }
        
        return facility_info
    
    def _extract_transit_info(self, node) -> Dict[str, Any]:
        """提取公共交通信息"""
        label = node.label
        label_lower = label.lower()
        
        transit_info = {}
        
        # 地铁信息
        if any(kw in label_lower for kw in ["地铁", "subway", "metro"]):
            # 尝试提取线路号
            import re
            line_match = re.search(r'(\d+)', label)
            line_number = line_match.group(1) if line_match else "未知"
            
            transit_info = {
                "type": "subway",
                "line": line_number,
                "status": "operational",
                "frequency": "3-5分钟"
            }
        
        # 公交信息
        elif any(kw in label_lower for kw in ["公交", "bus"]):
            import re
            bus_match = re.search(r'(\d+)', label)
            bus_number = bus_match.group(1) if bus_match else "未知"
            
            transit_info = {
                "type": "bus",
                "route": bus_number,
                "status": "operational",
                "frequency": "5-10分钟"
            }
        
        # 车站信息
        elif "站" in label_lower and ("地铁" in label_lower or "公交" in label_lower):
            transit_info = {
                "type": "station",
                "accessibility": "wheelchair_accessible",
                "services": ["ticket", "info"]
            }
        
        return transit_info
    
    def _calculate_enhanced_layout(self, nodes: List[Dict]) -> Dict[str, Any]:
        """计算增强布局"""
        num_nodes = len(nodes)
        width = self.map_config["width"]
        height = self.map_config["height"]
        
        # 线性布局，预留信息面板空间
        layout = {
            'start_x': 100,
            'start_y': height // 2,
            'end_x': width - 400,  # 预留右侧信息面板
            'end_y': height // 2,
            'spacing': (width - 500) / max(num_nodes, 1),
            'layer_offsets': {
                'outdoor': -50,
                'indoor': 50
            }
        }
        
        return layout
    
    def _draw_enhanced_map(self, img: np.ndarray, nodes: List[Dict], layout: Dict):
        """绘制增强地图"""
        # 按图层分组绘制
        outdoor_nodes = [n for n in nodes if n['layer'] == 'outdoor']
        indoor_nodes = [n for n in nodes if n['layer'] == 'indoor']
        
        # 绘制室外图层
        self._draw_layer(img, outdoor_nodes, layout, 'outdoor')
        
        # 绘制室内图层
        self._draw_layer(img, indoor_nodes, layout, 'indoor')
    
    def _draw_layer(self, img: np.ndarray, nodes: List[Dict], layout: Dict, layer: str):
        """绘制图层"""
        if not nodes:
            return
        
        x_spacing = layout['spacing']
        y_base = layout['start_y'] + layout['layer_offsets'].get(layer, 0)
        
        for i, node in enumerate(nodes):
            x = layout['start_x'] + i * x_spacing
            y = y_base
            
            node_type = node['type']
            color = self.node_colors.get(node_type, (128, 128, 128))
            
            # 绘制节点
            self._draw_node(img, node, x, y, color)
            
            # 绘制连线（除了第一个节点）
            if i > 0:
                self._draw_connection(img, nodes[i-1], node, x - x_spacing, y, x, y)
    
    def _draw_node(self, img: np.ndarray, node: Dict, x: int, y: int, color: Tuple[int, int, int]):
        """绘制节点"""
        # 节点圆圈
        cv2.circle(img, (int(x), int(y)), self.map_config["node_size"], color, -1)
        cv2.circle(img, (int(x), int(y)), self.map_config["node_size"], (255, 255, 255), 3)
        
        # 节点编号
        node_id = len([n for n in node if 'original' in n]) if isinstance(node, list) else 0
        # 这里简化处理，实际应该传递正确的节点索引
        
        # 节点标签
        label = node['original'].label if isinstance(node, dict) else node.label
        label_lines = label.split('（') if '（' in label else [label]
        label_short = label_lines[0]
        
        # 添加距离信息
        if 'distance' in node:
            distance_text = f"{node['distance']:.0f}m"
            cv2.putText(img, distance_text, (int(x-30), int(y-90)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # 节点标签
        cv2.putText(img, label_short, (int(x-80), int(y+100)),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    def _draw_connection(self, img: np.ndarray, from_node: Dict, to_node: Dict, 
                        x1: float, y1: float, x2: float, y2: float):
        """绘制连接线"""
        color = self.node_colors.get(from_node['type'], (128, 128, 128))
        pt1 = (int(x1+self.map_config["node_size"]//2), int(y1))
        pt2 = (int(x2-self.map_config["node_size"]//2), int(y2))
        cv2.arrowedLine(img, pt1, pt2, color, self.map_config["line_width"], tipLength=0.3)
    
    def _add_info_panel(self, img: np.ndarray, path_memory, nodes: List[Dict], total_distance: float):
        """添加信息面板"""
        width = self.map_config["width"]
        panel_x = width - 350
        
        # 信息面板背景
        cv2.rectangle(img, (panel_x, 100), (width-20, self.map_config["height"]-100),
                     (255, 255, 255), -1)
        cv2.rectangle(img, (panel_x, 100), (width-20, self.map_config["height"]-100),
                     (200, 200, 200), 2)
        
        y_offset = 130
        
        # 标题
        cv2.putText(img, "Path Information", (panel_x+10, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        y_offset += 40
        
        # 总距离
        total_text = f"Total: {total_distance:.0f}m"
        cv2.putText(img, total_text, (panel_x+10, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 0), 2)
        y_offset += 40
        
        # 节点统计
        node_counts = {}
        for node in nodes:
            node_type = node['type']
            node_counts[node_type] = node_counts.get(node_type, 0) + 1
        
        for node_type, count in node_counts.items():
            type_text = f"{node_type}: {count}"
            cv2.putText(img, type_text, (panel_x+10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 100, 100), 1)
            y_offset += 30
    
    def _add_title(self, img: np.ndarray, title: str):
        """添加标题"""
        width = self.map_config["width"]
        cv2.putText(img, title, (width//2 - 200, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
    
    def _create_canvas(self) -> np.ndarray:
        """创建画布"""
        width = self.map_config["width"]
        height = self.map_config["height"]
        bg_color = self.map_config["bg_color"]
        
        img = np.ones((height, width, 3), dtype=np.uint8)
        img[:, :] = bg_color
        
        return img


if __name__ == "__main__":
    # 测试增强地图生成器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    from core.scene_memory_system import PathMemory, SceneNode
    
    print("=" * 60)
    print("🗺️  增强地图生成器测试")
    print("=" * 60)
    
    generator = EnhancedMapGenerator()
    
    # 创建测试路径
    nodes = [
        SceneNode("n1", "医院主入口", "", timestamp=datetime.now().isoformat()),
        SceneNode("n2", "电梯厅", "", timestamp=datetime.now().isoformat()),
        SceneNode("n3", "挂号处", "", timestamp=datetime.now().isoformat()),
        SceneNode("n4", "急诊科", "", timestamp=datetime.now().isoformat()),
    ]
    
    path = PathMemory("test", "测试路径", nodes)
    
    # 生成地图
    map_file = generator.generate_enhanced_map_card(path, "test_enhanced.png")
    
    if map_file:
        print(f"✅ 增强地图已生成: {map_file}")
    else:
        print("❌ 地图生成失败")
    
    print("=" * 60)


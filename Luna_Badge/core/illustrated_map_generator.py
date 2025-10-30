#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 插图化地图生成器 v3.0
基于参考地图的手绘插画风格实现

核心特性:
- 丰富的插图元素（建筑物、场景、装饰）
- 多层次信息表达
- 手绘风格的视觉表现
- 实用信息标注
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random

logger = logging.getLogger(__name__)


class IllustratedMapGenerator:
    """插图化地图生成器 v3.0"""
    
    def __init__(self,
                 output_dir: str = "data/map_cards",
                 icons_dir: str = "assets/icons/tabler",
                 fonts_dir: str = "assets/fonts",
                 textures_dir: str = "assets/textures"):
        """初始化生成器"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.icons_dir = icons_dir
        self.fonts_dir = fonts_dir
        self.textures_dir = textures_dir
        
        # 加载字体
        self.font_heading = self._load_chinese_font(size=32)  # 标题大字
        self.font_label = self._load_chinese_font(size=18)    # 标签
        self.font_hint = self._load_chinese_font(size=14)     # 提示小字
        
        # 插图化配色方案（参考地图风格）
        self.colors = {
            "bg": (251, 248, 240),           # 米黄色背景
            "path": (100, 120, 140),         # 路径蓝灰色
            "node": (50, 50, 50),            # 节点深灰
            "region_light": (220, 230, 245),  # 浅蓝区域
            "region_warm": (255, 245, 220),   # 暖黄区域
            "highlight": (255, 100, 100),    # 高亮红
            "text_dark": (30, 30, 30),       # 深色文字
            "text_medium": (100, 100, 100),  # 中等文字
        }
        
        # 插图元素配置
        self.illustration_config = {
            "node_decor": True,              # 节点装饰
            "building_outline": True,        # 建筑轮廓
            "scene_bg": True,                # 场景背景
            "decorative_lines": True,        # 装饰线条
            "info_badges": True,             # 信息徽章
        }
        
        logger.info("🎨 插图化地图生成器 v3.0 初始化完成")
    
    def _load_chinese_font(self, size: int = 16) -> Optional[ImageFont.FreeTypeFont]:
        """加载中文字体"""
        font_paths = [
            os.path.join(self.fonts_dir, "handwriting.ttf"),
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
        
        return ImageFont.load_default()
    
    def _draw_building_outline(self, draw: ImageDraw.Draw, x: int, y: int, node_type: str) -> None:
        """绘制建筑物轮廓装饰"""
        if not self.illustration_config["building_outline"]:
            return
        
        # 根据节点类型绘制不同风格的建筑物轮廓
        if "hospital" in node_type.lower() or "building" in node_type.lower():
            # 绘制简单的建筑立面
            points = [
                (x - 25, y - 15),
                (x - 25, y - 30),
                (x - 15, y - 35),
                (x - 5, y - 32),
                (x + 5, y - 35),
                (x + 15, y - 32),
                (x + 25, y - 35),
                (x + 25, y - 15),
            ]
            # 主轮廓
            draw.polygon(points, outline=(120, 120, 120), width=2)
            # 窗户
            for i in range(3):
                wx = x - 15 + i * 15
                draw.rectangle([wx - 3, y - 25, wx + 3, y - 30], 
                             fill=(180, 200, 220), outline=(100, 120, 140))
        
        elif "entrance" in node_type.lower():
            # 入口门框装饰
            draw.rectangle([x - 30, y - 20, x - 20, y - 10],
                         outline=(120, 100, 80), width=2)
            draw.rectangle([x + 20, y - 20, x + 30, y - 10],
                         outline=(120, 100, 80), width=2)
            # 门楣
            draw.arc([x - 20, y - 15, x + 20, y + 5], 
                    start=180, end=0, fill=(120, 100, 80), width=3)
    
    def _draw_decorative_elements(self, draw: ImageDraw.Draw, x: int, y: int) -> None:
        """绘制装饰元素（光线、装饰线条等）"""
        if not self.illustration_config["decorative_lines"]:
            return
        
        # 随机添加一些装饰性短线
        for _ in range(3):
            dx = random.randint(-20, 20)
            dy = random.randint(-20, 20)
            draw.line([x + dx, y + dy, x + dx + random.randint(5, 15), y + dy],
                     fill=(200, 200, 200), width=1)
    
    def _draw_info_badge(self, draw: ImageDraw.Draw, text: str, position: Tuple[int, int], 
                        color: Tuple[int, int, int]) -> None:
        """绘制信息徽章（距离、时间等）"""
        if not self.illustration_config["info_badges"]:
            return
        
        x, y = position
        
        # 背景圆角矩形
        padding = 6
        bbox = draw.textbbox((0, 0), text, font=self.font_hint)
        w = bbox[2] - bbox[0] + padding * 2
        h = bbox[3] - bbox[1] + padding
        
        # 白色背景
        draw.rounded_rectangle([x - w//2, y, x + w//2, y + h],
                             radius=4, fill=(255, 255, 255, 230), 
                             outline=color, width=2)
        
        # 文字
        draw.text((x - w//2 + padding, y + padding//2), text,
                 font=self.font_hint, fill=self.colors["text_dark"])
    
    def _draw_handdrawn_path(self, draw: ImageDraw.Draw, points: List[Tuple[int, int]],
                            color: Tuple[int, int, int], width: int = 3) -> None:
        """绘制手绘风格路径"""
        if len(points) < 2:
            return
        
        # 添加抖动
        jitter_points = []
        for x, y in points:
            jx = x + random.randint(-2, 2)
            jy = y + random.randint(-2, 2)
            jitter_points.append((jx, jy))
        
        # 绘制路径
        for i in range(len(jitter_points) - 1):
            draw.line([jitter_points[i], jitter_points[i + 1]],
                     fill=color, width=width)
        
        # 添加箭头
        if len(jitter_points) >= 2:
            x1, y1 = jitter_points[-2]
            x2, y2 = jitter_points[-1]
            dx, dy = x2 - x1, y2 - y1
            
            # 箭头三角形
            arrow_len = 12
            angle = np.arctan2(dy, dx)
            arrow_x1 = int(x2 - arrow_len * np.cos(angle - np.pi / 6))
            arrow_y1 = int(y2 - arrow_len * np.sin(angle - np.pi / 6))
            arrow_x2 = int(x2 - arrow_len * np.cos(angle + np.pi / 6))
            arrow_y2 = int(y2 - arrow_len * np.sin(angle + np.pi / 6))
            
            draw.polygon([(x2, y2), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)],
                        fill=color, outline=color)
    
    def _apply_handdrawn_filter(self, img: Image.Image) -> Image.Image:
        """应用手绘风格滤镜"""
        # 轻微的模糊模拟手绘感
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # 增强对比度
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        
        # 轻微的不规则处理
        width, height = img.size
        noise = np.random.randint(-3, 4, (height, width, 3), dtype=np.int16)
        img_array = np.array(img, dtype=np.int16)
        img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        
        return Image.fromarray(img_array)
    
    def generate_illustrated_map(self, path_data: Dict, output_name: str) -> Optional[str]:
        """
        生成插图化风格地图
        
        Args:
            path_data: 路径数据
            output_name: 输出文件名
            
        Returns:
            生成的文件路径
        """
        try:
            # 创建画布
            width, height = 2400, 1800
            img = Image.new('RGB', (width, height), self.colors["bg"])
            draw = ImageDraw.Draw(img)
            
            nodes = path_data.get("nodes", [])
            if not nodes:
                logger.error("无节点数据")
                return None
            
            # 计算节点位置
            positions = self._calculate_positions(nodes, width, height)
            
            # 绘制区域背景
            self._draw_regions(draw, nodes, positions, width, height)
            
            # 绘制路径
            self._draw_paths(draw, nodes, positions)
            
            # 绘制节点和装饰
            for i, (node, pos) in enumerate(zip(nodes, positions)):
                self._draw_node_with_illustration(draw, node, pos, i + 1)
            
            # 绘制指南针
            self._draw_compass(draw, width - 120, 120)
            
            # 应用手绘滤镜
            img = self._apply_handdrawn_filter(img)
            
            # 保存
            output_path = self.output_dir / f"{output_name}_illustrated.png"
            img.save(output_path)
            
            logger.info(f"✅ 插图化地图已生成: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ 生成失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _calculate_positions(self, nodes: List[Dict], width: int, height: int) -> List[Tuple[int, int]]:
        """计算节点位置"""
        num_nodes = len(nodes)
        center_x, center_y = width // 2, height // 2
        radius = 300
        angle_step = 360 / num_nodes if num_nodes > 0 else 0
        
        positions = []
        for i in range(num_nodes):
            angle = np.radians(i * angle_step)
            x = int(center_x + radius * np.cos(angle))
            y = int(center_y + radius * np.sin(angle))
            positions.append((x, y))
        
        return positions
    
    def _draw_regions(self, draw: ImageDraw.Draw, nodes: List[Dict], 
                     positions: List[Tuple[int, int]], width: int, height: int) -> None:
        """绘制区域背景"""
        # 简化的区域绘制
        for i, node in enumerate(nodes):
            level = node.get("level", "")
            if level and i < len(positions):
                x, y = positions[i]
                # 绘制圆形区域
                draw.ellipse([x - 150, y - 150, x + 150, y + 150],
                           fill=self.colors["region_light"], 
                           outline=(180, 190, 200), width=2)
    
    def _draw_paths(self, draw: ImageDraw.Draw, nodes: List[Dict], 
                   positions: List[Tuple[int, int]]) -> None:
        """绘制路径"""
        for i in range(len(nodes) - 1):
            from_pos = positions[i]
            to_pos = positions[i + 1]
            
            # 使用手绘路径
            self._draw_handdrawn_path(draw, [from_pos, to_pos], 
                                     self.colors["path"], width=4)
            
            # 添加距离标注
            distance = nodes[i].get("distance", 0)
            if distance > 0:
                mid_x = (from_pos[0] + to_pos[0]) // 2
                mid_y = (from_pos[1] + to_pos[1]) // 2
                self._draw_info_badge(draw, f"{distance}米", 
                                     (mid_x, mid_y - 20),
                                     self.colors["path"])
    
    def _draw_node_with_illustration(self, draw: ImageDraw.Draw, node: Dict, 
                                    position: Tuple[int, int], index: int) -> None:
        """绘制带插图的节点"""
        x, y = position
        node_type = node.get("type", "").lower()
        label = node.get("label", "")
        
        # 绘制建筑物轮廓装饰
        self._draw_building_outline(draw, x, y, node_type)
        
        # 绘制节点圆圈（更大）
        draw.ellipse([x - 40, y - 40, x + 40, y + 40],
                   fill=(255, 255, 255), 
                   outline=self.colors["node"], width=4)
        
        # 绘制编号
        draw.text((x - 8, y - 12), str(index),
                 font=self.font_label, fill=self.colors["node"])
        
        # 绘制标签（更大更醒目）
        if label and self.font_label:
            bbox = draw.textbbox((0, 0), label, font=self.font_label)
            text_width = bbox[2] - bbox[0]
            
            # 标签背景
            draw.rounded_rectangle(
                [x - text_width//2 - 10, y + 60,
                 x + text_width//2 + 10, y + 85],
                radius=6,
                fill=(255, 255, 255, 240),
                outline=(180, 180, 180),
                width=2
            )
            
            # 标签文字
            draw.text((x - text_width//2, y + 70),
                     label,
                     font=self.font_label,
                     fill=self.colors["text_dark"])
        
        # 绘制装饰元素
        self._draw_decorative_elements(draw, x, y)
        
        # 绘制情绪标签
        emotions = node.get("emotion", [])
        if emotions and isinstance(emotions, list):
            for idx, emotion in enumerate(emotions[:2]):
                self._draw_emotion_badge(draw, emotion, 
                                       (x + 60 + idx * 55, y))
    
    def _draw_emotion_badge(self, draw: ImageDraw.Draw, emotion: str, 
                           position: Tuple[int, int]) -> None:
        """绘制情绪徽章"""
        x, y = position
        
        # 情绪配色
        emotion_colors = {
            "推荐": (255, 182, 193),
            "安静": (144, 238, 144),
            "担忧": (255, 165, 0),
            "嘈杂": (169, 169, 169),
        }
        
        color = emotion_colors.get(emotion, (200, 200, 200))
        
        # 绘制徽章
        draw.ellipse([x - 20, y - 20, x + 20, y + 20],
                   fill=color, outline=(220, 220, 220), width=2)
        
        # 文字
        if self.font_hint:
            bbox = draw.textbbox((0, 0), emotion, font=self.font_hint)
            text_x = x - (bbox[2] - bbox[0]) // 2
            text_y = y - (bbox[3] - bbox[1]) // 2
            draw.text((text_x, text_y), emotion,
                     font=self.font_hint, fill=(255, 255, 255))
    
    def _draw_compass(self, draw: ImageDraw.Draw, x: int, y: int) -> None:
        """绘制指南针"""
        size = 60
        
        # 外圆
        draw.ellipse([x - size, y - size, x + size, y + size],
                   outline=(100, 100, 100), width=2)
        
        # 方向标记
        for direction, offset, color in [
            ("N", (0, -size + 10), (255, 0, 0)),
            ("S", (0, size - 10), (0, 0, 255)),
            ("E", (size - 10, 0), (0, 255, 0)),
            ("W", (-size + 10, 0), (255, 165, 0)),
        ]:
            px, py = x + offset[0], y + offset[1]
            if self.font_hint:
                bbox = draw.textbbox((0, 0), direction, font=self.font_hint)
                text_x = px - (bbox[2] - bbox[0]) // 2
                text_y = py - (bbox[3] - bbox[1]) // 2
                draw.text((text_x, text_y), direction,
                         font=self.font_hint, fill=color)


def main():
    """测试函数"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # 测试数据
    test_path = {
        "path_id": "hospital_test",
        "path_name": "医院导航路径",
        "nodes": [
            {"type": "entrance", "label": "医院入口", "emotion": ["明亮"], "distance": 0},
            {"type": "registration", "label": "挂号处", "emotion": ["推荐", "明亮"], "distance": 20},
            {"type": "elevator", "label": "电梯", "emotion": ["嘈杂", "推荐"], "distance": 15},
            {"type": "waiting_room", "label": "候诊区", "emotion": ["安静"], "distance": 20},
            {"type": "toilet", "label": "卫生间", "emotion": ["安静", "推荐"], "distance": 10},
            {"type": "destination", "label": "诊室", "emotion": ["推荐"], "distance": 5},
        ]
    }
    
    generator = IllustratedMapGenerator()
    result = generator.generate_illustrated_map(test_path, "test_illustrated")
    
    if result:
        print(f"✅ 生成成功: {result}")


if __name__ == "__main__":
    main()
